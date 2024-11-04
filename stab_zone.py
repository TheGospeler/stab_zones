import ee
import json
import datetime
import streamlit as st
import geopandas as gpd
import geemap.foliumap as geemap
import geopandas as gpd
import geemap as geemap_r

# setting webpage title and icon
st.set_page_config(page_title="Dynamic Yield Stability Map", page_icon='🛰️', layout='wide')

st.title("Interactive Raster Visualization")

# read important file 
aoi_shp = r"data/shapefile/Field123.shp"
region = geemap.shp_to_ee(aoi_shp)
planet = r"data/rasters/Planet.tif"

# Initialize Geemap map
map = geemap.Map(center=[43.582, -84.733], zoom=15, height=600)
map.add_basemap('HYBRID')
map.addLayer(region, {}, "Field Boundaries")
map.add_raster(planet)

# Display map
map.to_streamlit(height=600)