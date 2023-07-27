# traders.py

# this file contains the definition of the various type of traders that populate the market
# in particular:
# - informed traders: they know the true value of the security, and will buy only if Pa < V(i) and sell only if Pb > V(i)
# - noisy traders: they consider true a value given by W(i) = V(i) + eps(i), eps ~ N(m, s**2); they will buy only if Pa < W(i) 
#                  and sell if Pb > W(i)
# - uninformed (liquidity) traders: they will place buy, sell or no order following a given probability;
#   they can be divided in:
#   + risk-averse: will trade less in riskier market times (i.e. market volatility)
#   + risk-neutral: will trade equally in any market condition
#   + risk-diver: will trade more in riskier market times (they will try to anticipate the market)
#   in general, uninformed traders will be biased in their decisions depending on the market movements (i.e. past performances)

import math
import numpy as np
import random

__all__ = ['Traders', 'InformedTraders']


class Traders:
    '''
    Traders class will populate the market with the three following three types of traders:
    - Informed traders (alpha)
    - Noisy traders (beta)
    - Uninformed traders (1-alpha-beta)
    
    weights = (alpha, beta) indicate the presence in percentage of informed traders (alpha)
        and noisy traders (beta) in the market. The remaining portion will represent uninformed traders
        N.B.: risk-aversion not implemented at the moment
    prices = [p_bid, p_ask, true_value] stores the market conditions over the traded security 
        (bid, ask and true value)
    '''
    def __init__(self, weights, prices) -> None:
        self.weights = weights
        self.prices = prices
    
    def __str__(self) -> str:
        pass

    def __str__(self) -> str:
        pass

    def __eq__(self, __other: object) -> bool:
        pass


class InformedTraders:
    '''
    InformedTraders class defines the behaviour of informed traders in the market
    '''
    def __init__(self, holdings: int = 0, budget: float = 1000) -> None:
        self.holdings = holdings
        self.budget = budget
        self.trading_history = dict()
        self.execution_price = 0
        self.pnl = list()

    def trade(self, security_value, market_prices, t):
        '''
        Defines how the InformedTrader will behave with respect to bid and ask prices
        '''
        bid_price, ask_price = market_prices
        
        if security_value > ask_price and self.budget > 0:
            price_request = 'ask'
            self.holdings += 1
            self.trading_history[f'{t} - ask'] = ask_price
            self.execution_price = (1 - 1 / self.holdings) * self.execution_price + 1 / self.holdings * ask_price

        elif security_value < bid_price and self.holdings > 0:
            price_request = 'bid'
            self.holdings -= 1
            self.trading_history[f'{t} - bid'] = bid_price
            pnl = bid_price - self.execution_price
            self.budget += pnl
            self.pnl.append(pnl)

        else:
            price_request = None
            self.trading_history[f'{t} - None'] = 0
            self.pnl.append(0)

        return price_request
    
    def pnl_calculation(self):
        return np.cumsum(self.pnl)
    

class LiquidityTraders:
    """
    LiquidityTraders class defines the behavior of noisy trders in the market
    """
    def __init__(self, holdings: int = 0, budget: float = 1000) -> None:
        self.holdings = holdings
        self.budget = budget
        self.trading_history = dict()
        self.execution_price = 0
        self.pnl = list()

    def trade(self, market_prices, t):
        '''
        Defines how the LiquidityTrader will behave with respect to bid and ask prices
        '''
        bid_price, ask_price = market_prices

        price_request = random.choice(['bid', 'ask'])

        if price_request == 'bid' and self.holdings > 0:
            self.holdings -= 1
            self.trading_history[f'{t} - bid'] = bid_price
            pnl = bid_price - self.execution_price
            self.budget += pnl
            self.pnl.append(pnl)

        else:
            price_request = 'ask'
            self.holdings += 1
            self.trading_history[f'{t} - ask'] = ask_price
            self.execution_price = (1 - 1 / self.holdings) * self.execution_price + 1 / self.holdings * ask_price

        return price_request
    
    def pnl_calculation(self):
        return np.cumsum(self.pnl)


