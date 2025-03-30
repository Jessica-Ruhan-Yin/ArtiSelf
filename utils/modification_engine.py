from typing import List, TypedDict, Optional, Dict, Any
from datetime import datetime
import os
from dotenv import load_dotenv
import replicate
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from utils.image_generators.replicate_image_generator import ImageGenerator
from utils.image_analysis import analyze_image

# Load environment variables
load_dotenv()
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")


# ===============================
# STATE DEFINITION
# ===============================
class ModificationState(TypedDict):
    messages: List[BaseMessage]
    original_concept: str
    refined_concept: str
    current_image_url: str
    previous_images: List[str]
    modification_type: str
    iteration: int
    modification_history: List[Dict[str, Any]]
    feedback: str
    image_analysis: Optional[str]


# ===============================
# HELPER FUNCTIONS
# ===============================
def get_llm():
    if not REPLICATE_API_TOKEN:
        raise ValueError("REPLICATE_API_TOKEN environment variable is not set")
    return replicate.Client(api_token=REPLICATE_API_TOKEN)


def _process_modification(state: ModificationState, prompt: str, temperature: float, max_new_tokens: int = 500) -> ModificationState:
    """
    Helper to run the modification prompt and update the concept.
    """
    client = get_llm()
    output = client.run(
        "ibm-granite/granite-3.1-8b-instruct",
        input={"prompt": prompt, "max_new_tokens": max_new_tokens, "temperature": temperature}
    )
    modified_concept = "".join(output) if isinstance(output, list) else str(output)
    state["refined_concept"] = modified_concept
    state["messages"].append(HumanMessage(content=prompt))
    state["messages"].append(AIMessage(content=modified_concept))
    return state


# ===============================
# MODIFICATION STRATEGIES
# ===============================
def no_modification(state: ModificationState) -> ModificationState:
    """Strategy: Reproduce - Create a similar version of your current artwork."""
    state["messages"].append(AIMessage(content="Applying reproduction strategy - creating a refined version of your current artwork."))
    return state


def unsystematic_change(state: ModificationState) -> ModificationState:
    """Strategy: Experimental Play - Introduce random, unexpected elements."""
    current_concept = state["refined_concept"]
    prompt = f"""
Take this artistic concept and introduce playful, experimental modifications:

Original concept: {current_concept}

Create a playful variation by:
1. Introducing unexpected elements or combinations
2. Experimenting with chance operations or randomness
3. Breaking conventional patterns or expectations
4. Allowing for spontaneity and discovery

The changes should feel fresh and surprising while maintaining a connection to the original concept.
    """
    return _process_modification(state, prompt, temperature=0.9)


def idea_based_change(state: ModificationState) -> ModificationState:
    """Strategy: Build on Previous Ideas - Develop concepts from your artistic journey."""
    current_concept = state["refined_concept"]
    # Use the last three iterations from history for context
    previous_ideas = [entry.get("concept", "") for entry in state["modification_history"] if "concept" in entry]
    previous_ideas_text = "\n".join(previous_ideas[-3:])
    prompt = f"""
Develop a new artistic concept by building on ideas from your creative journey:

Current concept: {current_concept}

Previous concepts and ideas:
{previous_ideas_text}

Create a new concept that:
1. Identifies compelling elements or themes from your previous works
2. Combines or transforms these elements in fresh, meaningful ways
3. Builds natural connections to your artistic evolution
4. Takes your creative exploration to its next logical step

This should feel like a natural progression in your artistic development.
    """
    return _process_modification(state, prompt, temperature=0.7)


def quantitative_modification(state: ModificationState) -> ModificationState:
    """Strategy: Change Scale or Materials - Modify proportions, textures, or elements."""
    current_concept = state["refined_concept"]
    prompt = f"""
Transform this artistic concept by changing scale, proportions, or material qualities:

Current concept: {current_concept}

Consider modifications such as:
1. Dramatically changing the scale or size of elements
2. Altering the density, quantity, or arrangement of components
3. Playing with new proportions or spatial relationships
4. Exploring different textures, weights, or material qualities
5. Shifting color relationships, contrasts, or temperature

Keep the core subject and concept intact while transforming these physical aspects.
    """
    return _process_modification(state, prompt, temperature=0.6)


def subject_modification(state: ModificationState) -> ModificationState:
    """Strategy: New Subject, Same Style - Apply your technique to different content."""
    current_concept = state["refined_concept"]
    prompt = f"""
Apply your current artistic approach to an entirely new subject:

Current concept: {current_concept}

To create this transformation:
1. Identify the essential style, technique and treatment in your current artwork
2. Select a completely different subject matter that would create interesting tension or harmony
3. Apply your established artistic approach to this new subject
4. Maintain the same level of complexity and technical approach

This should feel like seeing your artistic voice applied to fresh content.
    """
    return _process_modification(state, prompt, temperature=0.7)


