---
name: capture-learning
description: Capture a reusable lesson after a verified bug fix, user correction, non-obvious discovery, recurring failure, or successful procedure. Search first, then call royo-learn. Capturing never publishes or changes agent behavior.
license: MIT
metadata:
  author: RoyoTech
  version: "3.0.0"
  mcp_profile: agent
---

# Capture Learning

## Use when

- the user corrects the agent;
- a non-obvious bug is fixed;
- a failed approach reveals a prevention rule;
- a procedure succeeds repeatedly;
- a tool limitation is discovered;
- the same explanation is being repeated;
- a significant task ends with a reusable lesson.

Do not use for routine progress or a session dump.

## Workflow

1. Search `learning_search` using the central terms.
2. Search Engram through the same tool when useful.
3. Decide whether there is an atomic, reusable lesson.
4. Separate direct observation from interpretation.
5. Gather only necessary evidence.
6. Call `learning_capture`.
7. Do not curate or publish in the same step unless the user explicitly requests the full cycle and evidence is sufficient.

## Required quality

The candidate must contain:

- minimal context;
- direct observation;
- reusable lesson;
- procedure;
- limits;
- confidence;
- evidence level;
- retrieval terms;
- source actor/session.

Never include private chain-of-thought, secrets, credentials, personal data, or raw conversation history.

## Outcome

If no lesson qualifies, state `NO_REUSABLE_LEARNING` and do not call capture.
