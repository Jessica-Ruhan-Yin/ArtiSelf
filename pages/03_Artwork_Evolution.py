import streamlit as st
from styles.styles import style_global, style_custom, style_buttons
from utils.timeline_visualization import visualize_art_history

def configure_page():
    """Configure the page settings and apply global styles."""
    st.set_page_config(
        page_title="Artiself - Artwork Evolution",
        page_icon=":artist:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(style_global + style_custom + style_buttons, unsafe_allow_html=True)

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


def main():
    configure_page()
    display_title()
    art_history = get_art_history()
    display_metrics(art_history)
    visualize_art_history(art_history)

if __name__ == "__main__":
    main()
