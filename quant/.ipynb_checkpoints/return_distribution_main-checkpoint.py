from return_distribution import*

# Load Config
config_file = os.path.join(os.path.dirname("__file__"), 'Config/config.ini')
config = configparser.ConfigParser(allow_no_value=True)
config.read(config_file)

dest_dir=os.path.join(os.path.dirname("__file__"),config['develop']['dest_dir'])
src_dir=os.path.join(os.path.dirname("__file__"),config['develop']['src_dir'])

if __name__ == "__main__":
    daily_df, weekly_df, monthly_df, quarterly_df = read_data(sticker='NVDA', start_date='2013-01-07', end_date='2023-03-30',
                                                             start='2013-01-07', end='2023-03-30')
    Load(dest_dir=dest_dir, sticker='NVDA', daily_data=daily_df, weekly_data=weekly_df, monthly_data=monthly_df, quarterly_data=quarterly_df, file_name='nvidia-returns', file_extension='.xlsx')
    
    
    