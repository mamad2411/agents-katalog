---
name: legal-review-contract
version: 1.0.0
description: Review a contract against a negotiation playbook, flag deviations from preferred and fallback positions, and produce redline-ready comments with a sign/negotiate/reject verdict.
author: matrixx0070
tags: [legal, contract, review, redline, playbook, escalation]
capabilities: []
---

## When to use
Use this to review an incoming or draft contract — MSA, SOW, DPA, license, vendor or partner agreement — against a defined playbook of acceptable terms. It finds where the document departs from what your organization will accept and prepares the redline.

**Not for:** contracts with no playbook or a novel structure (escalate to counsel), drafting a contract from scratch, or a one-line clause question (use `legal-response`). Final legal sign-off on execution-ready contracts stays with an attorney.

## Method
1. **Identify contract type and load the playbook.** Preferred, fallback, and walk-away position for each key clause. *Decision point:* no playbook exists → escalate to counsel rather than guess.
2. **Read for the critical clauses.** Liability caps and exclusions, indemnity, IP ownership and license grant, confidentiality, data protection, term and termination, payment, warranty, governing law, assignment, auto-renewal.
3. **Compare each clause to the playbook.** Mark: acceptable / within-fallback / beyond-fallback / missing / one-sided.
4. **Assess each deviation.** State the risk it creates and its business impact.
5. **Draft the redline.** For every problem clause, give the specific proposed edit plus a one-line rationale for the counterparty.
6. **Prioritize.** Separate deal-breakers (must fix) from negotiables (nice to fix).
7. **Flag counsel items.** Anything novel or beyond fallback goes to an attorney before signature.

## Example
Contract: vendor MSA. Liability clause caps vendor at 3 months' fees and excludes all indirect damages including a data-breach carve-out. Playbook: cap ≥ 12 months' fees, breach must be super-cap. Status: beyond-fallback. Risk: a breach of our customer data could leave us bearing seven-figure exposure against a capped vendor. Redline: "Liability cap raised to 12 months' fees; data-breach and confidentiality violations excluded from the cap." Rationale: "Aligns risk with the sensitivity of data processed." Priority: deal-breaker. Escalate: yes — cap structure beyond fallback.

## Pitfalls
- **Reviewing without a playbook.** "Looks fine" is not a standard; every clause needs a benchmark.
- **Flagging problems without proposed text.** A comment the counterparty can't paste in stalls the deal.
- **Missing what's absent.** A missing indemnity or DPA is a deviation too — check for silence, not just bad language.
- **Treating every deviation as a deal-breaker.** Mixing must-fix with nice-to-fix buries the real blockers.

## Output format
```
Contract / parties / type / playbook:
Summary verdict: sign | negotiate | reject
Clause table:
  | Clause | Playbook position | Contract says | Status | Risk |
Redlines:
  | Clause | Proposed edit | Rationale |
Deal-breakers vs. negotiables:
Escalate to counsel: <items beyond fallback / novel>
```

## Clause playbook
Use this as your default negotiation grid for a commercial MSA/SOW/DPA where you are the customer or a balanced-risk party. Numbers are typical mid-market defaults, not legal advice — adjust to deal size and data sensitivity, and escalate anything in the walk-away column.

