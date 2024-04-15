import pandas as pd

# Read the CSV file
df = pd.read_csv('/Users/naveenmalla/Desktop/RCS/Code/us_cities_over_1000_population.csv')

# Keep only the cities column
df = df[['City']]

# Save the modified DataFrame to a new CSV file
df.to_csv('/Users/naveenmalla/Desktop/RCS/Code/us_cities_over_1000_population.csv', index=False)