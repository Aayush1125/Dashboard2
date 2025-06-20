import streamlit as st
import requests

# File ID from Google Drive
file_id = "1IS8Vjv4oHzHoBOIvLwCmeTrlFFt0_WnU"

# Use gdretrieve (Cloudflare worker proxy) to fetch raw HTML
url = f"https://www.gdretrieve.workers.dev/{file_id}"

try:
    response = requests.get(url)
    response.raise_for_status()
    st.components.v1.html(response.text, height=800, scrolling=True)
except Exception as e:
    st.error(f"Failed to load HTML: {e}")
