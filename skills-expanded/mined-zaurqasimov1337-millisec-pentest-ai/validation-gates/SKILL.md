---
name: validation-gates
description: The false-positive elimination process. Run every candidate finding through these gates BEFORE recording it as confirmed. Use as the Validator Agent after any hunting phase. A finding that fails a gate is downgraded to "potential" or dropped. This is what separates a professional report from scanner noise.
---

# Validation Gates (Validator Agent — assume false-positive until proven otherwise)

Run each candidate finding through **all** gates. Be skeptical: your job is to try to
**disprove** the finding. Only what survives is recorded as `confirmed`.

## Gate 1 — Scope
Is the affected asset within the authorized scope (`engagement.md`)? If not → discard, and do
not have tested it. Never report out-of-scope hosts.

## Gate 2 — Reproducibility
Reproduce the issue **at least twice**. Blind/time-based signals must repeat consistently
(e.g. the delay recurs; a one-off slow response is not a finding). Save both attempts.

## Gate 3 — Evidence
You must have the **exact HTTP request + response** (or tool output) that demonstrates the
issue. No evidence → not a finding. Store it verbatim for the report.

## Gate 4 — Real impact (security boundary crossed)
Distinguish a genuine hit from noise:
- **Soft-404 / SPA calibration:** a `200` whose body ≈ the random-path baseline (length within
  ~5%) is **not** real content.
- Generic error pages, default pages, and reflected-but-encoded input are **not** vulns.
- Ask (ASVS lens): is a control that *should* be enforced actually broken? Does an attacker gain
  something (data, access, code exec, money)? If not → informational, not a vulnerability.

## Gate 5 — False-positive class checks
- **Injection (SQLi/SSTI/LFI/XSS):** the evidence marker must be present in the injected
  response **and absent from a benign baseline**, and the literal payload not merely echoed.
  Use unique products (`1337*1337→1787569`), unique markers, `root:.*:0:0:` etc.
- **Blind classes (SSRF/RFI/blind SQLi/RCE/XXE/CMDi):** require an **out-of-band callback**
  (interactsh). No callback → "potential", never "confirmed".
- **Access control / IDOR:** anonymous must be denied while the role gets real, distinct data;
  skip the user's own object; confirm across 2 accounts where possible.
- **Cross-method agreement:** a finding confirmed by ≥2 independent methods/tools is stronger.

## Gate 6 — Severity & classification
Assign honestly: **CVSS 3.1** (score + vector), **CWE**, **OWASP** category. Right-size
severity to real impact and exploit difficulty — don't inflate. Then run
`zero-day-classification` for novelty (never over-claim a 0-day).

## Outcome
- Passes all gates → record in `findings.md` as **confirmed** with full evidence.
- Fails Gate 5 blind/marker → keep as **potential** (report separately, clearly labelled).
- Fails Gate 1/2/3/4 → **drop**.
Prefer fewer, bullet-proof findings over a long noisy list.
