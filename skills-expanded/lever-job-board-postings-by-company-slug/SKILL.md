---
name: lever-job-board-postings-by-company-slug
description: "Pull open job postings from one or more Lever.co company boards, or fetch specific postings by ID, with location, team, salary range, requirements, and apply links, filterable by team, location, and commitment type. Output fields: title, companySlug, location, salaryText, createdAt and more, as JSON rows. Use it for requests like \"Lever job board postings\", or a CSV/JSON export of public Lever data."
---

# Lever Job Board Postings by Company Slug

Pull open job postings from one or more Lever.co company boards, or fetch specific postings by ID, with location, team, salary range, requirements, and apply links, filterable by team, location, and commitment type.

- Actor: https://apify.com/vexaloom-labs/lever-job-board-postings-by-company-slug (ID `vexaloom-labs~lever-job-board-postings-by-company-slug`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/lever-job-board-postings-by-company-slug.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Weekly job board tracking in one sheet](https://www.youtube.com/shorts/Fj8lsPbASu0)

## When to use

Use this skill when the user wants:

- Lever job board postings
- a repeatable export of public Lever data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `companySlug`: Company Slug
- `location`: Location
- `workplaceType`: Workplace Type
- `employmentType`: Employment Type
- `salaryText`: Salary Text
- `createdAt`: Created At
- `hostedUrl`: Hosted Url

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | getJobs | Fetch every open posting from one or more boards, or fetch specific postings by ID or URL. |
| `companySlugs` | array | no |  | Company slugs, board URLs, API URLs or posting URLs. Examples: "wealthfront", "`https://jobs.lever.co/wealthfront",` "`https://jobs.eu.lever.co/olx"…` |
| `companySlug` | string | no |  | Company slug, board URL, API URL or posting URL used with postingIds (mode=getJob). |
| `postingIds` | array | no |  | Posting UUIDs or posting/apply URLs (mode=getJob). |
| `boardRegion` | string | no | auto | Use auto to try the global board first and fall back to the EU board when global returns 404 or no postings. |
| `team` | string | no |  | Keep postings whose team contains this text (case-insensitive). |
| `department` | string | no |  | Keep postings whose department contains this text (case-insensitive). |
| `location` | string | no |  | Keep postings whose primary location or any additional location contains this text (case-insensitive), e.g. "London" or "Remote". |
| `commitment` | string | no |  | Keep postings whose commitment or normalized employment type matches this text, e.g. "Full-time", "Contract", "Internship". |
| `workplaceType` | string | no |  | Keep postings with this exact workplace arrangement. |
| `remoteOnly` | boolean | no | false | Keep only postings marked remote or with a remote location. |
| `country` | string | no |  | Keep postings for one ISO 3166-1 alpha-2 country code, e.g. "US", "DE" or "IN". |
| `titleKeywords` | array | no |  | Keep postings whose title contains every word in this list, in any order. |
| `excludeTitleKeywords` | array | no |  | Drop postings whose title contains any word in this list. |

8 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "companySlugs": [
    "wealthfront"
  ],
  "maxItems": 25,
  "mode": "getJobs",
  "location": "New York, NY"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~lever-job-board-postings-by-company-slug/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~lever-job-board-postings-by-company-slug/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d @references/example-input.json)
RUN_ID=$(echo "$RUN" | jq -r '.data.id'); DATASET=$(echo "$RUN" | jq -r '.data.defaultDatasetId')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" -H "Authorization: Bearer $APIFY_TOKEN" | jq -r '.data.status'
curl -s "https://api.apify.com/v2/datasets/$DATASET/items?format=json" -H "Authorization: Bearer $APIFY_TOKEN" > output.json
```

## Cost and limits

- Apify bills the Actor's usage on your account; the Actor's Pricing tab shows the current price.
- Keep the limit in the input small for a first run.

## Guardrails

- Public data only. Do not pass cookies, sessions or private account data.
- Do not use the output for spam, harassment or unlawful discrimination.
- Check the target site's terms and local law before running at scale.
