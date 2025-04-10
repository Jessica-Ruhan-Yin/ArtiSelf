import streamlit as st
import os
from styles.styles import style_global, style_buttons, create_artwork_styles
from styles.empty_state import empty_state_html
from utils.art_graph import generate_artwork
from streamlit.components.v1 import html

def configure_page():
    """Configure page settings and apply styles."""
    st.set_page_config(
        page_title="Artiself - Create Artworks",
        page_icon=":artist:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(style_global + style_buttons + create_artwork_styles, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables if they don't already exist."""
    defaults = {
        "artwork_concept": "",
        "artwork_image_path": "",
        "refined_concept": "",
        "generation_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "art_history" not in st.session_state:
        st.session_state.art_history = []

def display_page_header():
    """Display the title and introductory text for the page."""
    st.markdown('<h1 class="page-title">Create Artworks</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem;'>Begin your artistic journey by providing a concept or idea.</p>",
        unsafe_allow_html=True
    )

def display_input_section():
    """Display the text area for input and a creative tip."""
    st.subheader("Your Artistic Concept")
    art_concept = st.text_area(
        "Describe your artistic idea or concept:",
        value=st.session_state.artwork_concept,
        help="For example: A surreal underwater cityscape with floating buildings and bioluminescent sea creatures",
        height=150,
        key="concept_input"
    )
    st.session_state.artwork_concept = art_concept

    st.markdown(
        """
        <div class="creative-tip">
            <strong>Creative Tip:</strong> Be specific with visual details, atmosphere, and style references 
            for more personalized results. Try phrases like "in the style of..." or "with a mood of..."
        </div>
        """, unsafe_allow_html=True
    )
    return art_concept

def handle_artwork_generation(art_concept):
    """Generate the artwork using the provided concept and update session state."""
    if art_concept:
        with st.spinner("Creating your artwork... This may take a moment as we craft your vision."):
            result = generate_artwork(art_concept)
            st.session_state.generation_result = result
            st.session_state.refined_concept = result["art_concept"]
            st.session_state.artwork_image_path = result["current_image_url"]

            # Add generated artwork to art history
            st.session_state.art_history.append({
                "concept": result["art_concept"],
                "image_url": result["current_image_url"],
                "iteration": 0
            })
    else:
        st.warning("Please enter an artistic concept first.")

def display_artwork_result(result):
    """Display the generated artwork and its refined concept in two columns."""
    st.subheader("Your Generated Artwork")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Refined Concept")
        st.text_area(
            label="Refined Concept",
            value=result["art_concept"],
            height=440,
            label_visibility="collapsed",
            key="refined-concept"
        )

    with col2:
        try:
            if os.path.exists(result["current_image_url"]):
                st.image(
                    result["current_image_url"],
                    caption="Your Generated Artwork",
                    use_container_width=True
                )
            else:
                st.warning("Image file not found. Please try regenerating.")
                st.image("images/example_image.png", caption="Placeholder Artwork")
        except Exception as e:
            st.error(f"Error displaying image: {e}")

def display_next_steps():
    """Display buttons to evolve or regenerate artwork."""
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Evolve This Artwork", type="primary", use_container_width=True):
            st.switch_page("pages/02_Process_Modification.py")
            
    with col2:
        if st.button("Regenerate a new artwork", type="primary", use_container_width=True):
            # Reset the artwork state and remove the last history entry
            st.session_state.generation_result = None
            st.session_state.artwork_image_path = ""
            st.session_state.refined_concept = ""
            if st.session_state.art_history:
                st.session_state.art_history.pop()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def display_empty_state():
    """Show an inspirational empty state when no artwork has been generated."""
    html(empty_state_html, height=600)

def main():
    configure_page()
    initialize_session_state()
    display_page_header()
    
    # Display input area and capture the artistic concept
    art_concept = display_input_section()

    # If user clicks "Generate Artwork", handle artwork generation
    if st.button("Generate Artwork", type="primary", use_container_width=True):
        handle_artwork_generation(art_concept)

    # Display artwork result if available; otherwise, show an inspirational empty state
    if st.session_state.generation_result or st.session_state.artwork_image_path:
        result = st.session_state.generation_result or {
            "art_concept": st.session_state.refined_concept,
            "current_image_url": st.session_state.artwork_image_path
        }
        display_artwork_result(result)
        display_next_steps()
    else:
        display_empty_state()

    # If a prompt was selected from the empty state, update the input and refresh the UI
    if st.session_state.get("selected_prompt"):
        st.session_state.artwork_concept = st.session_state.selected_prompt
        st.session_state.selected_prompt = None
        st.rerun()

if __name__ == "__main__":
    main()