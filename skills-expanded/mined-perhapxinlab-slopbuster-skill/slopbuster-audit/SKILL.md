---
name: slopbuster-audit
license: Apache-2.0
description: Audit a repository or diff for AI slop, dead/mock/fake code, duplication, architecture drift, performance problems, and technical debt. Use when asked to review code quality, run a codebase health check, clean up a project, find slop/tech debt, or review a PR. Also has a user-journey simulation mode that war-games real usage step by step to catch redundant steps, breakage, and confusing flows. Produces a structured score master, an executive overview with prompt-your-agent guidance, a prioritized fix plan, and per-category reports with a health score.
---

# SlopBuster — Audit

You are auditing a codebase for the things AI-generated code accumulates silently:
slop, dead weight, drift, and debt. Your output is a **decision**, not a tour —
prioritized, specific, and actionable.

## Three modes — pick by intent

- **Repo audit** — the whole codebase, or a subsystem. Go file-by-file: every file
  matters, *changed or not*. Slop hides in files nobody reviewed. This is the signature mode.
- **Diff / PR review** — only the changed surface, judged against the architecture
  it lives in. Faster, gate-style.
- **Simulation (user-journey war-game)** — don't read code for slop; instead role-play a
  real user and walk each flow step by step, reasoning about what actually happens at every
  step, to surface redundant steps, points that break, and confusing or wrong behavior. This
  is a behavioral/UX audit, not a static one — follow [references/simulation.md](references/simulation.md)
  and use its output shape instead of the report format below.

If the user didn't say which, ask once, then proceed. The first two share everything below;
simulation diverges per its reference.

## Before reading any code

1. **Reconstruct intent.** What does this system do? What's the stack? Is the area
   under audit sync / streaming / async, agent-based / plain?
2. **Detect the stack** from manifests and layout (`pyproject.toml`/`requirements.txt`,
   `Cargo.toml`, `package.json` + `next.config`). Load the matching review pack:
   - Python (Quart-style backend) → [references/python-review.md](references/python-review.md)
   - Rust backend → [references/rust-review.md](references/rust-review.md)
   - Next.js / React / TS frontend → [references/frontend-review.md](references/frontend-review.md)
3. Always load [references/repo-audit.md](references/repo-audit.md) — the stack-agnostic
   detection catalogue and the comment-cleanup pass.

With intent reconstructed, the stack detected, and the review pack loaded, you have the
architecture in view. Now read file-by-file.

## File-by-file coverage is mandatory — read every file, never from memory

This is the non-negotiable core of the audit. **Working from memory, prior context, a summary,
a diff, or a changelog is forbidden** — it produces a fake audit that misses the real bugs.

1. **Enumerate the full file set first.** Glob every source file in scope (exclude only
   build/vendor dirs) and write the list down. State the count. This list is your checklist.
2. **Open and read each file's full contents with the Read tool — every one, end to end.** Not a
   grep sample, not the first screen, not "I recall this file." If a file is long, read it in
   successive chunks until you've seen all of it. A file you did not actually open does not count
   as audited.
3. **Track coverage explicitly.** Keep a running tally of files read vs. the enumerated list. The
   audit is **invalid and must not be reported as complete** until every file in the list has been
   opened and read. In the final report, state coverage as `N/N files read` and, for a focused
   audit, list them.
4. **Trace, don't pattern-match.** Real bugs live in the logic and the data path, not at a keyword.
   Grep is only for *locating* things to then read — never a substitute for reading. See the
   inspection method in `repo-audit.md`.

Do not claim a file is "fine" or "unchanged" without having read it in this pass. Re-reading a file
you wrote earlier in the same session still counts as reading only if you actually open it now —
your memory of it is not evidence.

## What to find

Sweep every file (read per the protocol above) for, at minimum:

- **Dead weight** — dead code, unused imports/functions/variables, unreachable branches.
- **Fake work** — mock/stub/fake implementations left in place, `TODO` explosions,
  hallucinated architecture (abstractions for things that never arrived).
- **Duplication** — repeated logic, copy-paste blocks, parallel implementations of one idea.
- **AI slop** — generic naming, over-engineering, wrapper hell, abstraction hell,
  layers that add indirection without adding meaning.
- **Architecture** — broken module/service/domain boundaries, wrong dependency
  direction, circular dependencies, responsibility leaks across layers.
- **Correctness & logic** — wrong conditionals, off-by-one, mishandled edge cases,
  swallowed errors, async/concurrency races, bad state mutations, contract mismatches.
  These are found by reading and tracing flow, not by keyword search.
- **Security** — untrusted input reaching a sink (injection/XSS/SSRF/path traversal),
  missing or misplaced authn/authz, IDOR, leaked secrets/PII, weak crypto, missing rate
  limits, insecure defaults, vulnerable dependencies. Trace input from entry to sink.
- **Performance** — N+1 queries, missing cache, sequential awaits that could be parallel,
  redundant computation, obvious bottlenecks.
