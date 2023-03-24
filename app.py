# External libraries
import streamlit as st
from PIL import Image
import zipfile
import io

# Classes in this project
from ImageProcessor import ImageProcessor

st.title('THEBO Afbeeldingen')

uploaded_files = st.file_uploader('Selecteer afbeeldingen...', type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
processed_images = []

if uploaded_files is not None:
    for uploade_file in uploaded_files:
        image = Image.open(uploade_file)
        image.filename = uploade_file.name
        image_processor = ImageProcessor(image)
        image_processor.trim()
        image_processor.resize(800, 800)
        image = image.convert('RGB')
        processed_images.append(image)

if st.button('Download afbeeldingen als zip'):
    zip_file = io.BytesIO()
    with zipfile.ZipFile(zip_file, mode='w') as z:
        for processed_image in processed_images:
            image_name = processed_image.filename
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            z.writestr(image_name, image_bytes.getvalue())
    zip_file.seek(0)
    st.download_button('Download', data=zip_file.getvalue(), file_name='gecorrigeerde_afbeeldingen.zip', mime='application/zip')
