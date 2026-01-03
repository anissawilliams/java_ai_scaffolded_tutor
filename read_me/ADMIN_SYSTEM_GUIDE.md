# Admin System Documentation

## 🔧 Admin Access for Testing All Conditions

As a researcher, you need to test all three experimental conditions without being randomly assigned. The admin system lets you do this!

## Setup

### Step 1: Add Your Email as Admin

Edit `admin_module.py`:

```python
# Admin emails - add your email(s) here
ADMIN_EMAILS = [
    "your-email@university.edu",  # Replace with your actual email
    "researcher@university.edu",
    "professor@university.edu",
    # Add more admin emails as needed
]
```

### Step 2: Login with Admin Email

When you create an account or login with an email in the `ADMIN_EMAILS` list, you'll automatically get admin access.

## Admin Dashboard

### What You See

Instead of the regular student dashboard, admins see:

```
🔧 Admin Dashboard

Welcome, your-email@university.edu (Admin)

As an admin, you can test all three experimental conditions.

┌─────────────────────────────────────────────────────┐
│  Condition 1        │  Condition 2        │  Condition 3  │
│  Character-Based    │  Non-Character      │  Direct Chat  │
│  Scaffolded         │  Scaffolded         │  (Control)    │
│  [Test Condition 1] │  [Test Condition 2] │  [Test Condition 3] │
└─────────────────────────────────────────────────────┘

🛠️ Admin Tools
- Data Export
- User Management Statistics

Test Sessions
- ArrayList (Easy)     [Start Test]
- Recursion (Hard)     [Start Test]
```

### How to Test

1. **Select a Condition**: Click one of the three "Test Condition X" buttons
2. **Start a Session**: Click "Start Test" on ArrayList or Recursion
3. **Go Through the Flow**: Complete the learning session normally
4. **Try All Conditions**: Go back and test the other conditions

## Key Features

### 1. Condition Selection

Unlike students who are randomly assigned, you can choose which condition to test:

- **Condition 1**: Character selection → Character-based scaffolding → Visuals → Practice
- **Condition 2**: Generic tutor → Same scaffolding → Same visuals → No character
- **Condition 3**: Plain chat → No scaffolding → No visuals → Just Q&A

### 2. Data Isolation

**Admin test data is NOT saved to the research database!**

When you test as admin:
- ✅ All features work normally
- ✅ You see everything students see
- ❌ Your data is NOT saved to Firebase
- ❌ You don't pollute the research data

You'll see this indicator during testing:
```
🔧 Admin Test Mode - Testing Condition 2 - Data will not be saved
```

### 3. Switch Between Conditions

You can test all three conditions:

```
Test Condition 1 → Complete session → Back to dashboard
    ↓
Test Condition 2 → Complete session → Back to dashboard  
    ↓
Test Condition 3 → Complete session → Done!
```

### 4. Admin Tools

**User Management Statistics:**
- Total students enrolled
- Students per condition (balanced assignment)
- Completion rates

**Data Export:**
- Quick link to export dashboard
- Access via `?admin=true` URL parameter

## Testing Workflow

### Quick Test (Each Condition)

```
1. Login with admin email
2. Click "Test Condition 1"
3. Click "Start Test" on ArrayList
4. Choose a character (Condition 1 only)
5. Have a 2-3 minute conversation
6. See the scaffolding in action
7. Complete quiz
8. Complete survey
9. Back to dashboard
10. Repeat for Conditions 2 and 3
```

### Full Test (Thorough)

```
1. Test Condition 1:
   - Try different characters
   - Test all scaffold steps
   - Verify visual diagrams appear
   - Complete full 10-minute session
   - Check quiz works
   - Check survey works
   
2. Test Condition 2:
   - Verify no character selection
   - Verify same scaffolding structure
   - Verify visuals still appear
   - Complete session
   
3. Test Condition 3:
   - Verify no scaffolding
   - Verify direct chat interface
   - Verify no visuals
   - Test Q&A functionality
```

## What to Check When Testing

### Condition 1 (Character-Based)

- [ ] Character selection screen appears
- [ ] Character personality in responses
- [ ] Step 1: Character gives metaphor
- [ ] Step 2: Student shares metaphor
- [ ] Step 3: Visual diagram + code appears
- [ ] Step 4: Usage examples
- [ ] Step 5: Practice
- [ ] Character voice consistent throughout
- [ ] Toast notifications for step advancement

