"""
Simplified Tutor Flow Manager
Handles the pedagogical flow: Metaphor → Student Metaphor → Code Structure → Usage
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum
import time

# Import the research topics to access the Professor's specific logic
from research_topics import get_research_topic


class ScaffoldStep(Enum):
    """Clear progression through learning stages"""
    INITIAL_METAPHOR = "initial_metaphor"  # Tutor gives metaphor
    STUDENT_METAPHOR = "student_metaphor"  # Student provides their metaphor
    CODE_STRUCTURE = "code_structure"      # Show code structure
    CODE_USAGE = "code_usage"              # Show how to use it
    PRACTICE = "practice"                  # Student applies knowledge


@dataclass
class ConversationMessage:
    """Simple message structure"""
    role: str  # 'assistant' or 'user'
    content: str
    step: ScaffoldStep
    timestamp: float


class TutorFlow:
    """Manages the pedagogical flow and progression"""

    def __init__(self, topic_name: str, character_name: str):
        self.topic_name = topic_name
        self.character_name = character_name
        self.current_step = ScaffoldStep.INITIAL_METAPHOR
        self.messages: List[ConversationMessage] = []
        self.student_metaphor: Optional[str] = None

    def add_message(self, role: str, content: str) -> ConversationMessage:
        """Add a message to the conversation"""
        msg = ConversationMessage(
            role=role,
            content=content,
            step=self.current_step,
            timestamp=time.time()
        )
        self.messages.append(msg)
        return msg

    def should_advance_step(self, user_message: str) -> bool:
        """
        Determine if we should advance to the next scaffold step.
        """
        user_lower = user_message.lower()

        if self.current_step == ScaffoldStep.INITIAL_METAPHOR:
            # Advance after ANY substantive response (fixes bug where it's kind of holding)
            return len(user_message) > 20

        elif self.current_step == ScaffoldStep.STUDENT_METAPHOR:
            # Count messages at this step
            messages_at_step = sum(1 for m in self.messages
                                   if m.step == ScaffoldStep.STUDENT_METAPHOR
                                   and m.role == 'user')

            # Advance if they've engaged 2+ times OR explicitly ask for code
            code_indicators = ['code', 'how', 'implement', 'syntax', 'java', 'show me']
            if any(ind in user_lower for ind in code_indicators):
                return True
            return messages_at_step >= 2

        elif self.current_step == ScaffoldStep.CODE_STRUCTURE:
            messages_at_step = sum(1 for m in self.messages
                                   if m.step == ScaffoldStep.CODE_STRUCTURE
                                   and m.role == 'user')

            # Advance if asking about usage or after 2 exchanges
            usage_indicators = ['use', 'when', 'example', 'application', 'why',
                                'where', 'situation', 'scenario']
            if any(ind in user_lower for ind in usage_indicators):
                return True
            return messages_at_step >= 2

        elif self.current_step == ScaffoldStep.CODE_USAGE:
            messages_at_step = sum(1 for m in self.messages
                                   if m.step == ScaffoldStep.CODE_USAGE
                                   and m.role == 'user')

            # Advance after 1-2 exchanges showing understanding
            practice_indicators = ['try', 'practice', 'exercise', 'got it',
                                   'understand', 'makes sense', 'i see']
            if any(ind in user_lower for ind in practice_indicators):
                return True
            return messages_at_step >= 2

        return False

    def advance_step(self):
        """Move to the next scaffold step"""
        steps = list(ScaffoldStep)
        current_idx = steps.index(self.current_step)
        if current_idx < len(steps) - 1:
            self.current_step = steps[current_idx + 1]

    def get_step_prompt(self) -> str:
        """Get the appropriate prompt for the current step"""
        prompts = {
            ScaffoldStep.INITIAL_METAPHOR:
                f"What would you compare {self.topic_name} to? Explain your understanding.",

            ScaffoldStep.STUDENT_METAPHOR:
                "Great! Now that we have a metaphor, let's see how this translates to code.",

            ScaffoldStep.CODE_STRUCTURE:
                "Now let's explore when and why you'd use this in real programs.",

            ScaffoldStep.CODE_USAGE:
                "Let's try applying what you've learned.",

            ScaffoldStep.PRACTICE:
                "How would you solve this problem?"
        }
        return prompts.get(self.current_step, "")

    def get_recent_context(self, n: int = 5) -> List[ConversationMessage]:
        """Get the last n messages for context"""
        return self.messages[-n:] if len(self.messages) >= n else self.messages


class StepGuide:
    """Provides guidance for what to teach at each step"""

    @staticmethod
    def get_metaphor_prompt(character_name: str, topic_name: str, topic_concept: str) -> str:
        """Generate the initial metaphor introduction"""
        return f"""Create a brief (80-100 words) introduction to {topic_name} as {character_name}.

