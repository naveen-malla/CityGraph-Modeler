import os

# Path to the 'Data' directory
data_directory = 'Cseq_Data_Training/'

# Iterate over the directories in 'Data'
for folder_name in os.listdir(data_directory):
    folder_path = os.path.join(data_directory, folder_name)
    
    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Remove ' ci_' and replace it with '_'
        new_folder_name = folder_name.replace(' ci_', '_')
        new_folder_path = os.path.join(data_directory, new_folder_name)
        
        # Rename the directory
        os.rename(folder_path, new_folder_path)

print("Folders have been renamed.")
