---
name: omv-critic
description: |
  Performs adversarial pre-submission review of an Evidence.v1 finding plus optional ThreatMap.v1 and Verification.v1 sidecars. Use before `/omv-report` when the user wants likely CNA rejection reasons, report argument quality review, a reject_risk rating, or a recommendation of which researcher_goal (VulDB, CVE, GHSA, advisory) fits the finding.
---

# omv-critic

Challenge the finding before report submission.

## Invocation

```text
/omv-critic <id>
```

## Workflow

1. Read `.omv/findings/<id>.yaml` using `contracts/evidence.v1.yaml` as the local schema reference.
2. If present, read `.omv/threatmaps/<id>.yaml` using `contracts/threat-map.v1.yaml` as the local schema reference.
3. If present, read `.omv/verifications/<id>.yaml` using `contracts/verification.v1.yaml` as the local schema reference.
4. Run or inspect `omv findings validate <id>` and `omv verification validate <id>` when the sidecar exists.
5. Evaluate argument quality separately from structural validation.
6. Evaluate acceptance precedent (below) — evidence quality and acceptance odds are different axes.
7. Output `reject_risk: low|medium|high` and a recommended `researcher_goal`.
8. For medium or high risk, list 3-5 likely CNA or maintainer rejection reasons and concrete strengthening actions.

## Review Focus

- novelty and duplicate risk
- acceptance precedent (see below)
- affected version proof
- source -> sink -> guard clarity
- local observed result quality
- CVSS and impact overclaiming
- disclosure readiness

If `reject_risk: high`, do not recommend `/omv-report` yet.

## Acceptance-Precedent Method

Ask three questions the machine gates cannot:

1. **Class precedent in this ecosystem**: has this CNA/database accepted this
   vulnerability class for library packages before (e.g. code execution in a
   parser when input is attacker-controlled in realistic deployments)? No
   precedent means higher bar: the finding needs an airtight untrusted-input
   story, not just a reachable sink.
2. **Maintainer stance**: does the project document the behavior as intended
   (opt-in features, "power user" escape hatches, README warnings)?
   By-design findings die at the maintainer even when technically real.
   Check README/docs/issues for the project's stated position.
3. **Public discussion**: verify the dedup block covers the discussion sources
   (issues/PRs, commits, blogs — all six fields). An advisory-clean finding
   with an unsearched issue tracker is an unreviewed novelty claim: do not
   greenlight `/omv-report` until those searches are recorded. A public
   issue/PR disclosing the same bug caps reject_risk at high regardless of
   evidence quality.

## Recommended researcher_goal

Output one goal with reasoning:

- `VulDB`: accepts publicly-disclosed and lower-precedent classes; entry is
  near-guaranteed but researcher credit is thin. Fits evidence-complete
  findings with weak CVE precedent.
- `GHSA`: best when the package lives on GitHub and the maintainer is likely
  to concur; draft advisories travel with a fix.
- `CVE`: needs class precedent and a cooperative CNA; slowest, strongest.
- `advisory`: direct maintainer contact first — often the fastest real fix
  even when no identifier is ever issued.
- `triage`: evidence or novelty is too weak for any submission; say so.

A finding blocked by public disclosure gets no goal recommendation — recommend
archival or a variant campaign instead (`/omv-radar variant <id>`).

## Rejection-Risk Method

Frame findings as argument-quality gaps:

- Novelty: duplicate risk, same affected range, same fix, unresolved CNA path,
  or public disclosure already on record.
- Evidence chain: missing file:line source, sink, guard, transform, or ThreatMap edge.
- Verification: failed, stale, or missing adversarial review when the user expects a high-confidence submission.
- Reproducibility: no user-reported local observation or unclear tested version.
- Severity: CVSS metric overclaim, missing preconditions, or unsupported impact claim.
- Precedent: class without prior acceptance, or maintainer-documented intent.
- Disclosure readiness: no contact plan, unclear vendor, or missing timeline.

Use generic, sanitized examples when explaining risk. Do not copy conclusions from a real vulnerability case unless the user supplied that finding as active research context.
