import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import plotly.express as px
from st_aggrid import AgGrid
import plotly.graph_objects as go

st.set_page_config(layout="wide")


def set_bg():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
        f"""
         <style>
         
         .stApp {{
             background: url("https://dl.dropbox.com/s/morqn6674wqgkmk/Backround_Diploma.png?dl=0"); 

         }}
         .css-18e3th9 {{
             padding-top: 33px;
             padding-bottom: 0px;
             padding-left: 50px;
             padding-right: 0px;
         }}

         </style>
         """,
        unsafe_allow_html=True
    )


set_bg()

fname = 'map.geojson'
nil = gpd.read_file(fname)

m = folium.Map(location=[45.758, 21.223], zoom_start=12.5, tiles="CartoDB dark_matter",
               name='Statistici imobiliare Timișoara',
               attr="My Data attribution")


col1, col2, col3, col4 = st.columns((1, 1, 1, 1))


with col1:
    choice1 = ['PretMediu', 'PretMinim', 'PretMaxim', 'PretMediu_MetruPatrat', 'NumarAnunturi', 'MetriPartrati_InMedie']

    choice_selected1 = st.selectbox("Alegeți o opțiune pentru a fi reprezentată. De menționat este că prețurile sunt în Euro.", choice1,
                                    help='Alegerea selectată urmează să fie '
                                         'reprezentată pe hartă, în fiecare regiune.'
                                         'Spre exemplu, daca alegerea făcută indică'
                                         '"PretMediu", prețul mediu va fi afișat în'
                                         'fiecare regiune, alături de numele acesteia,'
                                         'totodată facându-se și o departajare '
                                         'de culoare.')

    choice2 = ['1 Cameră', '2 Camere', '3 Camere', '4 Camere']

    choice_selected2 = st.radio("Alegeți numărul de camere. ", choice2,
                                help='Alegerea selectată reprezintă numărul de '
                                     'camere  dorit')

    color = st.color_picker('Alegeți o culoare pentru a evdenția zonele', '#6edab2')
    st.write('Culoarea curentă este: ', color)

fname = 'map.geojson'
nil = gpd.read_file(fname)
nil = nil[['geometry', 'text']]
cam1 = pd.read_csv('sql_query_1cam.csv')
cam2 = pd.read_csv('sql_query_2cam.csv')
cam3 = pd.read_csv('sql_query_3cam.csv')
cam4 = pd.read_csv('sql_query_4cam.csv')

if choice_selected2 == '1 Cameră':
    df_final = nil.merge(cam1, left_on="text", right_on="ZonăApartament", how="inner")
if choice_selected2 == '2 Camere':
    df_final = nil.merge(cam2, left_on="text", right_on="ZonăApartament", how="inner")
if choice_selected2 == '3 Camere':
    df_final = nil.merge(cam3, left_on="text", right_on="ZonăApartament", how="inner")
if choice_selected2 == '4 Camere':
    df_final = nil.merge(cam4, left_on="text", right_on="ZonăApartament", how="inner")

with col1:
    st.markdown(f"""
    <style>
    .paragraf {{
        font-family: Helvetica;
        font-size: 20px;
        color:{color};
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="paragraf">Tabel cu zonele și cu opțiunea selectată. </p>', unsafe_allow_html=True)

    grid_response = AgGrid(
        df_final[['ZonăApartament', choice_selected1]],
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=True,
        height=360,
        width='100%',
        reload_data=True,
        theme='dark'
    )



choropleth1 = folium.Choropleth(
    geo_data='map.geojson',
    data=df_final,
    columns=['ZonăApartament', choice_selected1],
    key_on='feature.properties.text',
    fill_color='Greys',
    nan_fill_color="black",
    line_color='White',
    fill_opacity=0.7,
    line_opacity=0.2

).geojson.add_to(m)

style_function = lambda x: {'fillColor': color,
                            'color': '#ffffff',
                            'fillOpacity': 0.5,
                            'weight': 0.8}
highlight_function = lambda x: {'fillColor': color,
                                'color': '#ffffff',
                                'fillOpacity': 0.85,
                                'weight': 0.1}

NIL = folium.features.GeoJson(
    df_final,
    style_function=style_function,
    control=False,
    highlight_function=highlight_function,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['ZonăApartament', choice_selected1],
        aliases=['Nume Regiune: ', choice_selected1],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 13.5px; padding: 10px;")
    )
)
m.add_child(NIL)
m.keep_in_front(NIL)
folium.LayerControl().add_to(m)
with col4:
    folium_static(m, width=490, height=500)


if choice_selected2 == '1 Cameră' or choice_selected2 == '2 Camere':
    fig = px.scatter_3d(
        df_final,
        x=choice_selected1,
        y="ZonăApartament",
        z=choice_selected1,
        hover_name="ZonăApartament",
        size=choice_selected1,
        size_max=40,
        color=[color, color, color, color, color, color, color, color, color, color, color],
        color_discrete_map="identity",
        template="plotly_dark")

else:
    fig = px.scatter_3d(
        df_final,
        x=choice_selected1,
        y="ZonăApartament",
        z=choice_selected1,
        hover_name="ZonăApartament",
        size=choice_selected1,
        size_max=40,
        color=[color, color, color, color, color, color, color, color, color, color],
        color_discrete_map="identity",
        template="plotly_dark")

fig.update_layout(

    scene={
        'camera_eye': {"x": 2, "y": 0.6, "z": 1},
        "aspectratio": {"x": 1, "y": 1.5, "z": 0.75}

    },
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    width=425,
    height=400)

if choice_selected2 == '1 Cameră' or choice_selected2 == '2 Camere':
    fig4 = px.density_contour(df_final, y=choice_selected1, x="ZonăApartament",
                        color=[color, color, color, color, color, color, color, color, color, color, color],
                        color_discrete_map="identity",
                        template="plotly_dark",
                        height=425,
                        width=500
                        )

else:
    fig4 = px.density_contour(df_final, y=choice_selected1, x="ZonăApartament",
                        color=[color, color, color, color, color, color, color, color, color, color],
                        color_discrete_map="identity",
                        template="plotly_dark",
                        height=425,
                        width=500
                        )

fig4.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


with col3:
    st.plotly_chart(fig, use_container_width=True)

    st.plotly_chart(fig4, use_container_width=True)

if choice_selected2 == '1 Cameră' or choice_selected2 == '2 Camere':
    fig2 = px.bar_polar(df_final, r=choice_selected1, theta="ZonăApartament",
                        color=[color, color, color, color, color, color, color, color, color, color, color],
                        color_discrete_map="identity",
                        template="plotly_dark",
                        height=425,
                        width=500
                        )

else:
    fig2 = px.bar_polar(df_final, r=choice_selected1, theta="ZonăApartament",
                        color=[color, color, color, color, color, color, color, color, color, color],
                        color_discrete_map="identity",
                        template="plotly_dark",
                        height=425,
                        width=500
                        )

fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)



if choice_selected2 == '1 Cameră' or choice_selected2 == '2 Camere':
    fig3 = px.violin(df_final, y=choice_selected1, x="ZonăApartament",
                        color=[color, color, color, color, color, color, color, color, color, color, color],
                        color_discrete_map="identity",
                        template="plotly_dark",
                        height=425,
                        width=500
                        )

else:
    fig3 = px.violin(df_final, y=choice_selected1, x="ZonăApartament",
                        color=[color, color, color, color, color, color, color, color, color, color],
                        color_discrete_map="identity",
                        template="plotly_dark",
                        height=425,
                        width=500
                        )

fig3.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
