import os
from dotenv import load_dotenv
import replicate

load_dotenv()
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

def analyze_image(image_url: str) -> str:
    """
    Analyze an image to extract artistic elements useful for further modifications.
    
    Args:
        image_url (str): The URL or file path to the image.
    
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
        output = client.run(
            "yorickvp/llava-13b:80537f9eead1a5bfa72d5ac6ea6414379be41d4d4f6679fd776e9535d1eb58bb",
            input={
                "image": image_url,
                "prompt": analysis_prompt,
                "temperature": 0.5,
                "max_tokens": 500
            }
        )
        analysis = "".join(output) if isinstance(output, list) else str(output)
        return analysis
    except Exception as e:
        return f"Error analyzing image: {str(e)}. Proceeding with modification based on textual concept only."
