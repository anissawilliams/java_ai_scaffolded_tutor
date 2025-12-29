"""
Authentication Module
Handles user login and session management with Firebase
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, db
import pyrebase
from firebase_config import FIREBASE_CONFIG, SERVICE_ACCOUNT_KEY
from config import CONDITIONS, PARTICIPANTS_PER_CONDITION
import time

# Initialize Firebase Admin (for backend operations)
if not firebase_admin._apps:
    try:
        # Try to load from service account key
        if isinstance(SERVICE_ACCOUNT_KEY, dict) and SERVICE_ACCOUNT_KEY.get('project_id') != 'YOUR_PROJECT_ID':
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_CONFIG['databaseURL']
            })
        else:
            st.error("Firebase credentials not configured. Please update firebase_config.py")
    except Exception as e:
        st.error(f"Firebase Admin initialization error: {e}")

# Initialize Pyrebase (for client-side auth)
try:
    if FIREBASE_CONFIG['apiKey'] != 'YOUR_API_KEY':
        firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        auth_client = firebase.auth()
    else:
        auth_client = None
except Exception as e:
    st.error(f"Pyrebase initialization error: {e}")
    auth_client = None


def login_user(email: str, password: str) -> dict:
    """
    Log in a user with email and password.
    
    Returns:
        dict with 'success', 'user_id', 'token', 'message'
    """
    if not auth_client:
        return {'success': False, 'message': 'Firebase not configured'}
    
    try:
        # Authenticate user
        user = auth_client.sign_in_with_email_and_password(email, password)
        
        return {
            'success': True,
            'user_id': user['localId'],
            'token': user['idToken'],
            'email': email,
            'message': 'Login successful'
        }
    except Exception as e:
        error_message = str(e)
        if 'INVALID_PASSWORD' in error_message or 'EMAIL_NOT_FOUND' in error_message:
            return {'success': False, 'message': 'Invalid email or password'}
        elif 'TOO_MANY_ATTEMPTS' in error_message:
            return {'success': False, 'message': 'Too many attempts. Please try again later.'}
        else:
            return {'success': False, 'message': f'Login failed: {error_message}'}


def create_user(email: str, password: str) -> dict:
    """
    Create a new user account.
    
    Returns:
        dict with 'success', 'user_id', 'message'
    """
    if not auth_client:
        return {'success': False, 'message': 'Firebase not configured'}
    
    try:
        # Create user
        user = auth_client.create_user_with_email_and_password(email, password)
        
        # Automatically log them in
        login_result = login_user(email, password)
        
        if login_result['success']:
            # Assign condition and initialize user data
            user_id = login_result['user_id']
            assign_condition(user_id, email)
            
            return {
                'success': True,
                'user_id': user_id,
                'message': 'Account created successfully'
            }
        else:
            return login_result
            
    except Exception as e:
        error_message = str(e)
        if 'EMAIL_EXISTS' in error_message:
            return {'success': False, 'message': 'Email already registered. Please log in.'}
        elif 'WEAK_PASSWORD' in error_message:
            return {'success': False, 'message': 'Password should be at least 6 characters'}
        else:
            return {'success': False, 'message': f'Registration failed: {error_message}'}


def assign_condition(user_id: str, email: str) -> int:
    """
    Assign a user to a condition (balanced across 3 conditions).
    
    Returns:
        condition number (1, 2, or 3)
    """
    try:
        # Get reference to users
        ref = db.reference('users')
        
        # Count users in each condition
        all_users = ref.get() or {}
        
        condition_counts = {1: 0, 2: 0, 3: 0}
        for uid, user_data in all_users.items():
            if uid != user_id and 'condition' in user_data:
                condition = user_data['condition']
                if condition in condition_counts:
                    condition_counts[condition] += 1
        
        # Assign to condition with fewest users
        assigned_condition = min(condition_counts, key=condition_counts.get)
        
        # Check if condition is full
        if condition_counts[assigned_condition] >= PARTICIPANTS_PER_CONDITION:
            # Find next available condition
            for cond in [1, 2, 3]:
                if condition_counts[cond] < PARTICIPANTS_PER_CONDITION:
                    assigned_condition = cond
                    break
        
        # Save to database
        user_ref = ref.child(user_id)
        user_ref.update({
            'email': email,
            'condition': assigned_condition,
            'condition_name': CONDITIONS[assigned_condition],
            'assigned_date': time.time(),
            'sessions': {
                'arraylist': {'status': 'not_started'},
                'recursion': {'status': 'not_started'}
            }
        })
        
        return assigned_condition
        
    except Exception as e:
        st.error(f"Error assigning condition: {e}")
        # Default to condition 1 if error
        return 1


def get_user_data(user_id: str) -> dict:
    """
    Get user data from database.
    
    Returns:
        User data dict or None
    """
    try:
        ref = db.reference(f'users/{user_id}')
        return ref.get()
    except Exception as e:
        st.error(f"Error getting user data: {e}")
        return None


def update_user_data(user_id: str, data: dict):
    """Update user data in database."""
    try:
        ref = db.reference(f'users/{user_id}')
        ref.update(data)
    except Exception as e:
        st.error(f"Error updating user data: {e}")


def logout_user():
    """Log out the current user."""
    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def require_auth():
    """
    Decorator/function to require authentication.
    Call this at the start of pages that need login.
    
    Returns True if authenticated, False otherwise.
    """
    if 'user_id' not in st.session_state or not st.session_state.user_id:
        return False
    return True


def render_login_page():
    """Render the login/registration page."""
    st.title("🔐 Java Learning Study")
    st.write("Welcome! Please log in or create an account to participate.")
    
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if email and password:
                with st.spinner("Logging in..."):
                    result = login_user(email, password)
                
                if result['success']:
                    st.session_state.user_id = result['user_id']
                    st.session_state.email = result['email']
                    st.session_state.token = result['token']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.warning("Please enter email and password")
    
    with tab2:
        st.subheader("Create Account")
        st.info("You'll be randomly assigned to one of our study conditions.")
        
        new_email = st.text_input("Email", key="register_email")
        new_password = st.text_input("Password (min 6 characters)", type="password", key="register_password")
        new_password_confirm = st.text_input("Confirm Password", type="password", key="register_password_confirm")
        
        if st.button("Create Account", key="register_button"):
            if new_email and new_password and new_password_confirm:
                if new_password != new_password_confirm:
                    st.error("Passwords don't match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    with st.spinner("Creating account..."):
                        result = create_user(new_email, new_password)
                    
                    if result['success']:
                        st.session_state.user_id = result['user_id']
                        st.session_state.email = new_email
                        st.success("Account created! Redirecting...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(result['message'])
            else:
                st.warning("Please fill in all fields")
    
    st.write("---")
    st.caption("This is a research study. Your data will be kept confidential and used for research purposes only.")
