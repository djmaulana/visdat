import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_file, output_notebook
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models.widgets import Tabs, Panel

data = df[df["Country/Region"].str.contains("Afghanistan")==True]

df = pd.read_csv(r'C:\Users\djmaulana\Downloads\visdat\full_grouped.csv')

import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import row, widgetbox
from bokeh.palettes import Category20_16
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import show
from bokeh.io import curdoc
from bokeh.layouts import column, row, WidgetBox
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs


df = df[['Date','Country/Region','Confirmed','Deaths','Recovered','Active']]

lokasi = list(df['Country/Region'].unique())

col_list = list(df.columns)

# Method untuk pembuatan dataset yang akan di select nanti
def buatdataset(lokasi, feature):
    list_x = []
    list_y = []
    colors = []
    labels = []

    for i, lokasi in enumerate(lokasi):

        op = data[data['Country/Region'] == lokasi].reset_index(drop = True)
        
        x = list(op['Date'])
        y = list(op[feature])
        
        list_x.append(list(x))
        list_y.append(list(y))

        colors.append(Category20_16[i])
        labels.append(lokasi)

    new_index = ColumnDataSource(data={'x': list_x, 'y': list_y, 'color': colors, 'label': labels})

    return new_index

# Method untuk pembuatan multiple line plot yang akan di select nanti
def buatplot(src, feature):
    
    c = figure(plot_width = 820, plot_height = 430, 
            title = 'Covid19',
            x_axis_label = 'Date', y_axis_label = 'Feature Selected')

    c.multi_line('x', 'y', color = 'color', legend_field = 'label', line_width = 3, source = src)

    tooltips = [ ('Date','$x'), ('Total', '$y'), ]
           
    c.add_tools(HoverTool(tooltips=tooltips)) # Melakukan hover

    return c

# Method callback untuk interaktif checkbox
def updatelokasi(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]

    new_index = buatdataset(lokasi_plot, feature_select.value)

    src.data.update(new_index.data)

# Method callback untuk interaktif dropdown
def updatefitur(attr, old, new):
    lokasi_plot = [lokasi_selection.labels[i] for i in lokasi_selection.active]
    
    feature = feature_select.value
    
    new_index = buatdataset(lokasi_plot, feature)

    src.data.update(new_index.data)

# Pembuatan checkboxgroup berdasarkan pada provinsi/lokasi
lokasi_selection = CheckboxGroup(labels=lokasi, active = [0])
lokasi_selection.on_change('active', updatelokasi)

# Pembuatan fitur select dropdown 
feature_select = Select(options = col_list[2:], value = 'Confirmed', title = 'Feature Select')
feature_select.on_change('value', updatefitur)
lokasi_now = [lokasi_selection.labels[i] for i in lokasi_selection.active]
src = buatdataset(lokasi_now, feature_select.value)

# Pemanggilan method plot
c = buatplot(src, feature_select.value)

# Pemasangan widget untuk interaktive visualisasi data covid
controls = WidgetBox(feature_select, lokasi_selection)
layout = row(controls, c)
curdoc().add_root(layout)