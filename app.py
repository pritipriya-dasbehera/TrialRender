import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

# Function to compute polynomial roots
def poly(h, a, b):
    return np.polynomial.Polynomial([h, a, 0, -b])

def rroots(h, a, b):
    p = poly(h, a, b)
    rts = p.roots()
    rtyp = p.deriv(1)(rts)

    stab_r = np.real(rts[np.logical_and(np.imag(rts) == 0, np.real(rtyp) <= 0)])
    unstab_r = np.real(rts[np.logical_and(np.imag(rts) == 0, np.real(rtyp) > 0)])

    return [stab_r, unstab_r]

# Constants
b = 1
ass = np.linspace(-10, 10, 200)

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Required for deployment

# Layout
app.layout = html.Div([
    html.H1("Interactive Polynomial Root Visualization"),
    
    # Slider for h
    html.Label("h value:"),
    dcc.Slider(id='h-slider', min=-5, max=5, step=0.1, value=0.1,
               marks={i: str(i) for i in range(-5, 6)}),

    # Slider for a
    html.Label("a value:"),
    dcc.Slider(id='a-slider', min=-10, max=10, step=0.1, value=0.0,
               marks={i: str(i) for i in range(-10, 11, 2)}),

    # Graphs
    dcc.Graph(id='plot-a'),
    dcc.Graph(id='plot-h')
])

# Callback to update both plots
@app.callback(
    [Output('plot-a', 'figure'), Output('plot-h', 'figure')],
    [Input('h-slider', 'value'), Input('a-slider', 'value')]
)
def update_plots(h_val, a_val):
    # Compute roots for plot 1 (rroot vs a)
    y_values_a = np.array([rroots(h_val, a, b) for a in ass], dtype=object)
    blue_y_a = np.concatenate(y_values_a.T[0])
    blue_x_a = np.concatenate([np.full_like(y, a) for y, a in zip(y_values_a.T[0], ass)])
    red_y_a = np.concatenate(y_values_a.T[1])
    red_x_a = np.concatenate([np.full_like(y, a) for y, a in zip(y_values_a.T[1], ass)])

    # Compute roots for plot 2 (rroot vs h)
    y_values_h = np.array([rroots(h, a_val, b) for h in ass], dtype=object)
    blue_y_h = np.concatenate(y_values_h.T[0])
    blue_x_h = np.concatenate([np.full_like(y, h) for y, h in zip(y_values_h.T[0], ass)])
    red_y_h = np.concatenate(y_values_h.T[1])
    red_x_h = np.concatenate([np.full_like(y, h) for y, h in zip(y_values_h.T[1], ass)])

    # Create figure 1 (rroot vs a)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=blue_x_a, y=blue_y_a, mode='markers', marker=dict(color='blue', size=3), name='Stable Roots'))
    fig1.add_trace(go.Scatter(x=red_x_a, y=red_y_a, mode='markers', marker=dict(color='red', size=3), name='Unstable Roots'))
    fig1.update_layout(title=f"Roots vs a (h = {h_val:.2f})", xaxis_title="a", yaxis_title="Roots")

    # Create figure 2 (rroot vs h)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=blue_x_h, y=blue_y_h, mode='markers', marker=dict(color='blue', size=3), name='Stable Roots'))
    fig2.add_trace(go.Scatter(x=red_x_h, y=red_y_h, mode='markers', marker=dict(color='red', size=3), name='Unstable Roots'))
    fig2.update_layout(title=f"Roots vs h (a = {a_val:.2f})", xaxis_title="h", yaxis_title="Roots")

    return fig1, fig2

# Run app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
