import os
import csv
import subprocess

# Constants
MAX_TOKENS = 1024  # Adjustable maximum token capacity of the GPT model

# Define the root directory of the test data and the target output directory
root_test_dir = 'Cseq_Data_Test'  # Replace with the actual path to your data
root_output_dir = 'Cseq_Predicted'

def get_cseq_files(directory):
    """Traverse the directory structure and get all the cseq files."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('_cseq.txt'):
                yield os.path.join(root, file)

def read_coordinates(file_path):
    """Read all coordinates from a cseq file."""
    with open(file_path, 'r') as file:
        data = file.read()
        coordinates = data.split()
    return coordinates

def predict_and_validate_coordinates(coordinates, max_new_tokens):
    """Run the model prediction command with a specified number of new tokens and validate the output."""
    start_len = int(len(coordinates) * 0.20)  # Using 20% of coordinates as the start sequence
    
    if start_len % 2 != 0:  # making the starting sequence length even for pairs of coordinates
        start_len -= 1

    coordinates_str = ' '.join(coordinates[:start_len])

    if start_len < 6:  # if coordinates are less than 6 the starting sequence will be only 2 coordinate pairs
        # Validate range and form pairs
        coord_pairs = []
        print(f"Coordinates: {coordinates}")
        for i in range(0, len(coordinates), 2):
            x, y = int(coordinates[i]), int(coordinates[i + 1])
            coord_pairs.append((x, y))
        print(f"Coordinate pairs: {coord_pairs}")
        return coord_pairs
        
    print("Coordinates Start Sequence: ", coordinates_str)
    command = f"python sample.py --out_dir=out-osm-1024-20000 --start=\"{coordinates_str}\" --max_new_tokens={max_new_tokens}"
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        lines = output.split('\n')
        for i, line in enumerate(lines):
            if 'Loading meta from data/osm/meta.pkl...' in line:
                output = '\n'.join(lines[i+1:])
                break
        else:
            return []

        # Process and validate coordinates
        coords = output.split()
        if len(coords) % 2 == 0:
            coords = coords[:-2]  # Remove last pair if even count
        else:
            coords = coords[:-3]  # Remove last three values if odd count
        
        # Validate range and form pairs
        valid_coords = []
        for i in range(0, len(coords), 2):
            try:
                x, y = int(coords[i]), int(coords[i + 1])
                if 0 <= x <= 255 and 0 <= y <= 255:
                    valid_coords.append((x, y))
            except IndexError:
                continue  # Skip if there's no pair
        # print(f"Valid cords: {valid_coords}")
        return valid_coords
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the model: {e}")
        return []


def calculate_tokens(num_coordinates):
    """Estimate the number of tokens required for the given number of coordinates."""
    return int(num_coordinates * 3.20)  # Adjust based on the calculated ratio from your empirical data

def split_and_predict(coordinates):
    """Split the coordinates into manageable parts and predict and validate each part."""
    part_size = int(MAX_TOKENS / 3.20)  # Approximation from token-to-coordinate ratio
    parts = [coordinates[i:i + part_size] for i in range(0, len(coordinates), part_size)]
    valid_coords = []
    for part in parts:
        part_tokens_required = calculate_tokens(len(part) + 2)  # Include buffer
        validated_part = predict_and_validate_coordinates(part, part_tokens_required)
        if validated_part:
            valid_coords.extend(validated_part)  # Append valid coordinate pairs directly
    return valid_coords


def save_to_csv(valid_coords, output_dir, filename):
    """Save validated coordinates to a CSV file."""
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, filename)
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['nodeId', 'X', 'Y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx, (x, y) in enumerate(valid_coords):
            writer.writerow({'nodeId': idx, 'X': x, 'Y': y})

if __name__ == '__main__':
    for cseq_file in get_cseq_files(root_test_dir):
        print(f"Processing {cseq_file}")
        coordinates = read_coordinates(cseq_file)
        required_tokens = calculate_tokens(len(coordinates) + 2)  # Including buffer for safety
        if required_tokens <= MAX_TOKENS:
            valid_coords = predict_and_validate_coordinates(coordinates, required_tokens)
        else:
            valid_coords = split_and_predict(coordinates)  # Uses the updated function
        if valid_coords:
            rel_path = os.path.relpath(cseq_file, root_test_dir)
            output_dir = os.path.join(root_output_dir, os.path.dirname(rel_path))
            save_to_csv(valid_coords, output_dir, os.path.basename(cseq_file).replace('.txt', '.csv'))
            print(f"Processed {cseq_file}")
    print("All cities processed. Check the 'Cseq_Predicted' directory for output CSV files.")
