import streamlit as st
import requests
import io
import urllib.parse
from PIL import Image

# ==========================================
# 1. INITIALIZATION & SETUP
# ==========================================
st.set_page_config(page_title="Multimodal Studio", page_icon="🎨", layout="wide")
st.title("🎨 Multimodal Image Generation Studio")
st.markdown("Translate natural language descriptions into high-quality digital artwork using Stable Diffusion.")

# ==========================================
# 2. FRONTEND: SIDEBAR PARAMETERS
# ==========================================
st.sidebar.header("🎛️ Design Parameters")
st.sidebar.markdown("Configure your payload constraints.")

# Payload parameters required by the project rubric
image_count = st.sidebar.number_input("Generation Count", min_value=1, max_value=4, value=1)
aspect_ratio = st.sidebar.selectbox("Aspect Ratio (Resolution)", ["Square (1024x1024)", "Landscape (1024x768)", "Portrait (768x1024)"])

# Map aspect ratio to actual width/height for the payload
if aspect_ratio == "Square (1024x1024)":
    width, height = 1024, 1024
elif aspect_ratio == "Landscape (1024x768)":
    width, height = 1024, 768
else:
    width, height = 768, 1024

# ==========================================
# 3. BACKEND: API INTEGRATION LOGIC (UPDATED)
# ==========================================
def generate_image(prompt, w, h, seed):
    """Handles the API call and binary stream processing using Pollinations API."""
    
    # URL encode the prompt so it can be passed safely in the web request
    safe_prompt = urllib.parse.quote(prompt)
    
    # Setting up the payload parameters (width, height, and seed for variation)
    # The 'nologo=true' parameter removes the API watermark
    API_URL = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={w}&height={h}&seed={seed}&nologo=true"
    
    # Sending request to the API
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        # Fulfilling the binary stream handling requirement
        return response.content 
    else:
        st.error(f"API Error: {response.status_code}")
        return None

# ==========================================
# 4. FRONTEND: USER INPUT & DISPLAY
# ==========================================
st.subheader("Text-to-Image Prompt")
prompt = st.text_area("Describe the image you want to generate:", "A futuristic cyberpunk city at sunset, neon lights, highly detailed, digital art")

if st.button("✨ Generate Artwork", use_container_width=True):
    if not prompt:
        st.warning("⚠️ Please enter a text prompt.")
    else:
        st.markdown("### 🖼️ Generated Results")
        
        # Create columns based on the generation count requested
        cols = st.columns(image_count)
        
        for i in range(image_count):
            with cols[i]:
                with st.spinner(f"Generating Image {i+1}..."):
                    
                    # We pass 'i' as a seed parameter so each image in the batch is unique
                    image_bytes = generate_image(prompt, width, height, seed=i+42)
                    
                    if image_bytes:
                        # Convert binary stream to a readable image using io and PIL
                        image = Image.open(io.BytesIO(image_bytes))
                        
                        # Display cleanly to the user
                        st.image(image, caption=f"Result {i+1} ({width}x{height})", use_column_width=True)
                        
                        # Add a download button for the binary data
                        st.download_button(
                            label=f"⬇️ Download Image {i+1}",
                            data=image_bytes,
                            file_name=f"generated_art_{i+1}.png",
                            mime="image/png"
                        )