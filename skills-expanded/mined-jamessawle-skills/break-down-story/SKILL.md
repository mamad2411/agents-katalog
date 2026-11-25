---
name: break-down-story
description: Use this skill whenever someone asks to break down a Jira story, split a story into vertical slices, decompose a user story, break PROJ-123 into vertical slices, slice a Jira ticket, or produce child tickets from a story. Fetches the target story from Jira, gathers codebase and Jira domain context in parallel, then synthesises a markdown breakdown of vertically releasable child slices shaped like draft Jira tickets. v1 outputs markdown only — no writes to Jira.
license: MIT
compatibility: Requires the Atlassian MCP server configured with Jira read access. Run from the cwd of the affected service repo.
allowed-tools: Bash, Read, Grep, Glob, Agent
argument-hint: "<jira-key-or-url>"
metadata:
  author: jamessawle
  version: "0.1"
---

# Break Down Story

Fetch a Jira story, gather context in parallel, and emit a vertically sliced breakdown as draft Jira tickets in markdown.

The pipeline has a non-interactive core (Steps 1–3) and a thin interactive layer (Step 4) so a future Jira-event runner can reuse the core without modification — the core either returns a markdown breakdown or a structured `cannot-break-down` result, never a question.

## Arguments

Single positional arg: a Jira issue key (`PROJ-123`) or full Jira URL. If neither is supplied, ask once then proceed.

Extract the key from a URL by taking the last path segment that matches `[A-Z]+-[0-9]+`.

## Preconditions

Run both checks before calling any MCP tools:

```bash
git rev-parse --show-toplevel
```

If the command fails, stop: "cwd is not a git repository."

If no key or URL is available after asking once, stop: "No Jira issue key provided."

## Step 1 — Fetch the target story

Call `mcp__claude_ai_Atlassian__getJiraIssue` with the extracted key. Capture: summary, description, acceptance criteria, status, issue type, labels, components, parent epic key, issue links (with link types), and child issues.

**Suitability check — stop if any condition holds.** Return a structured result with a machine-readable `reason` code and a human-readable `explanation` (this contract is what a future Jira-event runner depends on):

| Code | Condition |
|------|-----------|
| `already-broken-down` | Story has child issues |
| `is-sub-task` | Issue type is Sub-task |
| `already-sliced` | Story is small/self-contained and would not benefit from slicing |
| `too-vague` | Description or ACs are missing or contradictory — list exactly what is missing |
| `wrong-repo` | Story references a service that doesn't match the current repo |

Example stop message: "Cannot break down PROJ-123 (`too-vague`): acceptance criteria are missing and the description contains no behavioural requirements."

If none apply, continue.

## Step 2 — Gather context in parallel

Dispatch two subagents in a **single Agent tool message** (parallel execution). Wait for both before Step 3.

**Jira-context subagent** (`subagent_type: general-purpose`): read `references/jira-context-prompt.md` relative to this file's directory and substitute the target story's fields. This subagent fetches linked epics, sibling stories, and recent completions in the same component to surface domain patterns and done/not-done split.

**Codebase-context subagent** (`subagent_type: Explore`): read `references/codebase-context-prompt.md` relative to this file's directory and substitute the target story's fields. This subagent explores the repo to surface the relevant layers, entry points, and test patterns for the story's domain area.

Each subagent returns a ~300-word brief — not raw dumps. Instruct them to be concise and structured.

## Step 3 — Synthesise the breakdown

Read `references/output-format.md` relative to this file's directory. Follow the slice template and trailing sections exactly — it is the source of truth for structure.

Before emitting, run through the invariant checklist in `references/output-format.md`:

- Every acceptance criterion from the original story is covered by exactly one slice
- Every slice is independently releasable (passes CI in isolation)
- Slices are ordered by dependency (blocked slice appears after the slice it depends on)
- No slice invents ACs not traceable to the original story or gathered context

If any invariant fails, fix the breakdown first.

Each slice is shaped like a draft Jira ticket: **Summary / Description / Acceptance Criteria**, followed by a `---`-delimited "Reviewer notes" block covering estimated size, relevant code areas, and inter-slice dependencies.

## Step 4 — Present and revise

Print the full markdown to the conversation, then stop. Do not ask follow-up questions.

If the user replies with a revision request (e.g. "merge slices 2 and 3", "split slice 1 further"), apply the change and re-emit the complete updated markdown. Re-verify the Step 3 invariants on every revision.

## What this skill does not do (v1)

- Does not write to Jira
- Assumes a single repo at cwd — cross-repo stories are flagged as `wrong-repo`
- Does not learn slicing style from prior breakdowns (sibling stories are read for domain context only)

## Notes for future iterations

The non-interactive core (Steps 1–3) always produces either a markdown breakdown or a structured `cannot-break-down` result with a machine-readable reason code. A future Jira-event runner can call the core, inspect the result, and act accordingly — post the breakdown as a comment, open child issues after approval, or post a needs-clarification comment — without changes to this skill.
