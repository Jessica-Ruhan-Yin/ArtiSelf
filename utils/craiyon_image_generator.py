import os
import time
import requests
from PIL import Image
from craiyon import Craiyon

class ImageGenerator:
    def __init__(self):
        # Initialize the Craiyon API client.
        self.generator = Craiyon()

    def generate_image(self, prompt: str) -> str:
        """
        Generate an image using the Craiyon API and return the local path to the saved image.
        """
        try:
            # Generate images from the prompt
            result = self.generator.generate(prompt)
            
            # Check if we have images in the result
            if not hasattr(result, 'images') or not result.images:
                print("No images returned from Craiyon API")
                return "images/example_image.png"
            
            # Use the first generated image URL
            image_url = result.images[0]
            print(f"Image URL: {image_url}")
            image_path = f"images/generated_images/generated_{int(time.time())}.png"
            
            # Download the image from the URL
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                
                # Verify the image was saved correctly
                try:
                    Image.open(image_path).verify()  # Verify it's a valid image
                    print(f"Image successfully downloaded and saved to {image_path}")
                    return image_path
                except Exception as e:
                    print(f"Downloaded file is not a valid image: {e}")
                    if os.path.exists(image_path):
                        os.remove(image_path)  # Remove invalid file
            else:
                print(f"Failed to download image: HTTP {response.status_code}")
            
            # If we get here, something went wrong
            print("Falling back to example image")
            return "images/example_image.png"

        except Exception as e:
            print(f"Error generating image with Craiyon API: {e}")
            return "images/example_image.png"