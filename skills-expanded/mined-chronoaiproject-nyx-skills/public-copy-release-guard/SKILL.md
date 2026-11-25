---
name: public-copy-release-guard
description: Portable checklist for gating public-facing copy before release. Use when captions, posts, manifests, topics, titles, or launch copy must be checked for generic AI wording, leaked internal labels, forbidden experiment or tool names, platform topic allowlists, CTA spam, and unsupported overclaims.
version: "0.2"
license: MIT
metadata:
  category: plain
  tag:
    - public-copy
    - release-gate
    - content-safety
---

# Public Copy Release Guard

Use this method as a preflight gate before public-facing text leaves a draft, manifest, scheduler, or publishing tool.

## Gate Order

1. Identify public fields.
   - Inspect title, caption, body, alt text, topics, hashtags, card text, video scripts, metadata summaries, and generated file names that may become visible.
   - Treat unknown text fields as public until proven otherwise.

2. Remove internal process leakage.
   - BLOCK visible references to experiments, tests, A/B labels, internal variants, draft labels, run IDs, local paths, account handles, private project names, issue IDs, branch names, and unpublished tool names.
   - BLOCK source-production labels such as "private source-tool name", "private renderer name", caller-supplied internal tool/automation names, "internal", "draft", "test", "experiment", "A/B", "ab test", "control", "variant", "hypothesis", and "pipeline" unless the human explicitly wants public methodology disclosure.
   - BLOCK local file paths, private workspace paths, secret names, credential names, and private account identifiers.

3. Remove generic AI and marketing language.
   - BLOCK or rewrite "delve", "let's explore", "in conclusion", "fascinating", "journey", "game-changing", "revolutionary", "breakthrough", "unlock", "harness", "ultimate guide", "must-read", and similar filler.
   - Remove engagement-bait CTAs such as "like", "follow", "subscribe", "share this", "save this", "must watch", "do not miss", and platform-specific equivalents unless the campaign explicitly requires them.
   - Rewrite jargon labels into natural language. A card title or section heading should read like public copy, not an internal planning label.

4. Enforce platform topic rules.
   - Compare topics and hashtags against the platform or account allowlist.
   - BLOCK forbidden topics and weak tags that are unrelated to the content.
   - Prefer a small number of precise tags over broad reach tags.
   - If the platform has sensitive words, banned phrases, or disclosure rules, apply those rules before style review.

5. Check explanatory density.
   - Ensure the copy contains enough context for a public reader to understand what the object is and why it is being shown.
   - If a minimum length, context marker, or identity sentence is required by the platform playbook, enforce it.
   - Reject captions that are only a hook, slogan, link wrapper, or vague summary.

6. Guard against overclaiming.
   - BLOCK claims that imply proof, production readiness, benchmark superiority, user adoption, safety, reliability, novelty, or official status without evidence.
   - BLOCK numeric claims unless they have a fresh source.
   - WARN claims that are plausible but too broad for the supplied artifact.
   - Prefer narrow, inspectable phrasing over impact language.

7. Produce a release decision.
   - `BLOCK`: public copy contains leakage, forbidden terms, unsupported claims, unsafe content, platform-forbidden wording, or missing mandatory context.
   - `WARN`: copy is public-safe but should be narrowed, de-jargoned, shortened, or made more concrete.
   - `OK`: copy is public-safe, platform-compatible, and claim-faithful.

## Issue Format

```text
Decision: BLOCK | WARN | OK

Issues:
- severity: BLOCK
  field: [title | caption | body | topics | file name | other]
  match: [term or claim]
  reason: [why this cannot ship]
  fix: [specific rewrite or deletion]

Public-safe rewrite:
[only include if useful]
```

## Portable Forbidden-Term Seed List

Use this as a seed list, then add the platform or organization-specific rules supplied by the human:

- Internal process: "test", "experiment", "A/B", "ab test", "variant", "control", "hypothesis", "draft", "internal", "pipeline", "run id".
- Source tooling: "private source-tool name", "private renderer name", caller-supplied internal tool/automation names, private notebook names, unpublished automation names.
- Generic AI copy: "delve", "let's explore", "in conclusion", "fascinating", "journey", "game-changing", "revolutionary", "breakthrough", "unlock", "harness".
- Marketing and CTA spam: "must-read", "must-watch", "like", "follow", "subscribe", "save this", "share this", "do not miss".
- Leakage: local paths, private account names, unreleased customer names, credential variables, ticket IDs, private handles, and private repo names.

## Final Pass

Before release, scan the final rendered artifact, not just the source draft. Public leakage often appears in generated titles, card headings, topics, or scheduler metadata after the main copy has already been edited.
