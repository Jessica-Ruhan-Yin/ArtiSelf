import streamlit as st
from styles.styles import style_sidebar
from utils.art_graph import generate_artwork
import os

# Style the sidebar
st.markdown(style_sidebar, unsafe_allow_html=True)

# Page title
st.title("Create Artwork")

# Introduction
st.markdown("""
    Begin your artistic journey by providing a concept or idea.
""")

# Input section
st.header("Your Artistic Concept")
art_concept = st.text_area("Describe your artistic idea or concept:", 
                           help="For example: A surreal underwater cityscape with floating buildings and bioluminescent sea creatures")

# Generate button
if st.button("Generate Artwork"):
    if art_concept:
        with st.spinner("Creating your artwork..."):
            # Run the Langgraph workflow
            result = generate_artwork(art_concept)
            
            # Extract the results
            refined_concept = result["art_concept"]
            image_path = result["current_image_url"]
            
            # Display the results
            st.header("Refined Concept")
            st.write(refined_concept)
            
            st.header("Generated Artwork")
            try:
                # Check if the image exists
                if os.path.exists(image_path):
                    st.image(image_path, caption="Generated Artwork")
                else:
                    # Fallback to a placeholder if the file doesn't exist
                    st.warning(f"Image file not found. Please try again.")
                    st.image("images/example_image.png", caption="Placeholder Artwork")
                
                # Save to history
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