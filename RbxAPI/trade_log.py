from PySide.QtCore import Signal, QObject
import time
import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s -%(levelname)s %(funcName)s %(message)s  %(module)s: <Line %(lineno)s>")
# For Debugging:
# logging.disable(logging.CRITICAL)


def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    ts = ""
    if h != 0:
        ts += "{:.0f} Hours ".format(h)
    if m != 0:
        ts += "{:.0f} Minutes ".format(m)
    ts += "{:.2f} Seconds".format(s)
    return ts

abbr = {
    'Tickets': 'Tx',
    'Robux': 'R$'
}


class Trade(QObject):

    trade_updated = Signal(QObject)

    def __init__(self, amount1, amount2, type1, type2, rate):
        super().__init__()
        self.time = time.time()
        self.amount1 = self.remaining1 = amount1
        self.amount2 = self.remaining2 = amount2
        self.type1 = type1
        self.type2 = type2
        self.start_rate = rate
        self.current_rate = rate
        self.seconds_time = time.time()
        self.start_time = datetime.datetime.now()
        self.complete_time = 'Incomplete'
        self.row = None  # The GUI display row
        logging.info(str(self))

    def update(self, remaining1, rate=None):
        self.remaining1 = remaining1
        if rate is not None:
            self.current_rate = rate
        self.trade_updated.emit(self)

    def __str__(self):
        starttup = (self.amount1, self.type1, self.start_rate,
                    self.amount2, self.type2)
        currenttup = (self.remaining1, self.type1, self.current_rate)
        s =    "\n" +\
               "Start: Trading {} {} @ {:.3f} for {} {}".format(*starttup) + "\n" +\
               "Current Status: Trading {} {} @ {:.3f}".format(*currenttup) + "\n" +\
               "Start time: {0}".format(self.start_time) +"\n" +\
               "Complete time: {0}".format(self.complete_time)
        if self.complete_time != 'Incomplete':
            s += "\nTime Elapsed: {0}".format(format_time((self.complete_time - self.start_time).total_seconds()))
        return s

class TradeLog(QObject):

    trade_added = Signal(QObject)
    trade_completed = Signal(QObject)

    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.log = []

    def add_trade(self, trade):
        self.trade_added.emit(trade)

    def complete_trade(self, trade):
        trade.complete_time = datetime.datetime.now()
        logging.info("Completed trade!")
        logging.debug("Start amount1: {} \t Remaining amount1: {}".format(str(trade.amount1),str(trade.remaining1)))
        self.log.append(trade)
        self.trade_completed.emit(trade)

