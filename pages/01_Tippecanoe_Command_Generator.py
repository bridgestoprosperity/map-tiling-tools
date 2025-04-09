import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard

# Moving content from home.py to this page file

# TODO - fix mbtiles/pmtiles output switching

st.set_page_config(
    page_title="Tippecanoe Command Generator", page_icon="🛶", layout="wide"
)

st.title("🛶 Tippecanoe Command Generator")
st.markdown(
    """
This tool helps generate commands for [Tippecanoe](https://github.com/felt/tippecanoe?tab=readme-ov-file#tippecanoe), a tool that builds vector tilesets from GeoJSON, FlatGeobuf, or CSV files. Use the interface below to choose your settings and copy the command generated at the bottom to run in your terminal. Shout out to [Erica Fischer](https://github.com/e-n-f) for all their work creating and documenting Tippecanoe!
"""
)

# Initialize session state for storing inputs
if "input_files" not in st.session_state:
    st.session_state.input_files = [{"path": "", "layer": ""}]


# Function to add a new input file
def add_input_file():
    st.session_state.input_files.append({"path": "", "layer": ""})


# Function to remove an input file
def remove_input_file(index):
    st.session_state.input_files.pop(index)


# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Basic Options",
        "Zoom & Detail",
        "Feature Handling",
        "Attributes",
        "Advanced Options",
    ]
)

# Basic Options tab
with tab1:
    st.header("Output Settings")
    col1, col2 = st.columns(2)

    with col1:
        def sanitize_output_filename(name, extension):
            if name.endswith(".mbtiles") or name.endswith(".pmtiles"):
                name = name.rsplit(".", 1)[0]  # Remove existing extension
            return name + extension

        file_extension = ".mbtiles"
        output_file = st.text_input(
            "Output Filename",
            value="output" + file_extension,
            help="Name of the output file",
        )

        output_format = st.radio(
            "Output Format",
            ["MBTiles", "PMTiles", "Directory"],
            horizontal=True,
            help="Format of the output tileset",
        )

        if output_format == "Directory":
            output_dir = st.text_input(
            "Output Directory",
            value="output_tiles",
            help="Directory to output the tiles",
            )
        elif output_format == "MBTiles":
            file_extension = ".mbtiles"
            output_file = sanitize_output_filename(output_file, file_extension)
        else:
            file_extension = ".pmtiles"
            output_file = sanitize_output_filename(output_file, file_extension)

        force_overwrite = st.checkbox(
            "Force Overwrite",
            value=True,
            help="Delete output file if it already exists",
        )
        read_parallel = st.checkbox(
            "Parallel Processing",
            value=False,
            help="Use multiple threads to read different parts of each GeoJSON input file at once. This will only work if the input is line-delimited JSON with each Feature on its own line.",
        )

    with col2:
        name = st.text_input("Tileset Name", help="Human-readable name for the tileset")
        description = st.text_input("Description", help="Description for the tileset")
        attribution = st.text_input(
            "Attribution", help="Attribution text shown with maps using this tileset"
        )
        

    st.header("Input Files")
    st.info(
        "Add one or more GeoJSON, FlatGeobuf, or CSV files to process. For each file, you can specify a custom layer name. CSV input files currently support only Point geometries, from columns named latitude, longitude, lat, lon, long, lng, x, or y"
    )

    # Display input file fields
    for i, file_input in enumerate(st.session_state.input_files):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.session_state.input_files[i]["path"] = st.text_input(
                "File Path",
                value=file_input["path"],
                key=f"file_{i}",
                help="Path to GeoJSON, FlatGeobuf, or CSV file",
            )
        with col2:
            st.session_state.input_files[i]["layer"] = st.text_input(
                "Layer Name (optional)",
                value=file_input["layer"],
                key=f"layer_{i}",
                help="Custom layer name for this file",
            )
        with col3:
            if i > 0:  # Don't allow removing the first file
                st.button(
                    "Remove", key=f"remove_{i}", on_click=remove_input_file, args=(i,)
                )

    st.button("Add Another File", on_click=add_input_file)

