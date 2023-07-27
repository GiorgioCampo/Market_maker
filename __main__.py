# main file

# this file contains a market simulation
# the market is characterized by 
### a market maker providing liquidity for a single security
### informed traders
### noisy traders
### uninformed (liquidity) traders


import math
import matplotlib.pyplot as plt
import numpy as np
from traders import InformedTraders, LiquidityTraders
from market_maker import MarketMaker
from traded_security import *

stock = Stock(100, mu=0.001, sigma=0.05)
stock_market_maker = MarketMaker(100, 1000, spread=3)
informed_trader = InformedTraders(holdings=100, budget=100_000)
liquidity_trader = LiquidityTraders(budget=100_000_000)
stock_price = list()
bid_price = list()
ask_price = list()
average_mm_cost = list()

for t in range(1000):
    stock_price.append(stock.value_evolution(t=t))
    # HP: informed traders trade before liquidity traders
    price_request = informed_trader.trade(stock.current_value, (stock_market_maker.bid_price, stock_market_maker.ask_price), t)
    bid, ask = stock_market_maker.pricing(price_request)
    price_request = liquidity_trader.trade((stock_market_maker.bid_price, stock_market_maker.ask_price), t)
    bid, ask = stock_market_maker.pricing(price_request)
    bid_price.append(bid)
    ask_price.append(ask)
    average_mm_cost.append(stock_market_maker.avg_cost)
    if stock.current_value < 0:
        break

fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(stock_price, label='Stock True Value')
ax1.plot(bid_price, label='Bid Price')
ax1.plot(ask_price, label='Ask Price')
ax1.vlines(
    np.linspace(90,990,11), 
    ymin=0,
    ymax=max(stock_price),
    colors='yellow',
    linestyles='dashed'
    )
ax1.vlines(
    stock.shocks,
    ymin=0,
    ymax=max(stock_price),
    colors='red',
)
ax1.legend()
ax2.plot(np.array(ask_price) - np.array(bid_price), label="Bid-Ask spread")

fig, (ax3, ax4, ax5, ax6, ax7) = plt.subplots(5)

ax3.plot(informed_trader.pnl_calculation())
ax4.plot(liquidity_trader.pnl_calculation())
ax5.plot(stock_market_maker.pnl_calculation())
ax6.plot(stock_market_maker.historical_vol)
ax7.plot(average_mm_cost)


plt.show()

