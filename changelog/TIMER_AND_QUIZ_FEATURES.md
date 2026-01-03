# New Features: Timer & Quiz System

## Overview

Two major new features have been added to improve the learning experience:

1. **60-Second Hint System** - Provides helpful hints if student doesn't respond
2. **End-of-Session Quiz** - 4-question quiz to check understanding

---

## Feature 1: 60-Second Hint System

### How It Works

**Timer Starts When:**
- Session begins (with initial metaphor)
- After each AI response

**What Happens:**
1. Student has 60 seconds to respond
2. At 55 seconds: Countdown warning appears
3. At 60 seconds: AI generates and displays a helpful hint

**Hint Reset:**
- Timer resets when student sends a message
- Only one hint per AI response (won't spam hints)

### Example Flow

```
00:00 - Batman: "Let's examine Queue systematically..."
00:55 - Warning: "⏰ Hint coming in 5 seconds if no response..."
01:00 - Batman: "💡 Hint: Take your time! What comes to mind when 
               you think about waiting in line?"

[Student responds]
00:00 - Timer resets
```

### Hint Intelligence

Hints are **context-aware** based on current step:

**Step 1 - Initial Metaphor:**
> "Take your time! What comes to mind when you think about this?"

**Step 2 - Student Metaphor:**
> "Good start! Want to see how this looks in actual code?"

**Step 3 - Code Structure:**
> "What questions do you have about the code? Any part you'd like me to explain?"

**Step 4 - Code Usage:**
> "Can you think of a situation where you'd use this?"

**Step 5 - Practice:**
> "Want to try an example problem?"

### Technical Implementation

```python
# Timer tracking in session state
st.session_state.last_hint_time  # When last hint timer started
st.session_state.hint_given      # Whether hint already given

# Hint generation
def generate_hint():
    # Uses AI to generate character-appropriate hint
    # Falls back to hardcoded hints if AI fails
    
# Auto-refresh mechanism
# App checks timer every 5 seconds when near timeout
```

---

## Feature 2: End-of-Session Quiz

### When Quiz Appears

**Automatically:**
- When 20-minute session timer expires

**Manually:**
- Student clicks "End Session & Take Quiz" button

### Quiz Structure

**4 multiple-choice questions** covering:
- Conceptual understanding (not just memorization)
- Key principles of the topic
- Practical applications
- Common misconceptions

### Quiz Generation

**Primary Method - AI Generated:**
```python
generate_quiz(topic_key, ai_client, num_questions=4)
```
- AI creates custom questions for the topic
- Tests conceptual understanding
- Provides explanations

**Fallback - Hardcoded:**
- Each topic has 4 quality fallback questions
- Used if AI generation fails
- Ensures quiz always works

### Quiz Flow

```
1. Session ends (timer or manual)
   ↓
2. Quiz screen appears
   ↓
3. Student answers 4 questions
   ↓
4. Click "Submit Quiz"
   ↓
5. See results with explanations
   ↓
6. "Start New Session" button
```

### Quiz Display

**Question Format:**
```
Question 1
What is the key ordering principle of a Queue?

○ Last In, First Out (LIFO)
○ First In, First Out (FIFO)
○ Random Access
○ Priority-based

[All questions must be answered to submit]
```

**Results Format:**
```
Question 1 - ✅ Correct

Question: What is the key ordering principle of a Queue?
Your answer: First In, First Out (FIFO)

ℹ️ Explanation: Queues follow FIFO - the first element 
added is the first one removed.

---

Your Score: 3/4
Percentage: 75%

🎉 Excellent work! Batman would be proud!

[Start New Session]
```

### Scoring & Feedback

| Score | Percentage | Message |
|-------|------------|---------|
| 3-4/4 | 75-100% | 🎉 Excellent work! {Character} would be proud! |
| 2/4 | 50-74% | 👍 Good effort! {Character} thinks you're getting there! |
| 0-1/4 | 0-49% | 💪 Keep practicing! {Character} believes in you! |

---

## Example Quiz Questions by Topic

### Queue
1. **What is the key ordering principle of a Queue?**
   - Answer: First In, First Out (FIFO)

2. **Which operation adds an element to a Queue?**
   - Answer: enqueue()

3. **When would you use a Queue?**
   - Answer: Processing tasks in order

4. **What happens when you dequeue from an empty Queue?**
   - Answer: Returns null/throws exception

### Stack
1. **What is the key ordering principle of a Stack?**
   - Answer: Last In, First Out (LIFO)

2. **Which operation adds an element to a Stack?**
   - Answer: push()

3. **Which real-world scenario best represents a Stack?**
   - Answer: Undo button in a text editor

4. **What does peek() do on a Stack?**
   - Answer: Views top element without removing

---

## Session State Management

### New State Variables

```python
# Hint system
st.session_state.last_hint_time   # Timestamp of last hint timer start
st.session_state.hint_given       # Boolean: hint given for current response?

# Quiz system
st.session_state.show_quiz        # Boolean: show quiz screen?
st.session_state.quiz_questions   # List[QuizQuestion]: generated questions
st.session_state.quiz_answers     # Dict[int, str]: student's answers
st.session_state.quiz_submitted   # Boolean: quiz submitted?
```

### State Flow

```
Session Start
  ↓
last_hint_time = now
hint_given = False
  ↓
[Student responds]
  ↓
last_hint_time = now (reset)
hint_given = False
  ↓
[60 seconds pass]
  ↓
Generate hint
hint_given = True
  ↓
[Student responds]
  ↓
Reset for next message
```

---

## Handling Streamlit Timer Issues

### The Problem

Streamlit's rerun mechanism can interfere with timers because:
1. Reruns reset the execution context
2. Time-based checks need explicit triggers
3. Auto-refresh can conflict with user input

### The Solution

**1. Persistent State:**
```python
# Store all timing info in session_state
st.session_state.last_hint_time  # Survives reruns
```

**2. Smart Auto-Refresh:**
```python
# Only refresh when needed
if time_since_hint >= 55 and time_since_hint < 60:
    st.info("Hint coming in X seconds...")
    time.sleep(1)
    st.rerun()
```

**3. One-Time Hints:**
```python
# Flag prevents multiple hints
if not st.session_state.hint_given:
    generate_hint()
    st.session_state.hint_given = True
```

**4. Reset on User Input:**
```python
def handle_user_message(user_input):
    # ... process message ...
    st.session_state.last_hint_time = time.time()
    st.session_state.hint_given = False
```

---

## Testing the Features

### Test 60-Second Hint

1. Start a session
2. Wait for initial message
3. **Don't respond**
4. At 55 seconds: See countdown
5. At 60 seconds: Hint appears
6. Respond
7. Timer resets

### Test Quiz - Auto Trigger

1. Start a session
2. Wait 20 minutes (or change SESSION_DURATION to 60 for testing)
3. Quiz should automatically appear

### Test Quiz - Manual Trigger

1. Start a session
2. Have a conversation
3. Click "End Session & Take Quiz"
4. Quiz appears

### Test Quiz Flow

1. See 4 questions
2. Try to submit without answering all → Disabled
3. Answer all 4 questions
4. Click "Submit Quiz"
5. See results with explanations
6. See score and character message
7. Click "Start New Session"

---

## Configuration

### Adjustable Timeouts

```python
# In app_simplified.py
SESSION_DURATION = 20 * 60  # 20 minutes total session
RESPONSE_TIMEOUT = 60       # 60 seconds before hint

# For testing, you can reduce these:
SESSION_DURATION = 2 * 60   # 2 minutes
RESPONSE_TIMEOUT = 10       # 10 seconds
```

### Quiz Settings

```python
# In quiz_generator.py
num_questions = 4  # Default number of questions

# To change:
generate_quiz(topic_key, ai_client, num_questions=5)
```

---

## Files Modified/Created

### New Files
- `quiz_generator.py` - Quiz generation and fallback questions

### Modified Files
- `app_simplified.py` - Added hint system, quiz rendering, timer logic
- All topics now have fallback quiz questions

### Key Functions Added

```python
generate_hint() → str
  # Generates contextual hint based on current step

render_quiz()
  # Displays quiz questions and results

generate_quiz(topic, client, num) → List[QuizQuestion]
  # Creates quiz using AI or fallback
```

---

## Troubleshooting

### Hint Not Appearing

**Check:**
1. Is `last_hint_time` set?
2. Has 60 seconds actually passed?
3. Was last message from assistant?
4. Has hint already been given?

**Debug:**
```python
# Add to debug sidebar
st.write(f"Time since hint: {time.time() - st.session_state.last_hint_time:.0f}s")
st.write(f"Hint given: {st.session_state.hint_given}")
```

### Quiz Not Generating

**Check:**
1. Is AI client initialized?
2. Check console for errors
3. Fallback questions should still work

**Debug:**
```python
# Quiz generation logs errors
print(f"Error generating quiz: {e}")
```

### Timer Acting Weird

**Common Issues:**
1. Multiple tabs open → Each has own state
2. Streamlit Cloud → May have delays
3. System clock changes → Reset timer

**Solutions:**
1. Use single tab
2. Accept some delay on cloud deployments
3. Timer resets on next interaction

---

## Future Enhancements

Potential improvements:

1. **Adaptive Hints**
   - Track which steps student struggles with
   - Provide more detailed hints for difficult concepts

2. **Quiz Difficulty**
   - Generate easier/harder questions based on conversation
   - Adaptive difficulty

3. **Progress Tracking**
   - Save quiz scores across sessions
   - Track improvement over time

4. **Hint Preferences**
   - Let students disable hints
   - Adjust hint timing

5. **Quiz Review**
   - Let students review quiz before new session
   - Show common mistakes
