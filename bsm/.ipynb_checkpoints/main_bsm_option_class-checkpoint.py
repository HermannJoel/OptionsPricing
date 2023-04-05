from bsm_option_val import *

if __name__ == "__main__":
    o = call_option(100., 105., 1.0, 0.05, 0.2)
    type(o)
    value = o.value()
    value
    o.imp_vol(C0=value)
    o.vega()