---
name: write-advisory
description: Author a security or breaking-change advisory — severity, affected/fixed versions, action required (prioritized), workaround, verification step, credit.
---

# write-advisory

> Advisories are read once, scanned for the action. The structure must let the reader answer "am I affected? what do I do?" in 30 seconds.

## When to use

- A vulnerability has been fixed and customers need to know.
- A breaking change is going out and a separate advisory is warranted (beyond the release notes).
- A compliance-driven change affects callers.

## Inputs

- Advisory ID (assign `<PROJECT>-YYYY-NNNN` if you don't have one).
- Classification: Security / Breaking change / Data integrity / Compliance.
- Severity: Critical / High / Medium / Low (justify if Critical).
- Affected versions + fixed versions (exact ranges).
- For security: reporter name + consent to credit.

## Procedure

1. Read [`Advisory.md`](../../templates/Advisory.md).
2. Compute slug from the advisory ID.
3. Draft `docs/advisories/<slug>.md`:
   - **Severity + classification** at the top.
   - **Affected / fixed versions** in exact ranges, not "all old versions".
   - **Action required** in priority order. Upgrade is usually #1; workaround #2.
   - **Workaround** — concrete steps with the trade-off it makes. Expires when the upgrade is feasible.
   - **Verification** — a command / query / health-check that confirms protection after action.
   - **Technical detail** — vulnerability class (CWE) or breaking-change scope.
   - **Credit** — the reporter, with their consent. Security-research credit is the right thing.
   - **Timeline** — discovery / fix / publish. For coordinated disclosure, the dates of the disclosure process.

## Tone

- Calm + informative. Not alarming, not minimizing.
- Active voice.
- No marketing language ("we take security very seriously"). Show, don't claim.
- If the bug was bad, name what could have happened concretely; don't soften.

## Output

- File: `docs/advisories/<slug>.md`.
- Summary: advisory ID + severity + affected-range + fixed-range.

## Quality bar

- Severity is justified (impact + exploitability for security; breaking scope for breaking change).
- Affected + fixed versions are exact ranges.
- "Action required" lists at least one bullet beyond "upgrade" (a workaround or a verification).
- Verification command/query present.
- For security: CVE referenced if available; reporter credited (or "reported privately").

## Anti-patterns to avoid

- "All versions before today are affected" — name a range.
- No workaround offered. There's almost always one even if it's "block via firewall".
- No verification step. Customers can't confirm they're protected.
- Marketing tone in the description. The reader is anxious; calm + concrete beats reassuring.