# Zoom & Detail tab
with tab2:
    st.header("Zoom Levels")
    col1, col2 = st.columns(2)

    with col1:
        zoom_mode = st.radio(
            "Maximum Zoom Mode",
            ["Specify", "Auto-detect"],
            help="Choose how the maximum zoom level is determined",
        )

        if zoom_mode == "Specify":
            max_zoom = st.number_input(
                "Maximum Zoom",
                value=14,
                min_value=0,
                max_value=22,
                help="Highest zoom level for which tiles are generated",
            )

        min_zoom = st.number_input(
            "Minimum Zoom",
            value=0,
            min_value=0,
            max_value=22,
            help="Lowest zoom level for which tiles are generated",
        )

        extend_zooms = st.checkbox(
            "Extend Zooms If Still Dropping",
            help="Increase the maxzoom if features are still being dropped at that zoom level",
        )

    with col2:
        st.subheader("Tile Detail")
        auto_detail = st.checkbox(
            "Auto Tile Resolution",
            value=True,
            help="Automatically choose tile resolutions",
        )
        if auto_detail != True:
            full_detail = st.number_input(
                "Full Detail",
                value=12,
                min_value=0,
                max_value=32,
                help="Detail at max zoom level (tile resolution = 2^detail)",
            )

            low_detail = st.number_input(
                "Low Detail",
                value=12,
                min_value=0,
                max_value=32,
                help="Detail at lower zoom levels",
            )

            min_detail = st.number_input(
                "Minimum Detail",
                value=7,
                min_value=0,
                max_value=32,
                help="Minimum detail to try if tiles are too big at regular detail",
            )

# Feature Handling tab
with tab3:
    st.header("Feature Handling")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Feature Dropping & Simplification")

        drop_options = st.multiselect(
            "Drop Options",
            [
                "Drop Densest As Needed",
                "Drop Fraction As Needed",
                "Drop Smallest As Needed",
                "Coalesce Densest As Needed",
                "Coalesce Smallest As Needed",
                "Coalesce Fraction As Needed",
                "No Line Simplification",
                "No Tiny Polygon Reduction",
                "No Feature Limit",
                "No Tile Size Limit",
            ],
            help="Options for dropping features to keep tiles under size limits",
        )

        drop_rate = st.number_input(
            "Drop Rate",
            value=2.5,
            min_value=0.0,
            help="Rate at which features are dropped at zoom levels below basezoom",
        )

        # st.checkbox("Drop Lines", help="Let feature dropping apply to lines too")
        # st.checkbox("Drop Polygons", help="Let feature dropping apply to polygons too")

    with col2:
        st.subheader("Clustering & Density")

        cluster_options = st.selectbox(
            "Clustering Method",
            ["None", "Fixed Distance", "Cluster Densest As Needed"],
            help="Method for clustering points",
        )

        if cluster_options in ["Fixed Distance", "Cluster Densest As Needed"]:
            cluster_distance = st.number_input(
                "Cluster Distance",
                value=10,
                min_value=1,
                max_value=255,
                help="Cluster points within this distance",
            )

            cluster_maxzoom = st.number_input(
                "Cluster Max Zoom",
                value=14,
                min_value=0,
                max_value=22,
                help="Maximum zoom at which to cluster points",
            )

            accumulate_attributes = st.text_input(
                "Accumulate Attributes (comma-separated)",
                help="Attributes to preserve from features that are clustered (format: attr:operation, e.g. population:sum)",
            )

        calculate_feature_density = st.checkbox(
            "Calculate Feature Density",
            help="Add a tippecanoe_feature_density attribute to each feature",
        )

        detect_shared_borders = st.checkbox(
            "Detect Shared Borders",
            help="detect borders that are shared between multiple polygons and simplify them identically in each polygon. This takes more time and memory than considering each polygon individually.",
        )

        grid_low_zooms = st.checkbox(
            "Grid Low Zooms",
            help="At all zoom levels below maxzoom, snap all lines and polygons to a stairstep grid instead of allowing diagonals. You will also want to specify a tile resolution, probably -D8",
        )

# Attributes tab
with tab4:
    st.header("Feature Attributes")
    col1, col2 = st.columns(2)

    with col1:
        attribute_mode = st.radio(
            "Attribute Mode",
            ["Keep All", "Include Only", "Exclude Some", "Exclude All"],
            help="How to handle feature attributes",
        )

        if attribute_mode == "Include Only":
            include_attributes = st.text_area(
                "Include Attributes (one per line)",
                help="Only these attributes will be included in the output",
            )

        if attribute_mode == "Exclude Some":
            exclude_attributes = st.text_area(
                "Exclude Attributes (one per line)",
                help="These attributes will be excluded from the output",
            )

    with col2:
        generate_ids = st.checkbox(
            "Generate IDs",
            help="Add an ID to each feature that doesn't already have one",
        )

        attribute_types = st.text_area(
            "Attribute Types (one per line type)",
            help="Coerce attributes to specific types. Type can be the following strings, float, int, or bool",
        )

        set_attributes = st.text_area(
            "Set Attributes (one per line, format: attribute:value)",
            help="Set attribute values for all features. Format: attribute:value",
        )

