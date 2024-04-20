import numpy as np
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)
premier_elem = lambda x: x.iloc[0] if not x.empty else None

data=pd.read_csv('eco-counter-data.csv',sep=';')
data['x'] = [float(chaine.split(', ')[0]) for chaine in data['geo']]
data['y'] = [float(chaine.split(', ')[1]) for chaine in data['geo']]
(data['x'],data['y']) = coor_wgs84_to_web_mercator(data['y'],data['x'])
data['annee']=[date.year for date in pd.to_datetime(data['date'])]
data=data.groupby(by=['annee','name']).agg({'counts':sum,'x':premier_elem,'y':premier_elem})

#On normalise pour l'affichage :
scaler = MinMaxScaler(feature_range=(8, 60))
data['counts'] = scaler.fit_transform(data[['counts']])

#On restructure :
data = data.pivot_table(index=['name', 'x', 'y'],
                        columns='annee',
                        values='counts',
                        aggfunc='sum').reset_index().fillna(0)
data.columns.name = None
new_column_names = {old_column_name: str(old_column_name) for old_column_name in data.columns}
data.rename(columns=new_column_names, inplace=True)

print(data)

with open("data.json", "w",encoding='utf-8') as jsonFile:
    jsonFile.write(data.to_json())