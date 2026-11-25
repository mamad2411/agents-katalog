---
name: scrupp-prospecting
description: Build lead lists with Scrupp — turn an audience described in words into a Sales Navigator search, export LinkedIn, Sales Navigator or Apollo searches, find decision makers at companies, and find or verify work emails. Use when the user asks for leads, prospects, a contact list, decision makers, or work emails, or pastes a Sales Navigator, LinkedIn or Apollo search URL.
---

# Prospecting with Scrupp

Scrupp's tools spend the user's credits (one credit per record requested, unused
credits are refunded when a job finishes). Most of the work below is about not
spending them on the wrong list.

## Before spending anything

1. Call `scrupp_credits` first. It is free. If the balance cannot cover what the
   user asked for, say so and give them https://app.scrupp.com/app/plans before
   starting a job.
2. Say how many credits the next step can cost (the `max` you are about to pass,
   or the number of people / companies / addresses) and get a yes before any
   call over 100 credits.

## Pick the tool from what the user has

| The user has | Tool |
| --- | --- |
| An audience in words ("CFOs at fintechs in Germany, 50–200 people") | `scrupp_build_sales_navigator_search`, then `scrupp_export_sales_navigator_search` |
| A `linkedin.com/sales/search/people` URL | `scrupp_export_sales_navigator_search` |
| A `linkedin.com/search/results/people` URL | `scrupp_export_linkedin_search` |
| An Apollo search URL | `scrupp_run_apollo_search` (needs the connected Apollo account email as `account`) |
| LinkedIn profile URLs | `scrupp_enrich_linkedin_profiles` |
| Company domains, LinkedIn pages or names, and wants company data | `scrupp_lookup_company` |
| Companies, and wants the people to write to | `scrupp_find_decision_makers` |
| First name, last name and company domain | `scrupp_find_emails` |
| Addresses already in hand | `scrupp_verify_emails` |

Do not run `scrupp_verify_emails` on addresses `scrupp_find_emails` or an export
just returned: those are verified already and it would charge twice.

## Sample first, then the whole list

For any search export, run it first with `max: 5`. Show those five people (name,
title, company, email if found) and ask whether this is the right audience. Only
after a yes, run the same URL again with the full `max`. A wrong filter caught on
five records costs five credits; caught on 2,500 it costs 2,500.

When building a search from words, report the size Sales Navigator gives. If it is
far from what the user wants (10 or 100,000 when they asked for a few hundred),
rephrase the audience and build again before exporting. Building costs nothing.

## Long jobs

A tool that runs out of time returns `{ "status": "running", "job_id": ... }`.
Tell the user the job is running, then call `scrupp_get_job` with that id to
collect it. Do not start the export again with different arguments to "speed it
up": that is a new job and holds credits a second time.

## When a tool refuses

- **No connected LinkedIn / Sales Navigator / Apollo account.** The LinkedIn and
  Apollo tools run on the user's own LinkedIn account with Sales Navigator when
  one is connected with the Scrupp browser extension, and otherwise on Scrupp's
  shared account pool, which is open to paid plans only. A refusal here means
  neither is available: give the user the link from the error (or
  https://scrupp.com/docs/api/claude) and ask them to retry once it is fixed. Do
  not try another tool to get around it.
- **Not enough credits.** Give https://app.scrupp.com/app/plans.
- **Token expired / connect your account.** Ask the user to open `/mcp`, pick
  `scrupp` and sign in again.

## Handing over the result

Return a table with name, title, company, LinkedIn URL and email, and say how many
records came back and how many credits were used (the difference in
`scrupp_credits` before and after). For more than about 50 rows, offer to write a
CSV instead of printing everything.
