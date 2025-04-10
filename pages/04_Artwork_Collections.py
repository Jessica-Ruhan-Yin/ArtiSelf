import streamlit as st
import os
import json
import datetime
import base64
from io import BytesIO
from PIL import Image
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
    
    # Apply custom styles
    st.markdown(style_global + style_custom + style_buttons + collection_styles, unsafe_allow_html=True)
    
    # Add custom CSS for fixing the image display issues
    st.markdown("""
    <style>
        /* Fix image display in cards */
        .stImage img {
            width: 100%;
            border-radius: 8px;
            object-fit: cover;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Make the captions prettier */
        .stImage figcaption {
            text-align: center;
            font-size: 0.8rem;
            color: #64748B;
            margin-top: 0.3rem;
            font-weight: 500;
        }
        
        /* Fix layout spacing */
        .row-widget.stButton {
            margin-bottom: 0.75rem;
        }
        
        /* Fix for collection cards */
        .collection-card {
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            height: auto;
            min-height: 350px;
        }
        
        /* Override Streamlit container padding */
        .block-container {
            padding: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

def display_page_header():
    """Display the title and introductory text for the page."""
    st.markdown('<h1 class="page-title">Artwork Collections</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem; color: #64748B; max-width: 600px; margin: 0 auto;'>"
        "Explore and manage your saved artwork evolutions. Each collection captures the journey of your artistic vision."
        "</p>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

def format_date(date_str):
    """Format ISO date string to a more readable format."""
    try:
        date_obj = datetime.datetime.fromisoformat(date_str)
        return date_obj.strftime("%b %d, %Y at %I:%M %p")
    except:
        return date_str

def encode_image_to_base64(image_path, max_size=(300, 300)):
    """
    Encode an image to base64 string with optional resizing.
    
    Args:
        image_path: Path to the image file
        max_size: Maximum width and height for resizing
        
    Returns:
        Base64 encoded string of the image
    """
    try:
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return ""
            
        with Image.open(image_path) as img:
            # Resize the image while preserving aspect ratio
            img.thumbnail(max_size)
            
            # Convert to RGB if RGBA to avoid PNG transparency issues
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                
            # Save to a BytesIO object
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            
            # Encode to base64
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str
    except Exception as e:
        print(f"Error encoding image to base64: {e}")
        return ""

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
                full_path = os.path.join(collection_dir, img_rel_path)
                if os.path.exists(full_path):
                    thumbnails.append(full_path)
            
            # Add middle image if collection has more than 2 images
            if len(art_history) > 2:
                middle_idx = len(art_history) // 2
                if "image_url" in art_history[middle_idx]:
                    img_rel_path = art_history[middle_idx]["image_url"]
                    full_path = os.path.join(collection_dir, img_rel_path)
                    if os.path.exists(full_path):
                        thumbnails.append(full_path)
            
            # Always include last image
            if len(art_history) > 1 and "image_url" in art_history[-1]:
                img_rel_path = art_history[-1]["image_url"]
                full_path = os.path.join(collection_dir, img_rel_path)
                if os.path.exists(full_path):
                    thumbnails.append(full_path)
                
            return thumbnails
            
        except Exception as e:
            print(f"Error getting collection thumbnails: {e}")
    
    return []

def display_collections():
    """Display all saved collections in a grid layout."""
    collections = list_collections()
    
    if not collections:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🖼️</div>
                <h3 class="empty-state-title">No collections yet</h3>
                <p class="empty-state-desc">Create and save artwork evolutions to build your collection gallery.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Creating Artworks", use_container_width=True, key="create_new_btn", type="primary"):
            st.switch_page("pages/01_Create_Artworks.py")
        st.stop()
    
    # Add a "Create New" button at the top right
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin-bottom: 1rem;'>Your Collections</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("+ Create New", key="new_collection", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Create_Artworks.py")
    
    # Instead of building one big HTML string, generate individual cards and use st.columns for layout
    num_cols = 3  # Number of columns in the grid
    
    # Calculate rows needed
    num_rows = (len(collections) + num_cols - 1) // num_cols
    
    # For each row
    for row_idx in range(num_rows):
        # Create columns for this row
        cols = st.columns(num_cols)
        
        # Fill the columns with collections
        for col_idx in range(num_cols):
            collection_idx = row_idx * num_cols + col_idx
            
            # Break if we've reached the end of collections
            if collection_idx >= len(collections):
                break
                
            collection = collections[collection_idx]
            
            with cols[col_idx]:
                # Start of card container
                st.markdown(f"""
                    <div class="collection-card">
                        <h4>{collection["name"]}</h4>
                        <p class="collection-meta">Created {format_date(collection["created_at"])}</p>
                        <p class="collection-desc">{collection["description"]}</p>
                        <p class="collection-count">{collection["artwork_count"]} artworks in evolution</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Get thumbnails for the collection
                thumbnails = get_collection_thumbnails(collection["id"], max_thumbnails=3)
                
                # Display thumbnails
                if thumbnails:
                    # Create columns for the thumbnails
                    if len(thumbnails) == 1:
                        thumb_cols = st.columns(1)
                        with thumb_cols[0]:
                            st.image(thumbnails[0], caption="Single Image", use_container_width=True)
                    elif len(thumbnails) == 2:
                        thumb_cols = st.columns([1, 0.2, 1])
                        with thumb_cols[0]:
                            st.image(thumbnails[0], caption="First", use_container_width=True)
                        with thumb_cols[1]:
                            st.markdown("<div style='display:flex;align-items:center;justify-content:center;height:50%'><span style='font-size:24px;color:#3B82F6;'>→</span></div>", unsafe_allow_html=True)
                        with thumb_cols[2]:
                            st.image(thumbnails[1], caption="Latest", use_container_width=True)
                    elif len(thumbnails) == 3:
                        thumb_cols = st.columns([1, 0.2, 1, 0.2, 1])
                        with thumb_cols[0]:
                            st.image(thumbnails[0], caption="First", use_container_width=True)
                        with thumb_cols[1]:
                            st.markdown("<div style='display:flex;align-items:center;justify-content:center;height:50%'><span style='font-size:24px;color:#3B82F6;'>→</span></div>", unsafe_allow_html=True)
                        with thumb_cols[2]:
                            st.image(thumbnails[1], caption="Middle", use_container_width=True)
                        with thumb_cols[3]:
                            st.markdown("<div style='display:flex;align-items:center;justify-content:center;height:100%'><span style='font-size:24px;color:#3B82F6;'>→</span></div>", unsafe_allow_html=True)
                        with thumb_cols[4]:
                            st.image(thumbnails[2], caption="Latest", use_container_width=True)
                else:
                    # Fallback to single thumbnail if available
                    if collection["thumbnail"] and os.path.exists(collection["thumbnail"]):
                        st.image(collection["thumbnail"], use_container_width=True)
                
                # Action buttons with Streamlit's button components
                btn_cols = st.columns(2)
                with btn_cols[0]:
                    if st.button("📂 Load", key=f"load_{collection['id']}", use_container_width=True, type="primary"):
                        load_collection_to_session(collection["id"])
                with btn_cols[1]:
                    if st.button("🗑️ Delete", key=f"delete_{collection['id']}", use_container_width=True, type="primary"):
                        confirm_delete_collection(collection["id"], collection["name"])
    
    # Add JavaScript for button handling
    st.markdown("""
    <script>
        function handleLoad(collectionId) {
            // Using Streamlit's postMessage to communicate with Python
            window.parent.postMessage({
                type: "streamlit:setComponentValue",
                value: {
                    action: "load",
                    collection_id: collectionId
                }
            }, "*");
        }
        
        function handleDelete(collectionId, collectionName) {
            window.parent.postMessage({
                type: "streamlit:setComponentValue",
                value: {
                    action: "delete",
                    collection_id: collectionId,
                    collection_name: collectionName
                }
            }, "*");
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Handle JavaScript callbacks
    if "component_value" in st.session_state:
        value = st.session_state.component_value
        if value and "action" in value:
            if value["action"] == "load":
                load_collection_to_session(value["collection_id"])
            elif value["action"] == "delete":
                confirm_delete_collection(value["collection_id"], value["collection_name"])

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
        
        # Show success toast notification
        st.toast(f"Collection loaded: {collection_data.get('name', 'Unnamed Collection')}", icon="✅")
        
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
    if "component_value" not in st.session_state:
        st.session_state.component_value = None

def main():
    configure_page()
    init_session_state()
    display_page_header()
    
    if st.session_state.get("show_delete_dialog"):
        show_delete_dialog()
    
    display_collections()

if __name__ == "__main__":
    main()