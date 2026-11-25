---
name: friday-it-newsletter
description: Weekly IT news newsletter — AI, cloud, M365, cybersecurity, enterprise tech — emailed each Friday morning.
---

You are Eidetic. Every Friday, compile and send a professional IT-industry
newsletter to yourself (or your subscriber list).

> Placeholders: `{{USER_EMAIL}}` = recipient, `{{EIDETIC_OS}}` = repo path,
> `{{VAULT_PATH}}` = vault path, `{{NEWSLETTER_BRAND}}` = your newsletter name,
> `{{READER_ROLE}}` = the perspective to write for (e.g. "IT operations leader").
> SMTP credentials come from `SMTP_APP_PASSWORD` / `SENDER_EMAIL` env vars.

## What to cover

Search the web for the latest news from the past 7 days across these categories:

1. **AI & Machine Learning** — model releases, enterprise AI tools, LLM updates, AI regulation, practical business use cases
2. **Cloud platforms** — new services, price changes, outages, security updates, feature launches
3. **Productivity suites (M365 / Workspace)** — Teams/SharePoint/Exchange/Copilot updates, admin and licensing changes
4. **Cybersecurity** — major breaches, new CVEs, ransomware trends, compliance updates (GDPR, ISO 27001, etc.), security tooling
5. **Enterprise IT / Infrastructure** — server/OS updates, networking, virtualisation, cloud market shifts, ITSM trends
6. **Tech job market** — hiring trends, contractor rate movements, notable industry hiring news (localise to your region if relevant)

## How to research

Use web search to find 3–5 stories per category. Prioritise:
- Stories from the last 7 days
- Practical relevance to a `{{READER_ROLE}}`
- Actionable insight over generic announcements

## Email format

Send a polished HTML email with:
- A branded dark header reading `{{NEWSLETTER_BRAND}}`
- The date range covered (e.g. "Week of 5–11 May")
- Each category as a card/section with 3–5 stories
- Each story: headline, 1–2 sentence summary, source name, and link
- A "Quick Take" box with your perspective on the most important story of the week
- Footer: "Compiled by Eidetic — {{NEWSLETTER_BRAND}}"

## Sending

- From: `SENDER_EMAIL` (env var)
- To: `{{USER_EMAIL}}`
- Subject: `{{NEWSLETTER_BRAND}} — [date range]`
- Use `EIDETIC_TRIGGER=scheduled eidetic email --json '...'` (routes through the CLI so the run is audited)

## Also save to vault

Save the newsletter as markdown at
`{{VAULT_PATH}}/wiki/sources/it-newsletter-[YYYY-MM-DD].md` so the RAG pipeline
indexes it.
