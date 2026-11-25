---
name: util-projectinit
model: claude-sonnet-4-6
effort: medium
description: >
  Initialize a new CO2 project by validating a hand-authored brainstorm session document and
  setting up the file-based, turn-based BRAINSTORMING session kit around it. The ONLY valid
  input is the path to an EXISTING `<topic>.brainstorm.md` file the user authored from the CO2
  application-development template (`brainstorm-template-appdev.md`) — free-form prompts, idea
  text or topic slugs are NOT accepted. The skill strictly validates the session document
  against the template, rejecting with a report on any deviation — it never creates or edits
  the session document. On a clean pass it scaffolds the rest of the brainstorm kit in the
  project folder: the shared `brainstorm-protocol.md`, the `co2-context-generation-guide.md`
  artifact rules, and the `/brainstorm-loop` slash command. The user then manually runs
  `/brainstorm-loop` — an iterative, token-efficient loop that converges the root `CLAUDE.md`
  (Phase A) and every application's `PRD.md` (Phase B) round by round. This skill seeds the
  project — it is the first skill to run before any `modelgen-*`, `mockgen-*`, `specgen-*`,
  `testgen-*`, `util-projectsync` or `util-preparek8senv` invocation.
  Trigger on keywords: "init project", "initialize project", "start project", "bootstrap project",
  "scaffold project", "new project", "project init", "brainstorm project", "brainstorm app idea",
  "setup brainstorm", "start brainstorming", "brainstorm session", "generate CLAUDE.md".
  Accepts one MANDATORY argument: the path to an existing `<topic>.brainstorm.md` session
  document based on the CO2 template. If the argument is missing, is not a `.brainstorm.md`
  path, or the file does not exist, the skill stops and instructs the user to copy the
  template manually.
---

# Util Project Init — CO2 Brainstorm Session Setup

Bootstrap a new CO2 project by validating a **user-authored brainstorming session document**
and setting up the brainstorm kit around it. A one-shot generation from a one-paragraph brief
produces shallow, guessed context; the brainstorm loop instead converges the context **round by
round** — the agent drafts, asks focused questions, the user answers in the document, and the
drafts improve until the user locks them.

The brainstorm produces the complete CO2 project context tree:

- **Phase A** — root `CLAUDE.md` (apps, modules, bounded contexts, App Codes, App × Module matrix)
- **Phase B** — one `PRD.md` per custom application (versioned User Stories / NFRs / Constraints /
  References / Tests)

`DEVTOOL.md` and `ENVIRONMENT.md` are NOT produced by the brainstorm — they come later
(`util-preparek8senv` and per-developer setup). Once the brainstorm session is CLOSED, downstream
skills (`util-projectsync`, `modelgen-*`, `mockgen-*`, `specgen-*`, `testgen-*`, `conductor-*`)
take over.

**This skill validates and sets up the kit only. It never creates or edits the session
document, and it never runs the brainstorm loop itself** — the user authors the session
document from the template beforehand and manually runs `/brainstorm-loop` when ready.

## The Kit

The session document is the **input** — hand-authored by the user from
`reference/brainstorm-template-appdev.md`. Three supporting files are copied from this skill's
`reference/` folder:

| File | Copied to | Role |
|------|-----------|------|
| `<topic>.brainstorm.md` | — (input — hand-authored by the user from `brainstorm-template-appdev.md`) | The session document the user fills in and the loop iterates on — validated by this skill, never created or edited by it |
| `brainstorm-protocol.md` | `<project-root>/brainstorm-protocol.md` | Shared static protocol (state machine, turn rules) — never edited during sessions |
| `co2-context-generation-guide.md` | `<project-root>/co2-context-generation-guide.md` | Artifact rules the agent follows when drafting CLAUDE.md and PRD.md — referenced from the session document |
| `brainstorm-loop.md` | `<project-root>/.claude/commands/brainstorm-loop.md` (only if the command is not already available) | The `/brainstorm-loop` slash command — the polling watch loop |

