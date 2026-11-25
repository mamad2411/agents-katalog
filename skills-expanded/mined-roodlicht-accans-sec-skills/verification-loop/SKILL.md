---
name: verification-loop
description: Structured red-team pass over your own output — surface assumptions, gaps, failure modes and security red flags before shipping.
---

# Verification Loop

## When to use

This skill triggers for Claude itself, not for the end user. Activate it when you're about to deliver non-trivial output and there's still room for one more pass. It activates when:

- You've written an analysis, review, report, patch, threat model, runbook, or policy document and are about to hand it to the user.
- The user explicitly asks for a second pass: "check your own work", "are you sure?", "are there gaps?", "red-team this", "play devil's advocate".
- Another security skill (e.g. `security-review`, `threat-modeler`, `pentest-reporter`, `ir-runbook`, `gdpr-pia`) has just produced output. This loop is the last step before delivery.
- Your own reasoning contains passages starting with "probably", "normally", "in practice", or "I assume". Those are assumptions that this loop should bring to the surface.

The pass is over what Claude has just produced, not over user input. This is a meta-skill. It does not review code or specs from third parties; it reviews your own work.

## Approach

The loop has two layers. **Layer 1** is universal and stands on its own. **Layer 2** adds security-specific checks and is removable as a self-contained block. In a non-security context you can drop the entire section without breaking Layer 1.

Work through the steps sequentially. Collect findings as you go; only formulate a verdict once every step has been done. Don't skip a step because it "doesn't seem to apply". The steps you want to skip are often exactly where the gaps are.

### Layer 1 — Universal self-review pass

1. **Scope check.** Place the original question next to your output. What was asked, what did you deliver? Mark every passage that drifts outside scope (scope creep) and every sub-question that went unanswered (scope gap). A delivered paragraph that doesn't directly serve the question is a candidate for cutting, not for keeping.

2. **Make assumptions explicit.** Search your output for "probably", "usually", "in most cases", "assuming that", "presumably". For each assumption, line up: (a) what's the assumption, (b) which source or check would confirm it, (c) what breaks if it's wrong. Assumptions where (c) yields nothing critical may stay as long as they're marked as assumptions. Assumptions where something critical breaks are blockers until they're verified or explicitly labelled "not verified, risk X".

3. **Gap analysis.** Think of three questions a critical reader would ask that you didn't answer. Think explicitly about edge cases (empty input, very large input, missing privileges), unhappy paths (timeouts, partial failures, concurrent writes), and interactions with systems you haven't seen (external services, caches, middleware, auth layers). If you can't come up with three questions, you haven't looked hard enough.

4. **Adversarial reader.** Read your output once from the perspective of someone who disagrees with your conclusion. Which phrasing is weakest? Which step in your reasoning has the least support? Which source would someone reject as non-primary or out of date? Note the three weakest points and either reinforce or cut them before delivery.

5. **Failure modes.** If your output is instructions, a patch, or a runbook: what happens when someone follows it step by step and fails halfway through? Is there a recovery path? Is the ordering reversible, or does an aborted run destroy work? If your output is an analysis: under what circumstances does the analysis not hold?

6. **Internal consistency.** Are there two statements in your output that contradict each other? Do references (to files, line numbers, sections, versions, sources) match what's actually there? If you made a choice earlier in the document, does the rest of the document follow that choice?

7. **Verdict.** Pick one of:
   - **pass**: no blockers, at most small nuances.
   - **revise**: there are blockers you can resolve yourself before delivery.
   - **rewrite**: scope is wrong or core reasoning is shaky. Starting over is cheaper than patching.

### Layer 2 — Security red flags (optional, security context)

> This section is additive and removable as a self-contained block. In a non-security repo it can be deleted without consequences for Layer 1. The verdict logic in Layer 1 stays intact.

Apply these checks on top of Layer 1 when the output contains security claims: CVE references, CVSS scores, payloads, threat models, compliance interpretations, exploit steps, risk assessments, incident-response instructions.

1. **CVE and CVSS verification.** For every CVE-ID you mention: does it actually exist in the NVD? Does the year match the timeline of your story? Does the description fit the context where you're citing it? For every CVSS score: did you verify it via the NVD or the FIRST calculator, or did you assume it because "it sounds plausible"? When in doubt, replace "CVE-2023-12345 (CVSS 9.8)" with `[verify: CVE-ID and CVSS]` or remove the claim. A non-existent CVE is more harmful than no CVE at all — it undermines trust in the rest of your output.

