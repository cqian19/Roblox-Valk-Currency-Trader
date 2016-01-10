LOGIN_URL = 'https://www.roblox.com/newlogin'
TC_URL = 'http://www.roblox.com/My/Money.aspx#/#TradeCurrency_tab'

data = {
    'Tickets': {
        'current': '//*[@id="nav-tix-balance"]/text()',
        'cancel_bid': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OpenBids$OpenBidsListView$ctrl0$ctl00$CancelBidButton',
        'trades': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsUpdatePanel"]/div[1][@class="NoResults"]/text()',
        'trade_info': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsUpdatePanel"]/table/tr[2]/td[1]/text()',
        'trade_remainder': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsUpdatePanel"]/table/tr[2]/td[2]/text()',
        'top_trade_info': '//*[@id="CurrencyBidsPane"]/div/div[1]/text()',
        'next_trade_info': '//*[@id="CurrencyBidsPane"]/div/div[2]/text()'
    },
    'Robux': {
        'current': '//*[@id="nav-robux-balance"]/text()',
        'cancel_bid': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OpenOffers$OpenOffersListView$ctrl0$ctl00$CancelOfferButton',
        'trades': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_OpenOffersUpdatePanel"]/div[1][@class="NoResults"]/text()',
        'trade_info': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_OpenOffersUpdatePanel"]/table/tr[2]/td[1]/text()',
        'trade_remainder': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_OpenOffersUpdatePanel"]/table/tr[2]/td[2]/text()',
        # Format: <div><span>robuxtext</span> @ rate </div>:
        'top_trade_info': ('//*[@id="CurrencyOffersPane"]/div/div[1]/span/text()', '//*[@id="CurrencyOffersPane"]/div/div[1]/text()'),
        'next_trade_info': ('//*[@id="CurrencyOffersPane"]/div/div[2]/span/text()', '//*[@id="CurrencyOffersPane"]/div/div[2]/text()')
    },
    'username': 'username',
    'password': 'password',
    # Trade currency elements
    'rates': '//*[@id="CurrencyQuotePane"]/div[1]/div[2]/div[2]/text()',
    'spread': '//*[@id="CurrencyQuotePane"]/div[1]/div[1]/div[4]/text()',
    # Trade frame elements
    'split_trades': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$AllowSplitTradesCheckBox',
    'limit_order': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$LimitOrderRadioButton',
    'trade_type': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OrderType',
    'give_type': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$HaveCurrencyDropDownList',
    'receive_type': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$WantCurrencyDropDownList',
    'give_box': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$HaveAmountTextBoxRestyle',
    'receive_box': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$WantAmountTextBox',
    'submit_trade_button': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$SubmitTradeButton',
}
