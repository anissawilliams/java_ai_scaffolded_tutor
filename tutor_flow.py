"""
Simplified Tutor Flow Manager
Handles the pedagogical flow: Metaphor → Student Metaphor → Code Structure → Usage
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum


class ScaffoldStep(Enum):
    """Clear progression through learning stages"""
    INITIAL_METAPHOR = "initial_metaphor"  # Tutor gives metaphor
    STUDENT_METAPHOR = "student_metaphor"  # Student provides their metaphor
    CODE_STRUCTURE = "code_structure"      # Show code structure
    CODE_USAGE = "code_usage"              # Show how to use it
    PRACTICE = "practice"                   # Student applies knowledge
    

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
        import time
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
        This is based on the user's response content.
        
        Now more lenient - advances when student shows understanding,
        not just when they use magic keywords.
        """
        user_lower = user_message.lower()
        
        if self.current_step == ScaffoldStep.INITIAL_METAPHOR:
            # They've responded with their own metaphor/understanding
            # Advance after ANY substantive response
            return len(user_message) > 20
            
        elif self.current_step == ScaffoldStep.STUDENT_METAPHOR:
            # Advance after 1-2 exchanges at this step
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
            # They understand structure - advance after understanding shown
            messages_at_step = sum(1 for m in self.messages 
                                  if m.step == ScaffoldStep.CODE_STRUCTURE 
                                  and m.role == 'user')
            
            # Advance if asking about usage/when/why OR after 2 exchanges
            usage_indicators = ['use', 'when', 'example', 'application', 'why', 
                              'where', 'situation', 'scenario']
            if any(ind in user_lower for ind in usage_indicators):
                return True
            return messages_at_step >= 2
            
        elif self.current_step == ScaffoldStep.CODE_USAGE:
            # Move to practice after they engage with usage
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
    def get_response_prompt(character_name: str, topic_name: str, 
                           current_step: ScaffoldStep, user_message: str, 
                           recent_context: str) -> str:
        """Generate prompt for responding to student"""
        
        step_instructions = {
            ScaffoldStep.STUDENT_METAPHOR: """
The student just shared their metaphor/understanding. You should:
1. Acknowledge their SPECIFIC metaphor - quote or reference their exact words
2. Validate what's correct in their understanding
3. Gently extend or refine if needed
4. After 1-2 exchanges, naturally transition: "Now let's see how this translates to Java code..."
5. Keep it under 100 words""",
            
            ScaffoldStep.CODE_STRUCTURE: """
The student is ready for code. You MUST show them actual Java code now.
NOTE: A visual diagram will automatically be displayed above your response to help them understand.

CRITICAL: Include actual code in your response! Don't just describe it.

Format your response like this:

"Perfect! Let's see how that [metaphor they mentioned] translates to Java code.

```java
Queue<String> queue = new LinkedList<>();
queue.add("first");     // enqueue - add to back
queue.add("second");    
String item = queue.remove();  // dequeue - remove from front
// item is "first" (FIFO - First In, First Out)
```

See how just like [reference their metaphor], the first element we added ('first') is the first one removed? The diagram above shows this visually.

[Ask if they understand or have questions about the code]"

You should:
1. Reference the visual diagram that appears above your message
2. Show actual Java code (5-10 lines with comments)
3. Connect code back to their metaphor
4. Keep explanations simple and clear
5. Ask if they have questions

Keep response under 200 words (code included).""",
            
            ScaffoldStep.CODE_USAGE: """
The student understands structure. You should:
1. Show a practical example of when/why to use it
2. Provide a simple code example in context
3. Connect to real-world applications they mentioned
4. After showing usage, ask: "Can you think of another scenario?" or "Want to try an example?"
5. Be ready to move to practice""",
            
            ScaffoldStep.PRACTICE: """
The student is practicing. You should:
1. Review their attempt or answer their question
2. Provide specific feedback
3. Encourage further exploration
4. Stay in character and be supportive"""
        }
        
        instruction = step_instructions.get(current_step, 
            "Respond naturally to the student's message, staying in character.")
        
        return f"""You are {character_name} teaching {topic_name}.

Current stage: {current_step.value}

{instruction}

Recent conversation:
{recent_context}

Student just said: "{user_message}"

CRITICAL: 
- Respond to their SPECIFIC words - don't be generic
- Stay in character as {character_name}
- Be conversational, not scripted
- Keep under 150 words unless showing code

Your response:"""
