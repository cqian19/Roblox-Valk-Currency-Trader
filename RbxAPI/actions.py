from PySide import QtCore
from lxml import html
from .rbx_data import data
from .errors import *
from .trade_log import Trade
from .utils import round_down, round_up, to_num, find_data_file

import time
import logging
import math
import requests
import os
import sys

LOGIN_URL = 'https://www.roblox.com/newlogin'
TC_URL = 'http://www.roblox.com/My/Money.aspx#/#TradeCurrency_tab'

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s -%(levelname)s %(funcName)s %(message)s  %(module)s: <Line %(lineno)s>"
)
# Disable For Debugging:
logging.disable(logging.CRITICAL)

delay = .15  # Second delay between calculating trades.
gap = .015 # Maximum gap between our rate and next to top rate permitted (Lower gap = more safety)
reset_time = 300 # Number of seconds the bot goes without trading before resetting last rates to be able to trade again (might result in loss)

# Initializing requests.Session for frozen application
cacertpath = find_data_file('cacert.pem')
os.environ["REQUESTS_CA_BUNDLE"] = cacertpath
session = requests.Session()


class Trader(QtCore.QObject):

    last_tix_rate = 0
    last_robux_rate = 0
    current_tix_rate = 0
    current_robux_rate = 0

    def __init__(self, currency):
        QtCore.QObject.__init__(self)
        self.started = False
        self.currency = currency
        self._current_trade = None
        self.last_tree = None
        self.last_trade_time = time.time()
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
            'amount': 0
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

    def set_config(self, option, value):
        self.config[option] = value
        # Redo trades with new configuration
        if self.started:
            self.cancel_trades()

    def refresh(self):
        r = session.get(TC_URL)
        self.last_tree = html.fromstring(r.text)

    def get_raw_data(self, d):
        tree = self.last_tree
        data = tree.xpath(d)
        if len(data) == 1:
            return data[0]
        return data

    def get_auth_tools(self):
        # VIEWSTATE and EVENTVALIDATION must be from the same session
        viewstate = self.get_raw_data('//input[@name="__VIEWSTATE"]').attrib['value']
        eventvalidation = self.get_raw_data('//input[@name="__EVENTVALIDATION"]').attrib['value']
        return viewstate, eventvalidation

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

    def get_spread(self):
        spread = self.get_raw_data(data['spread'])
        return float(spread)

    def get_tolerance(self, amount):
        """A magical method that determines the minimum % (in decimal) to trade"""
        if amount//10 == 0:
            return .9
        return min(.9 + .025*math.floor(math.log(amount//10, 10)), .975)

    def get_trade_remainder(self):
        rem_str = self.get_raw_data(data[self.currency]['trade_remainder'])
        if rem_str:
            return to_num(rem_str)

    def check_trades(self):
        """Returns True if a trade is still active"""
        return self.get_raw_data(data[self.currency]['trades']) == []
            
    def cancel_trades(self):
        payload = {
            '__EVENTTARGET': data[self.currency]['cancel_bid']
        }
        if self.current_trade:
            self.update_current_trade()
            self.current_trade = None
        #Cancelling top trade ()
        vs, ev = self.get_auth_tools()
        payload['__EVENTVALIDATION'] = ev
        payload['__VIEWSTATE'] = vs
        session.post(TC_URL, data=payload)
        if self.currency == 'Tickets':
            Trader.current_tix_rate = 0
        else:
            Trader.current_robux_rate = 0

    def calculate_trade(self, amount):
        """Determines which rate to match."""
        spread, this_top_rate, other_top_rate = self.get_spread(), self.get_currency_rate(), self.get_other_rate()
        top_rate = 0
        if spread > 10000 or spread < -10000:
            raise BadSpreadError
        if this_top_rate <= 10 or other_top_rate <= 10:
            raise LowRateError
        if spread >= 0:
            rate = this_top_rate
            other_threshold_rate = other_top_rate
        elif self.other_trader.holds_top_trade:
            # The spread is forcibly negative due to your split trade
            # In this case, get the second highest trade rate of the other currency.
            rate = this_top_rate
            other_threshold_rate = self.other_trader.get_available_trade_info(self, data[self.other_currency]['next_trade_info'])[1]
            print("I hold the top trade", rate , other_threshold_rate)
        else:
            # Otherwise get the second best trade in this category.
            rate = self.get_available_trade_info(data[self.currency]['next_trade_info'])[1]
            other_threshold_rate = other_top_rate
            print("I don't hold the top trade", rate)
        return self.balance_rate(amount, rate, this_top_rate, other_threshold_rate)

    def submit_trade(self, amount_to_give, amount_to_receive):
        self.last_trade_time = time.time()
        vs, ev = self.get_auth_tools()
        self.trade_payload[data['split_trades']] = self.config['split_trades']
        self.trade_payload[data['give_box']] = str(amount_to_give)
        self.trade_payload[data['receive_box']] = str(amount_to_receive)
        self.trade_payload['__EVENTVALIDATION'] = ev
        self.trade_payload['__VIEWSTATE'] = vs
        session.post(TC_URL, data=self.trade_payload)

    def check_bot_stopped(self):
        if not self.started:
            raise BotStoppedError

    def start(self):
        self.started = True
        while self.started:
            time.sleep(delay)
            try:
                self.refresh()
                self.check_no_recent_trades()
                if not self.check_trades():
                    if self.current_trade: # BUG: Post requests may not register yet on Roblox's server
                        self.fully_complete_trade()
                    self.do_trade()
                elif self.current_trade:
                    if self.check_better_rate():
                        self.do_trade()
                    else:
                        self.check_current_worse_trade()
                        self.check_trade_gap()
                else:
                    self.cancel_trades()
            except BotStoppedError:
                break
            except (WorseRateError, LowRateError, BadSpreadError, MarketTraderError, TradeGapError) as e:
                logging.debug(e)
            except (ZeroDivisionError, NoMoneyError) as e:
                logging.debug(e)
                #time.sleep(1)
            except Exception as e:
                print(e)

    def stop(self):
        self.started = False
        logging.info("Stopping trades.")
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

    def get_available_trade_info(self, trade_info):
        """Parses the trade information string from the available tix column"""
         # Format: '\r\n (bunch of spaces) Tix @ rate:1\r\n (bunch of spaces)'
        rate_split = [x for x in self.get_raw_data(trade_info).split(' ') if x and x[0].isdigit()]
        # If the trader is @ Market
        if len(rate_split) <= 1:
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
            logging.info("TIX UPDATE amount_remain: " + str(amount_remain) + "")
            if amount_remain < self.current_trade.remaining1:
                start_rate = self.current_trade.start_rate
                Trader.current_tix_rate = start_rate
                Trader.last_tix_rate = max(start_rate, Trader.last_tix_rate)
                self.current_trade.update(amount_remain, top_rate)
        elif self.current_trade:  #  Trade is complete.
            self.fully_complete_trade()

    def check_current_worse_trade(self):
        self.check_bot_stopped()
        # If the trade is a split trade, the rate may appear low, but the trade amount remains a profit, so don't cancel
        if self.current_trade and self.current_trade.amount1 == self.current_trade.remaining1:
            rate = self.current_trade.current_rate
            if self.last_robux_rate and rate > self.last_robux_rate:
                self.cancel_trades()
            elif self.current_robux_rate and rate > self.current_robux_rate:
                self.cancel_trades()
            elif not self.last_robux_rate and not self.current_robux_rate:
                if rate > self.get_other_rate():
                    self.cancel_trades()

    def check_trade_gap(self):
        self.check_bot_stopped()
        if self.current_trade and self.current_trade.amount1 == self.current_trade.remaining1:
            trade_info = data[self.currency]['next_trade_info']
            next_tix, next_rate = self.get_available_trade_info(trade_info)
            diff = self.current_trade.current_rate - next_rate
            if diff > gap:
                logging.info('Trade gap is big ({}) Trading for a better rate...'.format(str(diff)))
                self.cancel_trades()

    def check_better_rate(self):
        """Check if a better rate for tix to robux exists, updates the GUI if our trade is top"""
        self.check_bot_stopped()

        trade_info = data[self.currency]['top_trade_info']
        our_tix = self.get_trade_remainder()
        top_tix, top_rate = self.get_available_trade_info(trade_info) #  Some speed errors may occur
        
        # Check if the top trade is not our trade
        if our_tix and our_tix != top_tix:
            self.update_current_trade(our_tix) # Update the remaining tix first
            TixTrader.holds_top_trade = False
            if top_rate < self.last_robux_rate or self.current_robux_rate and top_rate < self.current_robux_rate:
                return True
            elif not self.last_robux_rate and not self.current_robux_rate and top_rate < self.get_other_rate():
                return True
        elif our_tix is not None:
            TixTrader.holds_top_trade = True
            self.update_current_trade(our_tix, top_rate)
        return False

    def test_rate(self, rate, this_top_rate, threshold_rate):
        """Tests if the rate is better than the last rate"""
        current_rate, last_rate = Trader.current_robux_rate, Trader.last_robux_rate
        if rate - this_top_rate > gap:
            raise TradeGapError
        if last_rate and rate >= last_rate:
            raise WorseRateError(self.currency, self.other_currency, rate, last_rate)
        elif not last_rate:
            if not threshold_rate:
                raise BadSpreadError
            if round_down(rate) > threshold_rate - .0015:
                raise WorseRateError(self.currency, self.other_currency, rate, threshold_rate-.0015)

    def balance_rate(self, amount, rate, this_top_rate, threshold_rate):
        """Gives a trade amount nearest the exact rate, with the highest 4th decimal place and the corresponding robux to receive"""
        self.check_bot_stopped()
        self.test_rate(rate, this_top_rate, threshold_rate)
        x, best_x = amount, 0
        closest_within_rate, closest_outside_rate = 0, sys.maxsize
        # Add tolerance check
        while x > self.get_tolerance(amount)*amount:
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
        if completed_trade:
            completed_trade.update(0)
            Trader.current_tix_rate = 0
            Trader.last_tix_rate = max(completed_trade.start_rate, Trader.last_tix_rate)
            self.current_trade = None

    def check_no_recent_trades(self):
        """If the trader hasn't traded in a while, reset the last_robux_rate so the bot 
        could possibly trade at a worse rate but gain in the long run."""
        now = time.time()
        if now - self.last_trade_time > reset_time:
            if not self.my_trader.holds_top_trade:
                print('No recent')
                self.last_trade_time = now
                Trader.last_robux_rate = 0
                self.cancel_trades()
            else: # Extend the time
                self.last_trade_time = now

    def do_trade(self):
        our_money = self.get_currency()
        if self.current_trade: # If a trade is active, trade with the remaining amount
            remainder = self.get_trade_remainder()
            if self.config['trade_all']:
                amount = our_money + remainder
            else:
                amount = min(our_money+remainder, self.config['amount'])
        elif self.config['trade_all']:
            amount = our_money
        else:
            amount = min(self.config['amount'], our_money)
            if not amount or amount > our_money:
                raise NoMoneyError(self.currency)
        # Especially if split trades are on, don't constantly trade small amounts
        self.check_bot_stopped()
        to_trade, receive, rate = self.calculate_trade(amount)
        self.check_bot_stopped()
        if self.check_trades():
            self.cancel_trades()
        if to_trade > self.get_currency():
            raise NoMoneyError(self.currency)
        self.submit_trade(to_trade, receive)

        new_trade = Trade(to_trade, receive, 'Tickets', 'Robux', rate)
        if Trader.last_tix_rate == 0:
            Trader.last_tix_rate = rate
        Trader.current_tix_rate = rate
        self.current_trade = new_trade
        self.trade_log.add_trade(new_trade)


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
                start_rate = self.current_trade.start_rate 
                Trader.current_robux_rate = start_rate
                if Trader.last_robux_rate:
                    Trader.last_robux_rate = min(start_rate, Trader.last_robux_rate)
                else:
                    Trader.last_robux_rate = start_rate
                self.current_trade.update(amount_remain, top_rate)
        elif self.current_trade:
            self.fully_complete_trade()

    def check_current_worse_trade(self):
        self.check_bot_stopped()
        if self.current_trade and self.current_trade.amount1 == self.current_trade.remaining1:
            rate = self.current_trade.current_rate
            if self.last_tix_rate and rate < self.last_tix_rate:
                self.cancel_trades()
            elif self.current_tix_rate and rate < self.current_tix_rate:
                self.cancel_trades()
            elif not self.last_tix_rate and not self.current_tix_rate:
                if rate < self.get_other_rate():
                    self.cancel_trades()

    def get_available_trade_info(self, trade_info):
        """Parses the trade information string from the available robux column"""
        robux = to_num(self.get_raw_data(trade_info[0]))
        #Format ['\r\n (bunch of spaces)', ' @ 1:rate\r\n']
        # Gets the 1:rate\r\n part
        all_rate = [x for x in self.get_raw_data(trade_info[1])[1].split(' ') if x and x[0].isdigit()]
        # Check if the trade is @ Market
        if not all_rate:
            raise MarketTraderError
        # Gets the rate part
        rate = (all_rate[0].split(':')[1]).split('\\')[0]
        rate = float(rate)
        return robux, rate

    def check_trade_gap(self):
        """Check if our rate is far higher than the next rate."""
        self.check_bot_stopped()
        if self.current_trade and self.current_trade.amount1 == self.current_trade.remaining1:
            # Get the second highest trade's info
            trade_info = data[self.currency]['next_trade_info']
            next_robux, next_rate = self.get_available_trade_info(trade_info)
            diff = next_rate - self.current_trade.current_rate
            if diff > gap:
                logging.info('Trade gap is big ({}) Trading for a better rate...'.format(str(diff)))
                self.cancel_trades()

    def check_better_rate(self):
        """Check if a better rate for robux to tix exists"""
        # See rbx_data since this one is weird.
        trade_info = data[self.currency]['top_trade_info']
        our_robux = self.get_trade_remainder()
        top_robux, top_rate = self.get_available_trade_info(trade_info)
        # Check if the top trade is not our trade
        if our_robux and our_robux != top_robux:
            self.update_current_trade(our_robux)
            RobuxTrader.holds_top_trade = False
            if self.last_tix_rate and top_rate > self.last_tix_rate or self.current_tix_rate and top_rate > self.current_tix_rate:
                return True
            elif not self.last_tix_rate and not self.current_tix_rate and top_rate > self.get_other_rate():
                return True
        elif our_robux is not None:
            RobuxTrader.holds_top_trade = True
            self.update_current_trade(our_robux, top_rate)
        return False

    def test_rate(self, rate, this_top_rate, threshold_rate):
        """Verifies that this is a better and profit making rate to trade at"""
        current_rate, last_rate = Trader.current_tix_rate, Trader.last_tix_rate
        if this_top_rate - rate > gap:
            raise TradeGapError
        if last_rate and rate <= last_rate:
            raise WorseRateError(self.currency, self.other_currency, rate, last_rate)
        elif not last_rate:
            if not threshold_rate:
                raise BadSpreadError
            if round_down(rate) < threshold_rate + .0015:
                raise WorseRateError(self.currency, self.other_currency, rate, threshold_rate+.0015)

    def balance_rate(self, amount, rate, this_top_rate, threshold_rate):
        """Gives a trade amount nearest the exact rate, and the corresponding tix to receive"""
        self.check_bot_stopped()
        self.test_rate(rate, this_top_rate, threshold_rate)
        x, closest, best_x = amount, sys.maxsize, 0
        while x > self.get_tolerance(amount)*amount:
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
        if completed_trade: # Trade has been fully completed?
            completed_trade.update(0)
            Trader.current_robux_rate = 0
            if Trader.last_robux_rate:
                Trader.last_robux_rate = min(completed_trade.start_rate, Trader.last_robux_rate)
            else:
                Trader.last_robux_rate = completed_trade.start_rate
            self.current_trade = None

    def check_no_recent_trades(self):
        """If the trader hasn't traded in a while, reset the last_tix_rate so the bot 
        could possibly trade at a worse rate but gain in the long run."""
        now = time.time()
        if now - self.last_trade_time > reset_time:
            if not self.my_trader.holds_top_trade:
                print('No recent')
                self.last_trade_time = now
                Trader.last_tix_rate = 0
                self.cancel_trades()
            else:
                self.last_trade_time = now

    def do_trade(self):
        our_money = self.get_currency()
        if self.current_trade: # If a trade is active, trade with the remaining amount
            remainder = self.get_trade_remainder()
            if self.config['trade_all']:
                amount = our_money + remainder
            else:
                amount = min(our_money+remainder, self.config['amount'])
        elif self.config['trade_all']:
            amount = our_money
        else:
            amount = min(self.config['amount'], our_money)
            if not amount or amount > our_money:
                raise NoMoneyError(self.currency)
        self.check_bot_stopped()
        to_trade, receive, rate = self.calculate_trade(amount)
        self.check_bot_stopped()
        if self.check_trades:
            self.cancel_trades()
        if to_trade > self.get_currency():
            raise NoMoneyError(self.currency)
        self.submit_trade(to_trade, receive)

        new_trade = Trade(to_trade, receive, 'Robux', 'Tickets', rate)
        if Trader.last_robux_rate == 0:
            Trader.last_robux_rate = rate
        Trader.current_robux_rate = rate
        self.current_trade = new_trade
        self.trade_log.add_trade(new_trade)


def test_login(user, pw):
    payload = {
        'username': user,
        'password': pw,
    }
    r = session.post(LOGIN_URL, payload)
    if r.url == LOGIN_URL:
        raise LoginError
