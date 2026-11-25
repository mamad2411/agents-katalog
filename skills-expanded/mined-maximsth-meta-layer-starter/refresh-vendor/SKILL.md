---
name: refresh-vendor
description: Walk the vendor-knowledge refresh protocol on demand OR on the weekly calendar reminder OR on drift-on-encounter — fetch sources, surface drift, human gate. Change-marker semantics: no-op walks write the ledger, no PR.
---

# /refresh-vendor

Substance lives in [`markdowns/protocols/refresh-vendor.md`](../../../markdowns/protocols/refresh-vendor.md).

Steps:

1. **Discriminate kickoff vs iteration** per [`auto-trigger-discriminator.md`](../../../markdowns/protocols/auto-trigger-discriminator.md). If iteration / polish / investigation, exit silently — conversation continues without the protocol-walk. Explicit `/refresh-vendor` invocation bypasses the discriminator entirely (walks the full protocol). The other three entry points from [`refresh-vendor.md`](../../../markdowns/protocols/refresh-vendor.md) — weekly calendar reminder, drift-on-encounter, rate-limit / flag-mismatch failure in `scripts/cross-vendor-review.sh` — are kickoff by definition (no discriminator ambiguity to resolve).
2. **Pick the vendor.** Resolve to `markdowns/agents/vendor-knowledge/<vendor>.md` (`claude-code`, `codex-cli`, `antigravity-cli`). Unknown name = stop and ask.
3. **Read the knowledge file.** Note volatility tags (`[STABLE] / [MEDIUM] / [VOLATILE]`), source URLs in §-level citations, and the `last-verified` frontmatter date.
4. **Fetch sources.** Pull every cited URL via WebFetch. Read official changelogs / release notes / docs anchored in the file. Don't invent capabilities the vendor doesn't claim.
5. **Produce a drift report (drift-detected only)** per the protocol's "The walk" step 4: added capabilities, removed capabilities, changed behavior (renamed flags, deprecations, breaking changes), volatility re-tagging. One bullet per claim with the source channel cited. A walk that finds nothing skips the report and goes to step 8.
6. **Walk FCPSS coverage (drift-detected only)** per [`fcpss-gate.md`](../../../markdowns/protocols/fcpss-gate.md). Work shape = **research**. Output = updated knowledge file + drift memo (drift-detected) OR ledger entry only (no-op). No-op walks skip this step. Concrete artifacts only — paste-fill "N/A" defeats the gate per the anchored-observations rule in [`cross-vendor-review.md`](../../../markdowns/protocols/cross-vendor-review.md).
7. **Human gate.** Surface the drift report in chat (drift-detected walks only). Supervisor approves / declines / amends each delta. NO writes to the knowledge file before approval.
8. **Apply — conditional on drift.** If drift was detected and approved: edit `<vendor>.md`; bump `last-verified`; re-run dependent scripts. If no drift was found: do NOT edit `<vendor>.md`; append one line to [`markdowns/agents/refresh-log.md`](../../../markdowns/agents/refresh-log.md) per the protocol's "The walk" step 7; the walk ends here (no PR).
9. **Ship per tier (drift-detected only).** Tier 2 typical — supervision pattern via [`supervision.md`](../../../markdowns/protocols/supervision.md): worker self-check, cross-vendor review by a peer vendor, chat-checkpoint, wait for "ship it". No-op walks have nothing to ship.

Auto-trigger fires on (a) weekly calendar reminder (you open Claude Code and type `/refresh-vendor <vendor>`), (b) user invocation in chat (`/refresh-vendor <vendor>` typed directly), (c) drift-on-encounter (per-volatility ceiling exceeded since `last-verified` AND a vendor capability is referenced in-session), or (d) rate-limit / flag-mismatch failure in `scripts/cross-vendor-review.sh` traceable to a stale flag table — mandatory refresh per the failure-modes table in [`cross-vendor-review.md`](../../../markdowns/protocols/cross-vendor-review.md). Change-marker semantics: walks that find nothing append to the ledger and exit without editing the knowledge file.
