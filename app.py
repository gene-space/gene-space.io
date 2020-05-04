import sqreen
sqreen.start()
#### HOUSEKEEPING ####
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd 
import time
from flower_functions import *

#### DASH APP DESIGN ####
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {'background': 'powderblue', 'text': 'maroon'}

app.layout = html.Div(style = {'backgroundColor': colors['background']}, children=[

    # Title
    html.H1(children='Gene Space', style = {'textAlign': 'center', 'color': colors['text']}),

    # Authorship
    html.Div(children='Author: Akred', style={'textAlign':'center', 'color':colors['text']}),

    # Short description
    html.Div(children='''
        Choose your desired flower species (excluding roses), and then input the genotypes (numeric format) for 
        the desired parents to see the possible offspring along with their probabilities.
    ''', style = {'textAlign': 'center', 'color':colors['text']}),

    # Flower species selection
    html.Div([
    html.Div([
        html.Label('Flower Species Selection', style={'textAlign':'center', 'color':colors['text']}),
        dcc.Dropdown(id = 'flower-selection',
            options=[
                {'label': 'Tulip', 'value': 'tulip'},
                {'label': 'Hyacinth', 'value': 'hyacinth'},
                {'label': 'Cosmo', 'value': 'cosmo'},
                {'label': 'Windflower', 'value': 'windflower'},
                {'label': 'Mum', 'value': 'mum'},
                {'label': 'Pansy', 'value': 'pansy'},
                {'label': 'Lily', 'value': 'lily'},
                ],
            value='lily'),        
    ],style = {'width': '30%', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center'},),    
    ], style={'width':'100%', 'text-align':'center'}),

    # Parent inputs
    html.Label('Parent Selection: Input 3 digits, each between 0 and 2, uniquely identifying the genotype. Ex: 200', 
                    style={'textAlign':'center', 'color':colors['text']}),
    html.Div([        
        # Parent 1
        html.Div([
            html.Label('Parent 1', style={'textAlign':'center', 'color':colors['text']}),
            html.Div([
                dcc.Input(id='parent1-input', value='111', type='text'),
            ], style={'width':'100%', 'display':'inline-block', 'align-items':'center', 'justify-content':'center'}),            
        ], style={'width': '48%', 'display': 'inline-block'}),

        # Parent 2
        html.Div([
            html.Label('Parent 2', style={'textAlign':'center', 'color':colors['text']}),
            html.Div([
                dcc.Input(id='parent2-input', value='111', type='text'),
            ], style={'width':'100%', 'display':'flex', 'align-items':'center', 'justify-content':'center'})
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'text-align':'center'}),

    # Gene-space plot   
    html.Div([ 
        html.Div([
            dcc.Graph(id = 'gene-space'),
        ], style={'width':'700px', 'display':'inline-block'}),    
    ], style={'width':'100%', 'textAlign':'center'}),

    # Some explanation of the utility
    html.Div(children='''
        This aids in understanding the breeding paths, as it illuminates "genetic distance." 
        A few intuitive benefits: \n
        1. The value of island hybrids are made strikingly clear, because they are so much closer 
        to the otherwise rarer hybrids (purple windflowers, purple pansies, etc.) 
        2. Homozygosity is easily interpreted. Homozygous in only one gene means the flower lives on 
        one of the faces of the cube; in two genes: on the edges; and full homozygosity implies the flower
        is a corner of the cube.
        3. The "universal hybrid" (from which all other genotypes can be bred from via homogeneous
        cross-breeding), is simply the center of the cube.
    ''', style = {'textAlign':'center', 'color':colors['text']}),

    # Short credits
    html.Div(children='''
        Credits: to the Garden-Science discord for providing the information/background & gene flags.
    ''', style = {'textAlign': 'center', 'color':colors['text']}),     
])

@app.callback(
    Output(component_id='gene-space', component_property='figure'),
    [Input(component_id='flower-selection', component_property='value'),
    Input(component_id='parent1-input', component_property='value'),
    Input(component_id='parent2-input', component_property='value')]
)
def update_flower_fig(input_flower,parent1,parent2):
    def split(word): 
        return [int(char) for char in word] 
    # flwr = 'hyacinth' # choose the flower
    # par1 = [2,1,0] # choose the parents
    # par2 = [1,2,2]

    flwr = input_flower
    par1 = split(parent1)
    par2 = split(parent2)

    #### LOAD & CLEAN DF ####
    df = pd.read_csv('flower_flags_' + flwr + '.csv')

    # Clean it
    df['Kind'] = df['Color'].apply(findSeednIsland) # add col for seed/hybrid label
    df['Color'] = df['Color'].apply(removeSeed) # remove (seed) from color string
    df['Color'] = df['Color'].apply(removeIsland)
    df['Numeric'] = df['Numeric'].apply(lambda x: x.replace('/',' - ').replace('00','0').replace('01','1').replace('02','2'))

    #### PLOTTING ####
    # Get locations and properties of full gene-space
    x = [None]*27; y = [None]*27; z = [None]*27; clrs = [None]*27; kinds = [None]*27
    ind = -1
    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                ind = ind + 1            
                numeric_str = tup2num_str([i,j,k])
                clr = df[df['Numeric']==numeric_str]['Color']
                x[ind] = i; y[ind] = j; z[ind] = k; clrs[ind] = btr_purp(clr.item().lower())            
                knd = df[df['Numeric']==numeric_str]['Kind'].item()
                if knd == 'Seed' or knd == 'Island':
                    kinds[ind] = knd
                    
    # Create full gene space graphic object
    go1 = go.Scatter3d(x = x, y = y, z = z, mode = 'markers+text', text = kinds, textposition = 'middle left',
                    marker = dict(size=10,color=clrs,opacity=0.8,symbol='diamond',line=dict(width=1, color='black')),
                    showlegend=True, name='All Genetic Combinations')

    # Create parent graphic object
    parents = np.array([par1,par2])
    go2 = go.Scatter3d(x = parents[:,0]+0.1, y = parents[:,1]+0.1, z = parents[:,2], name = 'Parents',
                    mode = 'markers', marker = dict(size=8,color='cyan',opacity=0.9,symbol='circle'))

    # Determine children locations in gene-space & probabilities
    children = getChildren(par1, par2) # get children strs & probs
    num_keys = len(children.keys())
    x = [None]*num_keys; y = [None]*num_keys; z = [None]*num_keys; txts = [None]*num_keys;
    ind = -1
    for ky in children.keys():
        ch_tup = num_str2tup(ky)
        ind = ind + 1
        x[ind] = ch_tup[0] # locations in gene-space
        y[ind] = ch_tup[1] 
        z[ind] = ch_tup[2] 
        txts[ind] = str(children[ky]*100) + '%'
        
    # Create children graphic object
    go3 = go.Scatter3d(x = x, y = y, z = z, mode = 'text+markers', text = txts, name = 'Potential Children',
                    marker = dict(symbol='x',size=3,color='lime',opacity=0.9),showlegend=True)
        
    # Create and tailor figure    
    fig = go.Figure(data=[go1, go2, go3])
    fig.update_layout(
        title = dict(text=flwr.upper(), x=0.45, y = 0.9),
        scene = dict(
            xaxis_title = 'Red Genes',
            yaxis_title = 'Yellow Genes', 
            zaxis_title = 'White Genes',
            xaxis = dict(range=[-0.5,2.5], tickmode='array', tickvals=[0,1,2], ticktext=['rr', 'Rr', 'RR']),
            yaxis = dict(range=[-0.5,2.5], tickmode='array', tickvals=[0,1,2], ticktext=['yy', 'Yy', 'YY']),
            zaxis = dict(range=[-0.5,2.5], tickmode='array', tickvals=[0,1,2], ticktext=['ww', 'Ww', 'WW'])),
        width=700,
        margin=dict(r=20, l=10, b=10, t=10),
        legend = dict(x=0.9, y=0.5, itemsizing='constant'))

    # Return graph for update
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)