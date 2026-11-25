---
name: competitor-engagers
description: Find people actively engaging with competitor LinkedIn posts. Given a website URL, discovers competitors, fetches their company and employee posts, collects all commenters and reactors, and outputs a deduplicated CSV of engaged prospects. Use when someone wants to find leads from competitor engagement, build outreach lists from LinkedIn activity, or analyze who interacts with competitor content.
user_invocable: true
---

# Competitor Engagers

Finds people who are actively engaging with your competitors on LinkedIn — the highest-intent prospects for cold outreach.

## Required step: Qualify with /icp-prompt-builder (do not skip)

After collecting the engager CSV, sample ~50 rows and run `/icp-prompt-builder` before scaling further. LinkedIn engagement alone doesn't guarantee ICP fit — someone who reacted to a competitor's post might be a peer, a candidate, a student, or an actual buyer. Qualifying filters separates them.

**Why required:** unfiltered engager lists typically have 30-50% non-ICP rows (fans, peers, recruiters, students). Running `/icp-prompt-builder` on a 50-row sample, tuning the qualification prompt, then applying it to the full list cuts wasted enrichment + send costs. Takes 10-15 min.

## Setup (First Time Only)

Before running, ensure these environment variables are set in `~/.env`:

```
RAPIDAPI_KEY=<your key from https://rapidapi.com/apibuilderz/api/realtime-linkedin-bulk-data>
OPENROUTER_API_KEY=<your key from https://openrouter.ai/keys>
```

Test your credentials:
```bash
npm run competitor-engagers -- --check-auth
```

## Steps

1. Parse the user's input. They must provide a website URL (e.g., "clay.com"). Ask for:
   - How many competitors to discover (default: 20)
   - Posts per company (default: 30)
   - Any specific competitor LinkedIn URLs to include

   If the user just says "run it" or provides only a URL, use all defaults.

2. Run the auth preflight check:
   ```bash
   npm run competitor-engagers -- --check-auth
   ```
   If it fails, help the user set up their API keys.

3. Run the main script:
   ```bash
   npm run competitor-engagers -- --url={domain} --competitors={count} --posts={postsPerCompany} {--extra-competitor=URL ...} --verbose
   ```

4. The script prints live progress. It can take 30-120 minutes for a full run (20 competitors x 200 employees x engagement collection). If interrupted, re-run with `--resume`:
   ```bash
   npm run competitor-engagers -- --url={domain} --resume
   ```

5. Once complete, read the output CSV from `~/output/competitor-engagers/` and present:
   - Total unique engagers found
   - Top 10 most active engagers (by total_engagements)
   - Breakdown by competitor
   - Output file path

6. Offer follow-up actions:
   - "Want to filter to only people with 3+ engagements?"
   - "Want to enrich these with email addresses?"
   - "Want to run this for a different company?"
   - "Want me to start a dry run first to validate the competitor list?"

## CLI Reference

```
--url=<domain>            Target company domain (required)
--competitors=<n>         AI-discovered competitor count (default: 20)
--posts=<n>               Posts per company (default: 30)
--extra-competitor=<url>  Add a competitor manually (repeatable)
--dry-run                 Discover competitors only, skip engagement scraping
--resume                  Resume from checkpoint after interruption
--verbose                 Detailed per-request logging
--check-auth              Test API credentials and exit
```

## Notes

- Skips people employed at the target company OR any of the competitor companies
- Comments and reactions only (reposts not collected)
- 90-day lookback window for posts
- Fetches up to 200 employees per competitor
- One row per person in output (deduplicated, sorted by engagement count)
- Checkpoint saved at `~/output/competitor-engagers/{domain}-checkpoint.json`

---

## What to do next

**Run `/icp-prompt-builder`** on a 50-row sample of the engagers CSV (required step — LinkedIn engagement alone doesn't guarantee ICP fit). Then `/list-quality-scorecard` on the filtered list.

**Or wait:** if your sample shows heavy non-ICP noise (>50% fans/peers/recruiters), the competitors you chose may be too broad. Re-run this skill with tighter competitor selection.

## Related skills

- `/icp-prompt-builder` — required filter pass on this skill's output
- `/list-quality-scorecard` — grade the filtered list
- `/list-builder` (Phase 5, emails) — if LinkedIn engagement doesn't include emails
- `/campaign-copywriting` — write copy referencing their specific engagement pattern