> **Plugin note:** when this skill is installed as part of the `co2-skills` plugin, the
> `/brainstorm-loop` command ships with the plugin (`commands/brainstorm-loop.md`) and is already
> available — the project-local copy is a fallback for setups where the skill files were copied
> manually into `.claude/skills/`.

Generated at runtime by the loop (never created by this skill):
`<project-root>/.brainstorm-loop-status.md` — the live dashboard + compaction advisory.

## Input Resolution

```
/util-projectinit <path-to-topic.brainstorm.md>
```

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<session-file>` | **Yes** | `recruitment-hub.brainstorm.md` | Path to an EXISTING session document authored by the user from `brainstorm-template-appdev.md`. Free-form idea text or topic slugs are NOT accepted. |

### Argument Rules

1. The argument is **mandatory**, must be a path whose filename ends in `.brainstorm.md`, and
   must point to an existing file.
2. If the argument is omitted, is not a `.brainstorm.md` path, or the file does not exist →
   **stop** and print the block below, substituting `<template-path>` with the resolved
   absolute path of `reference/brainstorm-template-appdev.md` inside this skill's folder:

   ```
   ## util-projectinit — session document required

   This skill takes exactly one argument: the path to an existing
   <topic>.brainstorm.md authored from the CO2 template. Free-form prompts
   or idea text are not accepted.

   To create one:
     1. Copy the template
          <template-path>
        to your project root as <topic>.brainstorm.md
        (topic = short kebab-case slug, e.g. recruitment-hub.brainstorm.md)
     2. Fill in the human-owned parts:
        - frontmatter: session_id (<topic>-co2-context), title, created (today, YYYY-MM-DD)
        - # Context: describe your application idea
        - ## References: optional style-reference files (relative paths; keep the `./co2-context-generation-guide.md` line)
        - # Output Specification: confirm destination (default ./)
        Leave untouched: state, current_round, protocol_version, # Objective,
        # Status, # Question, # Output, # Feedback.
     3. Re-run: /util-projectinit <topic>.brainstorm.md
   ```

3. **Never create the session document on the user's behalf** — not even a template copy.

## Validation

Read the session document and check it against `reference/brainstorm-template-appdev.md`.
Validation is **read-only and strict**: if ANY check fails, print the validation report
(format below) listing EVERY failed check with expected vs. found, and **stop** — do not set
up the kit. Never edit the session document; the user fixes it and re-runs.

| # | Check | Rule |
|---|-------|------|
| V1 | Frontmatter | YAML frontmatter present with `doc_type: ai-brainstorm-session` |
| V2 | `session_id` | Set, contains no `CHANGE-ME`, is kebab-case, ends with `-co2-context`, and its `<topic>` part matches the filename (`<topic>.brainstorm.md`) |
| V3 | `title` | Set, contains no `CHANGE ME` and no `<Project Name>` placeholder |
| V4 | `created` | A real `YYYY-MM-DD` date (not the `<YYYY-MM-DD>` placeholder) |
| V5 | `state` / `current_round` | Requires `state: NEW` and `current_round: 0`; if `state` instead holds a recognized in-progress/finished value (`AWAITING_HUMAN`, `AWAITING_AGENT`, `ERROR`, `CLOSED`), reject with *"this session is already in progress — resume it with `/brainstorm-loop` instead"*; if the fields are missing or hold an unrecognized value, report a plain expected-vs-found row instead |
| V6 | `protocol_version` | Exactly `"2.0"` |
| V7 | Sections | All template sections present: `# Objective`, `# Context` (with `## References`), `# Output Specification`, `# Status`, `# Question`, `# Output`, `# Feedback` |
| V8 | `# Context` filled | The `[DESCRIBE YOUR APPLICATION IDEA HERE]` placeholder is gone and the section contains non-empty prose |
| V9 | Guide reference | `## References` still lists `./co2-context-generation-guide.md` |
| V10 | Output Specification | `format` is `co2-tree` and `destination` is set |
| V11 | `# Status` table | Exactly the template's single row 0: `Session completion | Human | PENDING` |
| V12 | Agent-owned sections | `# Question`, `# Output` and `# Feedback` bodies are empty (HTML comments allowed) |

