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
        Generate an image using the Replicate API with a text-to-image model.
        
        Parameters:
            prompt (str): The text prompt for image generation.
            width (int): Width of the generated image.
            height (int): Height of the generated image.
            num_outputs (int): Number of images to generate (default is 1).
        
        Returns:
            str: Local file path to the saved image.
        """
        try:
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

    def modify_image(self, prompt: str, base_image: str, width: int = 512, height: int = 512, strength: float = 0.6, num_outputs: int = 1) -> str:
        """
        Modify an existing image using an image-variation model from Replicate.
        Note: The chosen model does not accept a text prompt. It creates a variation
        of the given image, so the prompt is ignored.
        
        Parameters:
            prompt (str): The text prompt (ignored in this variation model).
            base_image (str): Path to the base image to modify.
            width (int): Width of the output image.
            height (int): Height of the output image.
            strength (float): (Ignored for this model.)
            num_outputs (int): Number of images to generate (default is 1).
        
        Returns:
            str: Local file path to the saved modified image.
        """
        try:
            # Open the base image file (pass the file object, not raw bytes).
            with open(base_image, "rb") as f:
                input_params = {
                    "input_image": f,  # Pass the file object directly.
                    "num_outputs": 1,
                    "guidance_scale": 5,
                    "num_inference_steps": 25
                }
                
                output = replicate.run(
                    "lambdal/stable-diffusion-image-variation:7c399ba0e1b33ed8ec39ed30eb6b0a2d9e054462543c428c251293034af82a8e",
                    input=input_params
                )
            
            # Expecting output to be a list of image URLs.
            if not output or not isinstance(output, list):
                print("No image URL returned from Replicate API for image variation.")
                return "images/example_image.png"
            
            image_url = output[0]
            print("Modified image URL:", image_url)
            
            # Download the modified image from the URL.
            response = requests.get(image_url, stream=True)
            if response.status_code != 200:
                print("Failed to download modified image, HTTP status code:", response.status_code)
                return "images/example_image.png"
            
            # Create the directory if it does not exist.
            output_dir = "images/generated_images"
            os.makedirs(output_dir, exist_ok=True)
            image_path = os.path.join(output_dir, f"modified_{int(time.time())}.png")
            
            # Save the downloaded image.
            with open(image_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            # Verify the modified image using PIL.
            try:
                with Image.open(image_path) as im:
                    im.verify()
                print("Modified image successfully saved to:", image_path)
                return image_path
            except Exception as e:
                print("Error verifying the modified image file:", e)
                return "images/example_image.png"
        
        except Exception as e:
            print("Error modifying image using Replicate API:", e)
            return "images/example_image.png"
