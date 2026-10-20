---
name: check-readability
description: "Checks whether the code is clear and easy to read."
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD, DECOMPOSITION_PROCEDURE]
  output: [CRITICAL_THINKING_STANDARD]
verification_spiral:
  tier: standard
  template_base: STANDARD_TIER_DEFAULT
  custom_dimensions:
    - name: "Primitive Coverage Completeness"
      threshold: ">= 4/5"
      standard_reference: "plugins/sulis/skills/codebase-assess/references/primitives.md CQ-01 + CQ-03"
      scorer: generating_agent
      evidence_required: "Existing naming/kitchen-sink/jargon + CQ-01 complexity + CQ-03 duplication all have status"
related_skills:
  - relationship: depends_on
    skill: code-health
    notes: invoked as wired tier 5 (Understandable) in code-health orchestrator
  - relationship: depends_on
    skill: _lib/baseline
  - relationship: depends_on
    skill: _lib/allowlist
  - relationship: depends_on
    skill: _lib/scope
  - relationship: depends_on
    skill: _lib/tools
  - relationship: depends_on
    skill: _lib/tools/lizard
    notes: NEW — to be created — covers CQ-01 cyclomatic complexity
  - relationship: depends_on
    skill: _lib/tools/jscpd
    notes: NEW — to be created — covers CQ-03 code duplication
---

# Check Readability

The stranger-reader check. Would a new person (or future-you) understand
this code? Audits naming, module cohesion, and jargon density. Reports
what's hard to read and why; recommends what to rename or split. Never
modifies code.

## What it checks

Three heuristic families. Per-finding scoring; combined into a single
legibility verdict.

1. **Naming clarity (per identifier)** — flags very short names that aren't
   loop variables, very long names, identifiers with high jargon density
   (mostly-uppercase-or-abbreviated chunks), and magic-string-prone names
   like `do_x`, `process`, `handle_data`.
2. **Module cohesion (per file)** — flags kitchen-sink files (default >1,500
   LOC with >4 distinct concerns) and files with unclear top-line purpose.
3. **Jargon density (per module)** — counts unexplained domain terms (terms
   absent from the project's known-vocabulary list — see *Resolved vocabulary*
   below). High density = stranger-reader bounce.

The audit is read-only. It NEVER modifies code. Rename suggestions are
advisory text only.

## Two modes

- **Founder mode (default).** Findings in plain English with FE-06 applied.
  Identifiers parenthetical to founder-readable labels. Plain-English
  remediation per finding. No internal IDs in chrome.
- **Operator mode (`--raw`).** Findings in JSON with `file:line` + heuristic
  name + raw metric values. For engineers wanting machine-readable output
  or for piping into other tools.

## Scope auto-detection

The audit runs against either a PR diff or the entire codebase. Detection
order:

1. If `--pr-number N` provided: fetch the PR diff via `gh pr diff N`. Scope =
   files in the diff.
2. Else if `--scope=pr` or `--scope=codebase` provided: respect the explicit flag.
3. Else: detect from local state.
   - On a feature branch with commits ahead of `--base-branch` (default
     auto-detected: `main`, `master`, `trunk`, or whatever HEAD diverged from):
     **PR scope** (audit only the diff).
   - On `main`/`master`/`trunk` with no diverging commits: **codebase scope**.
4. Override with `--scope=codebase` to force full audit even on a feature branch.

The detected base branch is reported in the verdict so the founder can verify
the right comparison ran.

## When invoked

1. **Resolve scope.** Run the auto-detection above. Echo the resolved scope
   and file count *before* the audit runs:
   *"Auditing 14 files in this branch's changes (comparing against main)."*
   or
   *"Auditing the whole codebase — 312 files."*
2. **Run the audit script.** All heuristics run; findings collected.
   ```bash
   python3 plugins/sulis/skills/check-readability/scripts/audit.py \
     --scope auto \
     [--base-branch BRANCH] \
     [--pr-number N] \
     [--raw] \
     [--kitchen-sink-threshold N]
   ```
3. **Translate to founder English** (founder mode only; skip in `--raw`).
   For each finding, apply the operator → founder translation table in
   `references/founder-translation.md`. Identifiers parenthetical
   (`observability_adapter.py` → `"the observability adapter file
   (observability_adapter.py)"`). Heuristic names → plain-English labels
   (`kitchen-sink-file` → `"this file is doing too many jobs"`).
4. **Present the verdict.** Use this template (omit empty categories):
   ```
   📖 Readability check — {scope description}

   Verdict: {clear / mostly clear / getting messy / hard to read}

   What I'd rename or restructure ({N} items):

   📛 Hard-to-read names ({M})
     • In the observability adapter file: the function `proc_d` could be
       `process_deploy` — it would explain itself.
       File: observability_adapter.py, line 47

   🗂  Files doing too many jobs ({K})
     • The work-package-lib file is 3,429 lines covering 6 distinct concerns
       (git operations, state machine, file IO, INDEX parsing, security
       findings, train run records). Worth splitting into focused files.
       File: _wpxlib.py

   🌫  Domain jargon a new person would struggle with ({L})
     • The term "wpx" appears 84 times across 12 files without explanation.
       Consider documenting in a glossary, or renaming to something
       self-explaining like "work-package-execution".

   The audit ran against {N} files. No code was changed.
   ```