- **Maintainability** — files too large, functions too long, a class doing too much,
  excessive nesting, folder/module layout that fights the domain.
- **Comments** — keep what explains *why*; remove history, redundant restatement of the
  code, and dead narration. See the comment-cleanup pass in `repo-audit.md`.

For sizing/boundary problems, propose a **concrete split** — which file/function/class,
into what, why.

## Output: a structured master + signature docs + one file per category

The audit's findings do **not** go into one giant document. They are split **by category**, one
markdown file per category, with a structured `scores.json` master on top that the app reads, plus
two whole-audit docs — `overview.md` and `fix-plan.md`. This keeps any single document small enough
to read and edit, and drives the desktop app's master-detail UI (left = the scores overview, right =
the selected category's findings, with a severity filter and a dashboard gauge driven by the
structured fields).

**Categories are not a fixed list — adapt them to the project.** Default to the six dimensions
below, but add, rename, drop, or split them to fit what this codebase actually is (a pure library
has no auth surface; a data pipeline may want a "Data Integrity" category; a CLI may fold
Security into Correctness). Each category you keep becomes one `scores.json` entry **and** one
markdown file.

Default dimensions: **Security, Correctness, Architecture, Performance, Maintainability,
AI-Slop/Debt**.

Order categories by severity (most damaged first). Within each category file, order findings by
severity, highest first. Every finding cites `file:line` and says what to do, not just what's
wrong.

**Be exhaustive about real issues — list every one, large and small.** A genuine audit of a
sizable codebase routinely surfaces *hundreds* of findings across severities; do not stop at the
headline issues or a representative sample, and do not drop the minor ones (a dead import, a
generic name, a missing edge case is still a finding worth a line). "Don't pad" means don't
fabricate, restate, or inflate — it never means omit a real issue. The per-category md files must
be **complete**, not a summary — the full finding set lives there.

### Repository Health Score (required)

Always produce a single overall grade for the whole audit on the `A+ A B C D F` scale, backed by
the per-category grades. The overall grade is **not an average** — a failing Security or
Correctness category caps it. Alongside the letter, carry an overall `numeric` (0..100) that drives
the dashboard gauge; it is **capped the same way**, not averaged — a failing Security or Correctness
category pulls it down regardless of how the other categories scored. This overall grade and number,
plus the per-category grades, is exactly what `scores.json` carries (below). Never end an audit
without it.

## Persist the audit (automatic) — manifest + per-category files

Each kind of SlopBuster artifact lives in **its own folder** (`audit/`, `plan/`, `docs/`), one
versioned subdir per run. Write the audit into a dated subdir of `.slopbuster/audit/` at the repo
root:

```
.slopbuster/audit/<YYYY-MM-DD>/
  scores.json        ← structured master, the app reads this first
  overview.md        ← whole-audit executive outline + how-to-prompt-your-agent guidance
  fix-plan.md        ← prioritized, dependency-ordered remediation plan
  security.md        ← one file per category, full findings for that category only
  correctness.md
  architecture.md
  …
```

Create the directory if it doesn't exist; get the date from the system (`date`). If the app passes
an explicit versioned target dir (e.g. `.slopbuster/audit/v3-<date>/`), write `scores.json` and the
category md files into that dir instead. If the user named a different location, use that. Tell the
user the directory path when finished.

### `scores.json` — the structured master (write first or last, but keep it consistent)

```json
{
  "overallGrade": "A+|A|B|C|D|F",
  "numeric": 61,
  "summary": "<overall status prose, a short paragraph>",
  "overviewDoc": "overview.md",
  "fixPlanDoc": "fix-plan.md",
  "meta": {
    "generatedBy": "<tool + model, e.g. 'claude-code / claude-opus-4-8' — never blank>",
    "author": "<git log -1 --format=%an>", "email": "<git log -1 --format=%ae>",
    "commit": "<git rev-parse HEAD>", "branch": "<current branch>",
    "generatedAt": "<ISO-8601 — date>"
  },
  "categories": [
    {
      "key": "security", "label": "Security", "grade": "D", "numeric": 58,
      "summary": "<1–2 line status of this category>", "doc": "security.md",
      "findingsCount": 18,
      "severityCounts": { "critical": 1, "high": 6, "medium": 11, "low": 0, "info": 0 },
      "findings": [
        { "n": 1, "severity": "critical", "title": "...", "file": "crates/...", "line": 647,
          "effort": "S", "what": "what's wrong and why it matters (prose)",
          "fix": "the concrete fix (prose)" }
      ]
    }
  ]
}
```

- `overallGrade` — the capped overall (a failing Security or Correctness category caps it), not an
  average. `numeric` is the matching overall 0..100, capped the same way; it drives the gauge.
- `overviewDoc` / `fixPlanDoc` — the filenames of the two whole-audit docs (`overview.md`,
  `fix-plan.md`).
