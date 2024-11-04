import ee
import datetime
import geemap
import xarray
import pycrs
import rasterio
import localtileserver
import streamlit as st
import geemap.foliumap as geemap

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