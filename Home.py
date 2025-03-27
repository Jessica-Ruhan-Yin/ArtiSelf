import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from styles.styles import style_global

# Set page configuration for the homepage
st.set_page_config(
    page_title="Artiself",
    page_icon=":artist:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(style_global, unsafe_allow_html=True)

# Title section
st.markdown("""
    <div class="hero-section">
        <h1 style='color: white; font-size: 56px;'>Discover Your Artistic Self</h1>
        <p style='color: white; font-size: 20px; text-align: center;'>
            Transform your creativity with AI-powered tools designed for artists of all levels
        </p>
    </div>
""", unsafe_allow_html=True)
if st.button("Start Creating Now"):
    # Redirect to the Create Artworks page
    st.switch_page("pages/01_Create_Artworks.py")