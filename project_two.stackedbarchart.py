import pandas as pd
import matplotlib.pyplot as plt

# Load Excel file and sheet
xls = pd.ExcelFile("Incoming and Outgoing Migrant Counts.xlsx")
df = xls.parse('FOTM2')

# Convert columns to appropriate types
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Percent'] = pd.to_numeric(df['Percent'], errors='coerce')

# Filter for 2020, outgoing migration, and exclude 'All' religions
df_2020_outgoing = df[
    (df['Year'] == 2020) &
    (df['Direction'] == 'Incoming') &
    (df['Religion'].str.lower() != 'all')
]

# Drop rows with missing values
df_2020_outgoing = df_2020_outgoing.dropna(subset=['Religion', 'Region', 'Percent'])

# Group by Region and Religion (average % if multiple entries)
grouped = df_2020_outgoing.groupby(['Region', 'Religion'])['Percent'].mean().unstack(fill_value=0)

# Ensure "Global" is the leftmost column
if 'Global' in grouped.index:
    grouped = grouped.reindex(['Global'] + [region for region in grouped.index if region != 'Global'])

# Rename religion labels
grouped = grouped.rename(columns={
    'Christian': 'Christianity',
    'Muslim': 'Islam',
    'Hindu': 'Hinduism',
    'Buddhist': 'Buddhism',
    'Jew': 'Judaism',
})

# Update the custom colors dictionary to match the new labels
custom_colors = {
    'Christianity': '#2443b2',  # Blue
    'Islam': '#bda238',         # Yellow
    'Hinduism': '#00bf63',      # Green
    'Buddhism': '#ff3131',      # Red
    'Judaism': '#ff66c4',       # Pink
    'Other': '#8f5d46',  # Brown
    'Unaffiliated': '#b1a1ed',   # Purple 
}

# Map the colors to the renamed religions
religion_colors = [custom_colors[religion] for religion in grouped.columns]

# Plot stacked bar chart with updated labels and colors
ax = grouped.plot(kind='bar', stacked=True, figsize=(12, 7), color=religion_colors)

plt.title('Incoming Migration by Religion and Region (2020, %)', fontsize=14)
plt.xlabel('Region')
plt.ylabel('Percent of Migrants')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Religion', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
