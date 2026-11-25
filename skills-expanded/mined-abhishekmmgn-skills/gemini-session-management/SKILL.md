---
name: gemini-session-management
description: strategies for managing agent sessions, handling conversation history (events), and implementing compaction (summarization/truncation) to prevent context overflow.
---

# Gemini Session Management Strategies

## Goal
Manage the "Session"—the turn-by-turn record of a conversation—to ensure the agent maintains immediate context without exceeding token limits or incurring high latency.

## Core Concepts

### 1. The Session Object
* **Definition:** A stateful container for a single, continuous conversation with a specific user. It isolates data so one user never sees another's context.
* **Components:**
    * **Events:** The chronological log of interactions (User Input, Agent Response, Tool Calls, Tool Outputs).
    * **State:** A structured "scratchpad" for temporary working memory (e.g., items in a shopping cart) that persists only for the session duration.

## Compaction Strategies (Managing Long Context)
As conversations grow, they risk "context rot" (model forgetting early details) and high latency. Use these strategies to manage history:

### Strategy A: Sliding Window (Truncation)
* **Mechanism:** Keep only the last $N$ turns (e.g., last 10 messages). Discard everything older.
* **Best For:** Simple, reactive agents where long-term history doesn't matter.
* **Implementation:**
    ```python
    # Example logic
    if len(history) > 10:
        history = history[-10:]
    ```

### Strategy B: Recursive Summarization
* **Mechanism:** Periodically use an LLM to summarize the oldest part of the conversation and replace the raw messages with that summary.
* **Structure:**
    1.  **System Prompt:** (Static instructions)
    2.  **Summary:** "Previously, the user asked about X and we determined Y..."
    3.  **Recent History:** (Last 5-10 verbatim messages)
* **Trigger:** Run this process asynchronously in the background when the turn count exceeds a threshold (e.g., every 5 turns).

## Production Best Practices
* **Async Processing:** Never block the user while saving the session. Upload context to storage (database) as a background event after the response is sent.
* **PII Redaction:** Always redact sensitive data (names, credit cards) *before* writing the session to persistent storage.
* **Immutability:** Treat the chronological order of events as immutable to ensure data integrity.
