import pandas as pd               
lb = pd.read_csv('data/10-11_London_Bridge.txt') # Comma-separated .txt file
df = lb.iloc[:, :3]

# Rename columns
df.columns = ['datetime', 'water_level', 'is_high_tide']

# Convert to datetime
df['datetime'] = pd.to_datetime(df['datetime'])

# Convert to float
df['water_level'] = df.water_level.astype(float)

# Create extra month and year columns for easy access
df['month'] = df['datetime'].dt.month
df['year'] = df['datetime'].dt.year

# Filter df for high and low tide
tide_high = df.query('is_high_tide==1')['water_level']
tide_low = df.query('is_high_tide==0')['water_level']

# Create summary statistics
summary_statistics = {'tide_high': {'mean':round(tide_high.mean(),2), 
              'median':round(tide_high.median(),2), 
              'interquartile_range':round((tide_high.quantile(.75) - tide_high.quantile(.25)),2)},
 'tide_low': {'mean':round(tide_low.mean()), 
              'median':round(tide_low.median(),2), 
              'interquartile_range':round((tide_low.quantile(.75) - tide_low.quantile(.25)),2)}}

# Calculate ratio of high tide days
all_high_days = df.query('is_high_tide==1').groupby('year').count()['water_level']
high_days = df.query(f'(water_level>{tide_high.quantile(.75)}) & (is_high_tide==1)').groupby('year').count()['water_level']
high_ratio = (high_days/all_high_days).reset_index()

# Calculate ratio of low tide days
all_low_days = df.query('is_high_tide==0').groupby('year').count()['water_level']
low_days = df.query(f'(water_level<{tide_low.quantile(.25)}) & (is_high_tide==0)').groupby('year').count()['water_level']
low_ratio = (low_days/all_low_days).reset_index()

solution = {'summary_statistics':summary_statistics, 'high_ratio': high_ratio, 'low_ratio':low_ratio}
print(solution)
