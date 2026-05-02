# BobTheBuilder — Self-Healing Code System

BobTheBuilder is a hackathon-ready proof-of-concept for the IBM Bob Dev Day Hackathon.

It demonstrates a developer workflow where a runtime error is converted into a structured repair plan:

**Error → Repo Context → Root Cause Chain → Multi-file Fix → Tests → Risk Analysis → PR Draft**

## Run Backend

```bash
cd backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## Run Frontend

Open:

```text
frontend/index.html
```

Paste this sample error:

```text
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Click **Heal Codebase**.

## Hackathon Positioning

We did not build another chatbot. We built a self-healing developer workflow powered by IBM Bob's repository-aware reasoning.

## IBM Bob Usage

IBM Bob is positioned as the repo-aware intelligence layer that helps analyze code context, identify root cause, generate patches, produce tests, and prepare PR-ready documentation.

For the POC, the backend returns structured demo output so judges can clearly see the complete workflow.
