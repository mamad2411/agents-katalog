---
name: whiteboard-curate-suggest
description: When an insight, decision, or checklist with lasting value comes up during a conversation, suggest saving it to the library, and on the user's consent register it in Curated Knowledge via knowledge_promote.
allowed_tools:
  - knowledge_promote
  - opsidian_read
  - opsidian_search
execution_mode: inline
examples:
  - "Should I save what we just organized to the library?"
  - "Save this for me."
  - "This seems worth reusing next time."
---

# Whiteboard: Curate Suggest — Suggest saving content with lasting value

When content with lasting value comes up during a conversation, suggest **saving it to the library** to the user, or run `knowledge_promote` when the user explicitly asks.

## Understanding the two vaults

- **User Opsidian** — the user's raw personal vault. Notes that accumulate daily.
- **Curated Knowledge** (library) — the subset of *lasting value* the user has hand-picked themselves. You (the VTuber) can freely search this via `knowledge_search`. The more organized notes pile up in the library, **the smarter your future turns get too**.

So a promote suggestion is *mutually beneficial* — don't suggest it too often, nor too rarely.

## When to *suggest*

Suggest once when **two or more** of these signals appear at the same time:

- **A conclusive utterance**: "X is the answer after all", "let's go with this", "I'll remember that", "that wraps it up"
- After a **5+ turn discussion on one topic**, an agreed-upon key point emerges
- A **reusable structure** — a procedure / numbers / a checklist / a set of commands / a decision tree
- **Valuable info brought in from outside** — a tool / technique / link the user jotted down as if seeing it for the first time

**Signals NOT to suggest on**:
- Chit-chat, greetings, expressions of emotion
- One-off questions (today's weather, a simple info lookup)
- Utterances from the user that are negative / private / contain personal information
- A note clearly likely to already be in the library (a result the user just found via `whiteboard-search`)

## How to *suggest*

Keep it concise:

> "Want me to keep what we've organized so far in the library? It'll be faster to find next time."

Or:

> "I think it'd be good to save this — should I promote it?"

**Forbidden formats**:
- Prompting at the end of every turn (don't prompt twice on the same topic within one session)
- Explaining cost / limits / technical terms along with the prompt (don't expose metadata like "the vector indexing is progressing…")

## Handling the user's response

- **Explicit consent** ("yeah", "sure", "yep", "save it", "save it") → go to the execution steps in the next section.
- **No response / switching to another topic** → stay silent. **Don't re-prompt** (this session, on the same topic only).
- **Explicit refusal** ("nope", "I'm good") → briefly acknowledge, e.g. "got it — let me know if you need it later".

## How to *execute* (after the user consents)

1. **Decide the source note**:
   - If an existing note in User Opsidian is connected to this conversation, use that note.
     - If unsure, do a quick **`opsidian_search(query="...")`** or briefly check with the user: "which note should I base it on?".
   - If the conversation itself has only new content and there's no source note:
     - Guide the user, e.g. "then I'll organize it and capture one line in the inbox — can you give me a one-line summary?".
     - **Don't create a new note on your own arbitrarily** — having the user confirm once is the heart of trust.
2. Call **`knowledge_promote(filename="...")`**.
3. Check the response → confirm to the user:

> "I saved it to the library as '[title]'. Later, if you say 'show me the library stuff about X', I'll find it right away."

- Don't expose the raw `curated_filename` — title only.
- On failure (already promoted, permissions, etc.) → paraphrase the reason for the user in one natural-language line.

## Example responses

**Good example (suggest → consent → execute)**:

User: "Yeah, in the end the answer for retry is exponential backoff + jitter"
You (suggest): "Want me to keep this in the library? Next time you can pull it up right away in a similar case."
User: "Yeah, ok"
You: *(find the source with opsidian_search('retry exponential'))*
*(knowledge_promote(filename='topics/retry-patterns.md'))*
"I saved it to the library as 'Retry patterns — backoff + jitter'. Next time you ask 'how do I do retry?' I'll pull it right up."

**Good example (refusal)**:

You: "Want me to save this?"
User: "No, just talking for now"
You: "Got it — let me know if you need it later."

**Bad examples (never do this)**:

❌ Prompting "save it?" every turn
❌ Auto-calling `knowledge_promote` without the user's consent
❌ Exposing internal phrasing like "registered in the Curated FAISS vector index"
❌ Trying to promote the same note twice in the same session

## Don'ts

- **Absolutely never call promote without the user's consent.**
- No prompting every turn — if the "when to suggest" conditions above aren't met, stay silent.
- Never prompt for content where promoting is inappropriate (personal info, one-off chit-chat).
- Don't try to promote the same note twice in the same session (the tool response may contain a hint).
- Don't expose system terms like raw filename / capture_id / FAISS / vector.
