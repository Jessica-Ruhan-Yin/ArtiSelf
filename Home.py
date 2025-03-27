import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from styles.styles import style_sidebar

# title of the homepage
st.set_page_config(
    page_title="Artiself",
    page_icon=":artist:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style the sidebar
st.markdown(style_sidebar, unsafe_allow_html=True)

# Title section
st.markdown("""
    <div class="hero-section">
        <h1 style='color: white; font-size: 56px;'>Discover Your Artistic Self</h1>
        <p style='color: white; font-size: 20px;'>Transform your creativity with AI-powered tools designed for artists of all levels</p>
        <a href='#' style='color: white' class='cta-button'>Start Creating Now</a>
    </div>
""", unsafe_allow_html=True)