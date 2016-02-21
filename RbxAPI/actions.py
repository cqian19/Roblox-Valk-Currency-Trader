from PySide import QtCore
from lxml import html
from requests.packages.urllib3.util import Retry
from requests_futures.sessions import FuturesSession
from functools import wraps
from .rbx_data import data, LOGIN_URL, TC_URL
from .errors import *
from .trade_log import Trade
from .utils import round_down, round_up, to_num, find_data_file, profile

import time
import logging
import math
import requests
import os
import sys


logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s -%(levelname)s %(funcName)s %(message)s  %(module)s: <Line %(lineno)s>"
)

# Enable For Debugging:
logging.disable(logging.INFO)

delay = .05  # Second delay between calculating trades.
rgap = .005 # Max gap before cancelling a robux split trade
tgap = .0025 # Max gap before cancelling a tix split trade
reset_time = 200 # Number of seconds the bot goes without trading before resetting last rates to be able to trade again (might result in loss)

# Initializing requests.Session for frozen application
cacertpath = find_data_file('cacert.pem')
os.environ["REQUESTS_CA_BUNDLE"] = cacertpath
session = requests.Session()
session.mount("http://", requests.adapters.HTTPAdapter(max_retries=Retry(total=20,connect=10,read=10,backoff_factor=.5)))
session.mount("https://", requests.adapters.HTTPAdapter(max_retries=Retry(total=20,connect=10,read=10,backoff_factor=.3)))
session = FuturesSession(session=session, max_workers=15)

# Storing variables since they can't be stored in QObject
class RateHandler():
    last_tix_rate = 0.0
    last_robux_rate = 0.0
    current_tix_rate = 0.0
    current_robux_rate = 0.0
rates = RateHandler # Ghetto

