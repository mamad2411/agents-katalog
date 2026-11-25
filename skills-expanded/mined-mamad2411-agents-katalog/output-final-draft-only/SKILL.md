---
name: output-final-draft-only
description: "Return only the finished draft when the user needs text ready for a downstream workflow."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["zero-preamble", "token-savings", "automation", "clean-output", "copy-paste", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Output Final Deliverable Only (Zero-Preamble Protocol) (AI Skill)

## Overview
Default AI behavior is to wrap every response in conversational packaging: an opening preamble (*"Sure! Here is the revised customer email you asked for:"*) and a polite sign-off (*"I hope this helps! Feel free to ask if you need further adjustments!"*).

When you are copying and pasting into email clients, CMS editors, or code files, this chatter forces you to manually select only the middle text, slowing you down and breaking automated pipelines.

The **Zero-Preamble Protocol** enforces negative output constraints, ensuring the AI outputs **100% pure deliverable content and zero chat filler**.

---

## Chat Bloat vs. Clean Deliverable Output

```
┌─────────────────────────────────────────────────────────────┐
│                 Chat Bloat vs. Clean Output                 │
│                                                             │
│  Chat Bloat (Standard AI Output):                           │
│  "Certainly! Here is the SQL query you requested:           │
│   ```sql                                                    │
│   SELECT * FROM users WHERE active = true;                  │
│   ```                                                       │
│   Let me know if you need to add indexes or join tables!"   │
│  ↳ Cannot be piped directly to CLI, requires manual cleanup │
│                                                             │
│  Zero-Preamble Output (Deliverable Only):                   │
│  ```sql                                                     │
│  SELECT * FROM users WHERE active = true;                   │
│  ```                                                        │
│  ↳ 1-Click Copy, Pipe-Ready, Zero Token Waste               │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Zero-Preamble Prompt Templates

### Pattern 1: The Raw Text Deliverable (Emails, Memos, Articles)

```markdown
Draft a response to [SITUATION / EMAIL].

Strict Output Constraints:
- Output the final email text ONLY.
- Do NOT include conversational greetings to me ("Here is your draft", "Sure thing").
- Do NOT include conversational sign-offs ("Let me know if you'd like changes").
- Begin your response immediately with the email subject line.
```

---

### Pattern 2: The Raw Code & Terminal Snippet Directive
Use for CLI commands, SQL queries, or configuration scripts:

```markdown
Write a bash one-liner to [TASK: e.g. Find and compress all .log files older than 30 days].

Output Rules:
- Provide ONLY the raw bash code block.
- Zero introductory explanation or concluding commentary.
```

---

### Pattern 3: The Automated Pipeline / JSON Strict Mode

```markdown
Convert this address string into structured JSON: [PASTE ADDRESS].

Output Rules:
- Output ONLY valid, raw JSON.
- No markdown code fences (```json), no preambles, no trailing text.
```

---

## Real-World Case Study

### Scenario: Fast Slack Status Update for Standup

#### With Chat Bloat (Manual Edit Required)
> **AI Output**:
> *"Here is a quick status update you can share with your team on Slack:*
> 
> *Yesterday: Finished the Stripe integration tests.*
> *Today: Working on the checkout webhook handler.*
> *Blockers: None at this time.*
> 
> *I hope this works well for your standup meeting! Have a great day!"*
> 
> *(User has to carefully highlight only lines 3-5 on their mobile screen).*

#### With Zero-Preamble Protocol
> **AI Output**:
> `Yesterday: Finished Stripe integration tests.`  
> `Today: Building checkout webhook handler.`  
> `Blockers: None.`

*(User clicks "Copy" and pastes directly into Slack in 1 second).*

---

## Quick Negative Constraint Snippets to Copy-Paste

| Need | Copy-Paste Constraint |
| :--- | :--- |
| **No Introductory Fluff** | *"Start immediately on line 1 with the content; no preamble."* |
| **No Friendly Sign-Offs** | *"Do not write closing remarks or offers to help."* |
| **Code Only** | *"Output code block only; no markdown commentary."* |
| **JSON Only** | *"Return pure parseable JSON object only."* |
