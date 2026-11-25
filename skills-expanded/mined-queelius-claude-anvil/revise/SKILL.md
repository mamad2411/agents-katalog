---
name: revise
description: >-
  Apply fixes from a multi-agent review report. Launches the reviser
  orchestrator, which triages the findings in .papermill/reviews/, dispatches
  section-writer specialists per finding domain, verifies each fix with the
  owning review specialist, and writes a revision report paired with the
  review. Closes the draft, review, revise loop. Updates .papermill/state.md.
argument-hint: "[path to review.md]"
---

# Revise From Review Findings

Launch the multi-agent revision system on an existing review report.

## Step 1: Read Context

Read `.papermill/state.md` (Read tool) if it exists for the paper path, format, and the latest `review_history` entry. Work gracefully without it.

## Step 2: Locate the Review Report

- If a report path was supplied (`$ARGUMENTS`, or named in the request), use it.
- Otherwise take the newest `.papermill/reviews/*/review.md` (Glob tool, sort by date directory).
- If no report exists, stop and suggest `/papermill:review` first.

If the chosen review_history entry already has a `revised` date, tell the user and ask whether to re-revise against the same report or run a fresh review first.

## Step 3: Confirm Scope

Ask the user (AskUserQuestion) which severities to address: all findings (default), Critical + Major only, or a custom selection. Mention how many findings the report contains per severity so the choice is informed.

## Step 4: Launch the Reviser Orchestrator

Spawn the reviser agent (Agent tool, `subagent_type: papermill:reviser`) with:

    <report>{path to review.md}</report>
    <paper>{manuscript path from state.md or discovery}</paper>
    <scope>{severity filter from Step 3}</scope>

    Work through the findings with fix-then-verify. Write revision.md next
    to the source review report.

## Step 5: Present Results

Summarize from the agent's report: findings fixed and verified, decisions needed from the author, retry failures (reverted), and the build status. Point at the revision report path.

## Step 5b: Resolve Decisions Needed

The reviser cannot ask questions itself (Claude Code removes AskUserQuestion from subagents), so it returns judgment calls as a `decisions-needed` YAML block. If that block is non-empty:

1. Ask the author with AskUserQuestion, one question per decision, using each item's `question`, its `options` (label as the option, consequence as the description), and `recommended` listed first with "(Recommended)". Batch up to 4 questions per call; group decisions that touch the same section.
2. Spawn the reviser again (Agent tool, `subagent_type: papermill:reviser`) with the same `<report>`, `<paper>`, and `<scope>` (so finding ids resolve against the same set), plus:

       <decisions>
       - id: F7
         choice: "Narrow the claim"
       </decisions>

   It fixes and verifies only those findings and appends them to the same `revision.md`.
3. Fold its fixed-and-verified count into the Step 6 total. Decisions the author explicitly skips stay listed as open.

## Step 6: Update State File

Update `.papermill/state.md` (Edit tool). If `.papermill/state.md` does not exist, skip this step and suggest `/papermill:init`. Updates:

Augment the review_history entry that matches the source report with:

```yaml
    revised: "YYYY-MM-DD"
    findings_fixed: N        # fixed-and-verified count from the revision report
```

Append a timestamped note to the markdown body summarizing the revision pass.

## Step 7: Suggest Next Steps

- If everything in scope was fixed: suggest re-running `/papermill:review` to confirm the recommendation moves toward `ready`.
- If the author skipped any decisions in Step 5b: list them as still open; re-running `/papermill:revise` on the same report picks them up.
- If the build failed: fix the build before anything else.
