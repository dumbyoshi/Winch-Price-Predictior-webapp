# Importing the libraries
import pickle
import pandas as pd
import webbrowser
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import numpy as np


# Declaring Global variables
print("hello")
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'], suppress_callback_exceptions=True)  # creating object of Dash


# Defining My functions
def load_model():

    global pickle_model
    file = open("F:\Winch Price Prediction Project\pickle_model.pkl", 'rb')
    pickle_model = pickle.load(file)

    global pickle_cTransformer
    file2 = open("F:\Winch Price Prediction Project\pickle_cTransformer.pkl", 'rb')
    pickle_cTransformer = pickle.load(file2)


def estimate_price(family_input, total_weight, steel_produced_weight, components_purchased_weight, items, swl):

    to_predict = [family_input, total_weight, steel_produced_weight,
                  components_purchased_weight, items, swl]
    to_predict = np.array(to_predict)
    to_predict = to_predict.reshape(1, 6)
    to_predict = np.array(pickle_cTransformer.transform(
        to_predict), dtype=np.float32)

    return pickle_model.predict(to_predict)

# to automatically open the browser


def open_browser():
    # pass
    webbrowser.open_new('http://127.0.0.1:8030/')


def create_app_ui():
    main_layout = html.Div(
        [
            html.Div([
                html.H4("Winch Price Prediction", style={
                        'text-align': 'center', 'color': '#007bff'}),
                html.Hr(),
                html.Div([

                    #html.I("Steel Price EUR"),
                    # html.Br(),
                    #dcc.Input(id="steel-price", type="number", placeholder="",className='input-field'),

                    html.I("Family input"),
                    html.Br(),
                    dcc.Dropdown(
                        id='family-input-dropdown',
                        options=[
                            {'label': x, 'value': x} for x in ['En-labber', 'To-labber', 'To-labber med spoleapparat',
                                                               'To-labber med sandwich', 'A-Frame', 'Moonpool hatch', 'Big winch']
                        ],
                        value=None,
                        placeholder='Select a input...',
                    ),
                    html.Br(),


                    html.I("Total weight"),
                    html.Br(),
                    dcc.Input(id="total-weight", type="number",
                              placeholder="", className='input-field'),

                    html.Br(),
                    html.Br(),

                    html.I("Steel Produced weight"),
                    html.Br(),
                    dcc.Input(id="steel-produced-weight", type="number",
                              placeholder="", className='input-field'),

                    html.Br(),
                    html.Br(),

                    html.I("Number of 160 items"),
                    html.Br(),
                    dcc.Input(id="items", type="number",
                              placeholder="", className='input-field'),

                    html.Br(),
                    html.Br(),

                    html.I("Components purchased weight"),
                    html.Br(),
                    dcc.Input(id="components-purchased-weight", type="number",
                              placeholder="", className='input-field'),

                    html.Br(),
                    html.Br(),

                    html.I("SWL"),
                    html.Br(),
                    dcc.Input(id="swl", type="number",
                              placeholder="", className='input-field'),

                    html.Br(),
                    html.Br(),

                    html.Div([
                        dbc.Row([
                            dbc.Col(html.Div(
                                [

                                    dbc.Button(
                                        children='Estimate',
                                        id='button_estimate',
                                        className='est-btn',
                                        color='primary'
                                    )


                                ]
                            ), md=7),


                            dbc.Col(html.Div(
                                [

                                    dbc.Button(
                                        children='Reset',
                                        id='reset_button',
                                        className='est-btn',
                                        color='primary'
                                    )


                                ]
                            ), md=5)



                        ])
                    ],
                        #style={'text-align': 'center'}
                    ),
                    html.Br(),

                    html.Div([

                        html.H5("Total Price NOK :"),
                        html.H5(id='result', style={'color': '#e25f6b'})
                    ])

                ], className='sub-div')

            ], className='main-div'),
        ]
    )
    return main_layout


@app.callback(
    Output('result', 'children'),
    [
        Input('button_estimate', 'n_clicks')
    ],
    [
        State('family-input-dropdown', 'value'),
        State('total-weight', 'value'),
        State('steel-produced-weight', 'value'),
        State('components-purchased-weight', 'value'),
        State('items', 'value'),
        State('swl', 'value'),
    ]

)
def update_app_ui(n_clicks, family_input, total_weight, steel_produced_weight, components_purchased_weight, items, swl):
    if n_clicks != None:

        if(n_clicks > 0):
            price = estimate_price(
                family_input, total_weight, steel_produced_weight, components_purchased_weight, items, swl)
            print(price, "Estimated price")
            return str(np.round(price[0], 2))


@app.callback(

    [
        Output('family-input-dropdown', 'value'),
        Output('total-weight', 'value'),
        Output('steel-produced-weight', 'value'),
        Output('components-purchased-weight', 'value'),
        Output('items', 'value'),
        Output('swl', 'value'),
        #Output('result', 'children')
    ],
    [Input('reset_button', 'n_clicks')],
    [
        State('family-input-dropdown', 'value'),
        State('total-weight', 'value'),
        State('steel-produced-weight', 'value'),
        State('components-purchased-weight', 'value'),
        State('items', 'value'),
        State('swl', 'value'),
    ]

)
def reset_form(n_clicks, family_input, total_weight, steel_produced_weight, components_purchased_weight, items, swl):
    if n_clicks != None:
        if n_clicks > 0:
            return "", "", "", "", "", ""
        else:
            return "", "", "", "", "", ""

    else:
        return "", "", "", "", "", ""

# Main Function to control the Flow of your Project


def main():
    print("Welcome to Dash app...")
    load_model()

    open_browser()

    # If you want to assign something to global variable inside a function, then we have to declare that variable as global.
    # If we are just reading, and not assigning then we don't have to declare global

    global project_name
    project_name = "Winch Price Estimation"

    global app
    app.title = project_name
    app.layout = create_app_ui()
    app.run_server(host='127.0.0.1', port=8030,debug=False)

    print("This would be executed only after the server is down/stopped")

    # Reset all the global variables once the server stops

    app = None
    project_name = None


if __name__ == '__main__':
    main()
