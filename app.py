# External libraries
import streamlit as st
from PIL import Image
import zipfile
import io

# Imports from this project
import utils

st.title('THEBO Afbeeldingen')

# User parameters
WIDTH = st.number_input('Breedte afbeelding:', min_value=100, max_value=2000, value=800, step=50)
HEIGHT = st.number_input('Hoogte afbeelding:', min_value=100, max_value=2000, value=800, step=50)
QUALITY = st.number_input('Afbeeldingskwaliteit:', min_value=1, max_value=95, value=50, step=5)

uploaded_files = st.file_uploader('Selecteer afbeeldingen...', type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
processed_images = []

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        image = utils.open_image(uploaded_file)
        image = utils.trim(image)
        image = utils.resize(image, WIDTH, HEIGHT)
        image.filename = uploaded_file.name
        processed_images.append(image)

if st.button('Download afbeeldingen als zip'):
    zip_file = io.BytesIO()
    with zipfile.ZipFile(zip_file, mode='w') as z:
        for processed_image in processed_images:
            image_name = processed_image.filename
            image_bytes = io.BytesIO()
            processed_image.save(image_bytes, format='PNG', quality=QUALITY, optimize=True)
            z.writestr(image_name, image_bytes.getvalue())
    zip_file.seek(0)
    st.download_button('Download', data=zip_file.getvalue(), file_name='gecorrigeerde_afbeeldingen.zip', mime='application/zip')