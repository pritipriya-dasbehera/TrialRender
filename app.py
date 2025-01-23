import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import io
import base64

# Define symbolic variables
x, y = sp.symbols("x y")

# Default equations
default_vx = "x*(x-y**2)"
default_vy = "y*(2*x-y)"

# List of Matplotlib colormaps
CMAPS = ["plasma", "viridis", "inferno", "magma", "cividis", 
         "coolwarm", "twilight", "jet", "turbo"]

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Required for deployment

# Layout
app.layout = html.Div([
    html.H1("Enhanced Streamplot Generator"),

    html.Label("vx equation (in terms of x, y):"),
    dcc.Input(id="vx-input", type="text", value=default_vx, debounce=True, style={"width": "100%"}),

    html.Label("vy equation (in terms of x, y):"),
    dcc.Input(id="vy-input", type="text", value=default_vy, debounce=True, style={"width": "100%"}),

    html.Label("Choose Colormap:"),
    dcc.Dropdown(
        id="cmap-dropdown",
        options=[{"label": cmap, "value": cmap} for cmap in CMAPS],
        value="plasma",
        clearable=False
    ),

    html.Label("Min Line Thickness:"),
    dcc.Input(id="min-thickness", type="number", value=0.5, step=0.1),

    html.Label("Max Line Thickness:"),
    dcc.Input(id="max-thickness", type="number", value=3.0, step=0.1),

    html.Img(id="streamplot")
])

# Function to compute velocity field
def compute_velocity_field(vx_expr, vy_expr, res=100):
    try:
        # Convert to sympy expressions
        vx_sym = sp.sympify(vx_expr)
        vy_sym = sp.sympify(vy_expr)

        # Convert to numerical functions using 'numpy' mode
        vx_func = sp.lambdify((x, y), vx_sym, "numpy")
        vy_func = sp.lambdify((x, y), vy_sym, "numpy")

        # Create meshgrid
        r = np.linspace(-5, 5, res)
        x_vals, y_vals = np.meshgrid(r, r)

        # Compute velocity field
        vx_vals = vx_func(x_vals, y_vals)
        vy_vals = vy_func(x_vals, y_vals)

        return x_vals, y_vals, vx_vals, vy_vals

    except Exception as e:
        print(f"Error in function evaluation: {e}")
        return None, None, None, None

# Function to generate streamplot
def generate_streamplot(vx_expr, vy_expr, cmap, min_thickness, max_thickness):
    x_vals, y_vals, vx_vals, vy_vals = compute_velocity_field(vx_expr, vy_expr)

    if x_vals is None:
        return None  # Return None if error occurs

    # Compute speed (for color and linewidth)
    speed = np.sqrt(vx_vals**2 + vy_vals**2)

    # Use logarithmic scaling to prevent extreme variation in line width
    speed_scaled = np.log1p(speed)  # Log-scaling for better balance
    linewidths = min_thickness + (speed_scaled / np.max(speed_scaled)) * (max_thickness - min_thickness)

    # Create Matplotlib streamplot
    fig, ax = plt.subplots(figsize=(6, 6))
    strm = ax.streamplot(x_vals, y_vals, vx_vals, vy_vals, 
                         color=speed, linewidth=linewidths,
                         cmap=cmap, arrowsize=1)

    # Add colorbar
    cbar = fig.colorbar(strm.lines)
    cbar.set_label("Speed Magnitude")

    ax.set_title(f"Streamplot with Colormap: {cmap}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Convert plot to image
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    plt.close(fig)
    img.seek(0)

    return "data:image/png;base64," + base64.b64encode(img.read()).decode()

# Callback to update the streamplot
@app.callback(
    Output("streamplot", "src"),
    [Input("vx-input", "value"), Input("vy-input", "value"),
     Input("cmap-dropdown", "value"),
     Input("min-thickness", "value"), Input("max-thickness", "value")]
)
def update_plot(vx_expr, vy_expr, cmap, min_thickness, max_thickness):
    return generate_streamplot(vx_expr, vy_expr, cmap, min_thickness, max_thickness)

# Run app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=5000)