def subject_with_method_refinement(state: ModificationState) -> ModificationState:
    """Strategy: New Subject with Style Refinements - Evolve both content and technique."""
    current_concept = state["refined_concept"]
    prompt = f"""
Transform both your subject matter and refine your artistic technique:

Current concept: {current_concept}

Create this evolution by:
1. Identifying the core stylistic elements of your current approach
2. Selecting a new subject matter that offers fresh creative possibilities
3. Making thoughtful refinements to your technique that enhance the treatment of this new subject
4. Allowing the new subject to inspire subtle shifts in your artistic approach

This should feel like a natural evolution of both what you create and how you create it.
    """
    return _process_modification(state, prompt, temperature=0.7)


def structure_modification(state: ModificationState) -> ModificationState:
    """Strategy: New Approach, Same Theme - Reimagine your method while keeping the concept."""
    current_concept = state["refined_concept"]
    original_concept = state["original_concept"]
    prompt = f"""
Reimagine your artistic approach while maintaining your core thematic focus:

Original concept: {original_concept}
Current concept: {current_concept}

Create this transformation by:
1. Identifying the essential themes and conceptual elements that define your work
2. Developing a completely new visual language or methodological approach
3. Thinking about how artists like Matisse evolved from painting to paper cut-outs
4. Maintaining thematic integrity while dramatically shifting execution

This should feel like seeing your artistic vision through an entirely new lens.
    """
    return _process_modification(state, prompt, temperature=0.7)


def concept_modification(state: ModificationState) -> ModificationState:
    """Strategy: Artistic Breakthrough - Create something significantly new but connected."""
    original_concept = state["original_concept"]
    current_concept = state["refined_concept"]
    # Summarize last three modification entries for context
    history_summary = ""
    for entry in state["modification_history"][-3:]:
        mod_type = entry.get("modification_type", "unknown")
        concept_snippet = entry.get("concept", "")
        concept_summary = (concept_snippet[:100] + "...") if len(concept_snippet) > 100 else concept_snippet
        history_summary += f"- {mod_type}: {concept_summary}\n"
    prompt = f"""
Create a breakthrough artistic concept that represents significant creative evolution:

Original concept: {original_concept}
Current concept: {current_concept}

Your artistic journey so far:
{history_summary}

Create a breakthrough by:
1. Identifying the deeper meaning or purpose driving your artistic exploration
2. Making a bold conceptual leap that still connects to your creative journey
3. Introducing innovative approaches that push your artistic boundaries
4. Reimagining your artistic voice while maintaining authenticity

This should feel like a significant moment of creative growth and discovery, similar to Picasso's transition to Cubism or Kandinsky's move to abstraction.
    """
    return _process_modification(state, prompt, temperature=0.8)


# ===============================
# IMAGE CREATION & STATE UPDATE
# ===============================
def create_image(state: ModificationState) -> ModificationState:
    """Generate an image based on the refined concept and update state memory."""
    concept = state["refined_concept"]
    image_generator = ImageGenerator()
    image_url = image_generator.generate_image(concept)
    state["current_image_url"] = image_url
    state["messages"].append(AIMessage(content=f"Generated image: {image_url}"))
    return update_memory(state)


def update_memory(state: ModificationState) -> ModificationState:
    """Record the latest artwork and modification details."""
    memory_entry = {
        "iteration": state["iteration"],
        "modification_type": state["modification_type"],
        "concept": state["refined_concept"],
        "image_url": state["current_image_url"],
        "feedback": state.get("feedback", ""),
        "image_analysis": state.get("image_analysis", ""),
        "timestamp": datetime.now().isoformat()
    }
    if state["current_image_url"] not in state["previous_images"]:
        state["previous_images"].append(state["current_image_url"])
    state["modification_history"].append(memory_entry)
    state["iteration"] += 1
    return state


def analyze_current_state(state: ModificationState) -> ModificationState:
    """Analyze the current image unless it's the initial iteration."""
    if state["iteration"] == 0:
        state["messages"].append(AIMessage(content="Initial concept created, proceeding to modification."))
        return state
    analysis = analyze_image(state["current_image_url"])
    state["image_analysis"] = analysis
    state["messages"].append(AIMessage(content=f"Image analysis: {analysis}"))
    return state


