---
name: ai-answer-visibility-check
description: |
  Check whether ChatGPT, Perplexity and other AI answer engines name your brand when a buyer asks about your category, which competitors they name instead, and which sources they cite. Use when someone asks if AI search recommends them, wants an AI visibility baseline, or needs to know which pages to improve for AI answers.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content]
metadata:
  title: "AI Answer Visibility Check"
  category: "seo-content"
  tags: "seo_content"
  keywords: "seo and content, does chatgpt recommend us, ai search visibility, are we in perplexity answers, which competitors does ai name, geo baseline"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# AI Answer Visibility Check

## What this does

Buyers now ask an AI assistant for a shortlist before they visit a website. This skill takes the questions a buyer would ask, records which brands each answer names and in what position, lists the sources the answers cite, and turns the gaps into a short list of pages to write or improve. It works from answers you paste, and can run live with an actor.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- does ChatGPT recommend us
- AI search visibility
- are we in Perplexity answers
- which competitors does AI name
- GEO baseline

## Inputs

- **questions**: five to twenty buyer questions in the buyer's words
- **brand**: your brand name and the competitors you track
- **answers**: the answers, pasted, if you are not running it live

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`
- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Write the questions the way a buyer asks them, without your brand name in them.
2. For each answer, record every brand named and its position, and every source cited.
3. Compute your share of answers that name you, and the same for each competitor.
4. List the sources cited most often. Those are the pages that shape the answers.
5. Turn the gaps into actions: a page to write, a comparison to publish, or a listing to claim on a cited source.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

A table per question with brands named, positions and sources; the share of answers per brand; the most cited sources; and the action list.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Questions do not contain the brand name
- Share of answers is reported for your brand and each competitor
- The most cited sources are listed
- Each gap has one concrete action

## Optional: run it on live data

This skill works with no tool. To add live data, run AI Answer Visibility Tracker (https://apify.com/mambalabs/ai-answer-visibility-tracker?fpr=mamba) on your own Apify
account to ask the AI answer engines your buyer questions on a schedule, and add Perplexity Answer Reader for the sources Perplexity cites.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `agent-readability-audit`
- `comparison-page-builder`
- `content-brief-builder`
