from bsm_option_val import *

if __name__ == "__main__":
    o = call_option(100., 105., 1.0, 0.05, 0.2)
    type(o)
    value = o.value()
    value
    o.imp_vol(C0=value)
    o.vega()
    
if __name__ == "__main__":
    S = 100
    X = 110
    r = 0.05
    sigma = 0.2
    T = 1
    option_type = "call"
    n = 10000
    probability = probability_of_touch(S, X, r, sigma, T, option_type, n)
    print(f"Estimated probability of touch: {probability: .2%}")