### Validation report format

```
## Session Document Validation FAILED — <file>

| # | Check | Expected | Found |
|---|-------|----------|-------|
| V4 | created date | real YYYY-MM-DD | <YYYY-MM-DD> (placeholder) |
| V8 | # Context filled | idea prose | [DESCRIBE YOUR APPLICATION IDEA HERE] |

Fix the items above in <file> and re-run:
    /util-projectinit <file>
(This skill never edits your session document.)
```

## Pre-Flight Checks

Inspect the project root (the folder where Claude Code was launched) before writing anything.
The skill is **non-destructive** — it never overwrites any existing file:

| Condition | Action |
|-----------|--------|
| Another `*.brainstorm.md` with `session_id: *-co2-context` exists (besides the input file) and is not `state: CLOSED` | Warn: a CO2 context session is already in progress; ask whether to set up this second session anyway or resume the existing one with `/brainstorm-loop`. |
| `CLAUDE.md` exists at the project root | Warn: the project looks already initialized. The brainstorm's destination will **overwrite CLAUDE.md draft-by-draft** once the loop runs. Since this skill never edits the session document, advise the user to change the session's `destination` to `./output/<project-code-lower>/` themselves and re-run if they want to keep the current CLAUDE.md untouched. Confirm before proceeding with `destination: ./`. |
| `brainstorm-protocol.md` / `co2-context-generation-guide.md` exist | Skip copying that file (log "already present"). |
| `.claude/commands/brainstorm-loop.md` exists | Skip the command copy. |

## Workflow

### 1. Validate the session document

Run the full V1–V12 validation above. On any failure: print the validation report and stop.
Only continue to the setup steps below on a clean pass.

### 2. Ensure the `/brainstorm-loop` command is available

1. If running as the `co2-skills` plugin, the command is already installed with the plugin —
   nothing to do.
2. Otherwise (or when unsure), copy `reference/brainstorm-loop.md` from this skill's folder to
   `<project-root>/.claude/commands/brainstorm-loop.md` (create the `.claude/commands/` folder if
   needed). Do not modify the file content.
3. Remind the user in the final instructions: if `/brainstorm-loop` is not recognized, restart the
   Claude Code session so newly added commands are picked up.

### 3. Copy the protocol and the generation guide to the project root

Copy verbatim from this skill's `reference/` folder:

- `brainstorm-protocol.md` → `<project-root>/brainstorm-protocol.md`
- `co2-context-generation-guide.md` → `<project-root>/co2-context-generation-guide.md`

Both must sit at the **scan root** (the project root): the loop reads the protocol from there,
and the session document references the guide as `./co2-context-generation-guide.md`.

### 4. Recommend permission pre-approval (Claude Code CLI)

The watch loop's blocking poll uses `find`, `sleep`, `md5sum` and `sort` via Bash. An unanswered
permission prompt **silently pauses the loop** while the user thinks it is watching. Tell the
user to either:

- choose **"Yes, and don't ask again"** on the first permission prompt after starting the loop, or
- pre-approve in `<project-root>/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(find:*)",
      "Bash(sleep:*)",
      "Bash(md5sum:*)",
      "Bash(sort:*)"
    ]
  }
}
```

If the user asks the skill to do it, merge these entries into the existing
`.claude/settings.json` (or `.claude/settings.local.json` if the user prefers not to commit
them) without removing anything already there.

### 5. Print the instruction block

End with a single instruction block. This is the hand-off — the skill stops here and the user
drives the rest from the Claude Code CLI:

```
## Brainstorm Session Ready

### Files set up
| File | Status |
|------|--------|
| <topic>.brainstorm.md | Validated — YOUR session document (V1–V12 passed) |
| brainstorm-protocol.md | Copied |
| co2-context-generation-guide.md | Copied |
| .claude/commands/brainstorm-loop.md | Copied | (or "Provided by co2-skills plugin")

### Next steps (manual)

1. VERIFY the session document <topic>.brainstorm.md one last time in your editor:
   - `# Context` — your application idea is stated the way you want it; the
     agent probes for the rest round by round.
   - `## References` — style-reference files (an existing CLAUDE.md or PRD.md)
     are listed as relative paths, if you want them used.
   - `# Output Specification` — `destination` is where you want the context
     tree drafted (default `./` = this project root).
   - Do NOT touch `state`, `current_round`, `# Status`, `# Question`, `# Output`.

