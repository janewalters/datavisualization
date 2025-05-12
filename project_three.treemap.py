import pandas as pd
import plotly.express as px

# Load the Excel file, skipping metadata rows
file_path = "Avian_Influenza_in_wild_birds_findings_2025_-_Week_16_and_Week_17.xlsx"
df = pd.read_excel(file_path, sheet_name='Avian Influenza in wild birds f', skiprows=2)

# Use correct columns for species, count, and pathotype
species_df = df[['Species (Positive)', 'Count', 'Pathotype']].copy()
species_df.columns = ['Species', 'Count', 'Pathotype']

# Drop missing values and filter out Count = 0
species_df = species_df.dropna(subset=['Species', 'Count', 'Pathotype'])
species_df = species_df[species_df['Count'] > 0]

# Group by species and pathotype to sum counts
species_summary = species_df.groupby(['Species', 'Pathotype'], as_index=False)['Count'].sum()

# Calculate the average of the total counts
total_count = species_summary['Count'].sum()
species_summary['Average of Total'] = species_summary['Count'] / total_count * 100  # Percentage of total

# Create an interactive treemap with Plotly
fig = px.treemap(
    species_summary,
    path=['Pathotype', 'Species'],  # Hierarchical path (Pathotype -> Species)
    values='Count',  # Size of the squares
    color='Count',  # Color gradient based on size
    color_continuous_scale='blues',  # Use a gradient color scale
    title="Treemap of Infected Bird Species by Pathotype (Jan-Apr 2025)",
    hover_data={  # Specify the data to include in the hover menu
        'Species': True,
        'Count': True,
        'Pathotype': True  # Flu strain
    }
)

# Customize hover template
fig.update_traces(
    hovertemplate=(
        '<b>Type:</b> %{label}<br>'
        '<b>Count:</b> %{value}<br>'
        '<b>Flu Strain:</b> %{parent}<extra></extra>'
    )
)

# Show the interactive plot
fig.show()
