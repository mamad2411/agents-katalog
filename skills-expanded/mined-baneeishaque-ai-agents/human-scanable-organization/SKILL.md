---
name: human-scanable-organization
description: >-
  Applies the 8±2 cognitive principle to organize folders for human scanability
  — consumes directory-tree-audit data and provides domain-grouping
  methodology.
category: General-Domain
---

# Human-Scanable Organization (v1)

A composer skill that applies the **8±2 human-scanability principle** — rooted
in cognitive science — to organize any collection of items into folders humans
can navigate at a glance. Delegates mechanical directory auditing to the base
[`directory-tree-audit`](../directory-tree-audit/SKILL.md) skill and provides
the judgement framework for sub-grouping decisions.

***

## Composition Rationale

This skill is a composer. It does NOT re-implement directory tree walking or
item counting. It orchestrates one base skill:

1. **[`directory-tree-audit`](../directory-tree-audit/SKILL.md)** — invoked
   FIRST to produce a deterministic JSON audit of the target directory. The
   base script's `flagged` entries identify every folder whose item count
   exceeds the threshold, providing the raw data that drives sub-grouping
   decisions.

The composer's domain-specific value-add over the base alone: the 8±2
cognitive principle (Tier C judgement) that interprets the audit data and
guides grouping strategy. A raw list of flagged folders is not actionable
without the "why" and "how" of grouping — this skill provides both.

Bidirectional discoverability: the base skill lists this composer in its
[`## Composition by Higher-Level Skills`](../directory-tree-audit/SKILL.md#composition-by-higher-level-skills)
table.

***

## 1. The 8±2 Principle

### 1.1 Cognitive Basis

Human working memory can hold approximately 7±2 chunks of information
simultaneously (Miller's Law, 1956). When applied to information architecture:

- **7±2 ≈ 8±2** in practice for folder navigation (the variance captures
  context switching cost, visual scanning overhead, and individual differences).
- Items in a list beyond this range require serial scanning rather than
  at-a-glance comprehension.
- The threshold applies at **every nesting level** — a folder with 12
  sub-folders is as hard to scan as a folder with 12 files.

### 1.2 Threshold

- **≤10 items**: human-scanable at a glance. No action needed.
- **>10 items**: exceeds the threshold. Sub-grouping should be considered.
- **>15 items**: urgent — the folder is definitively beyond comfortable scan
  range and MUST be sub-grouped before a human can navigate it efficiently.

### 1.3 When the Principle Applies

- Folder structures in any project (skill libraries, documentation, code
  repos, design assets).
- Menu and navigation trees (API docs, software UIs, CLI help hierarchy).
- Any list a human reads to decide where to go next.

### 1.4 When the Principle Does NOT Apply

- Machine-only paths (CI/CD artifacts, build output, cached data).
- Chronological lists (logs, backups by date) where the user expects a
  temporal scan.
- Flat lists that are NOT navigational (search results, tag clouds).

***

## 2. Sub-Grouping Methodology

### 2.1 Detection

Run the base skill's audit script to identify overstuffed folders:

```bash
python3 .agents/skills/general/directory-tree-audit/scripts/audit-folder-depths.py \
    --root <target-dir> \
    --threshold 10 \
    --json
```

Every entry where `"flagged": true` is a candidate for sub-grouping.

### 2.2 Grouping Strategies

Choose the strategy that best matches the folder's contents:

| Strategy | When to Use | Example |
| :--- | :--- | :--- |
| **Functional domain** | Items serve distinct purposes | `git/commit/`, `git/branch/`, `git/submodule/` |
| **Lifecycle stage** | Items progress through phases | `planning/`, `active/`, `archived/` |
| **Audience / role** | Items target different users | `admin/`, `user/`, `api/` |
| **Format / type** | Items are different file types | `scripts/`, `config/`, `docs/` |
| **Alphabetical range** | Large flat lists of named items | `a-f/`, `g-m/`, `n-z/` (last resort) |

### 2.3 Sub-Group Naming

- Use short, specific nouns (`edit/` not `commit-editing-operations/`).
- Match the parent domain's naming convention (hyphenated kebab-case for
  skill directories).
- A sub-group name MUST be unambiguous within its parent — `config/` under
  `git/` is clear; `config/` under `general/` is not.

### 2.4 Recursive Application

After sub-grouping, re-run the audit on the new structure. If a sub-group
itself exceeds the threshold, sub-group recursively. Maximum practical depth
is 3–4 levels before navigation becomes cumbersome for a different reason.

***

## 3. Worked Example

This skill's methodology was used to design the domain-grouped structure for
a ~160-skill library. The concrete taxonomy is maintained as a separate SSOT
in [`skill-library-domain-grouping`](../skill-library-domain-grouping/SKILL.md).

The example follows the pattern:

- **Top-level domains** (7–8 groups): keep flat at the root level.
- **Domains >10 items** (e.g., git, vscode, general): sub-group by function.
- **Sub-groups exceeding threshold**: further sub-group (e.g., `git/basic/`
  split into `edit/`, `message/`, `audit/`, `history/`).

***

## 4. Related Skills

- [`directory-tree-audit`](../directory-tree-audit/SKILL.md) — base skill that
  provides the mechanical directory audit consumed by this composer.
- [`skill-library-domain-grouping`](../skill-library-domain-grouping/SKILL.md) —
  project-specific domain taxonomy (worked example of this skill's methodology).
- [`skill-factory`](../../skill-factory/SKILL.md) — consumes the domain taxonomy
  to place newly-created skills in the correct location.
