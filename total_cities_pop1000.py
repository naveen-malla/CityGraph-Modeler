import os

# Base path to the 'Data'/'Cseq' folders containing country folders
base_folder_path = 'Test_dataset_Emb/'  

# Initialize a counter
total_cities_count = 0

# List all country folders in the 'Data' folder
for country_folder_name in os.listdir(base_folder_path):
    country_folder_path = os.path.join(base_folder_path, country_folder_name)
    
    # Check if it's a directory
    if os.path.isdir(country_folder_path):
        # List all CSV files in the country folder
        for city_file_name in os.listdir(country_folder_path):
            if city_file_name.endswith('.emb'):  # Check for CSV/txt extension
                # We assume each CSV file corresponds to a single city's street network
                total_cities_count += 1

# Print the total number of cities
print(f"Total number of cities: {total_cities_count}")