# Advanced Options tab
with tab5:
    st.header("Advanced Options")
    col1, col2 = st.columns(2)

    with col1:
        buffer_size = st.number_input(
            "Buffer Size",
            value=5,
            min_value=0,
            help="Buffer size where features are duplicated from adjacent tiles",
        )

        simplification = st.number_input(
            "Simplification",
            value=1.0,
            min_value=0.0,
            help="Multiply the tolerance for line and polygon simplification",
        )

        projection = st.selectbox(
            "Projection",
            ["EPSG:4326 (WGS84)", "EPSG:3857 (Web Mercator)"],
            help="Projection of the input data",
        )

        no_clipping = st.checkbox(
            "No Clipping", help="Don't clip features to the size of the tile"
        )

        no_duplication = st.checkbox(
            "No Duplication", help="Don't duplicate features between tiles"
        )

    with col2:
        feature_filter = st.text_area(
            "Feature Filter (JSON)",
            help="Filter features using a Mapbox GL Style expression",
        )

        max_tile_bytes = st.number_input(
            "Max Tile Bytes",
            value=500000,
            min_value=0,
            help="Maximum compressed tile size in bytes",
        )

        max_tile_features = st.number_input(
            "Max Tile Features",
            value=200000,
            min_value=0,
            help="Maximum number of features in a tile",
        )

        preserve_input_order = st.checkbox(
            "Preserve Input Order",
            help="Preserve the original input order of features as the drawing order",
        )

        no_tile_compression = st.checkbox(
            "No Tile Compression", help="Don't compress the PBF vector tile data"
        )

# Generate command
st.header("Generated Command")


def build_command():
    cmd = ["tippecanoe"]

    # Output settings
    if output_format == "MBTiles":
        cmd.append(f"-o {output_file}")
    elif output_format == "PMTiles":
        cmd.append(f"-o {output_file}")
    else:  # Directory
        cmd.append(f"-e {output_dir}")

    if force_overwrite:
        cmd.append("-f")

    if read_parallel:
        cmd.append("-P")

    if name:
        cmd.append(f'-n "{name}"')

    if description:
        cmd.append(f'-N "{description}"')

    if attribution:
        cmd.append(f'-A "{attribution}"')

    # Zoom levels
    if zoom_mode == "Auto-detect":
        cmd.append("-zg")
    else:
        cmd.append(f"-z{max_zoom}")

    if min_zoom > 0:
        cmd.append(f"-Z{min_zoom}")

    if extend_zooms:
        cmd.append("-ae")

    # Tile detail
    if auto_detail != True:
        if full_detail != 12:
            cmd.append(f"-d{full_detail}")

        if low_detail != 12:
            cmd.append(f"-D{low_detail}")

        if min_detail != 7:
            cmd.append(f"-m{min_detail}")

    # Feature handling
    if "Drop Densest As Needed" in drop_options:
        cmd.append("-as")

    if "Drop Fraction As Needed" in drop_options:
        cmd.append("-ad")

    if "Drop Smallest As Needed" in drop_options:
        cmd.append("-an")

    if "Coalesce Densest As Needed" in drop_options:
        cmd.append("-aD")

    if "Coalesce Smallest As Needed" in drop_options:
        cmd.append("-aN")

    if "Coalesce Fraction As Needed" in drop_options:
        cmd.append("-aS")

    if "No Line Simplification" in drop_options:
        cmd.append("-ps")

    if "No Tiny Polygon Reduction" in drop_options:
        cmd.append("-pt")

    if "No Feature Limit" in drop_options:
        cmd.append("-pf")

    if "No Tile Size Limit" in drop_options:
        cmd.append("-pk")

    if drop_rate != 2.5:
        cmd.append(f"-r{drop_rate}")

    # Clustering
    if cluster_options == "Fixed Distance":
        cmd.append(f"-K{cluster_distance}")
        cmd.append(f"-k{cluster_maxzoom}")
    elif cluster_options == "Cluster Densest As Needed":
        cmd.append("-aC")

    if (
        "accumulate_attributes" in locals()
        and accumulate_attributes
        and cluster_options != "None"
    ):
        for attr in accumulate_attributes.split(","):
            attr = attr.strip()
            if attr:
                cmd.append(f"-E{attr}")

    if calculate_feature_density:
        cmd.append("-ag")
    
    if detect_shared_borders:
        cmd.append("-ab")

    if grid_low_zooms:
        cmd.append("-aL")

    # Attributes
    if attribute_mode == "Exclude All":
        cmd.append("-X")
    elif attribute_mode == "Include Only":
        if include_attributes:
            for attr in include_attributes.strip().split("\n"):
                if attr.strip():
                    cmd.append(f"-y {attr.strip()}")
    elif attribute_mode == "Exclude Some":
        if exclude_attributes:
            for attr in exclude_attributes.strip().split("\n"):
                if attr.strip():
                    cmd.append(f"-x {attr.strip()}")

    if generate_ids:
        cmd.append("-ai")

    if attribute_types:
        for line in attribute_types.strip().split("\n"):
            if line.strip():
                cmd.append(f"-T attribute:{line.strip()}")

    if set_attributes:
        for line in set_attributes.strip().split("\n"):
            if line.strip():
                cmd.append(f"--set-attribute {line.strip()}")

    # Advanced options
    if buffer_size != 5:
        cmd.append(f"-b {buffer_size}")

    if simplification != 1.0:
        cmd.append(f"-S {simplification}")

    if projection == "EPSG:3857 (Web Mercator)":
        cmd.append("-s EPSG:3857")

    if no_clipping:
        cmd.append("-pc")

    if no_duplication:
        cmd.append("-pD")

    if feature_filter:
        cmd.append(f"-j '{feature_filter}'")

    if max_tile_bytes != 500000:
        cmd.append(f"-M {max_tile_bytes}")

    if max_tile_features != 200000:
        cmd.append(f"-O {max_tile_features}")

    if preserve_input_order:
        cmd.append("-pi")

    if no_tile_compression:
        cmd.append("-pC")

    # Input files
    input_file_args = []

    for file_input in st.session_state.input_files:
        path = file_input["path"].strip()
        layer = file_input["layer"].strip()

        if path:
            if layer:
                input_file_args.append(f"-L {layer}:{path}")
            else:
                input_file_args.append(path)

    cmd.extend(input_file_args)

    return " ".join(cmd)


