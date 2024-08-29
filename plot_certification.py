import os
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse

point_colors = {
    "unsafe": "red",
    "safe": "green",
    "unknown": "black"
}

def parse_certified_file(file_path):
    # Dictionary to store the results
    results = {
        'unsafe': [],
        'safe': [],
        'unknown': []
    }

    # Regular expressions to match each category and extract indexes
    patterns = {
        'unsafe': re.compile(r'unsafe-pgd \(total \d+\), index: \[(.*?)\]'),
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
def plot_data(all_x_values, all_y_values, parsed_data):
    plt.figure(figsize=(8, 8))

    #Draw the target point
    plt.scatter(1.0, 1.0, color='yellow', linewidths=5, label='Objetivo')
    
    # Draw horizontal line at y=1
    plt.axhline(y=1, color='gray', linestyle='--', linewidth=1, label='y=1')
    
    # Draw vertical line at z=1
    plt.axvline(x=1, color='gray', linestyle='--', linewidth=1, label='z=1')
    
    for k, v in parsed_data.items():
        for index in v:
            x1, x2 = all_x_values[index], all_y_values[index]
            plt.scatter(x1, x2, color=point_colors[k])
            if k == 'safe':
                # Draw a circle with the perturbation radius
                #TODO for now, the radius is fixed to 0.01, it can be parsed from the vnnlib directory name
                circle = plt.Circle((x1, x2), 0.01, color='blue', fill = True, alpha=0.2)
                plt.gca().add_artist(circle)

    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.title('Pontos certificados e violados')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='draw counter-examples from a directory in a plot script')
    parser.add_argument('--file_path', required=True, type=str, help='file containing the certified results')
    parser.add_argument('--directory', required=True, type=str, help='directory containing the dataset (csv files)')
    args = parser.parse_args()
    file_path = args.file_path
    directory = args.directory

    all_x_values = []
    all_y_values = []

    parsed_data = parse_certified_file(file_path)

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                lines = content.strip().split('\n')
                x_values, y_values = float(lines[1]), float(lines[2])
                all_x_values.append(x_values)
                all_y_values.append(y_values)
    
    plot_data(all_x_values, all_y_values, parsed_data)
