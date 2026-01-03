# Java Learning Research Study - Setup Guide

## Overview

This is a research study system with 3 experimental conditions to test different approaches to teaching Java concepts.

### Study Design

**Participants:** 60 students (3 classes of 20-25)
**Topics:** ArrayList (easy) and Recursion (hard)
**Sessions:** 2 sessions per student (10 min learning + quiz + survey each)
**Conditions:**
1. Character-Based Scaffolded Learning
2. Non-Character Scaffolded Learning  
3. Direct Chat (Control)

## Setup Steps

### 1. Install Dependencies

```bash
pip install streamlit firebase-admin pyrebase4 python-dotenv
```

### 2. Set up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create new project: "java-learning-study"
3. Enable Authentication:
   - Go to Authentication > Sign-in method
   - Enable "Email/Password"
4. Enable Realtime Database:
   - Go to Realtime Database > Create Database
   - Start in test mode
5. Get credentials:
   - Project Settings > General > Your apps
   - Add web app, copy config
   - Update `firebase_config.py`
6. Get service account:
   - Project Settings > Service Accounts
   - Generate private key
   - Save JSON file
   - Update `firebase_config.py`

### 3. Configure Study Settings

Edit `config.py`:
```python
TOTAL_PARTICIPANTS = 60
PARTICIPANTS_PER_CONDITION = 20
SESSION_DURATION = 10 * 60  # 10 minutes
```

### 4. Add Content (When Ready)

1. **ArrayList Content** → `research_topics.py`
2. **Recursion Content** → `research_topics.py`
3. **Quiz Questions** → `static_quiz.py`
4. **Survey Questions** → `survey.py`

### 5. Test the System

```bash
# Test Firebase connection
python test_connection.py

# Run the app
streamlit run app_simplified.py
```

### 6. Deploy

Options:
- **Streamlit Cloud** (easiest)
- **Heroku**
- **University Server**

## File Structure

```
research_study/
├── app_research.py          # Main application
├── config.py                # Study configuration
├── firebase_config.py       # Firebase credentials
├── auth.py                  # Authentication
├── database.py              # Data storage
├── research_topics.py       # ArrayList & Recursion content
├── static_quiz.py           # Quiz questions
├── survey.py                # Survey questions
├── data_export.py           # CSV export
├── conditions.py            # 3 condition implementations
└── README_SETUP.md          # This file

legacy/
└── app_simplified.py        # Original version (backup)
```

## Firebase Database Structure

```
users/
  {userId}/
    email: "student@example.com"
    condition: 1 | 2 | 3
    condition_name: "character_scaffolded" | ...
    assigned_date: timestamp
    
    sessions/
      arraylist/
        status: "not_started" | "in_progress" | "completed"
        start_time: timestamp
        end_time: timestamp
        duration_seconds: 600
        messages: [...]
        scaffold_progress: [...]
        quiz_responses: {...}
        quiz_score: 4
        quiz_total: 5
        survey_responses: {...}
        
      recursion/
        [same structure]
```

## Running the Study

### For Students

1. Share link: `your-app-url.streamlit.app`
2. Students create account with email
3. System randomly assigns condition
4. Student completes Session 1 (ArrayList)
5. Later: Student completes Session 2 (Recursion)

### For Researchers

1. Monitor progress via admin dashboard
2. Export data via `data_export.py`
3. Analyze CSV files

## Data Collection

Automatically collected:
- All conversation messages (timestamped)
- Scaffold step progression (conditions 1 & 2)
- Time spent in session
- Number of interactions
- Quiz responses and scores
- Survey responses
- Session completion status

## Export Data

Two CSV formats:

1. **Summary CSV** (one row per session):
   - user_id, email, condition, topic
   - duration, message counts
   - quiz score
   - survey responses summary

2. **Detailed CSV** (one row per message):
   - For conversation analysis
   - Complete message history
   - Timestamps and steps

## Conditions Explained

### Condition 1: Character-Based Scaffolded
- Student chooses character (Batman, Hermione, etc.)
- 5-step scaffolding:
  1. Initial Metaphor
  2. Student Metaphor
  3. Visual + Code
  4. Usage Examples
  5. Practice
- Visual diagrams
- Character personality maintained

### Condition 2: Non-Character Scaffolded
- Generic "tutor" voice
- Same 5-step scaffolding
- Same visuals and code
- No character personality

### Condition 3: Direct Chat (Control)
- Plain Q&A interface
- No scaffolding
- No character
- No step progression
- Just: "Ask me about ArrayList"

## Troubleshooting

### Firebase Connection Issues
```bash
# Check credentials
python -c "from firebase_config import FIREBASE_CONFIG; print(FIREBASE_CONFIG)"

# Should NOT show "YOUR_API_KEY"
```

### Assignment Balance Issues

```python
# Check condition distribution
from utils.database import get_all_users

users = get_all_users()
conditions = [u.get('condition') for u in users.values()]
print(f"C1: {conditions.count(1)}, C2: {conditions.count(2)}, C3: {conditions.count(3)}")
```

### Data Not Saving
- Check Firebase Realtime Database rules
- Verify user is authenticated
- Check browser console for errors

## Research Ethics

**Important:** 
- Add IRB approval info
- Include consent form
- Ensure data privacy
- Allow opt-out option

## Contact

For technical issues: [your-email]
For study questions: [professor-email]

## Timeline

- Week 1: Setup and test
- Week X: Session 1 (ArrayList)
- Week Y: Session 2 (Recursion)
- End: Data export and analysis

## Next Steps

1. ✅ Set up Firebase
2. ✅ Configure study settings
3. ⏳ Add ArrayList content
4. ⏳ Add Recursion content
5. ⏳ Finalize quiz questions
6. ⏳ Finalize survey questions
7. ⏳ Test with pilot group
8. ⏳ Deploy for actual study
9. ⏳ Collect data
10. ⏳ Export and analyze

Good luck with your research! 🎓
