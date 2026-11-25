---
name: vietnamese
description: "Vietnamese (tiếng Việt) for software: write, translate or review UI strings, errors, notifications, i18n files (vi.json, vi-VN), UX copy, product/dev docs, and how the agent replies in Vietnamese. Includes a 7,800-term glossary (core UI, shipped Android/Firefox phrasing, 21 industry packs) retrieved by script, never loaded whole."
---
# Vietnamese (router)

Pick ONE mode, load only its file, and fetch glossary lines with the script. `$SKILL_DIR` = the folder containing this file.

| Task | Load | Glossary |
|---|---|---|
| Reply to the user in Vietnamese (chat, summaries, explanations) | `modes/replies.md` | no |
| Write/translate/edit UI strings, errors, notifications, i18n files, web/product copy, docs | `modes/ui.md` | yes |
| Review or fix a batch (subagent playbook) | `modes/review.md` | yes |

## Workflow for UI/docs (token-cheap)
1. **Find the project's limits first.** Read `README*` and any design/spec docs (search `max|characters|chars|ký tự|limit`) before translating; write down each stated limit and pass it as `ctx.max` on every matching item. Never conclude "no limits" without having read them. Look for a project glossary too (`glossary*`, `terminology*`, `locales/vi*`) and pass it with `--glossary file.tsv` / `glossaryFile` (same columns as `glossary/project.template.tsv`).
   Then collect items `[{id, src, tgt?, ctx}]` with `ctx: {surface, max?, near?, standalone?}`: where the string is shown (`vi.mjs surfaces` lists 35 ids with GENERIC default limits), the real limit, text already visible next to it, and whether it must stand alone (push, SMS, background toast). Context on screen → shorten; standalone → minimum complete message.
2. **3+ strings or any ambiguity, and your harness has subagents** → hand ONE batch to `vietnamese-reviewer` (Claude Code agent / OMP task agent / Codex custom agent `vietnamese_reviewer`; else a general subagent) with:
   `Mode: translate|review|rewrite. Surface: … Audience: … Domains: <ids or auto>. SKILL_DIR=<abs path>. Project glossary: <path|none>. Read $SKILL_DIR/modes/review.md and follow it. Items: <JSON>`
   Otherwise do it inline: call MCP tool `vi_lookup` (server `vietnamese-drill`) if your harness lists it, else `node $SKILL_DIR/scripts/vi.mjs lookup [--domains a,b] < items.json` (same output), then follow `modes/review.md`. **Never write Vietnamese UI terms from memory when a lookup is possible.**
3. Verify UI strings in **items mode**: MCP `vi_check {items:[{id,src,tgt,ctx}]}` or `node $SKILL_DIR/scripts/vi.mjs check < {"items":[…]}` (same result; only items mode checks length, punctuation, context). Fix every error and re-run until none left (CLI exit 0); report remaining warnings. Text mode `{"text","sourceText","mode":"json"}` is for whole-file contracts (keys, placeholders) (CLI exit 0 ok/warnings, 1 contract error, 2 bad request). Run the project's i18n compiler for ICU; check the rendered UI when UI changed.
4. Never send secrets or customer data to a remote model. No numeric fluency score.

## Glossary packs (routing)
`lookup`/`check` auto-route domains from the source strings (deterministic keyword scoring, no LLM tokens). Pass `--domains` when you know the product's industry from the repo/README; `--domains none` disables routing. Precedence: project > domain > core > ui-ext.

core (329 curated UI terms) · ui-ext (3,499 shipped Android/Firefox phrases) · domains:
fintech (bank, e-wallet, QR, loan, KYC) · ecommerce (shop, voucher, flash sale, returns) · healthcare (clinic, BHYT, prescription) · education (LMS, grades, enrollment) · logistics (parcel, COD, waybill) · hr (payroll, leave, BHXH) · accounting (e-invoice, VAT, ledger) · insurance (policy, claim, premium) · legal (privacy, consent, terms) · realestate (listing, sổ hồng, deposit) · travel (flight, hotel, booking) · food (menu, delivery, POS) · telecom (SIM, data plan, roaming) · saas (CRM, pipeline, seats) · dev (git, CI/CD, cloud; keep-English rules) · gaming (rank, quest, gacha) · transport (ride, fare, EV charging) · erp (PO, BOM, stock) · media (posts, livestream, creators) · gov (căn cước, dịch vụ công) · security (2FA, passkey, devices)

Commands: `vi.mjs surfaces` (UI slots + limits) · `vi.mjs packs` (list with counts) · `vi.mjs route < {"strings":[…]}` · `vi.mjs lookup` · `vi.mjs check`. The MCP server `mcp/server.mjs` exposes `lookup` and `check` as `vi_lookup` / `vi_check`; the CLI needs only Node ≥ 18.

## References (load only when needed)
`references/microsoft-vi-style.md` (errors, notifications, punctuation) · `references/locale-and-glossary.md` (pronouns, dates, regions, glossary setup) · `references/sources.md` (provenance, limits). Never read `glossary/*.tsv` whole.
