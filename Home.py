import streamlit as st
import time
from styles.styles import style_global, style_buttons, styles_home

# Set page configuration for the homepage
st.set_page_config(
    page_title="ArtiSelf",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply existing styles
st.markdown(style_global + style_buttons + styles_home, unsafe_allow_html=True)

# st.markdown(home_styles, unsafe_allow_html=True)

# Create a spinning animation for loading
def load_with_animation():
    with st.spinner("Loading the creative experience..."):
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.01)
        progress_bar.empty()

# Hero Section with Animation
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">ArtiSelf</h1>
        <p class="hero-subtitle">
            Discover your artistic evolution through AI-assisted creation.
            Transform concepts into visual art and track your creative journey.
        </p>
        <button class="cta-button" id="start-button">
            Begin Your Artistic Journey
        </button>
    </div>
""", unsafe_allow_html=True)

# Feature section
st.markdown("<h2 style='text-align: center; margin-top: 50px; margin-bottom: 30px;'>Key Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🖌️</div>
            <div class="feature-title">AI-Powered Creation</div>
            <p class="feature-text">
                Transform your initial concepts into stunning artworks with advanced AI image generation.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <div class="feature-title">Artistic Evolution</div>
            <p class="feature-text">
                Apply different creative strategies to evolve your artwork through multiple iterations.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🪄</div>
            <div class="feature-title">Visual Journey</div>
            <p class="feature-text">
                Track your creative process with interactive visualizations showing your artistic development.
            </p>
        </div>
    """, unsafe_allow_html=True)

# How it works section
st.markdown("<h2 style='text-align: center; margin-top: 60px; margin-bottom: 30px;'>How It Works</h2>", unsafe_allow_html=True)

st.markdown("""
    <div class="how-it-works-step">
        <div class="step-number">1</div>
        <div>
            <h4>Create Initial Artwork</h4>
            <p>Enter your artistic concept and let ArtiSelf generate a visual representation.</p>
        </div>
    </div>
    
    <div class="how-it-works-step">
        <div class="step-number">2</div>
        <div>
            <h4>Apply Process Modifications</h4>
            <p>Choose from various artistic strategies to transform and evolve your artwork.</p>
        </div>
    </div>
    
    <div class="how-it-works-step">
        <div class="step-number">3</div>
        <div>
            <h4>Explore Your Artistic Evolution</h4>
            <p>Visualize your creative journey through interactive timelines and comparisons.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# CTA Section
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; 
         background: linear-gradient(to right, rgba(238,174,202,0.1), rgba(148,187,233,0.1)); 
         border-radius: 15px;">
        <h2 style="margin-bottom: 1.5rem; color: #333;">Ready to Begin?</h2>
        <p style="margin-bottom: 2rem; font-size: 1.1rem; color: #555;">
            Start your artistic journey today and discover new dimensions of your creativity.
        </p>
    </div>
""", unsafe_allow_html=True)

# Create a larger button at the bottom
if st.button("Start Creating Now", type="primary", use_container_width=True):
    load_with_animation()
    st.switch_page("pages/01_Create_Artworks.py")

# Footer
st.markdown("""
    <div class="footer">
        <p>ArtiSelf © 2025 | Developed by Jessica Yin (ruhany@andrew.cmu.edu)</p>
    </div>
""", unsafe_allow_html=True)