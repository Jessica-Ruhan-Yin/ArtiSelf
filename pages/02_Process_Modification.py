import streamlit as st
import os
from styles.styles import style_global
from utils.modification_engine import generate_artwork_with_modification

# --- Page Configuration & Global Style ---
st.set_page_config(
    page_title="Artiself - Process Modification",
    page_icon=":artist:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(style_global, unsafe_allow_html=True)

# --- Page Title & Introduction ---
st.title("Process Modification Engine")
st.markdown(
    "<p style='text-align: center; font-size: 1.2rem;'>Improve your artwork through process modification with AI assistance.</p>",
    unsafe_allow_html=True
)

# --- Ensure Existing Artwork ---
if "art_history" not in st.session_state or not st.session_state.art_history:
    st.markdown(
        """
        <div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; text-align: center; margin: 20px 0px;">
            <h3 style="color: #495057; margin-bottom: 15px;">No Artwork Found</h3>
            <p style="color: #6c757d; margin-bottom: 20px;">
                Please create an initial artwork before using the Process Modification Engine.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Go to Create Artworks", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Create_Artworks.py")
    
    st.stop()

# --- Helper Functions ---
def display_artwork(title, artwork):
    st.header(title)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Concept")
        st.text_area(label="Concept", value=artwork["concept"], height=512, label_visibility="collapsed")
    with col2:
        st.subheader("Image")
        st.image(artwork["image_url"], caption=f"Iteration {artwork['iteration']}")

def display_art_history(history):
    st.header("Artistic Evolution")
    st.write(f"Your artwork has gone through {len(history)} iterations.")
    tabs = st.tabs([f"Iteration {i}" for i in range(len(history))])
    for i, (tab, artwork) in enumerate(zip(tabs, history)):
        with tab:
            col1, col2 = st.columns(2)
            with col1:
                st.image(artwork["image_url"], caption=f"Iteration {i}")
            with col2:
                mod_type = artwork.get('modification_type') or "N/A"
                title = "Initial Creation" if i == 0 else f"Modification: {mod_type.replace('_', ' ').title()}"
                st.subheader(title)
                st.text_area(label="Refined Concept History", value=artwork["concept"], height=512, label_visibility="collapsed")
                

# --- Display Current Artwork ---
latest_artwork = st.session_state.art_history[-1]
display_artwork("Current Artwork", latest_artwork)

# --- Modification Options ---
st.header("Process Modification")
st.write("Select a modification strategy or let the AI choose based on your artistic journey:")

modification_options = [
    "AI Selection (Recommended)",
    "1. No modification (reproducing previous work)",
    "2. Unsystematic change (random modifications)",
    "3. Changing subjects and methods based on prior ideas",
    "4. Quantitative modification (changing size/material)",
    "5. Subject modification (applying the same method to new subjects)",
    "6. Subject modification with minor methodological refinements",
    "7. Structure modification (developing new methodology aligned with concept)",
    "8. Concept modification (forming new art concepts guided by creative vision)"
]
selected_option = st.radio("Modification Strategy:", modification_options, index=0)

strategy_descriptions = {
    "AI Selection (Recommended)": "The AI will analyze your artistic journey and select the most appropriate modification strategy.",
    "1. No modification (reproducing previous work)": "Reproduce the existing work with minimal changes.",
    "2. Unsystematic change (random modifications)": "Introduce random, unpredictable changes to explore new possibilities.",
    "3. Changing subjects and methods based on prior ideas": "Develop new directions based on ideas from previous iterations.",
    "4. Quantitative modification (changing size/material)": "Modify aspects such as size, scale, proportions, or materials while keeping the core concept.",
    "5. Subject modification (applying the same method to new subjects)": "Keep the same artistic approach but apply it to a new subject.",
    "6. Subject modification with minor methodological refinements": "Change the subject while making minor refinements to the methodology.",
    "7. Structure modification (developing new methodology aligned with concept)": "Develop a new methodological structure while retaining the core concept.",
    "8. Concept modification (forming new art concepts guided by creative vision)": "Create a new artistic concept that marks a significant evolution."
}
st.info(strategy_descriptions[selected_option])

user_feedback = st.text_area(
    "Optional feedback or guidance:", height=100,
    help="Provide any specific direction or feedback to guide the modification process."
)

strategy_map = {
    "AI Selection (Recommended)": None,  # Let AI decide
    "1. No modification (reproducing previous work)": "no_modification",
    "2. Unsystematic change (random modifications)": "unsystematic_change",
    "3. Changing subjects and methods based on prior ideas": "idea_based_change",
    "4. Quantitative modification (changing size/material)": "quantitative_modification",
    "5. Subject modification (applying the same method to new subjects)": "subject_modification",
    "6. Subject modification with minor methodological refinements": "subject_with_method_refinement",
    "7. Structure modification (developing new methodology aligned with concept)": "structure_modification",
    "8. Concept modification (forming new art concepts guided by creative vision)": "concept_modification"
}
selected_strategy = strategy_map[selected_option]

# --- Apply Modification ---
if st.button("Apply Modification"):
    with st.spinner("Applying artistic process modification..."):
        original_concept = st.session_state.art_history[0]["concept"]
        current_concept = latest_artwork["concept"]
        current_image = latest_artwork["image_url"]
        iteration = latest_artwork.get("iteration", 0) + 1

        result = generate_artwork_with_modification(
            original_concept=original_concept,
            current_concept=current_concept,
            current_image_url=current_image,
            modification_type=selected_strategy,
            iteration=iteration,
            feedback=user_feedback,
            modification_history=st.session_state.art_history
        )

        # Display the results
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Modified Concept")
            st.text_area(label="Refined Concept", value=result["refined_concept"], height=512, label_visibility="collapsed")
            st.subheader("Modification Approach")
            st.write(f"Strategy: {result['modification_type'].replace('_', ' ').title()}")
        with col2:
            st.header("New Artwork")
            if os.path.exists(result["current_image_url"]):
                st.image(result["current_image_url"], caption=f"Iteration {result['iteration']}")
            else:
                st.warning("Image file not found. Please try again.")

# --- Display Art History ---
if len(st.session_state.art_history) > 1:
    display_art_history(st.session_state.art_history)
