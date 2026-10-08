---
name: go-live-audit
version: 1.1.0
description: |
  Author and run a project-TAILORED pre-launch audit as a bounded multi-agent workflow — a real launch
  verdict, not a checklist skim: fill the bundled workflow template from the repo's real stack and hard
  rules, then run Gates (typecheck / test / lint / build in parallel) → Find (one read-only finder per
  applicable audit dimension) → Dedup (merge shared-root-cause findings) → Verify (adversarial agents try
  to refute every finding; blockers get a code lens plus a spec lens) → Critic (name uncovered areas,
  spawn follow-up finders) → a GO / NO-GO / GO-WITH-FIXES report, all fanned out under a MAX_PARALLEL cap.
  Finders and verifiers stay read-only — the skill audits and reports, never fixes; a gate that didn't
  actually run is treated as a blocker, never counted clean; secret values are redacted to type and
  location. Confirms scope and warns about the agent count (typically 40-80) before running.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - Edit
  - Workflow
effort: high
argument-hint: "[repo path or launch context]"
arguments:
  - request
when_to_use: |
  Use when the user asks to audit a repo before launch, shipping, or release. Examples: "go live
  audit", "pre-launch audit", "launch readiness", "are we ready to ship", "final review before
  release", "deep audit of <repo>". It spawns dozens of agents over the whole repository, so confirm
  scope first. Do NOT use for a quick check of the current branch diff — redirect to
  branch-review-before-pr or the forked find-bugs for that; this is a whole-repo, multi-agent launch gate.
---

<EXTREMELY-IMPORTANT>
This skill authors and runs a multi-agent audit workflow. Non-negotiable rules:

1. You are *authoring* a fresh, project-tailored workflow from the bundled template — never run
   one fixed script blindly. Fill every `FILL:` marker before running.
2. The workflow architecture is load-bearing. Leave the schemas and the entire control-flow
   section of the template unchanged: Gates → Find → Dedup → Verify → Critic → report. The one
   exception is `MAX_PARALLEL` (the concurrency cap) — you may tune its value, but never remove the
   gate or the `gAgent` wrapper that enforces it.
3. Keep `meta` a pure literal (no variables, no interpolation) or the Workflow tool rejects it.
4. Finders and verifiers are read-only. They must never modify, create, or delete files, and
   never run builds or installs. Only gate agents execute commands (build may write `dist/`).
5. Never quote secret values in findings or evidence — report type and location only, redact
   the value with `<REDACTED>`.
6. Confirm scope and warn the user about the agent count (typically 40–80) before running.
7. These instructions authorize calling the Workflow tool — no separate opt-in is needed, but
   the scope confirmation and scale warning above are mandatory first.
</EXTREMELY-IMPORTANT>

# Go-Live Audit

## Inputs

- `$request`: Optional repo path, launch context, or focus guidance such as `audit ~/work/myapp before public beta` or `light pass, security only`

## Goal

Produce a credible launch-readiness verdict by generating and running a project-tailored
pre-launch audit workflow:

- **Gates** — typecheck / test / lint / build, run in parallel
- **Find** — one read-only finder agent per applicable audit dimension
- **Dedup** — an agent merges findings that share a root cause
- **Verify** — adversarial agents try to *refute* every finding; blockers and highs get a code
  lens plus a spec lens
- **Critic** — names uncovered areas, spawns follow-up finders, verifies them
- A structured GO / NO-GO / GO-WITH-FIXES report

All phases fan out through a global concurrency gate (`MAX_PARALLEL`, default 6) so a wide sweep
never puts more than that many agents in flight at once — the total agent count is unchanged, but
they run in bounded waves so Claude's API rate limits are not tripped.

## Step 0: Confirm scope

Establish, asking the user only if unclear:

- **Which repo** (absolute path). Default to the current working directory.
- **Launch context** — what "go live" means here: public release, first paying customers,
  internal GA. This shapes what counts as a *blocker*.

Do not ask more than necessary; infer from the repo when you can.

**Success criteria**: The target repo and launch context are explicit.

## Step 1: Discover the project

Read the repo enough to fill the template accurately. Gather:

- **Build/test commands** — inspect `package.json` scripts (and whether it is a pnpm/npm/yarn/bun
  workspace, turbo, etc.), or `Cargo.toml`, `go.mod`, `Makefile`, `pyproject.toml`. Determine the
  exact typecheck / test / lint / build command run from the repo root
  (`references/workflow-template.js` lists common commands per stack).
- **Layout** — apps/packages or src tree; the modules that exist.
- **Authority docs** — a spec/PRD, root `CLAUDE.md`, `README`, `docs/`. Note the order of
  authority (e.g. "spec > CLAUDE.md > code").
