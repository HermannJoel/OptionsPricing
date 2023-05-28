import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def price_simulation(S, r, sigma, T, n):
    dt = T/252
    price_matrix = np.zeros((n, int(T/dt) + 1))
    price_matrix[:, 0] = S
    for i in range(1, int(T/dt) + 1):
        rand = np.random.standard_normal(n)
        price_matrix[:, i] = price_matrix[:, i - 1] * np.exp((r - 0.5 * sigma **2) * dt + sigma * np.sqrt(dt) * rand)
    return price_matrix


def probability_of_touch(S, X, r, sigma, T, option_type, n):
    price_matrix = price_simulation(S, r, sigma, T, n)
    if option_type == "call":
        payoff = np.maximum(price_matrix - X, 0)
    elif option_type == "put":
        payoff = np.maximum(price_matrix, 0)
    else:
        raise ValueError("Invalid option type. Choose either 'call' or 'put'.")
    touch_count = np.sum(np.max(payoff, axis=1) > 0)
    probability = touch_count / n
    
    fig, ax = plt.subplots()
    ax.plot(np.transpose(price_matrix), color='blue', alpha=0.05)
    ax.axhline(y=X, color="red", linestyle="--")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.set_title("Simulated_price_paths")
    plt.show()
    
    return probability
    
    
    
        
    
        
    
