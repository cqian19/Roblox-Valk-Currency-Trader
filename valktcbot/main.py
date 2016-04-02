from PySide import QtCore, QtGui
from functools import partial
from rbxAPI import *

import guifiles.mainGui as gui

import configparser
import logging
import sys
import time

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s -%(levelname)s %(funcName)s %(message)s  %(module)s: <Line %(lineno)s>"
)
# For Debugging:
# logging.disable(logging.CRITICAL)


class MainDialog(QtGui.QMainWindow, gui.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.started = False
    # Traders
        self.trade_log = TradeLog()
        self.tix_trader = TixTrader(self.trade_log)
        self.robux_trader = RobuxTrader(self.trade_log)
        self.tix_thread = self.assign_thread(self.tix_trader)
        self.robux_thread = self.assign_thread(self.robux_trader)
    # Login screen
        self.usernameField.returnPressed.connect(self.login_pressed)
        self.passwordField.returnPressed.connect(self.login_pressed)
        self.loginButton.clicked.connect(self.login_pressed)
    # Options
        # Check box
        self.tixSplitTrades.stateChanged.connect(partial(self.split_pressed, self.tix_trader))
        self.robuxSplitTrades.stateChanged.connect(partial(self.split_pressed, self.robux_trader))
        self.tixTradeAll.stateChanged.connect(
            partial(self.trade_all_pressed, self.tix_trader, self.tixAmount))
        self.robuxTradeAll.stateChanged.connect(
            partial(self.trade_all_pressed, self.robux_trader, self.robuxAmount))
        self.tixEarlyCancel.stateChanged.connect(partial(self.early_cancel_pressed, self.tix_trader))
        self.robuxEarlyCancel.stateChanged.connect(partial(self.early_cancel_pressed, self.robux_trader))
        # Spin box
        self.tixAmount.valueChanged.connect(partial(self.amount_changed, self.tix_trader))
        self.robuxAmount.valueChanged.connect(partial(self.amount_changed, self.robux_trader))
        self.tixThresholdRate.valueChanged.connect(partial(self.threshold_rate_changed, self.tix_trader))
        self.robuxThresholdRate.valueChanged.connect(partial(self.threshold_rate_changed, self.robux_trader))
        # Config settings
        self.initialize_config()
        # Start
        self.startButton.clicked.connect(self.start_pressed)
    # Trade Log
        self.last_tix_traded = self.last_robux_traded = 0
        self.trade_log.trade_added.connect(self.on_trade_added)
        self.trade_log.trade_completed.connect(self.on_trade_completed)
        print("Starting bot")

    def initialize_config(self):
        config = configparser.ConfigParser()
        try:
            with open('config.ini', 'r+'):
                config.read('config.ini')
        except (IOError, FileNotFoundError, configparser.MissingSectionHeaderError):
            self.save_config() # Create or fix the config file
        else:
            if not (config.has_section('TixTrader') and config.has_section('RobuxTrader')):
                self.save_config()
            else:
                tix_settings = config['TixTrader']
                self.tixSplitTrades.setChecked(tix_settings.getboolean('split_trades'))
                self.tixAmount.setValue(int(tix_settings['amount_to_trade']))
                self.tixTradeAll.setChecked(tix_settings.getboolean('trade_all'))
                self.tixEarlyCancel.setChecked(tix_settings.getboolean('early_cancel'))
                self.tixThresholdRate.setValue(float(tix_settings['threshold_rate']))
                self.threshold_rate_changed(self.tix_trader, float(tix_settings['threshold_rate']))

                robux_settings = config['RobuxTrader']
                self.robuxSplitTrades.setChecked(robux_settings.getboolean('split_trades'))
                self.robuxAmount.setValue(int(robux_settings['amount_to_trade']))
                self.robuxTradeAll.setChecked(robux_settings.getboolean('trade_all'))
                self.robuxEarlyCancel.setChecked(robux_settings.getboolean('early_cancel'))
                self.robuxThresholdRate.setValue(float(robux_settings['threshold_rate']))
                self.threshold_rate_changed(self.robux_trader, float(robux_settings['threshold_rate']))

    def save_config(self):
        config = configparser.ConfigParser()
        with open('config.ini', 'a+'): # Creates the file if it does not exist
            try:
                config.read('config.ini')
            except configparser.MissingSectionHeaderError:
                pass
        try:
            tix_settings, robux_settings = config['TixTrader'], config['RobuxTrader']
        except KeyError:          
            config['TixTrader'] = config['RobuxTrader'] = {}
            tix_settings, robux_settings = config['TixTrader'], config['RobuxTrader']                     

        tix_settings['split_trades'] = str(self.tixSplitTrades.isChecked())
        tix_settings['amount_to_trade'] = str(self.tixAmount.value())
        tix_settings['trade_all'] = str(self.tixTradeAll.isChecked())
        tix_settings['early_cancel'] = str(self.tixEarlyCancel.isChecked())
        tix_settings['threshold_rate'] = str(self.tixThresholdRate.value())

        robux_settings['split_trades'] = str(self.robuxSplitTrades.isChecked())
        robux_settings['amount_to_trade'] = str(self.robuxAmount.value())
        robux_settings['trade_all'] = str(self.robuxTradeAll.isChecked())
        robux_settings['early_cancel'] = str(self.robuxEarlyCancel.isChecked())
        robux_settings['threshold_rate'] = str(self.robuxThresholdRate.value())

        try:
            with open('config.ini', 'w+') as configfile:
                config.write(configfile)
        except Exception as e:
            print(e)
            print('Cannot save config settings. Try running as administrator next time.')

    def on_trade_added(self, trade):
        target = self.currentTradeTable
        tup = (trade.amount1, abbr[trade.type1], round_down(trade.current_rate))
        text = "{} {} @ {:.3f}".format(*tup)
        trade.row = self.add_trade_gui(text, target)
        trade.trade_updated.connect(self.on_trade_updated)

    def on_trade_updated(self, trade):
        tup = (trade.remaining1, abbr[trade.type1], round_down(trade.current_rate))
        text = "{} {} @ {:.3f}".format(*tup)
        row = trade.row
        if row:
            row.setText(text)

    def on_trade_completed(self, trade):
        current = self.currentTradeTable
        target = self.pastTradesTable
        if trade.row:
            current.takeItem(current.row(trade.row))

        amount_traded = trade.amount1 - trade.remaining1
        all_traded = amount_traded == trade.amount1
        text = ""

        # Preventing duplicates from showing.
        if trade.type1 == 'Tickets':  # Trade cancelled but some went through
            if not all_traded and amount_traded == self.last_tix_traded: # Duplicate trade
                return
            self.last_tix_traded = amount_traded
        elif trade.type1 == 'Robux':
            if not all_traded and amount_traded == self.last_robux_traded: # Duplicate trade
                return 
            self.last_robux_traded = amount_traded 
        if amount_traded > 0: # Some currency went through
            print(trade)
            if all_traded:  # Trade is fully completed
                tup = (amount_traded, abbr[trade.type1],
                       round_down(trade.start_rate), trade.amount2, abbr[trade.type2])
                text = "{} {} @ {:.3f} for {} {} ".format(*tup)
            else:
                tup = (amount_traded, abbr[trade.type1], round_down(trade.start_rate))
                text = "{} {} @ {:.3f} (Semi-complete)".format(*tup)
            trade.row = self.add_trade_gui(text, target)

    def clear_gui_log(self):
        self.currentTradeTable.clear()

    def make_row(self, text):
        new_row = QtGui.QListWidgetItem(text)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Unicode")
        font.setBold(True)
        font.setPointSize(8)
        new_row.setFont(font)
        # Black font color
        new_row.setForeground(QtGui.QBrush(QtGui.QColor('black')))
        new_row.setSizeHint(QtCore.QSize(20, 25))
        new_row.setText(text)
        return new_row

    def add_trade_gui(self, text, table):
        new_row = self.make_row(text)
        table.insertItem(0, new_row)
        return new_row

    def login_pressed(self):
        username = self.usernameField.text()
        pw = self.passwordField.text()
        try:
            test_login(username, pw)
            self.stackedWidget.setCurrentIndex(1)
        except LoginError as e:
            self.errorMessage.show()
            self.passwordField.clear()

    def split_pressed(self, trader, state):
        # State:0 if unchecked, 2 is checked
        is_checked = 'on' if state == 2 else ''
        trader.set_config('split_trades', is_checked)

    def amount_changed(self, trader, amount):
        trader.set_config('amount', amount)

    def trade_all_pressed(self, trader, amount_box, state):
        if state == 2:
            amount_box.setEnabled(False)
            trader.set_config('trade_all', True)
        else:
            amount_box.setEnabled(True)
            trader.set_config('trade_all', False)

    def early_cancel_pressed(self, trader, state):
        trader.set_config('early_cancel', state == 2)

    def threshold_rate_changed(self, trader, rate):
        trader.set_config('threshold_rate', rate)

    def assign_thread(self, obj):
        thread = QtCore.QThread()
        obj.moveToThread(thread)
        thread.started.connect(obj.start)
        return thread

    def start_bots(self):
        print("Starting bot trading")
        self.clear_gui_log()
        self.tix_thread.start()
        self.robux_thread.start()

    def stop_thread(self, thread):
        thread.quit()
        thread.wait()

    def stop_bots(self):
        print("Stopping bot trading")
        self.tix_trader.stop()
        self.robux_trader.stop()
        self.stop_thread(self.tix_thread)
        self.stop_thread(self.robux_thread)

    def start_pressed(self):
        # Cancel trades on end
        button = self.sender()
        if self.started:
            self.started = False
            button.setText('Start')
            self.startButton.setEnabled(False)
            self.stop_bots()
            self.startButton.setEnabled(True)
        else:
            self.started = True
            button.setText('Stop')
            self.start_bots()

    def closeEvent(self, event):
        """Builtin method executed when GUI is closed."""
        if self.started:
            self.stop_bots()
        self.save_config()
        print('Ending bot')


if __name__ == '__main__':
    QtGui.QApplication.setDesktopSettingsAware(False)
    app = QtGui.QApplication(sys.argv)
    form = MainDialog()
    form.show()
    sys.exit(app.exec_())
