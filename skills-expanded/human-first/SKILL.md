---
name: human-first
description: |
  Takes the agent's last message and explains it in plain language —
  without technical jargon, with concrete examples and analogies.
  Invoked manually when the user did not understand what the agent
  just wrote.

  Use when: "/human-first", "explain in plain language", "didn't get
  what you wrote", "explain simpler"
---

# Human-First Protocol

Explains the agent's last message in plain language with examples.

## Input

The agent's most recent chat message that the user found unclear or too technical.

## Output

A simplified explanation of that message in plain language with concrete examples and analogies, printed to chat.

## Hands off to

— (terminal).

---

## Step 1 — Find the last message

Take the agent's message that stands **immediately before the `/human-first` command** in the current conversation.

If no such message exists:

```
No previous message found to explain.
Type /human-first right after my reply.
```

End execution.

---

## Step 2 — Extract key ideas

Extract **1-3 main ideas** — what the agent was trying to say in essence. Don't retell structure or details — only the point.

Short message with one thought → explain the one. Long message → pick the most important, drop the rest.

---

## Step 3 — Explain each idea

For each idea — three elements:

**What it is** — one sentence, no technical terms. If a term is unavoidable — explain it in parentheses in one word.

**Why it's needed** — one sentence. Which problem it solves, what would be missing without it.

**For example** — a concrete example from real life, not from code. Start with "Imagine that..." or "For example, like..."

### Explanation rules

- Speak like to a friend, not like documentation
- Short sentences — max 15-20 words
- If original had 5 items → explain 2-3 most important, not all
- Don't add new information that wasn't in the original
- Don't make the explanation longer than the original

---

## Step 4 — Output the explanation

Output format:

```
In plain language:

**{Idea 1 — short name}**
What: {one sentence}
Why: {one sentence}
For example: {life analogy}

**{Idea 2}** (if any)
...

If something else is unclear — ask specifically.
```

The last line — always. Invites clarification without extra pressure.

---

## Anti-patterns

### ❌ Retell technically — only in different words

Original: "add an index on the column to speed up queries".
Bad: "create an index so SELECT works faster".
Good: "make a book index — so the database doesn't flip through all records, but opens the right page immediately".

**Rule:** if the explanation still contains technical words from the original — reformulate via an analogy.

### ❌ Invent an example outside the conversation context

Explaining databases — example about pizza recipe. User loses the thread.

**Rule:** the example must be understandable from the task context. Task about documents → example about documents. About money → about money.

### ❌ Explain everything in a long message

Original has 8 items. Agent explains all 8, producing a wall of text.

**Rule:** max 3 ideas. Pick the most important — the ones without which the rest is unclear.

### ❌ Add new information

While explaining, the agent adds details that weren't in the original — "by the way, this is also related to X".

**Rule:** only what was in the original message. No bonus knowledge.

---

## Related skills

- **note-first** — save the current explanation as a persistent note for the task
- **decision-first** — 5-part model when the agent has to choose instead of the user asking

---

## Step 99 — Log invocation

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'human-first', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true` keeps a logging failure from aborting the skill.
