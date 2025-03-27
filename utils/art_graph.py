from typing import List, TypedDict
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEndpoint
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv
from utils.replicate_image_generator import ImageGenerator

# Load environment variables
load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Define the state schema
class GraphState(TypedDict):
    messages: List[BaseMessage]
    art_concept: str
    current_image_url: str
    iteration: int

# Initialize the LLM
def get_llm():
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        temperature=0.5,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )
    return llm

# Define tools
tools = []

# Define the nodes for the graph
def concept_development(state: GraphState) -> GraphState:
    """Refine the initial concept provided by the user."""
    llm = get_llm()
    
    messages = state["messages"]
    concept = state["art_concept"]
    
    # Prompt the LLM to refine the art concept
    prompt = f"""
    I need to create an artistic concept based on this initial idea: {concept}
    
    Please refine this concept in a way that would work well for an AI image generator.
    Consider:
    - Visual elements that should be included
    - Style, mood, and atmosphere
    - Color palette
    - Composition
    
    Provide a detailed description that could be used as a prompt for image generation.
    """
    
    # TODO: Uncomment the following lines to use the LLM in production
    # response = llm.invoke([HumanMessage(content=prompt)])
    # refined_concept = response
    refined_concept = """
    A surreal underwater cityscape, where futuristic buildings float effortlessly in the deep ocean. The architecture blends organic and sci-fi elements, with translucent domes, spiraling towers, and coral-inspired structures. The city glows with soft, ethereal light from within, casting colorful reflections across the surrounding water. Swarms of bioluminescent sea creatures—jellyfish, manta rays, and fish with glowing patterns—drift gracefully through the scene. Giant kelp-like plants sway gently with the current, their tips sparkling with phosphorescence. In the distance, a glowing abyss adds depth and mystery.
    
    Style: Highly detailed digital painting, with elements of surrealism and dreamlike fantasy. The mood is calm, mysterious, and otherworldly.
    
    Color palette: Deep ocean blues, glowing teals, purples, and soft neon highlights in cyan, pink, and gold.
    
    Composition: Wide panoramic view showing multiple floating buildings at different heights, with sea creatures moving in layers from foreground to background. Light rays filter through the water from above, creating a magical, layered atmosphere.
    """
    
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
