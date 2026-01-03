"""
Simplified Java Tutor - Main Application
Clean architecture with clear pedagogical flow
"""

import streamlit as st
import time

from tutor_flow import TutorFlow, ScaffoldStep, StepGuide
from client.ai_client import SimpleAIClient
from characters import get_character, get_all_character_names
from __delete_later.topics import get_topic, get_all_topic_names
from __delete_later.quiz_generator import generate_quiz
from __delete_later.visuals import get_topic_visual


# Configuration
SESSION_DURATION = 10 * 60  # 10 minutes
RESPONSE_TIMEOUT = 60  # 60 seconds before prompting


def get_step_display_name(step: ScaffoldStep) -> str:
    """Get display name for a scaffold step"""
    names = {
        ScaffoldStep.INITIAL_METAPHOR: "Initial Metaphor",
        ScaffoldStep.STUDENT_METAPHOR: "Your Metaphor",
        ScaffoldStep.CODE_STRUCTURE: "Code Structure",
        ScaffoldStep.CODE_USAGE: "Usage Examples",
        ScaffoldStep.PRACTICE: "Practice"
    }
    return names.get(step, f"Unknown Step ({step.value if hasattr(step, 'value') else step})")


def initialize_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.session_active = False
        st.session_state.selected_topic = None
        st.session_state.selected_character = None
        st.session_state.flow = None
        st.session_state.ai_client = None
        st.session_state.start_time = None
        st.session_state.last_activity = None
        st.session_state.last_hint_time = None  # Track when we last gave a hint
        st.session_state.hint_given = False  # Whether we've given a hint for current message
        st.session_state.show_quiz = False  # Whether to show quiz
        st.session_state.quiz_questions = None  # Generated quiz questions
        st.session_state.quiz_answers = {}  # Student's answers
        st.session_state.quiz_submitted = False  # Whether quiz is submitted
    
    # Ensure new variables exist even in existing sessions
    if 'last_hint_time' not in st.session_state:
        st.session_state.last_hint_time = None
    if 'hint_given' not in st.session_state:
        st.session_state.hint_given = False
    if 'show_quiz' not in st.session_state:
        st.session_state.show_quiz = False
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = None
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False


def start_session(topic_key: str, character_name: str):
    """Start a new learning session"""
    try:
        # Initialize AI client
        st.session_state.ai_client = SimpleAIClient()
        
        # Get topic and character
        topic = get_topic(topic_key)
        character = get_character(character_name)
        
        # Initialize flow manager
        st.session_state.flow = TutorFlow(topic.name, character.name)
        
        # Generate initial metaphor
        char_prompt = character.get_system_prompt(topic.name)
        metaphor_prompt = StepGuide.get_metaphor_prompt(
            character.name, topic.name, topic.concept
        )
        
        with st.spinner(f'{character.name} is preparing your lesson...'):
            initial_message = st.session_state.ai_client.generate_initial_metaphor(
                char_prompt, metaphor_prompt
            )
        
        # Fallback if generation fails
        if not initial_message:
            # Create character-specific fallback with hint
            fallback_hints = {
                'queue': 'waiting in line at a store or a printer queue',
                'stack': 'stacking plates or a pile of books',
                'linked-list': 'a train with connected cars or a chain',
                'binary-search': 'looking up a word in a dictionary',
                'recursion': 'nested dolls or looking in a mirror facing a mirror'
            }
            hint = fallback_hints.get(topic_key, 'something from everyday life')
            
            initial_message = f"""Hello! I'm {character.name}, and I'm here to help you understand {topic.name}.

{topic.concept}

How would you explain this in your own words? Think about {hint}."""
        
        # Add to flow
        st.session_state.flow.add_message('assistant', initial_message)
        
        # Set session as active
        st.session_state.session_active = True
        st.session_state.start_time = time.time()
        st.session_state.last_activity = time.time()
        st.session_state.last_hint_time = time.time()  # Initialize hint timer
        st.session_state.hint_given = False
        st.session_state.selected_topic = topic_key
        st.session_state.selected_character = character_name
        
    except Exception as e:
        st.error(f"Error starting session: {str(e)}")
        st.session_state.session_active = False




