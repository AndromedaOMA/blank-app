import streamlit as st
import numpy as np
import pandas as pd


st.title("CongressBookers helper")

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

# st.image('./CongressBookers_template word-02')
a
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

    # Sort by distance (ascending) so the shortest is first
    df_sorted = df.sort_values(by='distance')

    return df_sorted

st.markdown(
    "Introduce the Longitude and Latitude of the desired tourist destination and let the algorithm make your job easier! "
)

cols = st.columns(2)
dest_longitude = cols[0].number_input(
    label="Longitude",
    help="Enter the longitude of the desired tourist destination",
    # value=0.00,
)
dest_latitude = cols[1].number_input(
    label="Latitude",
    help="Enter the latitude of the desired tourist destination",
    # value=0.00,
)

uploaded_files = st.file_uploader(
    "Choose a CSV file",
    accept_multiple_files=True,
    type=['csv']
)
for uploaded_file in uploaded_files:
    df = pd.read_csv(uploaded_file)

    st.write("Uploaded the filename:", uploaded_file.name)

    if 'longitude' in df.columns and 'latitude' in df.columns:
        df = df.dropna(subset=['longitude', 'latitude'])

        # hotel_longitudes = df['longitude']
        # st.write("First 5 Longitudes:", hotel_longitudes[:4])

    if st.button("Calculate"):
        if not df.empty:
            # Get the processed dataframe
            results = find_the_best_match(dest_longitude, dest_latitude, df)

            # Get the very shortest distance (first row)
            shortest_dist = results['distance'].iloc[0]
            closest_hotel = results.iloc[0]  # Assuming there's a 'hotel_name' column

            st.success(f"The shortest distance is {shortest_dist:.4f}")

            # Show the full list or the top 5
            st.write("Closest hotels found:")
            st.dataframe(results[['name', 'longitude', 'latitude', 'distance']].head(10))
        else:
            st.error("Please upload a file first!")
