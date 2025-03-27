import streamlit as st
from styles.styles import style_global
from utils.art_graph import generate_artwork
import os

# Set page configuration
st.set_page_config(
    page_title="Artiself - Create Artworks",
    page_icon=":artist:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(style_global, unsafe_allow_html=True)

# Page title and introduction
st.title("Create Artworks")
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Begin your artistic journey by providing a concept or idea.</p>", unsafe_allow_html=True)

# Input section
st.header("Your Artistic Concept")
art_concept = st.text_area(
    "Describe your artistic idea or concept:", 
    help="For example: A surreal underwater cityscape with floating buildings and bioluminescent sea creatures",
    height=150
)

# Image generation button
if st.button("Generate Artwork"):
    if art_concept:
        with st.spinner("Creating your artwork..."):
            result = generate_artwork(art_concept)
            refined_concept = result["art_concept"]
            image_path = result["current_image_url"]

            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.header("Refined Concept")
                st.write(refined_concept)
            with col2:
                st.header("Generated Artwork")
                try:
                    if os.path.exists(image_path):
                        st.image(image_path, caption="Generated Artwork")
                    else:
                        st.warning("Image file not found. Please try again.")
                        st.image("images/example_image.png", caption="Placeholder Artwork")
                    
                    if "art_history" not in st.session_state:
                        st.session_state.art_history = []
                    st.session_state.art_history.append({
                        "concept": refined_concept,
                        "image_url": image_path,
                        "iteration": 0
                    })
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
                    st.exception(e)
    else:
        st.warning("Please enter an artistic concept first.")