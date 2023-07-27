# market_maker.py

# This file describes the behaviour of the market maker that sets bid and ask prices for the traded securities

import math
import numpy as np
from collections import deque

__all__ = ['MarketMaker']


class MarketMaker:
    '''
    MarketMaker class allows to add a market maker to the market environment.
    Parameters:
    - intial_value: the market maker knows the initial value of the security that will offer
    - inventory: determines the initial quantity of the security that the market maker possesses
    '''
    def __init__(self, initial_value, inventory, spread):
        self.initial_value = initial_value
        self.inventory = inventory
        self.spread = spread
        self.bid_price = self.initial_value - self.spread / 2
        self.ask_price = self.initial_value + self.spread / 2
        self.avg_cost = self.initial_value
        self.last_price = initial_value
        self.pnl = list()
        self.vol_sample = deque(30*[self.initial_value], 30)
        self.historical_vol = [np.std(list(self.vol_sample))]

    def pricing(self, price_request):
        '''
        Defines the bid - ask price dinamycs, based on the last transaction from the market.
        - price_request: the request that a trader presents to the market maker
                         It can be a request for the bid price (MM buys) or for the ask price (MM sells)
        '''

        self.vol_sample.appendleft(self.last_price)
        realized_volatility = np.std(list(self.vol_sample))

        price_adjustment = realized_volatility / 2

        if realized_volatility > np.average(self.historical_vol[-30:-1]):
            price_adjustment_spread = price_adjustment + self.last_price / 10000
        else:
            price_adjustment_spread = price_adjustment - self.last_price / 10000
        
        self.historical_vol.append(realized_volatility)

        if price_request == 'bid':
            self.avg_cost = (self.avg_cost * self.inventory + self.bid_price) / (self.inventory + 1)
            self.inventory += 1
            self.last_price = self.bid_price

            self.bid_price -= price_adjustment_spread
            self.ask_price -= price_adjustment

        elif price_request == 'ask':
            self.inventory -= 1
            self.pnl.append(self.ask_price - self.avg_cost)
            self.last_price = self.ask_price

            self.bid_price += price_adjustment
            self.ask_price += price_adjustment_spread

        elif price_request is None:
            self.pnl.append(0)

        price_request = None

        return self.bid_price, self.ask_price
    
    def pnl_calculation(self):
        return np.cumsum(self.pnl)


