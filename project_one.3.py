import pandas as pd
import plotly.express as px

# Load your cleaned dataset (replace with your file path if needed)
df = pd.read_excel("TBR_USA_Dataset.xlsx")

# Filter for the 1990s
df_1990s = df[(df['Year'] >= 1990) & (df['Year'] <= 1999)]

# Calculate average birth rate per race and age group
heatmap_data = df_1990s.groupby(['Race or Hispanic Origin', 'Age Group'])['Birth Rate'].mean().reset_index()

# Pivot for heatmap structure
heatmap_pivot = heatmap_data.pivot(index='Race or Hispanic Origin', columns='Age Group', values='Birth Rate')

# Create heatmap
fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="Age Group", y="Race or Hispanic Origin", color="Avg Birth Rate"),
    color_continuous_scale="Purples",
    text_auto=True,
    aspect="auto"
)

fig.update_layout(
    title="Average Teen Birth Rate by Race and Age Group (1990–1999)",
    xaxis_title="Age Group",
    yaxis_title="Race or Hispanic Origin"
)

fig.show()
