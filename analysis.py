import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d


# extracts data form xml
def extract_data_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    player_points = []
    for frame in root.findall('.//frame'):
        x = float(frame.find('x').text)
        y = float(frame.find('y').text)
        speed = float(frame.find('velocity').text)
        player_data.append({'x': x, 'y': y, 'velocity': speed})
    return player_data

# Process XML files and extract data
xml_files = ['user1_game1.xml', 'user1_game2.xml', 'user2_game1.xml']  # Add more XML files as needed
all_player_data = []

for xml_file in xml_files:
    player_data = extract_data_from_xml(xml_file)
    all_player_data.extend(player_data)

# Extract x, y positions and velocity
x_positions = [point['x'] for point in all_player_data]
y_positions = [point['y'] for point in all_player_data]
velocity = [point['velocity'] for point in all_player_data]

# Heatmap generation
plt.figure(figsize=(8, 6))
plt.hexbin(x_positions, y_positions, gridsize=30, cmap='inferno')
plt.colorbar(label='Number of points')
plt.title('Player Movement Heatmap')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()

# Action Sequence Mining
# Convert x, y positions and velocity into DataFrame
df = pd.DataFrame({'x': x_positions, 'y': y_positions, 'velocity': velocity})

# Group actions by velocity
velocity_groups = df.groupby('velocity')

# Display top 5 action sequences for each velocity group
for velocity, group in velocity_groups:
    print(f"Velocity: {velocity}")
    action_sequences = group[['x', 'y']].apply(lambda x: ' '.join(x.astype(str)), axis=1).value_counts().head(5)
    print(action_sequences)
    print("\n")
