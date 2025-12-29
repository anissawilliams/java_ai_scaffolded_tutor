"""
Research Topics
ArrayList and Recursion content for the study
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ResearchTopic:
    """Represents a topic in the research study"""
    key: str
    name: str
    difficulty: str
    concept: str
    key_points: List[str]
    metaphor_prompt: str
    

# TODO: Replace with actual content from professors







ARRAYLIST_TOPIC = ResearchTopic(
    key='arraylist',
    name='Dynamic ArrayList',
    difficulty='easy',
    concept="""An ArrayList is a resizable array implementation in Java. Unlike regular arrays 
which have a fixed size, ArrayLists can grow and shrink dynamically as elements are added or removed. 
When an ArrayList runs out of space, it automatically creates a larger internal array and copies 
the elements over.""",
    key_points=[
        'ArrayList can grow and shrink dynamically (arrays cannot)',
        'Internally uses a regular array that gets resized when needed',
        'Automatic resizing happens when capacity is exceeded',
        'Common operations: add(), get(), remove(), size()',
        'Provides O(1) access by index, like arrays',
        'Resizing operation is O(n) but amortized to O(1) for add()'
    ],
    metaphor_prompt="""Think about ArrayList like a expandable photo album or a playlist that can 
keep growing. When you run out of pages in your photo album, you get a bigger one and move all 
your photos over. That's exactly how ArrayList works internally!"""
)

RECURSION_TOPIC = ResearchTopic(
    key='recursion',
    name='Recursion',
    difficulty='hard',
    concept="""Recursion is when a method calls itself to solve a problem by breaking it into 
smaller, similar subproblems. Every recursive method needs a base case (stopping condition) and 
a recursive case (where it calls itself with a smaller problem). Without a proper base case, 
recursion will continue infinitely and cause a stack overflow.""",
    key_points=[
        'Recursive method calls itself to solve smaller versions of the same problem',
        'Must have a base case to stop recursion',
        'Each recursive call is added to the call stack',
        'Common uses: tree traversal, factorial, fibonacci, divide-and-conquer',
        'Can be elegant but may use more memory than iterative solutions',
        'Stack overflow happens if base case is never reached'
    ],
    metaphor_prompt="""Think about recursion like nested Russian dolls or looking into two mirrors 
facing each other. Each reflection contains a smaller version of the same thing, until you reach 
the smallest doll or the reflection becomes too small to see (base case)."""
)


# Dictionary for easy lookup
RESEARCH_TOPICS = {
    'arraylist': ARRAYLIST_TOPIC,
    'recursion': RECURSION_TOPIC
}


def get_research_topic(topic_key: str) -> ResearchTopic:
    """Get a research topic by key."""
    if topic_key not in RESEARCH_TOPICS:
        raise ValueError(f"Topic '{topic_key}' not found")
    return RESEARCH_TOPICS[topic_key]


# Code examples for each topic

ARRAYLIST_CODE_EXAMPLES = {
    'basic': """// Creating and using an ArrayList
ArrayList<String> list = new ArrayList<>();

// Add elements (automatically resizes as needed)
list.add("first");
list.add("second");
list.add("third");

// Access elements by index (like an array)
String item = list.get(0);  // Returns "first"

// Remove elements
list.remove(1);  // Removes "second"

// Check size
int size = list.size();  // Returns 2""",

    'resizing': """// What happens behind the scenes when ArrayList resizes:

// Start with capacity 10
ArrayList<Integer> numbers = new ArrayList<>();

// Add elements 1-10: fits in current capacity
for (int i = 1; i <= 10; i++) {
    numbers.add(i);  // Fast
}

// Add 11th element: triggers resize!
numbers.add(11);  // Internally:
                  // 1. Creates new array (size ~15)
                  // 2. Copies all 10 elements to new array
                  // 3. Adds element 11
                  // 4. Discards old array""",

    'vs_array': """// Array (fixed size)
String[] arr = new String[3];
arr[0] = "first";
// Can't add more than 3 elements!

// ArrayList (dynamic size)
ArrayList<String> list = new ArrayList<>();
list.add("first");
list.add("second");
// Can keep adding forever!
list.add("third");
list.add("fourth");  // Works fine!"""
}

RECURSION_CODE_EXAMPLES = {
    'basic': """// Simple recursive function
public static int factorial(int n) {
    // Base case - stops recursion
    if (n <= 1) {
        return 1;
    }
    
    // Recursive case - calls itself
    return n * factorial(n - 1);
}

// factorial(5) returns 5 * 4 * 3 * 2 * 1 = 120""",

    'countdown': """// Countdown example showing the pattern
public static void countdown(int n) {
    // Base case
    if (n == 0) {
        System.out.println("Done!");
        return;
    }
    
    // Do something
    System.out.println(n);
    
    // Recursive call with smaller problem
    countdown(n - 1);
}

// countdown(3) prints: 3, 2, 1, Done!""",

    'fibonacci': """// Classic recursion: Fibonacci numbers
public static int fibonacci(int n) {
    // Base cases
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    // Recursive case - two recursive calls!
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// fibonacci(5) returns 5
// Sequence: 0, 1, 1, 2, 3, 5""",

    'call_stack': """// Understanding the call stack

factorial(3)
  ↓ calls
  3 * factorial(2)
       ↓ calls
       2 * factorial(1)
            ↓ calls
            1 (base case - returns 1)
            ↑ returns
       2 * 1 = 2
       ↑ returns
  3 * 2 = 6
  ↑ returns 6

Each call waits for the next to finish!"""
}


def get_code_example(topic_key: str, example_type: str = 'basic') -> str:
    """Get a code example for a topic."""
    if topic_key == 'arraylist':
        return ARRAYLIST_CODE_EXAMPLES.get(example_type, ARRAYLIST_CODE_EXAMPLES['basic'])
    elif topic_key == 'recursion':
        return RECURSION_CODE_EXAMPLES.get(example_type, RECURSION_CODE_EXAMPLES['basic'])
    return "# Code example not available"
