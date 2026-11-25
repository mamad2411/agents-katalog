---
name: intel-brief
description: Brief newly published or newly CISA KEV vulnerabilities from the public Fencer Intel feed over a time window, optionally filtered to a technology, ecosystem, vendor, or package. Use when the user asks what vulns dropped recently, what just entered KEV, or how to watch a stack for new ones. Cites https://intel.fencer.dev/<id>, gives the matching feed URL, and does not invent entries the lookup did not return.
allowed-tools: Read
---

# Brief recent vulnerabilities

Summarize what Fencer Intel newly lists, for a window the user names. Default the window to 7 days
when they do not name one.

This repo has no scheduled job. Watching means handing the user the public RSS URL for the same
filter and telling them a reader (including Slack's `/feed subscribe`) can poll it. Do not promise
to check again later.

## Before the lookup

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
```

Read `$SKILL_DIR/../../shared/references/using-intel.md` in full and follow it. Page only the
public tools. Do not invent entries to fill a quiet window.

## What to ask the feed

Run only the lists the user asked for. If they said "recent" with no other qualifier, run newly
published only.

**Newly published.** `search` with `published` set to the window (`7d`, `30d`, or a
`YYYY-MM-DD..YYYY-MM-DD` range) and `limit` 50. `published` filters the publish date, not the day
something entered KEV. If they instead mean "new on the feed" (an older CVE that the feed listed
late, or that turned critical), page `list_feed` with no `filter` and keep rows whose `listed`
falls inside the window. Say which date you used.

**Newly in KEV.** `list_feed` with `filter` `kev` and `limit` 50. The KEV feed is ordered by the
date added. Keep entries whose `kev` date falls inside the window. Stop when a page is older than
the window or when `next_cursor` is null. Cap at 5 pages. If the fifth page is still inside the
window, say the list is incomplete and point at the feed.

Optional filters, only when the user named them:

- `tech` — a technology slug the tool accepts (the error names the legal ones)
- `ecosystem` — one of the ecosystems in the shared reference
- `vendor` — a vendor or product, matched from the start of a word
- `package` — on `search` only, the exact package name

A stack of ecosystems is a filter on the brief, not a version check. When they want "is my
lockfile affected", use `intel-check-deps` instead of this skill.

`filter=critical` is a different list (KEV, active exploitation, or high CVSS plus EPSS). Use it
only when the user asked for critical items, and still apply the date window from `listed` or
`published` on the returned rows.

## Answer

Name the window, the filters, and that the rows are what Fencer Intel returned.

Two sections when both queries ran: **Newly published** and **Newly in CISA KEV**. For each row:

- `[<id>](url)` — title
- severity, CVSS score if present, EPSS if present, KEV added date if present
- one line on the fix only when `has_fix` is true; the list row does not include the version. Call
  `get_vulnerability` for the fixed versions when the user asked what to upgrade, and only for the
  rows you will actually discuss (up to five). Otherwise link the entry and say the fixed version
  is on that page.

If a section is empty, write "Fencer Intel returned no entries for this window." Do not borrow
older, better-known vulnerabilities.

**Keep watching.** Give the feed URL with the same filters you just used, `format` left as RSS.
An example shape, not a default, is `https://intel.fencer.dev/feed?filter=kev&tech=nextjs`.

Say they can subscribe to that URL, including with Slack's `/feed subscribe`. Do not create a
stored stack report for a watch.

End with the Sources paragraph from the shared reference.
