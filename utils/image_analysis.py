import os
import base64
from dotenv import load_dotenv
import replicate
import requests
from PIL import Image
import io

load_dotenv()
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

def analyze_image(image_path: str) -> str:
    """
    Analyze an image to extract artistic elements useful for further modifications.
    
    Args:
        image_path (str): The local file path to the image.
    
    Returns:
        str: A detailed analysis of the image.
    """
    if not REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN environment variable is not set")
    
    client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    
    analysis_prompt = (
        "Analyze this image as a work of art. Describe:\n"
        "1. The main visual elements and subjects\n"
        "2. The composition and structure\n"
        "3. The color palette and lighting\n"
        "4. The style and technique\n"
        "5. The mood and emotional impact\n"
        "6. Areas with potential for artistic development or refinement\n\n"
        "Provide specific details that would be useful for guiding further artistic iterations."
    )
    
    try:
        # Check if image_path is a local file
        if os.path.isfile(image_path):
            # Create a temporary upload to get a valid URL
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # Convert to base64 for upload
            image_b64 = base64.b64encode(image_data).decode("utf-8")
            
            # Use the data URI scheme which is supported by the API
            image_uri = f"data:image/png;base64,{image_b64}"
            
            output = client.run(
                "yorickvp/llava-13b:80537f9eead1a5bfa72d5ac6ea6414379be41d4d4f6679fd776e9535d1eb58bb",
                input={
                    "image": image_uri,
                    "prompt": analysis_prompt,
                    "temperature": 0.5,
                    "max_tokens": 500
                }
            )
        else:
            # If it's not a local file, assume it's a URL
            if not image_path.startswith(("http://", "https://")):
                image_path = f"https://{image_path}" if not image_path.startswith("//") else f"https:{image_path}"
            
            output = client.run(
                "yorickvp/llava-13b:80537f9eead1a5bfa72d5ac6ea6414379be41d4d4f6679fd776e9535d1eb58bb",
                input={
                    "image": image_path,
                    "prompt": analysis_prompt,
                    "temperature": 0.5,
                    "max_tokens": 500
                }
            )
        
        if hasattr(output, '__iter__') and not isinstance(output, (str, list)):
            analysis = "".join([chunk for chunk in output])
        elif isinstance(output, list):
            analysis = "".join(output)
        else:
            analysis = str(output)
        return analysis
    except Exception as e:
        return f"Error analyzing image: {str(e)}. Proceeding with modification based on textual concept only."