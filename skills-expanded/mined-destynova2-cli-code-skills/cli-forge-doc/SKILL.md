---
name: cli-forge-doc
metadata:
  author: clement
description: Generate and audit comprehensive project documentation from a Git repository. Produces standard documentation (CONTRIBUTING.md, architecture, troubleshooting) in Diataxis structure with zero AI markers by default. Use this skill whenever someone asks to document a project, generate docs, create a README, write API docs, or improve existing documentation. Also trigger when someone mentions "doc", "documentation", "readme", "explain this codebase", "onboard developers", or "make this project understandable".
argument-hint: "[git-repo-path]"
context: fork
agent: general-purpose
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the documentation in that language. If the project is bilingual, ask the user which language to use before proceeding.

> **Diacritics rule:** When the chosen output language uses diacritics (French, Spanish, Portuguese, etc.), render them correctly — including on capitals (É, À, Ç, Ô…). Never strip accents to ASCII: write "sécurité" not "securite", "Rôle" not "Role". ASCII-flattened French is a defect, not a style.

> **Writing style:** Favor clarity — short sentences, one idea per sentence, plain words. A metaphor only when it clarifies. Keep one consistent register (impersonal/infinitive for operational docs). Separate narrative prose, meant to make the reader understand, from telegraphic content (tables, commands, checklists) which stays terse for action.

