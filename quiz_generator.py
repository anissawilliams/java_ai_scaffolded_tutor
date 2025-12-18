"""
Quiz Generator for Java Topics
Generates understanding-check quizzes based on topics
"""

from typing import List, Dict
from topics import Topic, get_topic
from ai_client import SimpleAIClient


class QuizQuestion:
    """Represents a single quiz question"""
    def __init__(self, question: str, options: List[str], correct_index: int, explanation: str = ""):
        self.question = question
        self.options = options
        self.correct_index = correct_index
        self.explanation = explanation
    
    @property
    def correct_answer(self) -> str:
        return self.options[self.correct_index]


def generate_quiz(topic_key: str, ai_client: SimpleAIClient, num_questions: int = 4) -> List[QuizQuestion]:
    """
    Generate a quiz for a topic using AI.
    
    Args:
        topic_key: The topic key (e.g., 'queue', 'stack')
        ai_client: The AI client to use for generation
        num_questions: Number of questions to generate (default 4)
    
    Returns:
        List of QuizQuestion objects
    """
    topic = get_topic(topic_key)
    
    prompt = f"""Generate {num_questions} multiple choice questions to test understanding of {topic.name}.

Topic concept: {topic.concept}

Key points to cover:
{chr(10).join('- ' + point for point in topic.key_points)}

Requirements for each question:
1. Test conceptual understanding (not just memorization)
2. Have 4 answer options (A, B, C, D)
3. Only ONE correct answer
4. Include a brief explanation of why the answer is correct
5. Mix difficulty levels (some easier, some harder)

Format your response EXACTLY like this (this is critical):

QUESTION 1
What is the key characteristic of a {topic.name}?
A) First option
B) Second option  
C) Third option
D) Fourth option
CORRECT: B
EXPLANATION: Brief explanation of why B is correct.

QUESTION 2
[next question...]

Generate all {num_questions} questions now."""

    try:
        response = ai_client.generate_response(
            system_prompt=f"You are a CS professor creating quiz questions about {topic.name}.",
            user_message=prompt,
            temperature=0.7
        )
        
        # Parse the response
        questions = parse_quiz_response(response)
        
        # Debug logging
        print(f"[QUIZ DEBUG] AI generated {len(questions)} questions for {topic_key}")
        for idx, q in enumerate(questions):
            print(f"[QUIZ DEBUG] Q{idx+1}: '{q.question[:60]}...' ({len(q.options)} options)")
        
        # Validate questions quality
        valid_questions = [q for q in questions if len(q.question) >= 10 and len(q.options) == 4]
        
        if len(valid_questions) < num_questions:
            print(f"[QUIZ DEBUG] Only {len(valid_questions)} valid questions, using fallback")
            # Use fallback questions
            return get_fallback_quiz(topic_key)[:num_questions]
        
        return valid_questions[:num_questions]
        
    except Exception as e:
        print(f"[QUIZ DEBUG] Error generating quiz: {e}")
        import traceback
        traceback.print_exc()
        # Return fallback questions
        return get_fallback_quiz(topic_key)[:num_questions]


def parse_quiz_response(response: str) -> List[QuizQuestion]:
    """Parse AI response into QuizQuestion objects"""
    questions = []
    
    # Split by QUESTION markers
    parts = response.split('QUESTION ')
    
    for part in parts[1:]:  # Skip first empty part
        try:
            lines = [line.strip() for line in part.strip().split('\n') if line.strip()]
            
            if not lines:
                continue
            
            # Find question text (skip the number if present)
            question_text = ""
            options = []
            correct = None
            explanation = ""
            
            i = 0
            # First non-empty line after number should be the question
            # Skip lines that are just numbers
            while i < len(lines) and (lines[i].isdigit() or not lines[i]):
                i += 1
            
            if i < len(lines):
                question_text = lines[i]
                i += 1
            
            # Parse options - look for A), B), C), D) format
            while i < len(lines):
                line = lines[i]
                if line.startswith(('A)', 'B)', 'C)', 'D)', 'a)', 'b)', 'c)', 'd)')):
                    # Extract option text after the letter
                    option_text = line[2:].strip() if len(line) > 2 else line[3:].strip()
                    options.append(option_text)
                    i += 1
                elif line.upper().startswith('CORRECT'):
                    # Parse correct answer
                    try:
                        correct_letter = line.split(':')[1].strip()[0].upper()
                        correct = ord(correct_letter) - ord('A')
                    except:
                        pass
                    i += 1
                    break
                else:
                    i += 1
            
            # Get explanation
            while i < len(lines):
                line = lines[i]
                if line.upper().startswith('EXPLANATION'):
                    explanation = line.split(':', 1)[1].strip() if ':' in line else ""
                    i += 1
                    # Continue to get full explanation if it spans multiple lines
                    while i < len(lines) and not lines[i].upper().startswith(('QUESTION', 'CORRECT')):
                        explanation += " " + lines[i]
                        i += 1
                    break
                i += 1
            
            if question_text and len(options) >= 4 and correct is not None:
                questions.append(QuizQuestion(
                    question=question_text,
                    options=options[:4],
                    correct_index=correct,
                    explanation=explanation
                ))
        except Exception as e:
            print(f"Error parsing question: {e}")
            continue
    
    return questions


