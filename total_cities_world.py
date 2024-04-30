import os

# this code counts the total cities in the world obtained from the Overpass API

folder_path = "cities"  

city_count = 0

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            city_count += len(file.readlines())

print("Total number of cities:", city_count)