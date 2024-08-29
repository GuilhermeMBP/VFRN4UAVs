import os
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Action directions and intensities table
action_table = [
    {"direction": "Direita", "intensity": "Forte"}, #0
    {"direction": "Direita", "intensity": "Média"}, #1
    {"direction": "Direita", "intensity": "Fraca"}, #2
    {"direction": "Direita-Cima", "intensity": "Forte"}, #3
    {"direction": "Direita-Cima", "intensity": "Média"}, #4
    {"direction": "Direita-Cima", "intensity": "Fraca"}, #5
    {"direction": "Cima", "intensity": "Forte"}, #6
    {"direction": "Cima", "intensity": "Média"}, #7
    {"direction": "Cima", "intensity": "Fraca"}, #8
    {"direction": "Voo estacionário", "intensity": "Nula"}, #9
    {"direction": "Esquerda-Cima", "intensity": "Forte"}, #10
    {"direction": "Esquerda-Cima", "intensity": "Média"}, #11
    {"direction": "Esquerda-Cima", "intensity": "Fraca"}, #12
    {"direction": "Esquerda", "intensity": "Forte"}, #13
    {"direction": "Esquerda", "intensity": "Média"}, #14
    {"direction": "Esquerda", "intensity": "Fraca"}, #15
    {"direction": "Esquerda-Baixo", "intensity": "Forte"}, #16
    {"direction": "Esquerda-Baixo", "intensity": "Média"}, #17
    {"direction": "Esquerda-Baixo", "intensity": "Fraca"}, #18
    {"direction": "Baixo", "intensity": "Forte"}, #19
    {"direction": "Baixo", "intensity": "Média"}, #20
    {"direction": "Baixo", "intensity": "Fraca"}, #21
    {"direction": "Direita-Baixo", "intensity": "Forte"}, #22
    {"direction": "Direita-Baixo", "intensity": "Média"}, #23
    {"direction": "Direita-Baixo", "intensity": "Fraca"}  #24
]

# Directions corresponding to the action Y indices
direction_vectors = {
    "Direita": (1, 0),
    "Direita-Cima": (1, 1),
    "Cima": (0, 1),
    "Esquerda-Cima": (-1, 1),
    "Esquerda": (-1, 0),
    "Esquerda-Baixo": (-1, -1),
    "Baixo": (0, -1),
    "Direita-Baixo": (1, -1),
    "Voo estacionário": (0, 0)
}

# Intensity scale factors
intensity_scale = {
    "Forte": 0.2,
    "Média": 0.1,
    "Fraca": 0.05,
    "Nula": 0.0
}

intensity_colors = {
    "Forte": "red",
    "Média": "yellow",
    "Fraca": "green",
    "Nula": "black"
}

# Function to extract data from the file
def extract_data(content):
    x_pattern = re.compile(r'\(X_(\d+)\s+([-\d.]+)\)')
    y_pattern = re.compile(r'\(Y_(\d+)\s+([-\d.]+)\)')
    
    x_values = {int(match[0]): float(match[1]) for match in x_pattern.findall(content)}
    y_values = {int(match[0]): float(match[1]) for match in y_pattern.findall(content)}
    
    return x_values, y_values

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
    parser.add_argument('--directory', required=True, type=str, help='directory containing the counter-examples')
    args = parser.parse_args()
    directory = args.directory

    all_x_values = []
    all_y_values = []

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
