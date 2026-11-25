---
name: litig-demand-intake
version: 1.0.0
description: Intake a matter where your client wants to send a demand letter by gathering facts, damages, legal basis, leverage, and desired outcome.
author: matrixx0070
tags: [litigation, demand-letter, intake, damages, pre-suit]
capabilities: []
---

## When to use
Use this when a client asks you to prepare or evaluate a demand before any letter is drafted. Your job is to assemble the raw material: what happened, who owes whom, how much, and what the client actually wants. Do this before anyone drafts a single sentence of demand language.

**Not for:** actual drafting (see litig-demand-draft) or responding to a demand your client received (see litig-demand-received).

## Method
1. Capture the parties, roles, and any entity/individual distinctions (who is the correct obligor).
2. Build a chronology of the underlying transaction or event with dated documents.
3. Identify the legal basis: contract breach, tort, statute — and the elements each requires.
4. Quantify damages with categories (direct, consequential, statutory, fees) and supporting math.
5. Assess leverage: solvency, reputation exposure, contractual fee-shifting, statutory multipliers.
6. **Decision point:** if a limitations deadline is near (under 90 days), flag it for the attorney immediately and prioritize preserving the claim over drafting polish.
7. **Decision point:** if the desired outcome is a continuing business relationship, note a conciliatory tone target; if a clean break, note a hard-deadline tone.
8. Record the client's authorized settlement floor and walk-away number.
9. Route the intake summary to a supervising attorney for review before any demand is drafted or sent.

## Example
> Client: former vendor stiffed on a $42,000 invoice. Intake captures signed MSA (breach-of-contract basis), invoice + delivery receipts, $42k principal plus MSA §9 attorney-fee clause, debtor is a solvent LLC, client wants payment and is willing to accept $38k to avoid suit. Limitations: 4-year written-contract period, event 8 months ago — no deadline pressure.

## Pitfalls
- **Wrong obligor.** Suing or demanding from the individual when the contract binds the entity kills leverage — confirm the signatory's capacity.
- **Damages inflation.** Padding numbers you cannot substantiate undermines credibility if litigation follows; keep every figure sourced.
- **Missing the clock.** Statutes of limitation and pre-suit notice conditions (e.g., some consumer or construction statutes) can bar a claim; screen for them at intake.
- **No authority ceiling.** Without a client-authorized settlement range you cannot negotiate; capture it now.

## Output format
```
MATTER: <client v. target>
PARTIES: <correct obligor, capacity>
CHRONOLOGY: <dated events w/ doc cites>
LEGAL BASIS: <theory + elements>
DAMAGES: principal $__ | consequential $__ | fees $__ | total $__
LEVERAGE: <solvency / fee-shift / statutory>
DEADLINES: <limitations / notice conditions>
CLIENT GOAL: <outcome; settlement floor $__>
ATTORNEY REVIEW: <pending / cleared>
```

## Reference
Statutes of limitation vary widely by jurisdiction and claim type — written contracts commonly run 4-6 years, oral contracts 2-4, and many torts 2-3 years; always verify the governing state's code. Some claims carry pre-suit notice prerequisites (e.g., Texas DTPA 60-day notice, medical-malpractice notice-of-claim statutes, government tort-claims acts with short windows often 6 months to 1 year). Attorney-fee recovery generally requires a contractual clause or a fee-shifting statute — the American Rule presumes each side bears its own fees. Statutory multipliers (treble damages under many consumer, antitrust, or RICO provisions) can dramatically change leverage. This is general information and not legal advice; requirements vary by jurisdiction and a licensed attorney must confirm them.