| Clause | Standard position | Acceptable fallback | Walk-away / escalate |
|---|---|---|---|
| Limitation of liability (cap) | Mutual cap = 12 months' fees paid/payable in the trailing 12 months | 6-9 months' fees, or 1x total contract value on short terms | Cap < 3 months' fees; cap on your payment obligations; one-sided cap protecting only them |
| Consequential/indirect damages | Mutual waiver of indirect, incidental, consequential, special, punitive damages | Mutual waiver with lost-profits carve-in for confidentiality breach | One-sided waiver (only they're protected); waiver that also bars direct damages |
| Liability carve-outs (super-cap) | Breach of confidentiality, data/security breach, IP infringement, indemnity obligations, gross negligence/willful misconduct sit outside the cap | Some carve-outs super-capped at 2-3x the general cap rather than unlimited | No carve-outs at all — a data breach limited to 3 months' fees; escalate |
| Indemnity | Vendor indemnifies you for third-party IP infringement and their data/privacy breach; mutual for bodily injury/property damage | Add reasonable caps and control-of-defense terms; narrow IP indemnity to unmodified use | Uncapped indemnity flowing FROM you; you indemnify their negligence; escalate |
| IP ownership / assignment | Each party keeps pre-existing/background IP; you own your data and deliverables you paid for (in SOW work) | Vendor retains tooling/know-how but grants you a broad license to use deliverables | Assignment of YOUR background IP; vendor owns your data or your paid deliverables; escalate |
| License grant | Non-exclusive, worldwide license for the term, covering affiliates and normal use | Named-user or usage-metered scope with clear overage terms | Perpetual exclusivity; license revocable at their sole discretion; escalate |
| Confidentiality term | Survives 3-5 years post-termination; trade secrets protected for as long as they remain secret | 2 years for ordinary confidential info | Perpetual confidentiality on ordinary business info; one-sided obligations |
| Data protection / DPA | Signed DPA with Art. 28 processor terms, security measures, breach notice ≤ 72h, SCCs for cross-border transfer | Breach notice ≤ 5 business days; audit-by-report (SOC 2) instead of on-site | No DPA where personal data flows; unrestricted subprocessing; escalate |
| Term & renewal | 1-year initial term, renewal by mutual written agreement | Multi-year with annual price-increase cap (e.g. ≤ 5% or CPI) | Multi-year lock with no exit and uncapped price increases |
| Auto-renewal / notice period | Auto-renew only with ≥ 60-90 days' notice to cancel and a renewal reminder | Auto-renew with 30-day notice and pre-renewal email | Auto-renew with < 30 days' notice or no exit; one-sided; escalate |
| Termination (convenience & cause) | Termination for convenience on 30-60 days' notice; for cause with 30-day cure | Convenience right for you only, or after an initial committed period | No termination right for you; immediate termination by them without cure |
| Warranty | Services performed in a professional/workmanlike manner; deliverables conform to spec for 90 days | 30-day warranty with re-perform remedy | "AS IS", all warranties disclaimed with no re-perform/refund remedy |
| Governing law & venue | A familiar US state (e.g. Delaware, New York) with local courts | Neutral US state; arbitration (AAA/JAMS) seated domestically | Foreign governing law with no arbitration; venue that's impractical for you; escalate |
| Assignment | Neither party assigns without consent; consent not required for merger/acquisition of the whole business | Consent not unreasonably withheld | They may assign freely to anyone (incl. competitors); you may not assign at all |
| Insurance | CGL $1-2M per occurrence; cyber/tech E&O $2-5M where data is processed; workers' comp per statute | $1M CGL / $1M cyber for low-data engagements | No insurance where they host/process your data; escalate |
| Payment terms | Net-30 or net-45 from valid invoice; disputed amounts withheld pending resolution | Net-30 with 1-1.5%/mo late interest after cure notice | Payment in advance with no refund; unilateral fee changes mid-term |
| Publicity/reference rights | No use of your name/logo without prior written consent | Logo on customer list only, revocable on request | Perpetual publicity rights or press releases without approval |
| Force majeure | Mutual, excuses non-performance for genuine events; payment obligations survive | Adds a termination right if the event exceeds 30-60 days | One-sided (excuses them but not you); covers ordinary business/economic conditions |

## Red flags
These trigger counsel escalation regardless of what the playbook fallback would allow — never self-approve:
- Unlimited or uncapped liability on your side.
- Uncapped indemnity flowing FROM you (especially covering their acts or IP).
- Any assignment or ownership grant of your background/pre-existing IP.
- Perpetual exclusivity or perpetual non-competes.
- Non-compete or non-solicit obligations bundled into a commercial contract.
- One-sided auto-renewal with no meaningful exit.
- Foreign governing law with no arbitration fallback.
- Most-favored-nation (MFN) pricing/terms clauses.
- Unilateral amendment rights (they can change terms/policies by posting a URL).

## Reference
Redline etiquette keeps a deal moving:
- **Comment vs. edit.** Use tracked changes for concrete text you want; use margin comments to ask a question or explain a business constraint you can't unilaterally fix.
- **Tracked-changes hygiene.** Turn tracking on before you start, accept nothing silently, and clean up stray formatting marks. Send one consolidated turn, not five.
- **Rationale per change.** Attach a one-line "why" to each edit ("cap raised to align with data sensitivity") — counterparties concede faster when the reason is business-obvious, not just "our policy."
- **Batch deal-breakers vs. negotiables.** Lead your cover note with the 2-4 must-fix items and label the rest as nice-to-have; burying blockers among stylistic tweaks slows sign-off.
- **Phrase counters politely and firmly.** Prefer "We'd propose X to reflect Y" over "This is unacceptable." Offer a fallback in the same breath ("or, if X is difficult, we can live with Z") so each turn narrows the gap.
