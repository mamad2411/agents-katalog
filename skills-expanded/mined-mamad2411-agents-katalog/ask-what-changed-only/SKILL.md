---
name: ask-what-changed-only
description: "Request only changed lines or sentences and their relevant context when reviewing an update."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["diff-prompting", "delta-updates", "token-savings", "code-editing", "copywriting", "efficiency"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI for Changes Only (The Delta/Diff Protocol) (AI Skill)

## Overview
When asking an AI to tweak a sentence in a 1,500-word article or fix one function in a 400-line script, default model behavior is to regenerate the **entire document from start to finish**. 

This creates two major problems:
1. **Severe Token Waste**: Generates thousands of unnecessary output tokens ($$$ and slow generation time).
2. **Review Nightmare**: You have to re-read the entire document just to find what tiny phrase or line actually changed.

The **Delta / Diff Protocol** instructs the model to output **only the exact modified chunks**, with clear before-and-after references or standard Git-style diffs.

---

## Full Regeneration vs. Delta Output

```
┌─────────────────────────────────────────────────────────────┐
│                 Full Rewrite vs. Delta Output               │
│                                                             │
│  Full Document Regeneration:                                │
│  • 1,200 tokens generated                                   │
│  • 25 seconds wait time                                     │
│  • User must manually hunt for changes                      │
│                                                             │
│  Delta / Diff Output:                                       │
│  • 85 tokens generated (93% token reduction)                │
│  • 2 seconds generation time                                │
│  • Visual instant clarity on what changed                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Delta Prompt Templates

### Pattern 1: The Unified Diff Directive (Code & Configs)
Use this for codebases, YAML, JSON, or configuration files:

```markdown
Here is my code file: [PASTE CODE].

Task: [DESCRIBE THE REFACTOR / FIX].

Output Rules:
1. Do NOT reprint the entire file.
2. Provide ONLY a standard unified `diff` block showing `-` for removed lines and `+` for added lines.
3. Include 2 lines of unchanged context above and below each modification.
```

---

### Pattern 2: The "Before vs. After" Snippet (Text & Copywriting)
Use this for essays, contracts, emails, and articles:

```markdown
Here is my draft: [PASTE DRAFT].

Task: [MAKE THIS TONE MORE CONCISE / FIX GRAMMAR].

Output Rules:
- Do NOT rewrite the entire draft.
- List ONLY the specific sentences you changed.
- Format each change as:
  **Original**: "[Old sentence]"
  **Revised**: "[New sentence]"
  **Reason**: [1-sentence rationale for the change]
```

---

## Real-World Examples

### Example 1: Fixing a Single Backend Route

#### Wasteful Full Rewrite (300+ Lines Generated)
> *AI spits out the entire 350-line Flask server file just to change an HTTP status code from 200 to 201.*

#### Unified Diff Output (15 Lines Generated)
```diff
@@ -42,7 +42,7 @@ def create_user_subscription():
     if not plan_id:
         return jsonify({"error": "Missing plan_id"}), 400
 
     subscription = billing_service.subscribe(user_id, plan_id)
-    return jsonify(subscription.to_dict()), 200
+    return jsonify(subscription.to_dict()), 201
```

---

### Example 2: Copywriting Tone Edit

#### Delta Output for Article Edit
> **User Prompt**:
> *"Make paragraph 3 of my blog post punchier. Show ONLY the before and after."*

**AI Response**:
> **Original**:
> *"It is widely believed by many industry practitioners that when you deploy software on Fridays, you are significantly increasing the probability of encountering weekend outages."*
>
> **Revised**:
> *"Deploying on Friday is an open invitation to a ruined weekend."*
>
> **Reason**: Cut 21 filler words, switched from passive voice to an active, punchy hook.

---

## When to Use Full Rewrite vs. Delta Output

| Scenario | Preferred Mode |
| :--- | :--- |
| **Short text ($< 150$ words)** | Full rewrite is fine. |
| **Long documents ($> 500$ words)** | **Delta mode** (Before/After snippets). |
| **Production code files** | **Unified diff** mode. |
| **First draft creation** | Full generation. |
| **Iterative polishing / rounds 2 & 3** | **Delta mode strictly enforced**. |