> **Reader calibration (the Singh rule):** Before writing, name the expected reader and their situation (operator mid-incident, dev at setup, curious newcomer). Match their level — vulgarization means calibrating to the reader, not adding literary polish. For a general audience (Simon Singh's method): a concrete story motivates each concept, one strong analogy per hard idea, worked examples the reader can redo, hard details moved to an appendix. For practitioners (runbooks, how-tos, dev guides) the right level is the opposite of literary: command or fact first, the why in one short line after, imperative mood, no em-dash asides, no narrative voice, no scene-setting intro. If a sentence would read well in a magazine, it is miscalibrated for a runbook.

> **Reference grammar (the Stripe rule):** For reference and operational docs, borrow the mechanics of a great API reference (Stripe's): identical skeleton for every repeated unit (the reader learns the map once), concrete example or command before the abstract dictionary, fixed sentence templates reused throughout (success and failure always both stated — "Returns X…. Raises an error if…"), one verb per operation with zero synonym drift, and typed/badged entries for every parameter (type, default, required/optional). Every stated failure names the next action; a KO without a pointer is a dead end.

> **Deep links & render gate:** Every cross-reference is a clickable link to a validated anchor (dual renderers disagree on anchor slugs by default — align GitLab and pandoc with `+gfm_auto_identifiers`), and the reference graph is checked: a section the reader must reach (a procedure, a fix) with zero inbound links is unreachable in practice. For docs shipped as PDF or site, the render is the doc's runtime: make the render job blocking, failing on broken anchors and layout overflow (zero `Overfull \hbox`).

> **No fabricated output:** Never invent command output, console captures, API responses, metrics, or logs. When real output is needed, emit a clearly-marked placeholder (🚧 "replace with a real capture"), never plausible-but-fake text presented as real.

# Doc Forge — Dual Documentation Generator & Auditor

Generate production-grade documentation for any Git project, optimized for both AI agents and human readers.

## Philosophy

Four principles stolen from the best, plus one operational rule:

1. **OpenBSD doctrine**: "Developers making a change to the system are expected to update the man pages along with their change." Docs ship with code. Man pages are authoritative. If it's not documented, it doesn't exist.
2. **Diátaxis framework**: Documentation has four modes — tutorials, how-to guides, reference, explanation. Never mix them.
3. **One doc, two readers**: Good documentation serves both humans and AI agents. Standard files (architecture.md, CONTRIBUTING.md, TROUBLESHOOTING.md) are naturally consumable by both — no special AI format needed.
4. **Single source of truth (the spliceosome principle)**: each fact has exactly one canonical home. Other documents that need to mention the fact must link to it, transclude from it, or be generated from it — never duplicate it by hand. A eukaryotic gene is transcribed once and the spliceosome cuts the relevant exons for each context; documentation should work the same way. One source, many splicings (README, CONTRIBUTING, --help, slide deck), zero hand-maintained copies. Duplicated Truth is the #1 cause of doc rot — every parallel copy drifts.
5. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes

## Input

`$ARGUMENTS` is the path to the Git repository (or current directory if empty).

If no argument: look for a Git repo in the current working directory.

## Step 0: Reconnaissance

Before writing a single line of doc, **read the project**. This is non-negotiable.

```
1. List the root directory
2. Read: README.md, CONTRIBUTING.md, Cargo.toml, package.json, pyproject.toml, go.mod, Makefile, Dockerfile, docker-compose.yml, .gitlab-ci.yml, .github/workflows/*, justfile
3. Identify: primary language(s), build system, CI/CD, test framework, deployment method
4. Sample 10-15 key source files (entry points, public API, core modules)
5. Read: docs/ directory if it exists
6. Check: git log --oneline -20 for recent activity focus
7. Check: git remote -v for repo URL
```

Build a mental model of:
- **What** the project does (purpose, problem it solves)
- **How** it's structured (architecture, key abstractions)
- **Who** uses it (library consumers, CLI users, operators, contributors)
- **Where** it runs (local, cloud, air-gapped, container)

## Step 1: Completeness Scan (The Checklist)

Before generating, score what exists. Use the **Documentation Completeness Index (DCI)**.

### DCI Formula

```
DCI = Σ(wᵢ × sᵢ) / Σ(wᵢ) × 10

Where:
  wᵢ = weight of item i (importance)
  sᵢ = score of item i (0.0 to 1.0)
```

### Checklist Items (with weights)

| # | Item | Weight | What to check |
|---|------|--------|---------------|
| 1 | Project overview (README or equivalent) | 5 | Exists, has purpose statement, not just boilerplate |
| 2 | Getting started / quickstart | 5 | Can a new dev go from clone to running in <10 min? |
| 3 | Architecture overview | 4 | High-level structure documented somewhere |
| 4 | API reference (public surface) | 5 | Doc comments on public items, generated docs |
| 5 | Configuration reference | 3 | All config options documented with defaults |
| 6 | Error handling guide | 3 | Error types, what they mean, how to fix |
| 7 | Deployment / operations guide | 3 | How to deploy, monitor, troubleshoot |
| 8 | Contributing guide | 2 | How to contribute, code style, PR process |
| 9 | Changelog / release notes | 2 | History of changes |
| 10 | License | 1 | Exists and is clear |
| 11 | CI/CD documentation | 2 | Pipeline stages, environments, secrets needed |
| 12 | Security documentation | 3 | Threat model, auth flows, secrets management |
| 13 | Troubleshooting / gotchas guide | 3 | Known issues, workarounds, common mistakes documented |
| 14 | Examples / tutorials | 4 | Working, tested, progressive complexity |
| 15 | Inline doc coverage (public API) | 4 | % of public items with doc comments |
| 16 | Cross-references & linking | 2 | Types linked, related items connected |

**Scoring guide**: 0.0 = absent, 0.25 = stub/placeholder, 0.5 = exists but incomplete, 0.75 = good but gaps, 1.0 = excellent.

Output the DCI score table and overall score before proceeding.

### Gap Analysis (ISO 13485 pattern)

Beyond raw scoring, run a **compliance gap analysis** based on project type:

| Project type | Required docs (gap analysis target) |
|--------------|-------------------------------------|
| Library | README, CHANGELOG, LICENSE, API_REFERENCE, CONTRIBUTING, SECURITY |
| CLI tool | README, --help, man page or equivalent, CHANGELOG, LICENSE, examples |
| Service | README, ARCHITECTURE, DEPLOYMENT, OPERATIONS, SECURITY, MONITORING, RUNBOOK |
| Infrastructure | README, ARCHITECTURE, NORMS_DEVIATIONS, OPERATIONS, TROUBLESHOOTING, CIS_AUDIT (if applicable) |

**Output:**
```
Gap Analysis — {project-type}
Compliance: 7/10 required docs present (70%)

Missing (prioritized by impact):
  1. SECURITY.md (high — required for production)
  2. RUNBOOK.md (medium — required for on-call)
  3. CHANGELOG.md (low — semantic-release may auto-generate)
```

## Step 2: Generate Project Documentation (Machine + Human Layer)

All project knowledge is distributed into **standard documentation files**. No AI-specific markers are generated by default.

**OPSEC rationale:** Files named `AGENTS.md`, `CLAUDE.md`, or `llms.txt` score DREAD 8.8/10 — they expose full architecture, credential patterns, and gotchas in files explicitly labeled for AI consumption. During a security audit (CIS, SOC 2, PCI-DSS, ISO 27001, defense contracts), these files signal AI involvement in development, raising accountability and supply chain concerns. Standard documentation files carry the same content with zero signal.

### Self-contained operations pack mode

When the requested documentation is an **operations/exploitation pack** (signals:
`exploitation`, `operations`, `runbook`, `N1/N2/N3`, `support tiers`,
`PDF`, `DOCX`, `export`, `livrable documentaire`), generate a
self-contained dossier rather than a link-only index.

Rules for this mode:

- The directory itself must be usable offline by an operator and suitable as
  input to an external PDF/DOCX export tool. Do not add repository export
  scripts, Make targets, Pandoc wrappers, or generated PDF/DOCX artifacts unless
  the user explicitly asks for export automation.
- External project docs may remain engineering sources of truth, but the
  operations dossier must contain the minimum operational facts needed to act:
  scope, roles, severity, triage, commands, escalation, rollback, closure,
  request/change flow, known errors, and continual improvement.
- Prefer **bounded operational duplication** over link-only pages. If a fact is
  needed for N1/N2/N3 to act, include the usable version directly in the pack.
  Do not put external source/provenance paths in operator-facing pages by
  default; they make the pack look dependent on files outside the dossier.
- Every page must start with `Role:`, `Quand utiliser cette page:`, and `Sortie
  attendue:` (or project-language equivalents). `Role:` must describe the
  page's operational function in the dossier, such as `INDEX N1`, `PROCEDURE N2
  ROLLBACK`, `KEDB N2`, or `RACI EXPLOITATION`; do not use abstract
  doc-maintenance roles like `CANON`, `MAP`, or `NEW` for operations packs.
  `Sortie attendue:` must be an actionable operational output, not "open the
  canonical source".
- Do not create link-only pages. Each file in the directory must contain enough
  operational content to be usable on its own within its support level. Keep
  maintenance provenance outside operator-facing pages unless explicitly asked.
- Avoid unexplained engineering shorthand in operator-facing pages. Replace test
  tier codes like `T0/T2/T3/T4` with plain operational labels such as `local
  quick test`, `integration test`, `target/VM test`, or `release gate` unless
  the pack defines the shorthand locally.
- Do not impose a repository-local incident storage convention (for example
  `.artifacts/incident-*`, `status.txt`, `logs.txt`) when writing N1/N2/N3
  procedures. Operators usually already have ITSM, monitoring, on-call, or
  evidence tools. Specify the required information to capture and transmit,
  not the storage tool or file layout, unless the user explicitly asks for a
  project-local evidence convention.
- Do not create a monolithic `LIVRET.md` by default. The directory is the
  deliverable: `README.md` is the entry point, and each module/procedure file is
  part of the self-contained pack. Create a linear printable synthesis only if
  the user explicitly asks for one. Keep export mechanics outside the project
  unless explicitly requested.

### Content redistribution map

All project context is placed in standard files. An AI agent reads these files naturally — no special format needed.

| Content | Standard destination |
|---------|---------------------|
| Stack, Architecture | `docs/explanation/architecture.md` |
| Domain Concepts | `docs/explanation/glossary.md` or `docs/reference/glossary.md` |
| Key Patterns, Conventions | `docs/explanation/architecture.md` (section "Conventions") |
| Commands | `README.md` (section "Usage" or "Commands") |
| Gotchas, known issues | `docs/TROUBLESHOOTING.md` |
| Commit rules, git workflow | `CONTRIBUTING.md` |
| CI/CD validation | `docs/reference/ci-cd.md` |

**Rules:**
- Describe capabilities, not file paths (paths change, capabilities don't)
- Domain concepts are stable — document them. File structure is volatile — don't
- Include package manager explicitly if non-default
- Never dump style guides — let the linter do the linter's job
- Use progressive disclosure: point to `docs/` for details, don't inline everything
- **Each fact has exactly one home (SSOT, the spliceosome rule):** if two generated files would describe the same configuration option, port number, version, install command, or architectural component, one must link to the other instead of restating it. When in doubt, the canonical home is the file most likely to be read first by the relevant audience (README for users, CONTRIBUTING for contributors, ARCHITECTURE for designers). Never generate Duplicated Truth — every parallel copy is a future drift.

### Cleanup of existing AI markers

If any AI-specific files exist in the project, absorb their content and delete them:

| File | Tool | Absorb into |
|------|------|-------------|
| `CLAUDE.md` | Claude Code | `CONTRIBUTING.md` |
| `GEMINI.md` | Gemini CLI | `CONTRIBUTING.md` |
| `AGENTS.md` | Codex/multi-tool | `docs/explanation/architecture.md` |
| `llms.txt`, `llms-full.txt` | Generic | `docs/index.md` |
| `.cursorrules`, `.cursor/rules/*.mdc` | Cursor | `CONTRIBUTING.md` (coding conventions) |
| `.windsurfrules`, `.windsurf/rules/*.md` | Windsurf | `CONTRIBUTING.md` |
| `.github/copilot-instructions.md` | Copilot | `CONTRIBUTING.md` |
| `.aider.conf.yml` | Aider | Discard (tool config, not project knowledge) |

After absorption:
1. **Delete** all AI marker files listed above
2. **Add** AI tool config dirs to `.gitignore` (`.cursor/`, `.windsurf/`, `.aider*`, `.claude/`, `.continue/`, `.junie/`)
3. **Warn** the user about AI trailers in git history — delegate to `cli-git-conventional --audit-markers` for cleanup options

### Opt-in: AI marker files (`--ai-markers` flag)

When explicitly requested with `--ai-markers`, additionally generate:

- `AGENTS.md` — flat LLM context file (< 300 lines) with Stack, Architecture, Domain Concepts, Key Patterns, Commands, Gotchas
- `llms.txt` — documentation index following llmstxt.org standard
- `llms-full.txt` — (optional, small projects) single concatenated file with all doc content inline

These files **duplicate** content already in the standard docs. They exist only for convenience when OPSEC is not a concern.

## Step 3: Generate Human Documentation (Diátaxis Layer)

This layer serves humans — from newcomers to experts. Follow the **Diátaxis framework** strictly: tutorials, how-to guides, reference, explanation. Never mix modes.

Read `references/diataxis.md` for the full directory structure, writing rules per quadrant, design doc template, and progressive complexity funnel.

## Step 4: Audit (Score the Result)

After generation, run the doc-audit framework on the result. See `reference.md` for the full audit methodology.

### Quick Audit Checklist

This checklist + the Doc Debt threshold form this skill's post-verification gate before publishing; the 3-phase definition-of-done structure (pre → during → post) is canonical in `../shared/done-gate.md`.

For each generated file, verify:

1. **Accuracy**: Does the doc match the actual code? (Read the implementation.)
2. **Completeness**: Are all public items covered?
3. **Freshness**: Does it reference current APIs, not stale ones?
4. **Examples**: Do examples compile/run? Do they use `?` not `unwrap()`?
5. **Cross-refs**: Are types and functions linked, not just named?
6. **Progressive**: Can a newcomer navigate from zero to competent?

### Documentation Debt Score

```
Doc Debt = (Public Items − Documented Items) / Public Items × 100

Thresholds:
  0-10%  → Green  (healthy)
  10-25% → Yellow (needs attention)
  25-50% → Orange (significant debt)
  50%+   → Red    (documentation emergency)
```

## Step 5: Output

### Files to Generate

At minimum, produce:
1. `CONTRIBUTING.md` — Commit rules, git workflow, PR process
2. `docs/explanation/architecture.md` — Full architecture, domain concepts, conventions
3. `docs/TROUBLESHOOTING.md` — Gotchas, known issues, workarounds
4. `docs/index.md` — Human landing page
5. `docs/tutorials/getting-started.md` — First-contact tutorial
6. `docs/reviews/DCI-REPORT.md` — Documentation completeness index with scores and recommendations

If the project warrants it (public API, library, complex system), also produce:
- Full Diátaxis docs/ tree
- Updated inline doc comments (as a diff or suggestions)
- `docs/design/000-template.md` — Design doc template for the team to reuse
- Design docs for major existing architectural decisions (if none exist yet)

### Presentation

Present the DCI score first, then the generated files. Summarize:
- Current state (DCI score)
- What was generated
- Top 3 highest-impact improvements still needed
- Recommended next steps (ordered by effort vs impact)

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Project has shell scripts undocumented | `/cli-audit-shell` | Assess script quality for doc accuracy |
| Architecture section reveals coupling concerns | `/cli-audit-tangle` | Topology audit |
| README needs rewrite | `/cli-forge-readme` | Focused README generation |

**Rule:** Recommend, don't auto-execute.

## Adaptation Rules

1. **Scale to project size**: A 200-line CLI script needs a good README, not a docs site. A platform with 50K LOC needs the full Diátaxis treatment.
2. **Match the language**: Follow the language's idiomatic doc conventions (see `reference.md`).
3. **Respect existing docs**: Don't overwrite good existing docs. Augment and cross-reference.
4. **Monorepo support**: If the project has multiple packages/services, generate per-package docs + a root-level overview.
5. **Air-gapped aware**: If the project targets air-gapped environments, emphasize offline-complete documentation. No external links that won't resolve.
6. **Confidence markers**: If you're unsure about something (inferred from code but not confirmed), mark it with `<!-- NEEDS-REVIEW: [reason] -->` rather than guessing.
