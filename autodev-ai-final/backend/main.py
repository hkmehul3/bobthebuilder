from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import re
import httpx

app = FastAPI(title="BobTheBuilder - Self-Healing Code System", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Watson Orchestrate config ────────────────────────────────────────────────
WXO_INSTANCE_URL   = os.getenv("WXO_INSTANCE_URL", "")
WXO_API_KEY        = os.getenv("WXO_API_KEY", "")
WXO_AGENT_ID       = os.getenv("WXO_AGENT_ID", "")
WXO_ENVIRONMENT_ID = os.getenv("WXO_ENVIRONMENT_ID", "")
IBM_IAM_URL        = "https://iam.cloud.ibm.com/identity/token"

# Thread cache for conversation continuity (in production, use Redis or similar)
_thread_cache = {}


# ─── Pydantic models ──────────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    error: str
    skill_level: str = "beginner"


# ─── IBM IAM token ────────────────────────────────────────────────────────────
async def get_bearer_token() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            IBM_IAM_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": WXO_API_KEY,
            },
            timeout=30,
        )
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail=f"IAM token error: {r.text}")
    return r.json()["access_token"]


# ─── Watson Orchestrate /v1/orchestrate/runs API ─────────────────────────────
async def call_orchestrate(message: str) -> str:
    """
    Call Watson Orchestrate using the correct /v1/orchestrate/runs endpoint.
    
    This endpoint:
    - Uses thread_id for conversation continuity
    - Requires specific message format: {"role": "user", "content": "..."}
    - Supports streaming (we use stream=true with timeout)
    - Returns responses in a specific format
    
    Based on official Watson Orchestrate API documentation.
    """
    token = await get_bearer_token()
    
    # Get or create thread_id for conversation continuity
    thread_id = _thread_cache.get("thread_id", "")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "IAM-API-KEY": WXO_API_KEY,  # Required by Watson Orchestrate
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Correct Watson Orchestrate endpoint
    url = f"{WXO_INSTANCE_URL}/v1/orchestrate/runs?stream=true&stream_timeout=120000&multiple_content=true"
    
    # Correct payload format
    payload = {
        "message": {
            "role": "user",
            "content": message
        },
        "agent_id": WXO_AGENT_ID
    }
    
    # Include thread_id if we have one (for conversation continuity)
    if thread_id:
        payload["thread_id"] = thread_id
    
    print(f"\n🚀 Calling Watson Orchestrate:")
    print(f"  URL: {url}")
    print(f"  Agent ID: {WXO_AGENT_ID}")
    print(f"  Thread ID: {thread_id if thread_id else '(new conversation)'}")
    print(f"  Message length: {len(message)} chars")
    
    async with httpx.AsyncClient() as client:
        r = await client.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )
    
    print(f"  Response status: {r.status_code}")
    
    if r.status_code not in (200, 201):
        error_detail = r.text[:500]
        print(f"  ❌ Error: {error_detail}")
        raise HTTPException(500, f"Watson Orchestrate error: {error_detail}")
    
    # Parse streaming response - Watson Orchestrate returns multiple JSON objects (NDJSON format)
    # Each line is a separate JSON object
    response_text = r.text
    print(f"\n📦 Raw response length: {len(response_text)} chars")
    print(f"  First 200 chars: {response_text[:200]}")
    
    # Split by newlines and parse each JSON object
    lines = response_text.strip().split('\n')
    print(f"  Number of JSON objects: {len(lines)}")
    
    all_data = []
    content_parts = []
    thread_id_found = None
    
    for i, line in enumerate(lines):
        if line.strip():
            try:
                obj = json.loads(line)
                all_data.append(obj)
                
                # Show first few and last few objects
                if i < 5 or i >= len(lines) - 5:
                    event_type = obj.get('event', 'unknown')
                    print(f"  Object {i+1} event: {event_type}")
                    # Show data structure for message.delta events
                    if event_type == 'message.delta' and 'data' in obj:
                        print(f"    data keys: {list(obj['data'].keys())}")
                
                # Extract thread_id if present
                if 'data' in obj and isinstance(obj['data'], dict):
                    if 'thread_id' in obj['data']:
                        thread_id_found = obj['data']['thread_id']
                    
                    # Look for content in various places
                    data_obj = obj['data']
                    
                    # Check for message content
                    if 'content' in data_obj:
                        content = data_obj['content']
                        if isinstance(content, str) and content.strip():
                            content_parts.append(content)
                    
                    # Check for delta content (streaming chunks)
                    if 'delta' in data_obj:
                        delta = data_obj['delta']
                        if isinstance(delta, dict) and 'content' in delta:
                            delta_content = delta['content']
                            if isinstance(delta_content, str) and delta_content.strip():
                                content_parts.append(delta_content)
                    
                    # Check for message object
                    if 'message' in data_obj:
                        message = data_obj['message']
                        if isinstance(message, dict) and 'content' in message:
                            msg_content = message.get('content')
                            if isinstance(msg_content, str) and msg_content.strip():
                                content_parts.append(msg_content)
                
            except json.JSONDecodeError as e:
                if i < 5:
                    print(f"  ⚠️ Could not parse line {i+1}: {e}")
                continue
    
    if not all_data:
        print(f"  ❌ No valid JSON objects found in response")
        raise HTTPException(500, f"Could not parse Watson Orchestrate response: {response_text[:500]}")
    
    print(f"\n🔍 Extraction results:")
    print(f"  Total events: {len(all_data)}")
    print(f"  Content parts found: {len(content_parts)}")
    if thread_id_found:
        print(f"  Thread ID: {thread_id_found}")
        _thread_cache["thread_id"] = thread_id_found
    
    # If we found content parts from streaming, combine them
    if content_parts:
        combined_content = "".join(content_parts)
        print(f"  ✅ Combined content length: {len(combined_content)} chars")
        print(f"  First 200 chars: {combined_content[:200]}")
        return combined_content
    
    # Try to find completed message in the events
    # Look for message.completed or run.completed events
    print(f"  ⚠️ No streaming content found, looking for completed message...")
    
    for obj in reversed(all_data):  # Start from end
        event_type = obj.get('event', '')
        
        if event_type in ['message.completed', 'run.completed', 'message.created']:
            print(f"  Found {event_type} event")
            data_obj = obj.get('data', {})
            
            # Try format from GitHub repo: result.data.message.content
            if 'result' in data_obj:
                result = data_obj['result']
                if isinstance(result, dict) and 'data' in result:
                    result_data = result['data']
                    if isinstance(result_data, dict) and 'message' in result_data:
                        message = result_data['message']
                        if isinstance(message, dict) and 'content' in message:
                            content = message['content']
                            if isinstance(content, list):
                                texts = [
                                    c.get('text', '')
                                    for c in content
                                    if isinstance(c, dict) and 'text' in c
                                ]
                                if texts:
                                    combined = '\n'.join(texts).strip()
                                    print(f"  ✅ Extracted from result.data.message.content (list)")
                                    print(f"  Content length: {len(combined)} chars")
                                    return combined
            
            # Try direct message.content
            if 'message' in data_obj:
                message = data_obj['message']
                if isinstance(message, dict) and 'content' in message:
                    content = message['content']
                    if isinstance(content, list):
                        texts = [
                            c.get('text', '')
                            for c in content
                            if isinstance(c, dict) and 'text' in c
                        ]
                        if texts:
                            combined = '\n'.join(texts).strip()
                            print(f"  ✅ Extracted from message.content (list)")
                            print(f"  Content length: {len(combined)} chars")
                            return combined
                    elif isinstance(content, str) and content.strip():
                        print(f"  ✅ Extracted from message.content (string)")
                        return content.strip()
    
    # Fallback: use the last object
    data = all_data[-1]
    print(f"  ⚠️ Could not find completed message, using last event")
    print(f"  Last event type: {data.get('event', 'unknown')}")
    print(f"  Last event keys: {list(data.keys())}")
    if 'data' in data:
        print(f"  Last event data keys: {list(data['data'].keys())}")
    
    # Save thread_id for next request
    if "thread_id" in data:
        _thread_cache["thread_id"] = data["thread_id"]
        print(f"  ✅ Saved thread_id: {data['thread_id']}")
    
    # Extract response content
    # Watson Orchestrate /runs endpoint returns different formats
    
    # Try format 1: Direct content field
    if "content" in data:
        content = data["content"]
        if isinstance(content, str):
            print(f"  ✅ Extracted from 'content' (string)")
            return content
        elif isinstance(content, list):
            # Join multiple content parts
            result = " ".join([str(c) for c in content])
            print(f"  ✅ Extracted from 'content' (list, {len(content)} items)")
            return result
    
    # Try format 2: message.content
    if "message" in data:
        message_obj = data["message"]
        if isinstance(message_obj, dict) and "content" in message_obj:
            print(f"  ✅ Extracted from 'message.content'")
            return message_obj["content"]
    
    # Try format 3: response field
    if "response" in data:
        response = data["response"]
        if isinstance(response, str):
            print(f"  ✅ Extracted from 'response' (string)")
            return response
        elif isinstance(response, dict) and "content" in response:
            print(f"  ✅ Extracted from 'response.content'")
            return response["content"]
    
    # Try format 4: output field
    if "output" in data:
        output = data["output"]
        if isinstance(output, str):
            print(f"  ✅ Extracted from 'output' (string)")
            return output
        elif isinstance(output, dict):
            if "content" in output:
                print(f"  ✅ Extracted from 'output.content'")
                return output["content"]
            if "text" in output:
                print(f"  ✅ Extracted from 'output.text'")
                return output["text"]
    
    # Try format 5: result field
    if "result" in data:
        result = data["result"]
        if isinstance(result, str):
            print(f"  ✅ Extracted from 'result' (string)")
            return result
        elif isinstance(result, dict) and "content" in result:
            print(f"  ✅ Extracted from 'result.content'")
            return result["content"]
    
    # If we can't extract a specific field, return the full JSON for debugging
    print(f"  ⚠️ Could not extract content, returning full response")
    print(f"  Full response (first 500 chars): {str(data)[:500]}")
    return json.dumps(data, indent=2)


