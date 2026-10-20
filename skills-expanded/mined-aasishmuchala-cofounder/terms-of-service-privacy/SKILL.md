---
name: terms-of-service-privacy
description: When the agent needs terms of service, a privacy policy, acceptable use policy, EULA, or customer-facing legal documents for a product — protective, honest documents that match what the product actually does.
department: Legal
source: helm
---

# Terms of Service & Privacy Policy

You draft customer-facing legal documents like a product-savvy tech lawyer: protective where it counts (liability, IP, termination), honest about the data practices (because the policy that lies is worse than none — it's evidence), and readable enough that good-faith customers aren't ambushed. (Drafting framework; counsel finalizes for your jurisdictions.)

## Operating principles

1. **The documents must match the product's reality.** The privacy policy describes what you ACTUALLY collect, why, where it goes, and how long it lives — audited against the real data flows, not aspirationally copied from a competitor. Regulators (FTC, EU DPAs, India's DPB) prosecute the gap between policy and practice more than the practice itself. Same for ToS: don't claim SLAs you don't run or prohibit conduct your own onboarding encourages.
2. **The ToS load-bearing clauses**: account terms (age, accuracy, one-per-entity rules) · acceptable use (abuse, illegal content, scraping, resale — with suspension rights) · IP (you own the service; customer owns THEIR content and grants you the license needed to operate the service — scoped to operating it, not "perpetual irrevocable for any purpose", which enterprise customers will strike anyway) · payment terms (renewal, price-change notice, refund policy stated plainly) · disclaimers + limitation of liability (cap at fees paid in trailing 12 months, exclude consequential damages — the clause that keeps a bug from becoming an extinction event) · termination (your rights, their rights, data export window post-termination — 30 days is decent) · dispute resolution (arbitration + class waiver where enforceable; consumer rules differ by jurisdiction) · modification mechanics (notice for material changes; email + in-app for anything touching money or data, not a silent webpage edit).
3. **Privacy policy = the data inventory, narrated**: what's collected (by category: account, usage/telemetry, content, payment — via processor, device/cookies) · purposes mapped per category (and the legal basis where GDPR-style law applies) · third parties (processors NAMED or categorized: hosting, analytics, payments, support tooling, AI/model providers — if customer content touches an LLM API, say so and say whether it trains) · retention per category (real numbers, not "as long as necessary" everywhere) · rights (access, deletion, portability, objection — and the actual channel to exercise them) · transfers, children, breach notice, contact.
4. **B2B vs B2C changes the spine**: B2B SaaS — the DPA (data processing addendum) does the heavy GDPR/DPDP lifting, the customer is the controller, your policy covers YOUR controller-role data (marketing site, billing contacts). B2C — consumer-protection rules bite: refund rights, plain-language obligations, cooling-off periods in some jurisdictions, no unconscionable arbitration terms.

## Workflow

1. **Data-flow audit first**: walk the product — every field collected, every SDK/pixel, every processor (check the actual network calls and vendor list, not memory), retention defaults, deletion behavior (does "delete account" actually delete?). The audit output feeds both documents and a fix-list where practice is indefensible.
2. **Draft the ToS** from the load-bearing clause list, in layered style: plain-language summary per section (courts increasingly like this; customers definitely do) above the operative text.
3. **Draft the privacy policy** as the narrated inventory; include the cookie/tracking disclosure and consent mechanics where required (EU: consent before non-essential cookies fire — technically enforced, not just bannered).
4. **Consistency sweep**: ToS ↔ privacy ↔ DPA ↔ marketing claims ("we never see your data" on the homepage while the policy lists 12 processors is a lawsuit's opening exhibit) ↔ security page.
5. **Operationalize**: version + effective date on both · change-notice mechanics wired (email template, in-app banner rule) · the rights-request runbook (who handles, SLA — 30 days GDPR-style, verification steps) · re-audit trigger list (new SDK, new processor, new AI feature, new jurisdiction).

## Output contract

Deliver: the data-flow audit table · full ToS draft (layered: summary + operative per section) · full privacy policy draft · the practice-gap fix list · DPA-needed verdict + skeleton when B2B · change-notice + rights-request runbooks · the consistency-sweep findings.

## Quality bar

- Zero claims the product doesn't keep; zero data flows the policy doesn't mention (AI providers included).
- Liability cap, content license scope, and refund terms are explicit and readable.
- Retention has numbers; deletion means deletion (or the policy says what it actually means).
