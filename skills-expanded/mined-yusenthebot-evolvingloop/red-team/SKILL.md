---
name: red-team
description: Adversarially verify a measurable claim or result to catch self-deception BEFORE trusting it. Use whenever the loop is about to RECORD a metric, benchmark, "it works", or a research/ML result as progress. Refutation-first, independent. Mandatory for empirical/ML claims.
---

# red-team — refute the result before you believe it

The #1 failure of a long autonomous loop is convincing-looking-but-wrong progress. This pass tries to FALSIFY a claim. Run it — ideally as a SEPARATE agent prompted to refute, not the one who produced the result — before recording any headline claim.

## 1. State the claim and its falsifier
- The claim, precisely: "X reaches 92% success on task T."
- What would make it FALSE: "fails on unseen seeds / it exploits a sim bug / a trivial baseline matches it."

## 2. Run the domain self-deception checklist

**Empirical / ML / research:**
- [ ] Re-run on ≥3 fresh seeds — holds with error bars, or one lucky seed?
- [ ] Train/eval leakage — is eval data (or its distribution) seen in training?
- [ ] Metric ≠ goal — does it ACTUALLY do the task (watch a real rollout), or just minimize a proxy / latent loss?
- [ ] Trivial baseline — does random / zero / copy-last match it? If so it's noise.
- [ ] Reward hacking / sim exploit — is "success" from gaming the sim, not solving the task?
- [ ] Look at FAILURES, not just the average — where and how does it break?

**Software / feature:**
- [ ] Works on inputs NOT in the tests (edge / empty / malformed / large)?
- [ ] Did the test exercise the real path, or is it a tautology / mocked away?
- [ ] Run it for real (use `verify`) — don't trust green tests alone.

**Sim / robotics:**
- [ ] Holds under perturbation / domain randomization?
- [ ] Is "success" a sim artifact (clipping, infinite force, frame-perfect timing)?

## 3. Verdict
`confirmed` (survives all) · `refuted` (a check failed → NOT done; fix or downgrade the claim) · `uncertain` (→ treat as not done; get more evidence).

Record one honest line: "verified: 92% over 5 seeds, beats baseline by X" OR "REFUTED: single-seed, collapses on re-run." Never record a headline claim that hasn't survived this. Residual risk isn't zero — explicitly flag anything you're <80% sure of for the human to eyeball.
