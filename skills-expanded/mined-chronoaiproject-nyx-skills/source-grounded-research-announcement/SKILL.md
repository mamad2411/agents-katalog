---
name: source-grounded-research-announcement
description: Method for drafting and reviewing source-anchored research or technical announcements, especially X threads or short posts. Use when public copy must distinguish claimed from not claimed, attach every technical claim to an artifact anchor, avoid overclaiming, remove generic AI phrasing, and require dry-run plus human approval before live publishing.
version: "0.1"
license: MIT
metadata:
  category: plain
  tag:
    - research-announcement
    - source-fidelity
    - public-copy
---

# Source-Grounded Research Announcement

Use this method to turn a technical artifact into a public announcement without inflating what the artifact proves.

## Non-Negotiables

- Do not publish or trigger a live publishing path unless the human has reviewed a successful dry run and explicitly approved live release.
- Treat every technical claim as unsupported until it has a source anchor: file path, theorem or definition label, declaration name, README section, repository object, release note, paper section, dataset card, benchmark report, or other inspectable artifact.
- Re-verify numeric claims immediately before live release. Counts, dates, benchmark values, model sizes, status labels, and repository totals must not rely on memory.
- Preserve proof and verification status exactly. Do not turn a template, target, route, negative result, witness inventory, prototype, draft, or stated objective into a solved result.
- Keep a visible claim ledger whenever the topic invites overreading.
- Remove generic AI and hype phrasing: "delve", "let's explore", "in conclusion", "fascinating", "journey", "game-changing", "revolutionary", "breakthrough", "changes everything", and similar filler.

## Workflow

1. Collect source material before drafting.
   - Ask for or locate the artifact, repo, paper, docs, logs, benchmark output, release notes, or source bank.
   - Build a short source note with the artifact anchors, the draftable claims, the non-claims, open verification obligations, and any numeric claims.
   - If the evidence is missing, draft only a source request or a narrower announcement.

2. Define the claim boundary.
   - Write `Claimed:` bullets for exactly what the source establishes.
   - Write `NOT claimed:` bullets for tempting interpretations the source does not support.
   - Include proof status, implementation status, benchmark scope, and data scope when relevant.

3. Draft three angles when time permits.
   - Artifact-led: start from the named source object.
   - Constraint-led: start from the boundary, failure mode, proof obligation, or audit rule.
   - Research-positioning-led: start from why this artifact matters within a larger line of work, while keeping the claim narrow.

4. Format for the target platform.
   - For X threads, use 5 to 9 tweets by default.
   - Separate tweets with lines containing only `---`.
   - Do not use `1/`, `2/`, `(1)`, or numbered tweet prefixes.
   - Prefer one canonical link or artifact reference over link stacks.
   - Avoid tag and hashtag stacks unless the human supplied them.

5. Attach anchors in drafting metadata.
   - For each technical sentence, record the specific anchor that supports it.
   - Keep anchors adjacent to the draft in reviewer notes, a table, or a manifest field.
   - Mark numeric claims as `verify_before_post: true` until rechecked.

6. Review adversarially.
   - BLOCK if any technical claim lacks an anchor.
   - BLOCK if the copy implies a result, proof, verification, benchmark win, or production status stronger than the source supports.
   - BLOCK live release if numeric claims have not just been re-verified.
   - WARN if an anchor is too broad and should be narrowed before publishing.
   - WARN if the post sounds promotional rather than artifact-led.

7. Run dry-run first.
   - Render the post, manifest, or publish payload without posting.
   - Show the human the exact final copy, source anchors, verification obligations, and reviewer findings.
   - Accept only explicit human approval for live release after dry-run success.

## Claim Ledger Template

```text
Claimed:
- [narrow claim] - anchor: [artifact path, section, declaration, report, or link]
- [narrow claim] - anchor: [artifact path, section, declaration, report, or link]

NOT claimed:
- [tempting stronger interpretation that is not supported]
- [proof, benchmark, production, or scope claim the artifact does not establish]

Verify before live release:
- [numeric or status claim requiring fresh check]
```

## Reviewer Checklist

- Hook names a concrete artifact, boundary, theorem or definition label, source file, repo, release, or precise result shape.
- The thread or post moves from artifact to claim shape to boundary to significance, without repeated filler.
- Every technical claim maps to an inspectable artifact anchor.
- Non-claims are explicit when the subject is likely to be overread.
- Numeric claims have fresh evidence.
- The final wording avoids hype, generic AI phrases, engagement bait, and unsupported institutional claims.
- The publishing path is still dry-run unless the human has approved live release after seeing the final payload.
