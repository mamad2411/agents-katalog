---
name: cli-audit-doc
metadata:
  author: clement
description: "Audit documentation quality with weighted scoring across 12 dimensions (Diataxis coverage, completeness, freshness, readability, examples, accessibility, CI testing). Detects doc anti-patterns (Wall of Text, The Lie, Jargon Soup). Use when reviewing doc quality, auditing documentation, checking for stale docs, or saying 'audit docs', 'doc quality', 'documentation review'. Invoke with an optional file or directory path."
argument-hint: "[file-or-directory]"
context: fork
agent: general-purpose
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the report in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit Doc — Documentation Quality Index (DQI)

> "Stale docs are worse than no docs." — Docs-as-Tests methodology

## Core Principles

1. **Evidence-based** — every finding needs a `file:line` reference
2. **Read the code** — verify docs match implementation. Stale docs are the #1 problem
3. **Diataxis-aware** — classify each doc by type (tutorial, how-to, reference, explanation) and check mode purity
4. **Language-specific** — apply each language's idiomatic doc conventions (see `reference.md` for language-specific rules)
5. **Public API first** — public items are priority. Private items are nice-to-have
6. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes

## Input

`$ARGUMENTS` is the target to audit (file path, directory, or empty for whole `src/`).

- If a specific file: audit that file deeply
- If a directory: audit all source files in it
- If empty: audit `src/` (or project root) broadly (sample 15-20 key files)

First, detect the primary language(s) from file extensions. Consult `reference.md` for language-specific conventions.

## 12-Dimension Framework

Score each dimension **0.0-1.0**, then compute a weighted DQI. Read `references/categories.md` for detailed check lists per category.

| # | Category | Weight | Key question |
|---|----------|--------|-------------|
| C1 | Diataxis Coverage | 10% | All 4 doc types present? Mode purity? |
| C2 | Completeness | 12% | Public API items documented? Coverage > 80%? |
| C3 | Freshness & Accuracy | 10% | Docs match current code? No stale references? |
| C4 | Readability & Prose Quality | 10% | No weasel words, condescension, passive voice? Register calibrated to the expected reader? |
| C5 | Structure & Findability | 8% | Heading hierarchy? Scannable? No orphan pages? |
| C6 | Standard Sections | 8% | Errors, params, returns, examples documented? |
| C7 | Code Examples | 10% | Working, copy-pasteable, no `unwrap()`? |
| C8 | Accessibility & Inclusivity | 6% | Alt text? Bias-free language? Global-ready? |
| C9 | Inline Comments Quality | 8% | WHY not WHAT? No stale TODOs? |
| C10 | Cross-references & Linking | 5% | Types linked? Related items connected? |
| C11 | Testing & CI | 8% | Doc-tests? Link checking? Prose linting? |
| C12 | Maintenance Process | 5% | Docs reviewed in PRs? Ownership clear? |

## Workflow

### Step 1 — Discover and sample

Glob source and doc files. For broad audit: sample public API modules, README, docs/ directory, and most-changed files.

### Step 2 — Detect language and conventions

Identify project language, then load `reference.md` for language-specific doc conventions (Rust: RFC 1574 + rustdoc, Python: PEP 257, JS/TS: JSDoc/TSDoc, Go: godoc).

### Step 3 — Score all 12 dimensions

Read `references/categories.md` for detailed checks. For each category: collect evidence, assign score 0.0-1.0, note specific `file:line` findings.

### Step 4 — Compute DQI and detect anti-patterns

Read `references/scoring.md` for the DQI formula, Doc Debt Score, maturity level mapping, named anti-patterns, and comparative benchmarks.

```
DQI = Σ(wᵢ × sᵢ) / Σ(wᵢ) × 10
```

### Step 5 — Generate report

Finding tier and confidence semantics are canonical in `../shared/triage.md` (Tier 3/2/1 + GRADE + triangulation). D-dimension findings carry tier and confidence so `cli-cycle` can aggregate without re-parsing.

## Output Format

```markdown
# Documentation Quality Audit — {project-name}

**Target**: [file/directory] | **Language**: [detected] | **Date**: [date]
**DQI Score**: X.X/10 — {verdict} | **Doc Debt**: X% ({color})
**Maturity Level**: {1-5} — {name}

## Scores by Category

| # | Category | Weight | Score | Weighted | Findings |
|---|----------|--------|-------|----------|----------|
| C1-C12 rows with 0.0-1.0 scores... |
| | **DQI** | **100%** | | **X.X/10** | |

## Anti-Patterns Detected
| Pattern | Severity | File:Line | Recommendation |

## Critical Violations (must fix)
### [Category]: [violation title]
- **File**: `path/to/file:123`
- **What**: [description]
- **Rule**: [which standard it violates]
- **Fix**: [concrete suggestion]

## Good Practices Found
[positive reinforcement]

## Recommended Next Steps
1. [highest-impact fix first]
```

## Boundary with cli-audit-sync

| cli-audit-doc | cli-audit-sync |
|--------------|---------------|
| Is the doc **well-written**? | Is the doc **accurate**? |
| Quality of prose, structure, coverage | Coherence between doc and code |
| "This doc comment is vague" | "This doc comment references a deleted function" |

Both complement each other. Run cli-audit-doc for quality, cli-audit-sync for accuracy.

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Doc anti-pattern "The Lie" (docs describe nonexistent features) | `/cli-audit-sync` | Verify doc-code coherence |
| Missing architecture explanation | `/cli-forge-doc` | Generate architecture docs |
| README score low | `/cli-forge-readme` | Rewrite README |
| Missing diagrams referenced in docs | `/cli-forge-schema` | Generate Mermaid diagrams |

**Rule:** Recommend, don't auto-execute.

## What this skill does NOT do

- **Does not fix docs** — it reports. Use `cli-forge-doc` to generate documentation
- **Does not check doc-code coherence** — use `cli-audit-sync` for that
- **Does not replace Vale/markdownlint** — it complements them with semantic analysis
- **Does not audit code quality** — use `cli-audit-code` for that

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-sync` | Checks doc **accuracy**. cli-audit-doc checks doc **quality** |
| `cli-audit-code` | Scores code quality. cli-audit-doc scores **doc quality** |
| `cli-forge-doc` | Generates docs. cli-audit-doc **audits** existing docs |
| `cli-cycle` | Calls cli-audit-doc as part of full project review; emit `.claude/cli-audit-doc.json` per `../shared/result-schema.md` for orchestrator aggregation |

## Reference Sources

- Procida — Diataxis framework | Bhatti et al. — *Docs for Developers* | Martraire — *Living Documentation*
- Google Dev Docs Style Guide | Microsoft Writing Style Guide | RFC 1574 (Rust)
- Vale linter (prose quality) | lychee (link checking) | markdownlint | Spectral (OpenAPI)
- Write the Docs Podcast | I'd Rather Be Writing (Tom Johnson) | Knowledgebase Ninja
