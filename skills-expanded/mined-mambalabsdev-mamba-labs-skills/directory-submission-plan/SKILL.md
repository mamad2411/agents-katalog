---
name: directory-submission-plan
description: |
  Pick the directories and marketplaces worth listing on, and prepare one set of assets that fits all of them. Use when launching a tool, when someone asks where to list a product, or when directory submissions are eating time for no return.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content, seo_content_engine]
metadata:
  title: "Directory Submission Plan"
  category: "seo-content"
  tags: "seo_content, seo_content_engine"
  keywords: "seo and content, where should i list my product, directory submissions, launch listings, submit to directories, marketplace listings"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Directory Submission Plan

## What this does

Directory submission is usually done as a volume exercise against a list of a hundred sites, most of which send nobody. This skill ranks by whether a directory actually sends traffic to listings like yours, then prepares one asset set that satisfies the field requirements of all the ones that made the cut, so the submissions take an afternoon rather than a month.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- where should I list my product
- directory submissions
- launch listings
- submit to directories
- marketplace listings

## Inputs

- **product**: what it is and who it is for
- **assets**: logo, screenshots, descriptions you already have
- **time**: how much time this is worth

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Rank directories by whether they send anyone, which you can estimate from whether listings there rank for their own queries and whether the directory itself gets traffic. Domain authority is not the signal.
2. Cut the list hard. Ten directories that send visitors beat a hundred that host a link.
3. Check which ones a buyer in your category actually uses. A general software directory and a category specific one are not comparable and the second usually wins.
4. Inventory the field requirements across the surviving list and prepare one asset set that satisfies all of them: the longest description, the shortest description, every image ratio, and the category taxonomy.
5. Write descriptions at each length limit rather than truncating one. A truncated description reads as a fragment and that is what a visitor sees.
6. Track which listings were submitted, approved and rejected, since rejection is common and silent.
7. Set a review date to check which listings sent anyone, and delist the effort rather than the listing.
8. Approval stop. Before submitting the listing to any directory, show the user exactly what will happen and wait for an explicit yes. Nothing live changes without it.
9. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

Stop and ask before submitting the listing to any directory. Show exactly what will be sent or written, to whom or to
which records, and how many. Proceed only on an explicit yes from the user in this
conversation. A yes for one batch does not cover the next one.

## Output

The ranked directory list with the reason for each cut, the field requirement matrix, the asset set at every length and ratio, the submission tracker, and the review date.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- Directories are ranked by whether they send visitors, not by domain authority
- Category specific directories are separated from general ones
- Descriptions are written at each length limit rather than truncated
- A submission tracker records approvals and rejections
- A review date is set to check what actually sent traffic

## Optional: run it on live data

This skill works with no tool. To add live data, run Launch Directory List Builder (https://apify.com/mambalabs/launch-directory-list-builder?fpr=mamba) on your own Apify
account to build the directory list with submission links and terms.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `listing-page-optimizer`
- `comparison-page-builder`
- `agent-readability-audit`

Ships in the **seo-content-engine** pack.
