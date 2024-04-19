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
    data['x']=[coor_wgs84_to_web_mercator(list(map(float, coord.split(', '))))[1] for coord in data["geo"]]
    data['y']=[coor_wgs84_to_web_mercator(list(map(float, coord.split(', '))))[0] for coord in data["geo"]]
    data['annee']=[date.year for date in pd.to_datetime(data['date'])]
    datamieux=data.groupby(by=['annee','name']).agg({'counts':sum,'x':premier_elem,'y':premier_elem})
    databeaucoupmieux = datamieux.pivot_table(index=['name', 'x', 'y'],
                          columns='annee',
                          values='counts',
                          aggfunc='sum').reset_index().fillna(0)
    databeaucoupmieux.columns.name = None
    new_column_names = {old_column_name: str(old_column_name) for old_column_name in databeaucoupmieux.columns}
    databeaucoupmieux.rename(columns=new_column_names, inplace=True)
    print(databeaucoupmieux,databeaucoupmieux.columns)
    source = ColumnDataSource(databeaucoupmieux)
    # Onglet 1

    p1 = figure(x_axis_type="mercator", y_axis_type="mercator",
     active_scroll="wheel_zoom", 
     title="Nombre de piétons controler à Rennes")
    p1.add_tile("CartoDB Positron")

    #

    taille_2024 = databeaucoupmieux['2024'].apply(lambda x: x*0.00005)
    taille_2023 = databeaucoupmieux['2023'].apply(lambda x: x*0.00005)
    taille_2022 = databeaucoupmieux['2022'].apply(lambda x: x*0.00005)
    taille_2021 = databeaucoupmieux['2021'].apply(lambda x: x*0.00005)
    taille_2020 = databeaucoupmieux['2020'].apply(lambda x: x*0.00005)
    taille_2019 = databeaucoupmieux['2019'].apply(lambda x: x*0.00005)
    taille_2018 = databeaucoupmieux['2018'].apply(lambda x: x*0.00005)
    taille_2017 = databeaucoupmieux['2017'].apply(lambda x: x*0.00005)
    taille_2016 = databeaucoupmieux['2016'].apply(lambda x: x*0.00005)
    taille_2015 = databeaucoupmieux['2015'].apply(lambda x: x*0.00005)
    taille_2014 = databeaucoupmieux['2014'].apply(lambda x: x*0.00005)


    source.add(taille_2024,"taille_2024")
    source.add(taille_2023,"taille_2023")
    source.add(taille_2022,"taille_2022")
    source.add(taille_2021,"taille_2021")
    source.add(taille_2020,"taille_2020")
    source.add(taille_2019,"taille_2019")
    source.add(taille_2018,"taille_2018")
    source.add(taille_2017,"taille_2017")
    source.add(taille_2016,"taille_2016")
    source.add(taille_2015,"taille_2015")
    source.add(taille_2014,"taille_2014")

    gl1 = p1.circle('x','y',size='taille_2024', source=source,color="yellow")
    gl2 = p1.circle('x','y',size='taille_2023', source=source,color="green")
    gl3 = p1.circle('x','y',size='taille_2022', source=source,color="red")
    gl4 = p1.circle('x','y',size='taille_2021', source=source,color="blue")
    gl5 = p1.circle('x','y',size='taille_2020', source=source,color="purple")
    gl6 = p1.circle('x','y',size='taille_2019', source=source,color="orange")
    gl7 = p1.circle('x','y',size='taille_2018', source=source,color="pink")
    gl8 = p1.circle('x','y',size='taille_2017', source=source,color="black")
    gl9 = p1.circle('x','y',size='taille_2016', source=source,color="grey")
    gl10 = p1.circle('x','y',size='taille_2015', source=source,color="brown")
    gl11 = p1.circle('x','y',size='taille_2014', source=source,color="cyan")

    #Outil de survol
    hover_tool = HoverTool(tooltips=[("Nom de l'emplacement ",'@name'),
                                    ('2024','@2024'),
                                    ('2023','@2023'),
                                    ('2022','@2022'),
                                    ('2021','@2021'),
                                    ('2020','@2022'),
                                    ('2019','@2019'),
                                    ('2018','@2018'),
                                    ('2017','@2017'),
                                    ('2016','@2016'),
                                    ('2015','@2015'),
                                    ('2014','@2014')])
    p1.add_tools(hover_tool)

    #La légende
    legend = Legend(items=[("2024", [gl1]),
        ("2023", [gl2]),
        ("2022", [gl3]),
        ("2021", [gl4]),
        ("2020", [gl5]),
        ("2019", [gl6]),
        ("2018", [gl7]),
        ("2017", [gl8]),
        ("2016", [gl9]),
        ("2015", [gl10]),
        ("2014", [gl11]),], location = 'top')
    p1.add_layout(legend,'below')

    legend.click_policy="hide"
    legend.title = "Cliquer sur les années à afficher"

    #Pickers
    picker1 = ColorPicker(title="Couleur pour les données de 2024",color=gl1.glyph.line_color,width=100)
    picker1.js_link('color', gl1.glyph, 'line_color')

    picker2 = ColorPicker(title="Couleur pour les données de 2023",color=gl2.glyph.line_color,width=100)
    picker2.js_link('color', gl2.glyph, 'line_color')

    picker3 = ColorPicker(title="Couleur pour les données de 2022",color=gl3.glyph.line_color,width=100)
    picker3.js_link('color', gl3.glyph, 'line_color')

    picker4 = ColorPicker(title="Couleur pour les données de 2021",color=gl4.glyph.line_color,width=100)
    picker4.js_link('color', gl4.glyph, 'line_color')

    picker5 = ColorPicker(title="Couleur pour les données de 2020",color=gl5.glyph.line_color,width=100)
    picker5.js_link('color', gl5.glyph, 'line_color')

    picker6 = ColorPicker(title="Couleur pour les données de 2019",color=gl6.glyph.line_color,width=100)
    picker6.js_link('color', gl6.glyph, 'line_color')

    picker7 = ColorPicker(title="Couleur pour les données de 2018",color=gl7.glyph.line_color,width=100)
    picker7.js_link('color', gl7.glyph, 'line_color')

    picker8 = ColorPicker(title="Couleur pour les données de 2017",color=gl8.glyph.line_color,width=100)
    picker8.js_link('color', gl8.glyph, 'line_color')

    picker9 = ColorPicker(title="Couleur pour les données de 2016",color=gl9.glyph.line_color,width=100)
    picker9.js_link('color', gl9.glyph, 'line_color')

    picker10 = ColorPicker(title="Couleur pour les données de 2015",color=gl10.glyph.line_color,width=100)
    picker10.js_link('color', gl10.glyph, 'line_color')

    picker11 = ColorPicker(title="Couleur pour les données de 2014",color=gl11.glyph.line_color,width=100)
    picker11.js_link('color', gl11.glyph, 'line_color')




    #Préparation des onglets
    layout = row(p1,column(picker1, picker2, picker3, picker4, picker5, picker6, picker7, picker8, picker9, picker10, picker11))

    


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

    show(tabs)