- `meta` — attribution for the report: who/what generated it (`generatedBy`, never blank) and the
  git author/email/commit/branch/date. Powers the desktop + cloud "who ran this, on which commit"
  detail. Same shape across all SlopBuster skills.
- `categories[]` — **one entry per category you actually wrote** (flexible set, see above). `key`
  is a stable slug; `label` is the human title; `grade`/`numeric` (0..100) are that category's
  sub-grade; `summary` is a 1–2 line status; `doc` is the md filename for that category. Order by
  severity, worst first.
- `findings[]` is the **complete** structured finding set for the category — the same findings as
  the category md, not a sample. `severity` ∈ `critical | high | medium | low | info`; `effort` ∈
  `S | M | L` or null; `line` is a number or null (null for an architecture-wide finding with no
  single line); `n` is 1-based within the category, severity-ordered (critical first); `what` and
  `fix` are prose. `findingsCount` and every `severityCounts` bucket must equal what `findings`
  actually contains.

### Write rich, scannable markdown — not walls of text

Every md you write (the category files, `overview.md`, `fix-plan.md`) and the `what`/`fix` fields in
`scores.json` must read like a **proper report**, not a dense paragraph dump. Dense prose scares the
reader and hides the action. Use the full markdown toolbox:

- **Headings & subheadings** (`##`, `###`) to chunk a long document into navigable sections.
- **Bullet and numbered lists** — especially every **fix as ordered, step-by-step actions** (`1.`
  `2.` `3.`), each an imperative the reader can execute, not one run-on sentence.
- **Tables** for anything comparative or tallied — a severity/count summary, a per-file or
  per-module breakdown, a before/after, a checklist with status.
- **Inline `code`** for symbols/paths/values and **fenced code blocks** for the concrete snippet a
  fix should produce or replace.
- **Bold** for the load-bearing phrase in a sentence, and **blockquotes** for a key caveat.

Lead each document with a short orientation, then break the rest into sections. The bar: a developer
skimming it should grasp the shape in seconds and find the exact step they need without reading a
wall of text.

### One markdown file per category (write each one separately)

For every category in `scores.json`, write its own focused md file named by the `doc` field
(`security.md`, `correctness.md`, …). Write each in its **own** Write call so no single document
holds the whole audit. Each file contains the **complete** findings for that category only,
severity-ordered, **numbered `1. 2. 3.` to match each finding's `n`** in `scores.json`, each with
`file:line`, what's wrong, and the concrete fix (with a rough effort size S / M / L). The md is the
readable export of the same findings the structured `findings[]` carries; the two must agree, and
the manifest's `findingsCount` for the category must match what the file contains.

### `overview.md` — the signature export (write separately)

One whole-audit document, named in `overviewDoc`. Two parts:

- **Executive outline** — what the system is, the headline verdict, and the worst areas, in prose.
  This is the read-aloud summary of the whole audit.
- **How to prompt your AI agent / how to improve** — aimed at vibe coders who build by prompting an
  AI. Turn the recurring problems you found into forward-looking, reusable guidance: the rules,
  constraints, and checklists they should paste into future prompts so these *classes* of issue
  don't recur. This is the highest-value section — generalize from the findings into prompt-time
  prevention, don't just restate them.

### `fix-plan.md` — the remediation plan (write separately)

One whole-audit document, named in `fixPlanDoc`. A prioritized, dependency-ordered remediation plan:
numbered steps grouped into phases (quick wins → structural), ordered so prerequisites come before
the work that depends on them, each step citing `file:line` and an effort size (S / M / L). This is
the audit's remediation output — what to fix and in what order — not a from-scratch planning
artifact.

The full field-by-field contract is in
[references/output-contract.md](references/output-contract.md).

(Simulation mode does not use this layout — it writes into its own `.slopbuster/simulation/` folder
per [references/simulation.md](references/simulation.md).)

## Working in stages (large repos)

A big codebase won't fit one pass. Build the per-category md files up in stages instead of trying
to hold everything at once:

- Audit subsystem by subsystem, appending findings into the relevant category file as you go.
  Cluster by module and start at the hotspots — the entry points, the largest files, the
  most-imported modules.
- **Re-read what you already wrote** as you go. Later files routinely explain or contradict
  earlier findings — when they do, go back and update, merge, or downgrade the earlier note.
- **Compare across the codebase.** Many of the most valuable findings are blueprint-level: the
  same logic duplicated in three subsystems, an inconsistent boundary, a pattern that's right in
  one module and wrong in another. These only surface by holding the accumulating files against new
  files. Promote them into the Architecture category.
- The category files are working documents until the final pass: revisit, reconcile, and only then
  write `scores.json` with grades, structured `findings[]`, `severityCounts`, and `findingsCount`
  that all match the finalized files — then derive `overview.md` and `fix-plan.md` from the settled
  finding set. Coverage stays the bar — staging is how you reach 100% on a large repo, not an excuse
  to stop early.
