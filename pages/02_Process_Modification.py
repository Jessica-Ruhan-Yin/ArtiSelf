import streamlit as st
import os
from styles.styles import style_global, style_custom, style_buttons, create_artwork_styles
from utils.modification_engine import generate_artwork_with_modification

# --- Page Setup & Styling ---
def configure_page():
    st.set_page_config(
        page_title="Artiself - Process Modification",
        page_icon=":artist:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Combine and apply global and custom styles
    st.markdown(style_buttons + style_global + style_custom + create_artwork_styles, unsafe_allow_html=True)

# --- Page Title & Introduction ---
def display_title():
    st.title("Evolve Your Artwork")
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem;'>Transform your art through creative process modification with AI assistance.</p>",
        unsafe_allow_html=True
    )

def get_created_artwork():
    # Initialize art_history if it doesn't exist in session state
    if "art_history" not in st.session_state:
        st.session_state.art_history = []
        
    # Check if art_history is empty
    if not st.session_state.art_history:
        st.info("No artwork found. Please create an initial artwork before using modification.")
        if st.button("Create Initial Artwork", use_container_width=True):
            # Redirect to artwork creation page
            st.switch_page("pages/01_Create_Artworks.py")
        st.stop()
    
    return st.session_state.art_history[-1]

# --- Artwork Display Functions ---
def display_artwork(title, artwork):
    st.header(title)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="concept-display">', unsafe_allow_html=True)
        st.subheader("Concept")
        st.text_area(label="Concept", value=artwork["concept"], height=490, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="artwork-display">', unsafe_allow_html=True)
        st.subheader("Image")
        st.image(artwork["image_url"], caption=f"Iteration {artwork['iteration']}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Modification Options & Interaction ---
def display_modification_options(mod_options, strategy_desc):
    st.header("Process Modification")
    st.markdown(
        "<p style='font-size: 1.1rem;'>Select a strategy to modify your artwork. Click the Strategy Cards below to learn more about this option. </p>",
        unsafe_allow_html=True
    )

    # Set default selected strategy if not already in session state
    if "selected_strategy" not in st.session_state:
        # Default to the first option if no previous selection exists
        st.session_state.selected_strategy = mod_options[0]

    # Initialize session state for selected strategy if not already set
    for i in range(0, len(mod_options), 3):
        cols = st.columns(3)
        for j, option in enumerate(mod_options[i:i+3]):
            with cols[j]:
                title = option.split(" (")[0]
                description = option.split(" (")[1].replace(")", "") if "(" in option else ""
                button_label = f"""{title}: {description}"""
                if st.button(button_label, key=option, type="secondary"):
                    st.session_state.selected_strategy = option

    # Update session state from query parameters using st.query_params
    query_params = st.query_params
    if "selected_strategy" in query_params:
        st.session_state.selected_strategy = query_params["selected_strategy"][0]

    st.markdown(
        f"""
        <div class="strategy-description">
            <h3 class="strategy-title">{st.session_state.selected_strategy.split(" (")[0]}</h3>
            <div class="strategy-content">
                <p>{strategy_desc[st.session_state.selected_strategy]}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Apply Modification ---
def apply_modification(latest_artwork, modification_strategy, user_feedback):
    original_concept = st.session_state.art_history[0]["concept"]
    current_concept = latest_artwork["concept"]
    current_image = latest_artwork["image_url"]
    iteration = latest_artwork.get("iteration", 0) + 1

    return generate_artwork_with_modification(
        original_concept=original_concept,
        current_concept=current_concept,
        current_image_url=current_image,
        modification_type=modification_strategy,
        iteration=iteration,
        feedback=user_feedback,
        modification_history=st.session_state.art_history
    )

def display_modification_result(result):
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Modified Concept")
        st.text_area(label="Refined Concept", value=result["refined_concept"], height=500, label_visibility="collapsed")
    with col2:
        st.header("New Artwork")
        if os.path.exists(result["current_image_url"]):
            st.image(result["current_image_url"], caption=f"Iteration {result['iteration']}")
        else:
            st.warning("Image file not found. Please try again.")
    
    st.markdown(
        """
        <div class="creative-tip">
            <strong>Creative Tip:</strong> To continue making process modifications on this artwork, select a new strategy from
            the list above. You can also add your own creative direction to guide the AI.
        </div>
        """, unsafe_allow_html=True
    )

# --- Main Function ---
def main():
    configure_page()
    display_title()
    latest_artwork = get_created_artwork()
    display_artwork("Current Artwork", latest_artwork)
    
    # Define modification options and their descriptions
    modification_options = [
        "AI Recommendation (Let ArtiSelf choose a modification for you)",
        "Reproduce (Create a similar version of your current artwork)",
        "Experimental Play (Introduce random, unexpected elements)",
        "Build on Previous Ideas (Develop concepts from your artistic journey)",
        "Change Scale or Materials (Modify proportions, textures, or elements)",
        "New Subject, Same Style (Apply your technique to different content)",
        "New Subject with Style Refinements (Evolve both content and technique)",
        "New Approach, Same Theme (Reimagine your method while keeping the concept)",
        "Artistic Breakthrough (Create something significantly new but connected)"
    ]
    
    strategy_descriptions = {
        "AI Recommendation (Let ArtiSelf choose a modification for you)": 
            "ArtiSelf will analyze your artistic journey and select the most appropriate next step in your creative evolution.",
        
        "Reproduce (Create a similar version of your current artwork)": 
            "Create another version of your current artwork with minimal changes. This is a good option if you want to refine your existing concept.",
        
        "Experimental Play (Introduce random, unexpected elements)": 
            "Introduce chance operations or unexpected combinations. This strategy encourages spontaneity and can lead to surprising results.",
        
        "Build on Previous Ideas (Develop concepts from your artistic journey)": 
            "Combine and develop elements from your previous artworks. This strategy allows you to evolve your concepts by building on what has already been created.",
        
        "Change Scale or Materials (Modify proportions, textures, or elements)": 
            "Modify size, proportions, colors, or textures while keeping the core concept. This can involve changing the scale of your elements or experimenting with different materials.",
        
        "New Subject, Same Style (Apply your technique to different content)": 
            "Apply your current artistic style to a completely different subject. This allows you to explore new themes while maintaining your established technique.",
        
        "New Subject with Style Refinements (Evolve both content and technique)": 
            "Change your subject while also making subtle refinements to your technique. This approach allows for both thematic and stylistic evolution in your artwork.",
        
        "New Approach, Same Theme (Reimagine your method while keeping the concept)": 
            "Develop a new artistic approach while maintaining the core theme. This strategy encourages you to rethink your methods and techniques while staying true to the original concept.",
        
        "Artistic Breakthrough (Create something significantly new but connected)": 
            "Make a bold conceptual leap that represents major artistic growth. This strategy is for when you feel ready to push the boundaries of your art and create something entirely new, yet still connected to your previous work."
    }
    
    display_modification_options(modification_options, strategy_descriptions)
    
    st.markdown(
        """
        <div style="margin-top: 20px;">
            <h4>Optional: Add Your Creative Direction</h4>
            <p style="color: #666; font-size: 0.9em;">
                Guide ArtiSelf with specific ideas or preferences for this modification.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    user_feedback = st.text_area(
        "Your guidance:", height=100, label_visibility="collapsed",
        placeholder="Example: 'I'd like to explore more vibrant colors' or 'Try a more minimalist approach'"
    )
    
    # Map the selected option to the backend modification type
    strategy_map = {
        "AI Recommendation (Let ArtiSelf choose a modification for you)": None,
        "Reproduce (Create a similar version of your current artwork)": "no_modification",
        "Experimental Play (Introduce random, unexpected elements)": "unsystematic_change",
        "Build on Previous Ideas (Develop concepts from your artistic journey)": "idea_based_change",
        "Change Scale or Materials (Modify proportions, textures, or elements)": "quantitative_modification",
        "New Subject, Same Style (Apply your technique to different content)": "subject_modification",
        "New Subject with Style Refinements (Evolve both content and technique)": "subject_with_method_refinement",
        "New Approach, Same Theme (Reimagine your method while keeping the concept)": "structure_modification",
        "Artistic Breakthrough (Create something significantly new but connected)": "concept_modification"
    }
    selected_strategy = strategy_map[st.session_state.selected_strategy]
    
    if st.button("Apply Modification", type="primary", use_container_width=True):
        with st.spinner("Applying artistic process modification..."):
            result = apply_modification(latest_artwork, selected_strategy, user_feedback)
            display_modification_result(result)

if __name__ == "__main__":
    main()