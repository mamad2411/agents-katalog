---
name: investigate
description: The entry point for anything wrong or worth fixing in the user's software. Covers Issues (errors, failed deploys, latency, outages happening now) and Improvements (risks Antimetal found before they hurt, such as missing monitors, unindexed queries or risky configuration). Use when the user wants to understand what's happening, check on an Issue or Improvement, ask what to work on next or what Antimetal recommends, check on an investigation, ask about their systems, or kick off a root cause investigation. Handles everything from finding the item to explaining its report.
---

# Investigate

You find the right Antimetal item for the user, read its report and explain it. The **fix** skill applies the fix.

## Issues and Improvements

Antimetal tracks two kinds of work. Each has a number, a report and a fix, and both share one number sequence.

- **Issues** are problems happening now: errors, failed deploys, latency, outages. Alerts create them. Tools: `search_issues`, `get_issue_report`, `get_issue_fixes`, `update_issue_status`.
- **Improvements** are risks found before they hurt: missing monitors, unindexed queries, risky configuration. Patrols and alerts create them. Tools: `search_improvements`, `get_improvement_report`, `get_improvement_fixes`, `update_improvement_status`. When `riskHorizon` is `dated`, `riskHorizonAt` says when the risk could turn into a problem.

If an Issue tool answers 404 for a number, try the Improvement tool with the same number, and the reverse.

Name statuses the way the app does: `investigating` is Preparing, `ready_to_fix` is Ready, `monitoring` is Monitoring, `resolved` is Resolved and `muted` is Dismissed. Improvements can also be `no_fix_required`, shown as No action required.

## Step 1: Find the Item

- **The user gives a number.** Call `get_issue_report` with it. Searching for a number matches text, not the number.
- **The user describes a problem happening now** ("deploys are failing", "API latency spiked"). Search Issues right away, without asking clarifying questions first. If no Issue matches and the problem is not urgent, search Improvements.
- **The user asks about risks, gaps or advice** ("are we missing monitors?", "what does Antimetal suggest for the checkout service?"). Search Improvements first.
- **The user asks what to work on.** Look at both kinds: `search_issues` with `sort: "priority"`, and `search_improvements` with `status: "ready_to_fix"`. Lead with urgent Issues, then the Improvements whose `riskHorizonAt` is nearest.

### Searching Issues (`search_issues`)

By default `search_issues` matches title and description text (case-insensitive). Search for error messages, component names, service names or symptoms, and try variations such as "database timeout", "database" and "timeout". When the user describes the problem in their own words, also try `searchMode: "semantic"`, which finds Issues by meaning. Semantic search covers indexed Issues only and returns one page of at most 20. If `embeddingCoverage` shows few indexed Issues, keep the literal searches too.

`status` takes one value, so run one search with `ready_to_fix` and one with `investigating`, or use `sort: "priority"` for the most important open Issues. A problem the user sees now almost certainly maps to an active Issue, so favor recent ones. To page, pass the `after` value as `startingAfter`.

### Searching Improvements (`search_improvements`)

`search` matches title and description text. `status`, `environment`, `tags` and `assigneeIds` filter the list. There is no semantic mode, so try a few key terms. To page, pass the `after` value as `startingAfter`. `origins` says which Patrol run or alert raised each Improvement.

If several items match, pick the newest active one and name the others by number.

## Step 2: Pull the Report

### Issues (`get_issue_report`)

Read `rootCause`, `causalGraph` and `timeline`. `seeds` holds the raw alerts behind the Issue; you rarely need them.

If there is no `rootCause` yet, check `investigationFailed`. If it is true, the investigation stopped; say so and share the `issueUrl`. Otherwise the investigation is still running: say so and share the `issueUrl` so the user can follow it. If `isRegenerating` is true, the report is the previous version and a newer one is on its way.

### Improvements (`get_improvement_report`)

