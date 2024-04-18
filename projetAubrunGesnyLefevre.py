# Import de module
import json
import numpy as np
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, ColorPicker, Legend
from bokeh.models import TabPanel, Tabs, GeoJSONDataSource
from bokeh.models import GMapPlot, GMapOptions, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
from bokeh.layouts import row, column

# Définition de fonction

def coor_wgs84_to_web_mercator(coord):
    lon=coord[0]
    lat=coord[1]
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return [x,y]

premier_elem = lambda x: x.iloc[0] if not x.empty else None

# Main
if __name__=='__main__':

    # Import des données

    data=pd.read_csv('eco-counter-data.csv',sep=';') # données de comptage des velos de rennes metropole: https://data.rennesmetropole.fr/explore/dataset/eco-counter-data/table/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImVjby1jb3VudGVyLWRhdGEiLCJvcHRpb25zIjp7fX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImxpbmUiLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJjb3VudHMiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjNjZjMmE1In1dLCJ4QXhpcyI6ImRhdGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJ5ZWFyIiwic29ydCI6IiJ9XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&location=14,48.11631,-1.68065&basemap=0a029a
    data['x']=[coor_wgs84_to_web_mercator(list(map(float, coord.split(', '))))[0] for coord in data["geo"]]
    data['y']=[coor_wgs84_to_web_mercator(list(map(float, coord.split(', '))))[1] for coord in data["geo"]]
    data['annee']=[date.year for date in pd.to_datetime(data['date'])]
    datamieux=data.groupby(by=['annee','name']).agg({'counts':sum,'x':premier_elem,'y':premier_elem})
    databeaucoupmieux = datamieux.pivot_table(index=['name', 'x', 'y'],
                          columns='annee',
                          values='counts',
                          aggfunc='sum').reset_index().fillna(0)
    databeaucoupmieux.columns.name = None
    print(databeaucoupmieux,databeaucoupmieux.columns)
    ''''# Onglet 1

    p1 = figure(x_axis_type="mercator", y_axis_type="mercator", 
        active_scroll="wheel_zoom", title="Graphe 1")
    p1.circle(x='x', y='y', size=5, alpha=0.7,source=data)
    p1.add_tile("CartoDB Positron")
    


    # Onglet 2

    p2 = figure(title="Graphe 2")

    # Onglet 3

    p3 = figure(title="Graphe 3")

    # Onglet 4

    p4 = figure(title="Graphe 4")  

    tab1 = TabPanel(child=p1, title="Graphe 1")
    tab2 = TabPanel(child=p2, title="Graphe 2")
    tab3 = TabPanel(child=p3, title="Graphe 3")
    tab4 = TabPanel(child=p4, title="Graphe 4")
    tabs = Tabs(tabs = [tab1, tab2, tab3, tab4])

    show(tabs)'''