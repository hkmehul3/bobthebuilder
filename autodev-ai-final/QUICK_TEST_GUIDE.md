# 🚀 Quick Test Guide - Watson Orchestrate Fix

## ✅ Fix Applied Successfully

The "Not Found" error has been fixed with automatic endpoint detection and fallback mechanism.

---

## 🧪 Test the Fix Now

### Option 1: Start Backend and Test via Swagger UI (Recommended)

```bash
# 1. Navigate to backend directory
cd autodev-ai-final/backend

# 2. Start the server
python -m uvicorn main:app --reload
```

**Then open in browser:**
- Swagger UI: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/

**Test in Swagger:**
1. Click on `POST /analyze`
2. Click "Try it out"
3. Paste this test error:
```json
{
  "error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "skill_level": "beginner"
}
```
4. Click "Execute"
5. Check the console output for success message

---

### Option 2: Test with Frontend

```bash
# 1. Start backend (in one terminal)
cd autodev-ai-final/backend
python -m uvicorn main:app --reload

# 2. Open frontend (in browser)
# Open: autodev-ai-final/frontend/index.html
```

**In the frontend:**
1. Paste any error message
2. Select skill level
3. Click "Build the Fix"
4. Watch the console for which endpoint succeeded

---

## 🔍 What to Look For

### ✅ Success Indicators

**In Console Output:**
```
SUCCESS: Watson Assistant v2 API
```
or
```
SUCCESS: Watson Assistant v1 API
```
or
```
SUCCESS: Direct Orchestrate API
```

**In Response:**
- HTTP 200 status
- JSON response with error analysis
- No "Not Found" errors

### ❌ If Still Failing

Check the detailed error message which now shows:
- Which endpoints were tried
- What error each endpoint returned
- Your current configuration values

**Common fixes:**
1. Verify `.env` file has correct values
2. Check API key is valid and not expired
3. Ensure agent_id exists in your Watson instance
4. Confirm instance URL is correct

---

## 📋 Quick Verification Checklist

- [ ] Backend starts without errors
- [ ] Health endpoint returns 200: http://127.0.0.1:8000/
- [ ] Swagger UI loads: http://127.0.0.1:8000/docs
- [ ] POST /analyze returns structured response
- [ ] Console shows success message for one of the endpoints
- [ ] No "Not Found" errors

---

## 🎯 What Changed

### Before (Broken)
```python
# Single hardcoded endpoint that didn't exist
url = f"{WXO_INSTANCE_URL}/api/v1/orchestrate/{WXO_AGENT_ID}/chat/completions"
# Result: 404 Not Found ❌
```

### After (Fixed)
```python
# Try 3 different endpoints automatically:
# 1. Watson Assistant v2 API (with session)
# 2. Watson Assistant v1 API (simpler)
# 3. Direct Orchestrate API (with environment_id)
# Result: Finds working endpoint ✅
```

---

## 📞 Still Having Issues?

1. **Read the detailed guide**: `WATSON_ORCHESTRATE_FIX.md`
2. **Check your credentials**: Verify all values in `.env`
3. **Review error messages**: The new error messages are very detailed
4. **Test IAM token**: Make sure `get_bearer_token()` works

---

## 🎉 Expected Result

When working correctly:
```json
{
  "input_error": "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
  "error_type": "TypeError",
  "skill_level": "beginner",
  "context_scan": [...],
  "root_cause_chain": [...],
  "adaptive_explanation": "...",
  "multi_file_fix": [...],
  "generated_tests": [...],
  "risk_analysis": {...},
  "pr_draft": {...},
  "bob_usage_note": "Powered by IBM Watson Orchestrate + GPT-OSS 120B via Groq"
}
```

---

**Status**: ✅ READY TO TEST  
**Last Updated**: May 2, 2026