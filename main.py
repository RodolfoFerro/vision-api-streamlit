# ==============================================================
# Author: Rodolfo Ferro
# Twitter: @FerroRodolfo
#
# ABOUT COPYING OR USING PARTIAL INFORMATION:
# This script has been originally created by Rodolfo Ferro.
# Any explicit usage of this script or its contents is granted
# according to the license provided and its conditions.
# ==============================================================

# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import requests
from PIL import Image


st.sidebar.title("Computer Vision API")
st.sidebar.markdown(
    """
    En esta sencilla app podrás poner a prueba tu servicio de _Computer Vision_
    de Microsoft Azure.
    """
)
api_key = st.sidebar.text_input('API Key')
endpoint = st.sidebar.text_input('Endpoint')


st.title("Análisis de imágenes con Computer Vision API")
st.markdown(
    """
    A continuación podrás explorar los resultados del análisis de imágenes
    que tiene Computer Vision API de Microsoft Azure. En el siguiente bloque
    podrás cargar una imagen desde tu computadore y utilizar tu propia API de
    Computer Vision para realizar un análisis de la misma.
    """
)

valid_formats = ['png', 'jpg', 'jpeg']
upfile = st.file_uploader('Por favor carga una imagen.', type=valid_formats)
if upfile is not None:
    img_bytes = upfile.read()
    img = Image.open(upfile)
    img = np.array(img).astype('uint8')
    st.image(img, caption='Imagen cargada.')


if st.button('Procesar imagen con Computer Vision API'):
    # Verify keys and values
    if upfile is None:
        st.error('Debes cargar una imagen.')

    if api_key == '':
        st.error('Debes ingresar una API Key.')
    
    if endpoint == '':
        st.error('Debes ingresar un endpoint válido.')
    
    if upfile and api_key and endpoint:
        # Create metadata for Computer Vision API
        analyze_url = endpoint + 'vision/v3.1/analyze'
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/octet-stream'
        }
        params = {
            'visualFeatures': 'Categories,Description,Color'
        }

        response = requests.post(
            analyze_url,
            headers=headers,
            params=params,
            data=img_bytes
        )
        response.raise_for_status()
        analysis = response.json()

        image_caption = analysis['description']['captions'][0]['text']
        image_caption = image_caption.capitalize()

        tags = analysis['description']['tags']
        items = [f'\n- {tag}' for tag in tags]
        items = ''.join(items)
        
        st.markdown(
            f"""
            ## Resultados del análisis de la imagen

            **Archivo JSON de respuesta:**
            ```json
            {analysis}
            ```

            **Descripción de Computer Vision API:**
            _"{image_caption}"_.
            """
        )

        st.markdown(
            f"""
            **Etiquetas de elementos detectados:**
            {items} 
            """
        )