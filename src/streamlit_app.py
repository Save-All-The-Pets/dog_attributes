import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

@st.cache
def load_data():
    combined_attrib_coords = pd.read_csv('../dogdata/combined_attrib_coords.csv')
    combined_breeds_coords = pd.read_csv('../dogdata/combined_breeds_coords.csv')
    returns = (combined_attrib_coords, combined_breeds_coords)
    return returns

combined_attrib_coords, combined_breeds_coords = load_data()

st.title("Dogs all over the world")
st.markdown('Compare dog attribtes and breed counts! <br> <br>', unsafe_allow_html = True)
st.subheader("How do world cities differ... in terms of their dog attributes?")

attrib_selection = st.radio("Select a dog attribute", combined_attrib_coords.Attribute.unique())
# attrib_selection = 'Trainable'

token = 'pk.eyJ1IjoibWljYWVsYW1jY2FsbCIsImEiOiJjazRrNHFkaGsyMm94M21xZHozazd5ODg3In0.aRQ114nE0WKa7AnPMGiRzQ'
# px.set_mapbox_access_token(token)
# fig = px.scatter_mapbox(combined_coords[combined_coords.Attribute == attrib_selection], lat="lat", lon="lon", color = "Average", size = "radius", opacity = 0.5, 
#                         center = {'lat' :10, 'lon': -160}, mapbox_style = 'light', zoom = .5,
#                         color_continuous_scale=px.colors.sequential.Plasma,)
# ['{}'.format(j) for j in combined_attrib_coords[combined_attrib_coords.Attribute == attrib_selection].City] + ['Score: {}'.format(i) for i in combined_attrib_coords[combined_attrib_coords.Attribute == attrib_selection].Average.round(decimals= 2)]
@st.cache
def plot_attributemap():
    attributemap = go.Figure([go.Scattermapbox(
        lat = combined_attrib_coords[combined_attrib_coords.Attribute == attrib_selection].lat, 
        lon = combined_attrib_coords[combined_attrib_coords.Attribute == attrib_selection].lon,
        hoverinfo= "text", 
        text = ['{} Score: {}'.format(*i) for i in zip(combined_attrib_coords[combined_attrib_coords.Attribute == attrib_selection].City, combined_attrib_coords[combined_attrib_coords.Attribute == attrib_selection].Average.round(decimals= 2))],
        mode = 'markers', 
        marker = dict(
            cmin = 0.4,
            cmax= 0.6,
            size = 20,
            opacity = 0.6,
            symbol = 'circle',
            color = combined_attrib_coords[combined_attrib_coords.Attribute == attrib_selection].Average,
            colorscale = 'OrRd',
            colorbar_title="Score"))])

    attributemap.update_layout(
        autosize=False,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=10,
                lon=-160
            ),
            pitch=0,
            zoom=0.5,
            style='light'
        ),
    )

    return attributemap


attributemap = plot_attributemap()


st.plotly_chart(attributemap)


st.subheader("Choose a breed and see how many dogs are in each city!")

breed_selection = st.selectbox(" ", combined_breeds_coords.Breed.unique())
# breed_selection = 'Akita'

@st.cache
def plot_breedmap():
    breedmap = go.Figure(go.Scattermapbox(
        lat = combined_breeds_coords[combined_breeds_coords.Breed == breed_selection].lat, 
        lon = combined_breeds_coords[combined_breeds_coords.Breed == breed_selection].lon,
        hoverinfo = 'text',
        text = ['{} Number of Dogs: {}'.format(*i) for i in zip(combined_breeds_coords[(combined_breeds_coords.Breed == breed_selection)].City, combined_breeds_coords[(combined_breeds_coords.Breed == breed_selection)].Count.astype('int'))], 
        mode = 'markers', 
        marker = dict(
            cmax = 0.1,
            cmin = 0,
            size = 20,
            opacity = 0.6,
            symbol = 'circle',
            color = combined_breeds_coords[(combined_breeds_coords.Breed == breed_selection)].NormalizedCount,
            colorscale = 'OrRd',
            colorbar_title="Normalized Count")))

    breedmap.update_layout(
        autosize=False,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=10,
                lon=-160
            ),
            pitch=0,
            zoom=0.5,
            style='dark'
        ),
    )

    return breedmap


breedmap = plot_breedmap()

st.plotly_chart(breedmap)

st.subheader("An in-depth look at each")
city_selection = st.radio('City', ['NYC', 'Seattle', 'Edmonton', 'Adelaide'])
# city_selection = 'Edmonton'

st.markdown(city_selection + ' top 5 breeds')

st.table(combined_breeds_coords[(combined_breeds_coords.City == city_selection)][['Breed','Count']].nlargest(6, ['Count']).set_index('Breed'))

st.markdown(city_selection + ' attribute score')

st.table(combined_attrib_coords[(combined_attrib_coords.City == city_selection)][['Attribute', 'Average']].set_index('Attribute'))