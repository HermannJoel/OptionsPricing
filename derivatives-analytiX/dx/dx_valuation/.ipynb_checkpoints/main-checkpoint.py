#main 

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
    
    %time paths_1 = gbm.get_instrument_values()
    paths_1
    
    gbm.update(volatility=0.5)
    %time paths_2 = gbm.get_instrument_values()
    
    plt.figure(figsize=(8, 4))
    p1 = plt.plot(gbm.time_grid, paths_1[:, :10], 'b')
    p2 = plt.plot(gbm.time_grid, paths_2[:, :10], 'r-.')
    plt.grid(True)
    l1 = plt.legend([p1[0], p2[0]],
    ['low volatility', 'high volatility'], loc=2)
    plt.gca().add_artist(l1)
    plt.xticks(rotation=30)