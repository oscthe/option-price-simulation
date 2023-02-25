import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class BlackScholesOption:
    def __init__(self, spot_price, strike_price, time_to_expiry, volatility, risk_free_rate, call_option=True):
        self.spot_price = spot_price
        self.strike_price = strike_price
        self.time_to_expiry = time_to_expiry
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate
        self.call_option = call_option

    def d1(self):
        d1_numerator = np.log(self.spot_price / self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_expiry
        d1_denominator = self.volatility * np.sqrt(self.time_to_expiry)
        return d1_numerator / d1_denominator

    def d2(self):
        return self.d1() - self.volatility * np.sqrt(self.time_to_expiry)
    
    def call_price(self):
        call_price = self.spot_price * norm.cdf(self.d1()) - self.strike_price * np.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(self.d2())
        return call_price
    
    def put_price(self):
        put_price = self.strike_price * np.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(-self.d2()) - self.spot_price * norm.cdf(-self.d1())
        return put_price
    
    def price(self):
        if self.call_option:
            return self.call_price()
        else:
            return self.put_price()

class OptionSimulator:
    def __init__(self, spot_price, strike_price, time_to_expiry, volatility, risk_free_rate, call_option=True):
        self.spot_price = np.array(spot_price, dtype=float)
        self.strike_price = np.array(strike_price, dtype=float)
        self.time_to_expiry = np.array(time_to_expiry, dtype=float)
        self.volatility = np.array(volatility, dtype=float)
        self.risk_free_rate = np.array(risk_free_rate, dtype=float)
        self.call_option = call_option

    def simulate(self):
        # Calculate option prices for all combinations of input parameters
        option_prices = {"price": [],
                         "S": [],
                         "K": [],
                         "T": [],
                         "sigma": [],
                         "r": [],
                         "call_option": []}
        for i, spot in enumerate(self.spot_price):
            for j, strike in enumerate(self.strike_price):
                for k, time in enumerate(self.time_to_expiry):
                    for l, sigma in enumerate(self.volatility):
                        for m, rate in enumerate(self.risk_free_rate):
                            option_prices["price"].append(BlackScholesOption(spot, strike, time, sigma, rate, call_option=self.call_option).price())
                            option_prices["S"].append(spot)
                            option_prices["K"].append(strike)
                            option_prices["T"].append(time)
                            option_prices["sigma"].append(sigma)
                            option_prices["r"].append(rate)
                            option_prices["call_option"].append(1 if self.call_option else 0)
                            
                            
        results_df = pd.DataFrame(option_prices)
        return results_df
