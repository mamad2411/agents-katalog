---
name: __SKILL_NAME__
description: >-
  __DOMAIN__ — REPLACE with the concrete triggers for this reference: the tasks, terms,
  and decisions where Claude should consult it. Use when writing, debugging, or reviewing
  work in this domain. Be specific; the description is what makes the skill fire.
---

# __SKILL_TITLE__ — cited reference

A fact-checked reference on **__DOMAIN__**, bundled with this plugin and built from primary
sources with adversarially-verified claims. **Don't dump the whole guide into context —
route to the one relevant section and read only that.**

## How to use it

1. **Route first.** Read the navigation manifest — it pre-joins each guide section (stable
   ids `#s0`…) to its code samples and primary sources:

   `${CLAUDE_PLUGIN_ROOT}/index.json`

   Pick the section whose `title` matches the task; note its `lines` range and `samples`.

2. **Read just that section** (use the `lines` range — do not load the whole file):

   `${CLAUDE_PLUGIN_ROOT}/docs/GUIDE.md`

   Each section is self-contained: principle → practices → inline citations → a `→ Code:`
   pointer to its runnable sample.

3. **Open the sample** the section points to, under `${CLAUDE_PLUGIN_ROOT}/code_samples/`.

4. **For provenance**, resolve a citation key (e.g. `[ex]`) to its source via
   `${CLAUDE_PLUGIN_ROOT}/raw_outputs/sources/INDEX.md`. Per-claim evidence (supporting
   quote + verification votes) is in
   `${CLAUDE_PLUGIN_ROOT}/raw_outputs/claims/verified-claims.json` — heavy; load only when
   you need claim-level provenance.

For fast "what should I do here?" decisions, jump to the **Quick decision cheat-sheet** and
**Top anti-patterns** near the end of the guide.

## Fallback if the bundled files aren't reachable

Fetch the same files from the public repo with WebFetch instead (replace with your URLs):

- Manifest: `https://raw.githubusercontent.com/__OWNER__/__REPO__/main/index.json`
- Guide: `https://raw.githubusercontent.com/__OWNER__/__REPO__/main/docs/GUIDE.md`
- Source index: `https://raw.githubusercontent.com/__OWNER__/__REPO__/main/raw_outputs/sources/INDEX.md`
