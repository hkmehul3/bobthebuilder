# 3-Minute Demo Script

## 0:00–0:25 Hook
Developers do not just need another chatbot. They need a system that can move from broken code to a safe fix faster. BobTheBuilder is a self-healing code system powered by IBM Bob.

## 0:25–0:50 Problem
Today, when an error happens, developers copy logs, search files, ask AI for help, manually edit code, write tests, and prepare a PR. This is slow and risky.

## 0:50–2:15 Live Demo
Here is a runtime error: TypeError unsupported operand type for int and str.

I paste the error into BobTheBuilder and click Heal Codebase.

The system scans repository context, identifies the affected files, and builds a root cause chain. It explains that text input reached the arithmetic function without validation.

Now it generates a multi-file fix. It updates utils.py with input normalization, updates main.py to use validation, and generates regression tests.

It also produces risk intelligence: confidence score, risk level, blast radius, and rollback plan.

Finally, it creates a PR draft with title, summary, and checklist.

## 2:15–2:45 IBM Bob Usage
IBM Bob acts as the repo-aware reasoning layer. It helps understand code relationships, root cause, safe fixes, tests, and PR documentation.

## 2:45–3:00 Closing
BobTheBuilder transforms debugging from a manual task into an automated workflow. We did not build another AI chatbot. We built a self-healing development system that helps builders ship high-quality software faster.
