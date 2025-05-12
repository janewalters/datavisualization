import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_excel("TBR_USA_Dataset.xlsx")

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Teen Birth Rates Explorer"

# Layout
app.layout = html.Div([
    html.H2("Teen Birth Rates in the U.S. (by Race and Age Group)", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Race or Ethnicity:"),
        dcc.Dropdown(
            id='race-dropdown',
            options=[{'label': race, 'value': race} for race in sorted(df['Race or Hispanic Origin'].unique())],
            value='Hispanic',
            clearable=False
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Age Group:"),
        dcc.Dropdown(
            id='age-dropdown',
            options=[{'label': age, 'value': age} for age in sorted(df['Age Group'].unique())],
            value='All Ages',
            clearable=False
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='line-graph')
])

# Callback to update the graph
@app.callback(
    Output('line-graph', 'figure'),
    Input('race-dropdown', 'value'),
    Input('age-dropdown', 'value')
)
def update_graph(selected_race, selected_age):
    filtered_df = df[
        (df['Race or Hispanic Origin'] == selected_race) &
        (df['Age Group'] == selected_age)
    ]
    
    fig = px.line(
        filtered_df,
        x='Year',
        y='Birth Rate',
        title=f"Teen Birth Rate Over Time ({selected_race}, {selected_age})",
        markers=True
    )

    fig.update_layout(
        yaxis_title='Birth Rate per 1,000',
        xaxis_title='Year',
        template='plotly_white'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
