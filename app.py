import streamlit as st

# Configure the page settings - this must be the first Streamlit command
st.set_page_config(
    page_title="Dark Triad Detector Quiz",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling - makes the app look cleaner and more professional
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #ff4b4b;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .tagline {
        text-align: center;
        color: #666;
        font-style: italic;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .question-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #ff4b4b;
    }
    .result-container {
        background-color: #fff3cd;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #ffc107;
    }
    .score-display {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #ff4b4b;
        margin: 1rem 0;
    }
    .result-message {
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 5px;
    }
    .low-risk { background-color: #d4edda; color: #155724; }
    .medium-risk { background-color: #fff3cd; color: #856404; }
    .high-risk { background-color: #f8d7da; color: #721c24; }
    .extreme-risk { background-color: #d1ecf1; color: #0c5460; }
</style>
""", unsafe_allow_html=True)

# The 12 questions from the original quiz
questions = [
    "Sabotage Campaign: Does he turn everyone—friends, family, dog—into spies who suddenly hate you?",
    "Triangulation Matrix: Does he pit you against mutual friends with whispers, lies, and fake beef?",
    "Success Assassin: Do your wins—job, hobby, mood—get crushed, interrupted, or turned into 'but you\'re ignoring ME'?",
    "Help-as-Alib: Does he ask for 'help' on easy shit—then blame you when he 'fails' (even if he never tried)?",
    "Public Scapegoat: Does he joke about your 'failure' in public? Use your name to book stuff—then no-show and trash your rep?",
    "Weaponized Insecurity (Twist Reality): Do innocent things—like walking your dog—get twisted into 'You\'re doing it to hurt me / fuck someone else'?",
    "Absence-Interrogation Flip: Is he gone all day—no word—then demands a 3-hour report on your moves while hiding his?",
    "Charm Blackout: Is he sweet only when he's about to vanish—or when he needs something? Cold the second you relax?",
    "Over-Information Burst: Does he suddenly spam details—'On 5th, buying gum'—right before ghosting or blowing up?",
    "Freeloader Flip: Does he leech when broke—then cut you off cold the second he's paid? 'Fuck off, you\'re not my kid'?",
    "Hypocrisy Vortex: Does he flirt with women but freak if you say hi to a guy? Accuse you of jealousy—while texting exes about you?",
    "Past-as-Bludgeon + Job Sabotage: Does he weaponize your past ('Remember when you were crazy?')—and make you late/tired so you lose jobs?"
]

def calculate_score(answers):
    """
    Calculate the total score based on 'Yes' answers.
    Each 'Yes' answer counts as 1 point.
    """
    score = sum(1 for answer in answers if answer == 'Yes')
    return score

def get_result_message(score):
    """
    Return the appropriate result message based on the score.
    Maintains the raw, direct tone from the original quiz.
    """
    if 0 <= score <= 3:
        return "Could just be an asshole. Or maybe he's just... bad at people. Watch it."
    elif 4 <= score <= 6:
        return "RED ZONE. Drain detected. Save yourself while you still remember your name."
    elif 7 <= score <= 9:
        return "BLACK HOLE CONFIRMED. You're not dating a man—you're orbiting a vampire. EVACUATE."
    elif 10 <= score <= 12:
        return "TOTAL FUCKING APOCALYPSE. He isn't human. He's a predator. Delete him. Block everywhere. Burn the hoodie. RUN."
    else:
        return "Invalid score."

def get_result_class(score):
    """
    Return the CSS class for styling based on the score range.
    """
    if 0 <= score <= 3:
        return "low-risk"
    elif 4 <= score <= 6:
        return "medium-risk"
    elif 7 <= score <= 9:
        return "high-risk"
    elif 10 <= score <= 12:
        return "extreme-risk"
    else:
        return "low-risk"

# Initialize session state variables to track quiz progress
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

# Sidebar with instructions
st.sidebar.markdown("### Instructions")
st.sidebar.markdown("""
Answer yes/no for each question. Be honest. Your truth matters.

**How it works:**
- 12 questions total
- Each "Yes" = 1 point
- Results based on total score
- One question at a time
""")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Progress:** {len(st.session_state.answers)}/12 questions")

# Main header and tagline
st.markdown('<h1 class="main-header">Dark Triad Detector Quiz</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Monsters don\'t see mirrors. They steal your reflection.</p>', unsafe_allow_html=True)

# Main quiz logic
if not st.session_state.quiz_completed:
    # Display current question
    if st.session_state.current_question < len(questions):
        current_q = st.session_state.current_question
        
        # Question container with styling
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown(f"### Question {current_q + 1} of {len(questions)}")
        st.markdown(f"**{questions[current_q]}**")
        
        # Radio buttons for Yes/No answer
        answer = st.radio(
            "Select your answer:",
            options=['Yes', 'No'],
            key=f"question_{current_q}",
            horizontal=True
        )
        
        # Next button
        if st.button("Next Question", type="primary"):
            # Store the answer
            st.session_state.answers.append(answer)
            
            # Move to next question or complete quiz
            if st.session_state.current_question < len(questions) - 1:
                st.session_state.current_question += 1
                st.rerun()  # Refresh the page to show next question
            else:
                # Quiz completed
                st.session_state.quiz_completed = True
                st.rerun()  # Refresh to show results
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # This shouldn't happen, but just in case
        st.session_state.quiz_completed = True
        st.rerun()

else:
    # Display results
    final_score = calculate_score(st.session_state.answers)
    result_message = get_result_message(final_score)
    result_class = get_result_class(final_score)
    
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.markdown("## Quiz Complete!")
    
    # Display score prominently
    st.markdown(f'<div class="score-display">Score: {final_score}/12</div>', unsafe_allow_html=True)
    
    # Display result message with appropriate styling
    st.markdown(f'<div class="result-message {result_class}">{result_message}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show all answers for review (optional)
    with st.expander("Review Your Answers"):
        for i, (question, answer) in enumerate(zip(questions, st.session_state.answers)):
            emoji = "✅" if answer == "Yes" else "❌"
            st.write(f"{i+1}. {question}")
            st.write(f"   {emoji} **{answer}**")
            st.write("")
    
    # Reset button to take quiz again
    if st.button("Take Quiz Again", type="secondary"):
        # Reset all session state variables
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.quiz_completed = False
        st.rerun()  # Refresh the page

# Footer with deployment info
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    <p>Built with Streamlit | Deploy to <a href='https://streamlit.io/cloud' target='_blank'>Streamlit Cloud</a></p>
</div>
""", unsafe_allow_html=True)