import numpy as np
import pandas as pd
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import cartopy.crs as ccrs
pd.options.plotting.backend = 'holoviews'
from scipy import stats
import boto3
import pymysql
import os

ENDPOINT = "<Enter Instance-Endpoint>"
PORT = 3306
USER = "<Your-Username>"
REGION = "<Region-of-HostedServer>"
DBNAME = "<DB-Name>"
SSLCERTIFICATE = "<Path of SSl Certificate(.pem)>"
conn = ''
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
#=========================Connecting to MySQL===========================
session = boto3.Session(profile_name='default')
client = session.client('rds')
token = client.generate_db_auth_token(
    DBHostname=ENDPOINT,
    Port=PORT,
    DBUsername=USER,
    Region=REGION
)

try:
    conn = pymysql.connect(
        host=ENDPOINT,
        user=USER,
        passwd=token,
        port=PORT,
        database=DBNAME,
        ssl_ca=SSLCERTIFICATE
    )
except Exception as e:
    print(f"Database connection failed due to: {e}")
    
mycursor = conn.cursor(buffered = True)
#=====================================================================================================================

#=========================================Creating and Cleaning Dataframe===============================================
def get_dataframe(proc_name: str, input_params: str,cols: list)-> pd.DataFrame:
    mycursor.callproc(proc_name, input_params)
    result = mycursor.stored_results()
    details = list()
    columns = ['Building Cost','Land Cost','Gross Tax'] + cols
    for i in result:
        details = i.fetchall()
    df = pd.DataFrame(details, columns=columns)
    df.replace('', np.nan, inplace=True)
    df.dropna(inplace=True)
    df['Building Cost']=df['Building Cost'].str.replace(r'[\$,]', '', regex=True).astype(float)
    df['Land Cost']=df['Land Cost'].str.replace(r'[\$,]', '', regex=True).astype(float)
    df['Gross Tax']=df['Gross Tax'].str.replace(r'[\$,]', '', regex=True).astype(float)
    return df
#========================================================================================================================

#====================================creating radio buttons for y axis===================================================
y_axis = pn.widgets.RadioButtonGroup(
    name = 'Y axis',
    options = ['Building Cost','Land Cost','Gross Tax'],
    button_type = 'success'
)
#===========================================Creating Year Slider=========================================================
year_slider = pn.widgets.IntSlider(name='Year slider', start=1970, end=2020, step=1, value=1970)

#===========================================Property View - First Pipeline===============================================
proc_name = 'get_building_att_and_area'
input_params = ['PROP_VIEW', 'YR_BUILT']
cols = ['Property View', 'Year']

df  = get_dataframe(proc_name,input_params,cols)
df['Property View'] = df['Property View'].str.extract(r'^(\S+)')

columns = ['Building Cost', 'Land Cost', 'Gross Tax', 'Year']
df = df.loc[(df[columns] != 0).all(axis=1)]
df = df[df['Year']>=1960]

PType= ['A','F','G', 'E', 'P']
idf = df.interactive()
first_pipeline = (
    idf
    [
        
         (idf.Year <= year_slider) &
        (idf['Property View'].isin(PType))
    ]
    .groupby(['Property View', 'Year'])[y_axis].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='Year')  
    .reset_index(drop=True)
)
first_plot = first_pipeline.hvplot.box(y = y_axis,by='Property View', color = 'lightgreen',outlier_color='white',title = f"Influence of Building Style on", yformatter='%f')
#=========================================================================================================================

#===========================================Gross Area - Second Pipeline==================================================
proc_name = 'get_building_attributes'
input_params = ['GROSS_AREA']
cols = ['Gross Area']

df_gr_ar  = get_dataframe(proc_name,input_params,cols)

columns = ['Building Cost', 'Land Cost', 'Gross Tax']
df_gr_ar = df_gr_ar.loc[(df_gr_ar[columns] != 0).all(axis=1)]
idf2 = df_gr_ar.interactive()

second_plot = idf2.hvplot.scatter(x='Gross Area', y = y_axis, color = 'blue', title = f'Impact of Gross Area on Structural Cost', yformatter='%f', xformatter='%f')
#==========================================================================================================================

#=============================================Roof Cover - Third Pipeline==================================================

proc_name = 'get_building_att_and_area'
input_params = ['ROOF_COVER', 'YR_BUILT']
cols = ['Roof Cover', 'Year']

df_ext_fin  = get_dataframe(proc_name,input_params,cols)
df_ext_fin['Roof Cover'] = df_ext_fin['Roof Cover'].str.extract(r'^(\S+)')

df_grouped = df_ext_fin.groupby(['Roof Cover', 'Year']).size().reset_index(name='Count')
idf3 = df_grouped.interactive()

third_pipeline = (
    idf3[
        (idf3.Year <= year_slider)
    ]
)

third_plot = third_pipeline.hvplot.scatter(x='Roof Cover', y='Count', by='Year', title='Impact of Roof Cover on Structural Cost')
#==========================================================================================================================
proc_name = 'get_building_att_and_area'
input_params = ['ROOF_STRUCTURE', 'YR_BUILT']
cols = ['Roof Structure', 'Year']

df_rf_struc = get_dataframe(proc_name,input_params,cols)
df_rf_struc['Roof Structure'] = df_rf_struc['Roof Structure'].str.extract(r'^(\S+)')

columns = ['Building Cost', 'Land Cost', 'Gross Tax', 'Year']
df_rf_struc = df_rf_struc.loc[(df_rf_struc[columns] != 0).all(axis=1)]
df_rf_struc = df_rf_struc[df_rf_struc['Year']>=1960]

RType= ['M','F','G', 'H', 'O']
idf4 = df_rf_struc.interactive()
forth_pipeline = (
    idf4
    [
        
         (idf4.Year <= year_slider) &
        (idf4['Roof Structure'].isin(RType))
    ]
    .groupby(['Roof Structure', 'Year'])[y_axis].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='Year')  
    .reset_index(drop=True)
)

forth_plot = forth_pipeline.hvplot.violin(y = y_axis,by='Roof Structure', color ='Roof Structure',title = f"Influence of Roof Structure on Structural Cost", yformatter='%f')
#==========================================================================================================================
template = pn.template.FastListTemplate(
    title='Boston Housing Dashboard', 
    sidebar=[pn.pane.Markdown("# Boston Housing Dataset"), 
             pn.pane.Markdown("#### The Boston Housing dataset is a popular dataset that is often used in machine learning and data science for regression problems. The dataset was first introduced in 1978 by Harrison and Rubinfeld, and it contains information collected by the U.S. Census Service concerning housing in the area of Boston, Massachusetts."), 
             pn.pane.JPG('Boston.jpg', sizing_mode='scale_both'),
             pn.pane.Markdown("## Settings")],
    main=[pn.Row(y_axis),
          pn.Row(year_slider),
        pn.Row(pn.Column(first_plot.panel(width=700), margin=(0,10)), 
                 second_plot.panel(width=700)),
         pn.Row(pn.Column(third_plot.panel(width=700, height = 350), margin=(0,10)), 
                forth_plot.panel(width=700, height = 350))],
    accent_base_color="#a34100",
    header_background="#a34100",
)
template.servable();