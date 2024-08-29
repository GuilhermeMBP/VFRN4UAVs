import os
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse

point_colors = {
    "unsafe": "red",
    "verified": "green",
    "unknown": "black"
}

def parse_certified_file(file_path):
    # Dictionary to store the results
    results = {
        'unsafe-pgd': [],
        'safe': [],
        'unknown': []
    }

    # Regular expressions to match each category and extract indexes
    patterns = {
        'unsafe-pgd': re.compile(r'unsafe-pgd \(total \d+\), index: \[(.*?)\]'),
        'safe': re.compile(r'safe \(total \d+\), index: \[(.*?)\]'),
        'unknown': re.compile(r'unknown \(total \d+\), index: \[(.*?)\]')
    }

    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract indexes for each category
    for category, pattern in patterns.items():
        match = pattern.search(content)
        if match:
            indexes = match.group(1)
            results[category] = [int(i) for i in indexes.split(', ')]

    return results


# Function to plot the data
def plot_data(all_x_values, all_y_values):
    plt.figure(figsize=(8, 8))

    #Draw the target point
    plt.scatter(1.0, 1.0, color='red', linewidths=5, label='Objetivo')
    
    # Draw horizontal line at y=1
    plt.axhline(y=1, color='gray', linestyle='--', linewidth=1, label='y=1')
    
    # Draw vertical line at z=1
    plt.axvline(x=1, color='gray', linestyle='--', linewidth=1, label='z=1')
    
    for x_values, y_values in zip(all_x_values, all_y_values):
        x1, x2 = x_values[1], x_values[2]

        plt.scatter(x1, x2, color='blue')

        # Find the index of the max Y value
        max_y_index = max(y_values, key=y_values.get)

        # Get the direction and intensity for the max Y index
        action = action_table[max_y_index]
        direction = action["direction"]
        intensity = action["intensity"]

        # Get the vector and scale it according to the intensity
        vector = direction_vectors[direction]
        scale = intensity_scale[intensity]
        color = intensity_colors[intensity]

        # Plot the arrow
        plt.quiver(x1, x2, vector[0], vector[1], angles='xy', scale_units='xy', scale=1/scale, color=color, width=0.002)

    # Draw zero-length arrows for each intensity to set the labels
    for intensity, color in intensity_colors.items():
        if intensity == "Nula":
            continue
        plt.quiver(0, 0, 0, 0, color=color, label=f'Intensidade: {intensity}', width=0.002)

    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.title('Contra-exemplos gerados')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='draw counter-examples from a directory in a plot script')
    parser.add_argument('--file_path', required=True, type=str, help='file containing the certified results')
    args = parser.parse_args()
    file_path = args.file_path

    all_x_values = []
    all_y_values = []

    parsed_data = parse_certified_file(file_path)

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                x_values, y_values = extract_data(content)
                all_x_values.append(x_values)
                all_y_values.append(y_values)
    
    plot_data(all_x_values, all_y_values)
