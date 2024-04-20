# Import de module
import json
import numpy as np
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.models import HoverTool, ColumnDataSource, ColorPicker, Legend
from bokeh.models import TabPanel, Tabs, GeoJSONDataSource
from bokeh.models import GMapPlot, GMapOptions, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
from bokeh.layouts import row, column

data=pd.read_json('data.json')

source = ColumnDataSource(data)
p = figure(width = 1200,height = 800,x_axis_type="mercator", y_axis_type="mercator", title="pieton")
p.add_tile("CartoDB Positron")
p.asterisk('x','y',source=source,size='counts')
show(p)

