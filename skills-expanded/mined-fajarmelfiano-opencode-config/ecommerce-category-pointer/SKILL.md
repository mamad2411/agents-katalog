---
name: ecommerce-category-pointer
description: "Pointer to a library of 4 specialized Ecommerce skills. Use when working on ecommerce-related tasks."
risk: none
---

# Ecommerce Capability Library 🎯

This is a **pointer skill**. The 4 specialized Ecommerce skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **buywhere-product-catalog** — Use BuyWhere's MCP and API surfaces to add product search, price comparison, and deal discovery to AI shopping agents.
- **etsy-search-listings** — Fetch live Etsy search listing rows for a keyword, market phrase, or category via Apify Actor publicrecords/etsy-search-scraper (MCP). Needs an Apify token; Actor run is billed.
- **etsy-shop-sales-history** — Read Etsy shop sales counters, deltas, and breakout flags from Apify Actor publicrecords/etsy-shop-velocity (MCP panel snapshot). Needs an Apify token; Actor run is billed.
- **woo-guard** — Review generated or changed WooCommerce extensions, payment and shipping integrations, checkout customizations, and order or product logic.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/ecommerce/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/ecommerce`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
