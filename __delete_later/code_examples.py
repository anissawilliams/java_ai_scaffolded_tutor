"""
Code Example Templates for Java Topics
These are reference examples the AI can use when teaching
"""

CODE_EXAMPLES = {
    'queue': {
        'basic': """Queue<String> queue = new LinkedList<>();
queue.add("first");     // enqueue - add to back
queue.add("second");    
queue.add("third");

String item = queue.remove();  // dequeue - remove from front
// item is now "first" (FIFO)""",
        
        'with_explanation': """// Create a Queue using LinkedList
Queue<String> queue = new LinkedList<>();

// Add elements (enqueue) - they go to the back
queue.add("Alice");   // Alice is first in line
queue.add("Bob");     // Bob is second
queue.add("Charlie"); // Charlie is third

// Remove elements (dequeue) - they come from the front
String next = queue.remove();  // Returns "Alice" (first in, first out)

// Check who's next without removing
String peek = queue.peek();  // Returns "Bob" (still in queue)""",
        
        'methods': """Key Queue methods:
- add(element)     → Adds to back of queue
- remove()         → Removes and returns front element  
- peek()           → Views front element (doesn't remove)
- isEmpty()        → Check if queue is empty
- size()           → Get number of elements"""
    },
    
    'stack': {
        'basic': """Stack<String> stack = new Stack<>();
stack.push("first");    // push - add to top
stack.push("second");   
stack.push("third");

String item = stack.pop();  // pop - remove from top
// item is now "third" (LIFO)""",
        
        'with_explanation': """// Create a Stack
Stack<String> stack = new Stack<>();

// Push elements (add to top)
stack.push("bottom");   // First in, last out
stack.push("middle");   
stack.push("top");      // Last in, first out

// Pop elements (remove from top)
String item = stack.pop();  // Returns "top" (LIFO)

// Peek at top without removing
String peek = stack.peek();  // Returns "middle" (still in stack)""",
        
        'methods': """Key Stack methods:
- push(element)    → Adds to top of stack
- pop()            → Removes and returns top element
- peek()           → Views top element (doesn't remove)
- empty()          → Check if stack is empty
- search(element)  → Find position of element from top"""
    },
    
    'linked-list': {
        'basic': """LinkedList<String> list = new LinkedList<>();
list.add("first");      // add to end
list.addFirst("new");   // add to beginning
list.addLast("last");   // add to end

String item = list.get(0);  // access by index
list.remove(1);             // remove by index""",
        
        'with_explanation': """// Create a LinkedList
LinkedList<Integer> list = new LinkedList<>();

// Add elements
list.add(10);          // Adds to end
list.add(20);
list.addFirst(5);      // Adds to beginning: [5, 10, 20]

// Access elements
int first = list.getFirst();  // Returns 5
int at_index = list.get(1);   // Returns 10

// Remove elements
list.remove(0);        // Removes first: [10, 20]
list.removeLast();     // Removes last: [10]""",
        
        'node_structure': """// What's happening behind the scenes:
class Node {
    int data;
    Node next;  // Reference to next node
    
    Node(int data) {
        this.data = data;
        this.next = null;
    }
}

// Each node points to the next one
// [5]→[10]→[20]→null""",
        
        'methods': """Key LinkedList methods:
- add(element)         → Add to end
- addFirst(element)    → Add to beginning
- addLast(element)     → Add to end
- get(index)           → Get element at index
- remove(index)        → Remove at index
- removeFirst()        → Remove first element
- removeLast()         → Remove last element"""
    },
    
    'binary-search': {
        'basic': """int[] arr = {1, 3, 5, 7, 9, 11, 13};  // Must be sorted!
int target = 7;

int index = Arrays.binarySearch(arr, target);
// Returns 3 (index where 7 is found)""",
        
        'with_explanation': """// Binary search on a sorted array
int[] numbers = {2, 4, 6, 8, 10, 12, 14, 16};
int target = 10;

// Using built-in method
int index = Arrays.binarySearch(numbers, target);
// Returns 4 (10 is at index 4)

// If not found, returns negative value
int notFound = Arrays.binarySearch(numbers, 5);
// Returns negative (5 not in array)""",
        
        'manual_implementation': """// Binary search implementation
public static int binarySearch(int[] arr, int target) {
    int left = 0;
    int right = arr.length - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;  // Found it!
        } else if (arr[mid] < target) {
            left = mid + 1;  // Search right half
        } else {
            right = mid - 1;  // Search left half
        }
    }
    
    return -1;  // Not found
}""",
        
        'key_points': """Binary Search Requirements:
1. Array MUST be sorted
2. Compare with middle element
3. Eliminate half the array each time
4. O(log n) time complexity

Example search for 10 in [2,4,6,8,10,12,14,16]:
Step 1: Check middle (8) → 10 > 8, search right half
Step 2: Check middle of right half (12) → 10 < 12, search left
Step 3: Check 10 → Found!"""
    },
    
    'recursion': {
        'basic': """// Simple recursive function
public static int factorial(int n) {
    if (n <= 1) {
        return 1;  // Base case
    }
    return n * factorial(n - 1);  // Recursive call
}

// factorial(5) returns 120""",
        
        'with_explanation': """// Recursion: a function that calls itself

public static int countdown(int n) {
    // Base case - stops the recursion
    if (n == 0) {
        System.out.println("Done!");
        return 0;
    }
    
    // Recursive case
    System.out.println(n);
    return countdown(n - 1);  // Calls itself with smaller value
}

// countdown(3) prints: 3, 2, 1, Done!""",
        
        'fibonacci': """// Classic recursion example - Fibonacci
public static int fibonacci(int n) {
    // Base cases
    if (n <= 1) {
        return n;
    }
    
    // Recursive case - breaks into smaller subproblems
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// fibonacci(5) returns 5 (sequence: 0,1,1,2,3,5)""",
        
        'key_points': """Recursion Requirements:
1. Base case - condition that stops recursion
2. Recursive case - function calls itself
3. Each call works on a SMALLER problem
4. Must eventually reach base case

Without base case → Stack Overflow!

Example: factorial(3)
  factorial(3)
  → 3 * factorial(2)
     → 2 * factorial(1)
        → 1 (base case)
     → 2 * 1 = 2
  → 3 * 2 = 6"""
    }
}


def get_code_example(topic_key: str, example_type: str = 'with_explanation') -> str:
    """
    Get a code example for a topic.
    
    Args:
        topic_key: Topic key (e.g., 'queue', 'stack')
        example_type: Type of example ('basic', 'with_explanation', 'methods', etc.)
    
    Returns:
        Code example as string
    """
    if topic_key not in CODE_EXAMPLES:
        return f"# Code example for {topic_key} not yet available"
    
    topic_examples = CODE_EXAMPLES[topic_key]
    
    if example_type not in topic_examples:
        # Return first available example
        example_type = list(topic_examples.keys())[0]
    
    return topic_examples[example_type]
