from typing import List, TypedDict
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv
import replicate
from utils.image_generators.replicate_image_generator import ImageGenerator

# Load environment variables
load_dotenv()
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

# Define the state schema
class GraphState(TypedDict):
    messages: List[BaseMessage]
    art_concept: str
    current_image_url: str
    iteration: int

# Initialize the Replicate client and model
def get_llm():
    if not REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN environment variable is not set")    
    return replicate.Client(api_token=REPLICATE_API_TOKEN)

# Define tools
tools = []

# Define the nodes for the graph
def concept_development(state: GraphState) -> GraphState:
    """Refine the initial concept provided by the user."""
    client = get_llm()
    
    messages = state["messages"]
    concept = state["art_concept"]
    
    # Prompt to refine the art concept
    prompt = f"""
    I need to create an artistic concept based on this initial idea: {concept}
    
    Please refine this concept in a way that would work well for an AI image generator.
    Consider:
    - Visual elements that should be included
    - Style, mood, and atmosphere
    - Color palette
    - Composition
    
    Provide a description of around 150 words that could be used as a prompt for image generation.
    """
    
    # Run the Granite model from Replicate
    output = client.run(
        "ibm-granite/granite-3.2-8b-instruct",
        input={
            "prompt": prompt,
            "max_new_tokens": 250,
            "temperature": 0.7,
            "top_p": 0.9,
        }
    )
    
    # Convert the output to a string if it's not already
    if isinstance(output, list):
        refined_concept = "".join(output)
    else:
        refined_concept = str(output)
    
    # Update the state with the refined concept and messages
    state["art_concept"] = refined_concept
    state["messages"].append(HumanMessage(content=prompt))
    state["messages"].append(AIMessage(content=refined_concept))
    
    return state

def create_image(state: GraphState) -> GraphState:
    """Generate an image based on the refined concept."""
    concept = state["art_concept"]
    
    # Instantiate the image generator class and generate the image
    image_generator = ImageGenerator()
    image_url = image_generator.generate_image(concept)
    
    # Update the state with the generated image URL (or file path)
    state["current_image_url"] = image_url
    state["messages"].append(AIMessage(content=f"Generated image: {image_url}"))
    return state

# Define the graph
def create_art_graph():
    # Define the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("concept_development", concept_development)
    workflow.add_node("create_image", create_image)
    
    # Define edges
    workflow.add_edge("concept_development", "create_image")
    workflow.add_edge("create_image", END)
    
    # Set the entry point
    workflow.set_entry_point("concept_development")
    
    # Compile the graph
    return workflow.compile()

# Function to run the graph
def generate_artwork(concept: str):
    # Initialize the state
    state = {
        "messages": [],
        "art_concept": concept,
        "current_image_url": "",
        "iteration": 0
    }
    
    # Create and run the graph
    graph = create_art_graph()
    result = graph.invoke(state)
    
    return result
