# Import de module
import json
import numpy as np
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, ColorPicker, Legend
from bokeh.models import TabPanel, Tabs, Div
from bokeh.models import GMapPlot, GMapOptions, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
from bokeh.layouts import row, column
from bokeh.palettes import Set1
import math

# Def des fonctions :
from bokeh.layouts import row, column
def coor_zone(lon, lat):
    k = 6378137
    x = (lon[0] * (k * np.pi/180.0),lon[1] * (k * np.pi/180.0))
    y = (np.log(np.tan((90 + lat[0]) * np.pi/360.0)) * k,np.log(np.tan((90 + lat[1]) * np.pi/360.0)) * k)
    return (x,y)

# Récupération et construction du necessaire pour les plots :
# (les données ont été préalablement travaillé dans prepa_donnes.py)
data=pd.read_json('data.json')
latitudes = [48.08,48.14]
longitudes = [-1.72,-1.6]
x_merc,y_merc = coor_zone(longitudes,latitudes)
source = ColumnDataSource(data)

data1 = pd.read_json("data_1.json")
noms = data1.columns[-3:]
# Construction des figures :
# Onglet 1 :
p1 = figure(width = 1000,height = 600,x_range = x_merc,y_range=y_merc,x_axis_type="mercator", y_axis_type="mercator", title="Nombre de piétons par année")
p1.add_tile("CartoDB Positron")
gl1 = p1.circle('x','y',size='2024', source=source,color="yellow")
gl2 = p1.circle('x','y',size='2023', source=source,color="green",visible=False)
gl3 = p1.circle('x','y',size='2022', source=source,color="red",visible=False)
gl4 = p1.circle('x','y',size='2021', source=source,color="blue",visible=False)
gl5 = p1.circle('x','y',size='2020', source=source,color="purple",visible=False)
gl6 = p1.circle('x','y',size='2019', source=source,color="orange",visible=False)
gl7 = p1.circle('x','y',size='2018', source=source,color="pink",visible=False)
gl8 = p1.circle('x','y',size='2017', source=source,color="black",visible=False)
gl9 = p1.circle('x','y',size='2016', source=source,color="grey",visible=False)
gl10 = p1.circle('x','y',size='2015', source=source,color="brown",visible=False)
gl11 = p1.circle('x','y',size='2014', source=source,color="cyan",visible=False)
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

#La légende clickable 
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
p1.add_layout(legend,'right')
legend.click_policy="hide"
legend.title = "Cliquez sur les années à afficher"

#Pickers
glyphs = [gl1, gl2, gl3, gl4, gl5, gl6, gl7, gl8, gl9, gl10, gl11]

# Créer et lier les ColorPickers
color_pickers = []
for i, glyph in zip(range(2024, 2013, -1), glyphs):
    picker = ColorPicker(title=f"Couleur pour les données de {i}", color=glyph.glyph.fill_color, width=100)
    picker.js_link('color', glyph.glyph, 'fill_color')
    color_pickers.append(picker)

# Créer la colonne de ColorPickers
color_picker_column = column(*color_pickers, sizing_mode='scale_width')

# Disposer le graphique et la colonne de ColorPickers en une rangée
p1 = row(p1, color_picker_column, sizing_mode='scale_width')

# Onglet 2 :
p2 = figure(title="Graphe 2")
for name, color in zip( noms, Set1[3]):
    p2.line(data1.index,data1[name],line_width=2, color=color, alpha=0.8, legend_label=name,muted_color=color, muted_alpha=0.2,)   
p2.legend.click_policy="mute"
# Onglet 3
p3 = figure(title="Graphe 3")

# Onglet 4
p4 = figure(title="Graphe 4") 

#Affichage des plots :
tab1 = TabPanel(child=p1, title="Graphe 1")
tab2 = TabPanel(child=p2, title="Graphe 2")
tab3 = TabPanel(child=p3, title="Graphe 3")
tab4 = TabPanel(child=p4, title="Graphe 4")
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4])
div = Div(text="""<h1 style="text-align: center;">Visualisation du nombre de piétons mesurés par Rennes Métropole</h1>
<p style="text-align: center;">L'objectif est de visualiser selon les années où on été prise les mesures du nombres de piétons à Rennes Métropoles et comment ce nombre évolue</p>
<p style="text-align: center;">auteurs: Baptiste Aubrun, Mathurin Gesny, Yvan Lefevre</p>""")
page = column(div,tabs, sizing_mode="scale_both")
show(page)

