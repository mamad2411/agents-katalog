---
name: forge-skill-from-docs
description: "Turn a repository's own checked-in documentation into an executable skill. Scan the repo's docs (docs/**, README, CONTRIBUTING, .github/**) for a repeatable operational runbook — ordered steps, shell commands, prerequisites, verification, failure modes — then forge a reusable SKILL.md that encodes that procedure as Conditions/Interface/Policy/Termination so a future agent can run it correctly instead of re-reading prose. Reads only the local checkout (no network, no session history), so it runs cleanly in cloud-agent automations. Triggers: forge skill from docs, turn runbook into a skill, generate skill from documentation, docs to skill, codegen runbook skill, build a skill from CONTRIBUTING."
user-invocable: true
---

# Forge Skill From Docs

Most repos already document their tricky procedures — regenerating protobuf code,
updating a submodule, bootstrapping a dev environment — in `docs/`, `README`, or
`CONTRIBUTING`. But prose runbooks are re-read and mis-followed every time. This skill
**mines the repo's own documentation** for the strongest procedural runbook and **forges
a skill**: a `SKILL.md` that encodes that procedure as a formal **Conditions (C) /
Interface (R) / Policy (π) / Termination (T)** model a future agent can execute directly.

Its evidence source is the **local checkout** — plain files read with `glob`/`grep`/`view`.
That means **no network egress and no session-store access**, so it is unaffected by the
automation-sandbox firewall, which makes it well suited to run inside a cloud-agent (CCA)
automation.

The output is a set of files written to a run directory for human review. This skill never
commits to any repo and never calls artifact-placement itself — surfacing the proposal as a
GitHub issue is an optional, separate downstream step.

## Contents

