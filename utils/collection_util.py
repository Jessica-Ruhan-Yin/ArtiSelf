import os
import json
import datetime
from typing import List, Dict, Any, Optional
import streamlit as st
import shutil

COLLECTIONS_DIR = "collections"

def ensure_collections_dir():
    """Ensure the collections directory exists."""
    if not os.path.exists(COLLECTIONS_DIR):
        os.makedirs(COLLECTIONS_DIR)
        # Create a .gitkeep file to ensure the directory is tracked by git
        with open(os.path.join(COLLECTIONS_DIR, ".gitkeep"), "w") as f:
            pass

def save_collection(name: str, description: str, art_history: List[Dict[str, Any]]) -> bool:
    """
    Save an art history collection to disk.
    
    Args:
        name: Name of the collection
        description: Description of the collection
        art_history: List of artwork dictionaries from the session state
    
    Returns:
        bool: True if saved successfully, False otherwise
    """
    ensure_collections_dir()
    
    # Create a sanitized filename
    filename = "".join(c if c.isalnum() or c in [' ', '_'] else '_' for c in name).strip()
    filename = filename.replace(' ', '_')
    
    # Create a unique ID for the collection
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    collection_id = f"{filename}_{timestamp}"
    
    # Create the collection directory
    collection_dir = os.path.join(COLLECTIONS_DIR, collection_id)
    os.makedirs(collection_dir, exist_ok=True)
    
    # Create images directory within the collection
    images_dir = os.path.join(collection_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Copy the image files to the collection directory
    processed_art_history = []
    for item in art_history:
        if "image_url" in item and os.path.exists(item["image_url"]):
            # Get just the filename from the path
            image_filename = os.path.basename(item["image_url"])
            # Create a path within the collection
            collection_image_path = os.path.join(images_dir, image_filename)
            # Copy the image file
            shutil.copy2(item["image_url"], collection_image_path)
            # Update the path in the art history
            item_copy = item.copy()
            item_copy["image_url"] = os.path.join("images", image_filename)
            processed_art_history.append(item_copy)
        else:
            processed_art_history.append(item)
    
    # Create the metadata file
    metadata = {
        "name": name,
        "description": description,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "art_history": processed_art_history
    }
    
    try:
        with open(os.path.join(collection_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving collection: {e}")
        return False

def list_collections() -> List[Dict[str, Any]]:
    """
    List all available collections.
    
    Returns:
        List of dictionaries with collection info
    """
    ensure_collections_dir()
    
    collections = []
    for item in os.listdir(COLLECTIONS_DIR):
        collection_dir = os.path.join(COLLECTIONS_DIR, item)
        metadata_file = os.path.join(collection_dir, "metadata.json")
        
        if os.path.isdir(collection_dir) and os.path.exists(metadata_file):
            try:
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                
                collections.append({
                    "id": item,
                    "name": metadata.get("name", "Unnamed Collection"),
                    "description": metadata.get("description", ""),
                    "created_at": metadata.get("created_at", ""),
                    "updated_at": metadata.get("updated_at", ""),
                    "artwork_count": len(metadata.get("art_history", [])),
                    "thumbnail": get_collection_thumbnail(item)
                })
            except Exception as e:
                st.warning(f"Error reading collection {item}: {e}")
    
    # Sort by created date, newest first
    collections.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return collections

def get_collection_thumbnail(collection_id: str) -> Optional[str]:
    """Get the first image from a collection to use as thumbnail."""
    collection_dir = os.path.join(COLLECTIONS_DIR, collection_id)
    metadata_file = os.path.join(collection_dir, "metadata.json")
    
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            art_history = metadata.get("art_history", [])
            if art_history and "image_url" in art_history[0]:
                # Return the full path to the image
                img_rel_path = art_history[0]["image_url"]
                return os.path.join(collection_dir, img_rel_path)
        except Exception:
            pass
    return None

def load_collection(collection_id: str) -> Dict[str, Any]:
    """
    Load a collection by ID.
    
    Args:
        collection_id: ID of the collection
    
    Returns:
        Dict with metadata and art history or empty dict if not found
    """
    collection_dir = os.path.join(COLLECTIONS_DIR, collection_id)
    metadata_file = os.path.join(collection_dir, "metadata.json")
    
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            # Update the image paths to be absolute
            art_history = metadata.get("art_history", [])
            for item in art_history:
                if "image_url" in item:
                    item["image_url"] = os.path.join(collection_dir, item["image_url"])
            
            metadata["art_history"] = art_history
            return metadata
        except Exception as e:
            st.error(f"Error loading collection: {e}")
    
    return {}

def delete_collection(collection_id: str) -> bool:
    """
    Delete a collection by ID.
    
    Args:
        collection_id: ID of the collection
    
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    collection_dir = os.path.join(COLLECTIONS_DIR, collection_id)
    
    if os.path.exists(collection_dir):
        try:
            shutil.rmtree(collection_dir)
            return True
        except Exception as e:
            st.error(f"Error deleting collection: {e}")
    
    return False

def update_collection(collection_id: str, art_history: List[Dict[str, Any]]) -> bool:
    """
    Update an existing collection with new artwork history.
    
    Args:
        collection_id: ID of the collection to update
        art_history: New art history to save
    
    Returns:
        bool: True if updated successfully, False otherwise
    """
    collection_dir = os.path.join("collections", collection_id)
    metadata_file = os.path.join(collection_dir, "metadata.json")
    
    if not os.path.exists(metadata_file):
        return False
        
    try:
        # Read existing metadata
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        
        # Create images directory within the collection if it doesn't exist
        images_dir = os.path.join(collection_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Copy any new image files to the collection directory and fix paths
        processed_art_history = []
        
        for item in art_history:
            item_copy = item.copy()
            
            if "image_url" in item and item["image_url"]:
                image_path = item["image_url"]
                
                # Check if this is already a path within our collection
                collection_path_prefix = os.path.join("collections", collection_id)
                
                if collection_path_prefix in image_path:
                    # This is already a collection image - extract just the filename
                    filename = os.path.basename(image_path)
                    # Store just the relative path within the collection
                    item_copy["image_url"] = os.path.join("images", filename)
                elif os.path.exists(image_path):
                    # This is a new image from outside the collection - copy it
                    filename = os.path.basename(image_path)
                    target_path = os.path.join(images_dir, filename)
                    shutil.copy2(image_path, target_path)
                    # Store just the relative path within the collection
                    item_copy["image_url"] = os.path.join("images", filename)
            
            processed_art_history.append(item_copy)
        
        # Update the metadata
        metadata["art_history"] = processed_art_history
        metadata["updated_at"] = datetime.datetime.now().isoformat()
        metadata["artwork_count"] = len(processed_art_history)
        
        # Save the updated metadata
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error updating collection: {e}")
        st.error(f"Error updating collection: {e}")
        return False