---
name: prose-draft
summary: "Drafts internal close-out prose (retros, poster entries) with a foreign model, for human review."
description: >
  First-draft internal close-out prose (retrospectives, product-poster entries, sprint-wrap
  summaries) by delegating to a cheap different-family model via the cross-agent rail. Use at
  sprint/epic close, or when the product owner asks to "draft the retro", "draft the poster entry", "write
  the sprint wrap". Runs scripts/prose-draft.mjs, which gathers the epic's own docs + git log,
  applies the house-voice prompt, and prints an advisory draft to stdout. The draft is NEVER
  committed as-is — the coordinating agent edits it for factual accuracy first (drafts invent
  plausible-sounding gaps; the output banner says so). PR bodies are NOT in scope: the agent
  that built a PR writes its body (it already holds the context).
# Repo-local scripts this skill wraps — its FULL closure: the entry script, everything it imports,
# scripts it runs as subprocesses, and data files it reads by path. Paths are relative to the
# CONSUMING project's scripts/ dir; they deliberately do NOT ship inside this plugin. CI
# (scripts/check-skill-scripts.mjs) walks the import graph and fails if this list understates it.
requires_scripts:
  - prose-draft.mjs
  - lib/cross-agent-cli.mjs
  - lib/review-shape.mjs
  - lib/prose-writer.mjs
  - lib/prose-guard.mjs
  - lib/jev.mjs
  # compiled-prompts D9: the Jev questions are data the guards read (not an import edge, so declared by hand).
  - lib/jev-questions.mjs
  - lib/jev-questions/prose.json
  - lib/reporting-config.mjs
  - prose/cpo-persona.md
  - prose/internal.task.md
  - lib/project-root.mjs
  - lib/config-registry.mjs
  - lib/config.mjs
---

# prose-draft — delegated first drafts for file-derived close-out prose

<!-- kit block: frozen at the move out of the plugin (plugin-1-0 S3.3); nothing renders it now, and in this repo
     the local scripts/ copy always wins, so the pinned version below is only the fallback. -->
> **Running this skill's scripts.** Each `node scripts/<name>.mjs <args>` below means, from the project root:
> `if [ -f scripts/<name>.mjs ]; then node scripts/<name>.mjs <args>; else npx -y @golden-frijoles/kit@0.45.0 <name> <args>; fi`
> The project's own copy always wins. The kit needs no install and copies nothing into the repo. If npx fails on
> the network or the registry (ENOTFOUND, ECONNREFUSED, ETIMEDOUT, E404, a proxy error), report **could not
> look: the kit is unreachable**, not a broken project, and offer to retry online or to copy the script into
> `scripts/`. This covers the scripts the kit carries (`frijoles-kit --list`). Any other `scripts/` command here is
> project tooling: if the project lacks it, say so and stop. Never re-implement a script's logic inline.
> If a script prints `GF-NEEDS-SETTING {"key",…}`, ask the user that question once, save the answer with
> `npx -y @golden-frijoles/kit@0.45.0 config set <key> <value>` (always the kit, never local-wins: a project
> may own an unrelated `scripts/config.mjs`), tell them they can change it later the same way, and run the
> script again if it exited 7.
<!-- kit:end -->

## The contract (why this is safe to delegate)

- **File-derived inputs only.** The tool reads the epic directory's `*.md` + `git log --oneline`
  for that path. Artifacts whose real source is the builder's in-head context (PR bodies,
  incident narratives mid-flight) stay with the agent that holds that context.
- **Advisory stdout, never a repo write.** Output opens with an
  `EDIT BEFORE COMMITTING` banner. The coordinating agent is the editor of record.
- **The editor's factual pass is non-optional.** Known limit, observed on the first live
  dogfood: with thin sources the model invents plausible "owed" items and learnings. Verify
  every date, ref, and gap claim against the sources before committing a word.

## Usage

```bash
node scripts/prose-draft.mjs --kind retro       --epic Roadmap/<area>/<epic-dir>
node scripts/prose-draft.mjs --kind poster      --epic Roadmap/<area>/<epic-dir>
node scripts/prose-draft.mjs --kind sprint-wrap --sprint Roadmap/<area>/<epic>/sprint-N.md
```

The writer is the shared prose rail (`scripts/lib/prose-writer.mjs`) — the same one the standup and
weekly recap use: **devin → agy → codex**, one pinned model (`PROSE_MODEL`, deliberately not a Gemini
one), the shared persona (`prose/cpo-persona.md`) plus `prose/internal.task.md`, the project's
`prose-lessons.md` when present, and the prose guard with a revision pass. The draft's banner names
the writer and model that actually ran and whether the guard passed clean. If the agy pin check dies
on the agy path, run `node scripts/agy-doctor.mjs --fix` (pre-authorized) and commit the bump.

## Gotchas

- **The draft WILL fabricate specifics when sources are thin** — a retro drafted before the
  sprint docs carry commit refs produces confident placeholders and invented owed-items. Draft
  AFTER the sprint docs are ticked, and diff every factual claim against the sources.
- **A FLAGGED banner is not a failure to ignore** — the guard found a banned pattern (an invented
  ref, a stack name, a length breach) and the revision pass did not clear it. Read it before pasting.
- devin takes the prompt in a file, so large epic dirs are fine there; if the rail falls through to
  agy, its 256 KB argv cap applies and that writer is skipped rather than fed a truncated prompt.
- Epic-path **commit subjects** ride along with the docs into the model payload (that's the
  `git log` section). Nothing else does — no env, no diffs — but don't point it at a directory
  whose commit messages you wouldn't paste into a third-party model.
- `--kind sprint-wrap` output is a THIN POINTER by design (SESSION-KICKOFFS §7) — if the draft
  re-summarizes the sprint, cut it down; don't commit a re-summary.
