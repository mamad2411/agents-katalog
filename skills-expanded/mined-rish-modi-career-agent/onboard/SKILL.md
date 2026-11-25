---
name: onboard
description: First-run setup for a fresh clone of career-agent. Bootstraps $PERSONAL, checks prerequisites (pandoc, python deps, git config), then runs a guided interview to populate personal-info, goals, impact-doc, and brag-doc. Detects partial setup and resumes. Use when the user says "/onboard", "set me up", "I just cloned the repo", "first time using this".
---

# Onboard

## When to use
On a fresh clone of the repo, or any time the user explicitly invokes `/onboard`. Also when the user says things like "I just cloned this", "set me up", "first time", "how do I start".

If the user is mid-task on something else (writing a resume, analyzing a Job Description), do **not** silently redirect them into onboarding. Confirm first.

## What it produces
- `$PERSONAL/` directory bootstrapped with `career/` and `applications/` subfolders.
- Four core personal docs populated (or skipped at the user's choice) in `$PERSONAL/career/`:
  - `personal-info.md`
  - `goals.md`
  - `impact-doc.md`
  - `brag-doc.md`
- A short readout of what was filled, what was deferred, and what tools (if any) are missing.

Nothing else. No git changes. No app launching. No resume generation.

## Workflow

Run these phases in order. **Each phase is resumable**: re-running `/onboard` after partial setup detects what already exists and picks up where the user left off. Confirm before overwriting any file that already has real content (not template stubs).

### Phase 0: Resolve $PERSONAL and detect state

1. Resolve `$PERSONAL` and `$LEETCODE_BANK` per `CLAUDE.md` (both are siblings of the main repo).
2. Check what already exists:
   - Does `$PERSONAL/` exist?
   - Does `$PERSONAL/career/` exist?
   - Does each of `personal-info.md`, `goals.md`, `impact-doc.md`, `brag-doc.md` exist?
   - For each existing file: is it still a template stub (contains the original `<!-- comments -->` and empty fields) or does it have real content?
   - Does `$LEETCODE_BANK/` exist (for Phase 2.5)?
3. Print a one-line state summary, e.g.:
   ```
   Setup status: $PERSONAL exists, personal-info filled, goals stub, impact-doc and brag-doc missing. $LEETCODE_BANK missing.
   Resuming from goals.
   ```
4. If everything is already filled with real content, ask the user whether they want to re-interview any section or just exit.

### Phase 1: Prerequisite checks

Run these silently and only report the **missing** ones. Don't list things that work.

| Check | How | Why it matters |
|---|---|---|
| `git config user.name` and `user.email` set | `git config user.name && git config user.email` | Commits and PR authorship. |
| `pandoc` installed | `pandoc --version` | `resume-builder` and `cover-letter-builder` produce `.docx`. |
| `python3` installed | `python3 --version` (Windows: `py --version` or `python --version`) | All doc-generation skills. |
| Python deps: `python-docx`, `reportlab`, `requests` | `python3 -c "import docx, reportlab, requests"` | Resume `.docx` / `.pdf` generation, Job Description fetching. |

For each missing item, print a one-line fix:
- `pandoc` → `brew install pandoc` / `winget install pandoc` / `apt install pandoc`.
- Python deps → `pip install python-docx reportlab requests`.
- Git config → `git config --global user.name "Your Name"` etc.

If everything is present, say so in one line ("Prereqs: all good") and move on. Do **not** block onboarding on missing tools. They're only needed when the relevant skill is later invoked.

### Phase 2: Bootstrap $PERSONAL

If `$PERSONAL/` or its subfolders don't exist, create them and copy the templates that aren't already in place:

```
$PERSONAL/career/
$PERSONAL/applications/
$PERSONAL/career/personal-info.md   (copy from career/personal-info.template.md if missing)
$PERSONAL/career/goals.md           (copy from career/goals.template.md if missing)
$PERSONAL/career/impact-doc.md      (copy from career/impact-doc.template.md if missing)
$PERSONAL/career/brag-doc.md        (copy from career/brag-doc.template.md if missing)
```

Never overwrite an existing file at this phase. Templates only land in slots that are empty.

### Phase 2.5: Bootstrap $LEETCODE_BANK

The `coding-prep` skill's company-lookup flow reads from a read-only sibling clone of an upstream open-source repo. Resolve `$LEETCODE_BANK` per `CLAUDE.md` (sibling of the main repo, named `leetcode-companywise-interview-questions/`).

1. **If `$LEETCODE_BANK` does not exist:** clone it shallow.
   ```bash
   git clone --depth 1 https://github.com/snehasishroy/leetcode-companywise-interview-questions.git "$LEETCODE_BANK"
   ```
   Tell the user what you're doing in one line ("Cloning company-tagged question bank to $LEETCODE_BANK") before running. The clone is several MB and takes a few seconds. Confirm success in one line.

2. **If `$LEETCODE_BANK` already exists:** fast-forward to upstream.
   ```bash
   git -C "$LEETCODE_BANK" pull --ff-only
   ```
   Silent if up-to-date. If it errors (uncommitted changes, diverged), tell the user and skip; do not force-update someone else's clone.

3. **If `git` is missing or the clone fails (no network, etc.):** report in one line and continue. The bank is optional infrastructure; everything else still works. Suggest the user re-run `/onboard` later or clone manually.

Never modify files inside `$LEETCODE_BANK`. It is upstream-owned. The only writes here are `git pull --ff-only` to refresh.

### Phase 3: Set expectations

Before starting the interview, tell the user (once, briefly):

> I'll walk you through four documents: personal info, goals, impact doc, brag doc. You can fill any of them in now, defer to later, or paste raw text I'll structure for you. **Filling everything now gives the most accurate resumes, fit analyses, and interview prep.** Deferred sections will block the skills that depend on them (e.g., resume-builder needs impact-doc).

Then ask: *"Want to go through all four, or pick which ones to do now?"*

### Phase 4: Interview, one doc at a time

For each doc in order, ask the user up front:

> **personal-info.md** — quick form: name, email, phone, location, LinkedIn, GitHub. ~2 min. Fill now, defer, or paste a block I'll parse?

Three branches:

- **Fill now (guided)**: Ask each field one at a time. Keep it tight. If the user already gave a value earlier in the session (e.g., from CLAUDE.md context like email), prefill and confirm rather than re-asking. Write the file when the section is complete.
- **Paste**: User pastes a block of raw text (e.g., LinkedIn export, an old resume, freeform). Parse it, populate the file, show the result, ask for corrections.
- **Defer**: Leave the template stub in place. Note this in the final readout. Move on.

Doc-specific guidance:

**personal-info.md** — simple key/value. Strip the placeholder formatting; write actual values. If the user volunteers links (portfolio, blog), add them as new lines.

**goals.md** — the template has six sections (current state, target roles, target companies, constraints, what I want, what I'm avoiding). Don't ask all 30+ fields. Ask in groups:
1. "Current role and level?" (title, level, YOE, preferred coding language)
2. "What roles are you targeting?" (titles, level direction, IC vs. EM, domains)
3. "Target companies, tier 1 / tier 2 / no-go list?"
4. "Constraints: location, comp expectation, timeline, dealbreakers?"
5. "What's drawing you to a new role, and what are you avoiding from past roles?"

Skip any group the user says they don't have an answer for yet; leave that section as a comment they can fill in.

**impact-doc.md** — the most important doc and the longest. Ask:
1. "List your companies in reverse-chronological order, with dates."
2. For each company: "Title progression?" then "What are the 2 to 4 projects you'd want a hiring manager to know about?"
3. For each project, prompt: *what it was, your specific role, tech stack, metrics/scope, outcome, what was hardest.* One project at a time. Don't batch.
4. After projects, ask about cross-cutting work (mentorship, hiring, on-call leadership, design reviews).

If the user has an existing resume, LinkedIn dump, or old impact doc, **offer to ingest it first**: *"Paste what you have, I'll structure it, then we'll fill the gaps."* This is usually faster than cold interviewing.

If the user wants to defer impact-doc, warn them explicitly: *"`resume-builder`, `cover-letter-builder`, `star-stories`, and `job-analyzer` all depend on this. They'll work but the output will be generic until you fill it in."*

**brag-doc.md** — four sections (quantified wins, recognition, things shipped, talks/writing/mentorship, failures/lessons). Ask:
1. "Top 5 quantified wins from the last 2 to 3 years? Metric + 1-line context each."
2. "Recognition: promotions, awards, named callouts?"
3. "Failures or hard lessons worth keeping? Useful later for behavioral stories."

Skip "things shipped" and "talks/writing" unless the user volunteers; impact-doc already covers most of that.

### Phase 5: Final readout

Print a compact summary:

```
Setup complete.

Filled:
- personal-info.md
- goals.md (deferred: target companies, dealbreakers)

Deferred:
- impact-doc.md  → blocks resume-builder, cover-letter-builder, star-stories, job-analyzer
- brag-doc.md    → used by resume-builder and interview-prep for quantified bullets

Missing tools: pandoc (needed for .docx output)

Suggested next step:
Fill impact-doc.md when you have ~30 min. Then run /help to see what each skill needs.
```

Then **stop**. Don't auto-launch another skill.

## Behaviors and edge cases

- **CLAUDE.md says "no em dashes."** Apply this from the moment of onboarding onward (in the files you write and in your responses). The user has confirmed this preference.
- **CLAUDE.md says "work on master."** If the user is on a branch when they invoke `/onboard`, gently flag it. Don't force a switch.
- **Templates may have changed since clone.** If the template file in the repo is newer than the personal copy and the personal copy is still a stub, prefer the latest template content. If the personal copy has real content, leave it alone.
- **Don't ingest external accounts.** No reaching out to LinkedIn, GitHub, etc. The user pastes what they want to share.
- **Persist incrementally.** Write each file as soon as its section is done. Don't hold everything in memory and write at the end; a crashed session shouldn't lose 40 minutes of interviewing.

## Anti-patterns

- **Don't auto-fill from CLAUDE.md context without confirming.** The user's email is visible in the system context but they still get to confirm it before it lands in `personal-info.md`.
- **Don't editorialize about gaps.** If a user defers a section or has thin content, note the dependency impact and move on. No "you really should fill this in" lectures.
- **Don't validate format pedantically.** If the user gives "tc: 320k" instead of a structured field, accept it and write it as-is. The docs are for the user, not for a schema.
- **Don't run other skills inside onboard.** Onboarding ends at the readout. The user runs `/help` or a specific skill next.
- **Don't ask "are you ready?" between every step.** Move through the interview at a brisk pace. Pause only at doc boundaries.
- **Don't create $PERSONAL silently if it already exists.** Detect, report, and resume.
