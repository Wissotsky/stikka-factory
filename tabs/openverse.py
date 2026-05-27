"""Openverse tab content."""

import logging
import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import os

import random

logger = logging.getLogger("sticker_factory.tabs.openverse")

from utils import fetch_image_from_url

def render(preper_image,printer_info, print_image, preset_query=None):
    search_query = None
    allow_custom_search = True
    visible_name_string = "Openverse"

    if preset_query:
        search_query = preset_query
        visible_name_string = preset_query
        allow_custom_search = False
    """Openverse tab"""
    st.subheader(f":printer: {visible_name_string}")
    st.caption("Find images from https://openverse.org/" if allow_custom_search else f"{visible_name_string} images from https://openverse.org/")
    
    # Initialize session state for image if not exists
    if 'openverse_image_grayscale' not in st.session_state:
        st.session_state.openverse_image_grayscale = None
        st.session_state.openverse_image_dithered = None

    if allow_custom_search:
        search_query = st.text_input("Search images")
    
    if search_query:
        if st.button(f"Fetch {visible_name_string}"):
            try:
                random_int = random.randint(1,240);
                # Get image URL
                response = requests.get(
                    "https://api.openverse.org/v1/images/",
                    params={"q":search_query,"page":random_int,"page_size":1}
                )
                response.raise_for_status()
                image_url = response.json()["results"][0]["url"]
                
                print(f"Fetched openverse image URL: {image_url}")
                # Download and process image
                img = fetch_image_from_url(image_url)
                grayscale_image, dithered_image = preper_image(img, label_width=printer_info['label_width'])
                
                # Store in session state
                st.session_state.openverse_image_grayscale = grayscale_image
                st.session_state.openverse_image_dithered = dithered_image
                
            except Exception as e:
                logger.error(f"Error fetching img: {str(e)}")
                st.error(f"Error fetching img: {str(e)}")
            
        # Show image and print button if we have a img
        if st.session_state.openverse_image_dithered is not None:
            st.image(st.session_state.openverse_image_dithered, caption=f"{visible_name_string}")
            if st.button(f"Print {visible_name_string} Img"):
                print_image(st.session_state.openverse_image_grayscale, printer_info, dither=True)
                st.success("Image sent to printer!")
