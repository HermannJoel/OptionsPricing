from dx import *
import matplotlib.pyplot as plt
import datetime as dt

#market environment
if __name__ == "__main__":
    dates = [dt.datetime(2015, 1, 1), dt.datetime(2015, 7, 1),
    dt.datetime(2016, 1, 1)]
    csr = constant_short_rate('csr', 0.05)
    me_1 = market_environment('me_1', dt.datetime(2015, 1, 1))
    me_1.add_list('symbols', ['AAPL', 'MSFT', 'FB'])
    me_1.get_list('symbols')
    me_2 = market_environment('me_2', dt.datetime(2015, 1, 1))
    me_2.add_constant('volatility', 0.2)
    me_2.add_curve('short_rate', csr) # add instance of discounting class
    me_2.get_curve('short_rate')
    me_1.add_environment(me_2) # add complete environment
    me_1.get_curve('short_rate')
    me_1.constants
    me_1.lists
    me_1.curves
    me_1.get_curve('short_rate').short_rate


#valuation mcs Eur exercise
if __name__ == "__main__":
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant('final_date', dt.datetime(2015, 12, 31))
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('frequency', 'M')
    me_gbm.add_constant('paths', 10000)
    csr = constant_short_rate('csr', 0.06)
    me_gbm.add_curve('discount_curve', csr)
    gbm = geometric_brownian_motion('gbm', me_gbm)
    
    me_call = market_environment('me_call', me_gbm.pricing_date)
    me_call.add_constant('strike', 40.)
    me_call.add_constant('maturity', dt.datetime(2015, 12, 31))
    me_call.add_constant('currency', 'EUR')
    payoff_func = 'np.maximum(maturity_value - strike, 0)'
    eur_call = valuation_mcs_european('eur_call', underlying=gbm,
                                      mar_env=me_call, payoff_func=payoff_func)
    %time eur_call.present_value()
    %time eur_call.delta()
    %time eur_call.vega()

#valuation mcs Amr exercise
if __name__ == "__main__":
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant('final_date', dt.datetime(2016, 12, 31))
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('frequency', 'W')
    payoff_func = 'np.maximum(strike - instrument_values, 0)'
    me_am_put = market_environment('me_am_put', dt.datetime(2015, 1, 1))
    me_am_put.add_constant('maturity', dt.datetime(2015, 12, 31))
    me_am_put.add_constant('strike', 40.)
    me_am_put.add_constant('currency', 'EUR')
    am_put = valuation_mcs_american('am_put', underlying=gbm,
    mar_env=me_am_put, payoff_func=payoff_func)
    
    %time am_put.present_value(fixed_seed=True, bf=5)
    %%time
    ls_table = []
    for initial_value in (36., 38., 40., 42., 44.):
        for volatility in (0.2, 0.4):
            for maturity in (dt.datetime(2015, 12, 31),
                             dt.datetime(2016, 12, 31)):
                am_put.update(initial_value=initial_value, 
                              volatility=volatility, 
                              maturity=maturity)
                ls_table.append([initial_value, 
                                 volatility, 
                                 maturity, 
                                 am_put.present_value(bf=5)])
    print("S0 | Vola | T | Value")
    print(22 * "-")
    for r in ls_table:
    print("%d | %3.1f | %d | %5.3f" % (r[0], r[1], r[2].year - 2014, r[3]))
    
    am_put.update(initial_value=36.)
    am_put.delta()
    am_put.vega()
    
# weekly frequency
me_gbm.add_constant('paths', 50000)
In [25]: csr = constant_short_rate('csr', 0.06)
In [26]: me_gbm.add_curve('discount_curve', csr)
In [27]: gbm = geometric_brownian_motion('gbm', me_gbm)
    
