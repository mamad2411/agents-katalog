---
name: execute
description: Execute an approved ops plan — research, write, review, update state, archive. Use after /plan approval. Not for code.
argument-hint: <path to plan file>
---

Execute the plan at: $ARGUMENTS

**Scope:** This skill produces research, content, strategy, and specs — not code. If the plan involves code changes, use `/implement` instead. If the repo's CLAUDE.md has an `## Autopilot` section, code or product work also becomes an entry in `backlog/ideas.md`, linking any spec this plan wrote, so autopilot routes it to a repository and weighs it against the charter.

## Instructions

### 1. Read the plan

Read the plan file. Understand the objective, steps, and success criteria. Where the plan or a file the work reads carries an `ASKED (decide <id>` marker, resolve it as `ops:decide`'s `references/format.md` says ("The ASKED marker"): apply an answer as part of the work and remove the marker; go on with the recommendation, or wait, while it is open.

### 2. Execute

Carry out the plan:

1. Do the research, analysis, or writing described in the plan.
2. When researching, **always cite sources** — include URLs, document names, or specific references.
3. Store outputs in the appropriate location:
   - Research findings → `references/<topic>/`
   - Work products and deliverables → `artifacts/` (or as specified in the plan)
4. If the plan needs to change mid-execution (new information, blocked path), update the plan file and confirm the revised approach with the user before continuing.
5. An outgoing step (an email, a form, a post, a submission, a curated-list pull request) becomes an outbox item, and a decision the user wants to take later a question item, through `ops:decide`; never a file to copy-paste.

**Opportunity lifecycle:** When researching and qualifying opportunities (grants, partnerships, platforms, etc.):
1. Raw idea → backlog item. The item *is* the task: "research and qualify this."
2. After research → reference file gets the findings. Then either:
   - **Pursue** → backlog action item linking to the reference
   - **Pass** → reference entry updated with pass rationale + date, backlog entry removed

### 3. Review

Before updating state, review the deliverables. In autonomous execution this is the **only** verification gate — nothing you produce is seen by a human before it lands in the repo's state and knowledge base — so approach it as a skeptic reading someone else's work, not as a rubber-stamp of what you just wrote. A clean pass is fine, but only after you've genuinely tried to find the weak claim, the unsupported assertion, and the inconsistency:

1. **Fact-check** — verify claims against cited sources. Flag unsupported assertions.
2. **Consistency** — check that new artifacts don't contradict existing state files or prior completed plans.
3. **Completeness** — confirm the output covers everything the plan promised. Fill gaps or note them as out-of-scope with justification.
4. **Quality** — check formatting consistency, broken links, and missing references.

### 4. State updates

1. **Complete the plan file** — fill in Outcome, Key Decisions, Artifacts, and Session Log sections.
2. **Update `backlog/`** — **delete** the completed item from the relevant file (don't mark it "done"). If only part was completed, rewrite the entry to cover remaining work. If new tasks emerged, add them **in priority order** (highest first) — not at the end.
3. **Update `state/` files** — if the task changed anything documented in `state/`, update those files. Create a new state file if a significant new aspect emerged.
4. **Harvest insights** — review what you learned and persist it:
   - **MEMORY.md Key Learnings** — add or update if you learned something that changes the project's understanding of its landscape, constraints, opportunities, or strategic position. **Never put WAITING markers, task status, or blocked items in MEMORY.md.**
   - **New backlog items** — add actionable opportunities or follow-up tasks to the appropriate backlog file in priority order. Where the repo's CLAUDE.md has an `## Autopilot` section, a product or feature idea goes into `backlog/ideas.md` instead.
   - **User feedback** — where the repo's CLAUDE.md has an `## Autopilot` section, anything in a user's own voice the work turned up goes only into `references/users/feedback.md`, newest first, as `- YYYY-MM-DD · <source type> · <persona, if one fits> — <the substance>`, anonymised before it is written: no names, email addresses, handles, phone numbers, street addresses or account IDs, no place finer than a city, never a screenshot of a message.
5. **Patterns, anti-patterns, and conventions** — if the work revealed patterns worth documenting for future agents (e.g., effective research approaches, naming conventions for artifacts, common pitfalls in a domain), add them to `CLAUDE.md` only if most sessions need them, otherwise to the relevant reference file.
6. **INDEX.md cascade** — list every file created, moved, renamed, or significantly changed. For each, confirm its folder's `INDEX.md` is up to date. Cascade to parent INDEX.md if needed.

### 5. Archive the plan

First handle each `ASKED (decide <id>` marker in the plan, since an archived plan is never read again: remove an answered one, which the work applied; move each open one into the backlog file the plan's work belongs to, as one entry `Revisit <matter> once to-decide item <id> is answered; went ahead with <recommendation>`, followed by the marker.

Then move the plan to `plans/completed/` with a date prefix: `YYYY-MM-DD_original-filename.md`.

### 6. Report

Tell the user, in one short paragraph, what the project now knows or has that it did not, how solid it is — which claims you verified against a source versus which rest on a single unconfirmed claim — and anything you decided that the plan didn't settle. If something couldn't be verified, or part of the work is unfinished, lead with that. No file list, no per-file walkthrough, no INDEX-cascade checklist: the plan file and the commit are the record. If they need to open the deliverable, one path on a line at the end is enough.

(A sub-agent running this skill returns whatever format its caller asked for instead.)
