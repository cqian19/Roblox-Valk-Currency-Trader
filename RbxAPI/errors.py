class LoginError(Exception):

    """Raised when login to roblox has failed"""
    attempts = 0

    def __init__(self):
        LoginError.attempts += 1
        self.msg = "Login has failed. Attempt {} (Roblox will lock you out after a certain number of attempts!)".format(
            self.attempts)

    def __str__(self):
        return self.msg

class TradeGapError(Exception):
    """Raised when your trade rate is far better than the next, decreasing potential profit"""
    msg = "Trade gap too big. Retrying..."

    def __str__(self):
        return self.msg
        
class LowRateError(Exception):

    """Raised when the trade rate is below a certain threshold"""
    msg = "Rate recorded is too low to trade at. Retrying..."

    def __str__(self):
        return self.msg


class BotStoppedError(Exception):

    """Raised when bot is paused"""
    msg = "Bot paused."

    def __str__(self):
        return self.msg


class WorseRateError(Exception):

    """Raised when rate is worse than the last traded rate"""

    def __init__(self, currency, other_currency, rate, last):
        self.msg = "{} to {} rate ({}) is worse than other rate ({})".format(
            currency, other_currency, rate, last)

    def __str__(self):
        return self.msg


class NoMoneyError(Exception):

    """Raised when amount of currency is too low to be traded"""

    def __init__(self, currency):
        self.msg = "Not enough " + currency + " to trade."

    def __str__(self):
        return self.msg


class BadSpreadError(Exception):

    """Raised when the spread is bad (0.00000 on one side of the currency)"""
    msg = "Bad spread recorded. Redoing trade..."

    def __str__(self):
        return self.msg


class MarketTraderError(Exception):

    """Raised when the rate is @ Market, so the rate doesn't exist"""
    msg = "Trade is by Market. Cannot get rate"

    def __str__(self):
        return self.msg

class ConnectionResetError(Exception):

    """Raised when item is None due to connection forcibly being closed."""
    msg = "Possible connection reset."

    def __str__(self):
        return self.msg