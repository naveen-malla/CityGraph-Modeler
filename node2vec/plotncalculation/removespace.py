import pandas as pd

# Load the CSV file
data = pd.read_csv('syn_avg_form_factor.csv')

# Remove leading and trailing spaces from the 'Value' column
data['Value'] = data['Value'].str.strip()

# Save the modified DataFrame back to a CSV file
data.to_csv('syn_avg_form_factor.csv', index=False)