if __name__ == "__main__":
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant('final_date', dt.datetime(2015, 12, 31))
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('frequency', 'M')
    
    # monthly frequency (respective month end)
    me_gbm.add_constant('paths', 10000)
    csr=constant_short_rate('csr', 0.05)
    me_gbm.add_curve('discount_curve', csr)
    #Second, we instantiate a model simulation object:
    
    gbm=geometric_brownian_motion('gbm', me_gbm)
    
    gbm.generate_time_grid()
    gbm.time_grid
    
    %%time paths_1 = gbm.get_instrument_values()
    paths_1
    
    gbm.update(volatility=0.5)
    %%time paths_2 = gbm.get_instrument_values()
    
    plt.figure(figsize=(8, 4))
    p1 = plt.plot(gbm.time_grid, paths_1[:, :10], 'b')
    p2 = plt.plot(gbm.time_grid, paths_2[:, :10], 'r-.')
    plt.grid(True)
    l1 = plt.legend([p1[0], p2[0]],
    ['low volatility', 'high volatility'], loc=2)
    plt.gca().add_artist(l1)
    plt.xticks(rotation=30)

#portfolio valuation
if __name__ == "__main__":
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('model', 'gbm')
    me_am_put = market_environment('me_am_put', dt.datetime(2015, 1, 1))
    me_am_put.add_constant('maturity', dt.datetime(2015, 12, 31))
    me_am_put.add_constant('strike', 40.)
    me_am_put.add_constant('currency', 'EUR')
    payoff_func = 'np.maximum(strike - instrument_values, 0)'
    am_put_pos = derivatives_position(
    name='am_put_pos',
    quantity=3,
    underlying='gbm',
    mar_env=me_am_put,
    otype='American',
    payoff_func=payoff_func)
    am_put_pos.get_info()
    
#derrivative portfolio
if __name__ == "__main__":
    models = {'gbm' : geometric_brownian_motion,
              'jd' : jump_diffusion,
              'srd': square_root_diffusion}
    
    otypes = {'European' : valuation_mcs_european,
              'American' : valuation_mcs_american}
    me_jd = market_environment('me_jd', me_gbm.pricing_date)
    # add jump diffusion-specific parameters
    me_jd.add_constant('lambda', 0.3)
    me_jd.add_constant('mu', -0.75)
    me_jd.add_constant('delta', 0.1)
    # add other parameters from gbm
    me_jd.add_environment(me_gbm)
    # needed for portfolio valuation
    me_jd.add_constant('model', 'jd')
    
    me_eur_call = market_environment('me_eur_call', me_jd.pricing_date)
    me_eur_call.add_constant('maturity', dt.datetime(2015, 6, 30))
    me_eur_call.add_constant('strike', 38.)
    me_eur_call.add_constant('currency', 'EUR')
    payoff_func = 'np.maximum(maturity_value - strike, 0)'
    eur_call_pos = derivatives_position(
    name='eur_call_pos',
    quantity=5,
    underlying='jd',
    mar_env=me_eur_call,
    otype='European',
    payoff_func=payoff_func)
    
    underlyings = {'gbm': me_gbm, 'jd' : me_jd}
    positions = {'am_put_pos' : am_put_pos, 'eur_call_pos' : eur_call_pos}
    # discounting object for the valuation
    csr = constant_short_rate('csr', 0.06)
    val_env = market_environment('general', me_gbm.pricing_date)
    val_env.add_constant('frequency', 'W')
    # monthly frequency
    val_env.add_constant('paths', 25000)
    val_env.add_constant('starting_date', val_env.pricing_date)
    val_env.add_constant('final_date', val_env.pricing_date)
    # not yet known; take pricing_date temporarily
    val_env.add_curve('discount_curve', csr)
    # select single discount_curve for whole portfolio
    portfolio = derivatives_portfolio(
        name='portfolio',
        positions=positions,
        val_env=val_env,
        assets=underlyings,
        fixed_seed=True)
    portfolio.get_statistics()
    # aggregate over all positions
    portfolio.get_statistics()[['pos_value', 'pos_delta', 'pos_vega']].sum()
