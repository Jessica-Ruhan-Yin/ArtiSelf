import streamlit as st
import os
import json
import datetime
from styles.styles import style_global, style_custom, style_buttons, collection_styles
from utils.collection_util import list_collections, load_collection, delete_collection

def configure_page():
    """Configure page settings and apply styles."""
    st.set_page_config(
        page_title="ArtiSelf - Collections",
        page_icon="🖼️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(style_global + style_custom + style_buttons + collection_styles, unsafe_allow_html=True)

def display_page_header():
    """Display the title and introductory text for the page."""
    st.markdown('<h1 class="page-title">Artwork Collections</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem;'>Manage your saved artwork evolution collections.</p>",
        unsafe_allow_html=True
    )

def format_date(date_str):
    """Format ISO date string to a more readable format."""
    try:
        date_obj = datetime.datetime.fromisoformat(date_str)
        return date_obj.strftime("%b %d, %Y at %I:%M %p")
    except:
        return date_str

def get_collection_thumbnails(collection_id, max_thumbnails=3):
    """Get multiple images from a collection to show the evolution."""
    collection_dir = os.path.join("collections", collection_id)
    metadata_file = os.path.join(collection_dir, "metadata.json")
    
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            art_history = metadata.get("art_history", [])
            if not art_history:
                return []
                
            # Get first, middle and last images for a good overview of evolution
            thumbnails = []
            
            # Always include first image
            if len(art_history) > 0 and "image_url" in art_history[0]:
                img_rel_path = art_history[0]["image_url"]
                thumbnails.append(os.path.join(collection_dir, img_rel_path))
            
            # Add middle image if collection has more than 2 images
            if len(art_history) > 2:
                middle_idx = len(art_history) // 2
                if "image_url" in art_history[middle_idx]:
                    img_rel_path = art_history[middle_idx]["image_url"]
                    thumbnails.append(os.path.join(collection_dir, img_rel_path))
            
            # Always include last image
            if len(art_history) > 1 and "image_url" in art_history[-1]:
                img_rel_path = art_history[-1]["image_url"]
                thumbnails.append(os.path.join(collection_dir, img_rel_path))
                
            return thumbnails
            
        except Exception as e:
            print(f"Error getting collection thumbnails: {e}")
    
    return []

def display_collections():
    """Display all saved collections in a grid layout."""
    collections = list_collections()
    
    if not collections:
        st.info("No collections found. Create and save artwork evolutions to build your collection.")
        if st.button("Go to Create Artworks", use_container_width=True):
            st.switch_page("pages/01_Create_Artworks.py")
        st.stop()
    
    st.markdown("<h2>Your Collections</h2>", unsafe_allow_html=True)
    
    # Use 3 columns for grid layout
    cols_per_row = 3
    
    # Display collections in rows
    for i in range(0, len(collections), cols_per_row):
        row_collections = collections[i:i+cols_per_row]
        cols = st.columns(cols_per_row)
        
        for j, collection in enumerate(row_collections):
            with cols[j]:
                st.markdown(
                    f"""
                    <div class="collection-card">
                        <h4>{collection["name"]}</h4>
                        <p class="collection-meta">Created {format_date(collection["created_at"])}</p>
                        <p class="collection-desc">{collection["description"]}</p>
                        <p class="collection-count">{collection["artwork_count"]} artworks in evolution</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Get thumbnails for the collection
                thumbnails = get_collection_thumbnails(collection["id"], max_thumbnails=3)
                
                if thumbnails:
                    # Create a multi-image preview
                    st.markdown('<div class="thumbnail-container">', unsafe_allow_html=True)
                    for idx, thumbnail in enumerate(thumbnails[:3]):
                        st.image(thumbnail, use_container_width=True, 
                                 caption=f"Step {idx+1}" if idx < len(thumbnails)-1 else "Latest")
                        if idx < len(thumbnails) - 1:
                            st.markdown('<span class="evolution-arrow">→</span>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # Fallback to single thumbnail if available
                    if collection["thumbnail"] and os.path.exists(collection["thumbnail"]):
                        st.image(collection["thumbnail"], use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Load", key=f"load_{collection['id']}", use_container_width=True, type="primary"):
                        load_collection_to_session(collection["id"])
                
                with col2:
                    if st.button("Delete", key=f"delete_{collection['id']}", use_container_width=True, type="primary"):
                        confirm_delete_collection(collection["id"], collection["name"])

def confirm_delete_collection(collection_id, collection_name):
    """Show a confirmation dialog for deleting a collection."""
    # Store the collection info in session state and set flag to show dialog
    st.session_state.delete_collection_id = collection_id
    st.session_state.delete_collection_name = collection_name
    st.session_state.show_delete_dialog = True
    st.rerun()

def load_collection_to_session(collection_id):
    """Load a collection into the session state and navigate to the artwork evolution page."""
    collection_data = load_collection(collection_id)
    
    if collection_data and "art_history" in collection_data:
        # Store the collection in session state
        st.session_state.art_history = collection_data["art_history"]
        
        # Store the collection ID and name for possible updates later
        st.session_state.current_collection_id = collection_id
        st.session_state.current_collection_name = collection_data.get("name", "Unnamed Collection")
        st.session_state.current_collection_description = collection_data.get("description", "")
        
        # Get the last artwork for current view
        if st.session_state.art_history:
            latest = st.session_state.art_history[-1]
            st.session_state.artwork_concept = latest.get("concept", "")
            st.session_state.artwork_image_path = latest.get("image_url", "")
            st.session_state.refined_concept = latest.get("concept", "")
            st.session_state.generation_result = {
                "art_concept": latest.get("concept", ""),
                "current_image_url": latest.get("image_url", "")
            }
        
        st.success(f"Loaded collection: {collection_data.get('name', 'Unnamed Collection')}")
        # Navigate to the artwork evolution page
        st.switch_page("pages/03_Artwork_Evolution.py")
    else:
        st.error("Could not load collection. The data might be corrupted.")

def show_delete_dialog():
    """Display a dialog for confirming deletion."""
    if not st.session_state.get("show_delete_dialog"):
        return
    
    collection_id = st.session_state.get("delete_collection_id")
    collection_name = st.session_state.get("delete_collection_name", "this collection")
    
    # Create a container with styling to make it look like a modal dialog
    with st.container():
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15); max-width: 500px; 
                        margin: 0 auto; text-align: center;">
                <h3>Confirm Deletion</h3>
                <p>Are you sure you want to delete this collection?</p>
                <p><strong>This action cannot be undone.</strong></p>
            </div>
        """, unsafe_allow_html=True)
        
        _, col2, col3, _ = st.columns(4)
        with col2:
            if st.button("Cancel", use_container_width=True, type="primary"):
                st.session_state.show_delete_dialog = False
                st.rerun()
        
        with col3:
            if st.button("Delete", use_container_width=True, type="primary"):
                if delete_collection(collection_id):
                    st.session_state.show_delete_dialog = False
                    st.success(f"Collection '{collection_name}' has been deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete the collection.")

def init_session_state():
    """Initialize session state variables."""
    if "show_delete_dialog" not in st.session_state:
        st.session_state.show_delete_dialog = False

def main():
    configure_page()
    init_session_state()
    display_page_header()
    
    if st.session_state.get("show_delete_dialog"):
        show_delete_dialog()
    
    display_collections()

if __name__ == "__main__":
    main()