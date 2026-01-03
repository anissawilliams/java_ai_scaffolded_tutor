# Fix: AI Not Showing Code at CODE_STRUCTURE Step

## The Problem

In your example conversation:
```
Katniss: "Now let's see how this principle translates to Java code."
```

But then no code was shown! The AI just talked *about* showing code instead of actually showing it.

## Root Cause

The step instructions weren't explicit enough. The AI understood it should discuss code, but not that it MUST include actual code snippets.

## The Fix

### 1. Made Step Instructions Ultra-Explicit

**Before:**
```python
"Show the basic structure/syntax..."
```

**After:**
```python
"""CRITICAL: Include actual code in your response! Don't just describe it.

Example for Queue:
"Here's how a Queue works in Java:

```java
Queue<String> queue = new LinkedList<>();
queue.add("first");     // enqueue - add to back
String item = queue.remove();  // dequeue - remove from front
```

See how the first element we added is the first one removed?"
```

### 2. Added Code Instructions to Character System Prompt

Every character now has this in their system prompt:

```
WHEN SHOWING CODE:
- ALWAYS include actual Java code snippets with proper syntax
- Use code blocks or clearly formatted code
- Explain what each line does
- Connect code back to the metaphor/concept discussed
```

### 3. Provided Concrete Examples

Created `code_examples.py` with reference examples for every topic that the AI can use as templates.

## What Should Happen Now

### Your Exact Conversation

**Before (What Happened):**
```
Student: "Waiting for basketball tickets"
Katniss: "Good job making that connection. Now let's see 
         how this translates to Java code."
```
❌ No code shown

**After (What Should Happen):**
```
Student: "Waiting for basketball tickets"
Katniss: "Exactly! Basketball ticket line is perfect. First in line, 
         first to get tickets - that's FIFO.

Here's how that looks in Java:

Queue<String> queue = new LinkedList<>();
queue.add("Alice");    // Alice gets in line first
queue.add("Bob");      // Bob gets in line second
queue.add("Charlie");  // Charlie gets in line third

String next = queue.remove();  // Who gets tickets first?
// next is "Alice" - first in, first out!

See how Alice, who was first in line, is the first to get served? 
That's exactly like your basketball ticket example. Got any questions 
about the code?"
```
✅ Code included with explanation

## Testing the Fix

### Test Case 1: Queue
```
1. Student mentions any metaphor (line, waiting, etc.)
2. Have 2 exchanges about metaphor
3. Student says something like "makes sense" or "I understand"
4. Look for CODE_STRUCTURE step response
5. ✅ Should include actual Java Queue code
6. ✅ Should have comments explaining each line
7. ✅ Should connect back to their metaphor
```

### Test Case 2: Stack
```
1. Student: "Like stacking plates"
2. Katniss: [validates]
3. Student: "Got it"
4. Check response:
   ✅ Should show Stack<String> code
   ✅ Should show push() and pop()
   ✅ Should reference plates metaphor
```

### Test Case 3: Any Topic
At CODE_STRUCTURE step, response should:
- [ ] Include actual code with proper Java syntax
- [ ] Have inline comments
- [ ] Be 5-10 lines of code (not too complex)
- [ ] Connect to student's metaphor
- [ ] Explain what code does

## Code Example Format

The AI is now instructed to format code like this:

```
Character: [natural transition]

[code block]
Queue<String> queue = new LinkedList<>();
queue.add("first");     // explanation
queue.add("second");    
String item = queue.remove();  // explanation
[/code block]

[connect back to metaphor and ask question]
```

## Reference Examples Available

Created `code_examples.py` with examples for:
- Queue (basic, with explanation, methods)
- Stack (basic, with explanation, methods)
- LinkedList (basic, with explanation, node structure)
- Binary Search (basic, manual implementation)
- Recursion (basic, countdown, fibonacci)

These serve as templates the AI can reference when generating code.

## Character-Specific Code Delivery

Each character should maintain their voice when showing code:

**Katniss:**
```
"Alright, here's the code. It's straightforward:

[code]

See? First in, first out. Just like that ticket line you mentioned."
```

**Batman:**
```
"Let me show you the evidence - the actual Java code:

[code]

Observe: The first element added is the first removed. 
That's the pattern we're looking for."
```

**Tony Stark:**
```
"Here's how we engineer this. Watch closely:

[code]

Elegant, right? First in, first out. Clean and efficient. 
That's how I like my code."
```

## If It Still Doesn't Show Code

### Debugging Steps

1. **Check the step:**
   - Look at debug sidebar
   - Should say "Code Structure" or "Code"

2. **Check the prompt:**
   - The AI is getting CODE_STRUCTURE instructions
   - Instructions now explicitly say "MUST show code"

3. **Check the response:**
   - If response is >100 words but no code
   - AI might be hitting token limit
   - Reduce temperature or try again

4. **Manual override:**
   - Student can explicitly ask: "Can you show me the Java code?"
   - This will definitely trigger code display

## Summary

**Problem:** AI wasn't showing actual code, just talking about it

**Root Cause:** Instructions weren't explicit enough about including code

**Solution:** 
- Made instructions ultra-explicit with examples
- Added code formatting rules to character prompts
- Created reference code examples
- Increased emphasis on "MUST include actual code"

**Result:** AI should now always include formatted Java code snippets at CODE_STRUCTURE step
