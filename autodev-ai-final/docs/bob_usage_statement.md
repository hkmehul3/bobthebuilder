# IBM Bob Usage Statement

We used IBM Bob as the intelligent development partner and repository-aware reasoning layer for BobTheBuilder. Bob helped shape the complete debugging workflow by analyzing how a developer moves from an error message to a safe production-ready fix.

In the project, Bob is used conceptually and practically across the following stages:

1. Understanding repository context and identifying files related to the error.
2. Creating a root cause chain that explains how the failure happened.
3. Generating a multi-file fix plan instead of a single isolated suggestion.
4. Producing regression tests to prevent the same bug from returning.
5. Creating a confidence score, risk analysis, and rollback plan.
6. Preparing a PR-ready title, summary, and checklist.

Bob's strength is its ability to understand intent, code relationships, and developer workflow. We used that capability to move beyond a simple AI error explainer and demonstrate a self-healing code system where Bob accelerates the entire debugging lifecycle.

If extended further, BobTheBuilder could connect Bob directly to a repository, generate actual patch files, run automated tests, and open pull requests through GitHub integration.
