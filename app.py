import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

# Define CMAPS
CMAPS = ["plasma", "inferno", "viridis", "magma", "cividis", "twilight", "coolwarm"]

# Default equations
default_vx = "x*(x-y)"
default_vy = "y*(2*x-y)"

# Initialize app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server  # Required for deployment

# Layout
app.layout = html.Div(style={
    'background': 'linear-gradient(135deg, #f7f7f7, #e0e0e0)',  # Light gradient background
    'fontFamily': '"Roboto", sans-serif',  # Using a modern, professional font
    'color': '#333',  # Dark text for readability
    'padding': '20px',
    'minHeight': '100vh',
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'alignItems': 'center'
}, children=[
    html.H1("2D Flow Plot", style={
        'textAlign': 'center', 
        'color': '#333', 
        'fontSize': '36px',
        'fontWeight': '600',
        'marginBottom': '20px'
    }),

    # Equation input section with explanation
    html.Div([
        html.Label("vx equation (in terms of x, y):", style={'fontSize': '16px', 'color': '#555'}),
        dcc.Input(id="vx-input", type="text", value=default_vx, debounce=True, style={
            "width": "100%", "padding": "10px", "borderRadius": "5px", "border": "1px solid #ddd", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
        }),
        html.Div("Write equations using 'x' and 'y'. Example: 'x*(x-y**2)', 'x**2' for powers.", style={
            'fontSize': '12px', 'color': '#666', 'marginTop': '5px', 'fontStyle': 'italic'
        })
    ], style={'maxWidth': '600px', 'width': '100%', 'paddingBottom': '20px'}),

    html.Div([
        html.Label("vy equation (in terms of x, y):", style={'fontSize': '16px', 'color': '#555'}),
        dcc.Input(id="vy-input", type="text", value=default_vy, debounce=True, style={
            "width": "100%", "padding": "10px", "borderRadius": "5px", "border": "1px solid #ddd", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
        }),
        html.Div("Write equations using 'x' and 'y'. Example: 'y*(2*x-y)', 'x**2' for powers.", style={
            'fontSize': '12px', 'color': '#666', 'marginTop': '5px', 'fontStyle': 'italic'
        })
    ], style={'maxWidth': '600px', 'width': '100%', 'paddingBottom': '20px'}),

    # Line thickness and colormap dropdown placed side by side
    html.Div([
        html.Div([
            html.Label("Min Line Thickness:", style={'fontSize': '14px', 'color': '#555'}),
            dcc.Input(id="min-thickness", type="number", value=0.5, step=0.1, style={
                "width": "100%", "padding": "8px", "borderRadius": "5px", "border": "1px solid #ddd", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "height": "50px"  # Reduced height
            }),
        ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px', 'boxSizing': 'border-box'}),

        html.Div([
            html.Label("Max Line Thickness:", style={'fontSize': '14px', 'color': '#555'}),
            dcc.Input(id="max-thickness", type="number", value=3.0, step=0.1, style={
                "width": "100%", "padding": "8px", "borderRadius": "5px", "border": "1px solid #ddd", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "height": "50px"  # Reduced height
            }),
        ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px', 'boxSizing': 'border-box'}),

        html.Div([
            html.Label("Choose Colormap:", style={'fontSize': '14px', 'color': '#555'}),
            dcc.Dropdown(
                id="cmap-dropdown",
                options=[{"label": cmap, "value": cmap} for cmap in CMAPS],
                value="plasma",
                clearable=False,
                style={
                    'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ddd', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    "height": "50px",  # Set the height of the dropdown button
                    "minHeight": "35px",  # Ensure the dropdown button height is consistent
                },
                className="dropdown-style"  # Custom class for more control
            ),
        ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px', 'boxSizing': 'border-box'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px', 'maxWidth': '1000px'}),

    # # Line thickness and colormap dropdown placed side by side
    # html.Div([
    #     html.Div([
    #         html.Label("Min Line Thickness:", style={'fontSize': '14px', 'color': '#555'}),
    #         dcc.Input(id="min-thickness", type="number", value=0.5, step=0.1, style={
    #             "width": "100%", "padding": "10px", "borderRadius": "5px", "border": "1px solid #ddd", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    #             "height": "50px"  # Set the height explicitly
    #         }),
    #     ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px', 'boxSizing': 'border-box'}),

    #     html.Div([
    #         html.Label("Max Line Thickness:", style={'fontSize': '14px', 'color': '#555'}),
    #         dcc.Input(id="max-thickness", type="number", value=3.0, step=0.1, style={
    #             "width": "100%", "padding": "10px", "borderRadius": "5px", "border": "1px solid #ddd", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    #             "height": "50px"  # Set the height explicitly
    #         }),
    #     ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px', 'boxSizing': 'border-box'}),

    #     html.Div([
    #         html.Label("Choose Colormap:", style={'fontSize': '14px', 'color': '#555'}),
    #         dcc.Dropdown(
    #             id="cmap-dropdown",
    #             options=[{"label": cmap, "value": cmap} for cmap in CMAPS],
    #             value="plasma",
    #             clearable=False,
    #             style={
    #                 'width': '100%', 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #ddd', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    #                 "height": "50px"  # Set the height explicitly
    #             }
    #         ),
    #     ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px', 'boxSizing': 'border-box'}),
    # ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px', 'maxWidth': '1000px'})


    # Streamplot Image
    html.Div([
        html.Img(id="streamplot", style={'width': '100%', 'maxWidth': '800px', 'marginTop': '20px'})
    ], style={'textAlign': 'center'}),

    # Error message section
    html.Div([
        html.Div(id="error-message", style={
            'color': 'red',
            'fontSize': '16px',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'visibility': 'hidden',  # Initially hidden
            'marginTop': '20px'
        })
    ], style={'padding': '10px'}),

    # Footer/Help Section
    html.Div([
        html.H5("How to Write Equations", style={'textAlign': 'center', 'color': '#333'}),
        html.P("When entering the equations, use '*' for multiplication. For example:", style={'textAlign': 'center', 'color': '#555'}),
        html.P("Correct: '2*x', Incorrect: '2x'.", style={'textAlign': 'center', 'fontSize': '14px', 'color': '#555'}),
        html.P("To write powers, use '**' (e.g., 'x**2' for x squared, 'x**2.5' for a decimal power).", style={'textAlign': 'center', 'fontSize': '14px', 'color': '#555'}),
    ], style={'padding': '20px', 'backgroundColor': '#f7f7f7', 'borderTop': '1px solid #ddd'})
])


# Callback to update the plot
@app.callback(
    Output("streamplot", "src"),
    Output("error-message", "style"),
    Input("vx-input", "value"),
    Input("vy-input", "value"),
    Input("min-thickness", "value"),
    Input("max-thickness", "value"),
    Input("cmap-dropdown", "value"),
)
def update_plot(vx_eq, vy_eq, min_thickness, max_thickness, cmap):
    try:
        # Grid resolution
        r = np.linspace(-20, 20, 100)
        x, y = np.meshgrid(r, r)

        # Using eval to dynamically calculate the equations
        vx = eval(vx_eq)  # This will calculate vx based on the input equation
        vy = eval(vy_eq)  # Similarly for vy

        # Calculate streamplot
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.streamplot(x, y, vx, vy, color=vx, linewidth=2, cmap=cmap, density=2)

        # Save plot to BytesIO to send as base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_str = "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')

        # Hide error message
        return img_str, {'visibility': 'hidden'}

    except Exception as e:
        # Display error message if the plot cannot be rendered
        return "", {'visibility': 'visible'}

if __name__ == "__main__":
    app.run_server(debug=True)
