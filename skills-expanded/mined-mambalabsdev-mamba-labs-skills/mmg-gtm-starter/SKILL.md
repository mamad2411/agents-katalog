---
name: mmg-gtm-starter
description: |
  Start here. Ask what the user is trying to get done, name the two or three Mamba Labs skills and actors that do it, in order, and what each one needs. Use when someone is new to these skills, asks where to start, or describes a go to market goal without naming a tool.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [agency_operations]
metadata:
  title: "Mamba Labs GTM Starter"
  category: "agency-operations"
  tags: "agency_operations"
  keywords: "agency, where do i start, which skill should i use, help me set up outbound, what can these skills do, start here"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Mamba Labs GTM Starter

## What this does

A catalog of more than a hundred skills is only useful if the first choice is right. This skill asks three questions: the goal, what the user already has, and what they can spend. It then names the shortest path through the catalog: the skill to run first, the one after it, the Mamba Labs actor or MCP server that supplies live data, and what each needs, with links to install them.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- where do I start
- which skill should I use
- help me set up outbound
- what can these skills do
- start here

## Inputs

- **goal**: what the user is trying to get done, in their words
- **has**: what they already have: a list, a CRM, a sending tool, an Apify account
- **budget**: whether they can pay for live data runs

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`
- `BRAND.md`
- `VOICE.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Ask the three questions before naming anything: the goal, what they already have, and what they can spend.
2. Name at most three skills, in the order they run, with one line on what each produces.
3. For each live data step, name the Mamba Labs actor or MCP server, its cost line, and the link to it.
4. If there is no budget for live data, choose skills that need no tool, and say which step would improve with live data later.
5. Offer to run the first skill now.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The goal restated; a path of up to three skills in order with what each produces; the actors or server for live steps with cost and links; and the first step offered.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The three questions are asked before any skill is named
- No more than three skills are named
- Every live data step names its actor or server and its cost
- A no budget path is offered when the user cannot pay for live data

## Rules that are not obvious

- Install links: the public skills at https://github.com/mambalabsdev/mamba-labs-skills, every skill and pack at https://mambabuilt.com/skills.

## Optional: run it on live data

This skill works with no tool. To add live data, run B2B Prospect Engine (https://apify.com/mambalabs/b2b-prospect-engine?fpr=mamba) on your own Apify
account to turn the first plan into a live list in one run.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `mamba-gtm-router`
- `brand-context-builder`
- `icp-definition-builder`