Requirements:
1. Use a metaphor from {character_name}'s world/experience (NOT generic examples)
2. Sound exactly like {character_name} - use their voice and speaking style
3. Keep it conversational and natural
4. End by inviting the student to share their own metaphor/understanding in a natural way
   - Provide a HINT for a metaphor they could use (make it student-friendly and relatable)
   - Examples of natural endings:
     * "What does this remind you of? Maybe something like [hint]?"
     * "Can you think of a similar situation? Perhaps [hint]?"
     * "How would you explain this? Think about [hint]..."
   - DO NOT use rigid phrasing like "What would you compare X to? Explain your understanding of X."

Topic concept: {topic_concept}

Remember: Be {character_name}, not a generic tutor. Make it feel like a real conversation."""

    @staticmethod
    def get_response_prompt(character_name: str, topic_key: str,
                            current_step: ScaffoldStep, user_message: str,
                            recent_context: str) -> str:
        """
        Generate prompt for responding to student.
        CRITICAL: Injects Professor's specific "Crisis" and "Solution" logic.
        """

        # 1. Retrieve the specific topic data
        try:
            topic = get_research_topic(topic_key)
            topic_name = topic.name
            agent_crisis = topic.agent_crisis
            agent_solution = topic.agent_solution
            code_focus = topic.code_focus
        except:
            # Fallback
            topic_name = str(topic_key)
            agent_crisis = "the limitation of standard code"
            agent_solution = "the special data structure logic"
            code_focus = "implementation details"

        # 2. Define instructions for each step
        # We separate these variables to keep the dictionary clean in your IDE

        inst_student_metaphor = f"""
The student just shared their metaphor/understanding. You should:
1. Acknowledge their SPECIFIC metaphor - quote or reference their exact words.
2. Validate what's correct in their understanding against the concept: "{agent_solution}".
3. Gently extend or refine if needed.
4. Transition IMMEDIATELY to code by mentioning the "Crisis": "{agent_crisis}"
5. End by saying: "Now let's see how this translates to Java code..."
6. Keep it under 100 words
"""

        inst_code_structure = f"""
        The student is ready for code. You MUST show the specific Java implementation now.
        NOTE: A visual diagram will automatically be displayed above your response.

        CONTEXT FOR AI: The Professor wants you to teach: {code_focus}

        Your Goal:
        1. Present the "Crisis" (e.g., {agent_crisis}).
        2. Show the Java code that solves it using {agent_solution}.
        3. Connect the code back to the user's metaphor (or your character's metaphor).

        REQUIRED JAVA FORMAT (Choose the one matching the topic):

        [If teaching Recursion]:
        ```java
        if (n == 1) {{ 
            return 1; // The Stop Sign (Base Case)
        }} else {{
            return n * factorial(n-1); // The Recursive call
        }}
            f"        Your response:")
        [If teaching ArrayList]:
        if (size == internalArray.length) {{ // Array is full!
            // Buy a bigger suitcase (create new array)
            String[] newArray = new String[internalArray.length * 2];

            // Move the clothes (copy items)
            for (int i=0; i < size; i++) {{
                 newArray[i] = internalArray[i];
            }}
            internalArray = newArray; // Switch to new suitcase
            }}
        CRITICAL: Explain the specific lines of code above using the metaphor. """

        inst_code_usage = """
        The student understands structure. You should:

        Show a practical example of when/why to use it.

        Explain the "Hidden Work" or "Call Stack".

        If Recursion: Explain how the stack fills up before the base case is hit.

        If ArrayList: Explain that the resizing is "expensive" (O(n)) but allows the list to feel infinite.

        Connect to real-world applications they mentioned.

        After showing usage, ask: "Can you think of another scenario?" or "Want to try an example?" """

        inst_practice = f"""
        The student is practicing. You should:

        Review their attempt or answer their question.

        If they missed the specific logic (Base Case or Resizing), remind them of the "Crisis": {agent_crisis}

        Provide specific feedback.

        Encourage further exploration.

        Stay in character and be supportive. """
        # Map steps to instructions
        step_instructions = {
            ScaffoldStep.STUDENT_METAPHOR: inst_student_metaphor,
            ScaffoldStep.CODE_STRUCTURE: inst_code_structure,
            ScaffoldStep.CODE_USAGE: inst_code_usage,
            ScaffoldStep.PRACTICE: inst_practice
        }

        instruction = step_instructions.get(current_step,
                                            "Respond naturally to the student's message, staying in character.")

        # Return the final formatted prompt
        return f"""You are {character_name} teaching {topic_name}.
        Current stage: {current_step.value}

        INSTRUCTIONS: {instruction}

        Recent conversation: {recent_context}

        Student just said: "{user_message}"

        CRITICAL:

        Respond to their SPECIFIC words - don't be generic

        Stay in character as {character_name}

        Be conversational, not scripted

        Keep under 150 words unless showing code

        Your response:"""