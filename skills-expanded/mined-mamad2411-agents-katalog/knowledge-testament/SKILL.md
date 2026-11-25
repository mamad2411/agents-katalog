---
name: knowledge-testament
description: "Knowledge testament: mines git blame/log to map where one developer's exclusive knowledge lives (sole-author hotspots, high-churn areas they own), generates a targeted interview asking exactly the questions nobody would know to ask, and writes a structured, code-linked testament document. Read-only towards the repo. Trigger: /testament"
trigger: /testament
---
# /testament

Mines git ownership to find where a person's exclusive knowledge lives and
runs a targeted handover interview - linked to code, honest about its own gaps.

## What this is for

- When someone leaves (resignation, sabbatical, team change) or proactively as a
  "living testament": implicit knowledge is by definition invisible to the carrier
  themselves - this skill uses git history to infer WHERE the knowledge lives
  and asks the exact questions nobody else would ask.
- **Read-only towards the repo.** No evaluation of individuals (no performance
  statements - only a knowledge map). No automatic mails/exports.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/testament -help` or `/testament -h` (without further arguments) is invoked:
output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target and author

Clarify `-ProjectDir` and the author (name/email as in git):

```powershell
& "<SKILL_DIR>/scripts/ownership.ps1" -ProjectDir "<path>" -ListAuthors
```

shows candidates with commit counts. Multiple git identities for the same person
(different emails): pass all associated entries as `-Author` values (script
accepts an array). Get confirmation.

### Step 3 - Ownership mining

```powershell
& "<SKILL_DIR>/scripts/ownership.ps1" -ProjectDir "<path>" -Author <values>
```

No commits found for the author: forward the `Write-Error` message (points to
`-ListAuthors`) directly and stop.

### Step 4 - Interview (block-wise, pausable)

1. Build a **knowledge map** from the JSON: areas, exclusivity level,
   interview priority (critical exclusive knowledge from `criticalExclusive` first).
2. Run interview block-wise, **max 3 questions per block**, then reflect answers in
   one line and follow up. Each question needs a concrete anchor from the evidence
   (file + blame share, or commit hash + subject) - never generic questions like
   "What is important?". Four question types:
   - **Decision**: "You wrote `<file>` at `<blameShare>` (anchor commit
     `<hash>`: `<subject>`) - what was wrong/different in the first approach?"
   - **Trap**: "What happens if someone 'simplifies' `<file>`? Where does it break
     first?"
   - **Context**: "What external constraint explains `<subject>` (commit
     `<hash>`)?"
   - **Handover**: "What should your successor in `<file>` NOT touch in week 1?"
3. **Pausability**: after each block immediately save the interim state as
   `testament-draft.md` in the current working directory. The user can abort at
   any time and resume later.
4. **Absence mode**: if the knowledge carrier is unavailable, still generate all
   interview questions and output them as a question catalog - clearly label as
   "Testament in absence / reduced mode", do not fabricate answers.
5. Evidence rule: interview statements
   are marked as such (source: interview, date) - they need no commit proof, but
   link every code reference as `file:line`/commit where possible.

### Step 5 - Write report

`testament-<author>.md` in the current working directory (**not** into the repo):

1. **Knowledge map** - table: area, exclusivity, risk.
2. Per area: **decisions** (with commit evidence), **traps** (verbatim from
   the interview, with file links), **context knowledge**.
3. **Week 1 warning list** for the successor.
4. **Open points** - questions not asked/unanswered. The testament is honest
   about its own gaps.

### Step 6 - Summarize

State the report path, give a short summary.

## Usage

```
/testament                       # interactive
/testament <repo> <author>       # testament for <author> from <repo>
/testament <repo> -list          # list authors with shares
/testament -help
```


