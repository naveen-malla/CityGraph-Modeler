import os
import shutil
import random
from collections import defaultdict

# Define the source and destination directories
source_directory = 'Cseq_Data_Master/'
duplicate_directory = 'Cseq_Data_Train/'
test_directory = 'Cseq_Data_Test/'

# Step 1: Create a complete copy of the original Cseq_Data directory
if not os.path.exists(duplicate_directory):
    shutil.copytree(source_directory, duplicate_directory)

# Step 2: Create a dictionary of countries and their cities
country_cities_dict = defaultdict(list)
for country_folder_name in os.listdir(duplicate_directory):
    country_folder_path = os.path.join(duplicate_directory, country_folder_name)
    if os.path.isdir(country_folder_path):
        for city_file in os.listdir(country_folder_path):
            if city_file.endswith('_cseq.txt'):
                country_cities_dict[country_folder_name].append(city_file)

# Step 3: Pre-determine the number of cities to take from each country
total_cities = sum(len(cities) for cities in country_cities_dict.values())
cities_per_country = {country: int((len(cities) / total_cities) * 4000) for country, cities in country_cities_dict.items()}

# Step 4: Randomly select cities and move them to the test directory
os.makedirs(test_directory, exist_ok=True)
for country, num_cities in cities_per_country.items():
    chosen_cities = random.sample(country_cities_dict[country], min(num_cities, len(country_cities_dict[country])))
    country_test_directory = os.path.join(test_directory, country)
    os.makedirs(country_test_directory, exist_ok=True)

    for city_file in chosen_cities:
        source_city_path = os.path.join(duplicate_directory, country, city_file)
        destination_city_path = os.path.join(country_test_directory, city_file)
        shutil.move(source_city_path, destination_city_path)
        country_cities_dict[country].remove(city_file)

print(f"Random selection and moving of Cseq city files completed.")
