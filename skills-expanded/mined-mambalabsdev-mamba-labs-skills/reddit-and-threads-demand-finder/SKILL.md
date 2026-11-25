---
name: reddit-and-threads-demand-finder
description: |
  Find posts where people describe the problem you solve or ask for a tool like yours, and sort them into buyer questions, complaints and content ideas. Use when someone wants to find demand on Reddit or Threads, research buyer language, or find threads worth answering.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content]
metadata:
  title: "Reddit and Threads Demand Finder"
  category: "seo-content"
  tags: "seo_content"
  keywords: "seo and content, find people asking for a tool like ours, reddit demand research, buyer language from reddit, threads worth replying to"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Reddit and Threads Demand Finder

## What this does

People describe their problems in public, in their own words, long before they fill in a form. This skill reads the posts you paste or export for a set of keywords, keeps the ones written by someone with the problem rather than someone selling a fix, and sorts them into buyer questions worth answering, complaints about current tools, and recurring phrases that belong in your copy.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- find people asking for a tool like ours
- Reddit demand research
- what are people saying about this problem
- buyer language from Reddit
- threads worth replying to

## Inputs

- **posts**: posts or threads you exported or pasted, with links
- **keywords**: the problem words, not your product name
- **offer**: what you sell, to judge fit

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

1. Search on problem words, not product names. People with the problem rarely know the category name.
2. Keep posts written by someone with the problem. Drop posts by vendors and by people promoting a fix.
3. Sort what is left into three groups: buyer questions, complaints about current tools, and content ideas.
4. Quote the exact phrases that recur. Those phrases go into headlines and first lines unchanged.
5. For a thread worth answering, draft a reply that helps without a link first. Posting it is the user's decision.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

Three grouped lists with post link, date and the quoted line; the recurring phrases with counts; and draft replies for the threads worth answering.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Vendor and promotional posts are removed
- Posts are sorted into buyer questions, complaints and content ideas
- Recurring phrases are quoted exactly with counts
- Replies are drafts and nothing is posted

## Optional: run it on live data

This skill works with no tool. To add live data, run Reddit Search Thread Scraper (https://apify.com/mambalabs/reddit-search-thread-scraper?fpr=mamba) on your own Apify
account to pull the threads for your keywords, and add Threads Keyword Search for posts on Threads.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `linkedin-profile-optimizer`
- `content-brief-builder`
- `objection-handling-library`
