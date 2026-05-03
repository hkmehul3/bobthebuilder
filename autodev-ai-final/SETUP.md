# 🚀 Setup Guide - BobTheBuilder

Complete step-by-step setup instructions for BobTheBuilder.

---

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] IBM Cloud account
- [ ] Watson Orchestrate instance created
- [ ] Watson Orchestrate agent configured
- [ ] IBM Cloud API key generated

---

## 🔧 Step 1: IBM Cloud Setup

### 1.1 Create Watson Orchestrate Instance

1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Navigate to **Catalog** → **AI / Machine Learning**
3. Select **Watson Orchestrate**
4. Click **Create**
5. Wait for instance to be provisioned
6. **Copy the Instance URL** (you'll need this for `.env`)

### 1.2 Create an Agent

1. Open your Watson Orchestrate instance
2. Go to **Agents** section
3. Click **Create Agent**
4. Configure your agent:
   - Name: `BobTheBuilder` (or your choice)
   - Description: Error analysis assistant
   - Configure skills and capabilities
5. **Copy the Agent ID** from agent settings

### 1.3 Get Environment ID

1. In Watson Orchestrate console
2. Go to **Settings** → **Environment**
3. **Copy the Environment ID**

### 1.4 Generate API Key

1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Click **Manage** → **Access (IAM)**
3. Select **API keys** from left menu
4. Click **Create**
5. Name: `BobTheBuilder-API-Key`
6. **Copy the API key** (you won't see it again!)

---

## 💻 Step 2: Local Setup

### 2.1 Clone Repository

```bash
git clone <your-repo-url>
cd autodev-ai-final
```

### 2.2 Set Up Python Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
```

### 2.3 Install Dependencies

```bash
# Make sure venv is activated
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages:
- fastapi
- uvicorn
- httpx
- pydantic
- python-dotenv

---

## 🔐 Step 3: Configure Environment Variables

### 3.1 Create .env File

```bash
# In the backend directory
# Copy the example file
cp .env.example .env

# Or create manually
# Windows:
type nul > .env
# macOS/Linux:
touch .env
```

### 3.2 Edit .env File

Open `backend/.env` in your text editor and add:

```env
WXO_INSTANCE_URL=https://api.eu-gb.watson-orchestrate.cloud.ibm.com/instances/YOUR_INSTANCE_ID
WXO_API_KEY=YOUR_IBM_CLOUD_API_KEY
WXO_AGENT_ID=YOUR_AGENT_ID
WXO_ENVIRONMENT_ID=YOUR_ENVIRONMENT_ID
```

### 3.3 Fill in Your Values

Replace the placeholders with values from Step 1:

| Variable | Where to Find It |
|----------|------------------|
| `WXO_INSTANCE_URL` | IBM Cloud → Watson Orchestrate → Instance URL |
| `WXO_API_KEY` | IBM Cloud → Manage → Access (IAM) → API keys |
| `WXO_AGENT_ID` | Watson Orchestrate Console → Agent Settings |
| `WXO_ENVIRONMENT_ID` | Watson Orchestrate Console → Environment Settings |

### 3.4 Verify .env File

```bash
# Check file exists and has content
# Windows:
type .env
# macOS/Linux:
cat .env
```

You should see all 4 variables with your actual values (not placeholders).

---

## ▶️ Step 4: Start the Application

### 4.1 Start Backend Server

```bash
# Make sure you're in backend directory with venv activated
cd backend
python -m uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 4.2 Verify Backend is Running

Open your browser and go to:
- **Health Check**: http://127.0.0.1:8000/
- **API Docs**: http://127.0.0.1:8000/docs

You should see:
- Health check returns JSON with status
- Swagger UI loads successfully

### 4.3 Open Frontend

**Option 1: Direct File**
```bash
# Simply open in browser
# Windows:
start frontend/index.html
# macOS:
open frontend/index.html
# Linux:
xdg-open frontend/index.html
```

**Option 2: Local Server** (recommended)
```bash
# In a new terminal, from project root
cd frontend
python -m http.server 8080
```

Then open: http://localhost:8080

---

## ✅ Step 5: Test the Setup

### 5.1 Test via Swagger UI

1. Go to http://127.0.0.1:8000/docs
2. Click on **POST /analyze**
3. Click **Try it out**
4. Enter test data:
   ```json
   {
     "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
     "skill_level": "beginner"
   }
   ```
5. Click **Execute**
6. Check response (should be HTTP 200 with JSON)

### 5.2 Test via Frontend

1. Open frontend (http://localhost:8080 or index.html)
2. Paste error message:
   ```
   TypeError: unsupported operand type(s) for +: 'int' and 'str'
   ```
3. Select skill level: **Beginner**
4. Click **🛠️ Build the Fix**
5. Wait for response (should see analysis results)

### 5.3 Check Backend Logs

In your backend terminal, you should see:
```
🚀 Calling Watson Orchestrate:
  URL: https://api.eu-gb.watson-orchestrate.cloud.ibm.com/...
  Agent ID: 428aca44-...
  Thread ID: (new conversation)
  Response status: 200

🔍 Extraction results:
  Total events: 955
  Content parts found: X
  ✅ Extracted from result.data.message.content
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Activate venv
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Missing env vars"

**Solution:**
```bash
# Check .env file exists
ls backend/.env  # Should show the file

# Check .env has content
cat backend/.env  # Should show 4 variables

# Verify no typos in variable names
```

### Issue: "401 Unauthorized"

**Solution:**
```bash
# Verify API key is correct
# Generate new API key from IBM Cloud if needed
# Update WXO_API_KEY in .env
```

### Issue: "404 Not Found"

**Solution:**
```bash
# Verify instance URL includes /instances/{id}
# Verify agent ID is correct
# Check Watson Orchestrate console
```

### Issue: Frontend can't connect

**Solution:**
```bash
# Ensure backend is running on port 8000
# Check http://127.0.0.1:8000/ works
# Check browser console for CORS errors
```

---

## 📝 Quick Reference

### Start Backend
```bash
cd backend
venv\Scripts\activate  # or source venv/bin/activate
python -m uvicorn main:app --reload
```

### Start Frontend
```bash
cd frontend
python -m http.server 8080
```

### View Logs
- Backend logs: Terminal where uvicorn is running
- Frontend logs: Browser Developer Console (F12)

### Stop Services
- Backend: Press `Ctrl+C` in terminal
- Frontend: Press `Ctrl+C` in terminal (if using http.server)

---

## 🎯 Next Steps

After successful setup:

1. ✅ Test with different error types
2. ✅ Try different skill levels (beginner/intermediate/expert)
3. ✅ Review the generated fixes and tests
4. ✅ Check risk analysis output
5. ✅ Explore the PR draft feature

---

## 📞 Need Help?

If you encounter issues:

1. Check this troubleshooting section
2. Review backend console logs
3. Verify all environment variables
4. Check IBM Watson Orchestrate console
5. Ensure agent is active and responding

---

**Setup Complete!** 🎉

You're now ready to use BobTheBuilder for intelligent error analysis!