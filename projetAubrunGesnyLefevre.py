# Import de module
import numpy as np
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, ColorPicker, Legend, FactorRange, Whisker
from bokeh.models import TabPanel, Tabs, Div, Spinner
from bokeh.layouts import row, column
from bokeh.transform import factor_cmap, jitter
from bokeh.palettes import Category10, Set1
# Définition de fonction

def coor_wgs84_to_web_mercator(coord):
    lon=coord[1]
    lat=coord[0]
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return [x,y]


# Main
if __name__=='__main__':

    # Import des données
    noms_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    noms_mois = {1:"Janvier",2: "Février",3: "Mars",4: "Avril",5: "Mai",6: "Juin",7: "Juillet",8:"Aout",9:"Septembre",10:"Octobre",11:"Novembre",12:"Decembre"}
    data=pd.read_csv('eco-counter-data.csv',sep=';') # données de comptage de velo de rennes metropole: https://data.rennesmetropole.fr/explore/dataset/eco-counter-data/table/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImVjby1jb3VudGVyLWRhdGEiLCJvcHRpb25zIjp7fX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImxpbmUiLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJjb3VudHMiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjNjZjMmE1In1dLCJ4QXhpcyI6ImRhdGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJ5ZWFyIiwic29ydCI6IiJ9XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&location=14,48.11631,-1.68065&basemap=0a029a
    data['x']=[coor_wgs84_to_web_mercator(list(map(float, coord.split(', '))))[0] for coord in data["geo"]]
    data['y']=[coor_wgs84_to_web_mercator(list(map(float, coord.split(', '))))[1] for coord in data["geo"]]
    data['annee']=[date.year for date in pd.to_datetime(data['date'])]
    data['mois']=[noms_mois[date.month] for date in pd.to_datetime(data['date'])]
    data['jour']=[noms_jours[date.weekday()] for date in pd.to_datetime(data['date'])]
    # Onglet 1
    ## Création du jeu de donnée aggréger par lieu et par année
    dfcarto = data.groupby(by=['annee','name']).agg({'counts':sum,'x':np.mean,'y':np.mean}).pivot_table(index=['name', 'x', 'y'],
                          columns='annee',
                          values='counts',
                          aggfunc='sum').reset_index().fillna(0)
    dfcarto.columns.name = None
    new_column_names = {old_column_name: str(old_column_name) for old_column_name in dfcarto.columns}
    dfcarto.rename(columns=new_column_names, inplace=True)#Passage du format de colonne de int à str
    source = ColumnDataSource(dfcarto)

    p1 = figure(x_axis_type="mercator", y_axis_type="mercator",
     active_scroll="wheel_zoom", 
     title="Nombre de velos controlés à Rennes")
    p1.add_tile("CartoDB Positron")

    ## Création du jeu de données

    taille_2024 = dfcarto['2024'].apply(lambda x: x*0.0001)
    taille_2023 = dfcarto['2023'].apply(lambda x: x*0.0001)
    taille_2022 = dfcarto['2022'].apply(lambda x: x*0.0001)
    taille_2021 = dfcarto['2021'].apply(lambda x: x*0.0001)
    taille_2020 = dfcarto['2020'].apply(lambda x: x*0.0001)
    taille_2019 = dfcarto['2019'].apply(lambda x: x*0.0001)
    taille_2018 = dfcarto['2018'].apply(lambda x: x*0.0001)
    taille_2017 = dfcarto['2017'].apply(lambda x: x*0.0001)
    taille_2016 = dfcarto['2016'].apply(lambda x: x*0.0001)
    taille_2015 = dfcarto['2015'].apply(lambda x: x*0.0001)
    taille_2014 = dfcarto['2014'].apply(lambda x: x*0.0001)


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

    ## Création de l'hovertool
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

    ## Création de la légende
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

    ## Création des Pickers
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


    ## Agencement de la page
    layout = row(p1,column(picker1, picker2, picker3, picker4, picker5, picker6, picker7, picker8, picker9, picker10, picker11),sizing_mode='scale_width')
    


    # Onglet 2
    ## Création du jeu de données aggréger par mois et par jour en gardant le nombre moyen de velo observés par jour
    dfparmoisetjour=data.groupby(by=['mois','jour']).agg({'counts':np.mean}).pivot_table(index='mois', columns='jour', values='counts', aggfunc='sum').reset_index()
    x = [ (mois, jour) for mois in noms_mois.values() for jour in noms_jours]
    counts = sum(zip(dfparmoisetjour['Lundi'],dfparmoisetjour['Mardi'],dfparmoisetjour['Mercredi'],dfparmoisetjour['Jeudi'],dfparmoisetjour['Vendredi'],dfparmoisetjour['Samedi'],dfparmoisetjour['Dimanche']), ())
    source2 = ColumnDataSource(data=dict(x=x, counts=counts))

    p2 = figure(x_range=FactorRange(*x), height=350, title="Nombre de velos moyen selon les jours du mois",
            toolbar_location=None, tools="hover",tooltips=[("Mois, Jour",'@x'),
                                    ('Nombre moyen de velos','@counts')])
    ## Création d'une palette avec une couleur par jour de la semaine
    palette = Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]+Category10[7]
    ## Création du 2nd graphique
    p2.vbar(x='x', top='counts', width=0.9, source=source2,color=factor_cmap('x', palette=palette, factors=x))
    p2.y_range.start = 0
    p2.x_range.range_padding = 0.1
    p2.xaxis.major_label_orientation = 1
    p2.xgrid.grid_line_color = None

    # Onglet 3
    ## Création du jeu de données
    df_p3 = data.groupby(by=['annee','name']).agg({'counts':sum}).reset_index()
    dum = pd.get_dummies(df_p3['name'])
    dum = dum.mul(df_p3['counts'], axis=0)
    df_p3 = pd.concat([df_p3,dum],axis=1)
    df_p3 = df_p3.groupby(by='annee').sum()
    noms = df_p3.columns[-3:]
    ## Afichage de la figure
    p3 = figure(title="Evolution du nombre de velo observé par Rennes Métropole selon les lieux")
    for name, color in zip( noms, Set1[3]):
        p3.line(df_p3.index,df_p3[name],line_width=2, color=color, alpha=0.8, legend_label=name,muted_color=color, muted_alpha=0.2)   
    p3.legend.click_policy="mute"
    p3.legend.location = "top_left"

    # Onglet 4
    ## Création des classes pour le graphique
    classes = list(sorted(data["name"].unique()))
    ## Création du dataframe pour le graphique
    df_par_lieu = data.groupby("name")
    upper = df_par_lieu.counts.quantile(0.80)
    lower = df_par_lieu.counts.quantile(0.20)
    source = ColumnDataSource(data=dict(base=classes, upper=upper, lower=lower))
    ## Création de la figure
    p4 = figure(height=400, x_range=classes,
            title="Nombre de velo observé par jour selon le lieu")
    p4.xgrid.grid_line_color = None
    ## Ajout de la ligne représentant l'écart entre le quartile 1/5 et 4/5
    error = Whisker(base="base", upper="upper", lower="lower", source=source,
                    level="annotation", line_width=2)
    error.upper_head.size=20
    error.lower_head.size=20
    p4.add_layout(error)
    ## Affichage des valeurs
    scatter=p4.scatter(jitter("name", 0.3, range=p4.x_range), "counts", source=data,
            alpha=0.5, size=13, line_color="white",
            color=factor_cmap("name", "Light7", classes))
    ## Création des deux spinner pour modifier l'affichage des valeurs
    spinner1 = Spinner(title="Taille des cercles", low=0,high=60, step=5, value=scatter.glyph.size) 
    spinner1.js_link("value", scatter.glyph, "size")

    spinner2 = Spinner(title="Transparence", low=0,high=1, step=0.1, value=scatter.glyph.fill_alpha) 
    spinner2.js_link("value", scatter.glyph, "fill_alpha")

    layout2 = row(p4, column (spinner1, spinner2))
    # Création des différents onglets sur la page html Bokeh
    tab1 = TabPanel(child=layout, title="Nombre de velos controlé à Rennes")
    tab2 = TabPanel(child=p2, title="Nombre de velos moyen selon les jours du mois")
    tab3 = TabPanel(child=p3, title="Evolution du nombre de velo observé par Rennes Métropole selon les lieux")
    tab4 = TabPanel(child=layout2, title="Nombre de velo observé par jour selon le lieu")
    tabs = Tabs(tabs = [tab1, tab2, tab3, tab4], sizing_mode="scale_both")
    # Création de l'en-tête de la page
    div = Div(text="""<h1 style="text-align: center;">Visualisation du nombre de velos mesuré par Rennes Métropole</h1>
    <p style="text-align: center;">L'objectif est de visualiser les mesures du nombre de velos effectuées à Rennes par Rennes Métropole, de suivre l'évolution de ce nombre au fil des années et des saisons, ainsi que de comprendre les méthodes utilisées pour effectuer ces mesures.</p>
    <p style="text-align: center;">Auteurs: Baptiste Aubrun, Mathurin Gesny, Yvan Lefevre</p>""")
    # Agencement de la page
    page = column(div,tabs, sizing_mode="scale_both")
    # Affichage de la page
    show(page)