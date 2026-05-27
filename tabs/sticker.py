"""Sticker tab content."""

import logging
import streamlit as st
import os
from PIL import Image
import io

logger = logging.getLogger("sticker_factory.tabs.sticker")

from utils import fetch_image_from_url

def render(preper_image, print_image,printer_info):
    """Render the Sticker tab."""
    st.subheader(":printer: a sticker")

    # Check if there's a selected image from history
    if 'selected_image_path' in st.session_state:
        image_path = st.session_state.selected_image_path
        try:
            image_to_process = Image.open(image_path).convert("RGB")
            grayscale_image, dithered_image = preper_image(image_to_process, label_width=printer_info['label_width'])
            
            st.info(f"Image loaded from history: {os.path.basename(image_path)}")
            
            # Create checkboxes for rotation and dithering
            col1, col2 = st.columns(2)
            with col1:
                dither_checkbox = st.checkbox(
                    "Dither - _use for high detail, true by default_", value=True,
                    key="dither_history"
                )
            with col2:
                rotate_checkbox = st.checkbox("Rotate - _90 degrees_", key="rotate_history")

            # Display image based on checkbox status
            if dither_checkbox:
                st.image(dithered_image, caption="Resized and Dithered Image")
            else:
                st.image(image_to_process, caption="Original Image")

            # Print button
            button_text = "Print "
            if rotate_checkbox:
                button_text += "Rotated "
            if dither_checkbox:
                button_text += "Dithered "
            button_text += "Image"

            if st.button(button_text, key="print_history"):
                rotate_value = 90 if rotate_checkbox else 0
                dither_value = dither_checkbox
                print_image(image_to_process, rotate=rotate_value, dither=dither_value)
                
            if st.button("Clear Selection"):
                del st.session_state.selected_image_path
                st.rerun()
                
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
            del st.session_state.selected_image_path
            st.rerun()

    # Allow the user to upload an image
    uploaded_image = st.file_uploader(
        "Choose an image file to print", type=["png", "jpg", "gif", "webp"],
        key="sticker_file_uploader"
    )
    
    # Or fetch from URL
    image_url = st.text_input("Or enter an HTTPS image URL to fetch and print")

    # Process uploaded file or URL
    if uploaded_image is not None:
        image_to_process = None
        original_filename_without_extension = os.path.splitext(uploaded_image.name)[0]
        
        # Convert the uploaded file to a PIL Image # TODO: Why is this different between sticker and sticker_pro
        image_to_process = Image.open(uploaded_image).convert("RGB")

        if image_to_process:
            grayscale_image, dithered_image = preper_image(image_to_process, label_width=printer_info['label_width'])

            # Paths to save the original and dithered images in the 'temp' directory with postfix
            original_image_path = os.path.join(
                "temp", original_filename_without_extension + "_original.png"
            )

            # Create checkboxes for rotation and dithering (dither default to True) inline
            col1, col2 = st.columns(2)
            with col1:
                dither_checkbox = st.checkbox(
                    "Dither - _use for high detail, true by default_", value=True,
                    key="sticker_dither"
                )
            with col2:
                rotate_checkbox = st.checkbox("Rotate - _90 degrees_", key="sticker_rotate")

            # Determine the button text based on checkbox states
            button_text = "Print "
            if rotate_checkbox:
                button_text += "Rotated "
            if dither_checkbox:
                button_text += "Dithered "
            button_text += "Image"

            # Create a single button with dynamic text
            if st.button(button_text, key="sticker_print"):
                rotate_value = 90 if rotate_checkbox else 0
                dither_value = dither_checkbox
                print_image(image_to_process,printer_info, rotate=rotate_value, dither=dither_value)

            # Display image based on checkbox status
            try:
                if dither_checkbox:
                    st.image(dithered_image, caption="Resized and Dithered Image")
                else:
                    st.image(image_to_process, caption="Original Image")
            

                # Create 'temp' directory if it doesn't exist
                os.makedirs("temp", exist_ok=True)
                
                # Save original image
                image_to_process.save(original_image_path, "PNG")
            except ValueError as e:
                logger.error(f"Error displaying image: {str(e)}")
        
    elif image_url:
        # Try to fetch and process image from URL
        image_to_process = fetch_image_from_url(image_url)
        if image_to_process:
            
            # Process the fetched image
            grayscale_image, dithered_image = preper_image(image_to_process, label_width=printer_info['label_width'])
            
            # Create checkboxes for rotation and dithering
            col1, col2 = st.columns(2)
            with col1:
                dither_checkbox = st.checkbox(
                    "Dither - _use for high detail, true by default_", value=True,
                    key="dither_url"
                )
            with col2:
                rotate_checkbox = st.checkbox("Rotate - _90 degrees_", key="rotate_url")

            # Determine button text
            button_text = "Print "
            if rotate_checkbox:
                button_text += "Rotated "
            if dither_checkbox:
                button_text += "Dithered "
            button_text += "Image"

            # Print button
            if st.button(button_text, key="print_url"):
                rotate_value = 90 if rotate_checkbox else 0
                dither_value = dither_checkbox
                print_image(image_to_process, rotate=rotate_value, dither=dither_value)

            # Display image based on checkbox status
            if dither_checkbox:
                st.image(dithered_image, caption="Resized and Dithered Image")
            else:
                st.image(image_to_process, caption="Original Image")

            # # Save original image
            # original_image_path = os.path.join("temp", filename)
            # image_to_process.save(original_image_path, "PNG")

