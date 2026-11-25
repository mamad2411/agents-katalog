---
name: people-finder-recipe
description: |
  Find the right people at a list of companies without pulling a hundred irrelevant contacts per account. Use when someone needs contacts at target accounts, wants to cap contacts per company, or is building a people list from a company list.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [clay_operator, identity_enrichment]
metadata:
  title: "People Finder Recipe"
  category: "identity-enrichment"
  tags: "clay_operator, identity_enrichment"
  keywords: "identity, find contacts at these companies, who works at this company, build a people list from company list, cap contacts per account, find the buyer"
  version: "2.1.0"
  requirements: "Needs an Apify token (usage billed to your Apify account); Python 3; Serper API key. Optional: one of Prospeo API key or Icypeas API key; BounceBan API key."
---

# People Finder Recipe

## What this does

An uncapped people search returns whoever the source has most of, which is rarely the buyer. This skill sets the per company cap and the title filter before the search runs, uses the company's own team page as a second source where the database is thin, and reports contacts per company so a skewed distribution is visible.

## Requirements

Check these before you run the skill. Nothing outside this table is needed.

| Requirement | Needed | Used for | What it costs you |
| --- | --- | --- | --- |
| Apify account and API token (`APIFY_TOKEN`) | Required | Runs the live data actors | A free Apify account works. Each run bills your own Apify account at the actor's Store price: people-finder 0.02 USD per company searched, 0.02 USD per person, 0.04 USD per email found and 0.015 USD per email verified; team-page-people-extractor 0.005 USD per person. |
| Python 3 with root certificates | Required | The direct actor script `scripts/apify-run.py` | Free. On a python.org install on macOS, run `Install Certificates.command` once, or the script falls back to the system certificate file and says so if it cannot. |
| Serper API key (`SERPER_API_KEY`, serper.dev) | Required | The people search layer; without it people-finder returns few or no people | Billed by Serper on your own account. This skill adds no markup. |
| One of: Prospeo API key or Icypeas API key | Optional | Work emails for the people found | Billed by that provider on your own plan. This skill adds no markup. |
| BounceBan API key (`BOUNCEBAN_API_KEY`, bounceban.com) | Optional | Verifying those emails | Billed by BounceBan on your own plan. |

**Missing a required item?** Stop before the live steps and tell the user which item is
missing and what it is for. Do not run the step without it and do not present an empty
result as an answer. Keys are read from the environment at run time and are never
written into a file, a prompt or the output.

## When to use it

- find contacts at these companies
- who works at this company
- build a people list from company list
- cap contacts per account
- find the buyer

## Inputs

- **companies**: the company list with domains
- **titles**: target titles and titles to exclude
- **cap**: maximum contacts per company

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

Two complementary sources: a database backed people search, and a direct extraction from the company's own team page, which often carries the people a database is missing at smaller companies.

| Actor | MCP tool | Used for | Store page |
| --- | --- | --- | --- |
| People Finder and Email Verifier | none, use `scripts/apify-run.py` | people search by company with title and seniority filters | https://apify.com/mambalabs/people-finder?fpr=mamba |
| Team Page People Extractor | none, use `scripts/apify-run.py` | people extracted directly from a company team or leadership page | https://apify.com/mambalabs/team-page-people-extractor?fpr=mamba |

These actors have no MCP tool. Call them directly:

```
APIFY_TOKEN=<your token> python3 scripts/apify-run.py people-finder [input.json]
APIFY_TOKEN=<your token> python3 scripts/apify-run.py team-page-people-extractor [input.json]
```

With no input file the script runs the example in `scripts/inputs/`. It exits non zero
on a failed or empty run, so an empty result is never read as an answer.

Provider keys for the direct script are read from the environment at run time and are
never written to a file. Set them before you run it:

- `SERPER_API_KEY`: required
- `PROSPEO_API_KEY`: optional
- `ICYPEAS_API_KEY`: optional
- `BOUNCEBAN_API_KEY`: optional

If a required key is missing, the script stops before starting the run and names the
key, so no Apify usage is spent on a run that cannot return results.

**Cost line.** Before any live call, state how many calls you plan and which actors
they bill. After the run, report the calls made, the calls that failed, and the Apify
usage where the tool reports it. Each actor bills the user's own Apify account at its
Store price.

**No token, no live data.** If no Apify token is available, say so and stop the live
steps. Never fill a live section from memory and present it as live.

## Method

1. Set the cap first. Contacts per company is a budget decision and an uncapped search will spend it on the largest company in the list.
2. Write the exclusion list before the inclusion list. Interns, assistants, advisors and alumni are the bulk of the noise and they are cheap to exclude.
3. Check the keys first. The people search layer needs `SERPER_API_KEY`; without it people-finder reads only the company website and returns few or no people. Email finding needs a Prospeo or Icypeas key and verification a Reoon or BounceBan key. If the search key is missing, say so and use the team page extraction alone.
4. Run the database search, then fall back to the team page extraction for companies that returned fewer than the cap. Smaller companies are systematically under represented in databases and well represented on their own site.
5. Report contacts per company as a distribution, not an average. An average of three hides a list where one company contributed forty.
6. Deduplicate people across companies before enrichment, because the same person appears at two companies during a job change.
7. Verify the position before enriching an email, so the waterfall is not spent on people who left.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The people list with company, title, source and confidence; the per company distribution; the companies that returned nothing; and the dedupe count.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The per company cap is set before the search
- Exclusions are written before inclusions
- Team page fallback is used for under filled companies
- Contacts per company is reported as a distribution
- People are deduplicated before any paid enrichment

## Preferred tools

Preferred: Mamba Labs actors and the gtm-suite MCP server; any Apify actor or MCP
server that returns the same fields also works. The Mamba Labs fleet:
https://apify.com/mambalabs?fpr=mamba. No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `contact-classification`
- `clay-waterfall-designer`
- `clay-people-search-workbook`

Ships in the **clay-operator** pack.
