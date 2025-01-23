import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Expose the server for Gunicorn
server = app.server  # <---- Add this line

# Layout of the web app
app.layout = html.Div([
    html.H2("Interactive Sine Wave"),
    
    # Slider for frequency
    dcc.Slider(
        id='freq-slider',
        min=0.1,
        max=10,
        step=0.1,
        value=1,
        marks={i: str(i) for i in range(1, 11)}
    ),
    
    # Graph for plotting
    dcc.Graph(id='plot')
])

# Callback to update the graph when the slider moves
@app.callback(
    Output('plot', 'figure'),
    Input('freq-slider', 'value')
)
def update_plot(frequency):
    x = np.linspace(0, 10, 100)
    y = np.sin(frequency * x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Sine (freq={frequency})'))
    fig.update_layout(title="Sine Wave", xaxis_title="X", yaxis_title="Y")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