- [1. Inputs](#1-inputs)
- [Prerequisites](#prerequisites)
- [2. Why this source is robust](#2-why-this-source-is-robust)
- [3. Procedure](#3-procedure)
- [4. Generated skill schema](#4-generated-skill-schema)
- [5. Validation gate](#5-validation-gate)
- [6. Output contract](#6-output-contract)
- [7. Safety defaults](#7-safety-defaults)

## Helper scripts

| Script | Purpose |
| --- | --- |
| `scripts/scan_docs.py` | Scan a checkout's docs; rank by procedural signal; extract title, headings, command blocks, prerequisites, gotchas. |
| `scripts/validate_skill.py` | Mechanically gate the generated `SKILL.md` (frontmatter + C/R/π/T sections). |

---

## 1. Inputs

Establish these when invoked (sensible defaults below — ask the user only if the goal is unclear):

- **Target repository** — the repo whose docs to mine, given as an **explicit input**
  (`owner/name` NWO **and** the path to its checkout). **Never hardcode a repo.** In a
  cloud-agent automation the target is already checked out at the workspace root; use that
  path as `--root`. The skill reads only files under `--root`.
- **Doc globs** (optional) — which files count as "documentation." Defaults to
  `docs/**/*.md`, `doc/**/*.md`, `README*.md`, `CONTRIBUTING*.md`, `.github/**/*.md`.
  Pass `--glob` (repeatable) to override.
- **Topic** (optional) — a keyword to prefer when several runbooks exist (e.g. `proto`,
  `submodule`, `release`). Docs matching the topic are boosted; off-topic docs are
  heavily deprioritised. Omit to let the highest procedural score win.
- **Output directory** — a fresh run directory **outside** the checkout (e.g.
  `docs-forge-run-<timestamp>/`). All run artifacts live here; **never write into a repo**.
- **Thresholds** (optional) — `--min-score` (default 5; the procedural-signal floor below
  which a doc is treated as narrative, not a runbook).

The proposed skill is written to **`$RUN_DIR/<name>/SKILL.md`** for a human to review and
install. `.github/skills/**` of any repo is touched only by the human reviewer who approves
the proposal.

### Prerequisites

This skill's evidence source is the **local filesystem** (the target repo's checkout), read
with built-in tools. It needs **no feature flag and no network**:

- **No session-store access** — there is nothing to query in any session store; this skill
  reads only files, so no related feature flag or query restriction applies.
- **No network/firewall dependency** — `scan_docs.py` only reads files under `--root`. The
  automation sandbox firewall (which blocks `gh api` / `curl`) is irrelevant.
- **The docs must actually be present in the checkout.** In a CCA automation the repo is
  checked out at the workspace root; confirm `--root` points at it and that the doc globs
  match real files before forging.

If the repo has no procedural documentation (no runbook clears `--min-score`), report that
and stop — do not invent a procedure.

---

## 2. Why this source is robust

This skill mines the repo's **own checked-in documentation** — plain files read with
`glob`/`grep`/`view`. Its evidence is human-authored intent ("here is the correct
procedure"), not observed behaviour or any external state.

That makes it:

- **Deterministic and reproducible** — the same doc forges the same skill every run, with
  no seeding ritual and no dependency on prior agent activity.
- **Fully self-contained** — it reads only the local checkout, so it has **no dependency on
  the session store and no network egress**. The automation-sandbox firewall (which blocks
  `gh api` / `curl`) and any session-store data quirks are irrelevant.

The forged skill is emitted in a formal **Conditions / Interface / Policy / Termination
(C/R/π/T)** shape, ready for a human to review and install.

---

## 3. Procedure

### Phase 1 — Read what already exists (don't duplicate)

Read the target repo's `.github/copilot-instructions.md` and `.github/skills/` for any skill
that already encodes the procedure you are about to forge. If one exists, prefer
`improve_existing_skill` over creating a duplicate.

### Phase 2 — Scan the docs and rank runbooks

```bash
SKILL_DIR="<this skill's directory>"
ROOT="<path to the target repo's checkout>"          # e.g. the automation workspace root
RUN_DIR="$(pwd)/docs-forge-run-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$RUN_DIR"

# Rank docs by procedural signal and extract their raw material.
# Add --topic <kw> to prefer a specific runbook (e.g. --topic proto).
"$SKILL_DIR/scripts/scan_docs.py" --root "$ROOT" --topic "<optional>" \
  --out "$RUN_DIR/docs-candidates.json"
```

`docs-candidates.json` ranks every procedural doc by `score`, with a `signals` breakdown
(`shellBlocks`, `numberedSteps`, `structuralHeadings`, `prerequisiteHits`, `verifyHits`,
`gotchaHits`, `topicMatch`) and the extracted `title`, `headings`, `commands`,
`prerequisiteCommands`, and `gotchaLines`. If `candidateCount` is 0, stop (no runbook to forge).

### Phase 3 — Pick the runbook and read it in full

Take the top candidate (or the best `topicMatch`). **Open the actual doc** (`view` the
`path`) and read it end-to-end — `scan_docs.py` extracts signals, but you author the skill
from the real text. Confirm the doc describes a genuine, repeatable procedure (not a one-off
note) and that its commands are intrinsic to the repo.

### Phase 4 — Author the skill (write to `$RUN_DIR`, never to a repo)

Write `$RUN_DIR/<name>/SKILL.md` following the [Generated skill schema](#4-generated-skill-schema).
Map the doc's content onto the formal model:

- **Conditions (C)** — when the procedure applies (the doc's "When to…" / trigger section).
- **Interface (R)** — the entry-point command sequence (the doc's "Procedure" / "Steps").
- **Policy (π)** — the ordering and prerequisites (what must run first, and why), drawn from
  `prerequisiteCommands` and the doc's prerequisite section.
- **Termination (T)** — the verification + failure modes (the doc's "Verify" and "Gotchas":
  success check, and what a known failure means / how to recover).
- **Always do / Never do** — the doc's Do/Don't guidance.

Preserve **exact** commands and file paths from the doc — never paraphrase a command. Cite the
source doc path in the skill body so a reviewer can trace each rule back to the runbook.

Also write `$RUN_DIR/docs-forge-summary.md`: the decision
(`create_skill | improve_existing_skill | hold_as_pattern_only`) + rationale, the candidate
table, the evidence→C/R/π/T mapping (which doc lines became which section), the comparison
against any installed skills, the validation result, and a 🚩 gaps/caveats section (thin or
ambiguous docs, steps the doc leaves implicit, etc.).

### Phase 5 — Validate and emit

```bash
"$SKILL_DIR/scripts/validate_skill.py" "$RUN_DIR/<name>/SKILL.md"   # exit 0 required
```

Fix any hard failures, then report the **absolute paths** of every file written to `$RUN_DIR`.
Do not commit to any repo and do not open a PR.

---

## 4. Generated skill schema

### Frontmatter (required)

- `name` (kebab-case, 1–64 chars, **matches the directory name**)
- `description` (what it does + when to use it, with trigger keywords). **Wrap the value
  in double quotes** — descriptions contain `Triggers: …` (a colon + space), which YAML
  otherwise reads as a nested mapping, making the skill fail to load.
- `allowed-tools` — a **comma-separated string** (e.g. `bash, view`), **not** a YAML
  array. The runtime skill loader parses this field as a string; a `["bash", "view"]`
  sequence fails to unmarshal and the whole skill is silently skipped at load time.
- `tags`
- `generated-by: forge-agent`

### Body sections (required, in order)

1. `# <Skill Title>`
2. `## Purpose`
3. `## Conditions (C)` — when this procedure applies (the doc's trigger conditions)
4. `## Interface (R)` — entry point + the exact command sequence
5. `## Policy (π)` — ordering + prerequisites (what must run first, and why)
6. `## Termination (T)` — success check + known failure modes / recovery
7. `## Always do`
8. `## Never do`
9. `## Gotchas / edge cases`
10. `## Source` (cite the doc path the skill was forged from)
11. `## Scope boundaries`

Keep frontmatter compact and discovery-oriented; keep the body concise and operational.
Preserve exact commands and paths — never substitute paraphrased steps.

---

## 5. Validation gate

Before promotion, confirm:

1. schema completeness (frontmatter + all required sections + C/R/π/T)
2. minimal-instruction executability (a fresh agent could follow R/π and reach T)
3. **fidelity to the source doc** — every command/path in the skill appears verbatim in the
   doc; no invented steps
4. the prerequisites and ordering are **internally consistent** (the π ordering matches the
   doc, and the T failure modes match the gotchas)
5. no conflict / duplication with nearby skills or `copilot-instructions.md`
6. the `## Source` section cites the exact doc path

`validate_skill.py` enforces (1) mechanically; you own (2)–(6).

---

## 6. Output contract

The run's deliverable is the set of **files written to `$RUN_DIR`** (Phase 5). Produce:

1. **`docs-forge-summary.md`** — decision + rationale, the candidate table, the
   evidence→C/R/π/T mapping, the comparison against installed skills, the validation result,
   and a 🚩 gaps section (thin/ambiguous docs, implicit steps, or why held).
2. **`<name>/SKILL.md`** — the full proposed skill (in its installable directory) (omit only
   if `hold_as_pattern_only`).
3. **`docs-candidates.json`** — the ranked scan evidence.

Then report the **absolute paths** of the written artifacts. Do not commit to any repo and do
not open a PR. Surfacing the artifacts as a GitHub issue (via `artifact-placement`) is an
optional, separate downstream step — not part of this skill.

---

## 7. Safety defaults

- **Never invent a procedure.** Only forge from a doc that clears `--min-score` and that you
  have read in full. Thin/ambiguous docs → emit a summary that says so and
  `hold_as_pattern_only`.
- **Fidelity over polish.** Preserve the doc's exact commands and paths; do not "improve" a
  command you cannot verify against the repo.
- **Cite the source.** The forged skill's `## Source` section must name the doc it came from.
- **Read-only on every repo.** Mine the checkout, propose to `$RUN_DIR`, stop. A human installs.
- **Target repo is an explicit input.** Never hardcode a repo or assume a default — scan only
  the checkout you were given via `--root`.
