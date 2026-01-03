# New Metaphor Prompt Examples

## The Change

### Old Approach (Rigid)
```
"Now, what would you compare Queue to? Explain your understanding of Queue."
```

### New Approach (Natural + Hint)
The AI now creates more conversational endings with student-friendly hints.

---

## Example Outputs by Character

### Batman + Queue
**Old:**
> Let's examine Queue systematically. Think of evidence processing at a crime scene - first piece collected, first analyzed. That's FIFO: First In, First Out.
> 
> Now, what would you compare Queue to? Explain your understanding of Queue.

**New (Expected):**
> Let's examine Queue systematically. Think of evidence processing at a crime scene - first piece collected, first analyzed. That's FIFO: First In, First Out.
> 
> How would you describe this? Maybe think about witnesses waiting to give testimony - who goes first?

OR

> Processing evidence follows strict order - first collected, first analyzed. No exceptions. That's a Queue.
> 
> What situation does this remind you of? Perhaps people waiting at the DMV?

---

### Tony Stark + Stack
**Old:**
> Alright, Stacks. Picture my arc reactor assembly - components stack up, latest one on top gets grabbed first. Last In, First Out. Clean, efficient, powerful.
>
> Now, what would you compare Stack to? Explain your understanding of Stack.

**New (Expected):**
> Alright, Stacks. Picture my arc reactor assembly - components stack up, latest one on top gets grabbed first. Last In, First Out. Clean, efficient, powerful.
>
> How would you explain this to someone? Think about stacking armor plates - what comes off first?

OR

> Stack is simple. Last thing you put on top is the first thing you take off. Like building a tower of arc reactors - you work from the top down.
>
> Can you think of something similar? Maybe like browser history or undo in your code editor?

---

### Katniss + Queue  
**Old:**
> In District 12, we know about waiting in lines. Food rations, reaping day - first in line, first served. That's a Queue. Fair, ordered, no cutting.
>
> Now, what would you compare Queue to? Explain your understanding of Queue.

**New (Expected):**
> In District 12, we know about waiting in lines. Food rations, reaping day - first in line, first served. That's a Queue. Fair, ordered, no cutting.
>
> What does this remind you of? Like waiting for your turn at the archery range?

OR

> Queues are about fairness - first in, first out. No one cuts in line. That's survival.
>
> How would you describe this? Think about tributes entering the arena - who entered first?

---

### Hermione + Linked List
**Old:**
> Oh, Linked Lists are fascinating! Each element points to the next, like pages in a spellbook where each page tells you which page to read next.
>
> Now, what would you compare Linked List to? Explain your understanding of Linked List.

**New (Expected):**
> Oh, Linked Lists are fascinating! Each element points to the next, like pages in a spellbook where each page tells you which page to read next.
>
> Can you think of something similar? Perhaps like a treasure hunt where each clue leads to the next one?

OR

> A Linked List is quite elegant - each node knows where the next one is, creating a chain. It's like a scavenger hunt through the library!
>
> How would you explain this? Maybe think of train cars connected one after another?

---

### Yoda + Recursion
**Old:**
> Recursion, a function that calls itself, it is. Like looking into mirrors facing each other - reflections within reflections, you see.
>
> Now, what would you compare Recursion to? Explain your understanding of Recursion.

**New (Expected):**
> Recursion, a function that calls itself, it is. Like looking into mirrors facing each other - reflections within reflections, you see.
>
> A similar pattern, can you find? Perhaps nested boxes, one inside another?

OR

> Call itself, the function does. Smaller and smaller, the problem becomes, until simple it is. Then, back up it builds.
>
> Think you can, hmm? Like Russian dolls, perhaps - one within another?

---

## Why This is Better

### Student Psychology
1. **Less intimidating** - Not asking them to formally "explain their understanding"
2. **Scaffolded thinking** - Gives them a hint/direction to think
3. **More conversational** - Feels like a real discussion, not a test
4. **Character-appropriate** - Each character suggests hints from THEIR perspective

### Pedagogical Benefits
1. **Reduces cognitive load** - The hint gives them a starting point
2. **Encourages engagement** - "Think about X" is more inviting than "Explain your understanding"
3. **Models thinking** - Shows them HOW to think analogically
4. **Natural flow** - Leads smoothly into their response

### Technical Benefits
1. **AI generates varied hints** - Won't be the same every time
2. **Context-appropriate** - Batman suggests detective things, Katniss suggests survival things
3. **Student-friendly** - AI chooses relatable, everyday examples
4. **Maintains character voice** - The hint sounds like the character would say it

---

## Implementation Notes

The prompt now instructs the AI to:

```
4. End by inviting the student to share their own metaphor/understanding in a natural way
   - Provide a HINT for a metaphor they could use (make it student-friendly and relatable)
   - Examples of natural endings:
     * "What does this remind you of? Maybe something like [hint]?"
     * "Can you think of a similar situation? Perhaps [hint]?"
     * "How would you explain this? Think about [hint]..."
   - DO NOT use rigid phrasing like "What would you compare X to? Explain your understanding of X."
```

This gives the AI:
- Clear instruction to be natural
- Example patterns to follow
- Explicit instruction to avoid the old rigid format
- Freedom to be creative within character

---

## Fallback Hints

If AI generation fails, we now have topic-specific hints:

```python
fallback_hints = {
    'queue': 'waiting in line at a store or a printer queue',
    'stack': 'stacking plates or a pile of books',
    'linked-list': 'a train with connected cars or a chain',
    'binary-search': 'looking up a word in a dictionary',
    'recursion': 'nested dolls or looking in a mirror facing a mirror'
}
```

These ensure even the fallback is student-friendly!

---

## Testing the Change

### What to Look For

1. **No more "What would you compare X to? Explain your understanding of X."**
2. **A hint or suggestion**: "Think about...", "Maybe like...", "Perhaps..."
3. **Character voice maintained**: Batman's hints vs. Katniss's hints should differ
4. **Student-friendly examples**: Relatable, everyday situations
5. **Natural conversation flow**: Should feel like the character is genuinely asking

### Example Test Session

Start a Queue session with Batman:

**Expected ending:** Something like:
- "What comes to mind? Think about processing tasks in order..."
- "How would you describe this? Maybe like evidence processing?"
- "Can you think of a similar situation? Perhaps interrogating suspects one at a time?"

**NOT:** "What would you compare Queue to? Explain your understanding of Queue."