### Condition 2 (Non-Character)

- [ ] NO character selection
- [ ] Generic tutor voice
- [ ] Same 5 scaffolding steps
- [ ] Visual diagram + code appears
- [ ] Same structure as Condition 1
- [ ] No personality quirks
- [ ] Professional teaching tone

### Condition 3 (Direct Chat)

- [ ] NO character selection
- [ ] NO scaffolding steps
- [ ] NO visual diagrams
- [ ] Simple chat interface
- [ ] Direct question answering
- [ ] Like ChatGPT for Java
- [ ] No step progression

## Access Data Export

### Option 1: From Admin Dashboard

Click "Go to Data Export" in Admin Tools

### Option 2: URL Parameter

Add `?admin=true` to your URL:
```
https://your-app.streamlit.app/?admin=true
```

### What You Can Export

**Summary CSV:**
- One row per completed session
- User ID, condition, topic, scores
- For statistical analysis

**Detailed CSV:**
- One row per message
- Complete conversation logs
- For qualitative coding

## Admin vs Student Experience

| Feature | Student | Admin |
|---------|---------|-------|
| **Dashboard** | Regular progress | Condition selector |
| **Condition** | Random assignment | Manual selection |
| **Data Saved** | ✅ Yes | ❌ No (test mode) |
| **Can Test All** | ❌ No | ✅ Yes |
| **Statistics** | ❌ No | ✅ Yes |
| **Export Data** | ❌ No | ✅ Yes |
| **Indicator** | None | "Admin Test Mode" banner |

## Adding More Admins

Just add their emails to the list:

```python
ADMIN_EMAILS = [
    "researcher1@university.edu",
    "researcher2@university.edu",
    "professor@university.edu",
    "ta@university.edu",
]
```

**Important:** Emails are case-insensitive, so "User@Email.com" and "user@email.com" are treated the same.

## Removing Admin Access

Remove the email from `ADMIN_EMAILS` list. The user will see the regular student dashboard on next login.

## Security Notes

### ✅ Good Practices

- Only add trusted researchers to admin list
- Don't share admin emails publicly
- Test thoroughly before student deployment
- Monitor admin access logs (if needed)

### ❌ Don't Do This

- Don't put admin emails in config files that go to Git
- Don't give admin access to students
- Don't test with real student accounts

## Troubleshooting

### "I'm not seeing the admin dashboard"

**Check:**
1. Is your email exactly as entered in `ADMIN_EMAILS`?
2. Did you restart the app after adding your email?
3. Are you logged in with that email?

**Solution:**
```python
# Debug: Add this temporarily to admin_module.py
print(f"Checking admin: {email}")
print(f"Is admin: {is_admin(email)}")
```

### "My test data is showing up in exports"

**This shouldn't happen!** The `is_admin_test` flag prevents data saving.

**Check:**
- Look for "Admin Test Mode" banner when testing
- Verify `st.session_state.is_admin_test` is True
- Check database - admin data should be in `admins/` not `users/`

### "I can't switch conditions"

**Solution:**
Go back to dashboard by completing the session or clicking the back button.

### "Students can see admin dashboard"

**Check:**
- Is the student's email accidentally in `ADMIN_EMAILS`?
- Remove it if so

## Example Testing Session

```python
# 1. Login
Email: researcher@university.edu
Password: ••••••••

# 2. See admin dashboard
✅ "Welcome, researcher@university.edu (Admin)"
✅ Three condition buttons visible
✅ Statistics showing: "Total Students: 5"

# 3. Test Condition 1
Click "Test Condition 1"
Click "Start Test" on ArrayList
Choose "Batman" character
🔧 Banner: "Admin Test Mode - Testing Condition 1"

# 4. Have conversation
You: "What's an ArrayList?"
Batman: "Think of it as my utility belt. It starts with..."
[5-step scaffolding proceeds normally]

# 5. Complete quiz & survey
[All works normally, no data saved]

# 6. Back to dashboard
✅ Can now test Condition 2 or 3

# 7. Test other conditions
Repeat for Conditions 2 and 3
```

## Summary

The admin system lets you:
- ✅ Test all three conditions
- ✅ Switch between conditions freely
- ✅ See exactly what students see
- ✅ Access data export tools
- ✅ Monitor study progress
- ❌ Without polluting research data

Perfect for testing, debugging, and demonstrating the system! 🎯
