# -*- coding: utf-8 -*-
"""# Import and Load"""

import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import column, row

df_bmkg = pd.read_excel('https://drive.google.com/uc?id=1Thha6U4ox6EHxDn8z-tbRuBZyyjkAVZL')

"""## Data Exploration"""

# df_bmkg.shape

# df_bmkg.head()

# df_bmkg.info()

# df_bmkg.describe()

"""## Data Preprocessing"""

# Cek nilai Null
df_bmkg.isnull().sum()

# Cek nilai tidak valid 8888
df_bmkg[df_bmkg == 8888].count()

# Cek nilai tidak valid 9999
df_bmkg[df_bmkg == 9999].count()

# Mengganti nilai 8888 dengan NaN
df_bmkg = df_bmkg.replace(8888, np.NaN)
df_bmkg.isnull().sum()

# Drop kolom tidak perlu
df_bmkg = df_bmkg.drop(columns=['ddd_car'])
df_bmkg.head()

"""## Visualisasi Bokeh"""

# Pembuatan Coloumn Data Source
source = ColumnDataSource(data={
    'x' : df_bmkg['Tn'],
    'y' : df_bmkg['Tx'],
    'Tanggal' : df_bmkg['Tanggal'],
})

# Tooltips untuk Hover
tooltips = [
            ('Tanggal', '@Tanggal'),
            ('x','$x{1.1}'),
            ('y', '$y{1.1}')
           ]

# Tools yang dipakai di kanan
select_tools = ['pan', 'wheel_zoom', 'reset']

# Membuat Figure
fig_titik = figure(title='Stasiun Meteorologi Kemayoran, DKI Jakarta, 16 April 2022 - 17 Juli 2022',
                   x_axis_label='Tn', y_axis_label='Tx',
                   tools=select_tools)

# Visualisasi Scatter
fig_titik.scatter(x='x', y='y',
              color='royalblue',
              size=7,
              source=source)

# Menambahkan Hover
fig_titik.add_tools(HoverTool(tooltips=tooltips))

# Interaksi
def update_plot(attr, old, new):
    # Mendapatkan nilai dari Widget Select
    x = x_select.value
    y = y_select.value

    # Mengganti nama label axis (sumbu)
    fig_titik.xaxis.axis_label = x
    fig_titik.yaxis.axis_label = y
    
    # Perubahan data baru
    new_data = {
    'x'       : df_bmkg[x],
    'y'       : df_bmkg[y],
    'Tanggal' : df_bmkg['Tanggal']
    }

    # Mengganti Coloumn Data Source dengan data baru
    source.data = new_data

# Pilihan pada Widget Select (Kecuali Tanggal)
option = df_bmkg.columns.to_list()
del option[0]

# Widget Select 1 (Sumbu X)
x_select = Select(
    options = option,
    title = 'Pilih Parameter 1',
    value = 'Tn'
)

# Widget Select 2 (Sumbu Y)
y_select = Select(
    options = option,
    title = 'Pilih Parameter 2',
    value = 'Tx'
)

# Jika Select dipilih
x_select.on_change('value', update_plot)
y_select.on_change('value', update_plot)

# Pengaturan Layout
layout = row(column(x_select, y_select,), fig_titik)

# Run Curdoc (Bokeh Application)
curdoc().add_root(layout)
curdoc().title = "Data BMKG"