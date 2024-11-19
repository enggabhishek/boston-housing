#=================Uploading Libraries=================================
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
#======================================================================

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

#================================Creating radio buttons for y axis=======================================================
y_axis = pn.widgets.RadioButtonGroup(
    name = 'Y axis',
    options = ['Building Cost','Land Cost','Gross Tax'],
    button_type = 'success'
)
#=========================================Creating Year Slider===========================================================
year_slider = pn.widgets.IntSlider(name='Year slider', start=1960, end=2020, step=1, value=1961)

#=========================================Kitchen Type Plot - First Pipeline=============================================
proc_name = "get_building_attributes"
input_params = ["KITCHEN_TYPE"]
cols = ['Kitchen Type']

df1  = get_dataframe(proc_name,input_params,cols)
df1['Kitchen Type'] = df1['Kitchen Type'].str.extract(r'^(\S+)')
idf = df1.interactive()

kit_type = ['0F','1F','2F','3F']
first_pipeline = (
    idf
    [
        (idf['Kitchen Type'].isin(kit_type))
    ]
)
kit_plot = first_pipeline.hvplot(y = 'Kitchen Type',  rot=90,by ='Kitchen Type', x = y_axis, line_width = 21, title = f"Influence of Kitchen Type on Structural Costs", xformatter ='%f')
#===========================================================================================================================

#=================================================Structure Type- Second Pipeline===========================================
proc_name = "get_building_attributes"
input_params = ["STRUCTURE_CLASS"]
cols = ['Structure Class']

df2  = get_dataframe(proc_name,input_params,cols)
df2['Structure Class'] = df2['Structure Class'].str.extract(r'^(\S+)')
idf2 = df2.interactive()

Stype = ['R','C','D','B', 'A']
second_pipeline = (
    idf2
    [
        (idf2['Structure Class'].isin(Stype))
    ]
    .groupby('Structure Class')[y_axis].agg(['min','mean', 'max'])
    .reset_index()
)
ac_plot = second_pipeline.hvplot(x = 'Structure Class' ,y = ['min','mean', 'max'],rot=90, kind = 'bar', xlabel = 'Structure Class', ylabel = y_axis, title = f"Influence of Air Conditioning Type on Structural Costs", yformatter='%f')
#=======================================================================================================================

#=================================================Third Pipeline (Hexbin)===============================================
proc_name = 'get_building_att_and_area'
input_params = ['GROSS_AREA', 'YR_BUILT']
cols = ['Gross Area', 'Year']
df_ar  = get_dataframe(proc_name,input_params,cols)

columns = ['Building Cost', 'Land Cost', 'Gross Tax', 'Year']
df_ar = df_ar.loc[(df_ar[columns] != 0).all(axis=1)]
df_ar = df_ar[df_ar['Year']>=1960]

idf3 = df_ar.interactive()
third_pipeline = (
    idf3[
        idf3.Year <= year_slider
    ]
)
count_data_points_plot = third_pipeline.hvplot.hexbin(x='Year', y=y_axis, gridsize=25, cmap='coolwarm', title = f"Annual Variation in Structural Costs Across Multiple Years", yformatter='%f')
#=======================================================================================================================

#=================================================Forth Pipeline -Kernel Density Estimate (KDE)=========================
proc_name4 = 'get_building_att_and_area'
input_params = ['BED_RMS', 'YR_BUILT']
cols = ['Number of Bedrooms','Year']
df_yr  = get_dataframe(proc_name,input_params,cols)

columns = ['Building Cost', 'Land Cost', 'Gross Tax', 'Year']
df_yr = df_yr.loc[(df_yr[columns] != 0).all(axis=1)]
df_yr = df_yr[df_yr['Year']>=1960]
df_yr = df_yr[columns]

idf4 = df_yr.interactive()
forth_pipeline = (
    idf4[
        idf4.Year == year_slider
    ]
)
kde = forth_pipeline.hvplot.kde(by='Year',y = y_axis, rot=90,title=f'Kernel Density Estimation of Structural Costs Over Multiple Years', xformatter ='%f', yformatter ='%f')
#==============================================================================================================================
template = pn.template.FastListTemplate(
    title='Boston Housing Dashboard', 
    sidebar=[pn.pane.Markdown("# Boston Housing Dataset"), 
             pn.pane.Markdown("#### The Boston Housing dataset is a popular dataset that is often used in machine learning and data science for regression problems. The dataset was first introduced in 1978 by Harrison and Rubinfeld, and it contains information collected by the U.S. Census Service concerning housing in the area of Boston, Massachusetts."), 
             pn.pane.JPG('Boston.jpg', sizing_mode='scale_both'),
             pn.pane.Markdown("## Settings")],
    main=[pn.Row(y_axis),
          pn.Row(year_slider),
        pn.Row(pn.Column(kit_plot.panel(width=700), margin=(0,25)), 
                 count_data_points_plot.panel(width=700)),
         pn.Row(pn.Column(ac_plot.panel(width=700, height = 350),margin=(0,25)),
                kde.panel(width=700, height = 350))],
    accent_base_color="#a34100",
    header_background="#a34100",
)
# template.show()
template.servable();