def select_modification_type(state: ModificationState):
    """
    If a strategy is provided, use it; otherwise, select one based on image analysis and history.
    """
    if state["modification_type"]:
        return state["modification_type"]
    if state["iteration"] == 0:
        return "no_modification"

    client = get_llm()
    analysis = state.get("image_analysis", "")
    history_summary = "".join(
        f"- Iteration {entry.get('iteration', 0)}: {entry.get('modification_type', 'unknown')}\n"
        for entry in state["modification_history"]
    )
    feedback_text = f"\nUser feedback: {state.get('feedback', '')}" if state.get("feedback", "") else ""
    prompt = f"""
Based on the current image analysis and modification history, select the most appropriate artistic process modification strategy from the options below:

1. No modification (reproduction of previous work)
2. Unsystematic change (random modifications)
3. Changing subjects and methods based on prior ideas
4. Quantitative modification (changing size, material, etc.)
5. Subject modification (applying the same method to new subjects)
6. Subject modification with minor methodological refinements
7. Structure modification (developing new methodology aligned with concept)
8. Concept modification (forming new art concepts guided by creative vision)

Current image analysis: {analysis}

Modification history:
{history_summary}{feedback_text}

Return only the number of the strategy to apply next.
    """
    output = client.run(
        "ibm-granite/granite-3.1-8b-instruct",
        input={"prompt": prompt, "max_new_tokens": 10, "temperature": 0.2}
    )
    strategy_map = {
        "1": "no_modification",
        "2": "unsystematic_change",
        "3": "idea_based_change",
        "4": "quantitative_modification",
        "5": "subject_modification",
        "6": "subject_with_method_refinement",
        "7": "structure_modification",
        "8": "concept_modification"
    }
    strategy_number = ''.join(filter(str.isdigit, str(output)[:3]))
    strategy = strategy_map.get(strategy_number, "subject_modification")
    state["modification_type"] = strategy
    state["messages"].append(AIMessage(content=f"Selected modification strategy: {strategy}"))
    return strategy


def check_completion(state: ModificationState):
    """Determine if the modification process should continue or end."""
    return "complete"


# ===============================
# GRAPH DEFINITION & EXECUTION
# ===============================
def create_modification_graph():
    workflow = StateGraph(ModificationState)
    
    # Nodes for analysis and modification strategies
    workflow.add_node("analyze_current_state", analyze_current_state)
    workflow.add_node("no_modification", no_modification)
    workflow.add_node("unsystematic_change", unsystematic_change)
    workflow.add_node("idea_based_change", idea_based_change)
    workflow.add_node("quantitative_modification", quantitative_modification)
    workflow.add_node("subject_modification", subject_modification)
    workflow.add_node("subject_with_method_refinement", subject_with_method_refinement)
    workflow.add_node("structure_modification", structure_modification)
    workflow.add_node("concept_modification", concept_modification)
    workflow.add_node("create_image", create_image)
    
    # Conditional routing based on analysis
    workflow.add_conditional_edges("analyze_current_state", select_modification_type, {
        "no_modification": "no_modification",
        "unsystematic_change": "unsystematic_change",
        "idea_based_change": "idea_based_change",
        "quantitative_modification": "quantitative_modification",
        "subject_modification": "subject_modification",
        "subject_with_method_refinement": "subject_with_method_refinement",
        "structure_modification": "structure_modification",
        "concept_modification": "concept_modification"
    })
    
    # All modification strategies lead to image creation
    for node in [
        "no_modification", "unsystematic_change", "idea_based_change", 
        "quantitative_modification", "subject_modification", 
        "subject_with_method_refinement", "structure_modification", 
        "concept_modification"
    ]:
        workflow.add_edge(node, "create_image")
    
    # End the process after image creation
    workflow.add_conditional_edges("create_image", check_completion, {
        "continue": "analyze_current_state",
        "complete": END
    })
    
    workflow.set_entry_point("analyze_current_state")
    return workflow.compile()


def generate_artwork_with_modification(
    original_concept: str,
    current_concept: str,
    current_image_url: str,
    modification_type: Optional[str] = None,
    iteration: int = 0,
    feedback: str = "",
    modification_history: List[Dict[str, Any]] = None
):
    """
    Initialize state and run the modification graph to generate a new artwork.
    """
    state: ModificationState = {
        "messages": [],
        "original_concept": original_concept,
        "refined_concept": current_concept,
        "current_image_url": current_image_url,
        "previous_images": [current_image_url] if current_image_url else [],
        "modification_type": modification_type,
        "iteration": iteration,
        "modification_history": modification_history or [],
        "feedback": feedback,
        "image_analysis": None
    }
    
    graph = create_modification_graph()
    result = graph.invoke(state)
    return result