2. START the loop in this Claude Code session:

       /brainstorm-loop

   (add the folder as an argument if your session file lives elsewhere:
   `/brainstorm-loop <scan-root>`). If the command is not recognized, restart
   Claude Code and run it again.

3. ITERATE — each round:
   - The agent drafts CLAUDE.md/PRD.md to the destination and appends numbered
     questions under `# Question > ## Round N`.
   - Answer under each `### Answer X` (unanswered = "agent's judgment"), save as
     often as you like — saves alone never trigger the agent.
   - COMMIT your turn by flipping exactly ONE row in the `# Status` table:
       keep iterating → set `Round N answers and feedback` to COMPLETED
       finish        → set `Session completion` (row 0) to COMPLETED
   - The agent wakes within ~60 s of the flip.

4. WATCH `.brainstorm-loop-status.md` (the live dashboard):
   - `compact_advice: RECOMMENDED/REQUIRED` → at your next pause run /compact,
     then /brainstorm-loop again. Nothing is lost — the documents are the database.

5. WHEN CLOSED — the CO2 context tree (CLAUDE.md + per-app PRD.md) is at the
   destination. Continue the CO2 workflow:
   - /util-projectsync         → scaffold app folders, PRD.md/BUG.md reconciliation
   - /conductor-feature-prepare → models, mockups, specifications, test specs
```

Adapt the block to what actually happened (files skipped because they existed, plugin-provided
command).

## Important Rules

- **Validate-only for the session document.** Never create, copy, template-fill, or edit
  `<topic>.brainstorm.md` — not to fix a placeholder, not to correct a date, not even when the
  user asks during setup. On any validation failure, report and stop; the user edits the file.
- **Setup only — never run the loop.** Always end by instructing the user to run
  `/brainstorm-loop` manually.
- **Non-destructive.** Never overwrite an existing `brainstorm-protocol.md`,
  `co2-context-generation-guide.md`, or `.claude/commands/brainstorm-loop.md`. Skip and report.
- **Copy verbatim.** The protocol, guide, and command files are copied byte-for-byte from
  `reference/` — never edited, summarized, or "improved" during setup.
- **One session document per topic.** Multiple independent sessions are allowed (the protocol
  isolates them), but warn before setting up a second `*-co2-context` session for the same
  project.
- **The session document is fully human-owned.** This skill reads it for validation and
  nothing more. It never pre-answers questions, never adds rounds, never touches the Status
  table.
- **Claude Code CLI is the interaction surface.** Instructions must be terminal-friendly: the
  loop runs inside the live session (no headless `claude -p`), the user edits the session file in
  a separate editor while the loop watches, and permission prompts appear in the terminal — an
  unanswered one silently pauses the loop (hence the pre-approval step).
- **Do not create per-application folders, DEVTOOL.md, ENVIRONMENT.md, or K8s manifests.** The
  brainstorm produces CLAUDE.md + PRD.md; folder scaffolding is `util-projectsync`'s job and
  environment expansion is `util-preparek8senv`'s job.

## Reference Files

| File | Read when |
|------|-----------|
| `reference/brainstorm-setup-guide.md` | For the full end-to-end walkthrough (setup, iteration cycle, compaction, troubleshooting) — use it to answer any user question about how the loop works |
| `reference/brainstorm-protocol.md` | To answer questions about the state machine, turn rules, or error handling |
| `reference/brainstorm-template-appdev.md` | The template users copy manually to author their session document — also the validation baseline for V1–V12 |
| `reference/co2-context-generation-guide.md` | The artifact rules the loop's agent follows (Phase A/B, probing checklists, CLAUDE.md/PRD.md content rules) |
| `reference/brainstorm-loop.md` | The `/brainstorm-loop` command source |
