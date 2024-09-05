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
        'safe': re.compile(r'\[.*?\],False'),
        'unsafe': re.compile(r'\[.*?\],True'),
        'unknown': re.compile(r'\[.*?\],---')
    }

    # Read the file content
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Extract indexes for each category
    for i, line in enumerate(content):
        for category, pattern in patterns.items():
            if pattern.search(line):
                results[category].append(i)

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
            x1, x2 = all_x_values[index-4], all_y_values[index-4]
            plt.scatter(x1, x2, color=point_colors[k], s=1)
            # Draw a circle with the perturbation radius
            circle = plt.Circle((x1, x2), 0.01, color= 'red' if k != 'safe' else 'blue', fill = True, alpha=0.2)
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
    parser.add_argument('--results_path', required=True, type=str, help='csv containing the certified results')
    parser.add_argument('--directory', required=True, type=str, help='directory containing the dataset (csv files)')
    args = parser.parse_args()
    results_path = args.results_path
    directory = args.directory

    all_x_values = []
    all_y_values = []

    parsed_data = parse_certified_file(results_path)

    # Iterate through the files in the directory
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                lines = content.strip().split('\n')
                x_values, y_values = float(lines[1]), float(lines[2])
                all_x_values.append(x_values)
                all_y_values.append(y_values)
    
    plot_data(all_x_values, all_y_values, parsed_data)
