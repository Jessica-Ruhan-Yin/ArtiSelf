import os
import time
import requests
import replicate
from PIL import Image

class ImageGenerator:
    def __init__(self):
        # Ensure that the REPLICATE_API_TOKEN environment variable is set.
        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        if not self.api_token:
            raise ValueError("REPLICATE_API_TOKEN not set in environment")

    def generate_image(self, prompt: str, width: int = 512, height: int = 512, num_outputs: int = 1) -> str:
        """
        Generate an image using the Replicate API.
        
        Parameters:
            prompt (str): The text prompt for image generation.
            width (int): Width of the generated image.
            height (int): Height of the generated image.
            num_outputs (int): Number of images to generate (default is 1).
        
        Returns:
            str: Local file path to the saved image.
        """
        try:
            print("Generating image using Replicate API with prompt:", prompt)
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "width": width,
                    "height": height,
                    "num_outputs": num_outputs
                }
            )
            
            # Expecting output to be a list of image URLs.
            if not output or not isinstance(output, list):
                print("No image URL returned from Replicate API.")
                return "images/example_image.png"
            
            image_url = output[0]
            print("Generated image URL:", image_url)
            
            # Download the image from the URL.
            response = requests.get(image_url, stream=True)
            if response.status_code != 200:
                print("Failed to download image, HTTP status code:", response.status_code)
                return "images/example_image.png"
            
            # Create the directory if it does not exist.
            output_dir = "images/generated_images"
            os.makedirs(output_dir, exist_ok=True)
            image_path = os.path.join(output_dir, f"generated_{int(time.time())}.png")
            
            # Save the downloaded image.
            with open(image_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            # Verify the image using PIL.
            try:
                with Image.open(image_path) as im:
                    im.verify()
                print("Image successfully saved to:", image_path)
                return image_path
            except Exception as e:
                print("Error verifying the image file:", e)
                return "images/example_image.png"
        
        except Exception as e:
            print("Error generating image using Replicate API:", e)
            return "images/example_image.png"
