---
name: linkedin-comment-strategy
description: |
  Decide which posts to comment on and write comments that do something other than agree. Use when someone wants to build presence through commenting, wants to be visible to a target account, or asks what to say on someone's post.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [linkedin, linkedin_authority]
metadata:
  title: "LinkedIn Comment Strategy"
  category: "linkedin"
  tags: "linkedin, linkedin_authority"
  keywords: "linkedin, what should i comment on, build presence through commenting, be visible to this account, comment strategy, reply to this post"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# LinkedIn Comment Strategy

## What this does

Commenting is the cheapest visible surface on the platform and almost all of it is wasted on agreement. This skill picks posts by whose audience matters rather than by whose post is popular, and writes comments that add a fact, a counter case, or a specific the post left out.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- what should I comment on
- build presence through commenting
- be visible to this account
- comment strategy
- reply to this post

## Inputs

- **targets**: the accounts or people whose attention matters
- **post**: the post to comment on, where there is one
- **expertise**: what you actually know that is worth saying

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`
- `VOICE.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Select posts by audience, not by engagement. A post with two hundred views from exactly the right people is worth more than one with twenty thousand.
2. Comment early enough to be read. Late comments on a large post are invisible regardless of quality.
3. Write one of three shapes: add a fact the post lacked, name the case where the post's claim does not hold, or give the specific number from your own experience. Nothing else is worth posting.
4. Never open by praising the post. It costs a line and signals nothing.
5. Keep it to two or three sentences. A comment that reads as a post is read as self promotion.
6. Do not pitch, ever. The comment earns the profile visit; the profile does the selling.
7. Track which comments led to a profile visit or a connection, because the ones that work are usually not the ones that felt best to write.
8. Approval stop. Before posting a comment, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before posting a comment. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The comment, its shape, and why this post was chosen over the others. Plus, when a set is requested, a prioritized post list with the audience reason for each.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Posts are selected by audience, not by engagement count
- The comment is one of the three named shapes
- No praise opener and no pitch appears
- Length stays within three sentences

## Optional: run it on live data

This skill works with no tool. To add live data, run Multi Platform Social Posts and Comments (https://apify.com/mambalabs/multi-platform-social-posts-comments?fpr=mamba) on your own Apify
account to pull recent posts and comments on a topic, to pick which ones to comment on.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `linkedin-post-writer`
- `linkedin-connection-campaign`

Ships in the **linkedin-authority** pack.
