---
name: learn-capture
description: Extract 1–5 atomic facts from pasted text and save them as spaced-repetition cards in workspace/learning/facts/ with SM-2 frontmatter. Use when the user says "capture this", "save fact", "learn this", "memorize this", or pastes content they want to retain.
---

# Learn Capture

Extracts atomic facts from user-provided text and saves them as SM-2 flashcard files in `workspace/learning/facts/`.

## Trigger

User pastes text (article, note, transcript excerpt) and wants to retain key facts for later review.  
**Does NOT fetch URLs automatically.** If the user provides a URL, ask them to paste the text content instead (v0 policy — no network dependency).

## Workflow

### Step 1 — Receive input

Ask the user (if not already provided):
- The text to capture (paste directly)
- Optional: deck name (default: infer from content or use `general`)
- Optional: source URL or description (default: `manual`)

If the user provides a URL only, respond:
> "Por favor, cole o texto do artigo diretamente aqui. A skill não faz fetch automático de URLs para evitar problemas de paywall e dependência de rede."

### Step 2 — Extract facts

Read the pasted text carefully. Extract **1 to 5 atomic facts** — each fact must be:
- **Atomic:** one idea per fact, not a summary paragraph
- **Memorable:** something worth reviewing in 1–30 days
- **Retrievable:** can be turned into a self-test question

Do NOT extract:
- Opinions without evidence
- Context that depends on reading the full article
- Facts already trivially known (e.g., "Python is a programming language")

### Step 3 — Generate file content for each fact

For each fact, produce content in this exact format:

```markdown
---
id: {YYYY-MM-DD}-{slug}
source: {source_url_or_"manual"}
deck: {deck_name}
created: {YYYY-MM-DD}
next_review: {YYYY-MM-DD+1 day}
interval: 1
ease: 2.5
reps: 0
lapses: 0
---

**Fact:** {The atomic fact stated directly, in pt-BR.}

**Why it matters:** {One sentence on why Davidson should remember this, in pt-BR.}

**Retrieval Q:** {A question whose answer is the fact above, in pt-BR.}
```

**Slug rules:**
- Kebab-case of the main topic of the fact
- Max 40 characters
- No accents, special characters, or spaces
- Example: `claude-skills-sao-arquivos-markdown`

**If slug collision (same date + same slug):** append `-2`, `-3`, etc.

**Dates (use today's actual date):**
- `created`: today in YYYY-MM-DD
- `next_review`: tomorrow in YYYY-MM-DD (today + 1 day)

**Language:** fact content (Fact, Why it matters, Retrieval Q) must be in **pt-BR** by default (workspace.language = pt-BR), regardless of the source language.

### Step 4 — Save files

For each fact:
1. Create `workspace/learning/facts/` directory if it does not exist
2. Write the file to `workspace/learning/facts/{YYYY-MM-DD}-{slug}.md`
3. Confirm success with the file path

### Step 5 — Report

After saving all files, output a summary:
```
✅ {N} fato(s) capturado(s) no deck "{deck}":
- workspace/learning/facts/{filename1}.md → {first 5 words of Retrieval Q}...
- workspace/learning/facts/{filename2}.md → ...
```

## Constraints

- Max 5 facts per capture session. If the text warrants more, tell the user to split it into multiple runs.
- Do NOT create or modify any file outside `workspace/learning/facts/`.
- Do NOT touch `review-log.jsonl` or any existing fact file.
- Do NOT fetch URLs — ask user to paste text.
- All 9 frontmatter fields must be present: `id`, `source`, `deck`, `created`, `next_review`, `interval`, `ease`, `reps`, `lapses`.
- `interval=1`, `ease=2.5`, `reps=0`, `lapses=0` are always the initial values.
