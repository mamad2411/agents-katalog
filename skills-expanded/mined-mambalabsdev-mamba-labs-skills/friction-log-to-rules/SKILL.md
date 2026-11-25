---
name: friction-log-to-rules
description: |
  Turn the things that went wrong in a working session into standing rules that stop them recurring. Use at the end of a project, after a mistake, during a retrospective, or when the same problem keeps happening.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_delivery, agency_operations, knowledge_ops_pack]
metadata:
  title: "Friction Log To Rules"
  category: "agency-operations"
  tags: "agency_delivery, agency_operations, knowledge_ops_pack"
  keywords: "agency, retrospective, this keeps happening, write up what went wrong, friction log, turn lessons into rules"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Friction Log To Rules

## What this does

Most retrospectives produce observations and no change, because an observation is not actionable and a rule is. This skill converts each friction point into a rule with a trigger, an action and a place it lives, and discards the ones that cannot be written that way, because a rule nobody can apply is noise in the rule set.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- retrospective
- this keeps happening
- write up what went wrong
- friction log
- turn lessons into rules

## Inputs

- **events**: what went wrong, in the order it happened
- **cost**: what each one cost in time, money or trust
- **existing**: the rules that already exist

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:


If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Write each friction point as an event, not as a judgment. What happened, what was expected, what it cost.
2. Find the cause one level below the event. The event is that a check passed wrongly; the cause is that the check could not fail.
3. Write the rule with three parts: when this situation arises, do this, and here is why. A rule without the why is discarded the first time it is inconvenient.
4. Discard any friction point that cannot be written as a rule. Some things are bad luck and adding them to a rule set dilutes the rules that matter.
5. Check against the existing rules. A rule that already exists means the failure was not knowing it, which is a placement problem rather than a rule problem, and the fix is different.
6. Say where each rule lives so it is read at the moment it applies, not filed where it will never be seen again.
7. Keep the set small. A rule set nobody can hold in their head is not applied.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The event list with costs, the causes, the new rules with trigger, action and reason, the discarded points with why, the duplicates found, and the placement per rule.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Every rule has a trigger, an action and a reason
- Causes are stated one level below the event
- Friction points that cannot become rules are discarded explicitly
- Duplicate rules are identified as a placement problem
- Each rule has a stated home

## Optional: run it on live data

This skill works with no tool. To add live data, run MCP Server Change and Health Monitor (https://apify.com/mambalabs/mcp-server-change-health-monitor?fpr=mamba) on your own Apify
account to watch the MCP servers your sessions depend on, so a broken tool shows up before it becomes friction.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `work-order-writer`
- `knowledge-write-discipline`
- `results-doc-verifier`

Ships in the **agency-delivery**, **knowledge-ops-pack** packs.
