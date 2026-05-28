"""Webcam tab content."""

import streamlit as st
from PIL import Image

from image_utils import (
    preper_image,
)
from printer_utils import (
    print_image,
)

def render(printer_info):
    """Render the Webcam tab."""
    st.subheader(":printer: a selfie")
    on = st.toggle("ask user for camera permission")
    if on:
        picture = st.camera_input("Take a picture")
        if picture is not None:
            # Convert and process image
            picture = Image.open(picture).convert("RGB")
            grayscale_image, dithered_image = preper_image(picture, label_width=printer_info['label_width'])

            # Display processed image
            st.image(dithered_image, caption="Resized and Dithered Image")

            # Print options
            colc, cold = st.columns(2)
            with colc:
                if st.button("Print rotated Image", key="print_rotated_webcam"):
                    print_image(grayscale_image, printer_info, rotate=90, dither=True)
                    st.balloons()
                    st.success("rotated image sent to printer!")
            with cold:
                if st.button("Print Image", key="print_webcam"):
                    print_image(grayscale_image, printer_info, dither=True)
                    st.success("image sent to printer!")
