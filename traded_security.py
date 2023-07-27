# traded_security.py

# this file will contain all the possible securities traded by the market maker and the traders in the market
# N.B.: the initial intent is to let the market be populated by a single security at a time

import math
import random
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['Stock']


class Stock:
    '''
    Stock class represents an equity title traded in the market.
    Given an initial value (e.g. after the IPO), the true (current) value of the 
    stock will evolve following a jump process.
    Different kind of jumps can occur:
    - periodical jumps, given by earnings reports, etc.
    - random jumps, given by market shocks, crashes, etc.
    '''
    def __init__(
            self,
            initial_value: float, 
            current_value: float = None,
            mu: float = 0.001,
            sigma: float = 0.025,
            probability_distribution = random.gauss,
            ) -> None:
        self.initial_value = initial_value
        self.current_value = initial_value
        self.mu = mu
        self.sigma = sigma
        self.probability_distribution = probability_distribution
        self.shocks = list()
        self.diffusion = 0

    def value_evolution(self, t: int = 1) -> float:
        '''
        Describes the value evolution for the Stock, given the initial value and a probability distribution.
        Value evolution is given by:
        - a random walk with drift, influenced by the passage of time (t)
        - periodical shocks (earnings reports)
        - random shocks (company news, market turmoils)
        '''

        if t % 90 == 0 and self.current_value:
            periodical_shock = random.gauss(0, self.sigma)
        else:
            periodical_shock = 0
        
        random_shock = float(*random.choices(
        (random.gauss(self.mu, self.sigma), 0), 
        weights=(0.005, 0.995)# MAKE IT A PARAM
        ))  * self.current_value

        if random_shock != 0:
            print(f'Time: {t} - shock = {random_shock}')
            self.shocks.append(t)
            self.initial_value -= random_shock
        
        # drift and diffusion following GBM theory
        drift = (self.mu - 0.5 * self.sigma**2) * t
        diffusion = self.sigma * random.gauss(0, 1)

        self.diffusion += diffusion

        self.current_value = (
            self.initial_value * np.exp(drift + self.diffusion)
            + periodical_shock
            - random_shock
            )
        
        return self.current_value


if __name__ == '__main__':
    stock = Stock(100)
    stock_price = list()
    for t in range(1_000):
        stock_price.append(stock.value_evolution(t=t))
        print(stock.current_value)
        if stock.current_value < 0:
            break

    plt.plot(stock_price)
    plt.vlines(
        np.linspace(90,990,11), 
        ymin=0,
        ymax=max(stock_price),
        colors='yellow',
        linestyles='dashed'
        )
    plt.vlines(
        stock.shocks,
        ymin=0,
        ymax=max(stock_price),
        colors='red',
    )
    plt.show()

