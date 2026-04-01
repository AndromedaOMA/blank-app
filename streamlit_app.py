import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image


st.set_page_config(
    page_title="CB helper",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto",
    # menu_items={
    #     "Get Help": "https://github.com/Siddhesh-Agarwal/CGPA-Calculator/discussions",
    #     "Report a bug": "https://github.com/Siddhesh-Agarwal/CGPA-Calculator/issues/new",
    #     "About": None,
    # },
)


def compute_distance(
        hotel_longitude: float,
        hotel_latitude: float,
        dest_longitude: float,
        dest_latitude: float,
):
    return np.sqrt((hotel_longitude - dest_longitude) ** 2 + (hotel_latitude - dest_latitude) ** 2)


def filter_col(column):
    result = []
    for value in column:
        if value is None:
            continue
        result.append(value)
    return result


def find_the_best_match(dest_longitude, dest_latitude, df):
    # Calculate distance for all rows at once
    df['distance'] = compute_distance(
        df['longitude'],
        df['latitude'],
        dest_longitude,
        dest_latitude
    )
    return df.sort_values(by='distance')


left_co, cent_co, last_co = st.columns([1, 4, 1])

with cent_co:
    # Logo
    try:
        image = Image.open('./images/CBlogo.png')
        st.image(image, use_container_width=True)
    except FileNotFoundError:
        st.warning("Logo file not found. Please check the path.")

    # Inputs
    cols = st.columns(2)
    dest_latitude = cols[0].number_input(
        label="Destination latitude",
        help="Enter the latitude of the desired tourist destination",
    )
    dest_longitude = cols[1].number_input(
        label="Destination longitude",
        help="Enter the longitude of the desired tourist destination",
    )

    uploaded_files = st.file_uploader(
        "Choose a CSV file",
        accept_multiple_files=True,
        type=['csv']
    )

    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        st.info(f"Uploaded: {uploaded_file.name}")

        if 'longitude' in df.columns and 'latitude' in df.columns:
            df = df.dropna(subset=['longitude', 'latitude'])

            if st.button("Calculate", use_container_width=True):
                if not df.empty:
                    results = find_the_best_match(dest_longitude, dest_latitude, df)
                    shortest_dist = results['distance'].iloc[0]

                    st.success(f"The shortest distance is {shortest_dist:.4f}")
                    st.write("### Closest hotels found:")
                    st.dataframe(results[['name', 'longitude', 'latitude', 'distance']].head(10),
                                 use_container_width=True)
                else:
                    st.error("The uploaded file is empty or missing data!")