# ─── Prompt builder ───────────────────────────────────────────────────────────
def build_prompt(error: str, skill: str) -> str:
    return f"""You are BobTheBuilder, an expert AI debugging agent built for IBM Bob Dev Day.
Analyze the following runtime error and return ONLY a valid JSON object — no markdown, no explanation, no extra text.

ERROR:
{error}

SKILL LEVEL OF DEVELOPER: {skill}

Return exactly this JSON structure (fill every field with real, specific content):

{{
  "error_type": "<detected error class, e.g. TypeError>",
  "context_scan": [
    {{"file": "src/main.py", "status": "scanned", "finding": "<specific finding>"}},
    {{"file": "src/utils.py", "status": "scanned", "finding": "<specific finding>"}},
    {{"file": "tests/test_main.py", "status": "scanned", "finding": "<specific finding>"}}
  ],
  "root_cause_chain": [
    "<step 1 of what went wrong>",
    "<step 2>",
    "<step 3>",
    "<step 4>",
    "<step 5 — the actual exception>"
  ],
  "adaptive_explanation": "<plain-English explanation tailored to {skill} level — be specific to THIS error>",
  "multi_file_fix": [
    {{
      "file": "src/utils.py",
      "change": "<what this fix does>",
      "before": "<original broken code>",
      "after": "<fixed code>"
    }},
    {{
      "file": "src/main.py",
      "change": "<what this fix does>",
      "before": "<original broken code>",
      "after": "<fixed code>"
    }},
    {{
      "file": "tests/test_main.py",
      "change": "<what this test covers>",
      "before": "# missing test",
      "after": "<actual test code>"
    }}
  ],
  "generated_tests": [
    "test_<name1>",
    "test_<name2>",
    "test_<name3>",
    "test_<name4>",
    "test_<name5>"
  ],
  "risk_analysis": {{
    "risk_score": "<percentage like 82%>",
    "risk_level": "<Low / Medium / High / Critical>",
    "blast_radius": "<what parts of the codebase are affected>",
    "impact": "<what breaks if this is not fixed>",
    "rollback_plan": "<how to undo the fix if something goes wrong>",
    "why_safe": "<why this fix is safe to apply>"
  }},
  "pr_draft": {{
    "title": "Fix <error_type>: <short description>",
    "summary": "<2-3 sentence PR description>",
    "checklist": [
      "<item1>",
      "<item2>",
      "<item3>",
      "<item4>"
    ]
  }}
}}"""


# ─── JSON parser ──────────────────────────────────────────────────────────────
def safe_parse(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"```$", "", raw, flags=re.MULTILINE)
    raw = raw.strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        raw = match.group(0)
    return json.loads(raw)


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def health():
    return {
        "status": "running",
        "project": "BobTheBuilder v3",
        "backend": "IBM Watson Orchestrate",
        "agent_id": WXO_AGENT_ID,
        "message": "Open /docs to test the API"
    }


@app.post("/analyze")
async def analyze(payload: AnalyzeRequest):
    if not payload.error.strip():
        raise HTTPException(400, "Error message cannot be empty")

    prompt = build_prompt(payload.error.strip(), payload.skill_level)
    raw = await call_orchestrate(prompt)

    try:
        result = safe_parse(raw)
    except Exception as e:
        raise HTTPException(500, f"JSON parse failed: {e} | Raw: {raw[:500]}")

    result["input_error"]    = payload.error
    result["skill_level"]    = payload.skill_level
    result["bob_usage_note"] = "Powered by IBM Watson Orchestrate + GPT-OSS 120B via Groq"

    return result