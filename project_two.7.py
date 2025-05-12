import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------
# LOAD DATA
# -----------------------

# Load the shapefile (use the .shp file you uploaded)
world = gpd.read_file('/Users/janewalters/Desktop/Data viz portfolio/ne_110m_admin_0_countries')

# Load Excel dataset
df = pd.read_excel("Migration_Dataset.xlsx", sheet_name="FOTM2")

# Clean up and ensure numeric migration counts
df = df[df['Religion'] != 'All']
df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
df = df.dropna(subset=['Count'])

# -----------------------
# PROCESS DATA
# -----------------------

# Group by direction, region, and religion
grouped = df.groupby(['Direction', 'Region', 'Religion'])['Count'].sum().reset_index()

# Pivot to get Incoming and Outgoing in columns
pivot_df = grouped.pivot_table(index=['Region', 'Religion'],
                               columns='Direction',
                               values='Count',
                               fill_value=0).reset_index()

# Calculate Net Migration
pivot_df['Net_Migration'] = pivot_df['Incoming'] - pivot_df['Outgoing']

# -----------------------
# PLOT MAP
# -----------------------

# Define color map for religions
religion_colors = {
    'Christian': '#2443b2',
    'Muslim': '#bda238',
    'Hindu': '#00bf63',
    'Jew': '#ff66c4',
    'Buddhist': '#ff3131',
    'Other': '#8f5d46',  # Brown
    'Unaffiliated': '#b1a1ed',   # Purple 
}


# Start plotting
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, color='lightgrey', edgecolor='black')

# Create a mapping of region names to centroids
region_centroids = {
    'Europe': (-10, 50),
    'Asia-Pacific': (100, 20),
    'Middle East-North Africa': (30, 30),
    'Sub-Saharan Africa': (20, -10),
    'North America': (-100, 40),
    'Latin America-Caribbean': (-70, -10)
}

np.random.seed(42)

# Plot each data point
for _, row in pivot_df.iterrows():
    region = row['Region']
    religion = row['Religion']
    net_mig = row['Net_Migration']
    
    if region not in region_centroids:
        continue  # Skip unmatched regions

    cx, cy = region_centroids[region]

    # Calculate the number of dots (1 dot per 100,000 people)
    num_dots = int(abs(net_mig) / 1000000)

    # Add jitter and plot each dot
    for _ in range(num_dots):
        jitter_x = np.random.uniform(-10, 10)
        jitter_y = np.random.uniform(-10, 10)

        # Offset for negative migration
        direction = -1 if net_mig < 0 else 1
        offset = 10 if net_mig < 0 else 2  # Increase offset for negative migration
        final_x = cx + jitter_x
        final_y = cy + jitter_y + offset * direction

        plt.plot(final_x, final_y, 'o',
                 markersize=4,  # Smaller dots for multiple points
                 color=religion_colors.get(religion, 'gray'),
                 label=religion)

# Build legend without duplicates
handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(), title="Religion")

plt.title("Net Migration by Religion and Region")
plt.axis("off")
plt.show()
