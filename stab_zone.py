import ee
import datetime
# import geemap
import json
import xarray
import pycrs
import folium
import rasterio
import numpy as np
import localtileserver
import streamlit as st
import geemap.foliumap as geemap

# setting webpage title and icon
st.set_page_config(page_title="Yield Stability Map", page_icon='🛰️', layout='wide')

st.title("Interactive YSM Visualization")
st.write("""
This website provides a dynamic visualization of the yield stability map (YSM), enabling the direct observation of pixel variation of the 
         stability zones, The sliding window also enables
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

# left, right = st.columns(2)  # month, year column
# with left:
#   st.write('##### Left-side Visualization:')
#   feature_l = st.selectbox('Select Feature / Raster:', ['Landsat', 'Sentinel', 'Planet', 'Field Boundary'], key='option_1')

# with right:
#   st.write('##### Right-side Visualization:')
#   feature_r = st.selectbox('Select Feature / Raster:', ['Sentinel', 'Landsat', 'Planet', 'Field Boundary'], key='option_2')

# Making use of button instead:
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
#st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

satellite =st.radio("Select Satellite to Visualize",('Landsat', 'Sentinel', 'Planet'))

# creating a dictionary that stores that holds the location of the feature/ Raster
info_dict = {
  "Landsat": r"data/rasters/Landsat.tif",
  "Sentinel": r"data/rasters/Sentinel.tif",
  "Planet": r"data/rasters/Planet.tif"
}

# read important file 
aoi_shp = r"data/shapefile/Field123.shp"
region = geemap.shp_to_ee(aoi_shp)
planet = r"data/rasters/Planet.tif"

# Initialize Geemap map
map = geemap.Map(center=[43.582, -84.733], zoom=15, height=600)
map.add_basemap('HYBRID')
map.add_shapefile(aoi_shp, layer_name="Field Boundaries")


# adding rasters
src = rasterio.open(info_dict[satellite])
array = src.read()
bounds = src.bounds

x1,y1,x2,y2 = src.bounds
bbox = [(bounds.bottom, bounds.left), (bounds.top, bounds.right)]

img = folium.raster_layers.ImageOverlay(
    name=satellite,
    image=np.moveaxis(array, 0, -1),
    bounds=bbox,
    opacity=1,
    interactive=True,
    cross_origin=False,
    zindex=1,
)

img.add_to(map)
folium.LayerControl().add_to(map)




# left_layer = geemap.ee_tile_layer(info_dict[feature_l], name=feature_l)
# right_layer = geemap.ee_tile_layer(info_dict[feature_r], name=feature_r)
# map.split_map(left_layer, right_layer)

# if feature_l == 'Field Boundaries':
#     map.add_shapefile(aoi_shp, layer_name="Field Boundaries")
#     #map.addLayer(info_dict[feature_l], {}, "Field Boundaries")
#     map.add_raster(info_dict[feature_r], layer_name=feature_l)

# elif feature_r == 'Field Boundaries':
#     map.add_shapefile(aoi_shp, layer_name="Field Boundaries")
#     #map.addLayer(info_dict[feature_r], {}, "Field Boundaries")
#     map.add_raster(info_dict[feature_r], layer_name=feature_r)

# else:
#     map.add_raster(info_dict[feature_r], layer_name=feature_r)
#     map.add_raster(info_dict[feature_l], layer_name=feature_l)

# Display map
map.to_streamlit(height=600)