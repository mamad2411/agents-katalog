---
name: research-claim-fidelity-reviewer
description: Severity-weighted BLOCK, WARN, OK reviewer method for technical and research posts. Use when reviewing X threads, announcements, captions, or launch copy for hook strength, thread arc, generic AI vocabulary, source fidelity, claim support, numeric-claim verification, and thread format before recommending publish.
version: "0.1"
license: MIT
metadata:
  category: plain
  tag:
    - research-review
    - claim-fidelity
    - severity-rubric
---

# Research Claim Fidelity Reviewer

Use this method to review a research or technical draft before publication. The output is a severity-weighted decision, not a vibes edit.

## Severity Model

- `BLOCK`: concrete rule violation. Do not publish until fixed.
- `WARN`: publishable only with caution or after a targeted edit.
- `OK`: dimension satisfies the rubric.

Default publish recommendation:

- Recommend publish only when there are no `BLOCK` findings.
- If any numeric or status claim is not freshly verified, recommend dry-run or review-ready status only.
- Weight source fidelity and claim support more heavily than style. A strong hook cannot compensate for unsupported claims.

## Required Inputs

- Draft text, with platform and format expectations.
- Source anchors for technical claims, if available.
- Any platform rules, banned phrases, topic allowlists, and human constraints.
- Fresh verification evidence for numeric claims, or an explicit note that those claims are not live-ready.

## Review Dimensions

1. `hook_strength`
   - OK: opening names a concrete artifact, source surface, theorem or definition label, release, dataset, benchmark, repo, or precise boundary.
   - WARN: opening is abstract but related to the artifact.
   - BLOCK: opening is hype, meta-summary, unsupported achievement framing, or context-free "thread" setup.

2. `thread_arc`
   - OK: sequence moves from artifact to claim shape to boundary to research positioning.
   - WARN: middle repeats the hook or lacks evidence.
   - BLOCK: arc implies a result the sources do not support.

3. `micro_rhythm`
   - OK: sentence and post lengths vary while staying precise.
   - WARN: several adjacent units are dense, same-shaped, or hard to scan.
   - BLOCK only when the format becomes unreadable or violates platform limits.

4. `ai_vocab_and_banned_phrases`
   - OK: language is concrete and source-led.
   - WARN: copy sounds generic, motivational, or promotional.
   - BLOCK: contains banned generic AI or hype wording such as "delve", "let's explore", "in conclusion", "fascinating", "journey", "game-changing", "revolutionary", or similar forbidden terms supplied by the human.

5. `shareable_research_shape`
   - OK: draft contains a counter-intuitive constraint, named artifact, proof boundary, audit rule, precise non-claim, or inspection handle.
   - WARN: no clear reason to share beyond general interest.
   - BLOCK only when shareability depends on an unsupported claim.

6. `spam_shape_check`
   - OK: reply, caption, or thread adds evidence, a sharper frame, or a useful source pointer.
   - WARN: light context or thin source support.
   - BLOCK: generic agreement, pure mention bait, CTA bait, hashtag stack, or context-free link.

7. `safety_proxy`
   - OK: safe technical communication.
   - WARN: metaphor or wording brushes sensitive categories.
   - BLOCK: unsafe content, harassment, hate, adult content, medical advice, violence, or unprovoked public-figure attack.

8. `voice_consistency`
   - OK: voice is institutional, object-led, or otherwise consistent with the requested account.
   - WARN: pronouns or register drift without reason.
   - BLOCK: unsupported institutional claim, personal claim presented as organization fact, or leaked private identity.

9. `source_fidelity`
   - OK: each technical claim maps to a specific artifact anchor.
   - WARN: anchor is plausible but broad and should be narrowed.
   - BLOCK: claim has no anchor, cites a non-existent source, or overstates the cited artifact.

10. `technical_claim_support`
    - OK: proof status, implementation status, benchmark scope, and non-claims are preserved.
    - WARN: numeric or status claim is plausible but not freshly verified.
    - BLOCK: states or implies a proof, count, verification status, benchmark result, production readiness, or solved problem stronger than the evidence supports.

11. `research_positioning_clarity`
    - OK: significance is narrow, useful, and defensible.
    - WARN: positioning is vague or inflated.
    - BLOCK: frames a template, target, prototype, route, or condition as a completed universal result.

12. `thread_format`
    - OK: target format is manifest-ready. For X threads, tweets are separated by `---` and have no numeric prefixes.
    - WARN: separators, title handling, or metadata need cleanup.
    - BLOCK: uses numbered tweet prefixes, breaks required platform structure, or cannot be rendered safely.

## Output Format

```text
Decision: BLOCK | WARN | OK
Publish recommendation: do not publish | dry-run only | ready after human approval

Severity matrix:
| dimension | severity | note |
| --- | --- | --- |
| hook_strength | OK | [reason] |

Blocking fixes:
- [specific edit required before publish]

Warnings:
- [specific improvement or verification obligation]

Claim ledger:
- Claim: [technical claim]
  Anchor: [artifact anchor or MISSING]
  Status: supported | overclaimed | needs fresh numeric verification

Recommended rewrite:
[optional revised draft preserving all supported claims]
```

## Review Loop

1. Score every dimension once.
2. If there is a `BLOCK`, revise only the failing parts and rescore the affected dimensions.
3. If a revision changes a technical claim, re-check its source anchor.
4. Stop after the draft is `OK`, or when the remaining issues require missing evidence or human direction.