command = build_command()

st.code(command, language="bash")
# st.button("Copy to clipboard", on_click=lambda: st.write("Copied!"))

st_copy_to_clipboard(command, "Copy Command")

# Add useful examples
with st.expander("Example Commands"):
    st.markdown(
        """
    ### Linear features (world railroads), visible at all zoom levels
    ```bash
    tippecanoe -zg -o ne_10m_railroads.mbtiles --drop-densest-as-needed --extend-zooms-if-still-dropping ne_10m_railroads.geojson
    ```
    
    ### Discontinuous polygon features (buildings), visible at all zoom levels
    ```bash
    tippecanoe -zg -o buildings.mbtiles --drop-densest-as-needed --extend-zooms-if-still-dropping buildings.geojson
    ```
    
    ### Continuous polygon features (states and provinces), visible at all zoom levels
    ```bash
    tippecanoe -zg -o ne_10m_admin_1_states_provinces.mbtiles --coalesce-densest-as-needed --extend-zooms-if-still-dropping ne_10m_admin_1_states_provinces.geojson
    ```
    
    ### Large point dataset (GPS bus locations), for visualization at all zoom levels
    ```bash
    tippecanoe -zg -o bus_locations.mbtiles --drop-densest-as-needed --extend-zooms-if-still-dropping bus_locations.csv
    ```
    
    ### Clustered points (world cities), summing the clustered population
    ```bash
    tippecanoe -zg -o ne_10m_populated_places.mbtiles -r1 --cluster-distance=10 --accumulate-attribute=POP_MAX:sum ne_10m_populated_places.geojson
    ```
    """
    )

with st.expander("Tippecanoe Documentation"):
    st.markdown(
        """
    For complete documentation, visit the [Tippecanoe GitHub page](https://github.com/felt/tippecanoe).
    
    Tippecanoe builds vector tilesets from large (or small) collections of GeoJSON, FlatGeobuf, or CSV features.
    The goal is to enable making a scale-independent view of your data, so that at any level from the entire world 
    to a single building, you can see the density and texture of the data rather than a simplification from dropping
    features or clustering them.
    """
    )