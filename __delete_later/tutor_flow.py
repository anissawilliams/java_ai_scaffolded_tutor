"""
Simplified Tutor Flow Manager
Handles the pedagogical flow with strict hand-holding.
"""

from dataclasses import dataclass
from typing import List
from enum import Enum
from content.research_topics import get_research_topic


class ScaffoldStep(Enum):
    INITIAL_METAPHOR = "initial_metaphor"
    STUDENT_METAPHOR = "student_metaphor"
    CODE_STRUCTURE = "code_structure"      # Focus: The Crisis & Manual Code
    CODE_USAGE = "code_usage"              # Focus: The Hidden Work / Cost
    PRACTICE = "practice"


@dataclass
class ConversationMessage:
    role: str
    content: str
    step: ScaffoldStep
    timestamp: float


class TutorFlow:
    def __init__(self, topic_name: str, character_name: str):
        self.topic_name = topic_name
        self.character_name = character_name
        self.current_step = ScaffoldStep.INITIAL_METAPHOR
        self.messages: List[ConversationMessage] = []

    def should_advance_step(self, user_message: str) -> bool:
        user_lower = user_message.lower()

        if self.current_step == ScaffoldStep.INITIAL_METAPHOR:
            return len(user_message) > 15

        elif self.current_step == ScaffoldStep.STUDENT_METAPHOR:
            ready_terms = ['ready', 'go', 'show me', 'yes', 'ok', 'understand', 'yep']
            return any(term in user_lower for term in ready_terms)

        elif self.current_step == ScaffoldStep.CODE_STRUCTURE:
            ack_terms = ['makes sense', 'i see', 'copy', 'expensive', 'heavy', 'got it']
            return any(term in user_lower for term in ack_terms)

        elif self.current_step == ScaffoldStep.CODE_USAGE:
            return len(user_message) > 10

        return False

    def advance_step(self):
        steps = list(ScaffoldStep)
        current_idx = steps.index(self.current_step)
        if current_idx < len(steps) - 1:
            self.current_step = steps[current_idx + 1]

    def get_recent_context(self, n: int = 5) -> List[ConversationMessage]:
        return self.messages[-n:] if len(self.messages) >= n else self.messages


class StepGuide:
    @staticmethod
    def get_response_prompt(
        character_name: str,
        topic_key: str,
        current_step: ScaffoldStep,
        user_message: str,
        recent_context: str
    ) -> str:

        topic = get_research_topic(topic_key)

        # Hand-Holding Instructions
        inst_student_metaphor = f"""
1. Briefly acknowledge their metaphor.
2. Immediately pivot to the "Conflict": Java arrays are rigid and fixed-size.
3. Pose the Crisis: "{topic.agent_crisis}"
4. Ask: "Are you ready to see the Java code that handles this 'Crisis'?"
5. Do not answer off-topic questions.
"""

        inst_code_structure = f"""
1. Present the MANUAL implementation code (not ArrayList).
2. Explain the "Hidden Work": {topic.code_focus}.
3. REQUIRED JAVA:
```java
if (size == elements.length) {{ // Array is full! Crisis!
    Object[] newArray = new Object[elements.length * 2]; // Bigger suitcase
    System.arraycopy(elements, 0, newArray, 0, elements.length); // Heavy Lift
    elements = newArray; // Reassign reference
}}
