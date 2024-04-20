import os

# Base directory containing the Cseq_Data folders with country Cseq files
cseq_data_base_directory = 'Cseq_Data_Training/'

# Path for the master Cseq file
master_cseq_file_path = 'training_cseq.txt'

# Make sure the master Cseq file is empty before we start appending data
with open(master_cseq_file_path, 'w') as master_file:
    master_file.write('')

# Iterate over each country folder in the Cseq_Data directory
for country_folder_name in os.listdir(cseq_data_base_directory):
    country_folder_path = os.path.join(cseq_data_base_directory, country_folder_name)

    # Skip if it's not a directory
    if not os.path.isdir(country_folder_path):
        continue

    # Iterate over each Cseq file in the country folder
    for cseq_file_name in os.listdir(country_folder_path):
        if cseq_file_name.endswith("_cseq.txt"):
            cseq_file_path = os.path.join(country_folder_path, cseq_file_name)
            
            # Read the contents of the Cseq file
            with open(cseq_file_path, 'r') as cseq_file:
                cseq_data = cseq_file.read().strip()
            
            # Append the contents to the master Cseq file, with a newline separating entries
            with open(master_cseq_file_path, 'a') as master_file:
                master_file.write(cseq_data + '\n\n')

print(f"All Cseq data has been appended to {master_cseq_file_path}.")
