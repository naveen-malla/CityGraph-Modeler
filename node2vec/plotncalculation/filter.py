# import pandas as pd

# # Load real data from the first CSV file
# real_data = pd.read_csv('real_circuity.csv')

# # Load synthetic data from the second CSV file
# synthetic_data = pd.read_csv('syn_avg_circuity.csv', sep=':', encoding='latin1')

# # Extract unique cities from both datasets
# real_cities = set(real_data['City'])
# synthetic_cities = set(synthetic_data['City'])

# # Find common cities
# common_cities = real_cities.intersection(synthetic_cities)

# # Filter real data to keep only common cities
# real_common_data = real_data[real_data['City'].isin(common_cities)]

# # Filter synthetic data to keep only common cities
# synthetic_common_data = synthetic_data[synthetic_data['City'].isin(common_cities)]

# # Save filtered datasets to new CSV files
# real_common_data.to_csv('real_circuity.csv', index=False)
# synthetic_common_data.to_csv('syn_avg_circuity.csv', index=False)


import pandas as pd

# Load synthetic data from the second CSV file
real_data = pd.read_csv('real_form_factor.csv', sep=':', encoding='latin1')

# Load synthetic data from the second CSV file
synthetic_data = pd.read_csv('syn_avg_form_factor.csv', sep=':', encoding='latin1')

# Extract unique cities from both datasets
real_cities = set(real_data['City'])
synthetic_cities = set(synthetic_data['City'])

# Find common cities
common_cities = real_cities.intersection(synthetic_cities)

# Filter real data to keep only common cities
real_common_data = real_data[real_data['City'].isin(common_cities)]

# Filter synthetic data to keep only common cities
synthetic_common_data = synthetic_data[synthetic_data['City'].isin(common_cities)]

# Save filtered datasets to new CSV files
real_common_data.to_csv('real_form_factor.csv', index=False)
synthetic_common_data.to_csv('syn_avg_form_factor.csv', index=False)