2. **Payload level.** Distinguish pattern-level payloads (illustrative, focused on the vulnerability class) from version-specific exploits (ready to fire against named software builds). Pattern-level (`<img src=x onerror=alert(1)>`, `{{7*7}}`, `../../etc/passwd`, `' OR 1=1 --`) is fine. Version-specific exploit chains against production targets only in explicitly agreed sandbox or lab context. Without that context, walk back to pattern-level with a `[lab: version-specific to be developed]` marker.

3. **Unsubstantiated practice claims.** Scan your output for "in practice we see", "most teams", "in most engagements", "many organizations", "teams often forget". Every such claim without a primary source must be either backed up by a reference (OWASP, NIST, MITRE, ENISA, vendor advisory, recent public report), reformulated as a hypothesis ("a plausible scenario is..."), or cut. Anecdote without source is for striking.

4. **Source quality.** Verify that references point to primary sources. OWASP cheat sheets directly, not via Medium posts. Vendor advisories directly, not via news sites. ATT&CK techniques with the T-number, not "ATT&CK says". For NL/EU compliance (AVG, NIS2, DORA, Cyberbeveiligingswet): the official text or supervising authority (Autoriteit Persoonsgegevens, RDI, DNB), not a consultancy summary.

5. **Scope demarcation: security vs legal/operational.** Does the output contain compliance or legal interpretations? Then a disclaimer must state that this is not legal advice. Does the output contain operational IR steps or offensive techniques? Then it needs a "within authorized scope" marker. Security skills inform; they don't act as the final ruling for legal advice or incident command.

6. **Security verdict.** On top of the Layer 1 verdict, flag one of:
   - **no red flags**: Layer 2 doesn't add anything.
   - **red flag — solvable**: concrete security issues you can fix now before delivery (typically: CVE/CVSS markers placed, payload reformulated, claim substantiated or cut).
   - **red flag — blocking**: the output cannot be delivered without changes or sign-off (e.g. an exploit chain outside agreed scope, or a factual claim whose accuracy you can't guarantee and which is material to the conclusion).

## Output

The result is not new text for the end user, but an internal report to yourself that determines what you deliver. Structure:

```
Verification-loop verdict: <pass | revise | rewrite>
[Security verdict: <n/a | no red flags | red flag — solvable | red flag — blocking>]

Layer 1:
- Scope: <summary — what's in, what's creep, what's gap>
- Assumptions: <list with risk level per assumption>
- Gaps: <three questions a critical reader would ask>
- Weakest points: <top 3 from adversarial pass>
- Failure modes: <list, or "n/a" for pure analysis>
- Consistency: <ok | conflicts: ...>

Layer 2 (where applicable):
- CVE/CVSS: <verified | markers placed | no CVEs cited>
- Payloads: <pattern-level | version-specific + context | n/a>
- Practice claims: <substantiated | reformulated | cut | n/a>
- Sources: <primary | corrected | n/a>
- Scope/disclaimer: <ok | added | n/a>

Actions before delivery:
1. ...
2. ...
```

On **pass** (and where applicable **no red flags**): deliver the output unchanged. On **revise**: execute the actions, then deliver. On **rewrite**: deliver nothing. Restart the task using the scope insight from the loop as your starting point.

The report stays internal unless the user explicitly asks for it. Don't paste verification-loop output as part of normal deliverables; that's noise to the reader.

## References

- NIST SP 800-115 — [Technical Guide to Information Security Testing and Assessment](https://csrc.nist.gov/pubs/sp/800/115/final), §6 (post-testing activities, validation).
- NVD — [https://nvd.nist.gov/](https://nvd.nist.gov/). Primary source for CVE verification (Layer 2).
- FIRST CVSS v3.1 calculator — [https://www.first.org/cvss/calculator/3.1](https://www.first.org/cvss/calculator/3.1). Primary source for score verification (Layer 2).
- MITRE ATT&CK — [https://attack.mitre.org/](https://attack.mitre.org/). Primary source for TTP nomenclature when output references techniques (Layer 2).

## Categories

- core
