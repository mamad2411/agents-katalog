---
name: sibling-uniqueness-audit
description: Use before launching or after editing any rank-and-rent or PBN site that has sibling sites, when writing copy for a site cloned from a source design, or when the user asks to check for duplicate content, shared H2s, or "town-name-swapped" copy between their sites.
---

# Sibling Uniqueness Audit

## Overview

Sibling rank-and-rent sites share design, never copy. Google treats town-name-swapped duplicates as doorway pages. This skill runs a mechanical cross-site overlap check so "I wrote original copy" is verified, not claimed.

## When to Use

- Step 9 of the rank-and-rent factory (`~/.claude/guides/WORKFLOW-TEMPLATES.md`) — blocking gate before launch
- After ANY copy edit to a site that has siblings
- Before launch of a site cloned from a SOURCE design site
- FACTS.md lists the sibling sites — audit against all of them

## Run It

```bash
python3 ~/.agents/skills/sibling-uniqueness-audit/audit.py \
  "/path/to/Site A" "/path/to/Site B" ["/path/to/Site C" ...]
```

- Scans `src/` only; skips specs, README, AGENTS.md, node_modules, dist
- **Reads page copy wherever it lives** — markup (`.astro/.md/.mdx/.html`) *and* content data
  modules (`.ts/.tsx/.js/.jsx`), because on these sites every customer-facing word is an HTML
  string in `src/data/services.ts`, not in a template
- **Excludes application code** — `src/lib/`, `src/pages/api/`, `middleware.ts`, configs and
  tests. Sibling sites are *supposed* to share architecture; only shared **prose** is the risk
- For code files only string and template literals are read, so identifiers, imports, control
  flow and developer comments can never be reported as duplicate copy
- Prints a **coverage block per site** before the verdict: files scanned, sentence counts, and
  the top contributing files. Read it. If `services.ts` is not near the top, something is wrong
- Reports per pair: shared headings (h1–h3), identical sentences (≥8 words), near-duplicates
  (difflib ≥ 0.85)
- Exit 0 = PASS, exit 1 = FAIL

### Why it is a code denylist, not a `src/data/` allowlist

The audit shipped for months reading only `.astro/.md/.mdx/.html`. Every word of copy on the
mobile-mechanic sites lives in `src/data/services.ts`, so it never read the content it exists to
check and printed `PASS — no significant overlap` for two sites sharing 112 identical sentences,
including textbook town-swaps like `…on a york driveway` ~ `…on a colchester driveway`.

An allowlist of `src/data/` would just re-encode today's layout: the next site that puts copy in
`src/content/` or inline in a page would silently drop out of the audit the same way. So the model
is **include everything, subtract known code paths**. A new *content* location is picked up with
no edit to the script. A new *code* location shows up as a false positive — loud, cheap, fixable.
The failure mode points in the safe direction.

### Fail-loud coverage checks

Two guards make a silent miss much harder. Both force the verdict to
`FAIL — coverage floor breached, audit is not trustworthy`, which is **not** a content failure —
it means the audit could not see enough to judge, and "cannot verify" must never read as "pass".

| Guard | Fires when |
|---|---|
| Coverage floor | A site yields fewer than 40 sentences. Override with `--min-sentences N` for a genuinely tiny site. |
| `!! UNREAD BULK` | A file has no reader for its extension (≥8KB), or was scanned but produced 150+ readable words and zero sentences. |

`UNREAD BULK` is the one that would have caught the original bug on day one: run the old
markup-only extension set today and it names `src/data/services.ts (154685 bytes, no reader for
this extension)` instead of printing PASS. If it fires, teach the extractor to read that file
before trusting any verdict.

## Reading the Report

| Finding | Action |
|---|---|
| `[HEADING]` any shared heading | FAIL. Rewrite the heading structurally — different angle, not a synonym swap. |
| `[EXACT]` shared sentence | FAIL. Rewrite one side from scratch. |
| `[NEAR]` town-name-swapped sentence | FAIL — this is the classic violation. Rewrite structurally. |
| `[NEAR]` hits that are CSS/class-attribute soup or deliberately shared legal/attribution lines (e.g. "reviews from previous business" disclosure) | Judgement call — note them in the report to the user, don't count toward the verdict. |
| `!! UNREAD BULK` or a coverage floor breach | Blocking, but it is **not** a duplicate-content finding. The audit could not read the site. Fix the extractor, then re-run before judging content at all. |

A FAIL verdict is blocking, same as a Critical quality-check issue: fix, re-run, only then deploy.

## Fixing Failures

Rewrites must be **structural**: different page skeleton, different heading angles, different sentence rhythm — not paraphrase. Re-run the audit after rewriting; repeat until PASS. Dispatch rewrites with the site's FACTS.md pasted in (see client-intake skill) so originality doesn't come at the cost of fabricated facts.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Auditing only the new site vs its SOURCE | Audit against ALL siblings — pairs the user didn't mention have shipped with shared H2s before. |
| Treating near-duplicates as "close enough to original" | Town-name swaps ARE the failure mode this exists to catch. |
| Running it only at launch | Post-launch edits reintroduce overlap; re-run after copy changes. |
| Trusting a copywriter agent's "all original" claim | Run the script. Claims aren't evidence. |
| Reading `PASS` without reading the coverage block above it | A PASS from a run that read 0 sentences of the actual copy is what this skill shipped with for months. Check `services.ts` is in the top contributors. |
| "Fixing" a FAIL by narrowing what the script scans | The verdict is the messenger. Rewrite the copy, not the audit. |
