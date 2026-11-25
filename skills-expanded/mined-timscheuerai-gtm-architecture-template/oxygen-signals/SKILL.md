---
name: oxygen-signals
description: Capture and read OXYGEN Signals: your LinkedIn network, followers, viewers and post engagers; hiring, funding, tech and news signal searches; public profile watchers and keyword post search; competitor ads; and standing auto-enroll into a Sequence.
---

# Capture why-now signals

Read [the runtime contract](../../../docs/runtime-contract.md). A Signal records that something happened. Capturing it contacts nobody; acting on it is a Sequence or a Workflow.

## Read the stream

- `oxygen signals list --since 30 --json`: raw events resolved onto people.
- `oxygen signals leads-today --json`: people to contact today, ranked by their strongest recent signal, with customers and do-not-contact left out. Free; start here before ranking by hand.
- `oxygen signals record` logs one inbound signal from your own system (free, idempotent on an external event id). Use it for job-change alerts from another tool.

## Sources

| Goal | Start with | Cost |
|---|---|---|
| Your network, followers, profile viewers, post engagers | LinkedIn captures | free; metered on the account |
| Companies hiring, adopting a technology, raising, in the news | `signals search plan --family <family>` | paid per page |
| Public posts about a topic | `signals search preview --family linkedin_posts` | free preview |
| A company page's followers | `tables followers check` | paid order, delivered later |
| A competitor's ads | Ads searches | paid per call |

## Hiring signals as account signals

- Job titles go to the title filter; describe what a posting must be (in-house, not an agency) in the AI filter, billed per posting read.
- A posting carries the company LinkedIn URL and an AI summary of the description, not a domain. Join to accounts on the normalized company LinkedIn URL, and read the summary with a free formula to name the ERP or tool the company runs.
- Market-wide postings land at companies of every size, so fit-check the company before any spend.

## Rules

1. Your own data through the connected account; anyone else's data cookieless with credits.
2. Every paid read previews first and runs with `--approved` and a `--max-credits` ceiling read from that preview.
3. Standing grants (auto-enroll, watchers, bound feeds, follower orders) need their own approval and ceiling.
4. Monitoring runs hosted as feeds, watchers or Workflows; a local cron is not a monitor.
5. Coverage is partial by design: report what landed, never "everyone".

[the AP automation worked example](../../../examples/ap-automation-signal-engine/README.md) layers four hiring families, a free ERP-from-job-ads formula and a free ContactOut count of new finance leaders into one score.
