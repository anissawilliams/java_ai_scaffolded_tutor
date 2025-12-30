"""
Research Topics
ArrayList and Recursion content for the study
Updated with Professor's "Stop Sign" and "Suitcase" methodologies
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ResearchTopic:
    """Represents a topic in the research study"""
    key: str
    name: str
    difficulty: str
    concept: str
    key_points: List[str]
    metaphor_prompt: str
    # New fields for Professor's Logic
    agent_crisis: str  # The problem/conflict (e.g., infinite loop, full array)
    agent_solution: str # The specific logic to teach (Base Case, New Array)
    code_focus: str    # The specific code pattern to show

# -------------------------------------------------------------------------
# TOPIC 1: ARRAYLIST (The Suitcase / Dynamic Resizing)
# -------------------------------------------------------------------------
ARRAYLIST_TOPIC = ResearchTopic(
    key='arraylist',
    name='Dynamic ArrayList',
    difficulty='easy',
    concept="""An abstraction that allows an array to feel "infinite" by secretly replacing 
a full underlying array with a larger one. While it grows automatically, it performs a 
heavy O(n) operation behind the scenes during a resize.""",
    key_points=[
        'Java arrays have fixed size; ArrayList feels infinite',
        'When full, it creates a new, larger array (Hidden Work)',
        'It copies all old items to the new array',
        'Then it points the reference variable to the new array',
        'The "Crisis": What happens when the suitcase is full?'
    ],
    metaphor_prompt="""Think about an ArrayList like a suitcase. If your suitcase is full, 
but you bought more clothes, what do you do? You have to buy a bigger suitcase and 
move ALL your clothes over to the new one before you can add the new items.""",

    agent_crisis="Java arrays are fixed size. If our array has 4 slots and they are all full, and we try to add a 5th element, the program crashes. How do we fix this?",
    agent_solution="We need to create a new, larger array, copy everything over, and then switch to using that new array.",
    code_focus="The resizing logic: checking if full, creating newArray, copying items, and reassigning internalArray."
)

# -------------------------------------------------------------------------
# TOPIC 2: RECURSION (The Stop Sign / Base Case)
# -------------------------------------------------------------------------
RECURSION_TOPIC = ResearchTopic(
    key='recursion',
    name='Recursion',
    difficulty='hard',
    concept="""A method that solves a problem by calling a smaller version of itself. 
The critical component is the Base Case (The Stop Sign) which prevents infinite recursion 
and Stack Overflow.""",
    key_points=[
        'Recursive Case: Doing work and calling itself again',
        'Base Case: The "Stop Sign" or exit strategy',
        'Without a base case, the Call Stack fills up until crash',
        'Always handle the Base Case (simplest version) first'
    ],
    metaphor_prompt="""Think about Recursion like a road with a Stop Sign. You keep driving 
(calling the function) until you hit the Stop Sign (Base Case). If the Stop Sign is missing, 
you keep driving forever until you run out of gas (Stack Overflow).""",

    agent_crisis="If I call a function that calls itself, which calls itself... when does it actually return a value? It's an infinite loop without a 'Stop Sign'.",
    agent_solution="We need a Base Case. What is the simplest version of the problem (like 1!) that needs no calculation?",
    code_focus="The IF statement (Base Case) at the start of the method, followed by the recursive call."
)

RESEARCH_TOPICS = {
    'arraylist': ARRAYLIST_TOPIC,
    'recursion': RECURSION_TOPIC
}

def get_research_topic(topic_key: str) -> ResearchTopic:
    if topic_key not in RESEARCH_TOPICS:
        raise ValueError(f"Topic '{topic_key}' not found")
    return RESEARCH_TOPICS[topic_key]