def get_fallback_quiz(topic_key: str) -> List[QuizQuestion]:
    """Get hardcoded fallback quiz questions for each topic"""
    
    fallback_quizzes = {
        'queue': [
            QuizQuestion(
                "What is the key ordering principle of a Queue?",
                ["Last In, First Out (LIFO)", "First In, First Out (FIFO)", "Random Access", "Priority-based"],
                1,
                "Queues follow FIFO - the first element added is the first one removed."
            ),
            QuizQuestion(
                "Which operation adds an element to a Queue?",
                ["push()", "enqueue()", "insert()", "append()"],
                1,
                "enqueue() is the standard operation to add elements to a queue."
            ),
            QuizQuestion(
                "When would you use a Queue?",
                ["Undo functionality", "Processing tasks in order", "Backtracking in a maze", "Managing nested function calls"],
                1,
                "Queues are ideal when you need to process items in the order they arrive."
            ),
            QuizQuestion(
                "What happens when you dequeue from an empty Queue?",
                ["Returns null/throws exception", "Returns the last element", "Queue automatically fills", "Nothing happens"],
                0,
                "Attempting to dequeue from an empty queue typically results in an error or null return."
            )
        ],
        'stack': [
            QuizQuestion(
                "What is the key ordering principle of a Stack?",
                ["First In, First Out (FIFO)", "Last In, First Out (LIFO)", "Random Access", "Sorted Order"],
                1,
                "Stacks follow LIFO - the last element added is the first one removed."
            ),
            QuizQuestion(
                "Which operation adds an element to a Stack?",
                ["enqueue()", "push()", "add()", "insert()"],
                1,
                "push() is the standard operation to add elements to a stack."
            ),
            QuizQuestion(
                "Which real-world scenario best represents a Stack?",
                ["People in a line", "Undo button in a text editor", "Print queue", "Playlist shuffle"],
                1,
                "Undo operations work like a stack - you undo the most recent action first."
            ),
            QuizQuestion(
                "What does peek() do on a Stack?",
                ["Removes the top element", "Views top element without removing", "Adds an element", "Empties the stack"],
                1,
                "peek() allows you to view the top element without removing it from the stack."
            )
        ],
        'linked-list': [
            QuizQuestion(
                "What makes a Linked List different from an array?",
                ["Elements are sorted", "Elements are stored contiguously", "Elements are connected by references", "Elements must be same type"],
                2,
                "Linked lists use pointers/references to connect nodes, unlike arrays which store elements contiguously."
            ),
            QuizQuestion(
                "What does each node in a Linked List contain?",
                ["Only data", "Data and reference to next node", "Only references", "Index and data"],
                1,
                "Each node stores data and a reference (pointer) to the next node in the list."
            ),
            QuizQuestion(
                "What is an advantage of Linked Lists over arrays?",
                ["Faster random access", "Less memory usage", "Efficient insertion/deletion", "Better cache performance"],
                2,
                "Linked lists excel at insertion and deletion since you only need to update references."
            ),
            QuizQuestion(
                "How do you access the middle element of a Linked List?",
                ["Use an index like arr[n/2]", "Traverse from the head", "Jump directly to middle", "Use peek()"],
                1,
                "You must traverse from the head node, following references until you reach the desired position."
            )
        ],
        'binary-search': [
            QuizQuestion(
                "What is required for Binary Search to work?",
                ["Large dataset", "Sorted data", "Linked structure", "Stack data structure"],
                1,
                "Binary search only works on sorted data since it relies on comparing with the middle element."
            ),
            QuizQuestion(
                "What is the time complexity of Binary Search?",
                ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                1,
                "Binary search has O(log n) complexity because it halves the search space each iteration."
            ),
            QuizQuestion(
                "Why is Binary Search faster than Linear Search?",
                ["It checks every element", "It eliminates half the remaining elements each step", "It sorts while searching", "It uses more memory"],
                1,
                "By comparing with the middle and eliminating half the elements each time, binary search is much faster."
            ),
            QuizQuestion(
                "What does Binary Search return if element is not found?",
                ["0", "-1 or null", "Last checked index", "Throws exception"],
                1,
                "Most implementations return -1 or null to indicate the element was not found."
            )
        ],
        'recursion': [
            QuizQuestion(
                "What is recursion?",
                ["A loop structure", "A function that calls itself", "A sorting algorithm", "A data structure"],
                1,
                "Recursion is when a function calls itself to solve smaller versions of the same problem."
            ),
            QuizQuestion(
                "What is essential for recursion to work properly?",
                ["A large stack", "A base case", "Multiple parameters", "Global variables"],
                1,
                "A base case is critical to stop the recursion and prevent infinite loops."
            ),
            QuizQuestion(
                "What happens if recursion has no base case?",
                ["Program runs faster", "Stack overflow error", "Returns null", "Compiles with warning"],
                1,
                "Without a base case, recursion continues forever until the stack overflows."
            ),
            QuizQuestion(
                "When is recursion particularly useful?",
                ["Iterating through arrays", "Problems with self-similar subproblems", "Simple calculations", "Memory optimization"],
                1,
                "Recursion excels when a problem can be broken into smaller, similar subproblems."
            )
        ]
    }
    
    return fallback_quizzes.get(topic_key, fallback_quizzes['queue'])
