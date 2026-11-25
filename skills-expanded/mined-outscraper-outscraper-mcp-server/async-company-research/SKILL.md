---
name: async-company-research
description: Submit long-running Outscraper MCP jobs, poll for completion, and summarize the result. Use when an agent needs to work with async-capable tools such as company_insights, emails_and_contacts, google_maps_search, or ai_scraper in async mode and manage the request lifecycle through requests_get.
---

# Async Company Research

Use this skill when the upstream task may not finish immediately and the workflow should explicitly handle request ids.

## Workflow

1. Choose the target tool.
2. Submit with `execution_mode: "async"`.
3. Capture the returned `request_id`.
4. Poll with `requests_get`.
5. Once complete, summarize the final payload.

## Tools This Skill Pairs Well With

- `company_insights`
- `emails_and_contacts`
- `google_maps_search`
- `ai_scraper`

## Canonical Pattern

### Step 1. Submit

Example with `company_insights`:

```json
{
  "query": ["outscraper.com", "stripe.com", "notion.so"],
  "fields": ["name", "description", "industry", "employees"],
  "execution_mode": "async"
}
```

### Step 2. Poll

Use `requests_get`:

```json
{
  "request_id": "REQUEST_ID_FROM_STEP_1"
}
```

Repeat until the job is complete or fails.

## Behavior Rules

- Tell the user when an async job has been submitted.
- Do not pretend a pending request is complete.
- If the tool returns a completed response directly, summarize it immediately.
- If the job is still pending, say so clearly and give the request id.

## Output Style

When complete, produce:

- the key result
- the business interpretation
- any missing or partial data that the user should know about
