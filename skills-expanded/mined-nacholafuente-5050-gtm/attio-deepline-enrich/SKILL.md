---
name: attio-deepline-enrich
description: Enrich records inside Attio with a clear cost gate before any credit is spent. Pull a chosen object (companies, people, or custom) from Attio, fill chosen attributes via Deepline providers (emails, phones, firmographics, LinkedIn, ICP fields), show the exact credit and dollar cost, wait for an explicit yes, run it, then write the values straight back into Attio. Use when the user says "/attio-deepline-enrich", "enrich my Attio companies/people", "fill in missing emails/phones/firmographics in Attio", "enrich N records in Attio", or "top up <attribute> on my Attio records". Never spends credits without confirmation.
---

# Attio + Deepline Enrich

Enrich records that already live in Attio, without exporting to a spreadsheet, hand-mapping columns, or guessing what it'll cost. You pick the object, the size, and the fields. The skill prices the run to the credit, asks once, then does it and writes the answers back into Attio.

Attio is both the source and the sink, and Attio reads/writes are free, so every credit is spent inside Deepline on the actual enrichment. Nothing is charged before you say yes.

> Powered by [Deepline](https://deepline.com). We're big fans, 50+ GTM data providers behind one CLI is the reason this skill is three steps instead of thirty.

## The flow

```
Attio (read, free)  ->  CSV  ->  Deepline enrich (paid, gated)  ->  CSV  ->  Attio (write, free)
```

## Setup (once)

- `ATTIO_API_KEY` in `.env` (Attio: Settings -> Apps & integrations -> API). Needs read + write scopes on the object you're enriching.
- Deepline CLI installed and authenticated: `deepline auth status`. Top up at https://code.deepline.com/dashboard/billing if needed.
- `pip install requests python-dotenv` (already in this repo's `requirements.txt`).

Pricing reference: **10 credits = $1**, so 1 credit = $0.10.

## Step 1: Which object?

Ask the user which Attio object to enrich (`companies`, `people`, or a custom object slug). Then show them what's actually on it, never guess slugs:

```bash
python skills/attio-deepline-enrich/enrich.py attrs --object companies
```

This prints every attribute as `slug | type | title` (free, read-only). Use it to confirm the **input** slugs (what Deepline needs to work from, e.g. `domains`, `name`, `email_addresses`) and the **target** slugs (what you'll fill).

## Step 2: How many, and which properties?

Ask three things and don't pick defaults silently:

1. **Which attributes to fill?** (the targets) Map each one to how Deepline will source it. Common ones:

   | Target in Attio | Deepline source | Typical tool family |
   |---|---|---|
   | work email | email waterfall | `bettercontact`, `findymail`, `prospeo`, `dropleads` |
   | direct/mobile phone | phone waterfall | `bettercontact`, `datagma`, `trestle` |
   | firmographics (employees, industry, revenue) | company enrich | `peopledatalabs`, `crustdata` |
   | LinkedIn URL | profile resolve | `linkedin_scraper`, `crustdata` (or the `linkedin-url-lookup` skill) |
   | job title / seniority | person enrich | `peopledatalabs`, `apollo` |
   | ICP score / segment / custom flag | classify | `aiinference` over the row |

   If unsure which provider, read `~/.agents/skills/deepline-gtm/provider-playbooks/<provider>.md` for cost and quality notes before committing.

2. **How many records?** This is the cost driver. Pull them, keeping only rows that still need the work so you never pay to re-enrich:

   ```bash
   python skills/attio-deepline-enrich/enrich.py pull \
     --object companies \
     --inputs domains,name \
     --target estimated_arr,employee_count \
     --only-missing \
     --limit 50 \
     --output /tmp/enrich_in.csv
   ```

   The script prints the real row count. **That count, not the user's round number, is N for costing.** If the user wants a hard cap of complete rows, over-provision ~1.4x at pull time and filter to the best N at the end (provider coverage has natural falloff; chasing the last few rows wastes credits).

## Step 3: Pilot one row to learn the true cost

Never estimate from a price list. Run the real enrichment on exactly one row and read what it actually cost:

```bash
deepline billing balance --json          # note the starting balance

deepline enrich --input /tmp/enrich_in.csv --output /tmp/enrich_out.csv --rows 0:1 \
  --with '{"alias":"work_email","tool":"bettercontact_enrich","payload":{ ...from provider playbook... }}'

deepline session usage --json            # credits the pilot consumed
```

Build the per-row cost from the pilot. **Per-row credits x N = the estimate.** If you're chaining several attributes (a waterfall), the pilot must include every step so the per-row number is real.

## Step 4: The cost gate (mandatory, blocking)

Before the full run, alert the Session UI, then show the gate verbatim and stop:

```bash
deepline session alert --message "Approval needed: enrich N rows in Attio (~X credits)"
```

Present exactly these four sections:

```
Assumptions
- <object, target attributes, providers, write mode>
- <which records: only-missing? capped at N?>

CSV Preview (ASCII)
<paste the verbatim ASCII preview from the deepline enrich --rows 0:1 pilot>

Credits + Scope + Cap
- Providers: <names>
- Per-row cost (from pilot): <credits>
- Full-run scope: <N rows>
- Estimated credits: <N x per-row> (~$<N x per-row x 0.10>)
- Spend cap: <cap>

Approval Question
About to spend ~<credits> credits (~$<dollars> at $0.10/credit) enriching <N> <object> in Attio.
Reply "YES I AGREE" to proceed.
```

Wait for the exact string **YES I AGREE** (case-insensitive). "yes", "ok", "go", "sure" are not consent, re-ask. One approval covers this exact run only; a new object, new attributes, or more rows needs a fresh gate.

## Step 5: Full run

Only after YES I AGREE. Enrich every row (omit `--rows`), writing to the output CSV:

```bash
deepline enrich --input /tmp/enrich_in.csv --output /tmp/enrich_out.csv \
  --with '{"alias":"work_email","tool":"...","payload":{ ... }}'
```

For multi-attribute or waterfall runs, use the `deepline enrich --with-waterfall ... --end-waterfall` form (see `deepline --help` and the deepline-gtm skill). Iterate with `--in-place` on `/tmp/enrich_out.csv` only, never on the source CSV.

## Step 6: Write back into Attio

Dry-run first so the user sees exactly what lands where, then write for real:

```bash
# preview
python skills/attio-deepline-enrich/enrich.py push \
  --object companies \
  --input /tmp/enrich_out.csv \
  --map work_email=email_addresses,arr=estimated_arr \
  --mode append \
  --dry-run

# write
python skills/attio-deepline-enrich/enrich.py push \
  --object companies \
  --input /tmp/enrich_out.csv \
  --map work_email=email_addresses,arr=estimated_arr \
  --mode append
```

`--map` is `csv_column=attio_slug`. Write modes:

- `append` (default) -> PATCH. Adds values, preserves existing ones. Right for multi-value fields (emails, phones, multi-select).
- `replace` -> PUT. Overwrites the attribute's values. Use only when the user wants the old value gone (removing/replacing a single-value field).

Writes are paced under Attio's 25/sec limit and auto-retry on 429. Report back: rows written, skipped (came back empty from the provider), and failed.

## Guardrails

- Read first, query attributes before writing so slugs and types are real.
- Pilot before pricing. The pilot is the only honest cost source.
- Gate before spending. No paid enrichment runs without `YES I AGREE`.
- Dry-run the write-back before mutating Attio.
- `append`/PATCH by default. Reach for `replace`/PUT only on explicit "overwrite it".
- Don't chase incomplete rows. Over-provision, then deliver the complete ones.
