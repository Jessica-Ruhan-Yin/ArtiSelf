import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ImageGenerator:
    def __init__(self):
        self.api_key = os.environ.get("STABILITY_API_KEY")
        self.endpoint = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    def generate_image(self, prompt: str) -> str:
        """
        Generate an image using Stability AI's DreamStudio API.
        Returns the local path to the saved image.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "image/*"
            }
            
            files = {"none": ""}
            form_data = {
                "prompt": prompt,
                "width": "1024",
                "height": "1024",
                "cfg_scale": "7.0",
                "samples": "1",
                "steps": "30"
            }
            
            # Make the API request
            response = requests.post(
                self.endpoint,
                headers=headers,
                files=files,
                data=form_data
            )
            
            if response.status_code != 200:
                print(f"API request failed with status code {response.status_code}")
                print(f"Response body: {response.text}")
                return "images/example_image.png"
            
            # Create images directory if it doesn't exist
            if not os.path.exists("images/generated_images"):
                os.makedirs("images/generated_images")
            
            # Save the image directly from response content
            image_path = f"images/generated_images/generated_{int(time.time())}.png"
            with open(image_path, "wb") as f:
                f.write(response.content)
            
            print(f"Image saved to {image_path}")
            return image_path
            
        except Exception as e:
            print(f"Error generating image with DreamStudio API: {e}")
            return "images/example_image.png"
