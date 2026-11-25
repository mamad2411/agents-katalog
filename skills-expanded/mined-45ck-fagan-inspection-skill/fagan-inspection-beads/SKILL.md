---
name: fagan-inspection-beads
description: Run a Fagan Inspection and create Beads issues from the defect log. Requires the fagan-inspection skill for the core review; this add-on converts defects into trackable Beads tasks with priorities and dependencies.
argument-hint: "[optional scope hints] [--include-minor]"
disable-model-invocation: true
---

Run a **Fagan Inspection** on the current change set, then create **Beads issues** from the defect log so defects become trackable tasks.

This is an add-on to `fagan-inspection`. Run the full five-phase inspection first, produce the consolidated defect log, then pipe defects into Beads.

---

## Phase 1: Run the Fagan Inspection

Execute all five phases of a standard Fagan Inspection (scope, plan, domain reviews, synthesis, rework). Produce the full **Fagan Inspection Report** with the consolidated defect log table before proceeding.

Use existing chat context for intent and acceptance criteria. If missing, derive scope from git (status, staged/unstaged diff, PR-range diff vs `origin/main` or `origin/master`).

### Inspection phases (same as core skill)

**A) Scope** -- Summarize impacted modules/files and externally visible behavior changes.

**B) Plan** -- Define Entry/Exit Criteria. Choose reviewer domains dynamically (correctness, security, performance, reliability, API/design, tests, docs, ops, data/migrations, concurrency, UI). Spawn parallel subagents per domain if supported; otherwise run sequentially.

**C) Preparation** -- Each domain reviewer outputs defects with: Title, Severity (MAJOR|MINOR), Domain, Location (file:line or symbol), What/Why + Evidence, Fix (specific change), Verify (test/command/scenario).

**D) Synthesis** -- De-duplicate, re-severity, prioritize. Produce a single defect log + rework plan.

**E) Rework** -- Fix MAJOR first if write permissions allow; otherwise give patch-level edits. Re-run checks/tests. Confirm Exit Criteria.

---

## Phase 2: Beads Integration

### Step 1 -- Detect Beads

Check if the `bd` CLI is available:

```bash
command -v bd
```

**If `bd` is not found:** Stop here. Output the Fagan Inspection Report only, and append:

```
## Beads Integration: Skipped

`bd` CLI not found. To install Beads and create trackable issues from this defect log:

  pip install beads-cli
  # or see https://github.com/steveyegge/beads

Then re-run: /fagan-inspection-beads
```

**If `bd` is found:** Continue to Step 2.

### Step 2 -- Initialize Beads (if needed)

Check if the repo is already initialized:

```bash
bd ready --json
```

If that fails (no `.beads/` directory, not initialized):

```bash
bd init --stealth
```

Use `--stealth` so Beads metadata is not committed to the main repo. This keeps the integration non-invasive.

### Step 3 -- Create parent inspection issue

Create one parent issue to group all defects from this inspection:

```bash
bd create "Fagan Inspection: <current-branch> — <short-summary-of-scope>" -p 1 --json
```

Capture the parent issue ID from the JSON output. Store scope, intent source, and exit criteria in the parent:

```bash
bd update <parent-id> --description "<1-2 sentence scope summary>" --acceptance "<exit criteria from the inspection>" --notes "Inspection date: <today>. Intent source: <chat|git>. Domains reviewed: <list>."
```

### Step 4 -- Create child issues per defect

For each defect in the consolidated defect log:

**MAJOR defects** -- always create:

```bash
bd create "[MAJOR] <defect-title>" -p 0 --json
```

**MINOR defects** -- create only if the user passed `--include-minor` in the invocation arguments. Otherwise skip and note them in the output.

For each created issue, immediately update with structured fields (do NOT use `bd edit` which opens an interactive editor):

```bash
bd update <child-id> --description "<what/why + evidence>" --notes "Domain: <domain>. Location: <file:line>. Evidence: <repro steps>." --acceptance "<verify steps from defect>"
```

Then link child to parent:

```bash
bd dep add <child-id> <parent-id>
```

### Step 5 -- Claim and verify

After all issues are created, show actionable next steps:

```bash
bd ready --json
```

---

## Output

Return a combined report with two sections:

### Section A: Fagan Inspection Report

1. Scope & intent source (chat or git)
2. Entry/Exit criteria
3. Overview + top risks
4. Defect log (table: ID | Sev | Domain | Location | Title | Status | Fix/Next)
5. Rework summary (if applied)
6. Verification evidence (commands/tests)

### Section B: Beads Integration Summary

1. **Status:** initialized | already-initialized | skipped (with reason)
2. **Parent bead:** `<id>` -- `<title>`
3. **Created defect beads:** table of Bead ID | Severity | Defect Title | Priority
4. **Skipped defects:** list with reasons (e.g., "MINOR, --include-minor not set")
5. **Next actions:** output of `bd ready --json`
