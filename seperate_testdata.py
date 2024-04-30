import os
import shutil

# Define the source directories and the new test dataset directory
cseq_test_directory = 'Cseq_Data_Test/'
data_directory = 'Street_Network_Data_Raw/'
test_dataset_directory = 'Test_dataset/'

# Function to remove the "_cseq.txt" part from the city names
def clean_city_name_from_cseq(file_name):
    return file_name.replace('_cseq.txt', '')

# Function to remove the "_street_network.csv" part from the city names
def clean_city_name_from_data(file_name):
    return file_name.replace('_street_network.csv', '')

# Create the Test_dataset directory if it does not exist
os.makedirs(test_dataset_directory, exist_ok=True)

# Initialize a counter for successfully processed files
successful_copies = 0

# Iterate over the country folders in the Cseq_Data_Test directory
for country_folder in os.listdir(cseq_test_directory):
    country_folder_path = os.path.join(cseq_test_directory, country_folder)

    # Make sure it's a directory
    if os.path.isdir(country_folder_path):
        # Create the same country structure in the new Test_dataset directory
        country_test_dataset_path = os.path.join(test_dataset_directory, country_folder)
        os.makedirs(country_test_dataset_path, exist_ok=True)

        # Iterate over each .cseq.txt file within the country directory
        for cseq_file in os.listdir(country_folder_path):
            if cseq_file.endswith('_cseq.txt'):
                # Clean the city name from the Cseq file name
                city_name_from_cseq = clean_city_name_from_cseq(cseq_file)
                
                # Look for the corresponding city data in the Data directory
                city_data_folder_path = os.path.join(data_directory, country_folder)
                if os.path.isdir(city_data_folder_path):
                    # Check for the exact city file
                    for data_file in os.listdir(city_data_folder_path):
                        if data_file.endswith('_street_network.csv'):
                            city_name_from_data = clean_city_name_from_data(data_file)

                            # If the city names match exactly, proceed to copy
                            if city_name_from_data == city_name_from_cseq:
                                source_file_path = os.path.join(city_data_folder_path, data_file)
                                destination_file_path = os.path.join(country_test_dataset_path, data_file)

                                # Copy the .csv file to the new Test_dataset directory
                                shutil.copy2(source_file_path, destination_file_path)
                                successful_copies += 1
                                break  # Break the loop since we found the correct city

# Print the total number of successfully processed files
print(f"Total number of city files copied: {successful_copies}")