class Trader(QtCore.QObject):


    def __init__(self, currency):
        QtCore.QObject.__init__(self)
        self.started = False
        self.currency = currency
        self._current_trade = None
        self.last_tree = None
        self.last_trade_time = time.time()
        self.rate_updated = False
        self.trade_payload = {
            data['give_type']: self.currency,
            data['receive_type']: self.other_currency,
            data['limit_order']: 'LimitOrderRadioButton',
            data['split_trades']: '',
            '__EVENTTARGET': data['submit_trade_button'],
        }
        self.config = {
            'split_trades': '',
            'trade_all': False,
            'amount': 0,
            'early_cancel': True
        }

    @property
    def current_trade(self):
        return self._current_trade

    @current_trade.setter
    def current_trade(self, value):
        old_trade = self._current_trade
        self._current_trade = value
        if self.my_trader.holds_top_trade:
            self.my_trader.holds_top_trade = False
        if old_trade:
            self.trade_log.complete_trade(old_trade)
        if self.rate_updated:
            self.rate_updated = False

    def set_config(self, option, value):
        self.config[option] = value
        # Redo trades with new configuration
        if self.started:
            self.cancel_trades()

    def refresh(self):
        r = session.get(TC_URL).result()
        self.last_tree = html.fromstring(r.text)

    def get_raw_data(self, d, unpack=True):
        tree = self.last_tree
        data = tree.xpath(d)
        if len(data) == 1 and unpack:
            return data[0]
        return data

    def get_auth_tools(self):
        # VIEWSTATE and EVENTVALIDATION must be from the same session
        vsd = self.get_raw_data(data['VIEWSTATE'])
        evd = self.get_raw_data(data['EVENTVALIDATION'])
        if vsd == [] or evd == []:
            raise requests.exceptions.ConnectionError
        viewstate = vsd.attrib['value']
        eventvalidation = evd.attrib['value']
        return viewstate, eventvalidation

    def get_tolerance(self, amount):
        """A magical method that determines the minimum % (in decimal) to trade"""
        if amount//10 == 0:
            return .9
        return min(.9 + .015*math.floor(math.log(amount//10, 10)), .975)

    def get_spread(self):
        spread = self.get_raw_data(data['spread'])
        return float(spread)

    def get_trade_remainder(self, index=1):
        """Gets remainder of our trade at index (Starting at index = 1)"""
        rem_str = self.get_raw_data(data[self.currency]['trade_remainder'](index))
        if rem_str:
            return to_num(rem_str)
        return 0

    def get_currency(self):
        currency = self.get_raw_data(data[self.currency]['current'])
        amount = to_num(currency)
        return amount

    def get_rates(self):
        rates = self.get_raw_data(data['rates'])
        tix_rates, robux_rates = rates.split('/')
        return float(tix_rates), float(robux_rates)

    def get_currency_rate(self, currency=None):
        """Rate from currency to the other currency"""
        if currency is None:
            currency = self.currency
        if currency == 'Tickets':
            return self.get_rates()[0]
        return self.get_rates()[1]

    def get_other_rate(self):
        return self.get_currency_rate(self.other_currency)

    def get_other_next_rate(self):
        """Returns the rate of the second top trade in the category of the other currency"""
        return self.other_trader.get_available_trade_info(self, 2)[1]

    def get_trade_count(self):
        trades = list(self.get_raw_data(data[self.currency]['open_trades'], False))
        trade_count = len(trades)
        return trade_count

    def get_trade_info(self, index):
        """Gets the trade info starting from the top (index = 0)"""
        return self.get_available_trade_info(index)

    # All lambda data functions starts at index 1
    def get_ith_trade_amount(self, index):
        return self.get_trade_info(index)[0]

    def get_ith_trade_rate(self, index):
        return self.get_trade_info(index)[1]

    def get_ith_trade_path(self, index, currency=None):
        if not currency:
            currency = self.currency
        return data[currency]['trade_info_path'](index)

    def get_ith_cancel_bid(self, index):
        return data[self.currency]['cancel_bid'](index)

    def get_amount_to_trade(self):
        our_money = self.get_currency()
        if self.config['trade_all']:
            if self.check_trades():
                remainder = self.get_trade_remainder()
                amount = our_money + remainder
            else:
                amount = our_money
        else:
            amount = self.config['amount']
            if not amount or amount > our_money + self.get_trade_remainder():
                raise NoMoneyError(self.currency)
        return amount

    def get_threshold_rate(self):
        """Gets the worst possible rate to trade at, so we don't go beyond it"""
        spread = self.get_spread()
        other_top_rate, other_second_top_rate = self.get_other_rate(), self.get_other_next_rate()
        if self.holds_top_trade:
            other_threshold_rate = other_top_rate
        elif spread >= 0:
            other_threshold_rate = other_top_rate
        else:
            if self.other_trader.holds_top_trade:
                # The spread is forcibly negative due to your split trade
                # In this case, get the second highest trade rate of the other currency.
                other_threshold_rate = other_second_top_rate
            else:
                if self.current_trade: # A better rate exists on our currency and goes below spread
                    other_threshold_rate = other_top_rate # Use the top rate on the other currency, since our trade may be the 2nd best
                else: # No trades exist and spread is negative. Match the second best trade in this category.
                    other_threshold_rate = other_second_top_rate
        return other_threshold_rate

    def check_trades(self):
        """Returns True if a trade is still active"""
        return self.get_raw_data(data[self.currency]['trades']) == []

    def check_bot_stopped(func):
        """Decorator that checks if bot has been stopped by user"""
        @wraps(func)
        def raise_if_stopped(inst, *args, **kwargs):
            if not inst.started:
                raise BotStoppedError
            return func(inst, *args, **kwargs)
        return raise_if_stopped

    @check_bot_stopped
    def calculate_trade(self, amount):
        """Determines which rate to match."""
        spread = self.get_spread()
        this_top_rate, second_top_rate, third_top_rate = (self.get_ith_trade_rate(i) for i in range(1, 4))
        # Check if our trade is top trade
        if self.holds_top_trade:
            rate, next_rate = second_top_rate, third_top_rate
        else:
            rate, next_rate = this_top_rate, second_top_rate
            if spread > 10000 or spread < -10000:
                raise BadSpreadError
            if this_top_rate <= 10:
                raise LowRateError
        other_threshold_rate = self.get_threshold_rate()
        #Trade at top rate
        #If that doesn't work, try trading at the second top rate instead
        try:
            return self.balance_rate(amount, rate, this_top_rate, other_threshold_rate)
        except (WorseRateError, BadSpreadError, TradeGapError) as e:
            # If the second rate is our rate, raise an error
            if self.current_trade and not self.holds_top_trade:
                our_amount = self.get_trade_remainder()
                # Check if trade has not gone through on Roblox's server
                if our_amount == 0 or self.get_ith_trade_amount(2) == our_amount:
                    raise OurTradeError
            return self.balance_rate(amount, next_rate, this_top_rate, other_threshold_rate)

    @check_bot_stopped
    def submit_trade(self, amount_to_give, amount_to_receive):
        vs, ev = self.get_auth_tools()
        self.trade_payload[data['split_trades']] = self.config['split_trades']
        self.trade_payload[data['give_box']] = str(amount_to_give)
        self.trade_payload[data['receive_box']] = str(amount_to_receive)
        self.trade_payload['__EVENTVALIDATION'] = ev
        self.trade_payload['__VIEWSTATE'] = vs
        session.post(TC_URL, data=self.trade_payload)

    def cancel_trades(self):
        """Cancels all existing trades. Useful if we accidentally submit multiple trades due to server lag."""
        trade_count = self.get_trade_count()
        if self.current_trade:
            self.update_current_trade()
            self.current_trade = None
        for i in range(trade_count, 0, -1):
            payload = {
                '__EVENTTARGET': self.get_ith_cancel_bid(i)
            }
            #Cancelling top trade ()
            vs, ev = self.get_auth_tools()
            payload['__EVENTVALIDATION'] = ev
            payload['__VIEWSTATE'] = vs
            session.post(TC_URL, data=payload)
        if self.currency == 'Tickets':
            rates.current_tix_rate = 0
        else:
            rates.current_robux_rate = 0

    def cancel_other_trades(self):
        """Cancels all trades except the current trade"""
        if self.current_trade:
            trade_count = self.get_trade_count()
            detected = False
            for i in range(trade_count, 0, -1):
                payload = {
                    '__EVENTTARGET': self.get_ith_cancel_bid(i)
                }
                remainder = self.get_trade_remainder(i)
                if self.get_trade_remainder(i) != self.current_trade.remaining1 or detected:
                    vs, ev = self.get_auth_tools()
                    payload['__EVENTVALIDATION'] = ev
                    payload['__VIEWSTATE'] = vs
                    session.post(TC_URL, data=payload)
                else:
                    detected = True
        else:
            self.cancel_trades()

    def check_no_recent_trades(self):
        """If the trader hasn't traded in a while, reset both rates so the bot 
        could possibly trade at a worse rate but gain in the long run."""
        now = time.time()
        if now - self.last_trade_time > reset_time:
            if not self.my_trader.holds_top_trade:
                print('No recent')
                self.last_trade_time = now
                rates.last_tix_rate = 0
                rates.last_robux_rate = 0
            else:
                self.last_trade_time = now

    def do_trade(self):
        amount = self.get_amount_to_trade()
        to_trade, receive, rate = self.calculate_trade(amount)
        if self.check_trades():
            self.cancel_trades()
        self.submit_trade(to_trade, receive)

        rates.current_robux_rate = rate

        new_trade = Trade(to_trade, receive, self.currency, self.other_currency, rate)
        self.current_trade = new_trade
        self.trade_log.add_trade(new_trade)

    # Uncomment below for testing speed/optimization
    # @profile
    def start(self):
        self.started = True
        while self.started:
            time.sleep(delay)
            try:
                self.refresh()
                self.check_no_recent_trades()
                if not self.check_trades():
                    if self.current_trade:
                        if self.fully_complete_trade():
                            self.do_trade()
                    else:
                        self.do_trade()
                elif self.get_trade_count() > 1: #Lag error? Better clean it up.
                    self.cancel_other_trades()
                elif self.current_trade:
                    if self.check_better_rate():
                        self.do_trade()
                    else:
                        self.check_trade_gap()
                else:
                    self.cancel_trades()
            except BotStoppedError:
                break
            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                print(e)
                print("Connection interrupted")
                raise e
            except (WorseRateError, LowRateError, BadSpreadError, MarketTraderError,
                    TradeGapError,  NoMoneyError, OurTradeError, ZeroDivisionError) as e:
                logging.debug(e)
            except Exception as e:
                logging.error(e)
                raise e
        self.cancel_trades()

    def stop(self):
        self.started = False
        print("Stopping trades.")
        self.cancel_trades()


class TixTrader(Trader):

    """Trades from tix to robux"""
    holds_top_trade = False
    currency = 'Tickets'
    other_currency = 'Robux'
   

    def __init__(self, trade_log):
        super().__init__(self.currency)
        self.trade_log = trade_log
        self.my_trader = TixTrader
        self.other_trader = RobuxTrader

    def get_available_trade_info(self, i):
        """Parses the trade information string of the ith trade from the available tix column"""
        # Format: '\r\n (bunch of spaces) Tix @ rate:1\r\n (bunch of spaces)'
        trade_info = self.get_ith_trade_path(i, 'Tickets')
        info = self.get_raw_data(trade_info) # May be None if connection is reset
        if not info:
            raise requests.exceptions.ConnectionError
        rate_split = [x for x in info.split(' ') if x and x[0].isdigit()]
        # If the trader is @ Market
        if len(rate_split) <= 1:
            print("ERROR", rate_split, i)
            raise MarketTraderError
        tix, all_rate = to_num(rate_split[0]), rate_split[1]
        rate = float(all_rate.split(':')[0])
        return tix, rate

    def update_current_trade(self, amount_remain=None, top_rate=None):
        """If a current trade is active, update its information for the trade log."""
        logging.info('Updating trade')
        if amount_remain is None:
            amount_remain = self.get_trade_remainder()
        if amount_remain and self.current_trade:
            if amount_remain < self.current_trade.remaining1:
                if not self.rate_updated:
                    start_rate = self.current_trade.start_rate
                    rates.last_tix_rate = max(start_rate, rates.last_tix_rate)
                    self.rate_updated = True
                    self.last_trade_time = time.time()
                self.current_trade.update(amount_remain, top_rate)
                rates.current_tix_rate = self.current_trade.current_rate
        elif self.current_trade:  #  Trade is complete.
            self.fully_complete_trade()

    def check_trade_gap(self):
        if self.config['early_cancel'] and self.current_trade and self.holds_top_trade:
            next_rate = self.get_ith_trade_rate(2)
            startdiff = self.current_trade.current_rate - self.current_trade.start_rate
            ntdiff = self.current_trade.current_rate - next_rate
            #if self.current_trade.amount1 == self.current_trade.remaining1:
            if startdiff >= tgap - .00001 or ntdiff >= tgap - .00001: # Float stuff
                self.do_trade()

    def check_better_rate(self):
        """Check if a better rate for tix to robux exists, updates the GUI if our trade is top"""
        our_tix = self.get_trade_remainder()
        top_tix, top_rate = self.get_trade_info(1)
        # Check if the top trade is not our trade
        if our_tix and our_tix != top_tix:
            self.update_current_trade(our_tix) # Update the remaining tix first
            TixTrader.holds_top_trade = False
            if top_rate < rates.last_robux_rate:
                return True
            elif rates.current_tix_rate and top_rate > round_down(rates.current_tix_rate):
                return True
            elif not rates.last_robux_rate and not rates.current_robux_rate and top_rate < self.get_other_rate():
                return True
        elif our_tix:
            TixTrader.holds_top_trade = True
            self.update_current_trade(our_tix, top_rate)
        return False

    def test_rate(self, rate, this_top_rate, threshold_rate):
        """Tests if the rate is better than the last rate"""
        last_rate = rates.last_robux_rate
        logging.debug("Last robux rate: ", str(last_rate))
        if rate - this_top_rate >= tgap - .00001:
            raise TradeGapError
        if last_rate and rate >= round_up(last_rate): # Rounding up may cause loss at up to 4th decimal point
            raise WorseRateError(self.currency, self.other_currency, rate, last_rate)
        elif not last_rate:
            if not threshold_rate:
                raise BadSpreadError
            if round_down(rate) > threshold_rate:
                raise WorseRateError(self.currency, self.other_currency, rate, threshold_rate)

    def balance_rate(self, amount, rate, this_top_rate, threshold_rate):
        """Gives a trade amount nearest the exact rate, with the highest 4th decimal place and the corresponding robux to receive"""
        x, best_x = amount, 0
        closest_within_rate, closest_outside_rate = 0, sys.maxsize
        # Trade within .001 of the top rate, or lower if the last robux rate is within .001 of this tix rate
        # Add tolerance check
        tolerance = self.get_tolerance(amount)# Lowest % to trade
        while x > tolerance*amount:
            diff = x/math.floor(x/rate) - rate # Difference between our actual rate and top tix rate.
            if diff < .001:
                if diff > closest_within_rate:
                    closest_within_rate = diff
                    best_x = x
            elif not closest_within_rate and diff < closest_outside_rate: # diff >= .001
                closest_outside_rate = diff
                best_x = x
            x -= 1
        to_trade, receive = best_x, math.floor(best_x/rate)
        actual_rate = to_trade/receive
        self.test_rate(actual_rate, this_top_rate, threshold_rate)
        return to_trade, receive, actual_rate

    def fully_complete_trade(self):
        completed_trade = self.current_trade
        if completed_trade and time.time() - self.last_trade_time > 1: # Trades can be incorrectly completed due to Roblox's time to process a trade
            completed_trade.update(0)
            rates.last_tix_rate = max(completed_trade.start_rate, rates.last_tix_rate)
            rates.current_tix_rate = 0
            self.current_trade = None
            return True
        return False

class RobuxTrader(Trader):
    """Trades from robux to tix"""

    holds_top_trade = False
    currency = 'Robux'
    other_currency = 'Tickets'
   

    def __init__(self, trade_log):
        super().__init__(self.currency)
        self.trade_log = trade_log
        self.my_trader = RobuxTrader
        self.other_trader = TixTrader

    def update_current_trade(self, amount_remain=None, top_rate=None):
        """If a current trade is active, update its information for the trade log."""
        if amount_remain is None:
            amount_remain = self.get_trade_remainder()
        if amount_remain and self.current_trade:
            if amount_remain < self.current_trade.remaining1:
                if not self.rate_updated:
                    start_rate = self.current_trade.start_rate 
                    if rates.last_robux_rate:
                        rates.last_robux_rate = min(start_rate, rates.last_robux_rate)
                    else:
                        rates.last_robux_rate = start_rate
                    self.rate_updated = True
                    self.last_trade_time = time.time()
                self.current_trade.update(amount_remain, top_rate)
                rates.current_robux_rate = self.current_trade.current_rate
        elif self.current_trade:
            self.fully_complete_trade()

    def check_at_market(self):
        """Checks if the top robux trade is @ Market"""
        trade_info_path = self.get_ith_trade_path(1, 'Robux') # Gets top robux trade xpath
        #Format ['\r\n (bunch of spaces)', ' @ 1:rate\r\n'] Second part is rate info
        trade_info = self.get_raw_data(trade_info_path[1])
        if not len(trade_info):
            raise requests.exceptions.ConnectionError
        rate_info = trade_info[1]
        return 'Market' in rate_info

    def get_available_trade_info(self, i):
        """Parses the trade information string of the ith trade in the available robux column"""
        if RobuxTrader.check_at_market(self): # Top trade is @ Market, real info is at index + 1
            i += 1

        trade_info = self.get_ith_trade_path(i, 'Robux')
        amount_info = self.get_raw_data(trade_info[0])
        # Format ['\r\n (bunch of spaces)', ' @ 1:rate\r\n']
        rate_info = self.get_raw_data(trade_info[1])
        if not amount_info or not rate_info:
            raise requests.exceptions.ConnectionError
        robux = to_num(amount_info)
        # Gets the 1:rate\r\n part
        all_rate = [x for x in rate_info[1].split(' ') if x and x[0].isdigit()]
        # Gets the rate part
        rate = (all_rate[0].split(':')[1]).split('\\')[0]
        rate = float(rate)
        return robux, rate

    def check_trade_gap(self):
        """Check if our rate is far higher than the next rate."""
        if self.config['early_cancel'] and self.current_trade and self.holds_top_trade:
            # Get the second highest trade's info
            next_rate = self.get_ith_trade_rate(2)
            startdiff = self.current_trade.start_rate - self.current_trade.current_rate
            ntdiff = next_rate - self.current_trade.current_rate
            #if self.current_trade.amount1 == self.current_trade.remaining1:
            if startdiff >= rgap - .000001 or ntdiff >= rgap - .000001: # Float stuff
                self.do_trade()

    def check_better_rate(self):
        """Check if a better rate for robux to tix exists"""
        # See rbx_data since this one is weird.
        our_robux = self.get_trade_remainder()
        top_robux, top_rate = self.get_trade_info(1)
        # Check if the top trade is not our trade
        if our_robux and our_robux != top_robux:
            self.update_current_trade(our_robux)
            RobuxTrader.holds_top_trade = False
            if rates.last_tix_rate and top_rate > rates.last_tix_rate:
                return True
            elif rates.current_robux_rate and top_rate < round_down(rates.current_robux_rate):
                return True
            elif not rates.last_tix_rate and not rates.current_tix_rate and top_rate > self.get_other_rate():
                return True
        elif our_robux is not None:
            RobuxTrader.holds_top_trade = True
            self.update_current_trade(our_robux, top_rate)
        return False

    def test_rate(self, rate, this_top_rate, threshold_rate):
        """Verifies that this is a better and profit making rate to trade at"""
        last_rate = rates.last_tix_rate
        logging.debug("Last tix rate: ", str(last_rate))
        if not self.holds_top_trade and this_top_rate - rate >= rgap:
            raise TradeGapError
        if last_rate and rate < round_down(last_rate): # IMPORTANT!: This potentially leads to trading at loss, but relies on early split trade cancelling.
            raise WorseRateError(self.currency, self.other_currency, rate, last_rate)
        elif not last_rate:
            if not threshold_rate:
                raise BadSpreadError
            if round_down(rate) < threshold_rate:
                raise WorseRateError(self.currency, self.other_currency, rate, threshold_rate)

    def balance_rate(self, amount, rate, this_top_rate, threshold_rate):
        """Gives a trade amount nearest the exact rate, and the corresponding tix to receive"""
        x, closest, best_x = amount, sys.maxsize, 0
        # Trade within .001 of top rate, or lower if the last tix rate is within .001 of top rate
        tolerance = self.get_tolerance(amount)
        while x > tolerance*amount:
            diff = math.ceil(x*rate)/x - rate # Difference between top trade rate and actual rate
            if diff < closest and diff >= 0:
                closest = diff
                best_x = x
            x -= 1
        to_trade, receive = best_x, math.floor(best_x*rate)
        actual_rate = receive/to_trade
        self.test_rate(actual_rate, this_top_rate, threshold_rate)
        return to_trade, receive, actual_rate

    def fully_complete_trade(self):
        completed_trade = self.current_trade
        if completed_trade and time.time() - self.last_trade_time > 1: # Trades can be incorrectly completed due to Roblox's time to process a trade
            completed_trade.update(0)
            if rates.last_robux_rate:
                rates.last_robux_rate = min(completed_trade.start_rate, rates.last_robux_rate)
            else:
                rates.last_robux_rate = completed_trade.start_rate
            rates.current_robux_rate = 0
            self.current_trade = None
            return True
        return False

def test_login(user, pw):
    payload = {
        'username': user,
        'password': pw,
    }
    r = session.post(LOGIN_URL, payload).result()
    if r.url == LOGIN_URL:
        raise LoginError
