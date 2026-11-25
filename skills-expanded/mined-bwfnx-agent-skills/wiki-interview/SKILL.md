---
name: wiki-interview
description: Conduct a structured 20-question conversational interview to find and fix gaps, inaccuracies, and missing information in any of the user's personal wikis. Use this skill whenever the user says "interview me about my wiki", "check my wiki for accuracy", "wiki review session", "update my wiki from memory", "wiki corrections", "let's do a wiki interview", "quiz me on my wiki", "fact-check my wiki", or wants to improve wiki accuracy through conversation. Also trigger when the user mentions wanting to add personal knowledge to any of the four wikis (personal, SBDC, FNX Pearl, Northfork). This is a conversational skill — it asks questions one at a time and compiles corrections at the end.
---

# Wiki Interview

A structured interview process for improving wiki accuracy. You ask 20 focused questions, one at a time, based on what's already in the wiki — then compile all corrections and additions into a dated markdown file dropped into the wiki's `raw/` folder for the nightly ingest pipeline.

## Before You Begin

1. **Identify which wiki** the user wants to review. There are four:

| Wiki | Markdown source | Raw folder | Builder |
|------|----------------|------------|---------|
| Personal | `personal/wiki/` | `personal/raw/` | `python3 wiki-build.py personal` |
| SBDC | `sbdc-advising/wiki/` | `sbdc-advising/raw/` | `python3 wiki-build.py sbdc` |
| FNX Pearl | `fnx-pearl-consulting/wiki/` | `fnx-pearl-consulting/raw/` | `python3 wiki-build.py fnx-pearl` |
| Northfork | `northfork-farm/wiki/` | `northfork-farm/raw/` | `python3 wiki-build.py northfork` |

2. **Read the wiki's INDEX.md** to understand the full scope of articles.
3. **Read every article** in the wiki's `wiki/` folder. You need to know what's already documented to ask good questions. Skim for: missing fields, placeholder text, open items sections, dates that may be stale, people mentioned without full context, and topics that feel thin.
4. **Read the synthesis-journal.md** if one exists — it often flags known gaps.

## Interview Rules

These are strict:

- **Ask exactly one question at a time.** Never combine multiple questions into one.
- **Keep questions short and conversational.** No multi-part questions. No preambles longer than one sentence.
- **20 questions per session.** Count them explicitly (Question 1, Question 2, etc.).
- **Ground every question in something specific from the wiki.** Reference what you read — a missing field, a stale date, a thin section, an open item. Don't ask generic questions.
- **Prioritize high-value gaps.** Start with things that are factually wrong or critically missing (health conditions, family members, financial details, key dates). Save nice-to-haves for the end.
- **Acknowledge each answer briefly** (one sentence max) before moving to the next question. Don't summarize or restate what the user said.
- **If the user uploads a file**, read it and acknowledge it. It may answer the current question or provide context for future questions.
- **Question 20 is always the catch-all:** "Is there anything flat-out wrong in the wiki, or any topic we haven't covered that you've been meaning to add?"

## Question Design Strategy

When preparing your 20 questions, organize them roughly in this priority:

1. **Factual errors** — things the wiki states that might be wrong or outdated
2. **Critical omissions** — major life facts, health conditions, key people who aren't documented
3. **Stale information** — dates, statuses, or plans that may have changed
4. **Open items** — things explicitly flagged as unknown or pending in the wiki
5. **Thin sections** — articles that exist but lack meaningful detail
6. **Missing articles** — topics that should exist based on cross-references or context clues
7. **Catch-all** — Question 20

## After All 20 Questions

Once the user has answered all 20 questions, compile everything into a single markdown corrections file:

### Output Format

**Filename:** `YYYY-MM-DD-wiki-corrections-{context}.md` where `{context}` is `personal`, `sbdc`, `fnx-pearl`, or `northfork`.

**Location:** Save to the wiki's `raw/` folder (e.g., `personal/raw/2026-06-07-wiki-corrections-personal.md`).

**Structure:**

```markdown
# {Context} Wiki Corrections and Additions — YYYY-MM-DD

Source: 20-question interview session with {{USER}}.

---

## CORRECTION: {article-name}.md — {Brief Description}

{Details of what needs to change, with full context from the interview answer.}

---

## ADDITION: {article-name}.md — {Brief Description}

{New content to add, structured with all relevant details.}

---

## ADDITION: {New Article Title} (New Article Candidate)

{Content for a proposed new article, with enough detail for the ingest pipeline to work with.}
```

**Rules for the corrections file:**

- Use `CORRECTION:` for changes to existing content
- Use `ADDITION:` for new content within existing articles
- Use `ADDITION: ... (New Article Candidate)` for entirely new articles
- Include the target article filename (e.g., `health-profile.md`) in each heading
- Write corrections with enough context that someone reading only the corrections file understands what changed and why
- Convert any relative dates from the interview to absolute dates (e.g., "last week" → "week of 2026-06-01")
- If the user uploaded files during the interview, note that they were saved to `raw/` and reference them

### After Writing the Corrections File

Ask the user whether they want to:

1. **Run the rebuild now** — execute `python3 wiki-build.py {context}` and git push
2. **Let the nightly pipeline handle it** — the Tue/Thu/Sat ingest will pick it up
3. **Start a new chat for the rebuild** — if the conversation is long

## Session Flow Summary

```
Read INDEX.md and all wiki articles
  ↓
Prepare 20 prioritized questions
  ↓
Ask Question 1 → wait for answer → brief acknowledgment
Ask Question 2 → wait for answer → brief acknowledgment
...
Ask Question 20 (catch-all) → wait for answer
  ↓
Compile corrections file → save to raw/ folder
  ↓
Offer rebuild options
```
