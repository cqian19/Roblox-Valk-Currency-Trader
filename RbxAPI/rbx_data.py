LOGIN_URL = 'https://www.roblox.com/newlogin'
TC_URL = 'http://www.roblox.com/My/Money.aspx#/#TradeCurrency_tab'

data = {
    'Tickets': {
        'current': '//*[@id="nav-tix-balance"]/text()',
        'open_trades': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsUpdatePanel"]/table/*[@class="TileGroup"]',
        'cancel_bid': lambda i: 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OpenBids$OpenBidsListView$ctrl' + str(i) + '$ctl00$CancelBidButton',
        'trades': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsUpdatePanel"]/div[1][@class="NoResults"]/text()',
        'trade_info': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsUpdatePanel"]/table/tr[2]/td[1]/text()',
        'trade_remainder': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsUpdatePanel"]/table/tr[2]/td[2]/text()',
        # Starts at index 1
        'trade_info_path': lambda i: '//*[@id="CurrencyBidsPane"]/div/div[' + str(i) +']/text()',
    },
    'Robux': {
        'current': '//*[@id="nav-robux-balance"]/text()',
        'open_trades': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_OpenOffersUpdatePanel"]/table/*[@class="TileGroup"]',
        'cancel_bid': lambda i: 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OpenOffers$OpenOffersListView$ctrl' + str(i) + '$ctl00$CancelOfferButton',
        'trades': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_OpenOffersUpdatePanel"]/div[1][@class="NoResults"]/text()',
        'trade_info': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_OpenOffersUpdatePanel"]/table/tr[2]/td[1]/text()',
        'trade_remainder': '//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_OpenOffersUpdatePanel"]/table/tr[2]/td[2]/text()',
        # Format: <div><span>robuxtext</span> @ rate </div>: 
        # Starts at index 1
        'trade_info_path': lambda i: ('//*[@id="CurrencyOffersPane"]/div/div[' + str(i) + ']/span/text()', 
                                      '//*[@id="CurrencyOffersPane"]/div/div[' + str(i) + ']/text()'),
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
