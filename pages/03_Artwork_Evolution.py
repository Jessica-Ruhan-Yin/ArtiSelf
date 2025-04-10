import streamlit as st
from styles.styles import style_global, style_custom, style_buttons
from utils.timeline_visualization import visualize_art_history
from utils.collection_util import save_collection, update_collection
import time

def configure_page():
    """Configure the page settings and apply global styles."""
    st.set_page_config(
        page_title="Artiself - Artwork Evolution",
        page_icon=":artist:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(style_global + style_custom + style_buttons, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "show_save_dialog" not in st.session_state:
        st.session_state.show_save_dialog = False

def display_title():
    """Display the page title and subtitle."""
    st.title("Artistic Evolution Timeline")
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem;'>Explore your artistic journey with interactive visualizations.</p>",
        unsafe_allow_html=True
    )

def get_art_history():
    """Retrieve the artwork history from session state or prompt creation if missing."""
    if "art_history" not in st.session_state or not st.session_state.art_history:
        st.info("No artwork found. Please create an initial artwork before exploring the evolution timeline.")
        if st.button("Go to Create Artworks", use_container_width=True):
            st.switch_page("pages/01_Create_Artworks.py")
        st.stop()
    return st.session_state.art_history

def display_metrics(art_history):
    """Display key metrics about the artwork history in a styled div."""
    total_iterations = len(art_history)
    unique_strategies = len({
        art.get("modification_type", "Initial Creation" if i == 0 else "Unknown")
        for i, art in enumerate(art_history)
    })
    unique_concepts = len({art.get("concept", "") for art in art_history if art.get("concept", "")})
    
    metrics_html = f"""
    <div style="display: flex; justify-content: space-around;
                background: linear-gradient(90deg, rgba(255,179,209,0.2) 0%, rgba(249,246,255,1) 42%, rgba(230,228,255,1) 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 40px;">
        <div style="text-align: center;">
            <h4>Total Iterations</h4>
            <p style="font-size: 1.4rem; margin: 0;">{total_iterations}</p>
        </div>
        <div style="text-align: center;">
            <h4>Unique Strategies</h4>
            <p style="font-size: 1.4rem; margin: 0;">{unique_strategies}</p>
        </div>
        <div style="text-align: center;">
            <h4>Unique Concepts</h4>
            <p style="font-size: 1.4rem; margin: 0;">{unique_concepts}</p>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

def display_save_dialog():
    """Show a dialog to save the current art history as a collection."""
    st.subheader("Save Your Artwork Collection")
    
    collection_name = st.text_input("Collection Name", placeholder="My Creative Journey")
    collection_desc = st.text_area("Description (optional)", placeholder="Describe your artistic process or inspiration...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True, type="primary"):
            st.session_state.show_save_dialog = False
            st.rerun()
    
    with col2:
        if st.button("Save Collection", type="primary", use_container_width=True):
            if not collection_name:
                st.warning("Please provide a name for your collection.")
            else:
                success = save_collection(
                    name=collection_name,
                    description=collection_desc,
                    art_history=st.session_state.art_history
                )
                
                if success:
                    st.session_state.show_save_dialog = False
                    st.session_state.saved_collection_name = collection_name
                    st.rerun()
                else:
                    st.error("Failed to save collection.")

def main():
    configure_page()
    initialize_session_state()
    display_title()
    
    # Show save dialog if active
    if st.session_state.get("show_save_dialog"):
        display_save_dialog()
        st.stop()  # Stop rendering the rest of the page
    
    # Display success message if collection was saved
    if "saved_collection_name" in st.session_state:
        st.success(f"Collection '{st.session_state.saved_collection_name}' saved successfully!")
        # Clear the message after displaying it
        del st.session_state.saved_collection_name
    
    art_history = get_art_history()
    display_metrics(art_history)
    visualize_art_history(art_history)
    
    # Add Collection management buttons
    st.markdown("---")
    
    # Check if we're working with a loaded collection
    if "current_collection_id" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Collection", use_container_width=True, type="primary"):
                if update_collection(st.session_state.current_collection_id, st.session_state.art_history):
                    st.success(f"Collection '{st.session_state.current_collection_name}' updated successfully!")
                    with st.spinner("Refreshing..."):
                        time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to update collection.")
        with col2:
            if st.button("Save as New Collection", use_container_width=True, type="primary"):
                st.session_state.show_save_dialog = True
                st.rerun()
    else:
        # No collection loaded, just show save option
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save as Collection", use_container_width=True, type="primary"):
                st.session_state.show_save_dialog = True
                st.rerun()
        with col2:
            if st.button("Browse Collections", use_container_width=True, type="primary"):
                st.switch_page("pages/04_Artwork_Collections.py")

if __name__ == "__main__":
    main()
