import ee
import datetime
import geemap
import json
import xarray
import pycrs
import rasterio
import localtileserver
import streamlit as st
import geemap.foliumap as geemap

# setting webpage title and icon
st.set_page_config(page_title="Dynamic Yield Stability Map", page_icon='🛰️', layout='wide')

st.title("Interactive Raster Visualization")
st.write("""
This website provides a dynamic visualization of the yield stability map (YSM). The sliding window also enables
         the comparison of any of the yield stability map created by the different satellite to visualize the 
         effects of the spatial resolution on the yield stability map.
""")

# initializing earth engine credentials
json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

json_object = json.loads(json_data, strict=False)
json_object = json.dumps(json_object)
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)

left, right = st.columns(2)  # month, year column
with left:
  st.write('##### Left-side Visualization:')
  feature_l = st.selectbox('Select Feature / Raster:', ['Landsat', 'Sentinel', 'Planet', 'Field Boundary'], key='option_1')

with right:
  st.write('##### Right-side Visualization:')
  feature_r = st.selectbox('Select Feature / Raster:', ['Sentinel', 'Landsat', 'Planet', 'Field Boundary'], key='option_2')

# creating a dictionary that stores that holds the location of the feature/ Raster

info_dict = {
  "Landsat": r"data/rasters/Landsat.tif",
  "Sentinel": r"data/rasters/Sentinel.tif",
  "Planet": r"data/rasters/Planet.tif",
  "Field Boundary": geemap.shp_to_ee(r"data/shapefile/Field123.shp")
}

# read important file 
aoi_shp = r"data/shapefile/Field123.shp"
region = geemap.shp_to_ee(aoi_shp)
planet = r"data/rasters/Planet.tif"

# Initialize Geemap map
map = geemap.Map(center=[43.582, -84.733], zoom=15, height=600)
map.add_basemap('HYBRID')
# map.add_raster(info_dict[feature_r], layer_name=feature_r)

# left_layer = geemap.ee_tile_layer(info_dict[feature_l], name=feature_l)
# right_layer = geemap.ee_tile_layer(info_dict[feature_r], name=feature_r)
# map.split_map(left_layer, right_layer)

if feature_l == 'Field Boundaries':
    map.add_shapefile(aoi_shp, layer_name="Field Boundaries")
    #map.addLayer(info_dict[feature_l], {}, "Field Boundaries")
    map.add_raster(info_dict[feature_r], layer_name=feature_l)

elif feature_r == 'Field Boundaries':
    map.add_shapefile(aoi_shp, layer_name="Field Boundaries")
    #map.addLayer(info_dict[feature_r], {}, "Field Boundaries")
    map.add_raster(info_dict[feature_r], layer_name=feature_r)

else:
    map.add_raster(info_dict[feature_r], layer_name=feature_r)
    map.add_raster(info_dict[feature_l], layer_name=feature_l)

# Display map
map.to_streamlit(height=600)