import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Actividad Integradora M6")
st.markdown("**Maximiliano Aragón Fragoso - A01702063**")
df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")
df.dropna(axis = 1, thresh = int(len(df)*.75), inplace = True)
df.drop(['SF Find Neighborhoods','Current Police Districts','Current Supervisor Districts','Analysis Neighborhoods','Areas of Vulnerability, 2016'], axis = 1, inplace = True)
df.dropna(inplace =True)
st.dataframe(df)
df2 = df[['Latitude', 'Longitude']]
df2.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace = True)
df2.dropna(inplace = True)
df2.astype(float)

mapa = pd.DataFrame()
mapa['Police District'] = df['Police District']
mapa['Analysis Neighborhood'] = df['Analysis Neighborhood']
mapa['Year'] = df['Incident Year']
mapa['lon'] = df['Longitude']
mapa['lat'] = df['Latitude']
mapa = mapa.dropna()
submapa = mapa

dist_inp = st.sidebar.multiselect('Police District', mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(dist_inp) > 0:
    submapa = mapa[mapa['Police District'].isin(dist_inp)]
    
an_inp = st.sidebar.multiselect('Analysis Neighborhood', mapa.groupby('Analysis Neighborhood').count().reset_index()['Analysis Neighborhood'].tolist())
if len(an_inp) > 0:
    submapa = mapa[mapa['Analysis Neighborhood'].isin(an_inp)]
    
year_inp = st.sidebar.multiselect('Year', mapa.groupby('Year').count().reset_index()['Year'].tolist())
if len(year_inp) > 0:
    submapa = mapa[mapa['Year'].isin(year_inp)]
    


    
# Number of Completed Handovers by Hour
    
g1, g2, g3 = st.columns((1,1,1))

fig = px.bar(df, x = df['Incident Day of Week'].unique(), y = df.groupby(['Incident Day of Week']).count()['Row ID'], height=500)

fig.update_traces(marker_color='#264653')

fig.update_layout(title_text="Número de incidentes por Día de la Semana",title_x = 0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title = None, xaxis_title = None)

g1.plotly_chart(fig, use_container_width=True) 

# Número de casos por Año

fig2 = px.bar(df, x = df['Incident Year'].unique(), y = df.groupby(['Incident Year']).count()['Row ID'], height=500)

fig2.update_traces(marker_color='#7A9E9F')

fig2.update_layout(title_text="Número de casos por Año",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)

g2.plotly_chart(fig2, use_container_width=True)  

# Police District

fig3 = px.bar(df, x = df['Police District'].unique(), y = df.groupby(['Police District']).count()['Row ID'], height=500)

fig3.update_layout(title_text="Casos por Distrito",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None, legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))

g3.plotly_chart(fig3, use_container_width=True)

df['contador'] = 1
fig4 = px.sunburst(df, color_discrete_sequence = ['#d70000','#ff5523'], values='contador', path=['Police District','Incident Category'], hover_name='Incident Category')
fig4.update_layout(plot_bgcolor="white", title = 'Tipo de Crimen por Distrito')
st.plotly_chart(fig4)
       
st.map(submapa) 