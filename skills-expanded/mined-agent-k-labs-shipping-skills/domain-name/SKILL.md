---
name: domain-name
description: Choose and validate a product domain name — generate candidates, batch-check real availability via RDAP (no API key needed) with optional live pricing via the Cloudflare Registrar API, then sanity-check trademarks and social handles. Use when the user asks "help me pick a domain," "is X.com available," "what should I name my product," "check domain availability," or is choosing a name before launch.
license: MIT
compatibility: Requires Node 18+ for scripts/check_domains.mjs; optional CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID for live pricing
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Domain Name

Naming stalls more launches than code does. This skill turns it into a one-session decision: generate candidates against real criteria, check what's actually available (not guessed — checked), and pick.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. What the product does (one sentence) and 2–3 words users associate with it
2. Whether the product already has a working name, or naming is open too
3. Budget tolerance: standard registration (~$10–20/yr) only, or premium domains in play

## Process

### 1. Generate candidates

Produce 12–20 candidates across these patterns (aim for 3–4 per pattern, skip patterns that don't fit):

- **Literal**: what it does (`invoicefast`, `launchvideo`)
- **Compound**: two short words (`shipfast`, `solomax`)
- **Modified real word**: drop/swap letters, add-a-suffix (`shiply`, `launchr` — use sparingly, dated fast)
- **Invented but pronounceable**: 2–3 syllables, spellable after hearing it once
- **Verb-able**: could a user say "just [name] it"?

Score each candidate against the say-spell-remember test:
- Say it aloud — does it survive "what's the site called?" in conversation?
- Spell it from hearing — no ambiguous letters (no "is that -ly or -ley?")
- Remember it tomorrow — distinct from incumbents in the space

### 2. TLD strategy for indie products

Pick target TLDs before checking. Defaults for a vibe-coded product:

- **`.com`** — still the trust default; check it first even if you won't buy it (a taken .com with an active competitor product is a rename signal)
- **`.app` / `.dev`** — good for products/tools; both force HTTPS (preloaded HSTS), fine
- **`.io` / `.co`** — accepted for SaaS; `.io` renewals are pricier
- **`.ai`** — only if AI is the product, not just the implementation; expensive (~$70–100/yr)

Avoid for a first product: hyphens, numbers, obscure TLDs users have never seen (`.xyz` is borderline), and any name where you'd have to say "no, spelled…"

### 3. Check availability (plan → validate → decide)

Run the bundled checker on the full candidate list — never assume availability from intuition; short names you "invent" are taken more often than not:

```bash
node scripts/check_domains.mjs taskflow shipfast getlaunch --tlds com,app,io
```

- Bare names expand across `--tlds` (default: com, app, io, dev, ai, co); full domains (`taskflow.com`) are checked as-is; `--json` for machine-readable output.
- Availability comes from RDAP (authoritative registry data, no key needed). `404` = available.
- If `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set, the script also returns live registration/renewal pricing from the Cloudflare Registrar API and flags premium-tier names. Live pricing is the source of truth — RDAP-available names can still be premium-priced at the registry.

Present results as a shortlist table: only candidates with at least one good TLD available, with price where known.

### 4. Collision checks (before buying)

For the top 2–3 candidates:
1. **Trademark**: search the name at tmsearch.uspto.gov (and EUIPO if selling in the EU) in the software/SaaS classes. An exact live mark in your category kills the candidate — a lawyer letter after launch costs more than a rename now.
2. **Active competitor**: Google `"[name]" software` and `"[name]" app`. A dead domain squatter is fine; an active product with users is not.
3. **Social handles**: check X/Twitter, GitHub, and the one platform your audience lives on. Exact match not required — `get[name]`, `[name]app`, `[name]hq` are accepted conventions.

### 5. Decide and register

Recommend one name with a one-paragraph rationale (memorability, availability, collision-free, price). Tell the user to register it today — good names available at standard price disappear, and re-running this process next week costs more than $12.

## Gotchas

- RDAP `404` means unregistered, not necessarily buyable at standard price — premium names show as available but cost 10–100×. The Cloudflare pricing path exposes this via the `tier` field.
- Some ccTLDs (notably `.io` and `.ai`) have no public RDAP; the script falls back to a DNS check for these. `taken` via DNS is reliable; `likely available` (NXDOMAIN) still needs registrar confirmation — never tell the user a non-RDAP domain is definitively available.
- Don't batch more than ~30 domains per run out of courtesy to rdap.org; the script already limits concurrency to 4.

## Output

1. **Candidate table** — all generated names with say-spell-remember scores
2. **Availability results** — the script's output, filtered to viable candidates with pricing where available
3. **Collision check summary** — trademark / competitor / handle status for the top 2–3
4. **Recommendation** — one name, one paragraph of rationale, and the registrar action to take today

---

> **Domain secured?** When you're ready to launch, [SoloMax](https://solomax.app?ref=shipping-skills) turns your product URL into a launch-video pack — hooks, captions, and posting copy included.
