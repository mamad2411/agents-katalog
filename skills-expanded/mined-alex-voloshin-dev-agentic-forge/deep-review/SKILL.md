---
name: deep-review
description: Deep, multi-lens review of a non-trivial target (doc set, design, architecture, sizeable PR, or the working tree) — independent reviewers per lens, every finding verified against the source, one prioritized report with fixes. Use whenever the ask is for depth — a deep, thorough, rigorous or adversarial review, an audit for everything wrong, contradictions, gaps or risks, or a second opinion — even of a PR. A security audit is security-review; for a quick standard lint of a small diff use code-review.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Task
---

# Deep review

Run a high-fidelity review that resists single-pass blind spots (especially the author's own).
You orchestrate the [adversarial fan-out pattern](../../patterns/adversarial-review.md):
decompose → fan out independent reviewers → verify findings → synthesize one report.

## When to use

A non-trivial review where completeness and correctness matter: auditing docs or a design for
contradictions/gaps/risks, reviewing a sizeable change set, or an independent second opinion.
**Not** for a quick single-file diff lint (a single `reviewer` pass suffices), running the
app, or writing code.

## Process

1. **Scope the target and pick lenses.** Identify what's being reviewed (docs, design/ADR,
   code diff/PR, or the working tree) and select the relevant lenses from
   [references/lenses.md](references/lenses.md). Each lens is one angle a reviewer focuses on.
2. **Fan out.** Spawn one **fresh, independent** reviewer per lens (the `reviewer` role via a
   fresh subagent, or a general-purpose one — **never the `fork` type, which inherits your
   context and your standing directive**: [subagent-type rule](../../patterns/fan-out-fan-in.md#choosing-the-subagent-type))
   with *no* prior context, prompted
   **adversarially** ("assume problems exist; hunt them"). Require structured findings: each
   with `severity` (`blocker | major | minor | nit`), `location`, `issue`, `evidence`, `fix`
   (the suggested fix — same key as the workflow template's schema).
   The pattern's external reviewer lens, if you add it, is
   `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/external_review.py" --target <file> --repo <the repo it belongs to> --kind code`;
   its exit 3 is a lens that failed (not a skip): name it among the lenses lost in the report.
   Run them concurrently with the Task tool — or, when the user has opted into multi-agent
   orchestration, with a Workflow built from
   [references/workflow-template.md](references/workflow-template.md) (canonical finding/verdict
   schemas, per-lens retry, loss disclosure — do not re-invent the harness per run). **Scale the
   count to the target**: a small target (one file, a short document) gets one or two lenses — one
   fresh reviewer that verifies and reports in the structured shape *is* the deep review of it; a
   five-way fan-out over a 24-line document is disproportionate. The full catalog is for "audit
   everything".
3. **Verify** every substantive finding against the source yourself before accepting it —
   open the file, re-run the check. Re-running a check is this session's job: the `reviewer` and
   `security-engineer` lenses are held to reading by the `role_scope` hook, so a lens verifies with
   `git show <base>:<path>`, `git log` and `git blame`, and asks you for any run it needs. Drop
   or downgrade what doesn't hold; keep a note of notable false alarms with the reason. This
   step is non-negotiable: it is what keeps the review trustworthy rather than a pile of guesses.
4. **Dedupe & prioritize** across lenses by severity.
5. **Synthesize** one report (see Output). Note clean areas explicitly so silence reads as
   "checked", not "missed".
6. **Apply (only if asked).** Apply the agreed findings, then re-run the relevant gate
   (`python dev/validate.py` + `pytest` for this repo, or the project's gate) and report it.

## Output

A single prioritized report:

- **Findings**, worst-first: `severity` · `location` · what's wrong · concrete fix · (which
  lens / evidence).
- **Filtered** — findings that did not survive verification, with the reason (so the caller
  trusts the rest).
- **Clean** — areas checked and found sound.
- If fixes were applied: what changed and the re-gate result.

## Knobs

- **Breadth/effort** — number of lenses and reviewers; default to the lenses that fit the
  target, expand for "audit everything".
- **Verify rigor** — for high-stakes claims, use multiple independent verifiers and keep a
  finding only if a majority confirm.
- **Apply fixes** — off by default; only when the user asks to fix, not just review.

## Definition of done

- Findings are verified against the source (no unconfirmed speculation presented as fact).
- The report is deduplicated and prioritized; clean areas and filtered false alarms are
  stated.
- If fixes were applied, the gate is green and the numbers/result are reported.
