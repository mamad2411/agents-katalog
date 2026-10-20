---
name: for-yourname-doc
description: Writes or updates a FOR[Name].md file that explains a project in plain language for a specific person. Covers technical architecture, codebase structure, technologies and why they were chosen, and lessons (bugs, pitfalls, best practices). Use when the user asks for "FOR [name].md", "project overview for me", "explain this project in plain language", "document this project for [name]", "write a FOR_ALEX style doc", or wants a single engaging project doc that doubles as onboarding and post-mortem.
---

# FOR[YourName].md — Project Doc for a Person

This skill produces **one human-focused project document**: `FOR_[NAME].md` (e.g. `FOR_ALEX.md`, `FOR_JANE.md`). It is *not* a README or API reference. It’s “the doc you wish you had when you first opened the repo”—plain language, engaging, with analogies and lessons so the named person can understand, run, and learn from the project.

---

## When to Use This Skill

- User says: “Write a FOR [name].md”, “Create FOR_ALEX style doc”, “Document this project for me”, “Explain this project in plain language for [name]”.
- User wants a single project doc that explains what it is, how it’s built, why, and what to learn (including bugs and fixes).
- At project handoff, onboarding, or “wrap-up” when you want a lasting, readable summary.

**Filename:** `FOR_[NAME].md` — replace `[NAME]` with the person’s name in UPPERCASE (e.g. `FOR_ALEX.md`, `FOR_JANE.md`). If the user only says “for me”, use a placeholder like `FOR_ME.md` or ask for their name.

---

## Tone and Style

- **Plain language.** No corporate speak, no textbook tone. Write like you’re explaining to a smart colleague over coffee.
- **Engaging.** Use analogies (e.g. “conveyor belt”, “loading dock”, “foreman”), short anecdotes, and concrete examples so ideas stick.
- **Memorable.** One-sentence summaries, small tables, and “what to fix first” lists are better than long paragraphs.
- **Honest.** Include real bugs, pitfalls, and “how we fixed it” so the doc doubles as a post-mortem and learning guide.

---

## Required Sections

Produce a single markdown file with these sections. Adapt depth to project size; keep the *structure* so every FOR[Name].md feels familiar.

### 1. Opening (1 short paragraph)

- State that this doc is *for* the named person.
- Say what it covers: what the project is, how it’s built, why, and what they can learn (including bugs and fixes).
- One line on tone: “No corporate speak, no textbook. Think of it as the doc you wish you had when you first opened the repo.”

### 2. What Is This Thing, Really?

- **One clear sentence:** what the project does (e.g. “turns messy invoices into structured data”).
- **A short “you know the drill” paragraph:** the real-world problem and how the project solves it in a few steps (e.g. “Wakes up every 5 minutes → grabs emails → reads PDFs → understands with AI → stores in DB → replies to sender”).
- **One-liner takeaway** so the reader knows the value (e.g. “Email in → structured data out”).

### 3. The Big Picture: How It All Fits Together

- **One analogy** (e.g. conveyor belt, factory floor, pipeline) so the reader sees the flow at a glance.
- **Short table:** “Who does what” — one sentence per layer (app, scheduler, processor, mail, DB, API, etc.). No jargon dumps; each row = one responsibility.
- **One sentence** that ties it together (e.g. “The scheduler orchestrates mail and processor; the processor orchestrates file, AI, vendor, DB.”).

### 4. Technical Architecture

- **How the app actually runs:** startup, trigger (e.g. cron, scheduler, webhook), and “what runs when”.
- **Flow of one unit of work** (e.g. one invoice, one request): step-by-step from input to output. Number the steps.
- **Where the code lives:** entrypoint, orchestration, and main modules in a short list or table (paths and one-line roles).

### 5. Technologies and Why We Chose Them

- For each major tech (framework, DB, AI/OCR, queue, etc.): **what it is** and **why we use it** (e.g. “boring where we can be, clever where it pays off”).
- One short **takeaway** (e.g. “Use boring technology except where boring doesn’t cut it.”).

### 6. Lessons You Can Learn From This Project

This section is what makes the doc a learning tool. Include:

- **Bugs that exist (or existed) and how to fix them.** Name the file/line or area, the mistake (e.g. wrong operator, wrong return type, missing argument), and the fix. No shame—real bugs, real fixes.
- **Pitfalls and how to avoid them next time.** E.g. “Call sites must match function signatures”; “Imports and namespaces”; “Don’t leave dead code that looks like the real API.”
- **How good engineers think and work.** E.g. single responsibility, config/secrets outside code, logging, failing one item not the whole batch.
- **Best practices to adopt.** E.g. run the main path after changes, tests that hit real code paths, one source of truth for env vars, type hints/docstrings where they prevent mix-ups.

### 7. Quick Reference: What to Fix First (if applicable)

- If there are known bugs or tech debt, a short **numbered list** of “fix these first” with file names and one-line actions.
- Optional: “After that, run the pipeline once end-to-end and fix any remaining issues.”

### 8. Summary

- **What / How / Why / What to learn** in 4 short bullets or sentences.
- Optional closing line (e.g. “Reading the doc gets you the map; running and fixing gets you the territory.”).

---

## How to Gather Content

- **Read the codebase:** entrypoint (e.g. `app.py`), scheduler/jobs, main service/orchestrator, key modules (mail, file, AI, DB, API). Follow one full flow from trigger to storage/output.
- **Infer architecture:** what triggers work, what calls what, where config and secrets live.
- **Find real issues:** run tests, grep for TODOs/FIXMEs, check for signature/import/return-type mismatches, duplicate definitions, missing args, env var name drift. Turn these into “bugs and fixes” and “pitfalls.”
- **Technologies:** list from dependencies (e.g. `requirements.txt`, `package.json`) and code; explain “why” from how they’re used (e.g. “schema-flexible so we don’t run migrations for every invoice shape”).

---

## Checklist Before Delivering

- [ ] Filename is `FOR_[NAME].md` with the correct name.
- [ ] Opening says who the doc is for and what it covers.
- [ ] “What Is This Thing” has one clear sentence and a short stepwise story.
- [ ] Big picture has an analogy and a “who does what” table.
- [ ] Technical architecture has “how it runs” and “flow of one unit” and “where code lives.”
- [ ] Technologies section explains “why” for each major choice.
- [ ] Lessons include: bugs + fixes, pitfalls, how good engineers work, best practices.
- [ ] Quick reference (if applicable) and summary are present.
- [ ] Tone is plain and engaging; analogies or concrete examples appear where they help.
- [ ] No generic “this project uses X” without saying why or what the reader should learn.

---

## Optional: Reference Template

For a minimal section outline to paste and fill, see [reference.md](reference.md) in this skill folder.
