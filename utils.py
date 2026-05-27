import streamlit as st
import logging
from PIL import Image

logger = logging.getLogger("sticker_factory.utils")

def fetch_image_from_url(url):
    """Validate and fetch image from URL."""
    if not url.startswith('https://'):
        st.error('Only HTTPS URLs are allowed for security')
        return None
        
    try:
        import requests
        from io import BytesIO
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Verify content type is an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            st.error('URL does not point to a valid image')
            return None
            
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        st.error(f'Error fetching image: {str(e)}')
        return None
