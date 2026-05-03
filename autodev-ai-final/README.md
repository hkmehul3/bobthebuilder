# 🤖 BobTheBuilder - AI-Powered Code Error Analysis

An intelligent error analysis system powered by IBM Watson Orchestrate that provides comprehensive debugging assistance, multi-file fixes, and risk analysis.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- IBM Watson Orchestrate account with API access
- Modern web browser

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd autodev-ai-final
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
# Create .env file
```

Add the following environment variables to `.env`:

```env
# Watson Orchestrate Configuration
WXO_INSTANCE_URL=https://api.eu-gb.watson-orchestrate.cloud.ibm.com/instances/YOUR_INSTANCE_ID
WXO_API_KEY=YOUR_IBM_CLOUD_API_KEY
WXO_AGENT_ID=YOUR_AGENT_ID
WXO_ENVIRONMENT_ID=YOUR_ENVIRONMENT_ID
```

#### How to Get These Values:

1. **WXO_INSTANCE_URL**
   - Go to IBM Cloud Console → Watson Orchestrate
   - Copy your instance URL (includes `/instances/{instance_id}`)

2. **WXO_API_KEY**
   - IBM Cloud Console → Manage → Access (IAM) → API keys
   - Create a new API key or use existing one
   - Copy the API key value

3. **WXO_AGENT_ID**
   - Watson Orchestrate Console → Your Agent
   - Copy the Agent ID from agent settings
   - Example: `428aca44-d8f0-41cd-b2d2-2c5b9b4dfc47`

4. **WXO_ENVIRONMENT_ID**
   - Watson Orchestrate Console → Environment settings
   - Copy the Environment ID
   - Example: `dbeb9543-d1f6-4e61-99bf-9fa1557787f9`

### 4. Start the Backend Server

```bash
# Make sure you're in the backend directory with venv activated
python -m uvicorn main:app --reload
```

The backend will start at: `http://127.0.0.1:8000`

### 5. Open the Frontend

Simply open `frontend/index.html` in your web browser.

Or use a local server:
```bash
# From the frontend directory
python -m http.server 8080
# Then open http://localhost:8080
```

---

## 📋 API Documentation

### Swagger UI

Once the backend is running, access the interactive API documentation:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Main Endpoint

**POST** `/analyze`

**Request Body:**
```json
{
  "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "skill_level": "beginner"
}
```

**Skill Levels:**
- `beginner` - Simple explanations
- `intermediate` - Technical details
- `expert` - Advanced solutions

**Response:**
```json
{
  "error_type": "TypeError",
  "context_scan": [...],
  "root_cause_chain": [...],
  "adaptive_explanation": "...",
  "multi_file_fix": [...],
  "generated_tests": [...],
  "risk_analysis": {...},
  "pr_draft": {...},
  "input_error": "...",
  "skill_level": "beginner",
  "bob_usage_note": "Powered by IBM Watson Orchestrate"
}
```

---

## 🧪 Testing

### Test via Swagger UI

1. Go to http://127.0.0.1:8000/docs
2. Click on `POST /analyze`
3. Click "Try it out"
4. Enter a test error message
5. Click "Execute"

### Test via Frontend

1. Open `frontend/index.html`
2. Paste any error message
3. Select skill level
4. Click "🛠️ Build the Fix"

### Example Test Errors

```python
# TypeError
"TypeError: unsupported operand type(s) for +: 'int' and 'str'"

# ZeroDivisionError
"ZeroDivisionError: division by zero"

# IndexError
"IndexError: list index out of range"

# KeyError
"KeyError: 'username'"

# AttributeError
"AttributeError: 'NoneType' object has no attribute 'split'"
```

---

## 🏗️ Project Structure

```
autodev-ai-final/
├── backend/
│   ├── .env                 # Environment variables (create this)
│   ├── main.py             # FastAPI backend
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html          # Web interface
├── docs/                   # Additional documentation
├── sample_repo/            # Sample code for testing
└── README.md              # This file
```

---

## 🔧 Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error**: `Missing env vars`
```bash
# Solution: Check .env file exists and has all required variables
cat backend/.env  # On Windows: type backend\.env
```

### API Returns 401 Unauthorized

**Problem**: Invalid API key
```bash
# Solution: Verify your WXO_API_KEY in .env
# Generate a new API key from IBM Cloud Console if needed
```

### API Returns 404 Not Found

**Problem**: Incorrect instance URL or agent ID
```bash
# Solution: Verify WXO_INSTANCE_URL and WXO_AGENT_ID in .env
# Check IBM Watson Orchestrate console for correct values
```

### No Response from Watson Orchestrate

**Problem**: Agent not responding
```bash
# Solution: 
# 1. Check Watson Orchestrate console - is the agent active?
# 2. Verify agent_id is correct
# 3. Check backend console logs for detailed error messages
```

### Frontend Can't Connect to Backend

**Problem**: CORS or connection error
```bash
# Solution:
# 1. Ensure backend is running on http://127.0.0.1:8000
# 2. Check browser console for errors
# 3. Try accessing http://127.0.0.1:8000/docs directly
```

---

## 📊 Features

### ✅ Intelligent Error Analysis
- Detects 9+ error types automatically
- Context-aware code scanning
- Root cause chain analysis

### ✅ Multi-File Fixes
- Before/after code snippets
- Multiple file modifications
- Test generation

### ✅ Risk Assessment
- Risk score calculation
- Impact analysis
- Rollback planning

### ✅ Adaptive Explanations
- Beginner-friendly language
- Intermediate technical details
- Expert-level solutions

### ✅ PR-Ready Output
- Auto-generated PR titles
- Detailed descriptions
- Implementation checklists

---

## 🔐 Security Notes

- **Never commit `.env` file** to version control
- Keep your API keys secure
- Rotate API keys regularly
- Use environment-specific configurations

---

## 📝 Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `WXO_INSTANCE_URL` | ✅ | Watson Orchestrate instance URL | `https://api.eu-gb.watson-orchestrate.cloud.ibm.com/instances/...` |
| `WXO_API_KEY` | ✅ | IBM Cloud API key | `` |
| `WXO_AGENT_ID` | ✅ | Watson Orchestrate agent ID | ` |
| `WXO_ENVIRONMENT_ID` | ✅ | Watson Orchestrate environment ID | `` |

---

## 🎯 Usage Examples

### Example 1: Simple TypeError

**Input:**
```json
{
  "error": "TypeError: can only concatenate str (not \"int\") to str",
  "skill_level": "beginner"
}
```

**Output:** Beginner-friendly explanation with simple fixes

### Example 2: Complex Error

**Input:**
```json
{
  "error": "AttributeError: 'NoneType' object has no attribute 'get'",
  "skill_level": "expert"
}
```

**Output:** Deep analysis with architectural recommendations

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend console logs for detailed errors
3. Verify all environment variables are correct
4. Check IBM Watson Orchestrate console for agent status

---

## 📄 License

[Your License Here]

---

## 🙏 Acknowledgments

- Built with IBM Watson Orchestrate
- Powered by FastAPI
- Frontend using vanilla JavaScript

---

**Last Updated**: May 2, 2026  
**Version**: 3.0.0  
**Status**: ✅ Production Ready