def generate_hint() -> str:
    """Generate a helpful hint based on current step"""
    if not st.session_state.flow:
        return ""
    
    flow = st.session_state.flow
    character = get_character(st.session_state.selected_character)
    topic = get_topic(st.session_state.selected_topic)
    
    # Get last assistant message
    last_msg = None
    for msg in reversed(flow.messages):
        if msg.role == 'assistant':
            last_msg = msg
            break
    
    if not last_msg:
        return ""
    
    # Generate hint based on current step
    hint_prompts = {
        ScaffoldStep.INITIAL_METAPHOR: f"The student hasn't responded to your initial metaphor about {topic.name}. Give them a gentle, encouraging hint to share their own metaphor or understanding. Keep it under 50 words.",
        
        ScaffoldStep.STUDENT_METAPHOR: f"The student shared a metaphor but hasn't continued the discussion. Give them a hint to explore their understanding further or ask about the code. Keep it under 50 words.",
        
        ScaffoldStep.CODE_STRUCTURE: f"The student saw the code structure but hasn't asked about it. Give them a hint to ask about specific parts or to think about when they'd use this. Keep it under 50 words.",
        
        ScaffoldStep.CODE_USAGE: f"The student learned about usage but hasn't engaged further. Give them a hint to think of their own examples or try applying it. Keep it under 50 words.",
        
        ScaffoldStep.PRACTICE: f"The student is in practice mode but hasn't asked anything. Give them an encouraging hint to try an example or ask a question. Keep it under 50 words."
    }
    
    prompt = hint_prompts.get(flow.current_step, "Give a brief encouraging hint (under 50 words).")
    
    try:
        hint = st.session_state.ai_client.generate_response(
            system_prompt=character.get_system_prompt(topic.name),
            user_message=prompt,
            temperature=0.8
        )
        return hint
    except:
        # Fallback hints
        fallback_hints = {
            ScaffoldStep.INITIAL_METAPHOR: "Take your time! What comes to mind when you think about this?",
            ScaffoldStep.STUDENT_METAPHOR: "Good start! Want to see how this looks in actual code?",
            ScaffoldStep.CODE_STRUCTURE: "What questions do you have about the code? Any part you'd like me to explain?",
            ScaffoldStep.CODE_USAGE: "Can you think of a situation where you'd use this?",
            ScaffoldStep.PRACTICE: "Want to try an example problem?"
        }
        return fallback_hints.get(flow.current_step, "Any questions?")


def handle_user_message(user_input: str):
    """Handle a message from the user"""
    if not st.session_state.session_active or not st.session_state.flow:
        return
    
    try:
        flow = st.session_state.flow
        topic = get_topic(st.session_state.selected_topic)
        character = get_character(st.session_state.selected_character)
        
        # Add user message to flow
        flow.add_message('user', user_input)
        
        # Check if we should advance to next step
        old_step = flow.current_step
        if flow.should_advance_step(user_input):
            flow.advance_step()
            # Show step transition with toast notification
            st.toast(f"✅ Step advanced: {get_step_display_name(old_step)} → {get_step_display_name(flow.current_step)}", icon="📈")
            
            # If we just advanced to CODE_STRUCTURE, inject a visual first
            if flow.current_step == ScaffoldStep.CODE_STRUCTURE:
                visual = get_topic_visual(st.session_state.selected_topic)
                flow.add_message('assistant', f"📊 **Visual Diagram:**\n{visual}")
                st.session_state.last_activity = time.time()
                st.session_state.last_hint_time = time.time()
        
        # Build recent context for AI
        recent_messages = flow.get_recent_context(5)
        context_str = "\n".join([
            f"{msg.role.upper()}: {msg.content}" 
            for msg in recent_messages
        ])
        
        # Generate response
        system_prompt = character.get_system_prompt(topic.name)
        response_prompt = StepGuide.get_response_prompt(
            character.name,
            topic.name,
            flow.current_step,
            user_input,
            context_str
        )
        
        # Build conversation history for OpenAI
        conversation_history = []
        for msg in recent_messages:
            conversation_history.append({
                'role': msg.role,
                'content': msg.content
            })
        
        with st.spinner(f'{character.name} is thinking...'):
            response = st.session_state.ai_client.generate_response(
                system_prompt=system_prompt + "\n\n" + response_prompt,
                user_message=user_input,
                conversation_history=conversation_history[:-1]  # Exclude the current message we just added
            )
        
        # Add assistant response to flow
        flow.add_message('assistant', response)
        
        # Update activity time and reset hint timer
        st.session_state.last_activity = time.time()
        st.session_state.last_hint_time = time.time()
        st.session_state.hint_given = False  # Reset hint flag
        
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        # Add a simple fallback message
        flow.add_message('assistant', 
                        f"I'm having trouble responding right now. Could you try rephrasing that?")


