
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from bs4 import BeautifulSoup


def extract_data(xml_file):
    with open(xml_file, 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")  # Using the default XML parser

    frames_data = []

    for frame in Bs_data.find_all('frame'):
        points = frame.find('points').text.strip().split(' ')
        points = [int(point) for point in points]

        # Extracting only the points in the format "X, Y, X, Y"
        formatted_points = [points[i:i + 2] for i in range(0, len(points), 2)]

        frames_data.append({
            'points': formatted_points
        })

    return pd.DataFrame(frames_data)





# Step 2: Data Preparation
def prepare_data(xml_file):
    df = extract_data(xml_file)
    return df


# Step 3: Descriptive Statistics
def descriptive_stats(df):
    print(df.describe())


# Step 3: Data Analysis and Visualization
def plot_visualizations(df):
    # Plot velocity
    plt.figure(figsize=(10, 6))
    plt.plot(df['velocity'], label='Velocity')
    plt.title('Velocity Over Time')
    plt.xlabel('Frame')
    plt.ylabel('Velocity')
    plt.legend()
    plt.show()

    # Plot direction
    plt.figure(figsize=(10, 6))
    plt.plot(df['direction x'], label='Direction X')
    plt.plot(df['direction y'], label='Direction Y')
    plt.title('Direction Over Time')
    plt.xlabel('Frame')
    plt.ylabel('Direction')
    plt.legend()
    plt.show()

    # Plot length and radius
    plt.figure(figsize=(10, 6))
    plt.plot(df['length'], label='Length')
    plt.plot(df['radius'], label='Radius')
    plt.title('Length and Radius Over Time')
    plt.xlabel('Frame')
    plt.ylabel('Value')
    plt.legend()
    plt.show()


# Step 5: Correlation Analysis
def correlation_analysis(df):
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()


if __name__ == "__main__":
    xml_file = 'xml1.xml'
    df = extract_data(xml_file)
    print(df.head())

    #descriptive_stats(df)
    plot_visualizations(df)
    # correlation_analysis(df)
