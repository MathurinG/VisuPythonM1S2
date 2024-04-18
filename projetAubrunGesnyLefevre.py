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

    data=pd.read_csv('eco-counter-data.csv',sep=';') # données de comptage de pieton de rennes metropole: https://data.rennesmetropole.fr/explore/dataset/eco-counter-data/table/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImVjby1jb3VudGVyLWRhdGEiLCJvcHRpb25zIjp7fX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImxpbmUiLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJjb3VudHMiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjNjZjMmE1In1dLCJ4QXhpcyI6ImRhdGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJ5ZWFyIiwic29ydCI6IiJ9XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&location=14,48.11631,-1.68065&basemap=0a029a
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
    source = ColumnDataSource(databeaucoupmieux)
    ''''# Onglet 1

    p1 = figure(x_axis_type="mercator", y_axis_type="mercator",
     active_scroll="wheel_zoom", 
     title="Nombre de sites de production d'énergie en 2021")
    p1.add_tile("CartoDB Positron")

    #

    taille_photo = df['photo'].apply(lambda x: x*0.5+10 if x>0 else 0)
    taille_bio = df['bio'].apply(lambda x: x*0.5+10 if x>0 else 0)
    taille_hydrau = df['hydrau'].apply(lambda x: x*0.5+10 if x>0 else 0)
    taille_cogen = df['cogen'].apply(lambda x: x*0.5+10 if x>0 else 0)

    source.add(taille_photo,"taille_photo")
    source.add(taille_bio,"taille_bio")
    source.add(taille_hydrau,"taille_hydrau")
    source.add(taille_cogen,"taille_cogen")

    gl1 = p1.asterisk('pointx','pointy',size='taille_photo', source=source,color="orange")
    gl2 = p1.asterisk('pointx','pointy',size='taille_bio',source=source,color="green")
    gl3 = p1.asterisk('pointx','pointy',size='taille_hydrau',source=source,color="blue")
    gl4 = p1.asterisk('pointx','pointy',size='taille_cogen',source=source,color="red")

    #Outil de survol
    hover_tool = HoverTool(tooltips=[( 'Commune ',   '@commune'),
                                    ('Sites photovoltaïques','@photo'),
                                    ('Sites bio-énergie','@bio'),
                                    ('Sites hydrauliques','@hydrau'),
                                    ('Sites de cogénération','@cogen')])
    p1.add_tools(hover_tool)

    #La légende
    legend = Legend(items=[("Sites photovoltaïques", [gl1]),
        ("Sites bio-énergie", [gl2]),
        ("Sites hydrauliques", [gl3]),
        ("Sites de cogéneration", [gl4]),], location = 'top')
    p1.add_layout(legend,'below')

    legend.click_policy="hide"
    legend.title = "Cliquer sur les séries à afficher"

    #Pickers
    picker1 = ColorPicker(title="Couleur des sites photovoltaïques",color=gl1.glyph.line_color,width=100)
    picker1.js_link('color', gl1.glyph, 'line_color')

    picker2 = ColorPicker(title="Couleur des sites bio-énergie",color=gl2.glyph.line_color,width=100)
    picker2.js_link('color', gl2.glyph, 'line_color')

    picker3 = ColorPicker(title="Couleur des sites hydrauliques",color=gl3.glyph.line_color,width=100)
    picker3.js_link('color', gl3.glyph, 'line_color')

    picker4 = ColorPicker(title="Couleur des sites de cogéneration",color=gl4.glyph.line_color,width=100)
    picker4.js_link('color', gl4.glyph, 'line_color')




    #Préparation des onglets
    layout = row(p1,column(picker1, picker2, picker3, picker4))

    


    # Onglet 2

    p2 = figure(title="Graphe 2")

    # Onglet 3

    p3 = figure(title="Graphe 3")

    # Onglet 4

    p4 = figure(title="Graphe 4")  

    tab1 = TabPanel(child=layout, title="Graphe 1")
    tab2 = TabPanel(child=p2, title="Graphe 2")
    tab3 = TabPanel(child=p3, title="Graphe 3")
    tab4 = TabPanel(child=p4, title="Graphe 4")
    tabs = Tabs(tabs = [tab1, tab2, tab3, tab4])

    show(tabs)'''