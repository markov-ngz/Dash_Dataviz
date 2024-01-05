from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('arbres10percent.csv').dropna(subset='STADE DE DEVELOPPEMENT')
df['lat'] = df['geo_point_2d'].map(lambda x: x.split(',')[0]).astype('float64')
df['lon'] = df['geo_point_2d'].map(lambda x: x.split(',')[1]).astype('float64')

app = Dash(__name__)

app.layout = html.Div(
    children=[
    html.Header(
        children=[
            html.H1(children='Dendrologie ou Etudes des Arbres ', style={'textAlign':'center'},className="app-header--title"),
        ],
        className="app-header",
    ),
    html.Div(className="graph1",children=[
    html.H2('Analyse des caractéristiques des arbres'),
    dcc.Dropdown(df.DOMANIALITE.unique(),'CIMETIERE', placeholder="Veuillez indiquer la Domanialité",searchable=True, id='dropdown-selection', className="w-80"),
    dcc.Dropdown(df['STADE DE DEVELOPPEMENT'].unique(), 'Adulte',placeholder="Veuillez indiquer la Domanialité",searchable=True, id='dropdown-selection2', className="w-80"),
    dcc.Graph(id='graph-content', className="w-80"),
    dcc.Graph(id='graph-height', className=""),
    ]),
    html.Div(className="graph1",children=[
        html.Div(className="line"),
        html.H2('Répartition des arbres par genre'),
        dcc.Dropdown(df['GENRE'].unique(), 'Platanus',placeholder="Veuillez indiquer le Genre",searchable=True, id='dropdown-selection3', className="w-80"),
        dcc.Graph(id='map', className="w-80"),
    ])
])

@callback(
    [Output('graph-content', 'figure'),
     Output('graph-height', 'figure'),
     Output('map','figure')],
    [Input('dropdown-selection', 'value'),
    Input('dropdown-selection2','value'),
    Input('dropdown-selection3','value')],
)
def update_graph(value, value2, value3):
    dff = df[df.DOMANIALITE==value][df['STADE DE DEVELOPPEMENT']==value2][['CIRCONFERENCE (cm)','HAUTEUR (m)']]

    hist_width = px.histogram(dff,
                            x='CIRCONFERENCE (cm)',
                            nbins=20,
                            title="Répartition de l'effectif selon la circonférence du tronc",
                            color_discrete_sequence=px.colors.qualitative.D3 )

    hist_height = px.histogram(dff,
                            x='HAUTEUR (m)',
                            nbins=20,
                            title="Répartition de l'effectif selon la hauteur de l'arbre",
                             color_discrete_sequence=px.colors.qualitative.D3 )

    dfmap= df[df.GENRE == value3]

    fig = px.scatter_mapbox(
        dfmap,
        lat='lat',
        lon='lon',
        zoom=10,
        mapbox_style='open-street-map'
    )


    return hist_width, hist_height, fig

if __name__ == '__main__':
    app.run(debug=True)