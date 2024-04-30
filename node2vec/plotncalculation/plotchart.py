import matplotlib.pyplot as plt
import pandas as pd

# Load real data from the CSV file
real_data = pd.read_csv('real_form_factor.csv')

# Load synthetic data from the CSV file
synthetic_data = pd.read_csv('synthetic_form_factor.csv')

# Extract values from synthetic data (assuming it's in the 'Value' column)
synthetic_values = synthetic_data['Value']

# Determine the range of values
min_value = min(real_data['Value'].min(), synthetic_values.min())
max_value = max(real_data['Value'].max(), synthetic_values.max())

# Determine the number of bins based on the range of values
num_bins = 50

# Plot histogram for real data
plt.hist(real_data['Value'], bins=num_bins, range=(min_value, max_value), alpha=0.5, label='Real Data')

# Plot histogram for synthetic data
plt.hist(synthetic_values, bins=num_bins, range=(min_value, max_value), alpha=0.5, label='Synthetic Data')

# Add labels and title
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Form Factor')
plt.legend()

# Set x-axis ticks
plt.xticks(rotation=45)

# Show the plot
plt.show()