5. **Resolved vocabulary** (footer). List the domain terms the audit
   recognised as legitimate (from `references/boring-code.md` if present,
   the project's GLOSSARY, etc.). So the founder can see what was NOT
   flagged and why.
6. **Handle shortcuts** if the founder asks for one.
   - **Safe shortcuts:** `[N] open file at finding`, `[d N] dismiss this
     finding from this run`. Echo-before-act per founder-facing-conventions.
   - **No rename shortcut.** The skill does NOT offer "press [1] to apply
     this rename across the codebase." Rename is a deliberate engineering
     change requiring a real refactor — not a one-keystroke action.

## Gotchas

- **PR-vs-codebase scope detection brittleness.** If your project uses a
  non-standard base branch, auto-detection might audit the wrong diff.
  Always check the echoed scope before trusting the findings. Override with
  `--base-branch` if needed.
  *Source: HD-008's INDEX-drift class; wpx-train's `_detect_branch_ci` fix.*
- **Operator jargon leakage in display strings.** Every founder-mode string
  must pass the FE-06 read-aloud test. If a finding still has
  `WP-AUTO-018` or `_wpxlib` as headline (vs parenthetical), it's a leak.
  *Source: founder-english.md anchor cases 3 + 4.*
- **False positives on legitimate domain vocabulary.** Words like `JOURNEY`,
  `HARDENING_DELTA`, `WP`, `concierge` look like jargon to a stranger but are
  load-bearing in this marketplace. The skill reads
  `references/boring-code.md` + the project's GLOSSARY (if any) and treats
  their terms as established. Founders can dismiss-as-domain-term with one
  key per finding.
  *Source: every codebase has its own vocabulary; flagging it as "jargon"
  is a false positive.*
- **Kitchen-sink threshold is opinionated.** Default 1,500 LOC + 4 concerns;
  too low = noise, too high = misses real cases. The threshold IS reported
  in the verdict so the founder can recalibrate. Override with
  `--kitchen-sink-threshold` (default 1,500). The canonical example we sized
  against: `_wpxlib.py` at 3,429 LOC.
  *Source: `_wpxlib.py` itself + the legibility critique earlier in this session.*
- **Destructive-action ambiguity (rename).** When the audit suggests
  "rename X to Y," the founder might press a shortcut expecting Claude to do
  it. The skill is read-only — there is NO rename shortcut. Rename is a
  refactor (touches every caller, breaks imports, requires review). The
  skill produces *suggestions*, not actions. Documented prominently in the
  presentation template.
  *Source: founder-facing-conventions.md Rule 3 (echo-before-act + prompt-before-destroy).*

## Vocabulary

- **stranger-reader** — the lens applied: would someone new to this
  codebase understand what each module / function / identifier does without
  external context? The audit asks this question of every name.
- **legibility** — the umbrella property the audit measures. Distinct from
  "readability" in the prose sense (which would include comment quality,
  documentation, etc.). Legibility = code-specific readability.
- **jargon-density** — ratio of unexplained domain-specific terms to total
  identifiers in a module. Threshold-based metric (default 0.15).
- **kitchen-sink-file** — a single file with LOC above threshold (default
  1,500) AND distinct-concern-count above threshold (default 4). Naming
  follows the `_wpxlib.py` archetype identified in this marketplace.
- **naming-clarity** — heuristic score combining identifier length, jargon
  presence, abbreviation density, and magic-name patterns
  (`do_x`, `process`, `handle_data`).
- **module-cohesion** — the inverse of kitchen-sink: how focused is each
  module? Heuristic based on function-count, concept-count, doc-coverage.

## When to invoke this skill

- Founder asks "is my code getting messy?", "could a new person read this?",
  "is the codebase clear?"
- Founder wants to check before opening a PR for review
- Founder is preparing to onboard a new contributor and wants to see what
  needs to be documented or renamed first
- After a major refactor — to see what cleanup the refactor revealed

## When NOT to invoke this skill

- Founder asks "is the code correct?" — use `sea:code-review` (PR-scope) or
  the future `/sulis:check-tests` (tier 3).
- Founder asks "is the code secure?" — use the future `/sulis:check-security`
  (tier 2) or `sulis-security:codebase-assess`.
- Founder wants an architectural audit (Form / Armor / Proof pillars) — use
  `sea:codebase-audit` (operator-facing; produces Hardening Deltas).
- Founder wants comprehensive multi-tier health — use the future
  `/sulis:code-health` (tier 5 included in the wrapper).
- Founder wants the code RENAMED or RESTRUCTURED — this skill suggests; it
  doesn't act. Take the suggestions into a real refactor session.
