---
name: lint
description: Health-check the wiki — find orphan pages, dead links, missing cross-references, and structural issues. Optionally auto-fix.
argument-hint: '[--fix to auto-fix structural issues]'
model: opus
---

User's request: $ARGUMENTS

# Lint Wiki

You are running a health check on the wiki knowledge base. Structural checks are handled by a script (fast, deterministic). You handle the semantic checks that require reading and judgment.

## Vault Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/vault-discovery.md`.

Store the resolved vault path as `$VAULT`.

## Step 1: Run Structural Checks

Run the lint script. It checks dead links, orphan pages, missing frontmatter, missing outbound links, index gaps, stale pages, and empty sections — without loading any wiki content into context:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh" "$VAULT"
```

Capture the output. Each line is a finding in the format `SEVERITY|check|path|detail`.

Parse and count findings by severity (CRITICAL / WARNING / SUGGESTION).

## Step 2: Semantic Checks (LLM)

The script cannot detect these — they require reading and reasoning. Read `wiki/index.md` to orient yourself, then selectively read pages flagged as relevant.

### Missing concepts

Look at the index for terms that appear frequently but have no dedicated concept page. A term mentioned in 3+ source or entity pages without a `concepts/<term>.md` is a candidate.

### Contradictions

For pages that cover the same entity or concept, check whether they make conflicting claims. Flag pairs for human review — do not auto-fix contradictions.

### Missing cross-references

Look for pages that clearly relate to each other but don't link. This is a suggestion-level finding.

Only read pages you actually need for these checks — do not load the entire wiki.

## Step 3: Report Findings

Present findings organized by severity:

```
Wiki Health Check — <date>

Pages scanned: <count>
Issues found: <count>

## Critical

### Dead Links (<count>)
- wiki/concepts/foo.md → [[bar]] target not found
- ...

### Missing Frontmatter (<count>)
- wiki/entities/foo.md — missing: type, updated
- ...

## Warnings

### Orphan Pages (<count>)
- wiki/entities/baz.md — no inbound links
- ...

### Index Gaps (<count>)
- wiki/concepts/qux.md — not listed in index.md
- ...

### Missing Concepts (<count>)
- "term" mentioned in N pages but has no concept page
- ...

## Suggestions

### Stale Pages (<count>)
- wiki/sources/old.md — last updated 2025-01-01 (105 days ago)
- ...

### Missing Cross-References
- wiki/concepts/foo.md and wiki/concepts/bar.md discuss similar topics but don't link

## Summary

<N> critical, <N> warnings, <N> suggestions
```

## Step 4: Auto-Fix (if `--fix` passed)

If `$ARGUMENTS` contains `--fix`, fix structural issues only:

1. **Dead links** — create stub pages: minimal frontmatter + `status: stub` + note
2. **Missing frontmatter** — infer `type` from directory, set dates to today, add `wiki/<type>` tag
3. **Index gaps** — add missing pages to the appropriate section in `wiki/index.md`
4. **No outbound links** — read the page and add wikilinks to related pages already in the index

Do NOT auto-fix:
- Contradictions (human judgment required)
- Stale pages (may be intentionally stable)
- Missing concepts (requires writing real content)

Report what was fixed after running.

## Step 5: Log the Operation

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/log-append.sh" "$VAULT" "lint" "Health Check"
```
