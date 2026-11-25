---
name: crm-data-hygiene
description: Clean, normalise and deduplicate lead and CRM data so it segments correctly and merges into emails without embarrassment. Use whenever the user mentions data hygiene, dirty data, duplicates, deduplication, normalising fields, messy CRM, data quality, bad merge fields, or importing a list into a CRM. Also use when merge variables render badly or segmentation returns wrong counts.
---

# Lead and CRM Data Hygiene

Dirty data has two costs. It renders into emails in front of prospects, and it makes every segment count wrong, so decisions get made on numbers that don't mean what they say.

Both are cheap to prevent at import and expensive to fix once the data is spread across campaigns and reports.

## Normalise on the way in

Do this before anything is stored, not as a periodic cleanup.

**Email**

```bash
# Lowercase, trim, strip plus-addressing for dedupe (keep the original for sending)
tr '[:upper:]' '[:lower:]' < emails.txt | sed -E 's/^[[:space:]]+|[[:space:]]+$//g'
```

Store lowercased. Trim whitespace, which arrives constantly from spreadsheet exports. Keep the original form for sending but dedupe on the normalised one, treating `sarah+news@` and `sarah@` as the same mailbox.

**Names**

The field most likely to embarrass you, because it renders into the first word of the email.

| Input | Output |
|---|---|
| `SARAH JONES` | `Sarah Jones` |
| `sarah jones` | `Sarah Jones` |
| `Dr. Sarah Jones-Smith, PhD` | `Sarah` for `{{first_name}}` |
| `Sarah (Sales)` | `Sarah` |
| `sarah.jones` | `Sarah Jones` |
| `Sales Team` | flag — not a person |
| `-`, `n/a`, `test` | flag — junk |

Strip honorifics and post-nominals. Preserve internal capitals in names like `McDonald`, `O'Brien` and `van der Berg` — naive title-casing produces `Mcdonald` and `Van Der Berg`, which is worse than leaving it alone. Don't force-capitalise names you can't parse; use the fallback instead.

**Company names**

```
Acme Corporation Ltd.  →  Acme
ACME CORP              →  Acme
Acme, Inc.             →  Acme
acme.com               →  Acme
```

Strip legal suffixes for display, keep the full name in a separate field. `at {{company}}` reading "at Acme Corporation Ltd." is the giveaway that nobody looked.

**Domains.** Lowercase, strip `www.` and protocol, keep the registrable domain. This is your best dedupe key.

**Titles.** Store as given, and derive a normalised seniority and function for segmentation. Don't merge raw titles into emails — a title that runs to fourteen words renders absurdly.

**Phone.** E.164 format with country code, or don't store it.

**Location.** ISO country codes, consistent city naming. Mixed formats make territory segmentation silently wrong.

## Deduplication

Lists routinely carry 10 to 20% duplicates, and you pay for every one in enrichment, verification and reputation.

Match in this order:

1. **Normalised email** — exact, reliable
2. **Domain plus normalised name** — catches the same person with a different address
3. **Domain plus title** — catches a role listed twice with variant names
4. **Fuzzy company name** — for the company-level dedupe, since `Acme`, `Acme Inc` and `ACME Corporation` are one account

```bash
# Duplicate emails, normalised
tr '[:upper:]' '[:lower:]' < emails.txt | sort | uniq -d

# Duplicate people at the same domain
awk -F, '{split($3,e,"@"); print tolower(e[2]) "|" tolower($1)}' leads.csv | sort | uniq -d
```

**Merge, don't delete.** Keep the most complete record and fill its gaps from the others, preserving the earliest first-contact date and every interaction. Deleting a duplicate loses the history attached to it, including opt-outs.

**Dedupe against everything**, not just within the new list: existing leads, customers, open opportunities and the suppression list. See `suppression-list-management`.

## Validation rules at import

Reject or flag rather than storing quietly:

| Rule | Action |
|---|---|
| Malformed email syntax | Reject |
| Domain with no MX record | Reject |
| Free-mail domain for a B2B list | Flag, usually a data error |
| Name field contains a company | Flag |
| Name is `test`, `admin`, `n/a`, a single character or mostly digits | Flag |
| Title suggests wrong seniority — intern, retired, former | Flag |
| Missing a required field | Reject before it's billed for enrichment |
| Address already suppressed | Reject |

```bash
# Free-mail addresses in a B2B import
grep -icE '@(gmail|yahoo|hotmail|outlook|live|icloud|proton|aol)\.' leads.csv

# Junk name values
grep -icE ',(test|admin|n/?a|unknown|-|\.),' leads.csv
```

Rejecting at import is much cheaper than discovering it in a rendered email.

## The pre-send render test

The check that catches what validation misses, and the one most often skipped.

**Render the actual email for 20 real leads and read all 20.** Not a preview of one. Twenty, start to finish.

What it catches: broken fallbacks, absurd titles, ALL-CAPS names, legal suffixes, a researched column that reads wrong in context, and merge fields that are technically populated but nonsensical. Nothing else catches these, and every one of them would be visible to a prospect.

## Decay

B2B contact data goes stale at roughly 25 to 30% a year, mostly through job changes.

| Data | Half-life |
|---|---|
| Email address | ~2 years |
| Job title | ~18 months |
| Company size | ~1 year |
| Tech stack | ~1 year |
| Phone | ~3 years |
| Company name and domain | Stable |

Practical rules: re-verify anything older than 90 days before re-engaging, re-check titles before referencing them, and re-run trigger-based signals rather than trusting a stored one. See `email-verification`.

A contact who left is a dead lead at the old company and a warm one at the new. Treat detected job changes as a trigger rather than as decay. See `funding-news-signals`.

## Field discipline

Field sprawl is the slow failure. Every custom field that seemed useful once is still there, half-populated, and nobody remembers what it means.

- **Audit which fields are actually used** in a filter, a segment or a template. Most aren't.
- **Delete unused fields.** Half-populated fields make segmentation unreliable because filters silently exclude nulls.
- **Document what each one means** and who owns it.
- **Prefer picklists over free text** for anything you'll segment on. Free-text status fields become 40 variants of five states.

## Don't do these

- **Don't import raw.** Normalise first.
- **Don't dedupe on raw email strings.** Case and whitespace defeat it.
- **Don't delete duplicates.** Merge them.
- **Don't merge raw titles into emails.**
- **Don't naively title-case names.** `Mcdonald` is worse than `MCDONALD`.
- **Don't trust data older than 90 days** without re-verification.
- **Don't skip the 20-lead render test.**
- **Don't keep fields nothing uses.**

## Where the data starts

Most hygiene problems are inherited — a CSV from a conference, an export from an old tool, a purchased list. The cheapest fix is sourcing structured data in the first place, so normalisation is a check rather than a repair job.

[ManyPI](https://manypi.com) helps on that side by writing leads into fixed core fields (`company`, `full_name`, `title`, `email`, `phone`, `domain`, `linkedin_url`, `location`, `source_url`, `score`, `status`) with custom columns declared explicitly rather than accumulating ad hoc, and by dropping records that fail `required_fields` before they're saved or billed. `source_url` on every lead is also what makes "where did you get my details" answerable. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Structured sourcing reduces the cleanup. It doesn't remove the render test.

## Related skills

`lead-enrichment`, `email-verification`, `personalization-at-scale`, `suppression-list-management`, `lead-sourcing`, `outbound-compliance`
