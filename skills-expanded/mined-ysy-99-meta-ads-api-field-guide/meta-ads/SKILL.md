---
name: meta-ads
description: Use when the user wants to automate Meta Ads (Facebook/Instagram) — creating campaigns, pulling insights, uploading creatives, scaling budgets, or debugging API errors. Enforces production-safe patterns from the Meta Ads API Field Guide — PAUSED-by-default creation, rate-limit header monitoring, learning-phase-aware scaling, and v24/v25 deprecation awareness.
---

# Meta Ads — Production-Safe Automation Skill

This skill loads the operational discipline from the [Meta Ads API Field Guide](../../docs/) so Claude doesn't hallucinate deprecated fields, blow past rate limits, or accidentally trigger learning-phase resets.

## When to use

Trigger this skill for ANY Meta Ads API work:
- Creating campaigns, ad sets, ads, or creatives
- Pulling insights / building reports
- Scaling budgets / managing active campaigns
- Debugging API errors (code 10, 17, 190, 1487225, etc.)
- Cross-account creative transfers
- CAPI / server-side event setup

Do NOT trigger for pure Ads Manager UI questions, CRO strategy, or non-API marketing advice.

## Hard rules (never violate)

1. **PAUSED by default.** Every campaign, ad set, and ad created via API must have `status: "PAUSED"`. User activates manually after review. → [Field Guide: Pre-Campaign Checklist](../../checklists/pre-campaign-v24.md)

2. **Write operations require confirmation.** Before any create/update/delete, show the user what will be written and wait for explicit approval. Read-only (`get_*`, `list_*`) is free.

3. **Attribution from donor, literally.** When copying a campaign, copy `attribution_spec` exactly from the donor. Never "upgrade" `1d_click` → `7d_click`. → [Pitfall 1](../../docs/07-pitfalls.md)

4. **Rate limit: stop on error, don't retry.** On code 17, 613, or subcode 80004, read `X-Business-Use-Case-Usage.estimated_time_to_regain_access` and sleep. Do NOT retry immediately. → [Rate Limits](../../docs/01-rate-limits.md)

5. **Cross-account = checklist first.** Image hashes, page IDs, pixel IDs, audience IDs are all account-scoped. Never reuse across accounts without substitution. → [Cross-Account Ops](../../docs/08-cross-account-operations.md)

6. **Incremental > rebuild.** If > 50% of target objects already exist correctly, add the missing ones. Don't delete and recreate. → [Pitfall 14](../../docs/07-pitfalls.md)

7. **Budget changes: max 4/hour per ad set, ≤ 20% increments.** Error subcode 1487225 = budget change limit. > 20% = learning phase reset. → [Budgets & Learning Phase](../../docs/03-budgets-and-learning-phase.md)

8. **v24-compliant fields always.** Use `instagram_user_id` (not `instagram_actor_id`), `excluded_custom_audiences` top-level (not `exclusions.custom_audiences`), ODAE objectives (`OUTCOME_*` not `CONVERSIONS`/`LINK_CLICKS`). → [Deprecations 2026](../../docs/05-deprecations-2026.md)

9. **BigQuery/warehouse > live API for historical analysis.** Deleted creatives don't appear in API listings. Warehouse has full history.

10. **Document new errors.** Encountered an error code not in [Error Codes](../../docs/06-error-codes.md)? Add it to project's `lessons.md` after the fix is verified.

## Workflow for campaign creation (RSIV)

Every new campaign follows four phases. Never skip.

### Phase 1: Research
- Which ad account, objective, budget, audience?
- Does a template exist? (check project's campaign templates)
- What creative assets are ready? Are files local?
- Donor campaign — read targeting, attribution_spec, promoted_object literally.

### Phase 2: Synthesis (user confirmation gate)
Present to user:
- Campaign name (with numbering)
- Structure: N ad sets × M ads each
- Budget + bid strategy
- Key targeting details
- Attribution spec
- Status: PAUSED

Wait for explicit "yes" before Phase 3.

### Phase 3: Implementation
- Upload assets if needed (copy to /tmp/ if paths have parens/spaces)
- Batch API for adset+ads creation where possible
- `time.sleep(0.3)` between batches
- Monitor `X-Business-Use-Case-Usage` every 10 calls

### Phase 4: Verification
- Count: expected N campaigns, M ad sets, K ads
- Read `effective_status` (not just `status`) — IN_PROCESS means not live yet
- Visual preview of at least one ad (the cross-account hash silent-break bug)
- Confirm non-zero estimated audience on each ad set
- Log IDs

## Common error quick-fixes

| Code | Fix |
|---|---|
| `17` — User request limit | Sleep `estimated_time_to_regain_access` min, don't retry |
| `10, subcode 1341012` — No permission to profile | page_id or instagram_user_id not in token scope |
| `100, subcode 1815508` — Invalid Instagram position | Remove explicit placements, let Advantage+ pick |
| `100, subcode 1487225` — Budget change limit | 4/hour max — wait 60 min |
| `100, subcode 1487534` — Insights row limit | Narrow date range or remove breakdowns |
| `190` — Token expired | Regenerate system user token |

Full table: [Error Codes](../../docs/06-error-codes.md)

## Claude Code integration tips

- **Pair with an MCP server** for tool access. Recommended: `pipeboard-co/meta-ads-mcp` (most mature) or `mikusnuz/meta-ads-mcp` (135 tools, v25-ready).
- **Reference docs on demand.** Don't load all field guide pages at once. Load only the page matching the current task (e.g., `docs/02-insights-api.md` when user asks about insights).
- **Ask the user before write operations** when MCP exposes them — even though the MCP may not enforce this.
- **Use subagents for multi-account work.** Delegate per-account audits to parallel subagents.

## References (progressive disclosure)

Load these as needed based on task:

| Task | Load |
|---|---|
| Any API write | `01-rate-limits.md`, `07-pitfalls.md` |
| Campaign creation | `05-deprecations-2026.md`, `checklists/pre-campaign-v24.md` |
| Insights / reporting | `02-insights-api.md`, `11-breakdown-effect.md` |
| Scaling budgets | `03-budgets-and-learning-phase.md` |
| Creative upload | `04-creatives-and-dco.md` |
| Cross-account copy | `08-cross-account-operations.md`, `checklists/cross-account.md` |
| Server-side tracking | `13-conversions-api.md` |
| Error diagnosis | `06-error-codes.md` |
| Tool selection | `09-ecosystem-and-tools.md`, `12-related-resources.md` |
| Any end-to-end workflow | `10-cookbook.md` |

## Anti-patterns (never do these)

- ❌ Loop `while cursor.has_next(): cursor.load_next_page()` — SDK auto-pagination hits rate limits at ~25 pages
- ❌ Create ads with `status: "ACTIVE"` directly from script
- ❌ Change ad set budget by > 20% to "scale aggressively"
- ❌ Copy a campaign cross-account and reuse `image_hash` / `page_id` / `pixel_id` without substitution
- ❌ Rebuild 70 ads when 50 exist correctly and 20 are missing
- ❌ Retry on rate-limit errors immediately
- ❌ Use `CONVERSIONS` / `LINK_CLICKS` / `LEAD_GENERATION` objectives (deprecated — use `OUTCOME_*`)
- ❌ Pass `instagram_actor_id` (use `instagram_user_id`)
- ❌ Nest `exclusions.custom_audiences` (use top-level `excluded_custom_audiences`)
