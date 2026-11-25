---
name: linkedin-post-writer
description: |
  Write a LinkedIn post that sounds like the person and earns a reason to exist. Use when someone needs a post, wants to build a publishing cadence, has a result to share, or asks for content ideas for their profile.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [linkedin, linkedin_authority]
metadata:
  title: "LinkedIn Post Writer"
  category: "linkedin"
  tags: "linkedin, linkedin_authority"
  keywords: "linkedin, write a linkedin post, post idea for my profile, i have a result to share, publishing cadence, content for linkedin"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# LinkedIn Post Writer

## What this does

Most generated LinkedIn posts fail on the first line and on the reason for posting. This skill starts from something that actually happened, finds the first line that makes the second line necessary, and writes in the poster's own rhythm rather than in platform voice.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- write a LinkedIn post
- post idea for my profile
- I have a result to share
- publishing cadence
- content for LinkedIn

## Inputs

- **subject**: what actually happened, with the specifics
- **angle**: why it matters to the reader, not to you
- **samples**: two or three posts the person has written before

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `VOICE.md`
- `BRAND.md`
- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Refuse to start from a topic. Start from a thing that happened, with a number, a date or a name in it. A post with no specific is a post nobody remembers.
2. Write the first line so that the second is necessary. That is the whole mechanism, and it is not a hook in the sense of a tease, it is an unfinished thought.
3. Extract the voice markers from the samples: sentence length, contractions, whether the person uses questions, and how they end a post.
4. Structure by what the reader gets: the specific, the mechanism behind it, and the thing they can do differently. Three moves, no more.
5. Cut every sentence that is true but does not advance. Generated posts are usually twice their necessary length.
6. End on the thought, not on an engagement question. An engagement question at the end of a post is the clearest tell that the post was written to be posted.
7. Do not invent the specifics. If the input has none, say what to go and find.
8. Approval stop. Before publishing a post, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before publishing a post. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The post, a one line note on what the first line is doing, and the two or three alternative first lines that were considered.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The post contains at least one specific: a number, a date, or a named thing
- No invented specifics appear
- The post does not end on an engagement question
- Voice markers from the samples are applied and named

## Optional: run it on live data

This skill works with no tool. To add live data, run Threads Keyword Search (https://apify.com/mambalabs/threads-keyword-search?fpr=mamba) on your own Apify
account to find what people are saying about the topic this week before you write.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `linkedin-comment-strategy`
- `outbound-copy-humanizer`
- `linkedin-profile-optimizer`

Ships in the **linkedin-authority** pack.
