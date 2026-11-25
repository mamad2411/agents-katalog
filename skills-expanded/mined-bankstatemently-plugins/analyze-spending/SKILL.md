---
name: analyze-spending
description: Use when the user asks to categorize spending, group by merchant or category, rank top merchants, or show monthly trends on converted statements. Do not use for first-time PDF conversion, period reconciliation, or benchmark scoring.
---

# Analyze

**Input:** the user's analysis scope — account, product, content hash, date range, or free-text filter.
**Output:** category totals, merchant or counterparty totals, top merchants, and a monthly trend, each row citing content_hash.

Treat the input as the user's analysis scope: account, product, content hash, date range, or free-text filter.

<!-- claude-only:start -->
**Before anything else:** if the Bankstatemently tools are not available in this session, the Bankstatemently connector is not connected. Tell the user that first, and how to connect it: Customize → Connectors → Bankstatemently → Connect, which asks them to sign in to a Bankstatemently account. Then ask whether they want to connect or have you do the task directly. If you do it directly, say that the result was not produced by Bankstatemently.
<!-- claude-only:end -->

Follow this sequence:

1. If the scoped statement has not been categorized, call `categorize_statement`.
2. Call `group_by` for category totals within the scope.
3. Call `group_by` for merchant or counterparty totals within the scope.
4. Call `top_n` to rank the largest merchants or counterparties within the scope.
5. Call `time_series` with monthly buckets for trend figures within the scope.
6. Present category totals, merchant or counterparty totals, top merchants, and the monthly trend. Cite content_hash for every figure or table row you report.

**Example prompt:** Categorize my checking account spending last quarter and show top merchants plus the monthly trend.