def render_topic_selection():
    """Render topic and character selection"""
    st.title("☕ Java 221 Tutor")
    st.write("Welcome! Select a topic and character to begin your learning session.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Select Topic")
        topic_names = get_all_topic_names()
        topic_display = {key: get_topic(key).name for key in topic_names}
        
        selected_topic = st.selectbox(
            "Choose a topic to learn:",
            options=topic_names,
            format_func=lambda x: topic_display[x],
            key='topic_selector'
        )
        
        if selected_topic:
            topic = get_topic(selected_topic)
            with st.expander("📖 Topic Overview"):
                st.write(f"**{topic.name}**")
                st.write(topic.concept)
                st.write("**Key Points:**")
                for point in topic.key_points:
                    st.write(f"• {point}")
    
    with col2:
        st.subheader("🎭 Select Character")
        character_names = get_all_character_names()
        
        selected_character = st.selectbox(
            "Choose your tutor:",
            options=character_names,
            key='character_selector'
        )
        
        if selected_character:
            character = get_character(selected_character)
            with st.expander("👤 Character Info"):
                st.write(f"**{character.name}**")
                st.write(f"*{character.personality}*")
                st.write(f"**Teaching Style:** {character.teaching_approach}")
    
    st.write("---")
    
    if selected_topic and selected_character:
        if st.button("🚀 Start Learning Session", type="primary", use_container_width=True):
            start_session(selected_topic, selected_character)
            st.rerun()




