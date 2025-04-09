import streamlit as st

st.set_page_config(
    page_title="B2P Map Tiling Tools", 
    page_icon="🛶", 
    layout="wide"
)

st.title("🛶 Bridges to Prosperity Map Tiling Tools")

st.markdown("""
Welcome to the B2P Map Tiling Tools suite! This application provides tools for generating
and working with map tiles for geospatial visualization.

## Available Tools

### 🛶 Tippecanoe Command Generator
Create optimized command lines for the Tippecanoe tool to generate vector tiles from geospatial data.
- Configure all Tippecanoe options through an intuitive interface
- Handle various input formats (GeoJSON, FlatGeobuf, CSV)
- Copy generated commands directly to your clipboard

### 🗺️ Raster Tile Helper (coming soon)
View and interact with generated map tiles.
- Guess the max zoom needed based on resolution
- Generate gdal2tiles.py commands for raster tiles

## Getting Started

Use the sidebar to navigate between different tools, or click one of the links below:
""")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/01_Tippecanoe_Command_Generator.py", label="Tippecanoe Command Generator", icon="🛶")
    
with col2:
    st.page_link("pages/02_Raster_Tile_Helper.py", label="Raster Tile Helper", icon="🗺️")

st.divider()

st.markdown("""
## About Tippecanoe

[Tippecanoe](https://github.com/felt/tippecanoe) is a powerful tool that builds vector tilesets 
from geospatial data. It's designed to create scale-independent views of your data, so that at any zoom level 
you can see the density and texture of the data rather than a simplification.

Developed by [Mapbox](https://www.mapbox.com/) and now maintained by [Felt](https://felt.com/), 
Tippecanoe is an essential tool for creating optimized vector tiles for web mapping.
""")