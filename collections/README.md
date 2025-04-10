# ArtiSelf Collections

This directory stores artwork evolution collections created in the ArtiSelf application. Each collection represents a complete artistic journey from initial concept to final artwork, with all intermediate evolutionary steps preserved.

## Collection Structure

Each collection is stored in its own subdirectory with a unique ID based on the collection name and timestamp:

```
collections/
├── Collection_Name_20250410_123456/
│   ├── metadata.json
│   └── images/
│   ├── generated_image1.png
│   ├── generated_image2.png
│   └── generated_image3.png
├── Another_Collection_20250410_234567/
│   ├── metadata.json
│   └── images/
│   ├── generated_image1.png
│   ├── generated_image2.png
│   └── generated_image3.png
└── ...
```

## Metadata Format

Each collection contains a `metadata.json` file with the following information:

```json
{
  "name": "Collection Name",
  "description": "Optional description of the collection",
  "created_at": "2025-04-10T12:34:56.789012",
  "updated_at": "2025-04-10T13:45:23.456789",
  "art_history": [
    {
      "concept": "Initial artwork concept",
      "image_url": "images/generated_image1.png",
      "timestamp": "2025-04-10T12:34:56.789012"
    },
    {
      "concept": "Modified concept",
      "image_url": "images/generated_image2.png",
      "timestamp": "2025-04-10T12:38:12.345678",
      "parent_id": 0
    },
    {
      "concept": "Final refined concept",
      "image_url": "images/generated_image3.png",
      "timestamp": "2025-04-10T12:45:34.567890",
      "parent_id": 1
    }
  ]
} 
```

## Working with Collections

### Loading Collections
Collections can be loaded from the Collections page. When a collection is loaded:

- The full art history is restored
- You can continue evolving the artwork from where you left off
- You can update the existing collection or save as a new one

### Updating Collections
When you load a collection and make changes:

- New generated images are added to the collection
- The evolution history is updated
- The collection's updated_at timestamp is refreshed

### Deleting Collections
Collections can be deleted from the Collections management page. This action cannot be undone and will remove all associated image files.

## Guidelines
- Back Up Important Collections: While this storage system is designed to be reliable, consider backing up particularly valuable collections.
- Collection Names: Use descriptive names to easily identify collections later.
- Descriptions: Adding a detailed description helps track your artistic intent and process.

## Technical Notes
- Images are stored as PNG files within each collection's images directory
- The application maintains relative paths in the metadata for portability
- When loading collections, paths are converted to absolute paths for the session