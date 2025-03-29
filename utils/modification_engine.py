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
    """Strategy 1: Reproduce previous work without changes."""
    state["messages"].append(AIMessage(content="Applying no modification strategy - reproducing previous work."))
    return state


def unsystematic_change(state: ModificationState) -> ModificationState:
    """Strategy 2: Introduce random, unpredictable modifications."""
    current_concept = state["refined_concept"]
    prompt = f"""
Take this artistic concept and introduce random, unpredictable modifications:

Original concept: {current_concept}

Introduce elements of chance, randomness, or unexpected juxtapositions. The changes should be unsystematic rather than following a clear pattern.
    """
    return _process_modification(state, prompt, temperature=0.9)


def idea_based_change(state: ModificationState) -> ModificationState:
    """Strategy 3: Evolve the concept by building on previous ideas."""
    current_concept = state["refined_concept"]
    # Use the last three iterations from history for context
    previous_ideas = [entry.get("concept", "") for entry in state["modification_history"] if "concept" in entry]
    previous_ideas_text = "\n".join(previous_ideas[-3:])
    prompt = f"""
Develop a new artistic concept based on ideas from previous iterations:

Current concept: {current_concept}

Previous concepts and ideas:
{previous_ideas_text}

Create a new concept that:
1. Builds upon elements or themes from previous iterations
2. Combines or transforms these elements in new ways
3. Develops the artistic direction based on the trajectory of previous works
4. Creates meaningful connections to the artistic journey so far
    """
    return _process_modification(state, prompt, temperature=0.7)


def quantitative_modification(state: ModificationState) -> ModificationState:
    """Strategy 4: Modify quantitative aspects (size, scale, materials)."""
    current_concept = state["refined_concept"]
    prompt = f"""
Modify this artistic concept by changing quantitative aspects such as size, scale, proportions, or materials:

Current concept: {current_concept}

Make quantitative modifications such as:
1. Changing the scale or size of elements
2. Altering the number or density of components
3. Shifting proportions or ratios between elements
4. Modifying material properties (texture, weight, transparency)
5. Adjusting color intensity, saturation, or contrast

Keep the core artistic approach and subject matter the same while transforming these quantitative aspects.
    """
    return _process_modification(state, prompt, temperature=0.6)


def subject_modification(state: ModificationState) -> ModificationState:
    """Strategy 5: Change the subject while preserving the artistic approach."""
    current_concept = state["refined_concept"]
    prompt = f"""
Transform this artistic concept by changing the subject while maintaining the same artistic approach:

Current concept: {current_concept}

Steps:
1. Identify the current subject and artistic technique/style
2. Replace the subject with a new one that creates interesting tensions or relationships
3. Apply the same artistic treatment to this new subject
4. Ensure the new concept maintains the same level of detail and technical approach

Provide a detailed revised concept that changes only the subject matter while preserving the artistic methodology.
    """
    return _process_modification(state, prompt, temperature=0.7)


def subject_with_method_refinement(state: ModificationState) -> ModificationState:
    """Strategy 6: Change the subject and apply minor methodological refinements."""
    current_concept = state["refined_concept"]
    prompt = f"""
Transform this artistic concept by changing the subject and making minor refinements to the methodology:

Current concept: {current_concept}

Steps:
1. Identify the current subject and artistic technique/style
2. Replace the subject with a new one that creates interesting tensions or relationships
3. Apply the same general artistic approach but with subtle refinements that enhance the treatment of the new subject
4. Consider how small methodological adjustments can better serve the new subject matter

Provide a detailed revised concept that changes both the subject matter and makes minor refinements to the artistic methodology.
    """
    return _process_modification(state, prompt, temperature=0.7)


def structure_modification(state: ModificationState) -> ModificationState:
    """Strategy 7: Develop a new methodology aligned with the core concept."""
    current_concept = state["refined_concept"]
    original_concept = state["original_concept"]
    prompt = f"""
Take this artistic concept and develop a new methodological structure while maintaining the core concept:

Original concept: {original_concept}
Current concept: {current_concept}

Reimagine the artistic approach by:
1. Identifying the core thematic elements
2. Developing a new visual language or compositional structure
3. Maintaining conceptual integrity while transforming the execution
4. Creating a cohesive new methodology that aligns with the original artistic intent
    """
    return _process_modification(state, prompt, temperature=0.7)


def concept_modification(state: ModificationState) -> ModificationState:
    """Strategy 8: Form a new art concept that marks significant evolution."""
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
Create a new artistic concept that represents a significant evolution from the current direction:

Original concept: {original_concept}
Current concept: {current_concept}

Artistic journey so far:
{history_summary}

Develop a new concept that:
1. Represents a meaningful conceptual advancement
2. Builds upon insights gained from previous iterations
3. Introduces a new creative vision or thematic direction
4. Maintains a connection to the original artistic intent
5. Suggests innovative technical approaches suitable for the new concept

Create a detailed concept that demonstrates artistic growth and conceptual evolution.
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
