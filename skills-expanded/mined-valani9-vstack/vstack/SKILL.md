---
name: vstack
description: Office-hours-style entry point for the vstack skill family. Routes a free-form complaint about an AI-agent / multi-agent system to the right specialized vstack skill (or directly to one of the 34 MCP tools when the right diagnostic is obvious).
---

# /vstack

The meta entry point for the vstack skill family. If you're not sure which specific `/vstack-*` skill to invoke, start here.

## When to invoke

Trigger phrases:

- "The agent / crew is doing X — what do we run?"
- "Help me diagnose this..."
- "Is this a vstack thing?"
- The user mentions an agent failure, team breakdown, culture issue, or org-design tension but hasn't named a pattern.

If the user has already named the pattern or the task ("run an AAR on this", "pull a Schein audit on the crew"), call the matching MCP tool directly instead — don't add a router hop.

## Workflow

### Step 1 — Surface what's happening

Ask ONE clarifying question — never more than one per turn. The goal is the *shape* of the problem, not the details. Probe along these axes:

- **Scope**: is this one agent, a multi-agent crew, or an organization-level structural concern?
- **Signal**: a failed run, a slow run, a cultural feel, a missing artifact, a design question?
- **Artifact in hand**: do they have a trace, a transcript, a team config, just a verbal report?

If two of the three axes are clear from the user's first message, skip the question and jump to Step 2.

### Step 2 — Map to a downstream skill or direct pattern call

Use this routing table. Pick the first row whose triggers match.

| User said... | Route to |
|---|---|
| "Here's a trace, what's wrong?", "just run it", "diagnose this", or a one-phrase failure ("stuck in a loop", "agents arguing") | `/vstack-diagnose` |
| "Postmortem", "AAR", "what went wrong on this run", "failure", "agent confidently wrong" | `/vstack-post-incident` |
| "Crew", "multi-agent team", "they don't agree", "groupthink", "psych safety", "trust" | `/vstack-audit-crew` |
| "Slowing down", "bottleneck", "load", "queues backing up", "centralized orchestrator", "span of control" | `/vstack-bottleneck` |
| "Culture", "values", "feel of the team", "implicit norms", "the way things actually work" | `/vstack-culture-check` |
| "Grade this", "are we getting better or worse?", "CI gate on agent behavior", "scorecard" | `/vstack-scorecard` |
| "Set up monitoring", "calibrate", "track drift", "baseline" | `/vstack-baseline` |
| "Which pattern should I use?", "what's the right diagnostic?" | `/vstack-pick-pattern` |
| The user named a specific pattern | Call `vstack_<pattern_name>` directly via MCP |
| The user has a trace but no clear failure framing | `/vstack-diagnose` (run the default bundle, route deeper on what it surfaces) |
| None of the above | `/vstack-pick-pattern` (default — let it interview) |

### Step 3 — Hand off

State the route in one sentence: "Sounds like a post-incident review. Invoking `/vstack-post-incident` — it'll run AAR first, then Lewin attribution, then 1-2 downstream patterns based on what those surface." Then invoke that skill.

Never ask "should I invoke /vstack-post-incident?". The routing decision is yours; just do it.

## Failure modes

- **User can't articulate the problem.** Don't push routing. Ask for one concrete example ("walk me through one recent moment that felt wrong"). When you have one anchor, route on that.
- **Multiple routes match.** Take the more diagnostic / less prescriptive one. Post-incident before culture check; bottleneck before audit-crew. The deeper diagnostic protects against premature solutioning.
- **MCP not configured.** If `vstack-mcp` isn't registered in the host (no `vstack_*` tools listed), tell the user: "I see vstack as a library but the MCP server isn't wired up. Run `vstack-mcp config-snippet claude-desktop` (or your client name) and paste the config snippet. Then restart the client."

## Composition

This skill is the entry; everything else is downstream. The downstream skills do NOT invoke `/vstack` back — they finish the workflow themselves.

## What you don't do here

- Don't run an analyzer. That's the downstream skill's job.
- Don't ask for the full trace yet. Each downstream skill has its own preflight.
- Don't summarize the 34 patterns. That's `/vstack-pick-pattern`.
- Don't lecture about organizational-behavior theory. The user came with a problem, not for a class.
