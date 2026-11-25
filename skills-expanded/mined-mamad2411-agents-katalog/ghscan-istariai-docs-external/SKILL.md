---
title: "Agent skill"
description: "A drop-in skill that teaches Claude (or any agent) to query GOI the disciplined way — so it returns clean results without you spelling out parameters."
---

The GOI MCP connector exposes powerful tools, but raw natural-language prompts (`search "macbook dubai"`) produce noisy results. This **skill** encodes the [cookbook recipes](/cookbooks/overview) as standing instructions, so the agent applies the right parameters automatically.

## How to use it

- **Claude Code / Claude Desktop:** save the block below as `SKILL.md` in your skills directory (or paste it into your project's `CLAUDE.md`).
- **Any agent / system prompt:** paste it into the system prompt alongside the GOI connector.

Once installed, asking *"find me corrugated cardboard makers in Germany"* makes the agent issue a disciplined `search_organizations` call instead of a bare query.

## SKILL.md

````md
---
name: goi-query
description: Query the ISTARI GOI connector for company intelligence. Use whenever the user wants to find, list, count, or compare real companies/organizations — suppliers, competitors, niche/deep-tech makers, market sizes, lookalikes.
---

# Querying GOI well

GOI covers ~20M web-verified organizations. Quality comes from parameters, not the search string. Pick the pattern that matches intent:

## 1. Find suppliers of a product  → search_organizations
- query: "{product} supplier manufacturer distributor wholesale vendor"
- nace_code: ["NACE C: Manufacturing", "NACE G: Wholesale and retail trade"]  ← does the real filtering
- keywords_must_any: ["supplier","distributor","wholesale","manufacturer","reseller","vendor","trading"]
- keywords_must_not: ["repair","rental","service center","maintenance","recruitment"]
- country: [<country>]   ·   dedup: true   ·   size: 12

## 2. Find companies that do one niche/deep-tech thing  → search_organizations
- query: rich description of the technology/product
- keywords_must_all: ["<anchor term>"]  ← the defining word; this removes drift
- use keywords_must_any for spelling variants (["electrolyzer","electrolyser"])
- keywords_must_not: ["consulting","recruitment","marketing agency"]
- nace_code: ["NACE C: Manufacturing"] only if you want makers
- Anchor on the technology, NOT organization_type=Startup (startup typing is sparse).

## 3. "Companies like X" / competitors / targets  → find_similar_organizations
- domains: [<1-3 reference domains>]   ·   exclude_domains: [<same references + known sister domains>]
- min_score: 0.6 (raise toward 0.65 if loose)   ·   optional country/nace filters

## 4. "How many" / distribution / market size  → aggregate_organizations
- structured filters only (country, nace_code, organization_size, region…) + group_by
- It IGNORES keywords_*. Report the result as a sector+geography denominator, never a product-specific count.

# Hard rules (these cause silent failures)
- Locations: resolve_location needs NATIVE names ("Bayern", not "Bavaria"). Resolve first, then use the returned filter.
- keywords_must_not cannot run alone — always pair with keywords_must_any/all.
- In keyword/hybrid mode the `Total` field is unreliable (often 0). Count returned rows.
- Do NOT set min_score in hybrid (keywords) mode — it collapses results.
- country is activity-based (where a firm operates), not legal HQ. Caveat the user if HQ is load-bearing.
- Always dedup: true. Hydrate full profiles with get_organization_details(domains=[...]).
````

## Tested

Following these instructions, the validated cookbooks held across quantum computing, solid-state batteries, corrugated cardboard, surgical gloves, process-mining lookalikes, and multi-country market sizing — see [Cookbooks](/cookbooks/overview) for the evidence.
