---
name: site-preflight
description: Use before launching or deploying any site (Astro / Next.js / Eleventy), after cloning a site from a sibling, or when the user asks to "check a site before deploy", "run a preflight", or find leftover placeholders, hardcoded keys, missing canonical/OG/robots, or clone contamination. Complements sibling-uniqueness-audit (which compares sites to each other); this checks one site in isolation.
---

# Site Preflight

## Overview

Mechanical pre-deploy check for one site. Catches the recurring launch gotchas
across the site factory — every check is a plain grep/file test, so it gives a
real signal without needing a capable model to spot the issue.

Checks: hardcoded secrets (Google/Stripe/OpenAI/Anthropic/Twilio/Mailchimp/etc.),
tracked or un-gitignored `.env` files, placeholder/leftover text (TODO, lorem,
"NaN years ago", localhost, `*.vercel.app`, placeholder phones), clone
contamination (leftover sibling town/phone/postcode), missing canonical / OG /
robots / sitemap, relative OG images, missing `site:` domain config or localhost
baked into built output, and title-doubling (layout template + hardcoded suffix).

## Run It

```bash
python3 ~/.agents/skills/site-preflight/preflight.py "/path/to/Site"

# For a cloned site, pass sibling tokens that must NOT appear in the clone:
python3 ~/.agents/skills/site-preflight/preflight.py "/path/to/Tiverton Boiler Repairs" \
  --contaminants "south molton,southmoltonboilers,01769,EX36,07590491329"
```

Exit 0 = clean (PASS/WARN). Exit 1 = at least one FAIL.

## Reading the Report

| Level | Meaning | Action |
|---|---|---|
| `[FAIL]` | Exploitable or shipping-broken: hardcoded secret, tracked `.env`, sibling contamination, localhost in built output | Blocking. Fix before deploy. Secrets also need **rotating** — removing from source doesn't un-leak them. |
| `[WARN]` | Real SEO/quality gap: missing canonical/OG/robots/sitemap, placeholder text, title-doubling, un-gitignored `.env` | Fix unless deliberate. |
| `[note]` | Minor/might-be-intentional (e.g. relative OG image) | Judgement call. |

## Notes

- Heuristics, not a parser — a WARN can be a false positive; eyeball it. The value
  is a weak model (or a rushed human) can run it and get a real list to work from.
- Pairs with `sibling-uniqueness-audit`: run that to compare siblings for duplicate
  copy, run this to check one site's own hygiene. Both before any clone launch.
- Self-test: `python3 preflight.py --self-test`.
