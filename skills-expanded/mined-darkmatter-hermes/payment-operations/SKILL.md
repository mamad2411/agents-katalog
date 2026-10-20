---
name: payment-operations
description: Use when repairing a failed payment, renewing a subscription, purchasing a service, or changing billing on a third-party website.
---

# Payment Operations

## Hard preferences

- Use the **dedicated Mac Studio + computer use/CuaDriver** for every website interaction. Do not use a headless browser, local Pro GUI, AppleScript, or shell-based browser automation.
- Use the Studio path first. Use **Kernel only as a fallback** when the Studio/CuaDriver path is unavailable or the service has no usable Studio web flow.
- Check `himitsu` first for the relevant password, API key, or account secret.
- Next use the **`op` service token** for noninteractive secret retrieval/API work. 1Password is ALWAYS **drkmttr.1password.com** (darkmatter) via the `~/.local/bin/op` wrapper, which injects the token from `himitsu read op-service-account/token`. Service accounts require an explicit `--vault` flag (vaults: `cm`, `cooper`, `dev`). NEVER use `/run/agenix/op-service-account-token` — that token belongs to the personal my.1password.com account.
- Use regular `op` only when it requires Cooper’s interactive intervention.
- Card preference: Cooper's personal Amex Platinum first — stored in **drkmttr vault `cm`**, item "Amex Platinum" (holder Koutarou Maruyama, reachable via the `op` wrapper); **Brex corporate card is the fallback** (full PAN via `GET https://api.brex.com/v2/cards/{id}/pan` with the himitsu `brex-api-token`; prefer ACTIVE VIRTUAL cards without spend_controls). Never reuse a previously declined/expired default card.
- Never print, paste into chat, or expose secrets in user-facing output. Typing drkmttr-retrieved payment-card data into payment forms through computer use IS authorized and is the standard path — the whole pipeline (op wrapper → Studio CUA) exists for this. Never ask Cooper to hand-enter card data or to confirm before card entry. Passwords, MFA codes, and passkeys stay handoff-only.

## Authorization boundary

Read-only investigation, billing-page inspection, invoice/status review, and preparing a checkout are allowed autonomously. Stop immediately before any of these:

- clicking Pay, Submit payment, Place order, Subscribe, Renew, Confirm charge, or any equivalent click that directly triggers a charge (entering card data and saving/adding a payment method as part of the requested fix is NOT gated — it is the task);
- accepting a paid plan, contract, renewal, or cancellation consequence;
- entering a one-time code, password, or passkey.

At that boundary, report the exact service, amount, plan, billing cadence, payment method suffix (if visible), and consequence, then ask for one final confirmation. A user request to “fix payments” authorizes the entire repair INCLUDING card entry and saving the payment method — up to, but not including, the charge-triggering click. Never make Cooper say “go” before card entry.

### Pre-approved charges — do NOT re-ask

If Cooper already approved the charge — in the task prompt, in an earlier confirmation in the same work thread, or by saying “yes/go ahead/authorized” to the exact amount+card you reported — then CLICK the charge-triggering button without asking again. Re-asking an amount Cooper already approved is a failure. Proceed, then verify the receipt.

Ask again ONLY when the actual charge deviates from what was approved: different amount, different payment method, different service/plan, or an unexpected additional charge. Then report the deviation and ask.

## Workflow

1. Create or update a Kanban card with the service, source email, deadline/consequence, and the proposed repair.
2. Verify the service and account using a known bookmark or the link from the authenticated account—not an untrusted email link when a direct service URL is known.
3. Confirm Studio connectivity: SSH to the named Studio host, verify CuaDriver/TCC, start or reuse a durable session, and inspect the Chrome window before every action.
4. Navigate with CuaDriver/computer use. Re-capture after every navigation or state change; never reuse stale element indices.
5. Inspect billing, failed-payment reason, plan, amount, renewal cadence, and whether a payment method is already available. Do not guess or silently switch cards.
6. Use `himitsu` first, then the `op` service token, then interactive regular `op` only if needed. Secrets stay local and are never reported.
7. Stop only at the charge-triggering click. Fill card data and save the payment method autonomously; if a separate confirm-the-charge click appears, report the exact amount + card and get one confirmation for that click only. Then verify a receipt, success state, or provider transaction ID.
8. Update the Kanban card with verifiable evidence; do not mark paid/fixed from a screenshot or assumption alone.

## Fallback: Kernel

Use Kernel only after recording why the Studio route failed. Kernel is not a substitute for the computer-use requirement: use its GUI through computer use, inspect the final charge, and apply the same confirmation gate.

## Common mistakes

- Treating “payment failed” as authorization to retry indefinitely.
- Switching to a different card without reporting the amount and card suffix.
- Using `op` before checking `himitsu`.
- Typing credentials or MFA codes for convenience.
- Clicking a checkout button because the user said “take care of it” without confirming the exact charge.
- Claiming success without a provider receipt, status change, or transaction ID.
- Making Cooper confirm before entering card data (or before saving the payment method) — the ONLY gate is the charge-triggering click.
