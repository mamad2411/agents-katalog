---
name: qa-quality-attributes
version: 1.0.0
description: ISO/IEC 25010 quality-characteristic pass for scoping test coverage beyond pure functional correctness. Load when planning test strategy for a feature or release to make sure non-functional risk isn't silently skipped.
---

# Quality Attributes Pass (ISO/IEC 25010)

Functional testing (does it produce the right output) is necessary but not sufficient. Before calling test coverage complete, walk the ISO/IEC 25010 characteristics and decide, explicitly, which apply to this piece of work and which don't — "not applicable" is a valid answer, silence is not.

## The characteristics

**Functional suitability** — completeness (does it cover the stated requirements), correctness (right output), appropriateness (does the way it works actually fit the task). This is the default focus of most test suites; the rest of this list is what's usually under-tested.

**Performance efficiency** — time behavior (latency under expected load), resource utilization (memory/CPU/connections), capacity (behavior at the stated max scale, and just past it). Test against a stated number, not a vibe — if no target exists, that's a gap to flag, not to guess past.

**Compatibility** — co-existence with other software on the same environment, interoperability (does it correctly exchange data with the systems it integrates with, including older/newer versions of them).

**Usability** — recognizability, learnability, operability, error protection (does the UI stop likely mistakes before they happen), UI aesthetics, accessibility. Accessibility is not optional polish — see the `accessibility` skill for a WCAG-specific pass.

**Reliability** — maturity (failure rate under normal operation), availability, fault tolerance (behavior when a dependency fails — degrade gracefully or fail loudly, never fail silently), recoverability (state after a crash/restart).

**Security** — confidentiality, integrity, non-repudiation, accountability (audit trail), authenticity. Cross-reference against OWASP Top 10-class issues as part of any input-handling or auth-adjacent test plan.

**Maintainability** — modularity, reusability, analyzability (can a failure be diagnosed from logs/traces alone), modifiability, testability (is the code actually structured so it *can* be tested, or does testing require heroics). Testability gaps found here are architecture feedback, not just a QA note — surface them to the engineering agent.

**Portability** — adaptability (different environments/config), installability, replaceability (can a component be swapped without breaking callers).

## How to use this in test planning

1. Go down the list and mark each characteristic: **in scope / explicitly out of scope / not applicable**, with one line of reasoning each.
2. For everything in scope, name the concrete test(s) that cover it — a checkbox with no corresponding test is a gap, not coverage.
3. Weight depth by risk and blast radius, not by giving every characteristic equal time — a login form needs deep security and usability scrutiny and shallow portability scrutiny; a CLI batch job is the reverse.
4. Anything marked out of scope on a release with real user impact should be said out loud to whoever owns the release decision, not silently dropped.

This pass is what prevents "all tests green" from meaning "we only checked the happy path." Pair with `qa-techniques` for *how* to test each in-scope characteristic, and `qa-triage` for classifying what a failure here actually means.