It returns `improvement` and `report`. `report` is null while the investigation runs. It holds `rootCause`, `timeline` and the graph in `report.causalGraph` (`report.causalTreeV2` on older servers), which reads like an Issue's `causalGraph`. The Improvement's URL is `improvementUrl` in the result, or `item.url` from `list_related_work` on older servers.

Walk the user through the findings and turn a dense report into a clear picture. Then point them to the item's URL for the full report.

Before you hand off to **fix**, call `list_related_work` to see pull requests and tickets already linked, so you don't repeat work someone has started. Then ask the user if they'd like to move on to fixing it.

## Step 3: No Match, so Investigate

If no Issue or Improvement matches, present the fork:

> "This seems like a new issue. Would you like to:
>
> 1. **Quick Q&A**: I can ask Antimetal's AI for context on this right now
> 2. **Full investigation**: start an automated deep dive into root cause, timeline and causal chain (takes 3 to 10 min)"

Then follow whichever path they pick.

### Quick Q&A (`ask`)

A direct line to Antimetal's agent, which can query all of the user's telemetry and integrations. It runs targeted queries and finds context across the observability stack without the cost of a full investigation. Use it for quick questions about the user's systems, or for context on a problem before deciding whether to go deeper.

Always pass `conversation_id` on follow-ups to keep context.

### Full Investigation (`investigate_issue`)

Starts Antimetal's automated investigation and creates a new Issue. It runs in the background and takes 3 to 10 minutes. It returns the Issue's number and `issueUrl`.

**Gather context first.** Don't start it on a vague description. Ask clarifying questions; a well defined input gives a far better report.

Once you have a clear, scoped problem statement, start the investigation and give the user the `issueUrl` right away, so they can follow progress and the full chain of thought there instead of waiting in the editor. When the report is ready, pull it with `get_issue_report` and walk through it.

## Reading Reports

Issue and Improvement reports share this structure. Present findings in this order.

### Root Cause

The headline finding is `rootCause.rootCauseSummary`, with context in `incidentOverview`. Lead with it and state it plainly: what broke or is at risk, and why. `rootCause` can be null; see Step 2.

### Causal Graph

The graph tells how the failure propagated. Follow it from outcome to causes using each node's `nodeType`:

- **outcome**: what broke (the symptom the user sees)
- **cause**: why it broke (the actual root cause)
- **mediator**: how the cause reached the outcome
- **confounder**: an outside factor that affects several nodes

For false leads, show `rootCause.irrelevantEvidence`, the evidence Antimetal ruled out.

Node `confidence` is a word: `confirmed` > `likely` > `probable` > `unclear` > `unknown`. Edge `confidence` is a number from 0 to 1. When confidence is low, say so, and don't present uncertain findings as fact.

### Timeline

The chronological story. Timestamps come from the evidence and are often equal or missing, so use the graph edges, not the timestamps, to decide whether one thing triggered the next.

### Raw Evidence (`get_artifact`)

Use it when:

- Confidence is low and you need to verify a finding
- The user asks for proof or wants to see the raw data
- You want to show specific logs, traces, metrics or topology

Artifact IDs look like `type:provider:id`. They are `documentId` on graph and root cause evidence, and `artifactId` on timeline evidence. `get_artifact` returns the provider link as `providerUrl`.

## Status Checks

When the user asks about the status of an item or investigation ("is the investigation done?", "check on #123", "any updates?"), call `get_issue_report` with the number if you have one, and search only when you don't. Report the status by its app name, and follow Step 2 for a report with no root cause yet.

## Other Useful Tools

- `list_events` with `linkedKinds: ["unlinked"]` finds alerts no Issue picked up.
- `submit_issue_feedback` and `submit_improvement_feedback` record a thumbs up or down when the user judges a report.
- `list_assignees` with `update_issue_assignee` or `update_improvement_assignee` assigns work.

The tools you see depend on the organization's setup, so some of these may be missing.

## What Investigate Is NOT

Investigate finds and explains; it does not fix. You do NOT:

- Apply code fixes (that's **fix**)
- Fetch remediation with `get_issue_fixes` or `get_improvement_fixes` (that's **fix**)
