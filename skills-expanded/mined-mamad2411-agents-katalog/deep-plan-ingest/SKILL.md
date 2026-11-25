---
name: deep-plan-ingest
description: >-
  Distills a completed deep-plan document (e.g. docs/PLAN.md) into durable
  project knowledge files: AGENTS.md (agent operating rules and verified
  ground truth), docs/ARCHITECTURE.md (component map, data flow, framework
  mechanisms with citations), and ROADMAP.md (phased roadmap with live
  status). Carries only VERIFIED evidence forward, re-checks stale claims,
  and merges into existing files instead of overwriting. Use after a
  deep-plan finishes, when the user mentions deep-plan-ingest or ingest the
  plan, or asks to generate/update AGENTS.md, ARCHITECTURE.md, or ROADMAP.md
  from a plan.
license: MIT
argument-hint: "[plan-path] [project-root]"
---

# Deep Plan Ingest

A plan document is a snapshot; it goes stale the day implementation starts.
This skill moves the **verified knowledge** out of the plan and into the three
files future agents actually load — so the research paid for once keeps paying.

| Target | Purpose | Audience |
|--------|---------|----------|
| `AGENTS.md` | Operating rules + ground-truth facts for agents working in this repo | Every future agent session |
| `docs/ARCHITECTURE.md` | Component map, data flow, framework mechanisms — with citations | Agents and humans exploring the system |
| `ROADMAP.md` | The phased roadmap with live phase status | Anyone asking "what's next?" |

## The Prime Directive (inherited from deep-plan)

> **Only VERIFIED knowledge gets ingested. Stale evidence is re-verified or dropped.**

- Claims tagged `UNVERIFIED` in the plan never enter `AGENTS.md` or
  `docs/ARCHITECTURE.md`. They may appear in `ROADMAP.md` only as explicit
  open questions.
- `CORRECTED` entries win over the beliefs they corrected — ingest the
  correction, never the original mistake.
- A citation is copied along with its claim. A fact that loses its
  `file:line` / vendor path / doc URL on the way over was not ingested, it
  was laundered.

## Progress checklist

Copy this into your response and check items off:

```
Ingest Progress:
- [ ] Step 1: Locate the plan and confirm targets
- [ ] Step 2: Staleness check — re-verify claims touched since the plan was written
- [ ] Step 3: Ingest AGENTS.md (merge, don't clobber)
- [ ] Step 4: Ingest docs/ARCHITECTURE.md (merge, don't clobber)
- [ ] Step 5: Ingest ROADMAP.md with phase status
- [ ] Step 6: Report — written / updated / skipped / dropped-as-stale
```

## Step 1 — Locate the plan and confirm targets

- Plan path: use the path given with the invocation (`$ARGUMENTS` on
  platforms that substitute it); else try `docs/PLAN.md`, then
  `docs/*PLAN*.md`. If several candidates exist, ask ONE question with your
  recommended pick.
- Target detection: if the repo already uses `CLAUDE.md` or `AGENT.md` as its
  agent-instructions file, merge into that file instead of creating a
  parallel `AGENTS.md`. Never create a second competing instructions file.
- Read the entire plan before writing anything.

## Step 2 — Staleness check

The plan was true when written; the repo has moved. Before ingesting:

1. `git log --oneline <plan-file-mtime-or-date>..HEAD` — list commits since
   the plan (or since its "Generated on" date).
2. For every plan claim whose cited file appears in those commits, **re-open
   the file and re-verify** before carrying the claim over.
3. Claims that no longer hold are dropped and listed in the Step 6 report —
   never silently ingested.

Skip nothing here: ingesting a stale "fact" into `AGENTS.md` poisons every
future session that loads it.

## Step 3–5 — Write the three files

Follow the exact structures in the references (read the one you need before
writing that file):

- `AGENTS.md` → [references/agents-template.md](references/agents-template.md)
- `docs/ARCHITECTURE.md` → [references/architecture-template.md](references/architecture-template.md)
- `ROADMAP.md` → [references/roadmap-template.md](references/roadmap-template.md)

**Merge policy (applies to all three):**

- If the target does not exist, create it from the template.
- If it exists, update it **section by section**: refresh sections this skill
  owns, and leave human-authored sections untouched. When ownership is
  unclear, append under a clearly marked section rather than editing prose
  you did not write.
- Keep it lean. `AGENTS.md` is loaded into context every session — hard
  budget **under 150 lines**; move depth to `docs/ARCHITECTURE.md` and link
  to it. Prefer deleting an outdated line over adding a clarifying one.
- No duplication between the three files: rules live in `AGENTS.md`,
  structure in `ARCHITECTURE.md`, sequencing in `ROADMAP.md`. Cross-link
  instead of copying.

Before reporting, run the **mechanical checks** — commands, not judgment
calls; all must pass:

1. `wc -l` on the AGENTS-type file → **150 or less**; over budget = cut
   lines until it passes, never present-and-apologize.
2. Repo metadata (remotes, hosting, author) must match `git remote -v` /
   git config output exactly — **never construct a GitHub/GitLab URL from
   the repo's name**; no remote = say so.
3. Every claim carried over kept its citation — grep the outputs for
   bare assertions that lost their `file:line` on the way.

## Step 6 — Report

End with a concise report:

- **Written/updated:** each file with a one-line summary of what changed.
- **Dropped as stale:** each plan claim that failed re-verification, with the
  commit or file that invalidated it.
- **Skipped:** `UNVERIFIED` items excluded (count is enough).
- **Suggested follow-up:** if many claims were stale, recommend re-running
  deep-plan for the affected area instead of patching the docs by hand.
