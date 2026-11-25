---
name: wcag-and-cookie-quick-audit
description: |
  Run a quick accessibility and cookie consent check on a website, rank the issues by risk, and give a fix list a developer can work through. Use when someone asks if their site is accessible, wants a WCAG check, worries about cookie consent, or needs a pre launch compliance pass.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content]
metadata:
  title: "WCAG and Cookie Quick Audit"
  category: "seo-content"
  tags: "seo_content"
  keywords: "seo and content, is our site accessible, wcag check, cookie consent audit, does tracking fire before consent, pre launch compliance check"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# WCAG and Cookie Quick Audit

## What this does

Accessibility and consent problems are found the same way: by checking what the page actually does. This skill checks the main page types for the accessibility failures that affect the most users, such as missing alt text, low contrast, unlabeled form fields and keyboard traps, and checks whether tracking loads before the visitor consents. It ranks issues by risk and writes the fix for each.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- is our site accessible
- WCAG check
- cookie consent audit
- does tracking fire before consent
- pre launch compliance check

## Inputs

- **site**: the website and the page types that matter: home, pricing, a form, a blog post
- **results**: scan results you already have, if not running it live
- **region**: where visitors are, which decides the consent rules that apply

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

1. Check one page of each type, not just the home page. Forms and checkouts fail most often.
2. List accessibility issues with the element, the rule it breaks, and how many users it affects.
3. Load the page with no consent given and list every tracker that fires. A tracker that fires before consent is a high risk issue in regions that require consent.
4. Rank all issues by risk: legal exposure first, then users affected.
5. Write the fix per issue in terms a developer can act on.
6. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

An issue table with page, element, rule, risk and fix; the list of trackers that fire before consent; and the ranked fix list. The output says it is a quick check, not a certified audit.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- One page of each type was checked
- Trackers that fire before consent are listed
- Issues are ranked by risk
- The output states it is not a certified audit

## Optional: run it on live data

This skill works with no tool. To add live data, run WCAG Accessibility Audit (https://apify.com/mambalabs/wcag-accessibility-audit?fpr=mamba) on your own Apify
account to scan the pages for accessibility issues, and add Cookie Consent Audit to check what loads before consent.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `agent-readability-audit`
- `listing-page-optimizer`
- `unsubscribe-compliance-check`