def render_quiz():
    """Render the end-of-session quiz"""
    st.header("📝 Knowledge Check Quiz")
    
    character = get_character(st.session_state.selected_character)
    topic = get_topic(st.session_state.selected_topic)
    
    st.write(f"Great job learning about {topic.name} with {character.name}!")
    st.write("Let's check your understanding with a few questions.")
    st.write("---")
    
    # Generate quiz if not already generated
    if st.session_state.quiz_questions is None:
        with st.spinner("Generating quiz..."):
            try:
                st.session_state.quiz_questions = generate_quiz(
                    st.session_state.selected_topic,
                    st.session_state.ai_client,
                    num_questions=4
                )
            except Exception as e:
                st.error(f"Error generating quiz: {e}")
                st.session_state.quiz_questions = []
    
    questions = st.session_state.quiz_questions
    
    if not st.session_state.quiz_submitted:
        # Display questions
        for i, q in enumerate(questions):
            st.subheader(f"Question {i+1}")
            st.write(q.question)
            
            # Radio buttons for options
            answer = st.radio(
                f"Select your answer:",
                options=q.options,
                key=f"quiz_q_{i}",
                index=None
            )
            
            if answer:
                st.session_state.quiz_answers[i] = answer
            
            st.write("")  # Spacing
        
        # Submit button
        all_answered = len(st.session_state.quiz_answers) == len(questions)
        if st.button("Submit Quiz", type="primary", disabled=not all_answered):
            st.session_state.quiz_submitted = True
            st.rerun()
        
        if not all_answered:
            st.info(f"Please answer all questions ({len(st.session_state.quiz_answers)}/{len(questions)} complete)")
    
    else:
        # Show results
        st.success("✅ Quiz Submitted!")
        st.write("---")
        
        correct_count = 0
        for i, q in enumerate(questions):
            user_answer = st.session_state.quiz_answers.get(i)
            is_correct = user_answer == q.correct_answer
            
            if is_correct:
                correct_count += 1
            
            # Display each question with result
            with st.expander(f"Question {i+1} - {'✅ Correct' if is_correct else '❌ Incorrect'}", expanded=True):
                st.write(f"**Question:** {q.question}")
                st.write(f"**Your answer:** {user_answer}")
                
                if not is_correct:
                    st.write(f"**Correct answer:** {q.correct_answer}")
                
                if q.explanation:
                    st.info(f"**Explanation:** {q.explanation}")
        
        # Score
        score_pct = (correct_count / len(questions)) * 100
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Score", f"{correct_count}/{len(questions)}")
        with col2:
            st.metric("Percentage", f"{score_pct:.0f}%")
        
        # Encouraging message from character
        if score_pct >= 75:
            st.success(f"🎉 Excellent work! {character.name} would be proud!")
        elif score_pct >= 50:
            st.info(f"👍 Good effort! {character.name} thinks you're getting there!")
        else:
            st.warning(f"💪 Keep practicing! {character.name} believes in you!")
        
        # New session button
        if st.button("Start New Session", type="primary"):
            # Reset everything
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_learning_session():
    """Render the active learning session"""
    flow = st.session_state.flow
    character = get_character(st.session_state.selected_character)
    topic = get_topic(st.session_state.selected_topic)
    
    # Debug sidebar (optional - can be removed in production)
    with st.sidebar:
        st.write("### 🔍 Debug Info")
        st.write(f"**Current Step:** {get_step_display_name(flow.current_step)}")
        
        # Count messages at current step
        user_msgs_at_step = sum(1 for m in flow.messages 
                               if m.step == flow.current_step 
                               and m.role == 'user')
        st.write(f"**User messages at step:** {user_msgs_at_step}")
        st.write(f"**Total messages:** {len(flow.messages)}")
        
        # Show message history
        with st.expander("📜 Message History"):
            for i, msg in enumerate(flow.messages):
                role_emoji = "🧑" if msg.role == "user" else "🤖"
                st.write(f"{i+1}. {role_emoji} {msg.role}: {msg.content[:50]}...")
        
        if st.button("🔄 Force Next Step", help="Skip to next step (debugging)"):
            flow.advance_step()
            st.rerun()
    
    # Header with session info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title(f"☕ Learning {topic.name}")
    with col2:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, SESSION_DURATION - elapsed)
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        st.metric("Time Remaining", f"{mins}:{secs:02d}")
    with col3:
        # Use shorter names for the header metric
        short_names = {
            ScaffoldStep.INITIAL_METAPHOR: "Metaphor",
            ScaffoldStep.STUDENT_METAPHOR: "Your Turn",
            ScaffoldStep.CODE_STRUCTURE: "Code",
            ScaffoldStep.CODE_USAGE: "Usage",
            ScaffoldStep.PRACTICE: "Practice"
        }
        st.metric("Current Step", short_names.get(flow.current_step, "Learning"))
    
    st.write(f"**Tutor:** {character.name}")
    st.write(f"**Messages:** {len(flow.messages)} total")
    st.write("---")
    
    # Display conversation with auto-scroll to bottom
    chat_container = st.container(height=500)  # Fixed height with scroll
    with chat_container:
        for msg in flow.messages:
            with st.chat_message(msg.role):
                st.write(msg.content)
    
    # Chat input - PROCESS THIS FIRST before any timer checks
    user_input = st.chat_input(
        placeholder="Type your response here...",
        key='chat_input'
    )
    
    if user_input:
        # User sent a message - handle it immediately
        handle_user_message(user_input)
        st.rerun()
    
    # Optional hint button (instead of automatic hints that can interfere)
    if st.session_state.last_hint_time and not st.session_state.hint_given:
        time_since_hint = time.time() - st.session_state.last_hint_time
        
        # Show hint button after 30 seconds of inactivity
        if time_since_hint >= 30:
            last_msg = flow.messages[-1] if flow.messages else None
            if last_msg and last_msg.role == 'assistant' and '💡 Hint:' not in last_msg.content:
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    if st.button("💡 Need a Hint?", key="hint_button"):
                        hint = generate_hint()
                        if hint:
                            flow.add_message('assistant', f"💡 Hint: {hint}")
                            st.session_state.hint_given = True
                            st.rerun()
    
    # End session button - triggers quiz
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("End Session & Take Quiz", type="secondary"):
            st.session_state.show_quiz = True
            st.rerun()


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Java 221 Tutor",
        page_icon="☕",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Show selection, learning session, or quiz
    if not st.session_state.session_active:
        render_topic_selection()
    elif hasattr(st.session_state, 'show_quiz') and st.session_state.show_quiz:
        # Show quiz
        render_quiz()
    else:
        # Check if session time is up - auto-trigger quiz
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            if elapsed >= SESSION_DURATION:
                st.session_state.show_quiz = True
                st.rerun()
        
        # Render learning session
        render_learning_session()


if __name__ == "__main__":
    main()
