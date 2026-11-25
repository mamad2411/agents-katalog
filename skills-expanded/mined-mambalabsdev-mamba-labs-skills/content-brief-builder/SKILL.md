---
name: content-brief-builder
description: |
  Write a content brief a writer can execute without inventing the substance, including where the non generic part comes from. Use when briefing a writer, planning an article, or when published content keeps reading like everything else.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content, seo_content_engine]
metadata:
  title: "Content Brief Builder"
  category: "seo-content"
  tags: "seo_content, seo_content_engine"
  keywords: "seo and content, brief a writer, plan an article, our content reads generic, content brief, what should this post cover"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Content Brief Builder

## What this does

Content reads generic when the brief specified the topic and the structure but not the substance, so the writer fills the gap with what everyone already knows. This skill requires a source for the one section that makes the piece unrepeatable, and refuses to brief a piece where that section does not exist.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- brief a writer
- plan an article
- our content reads generic
- content brief
- what should this post cover

## Inputs

- **topic**: what the piece is about and who it is for
- **angle**: what this piece says that others do not
- **sources**: what you have that a competitor does not

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`
- `ICP.md`
- `VOICE.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Name the unrepeatable section first: the data, the experience, the example, or the counter position that another company could not write. If it does not exist, say so and either find it or do not brief the piece.
2. Write the searcher's actual question and what a satisfying answer requires. Most briefs specify a keyword and leave the question implicit.
3. Specify the structure as questions the piece must answer in order, not as headings. Headings produce filler under each one; questions produce answers.
4. Specify what to leave out. Briefs almost never do this and it is why pieces drift into background nobody needs.
5. Name the source for every factual claim the piece will make, so the writer is not researching and inventing at the same time.
6. Specify the internal links and where they go, since a link added afterward lands in the wrong sentence.
7. Give the writer the voice markers rather than a description of the voice.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The unrepeatable section with its source, the searcher question, the ordered questions the piece answers, the exclusions, the claim sources, the internal links, and the voice markers.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The unrepeatable section is named and sourced, or the brief is refused
- Structure is specified as ordered questions rather than headings
- The brief states what to leave out
- Every factual claim has a named source
- Internal links are specified with their placement

## Optional: run it on live data

This skill works with no tool. To add live data, run Google Trends Scraper (https://apify.com/mambalabs/google-trends-scraper?fpr=mamba) on your own Apify
account to check whether interest in the topic is rising before you commission the piece.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `first-party-data-post`
- `comparison-page-builder`
- `programmatic-seo-planner`

Ships in the **seo-content-engine** pack.