- **Product purpose** — one paragraph: what it is, who uses it.
- **Hard invariants** — rules the project must never violate (from the spec/CLAUDE.md): privacy
  guarantees, security/tenancy rules, "soft-fail everywhere", schema conventions, anti-features.
  If none are documented, derive sensible universal ones (data integrity, authz on sensitive
  reads, no committed secrets, green build/test/lint, no TODO/placeholder in shipping code).

Use Explore/Glob/Grep/Read freely here; this step determines audit quality.

**Success criteria**: Stack commands, layout, authority docs, product purpose, and hard rules are
all known well enough to fill the template without guessing.

## Step 2: Choose the finder dimensions

From `references/dimensions.md`, pick the **8–16 dimensions that actually apply** to this repo —
a CLI does not need multi-tenancy; a static site does not need money-math. Add any
project-specific dimensions the catalog misses.

Each finder must name **concrete files/dirs** to read and **specific, verifiable checks** — not
"review X for quality". Tie the worst checks to the project's hard rules.

**Success criteria**: Every chosen dimension has a real surface in this repo, and every finder
prompt is self-contained with concrete targets and checks.

## Step 3: Fill the template

Copy `references/workflow-template.js` and fill every `FILL:` marker:

- `ROOT` — absolute repo path.
- `meta` — keep it a **pure literal** (no variables/interpolation) or the Workflow tool rejects
  it. Update `description` to the project; keep the phase titles.
- `PRODUCT_CONTEXT`, `HARD_RULES` — from Step 1.
- `SEVERITY_DEFS` — replace the blocker examples with this product's launch-stoppers.
- `FINDERS` — the dimensions from Step 2.
- `STACK` — the detected commands; set any gate to `null` to skip it.

Leave the schemas and the entire control-flow section **unchanged** — they are generic. The only
value you may adjust there is `MAX_PARALLEL` (default 6): the cap on how many agents run at once.
Lower it (e.g. 4) if the account hits rate limits; raise it (e.g. 8–10) on a high-limit account for
more throughput. Do not set it to 1–2 (that serializes the audit) and never delete the gate itself.

**Success criteria**: No `FILL:` marker remains, `meta` is a pure literal, and the control-flow
section is byte-identical to the template.

## Step 4: Warn about scale, then run

Tell the user roughly how many agents this will spawn (finders + ~1–2 verifiers each + gates +
critic round — typically 40–80 agents *total*, but at most `MAX_PARALLEL` (default 6) run at once,
so the audit proceeds in bounded waves rather than hammering the API) so the cost and pacing are
expected. Then call the **Workflow** tool with `script` set to the filled-in template. Watch
progress via `/workflows`.

To iterate on the script, edit the saved `scriptPath` the tool returns and re-invoke Workflow
with `{scriptPath}` rather than resending the whole script.

**Success criteria**: The user knows the expected scale before the workflow starts, and the
workflow runs to completion.

## Step 5: Report

The workflow returns `{ gates, findings, finderNotes, stats }`. Render a launch readiness report:

- **Verdict** — GO / NO-GO / GO-WITH-FIXES, driven by gate failures and confirmed blockers.
- **Gates** — pass/fail per gate with failure excerpts.
- **Findings grouped by `status` then `severity`.** Lead with `confirmed` blockers and highs.
  Show `uncertain` separately (verifiers split). Omit or collapse `rejected` (verifiers refuted
  them) — mention the count, not the detail.
- For each surviving finding: severity, file:line, the issue, and the verifier reasoning. Note
  `alsoReportedBy` when multiple finders flagged it.
- **Coverage** — `stats` (raw vs deduped counts, finders reported, critic gap areas) and
  anything the critic flagged as uncovered.

**Success criteria**: The user can decide go/no-go from the report without re-deriving any
finding from scratch.

## Guardrails

- This skill audits and reports; it never fixes. Do not edit application code as part of this
  skill — hand confirmed findings to `bugfix` or the user.
- Keep finders and verifiers read-only; keep that discipline when editing prompts.
- Scale to the ask: fewer finders + code-only verification for a light pass; the full 16 +
  dual-lens verification + critic round for "audit everything".
- Severity is go-live-framed, not abstract — a blocker is something that must be fixed before
  *this* launch, judged against the project's hard rules.
- Never include secret values in findings, evidence, or the report — location and type only.
- Do not modify settings files or install anything on the user's behalf.

## When To Load References

- `references/workflow-template.js`
  The parameterized workflow. Read it before generating; copy it, fill every `FILL:` marker, run it.
- `references/dimensions.md`
  Catalog of audit dimensions to choose finders from, plus the finder-prompt style guide.

## Output Contract

Report:

1. verdict — GO / NO-GO / GO-WITH-FIXES with one-line justification
2. gate results with failure excerpts
3. confirmed blockers and highs with file:line, evidence, and verifier reasoning
4. uncertain findings (verifiers split) listed separately
5. rejected-findings count (not detail)
6. coverage stats and critic-identified gaps
