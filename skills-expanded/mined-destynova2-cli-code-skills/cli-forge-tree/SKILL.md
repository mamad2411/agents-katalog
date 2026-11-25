---
name: cli-forge-tree
metadata:
  author: clement
description: "Use this skill whenever the user wants to visualize, generate, audit, or scaffold a project directory structure. Triggers include: 'project structure', 'folder structure', 'directory layout', 'tree', 'arborescence', 'scaffold', 'init project', 'organize my files', 'naming conventions', or any request to understand or create how files and folders should be organized in a codebase. Also triggers when someone says 'create a new project', 'bootstrap', 'init', or asks 'where should I put this file'. Use for any language or framework. Do NOT use for file system operations unrelated to project organization (like disk cleanup or backup scripts)."
argument-hint: "[project-path]"
context: fork
agent: general-purpose
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Project Tree — Structure & Scaffold

Visualize, audit, or scaffold project directory structures with **human-readable naming** that any skill level can navigate.

## Core Principles

- **Read `../gotchas.md`** before producing output to avoid known pitfalls.

## Core Conventions (Summary)

Read `references/conventions.md` for detailed naming rules, depth guidelines, and cross-cutting folders.

| Rule | Example |
|------|---------|
| **lowercase-kebab-case** for folders & files | `api-gateway/`, `user-service.ts` |
| **UPPER_CASE** only for root meta-files | `README.md`, `LICENSE` |
| **dot-prefix** for config/hidden files | `.env`, `.gitignore` |
| **Max 3 levels** before needing justification | `src/api/handlers/` ok, deeper = rethink |
| **Descriptive, short, no redundancy** | `docs/` not `documentation-files/` |
| **Plural for collections** | `tests/`, `scripts/` |

**Exceptions:** Follow ecosystem conventions when universal (`Cargo.toml`, `package.json`, `__init__.py`, `lib.rs`).

## Workflow

### Step 1 — Detect or Ask

**If a project exists** — read the root directory and detect archetype:

| Signal | Archetype |
|--------|----------|
| `Cargo.toml` | `rust` |
| `go.mod` | `go` |
| `package.json` | `js/ts` |
| `pyproject.toml` / `setup.py` | `python` |
| `*.tf` | `terraform` |
| `Chart.yaml` / `helmfile.yaml` | `helm` |
| `kustomization.yaml` | `kustomize` (check for `flux-system/` → `flux`) |
| `Containerfile` / `Dockerfile` | `oci-container` |
| `*.container` / `*.kube` | `podman-quadlet` |
| `site.yml` / `playbooks/` / `roles/` | `ansible` |
| `docker-compose*.yml` | `docker-compose` |
| `*.sh` + no other code | `shell-scripts` |
| `flake.nix` | `nix` |
| Multiple of the above | `monorepo` |

Then: display the current tree (annotated), highlight issues, suggest improvements.

**If no project or empty directory** — use `ask_user_input` QCM:
- Q1: "What are you building?" (Library, CLI, API, Infra, Full-stack, Monorepo, Other)
- Q2: "Primary language/stack?"
- Q3: "Extras to include?" (Docker, CI/CD, Docs, Nix, Benchmarks, Examples)

### Step 2 — Generate or Audit

**Generate mode** (new project): Read `references/archetypes.md` for the full template matching the detected archetype. Scaffold using `mkdir -p` and touch for placeholder files.

**Audit mode** (existing project): display annotated tree, then list naming violations, missing standard files, suggested reorganization.

### Step 3 — Display

Always show the tree in annotated format:

```
project-name/
├── src/                    # Source code
│   ├── lib.rs              # Library entry point
│   └── handlers/           # Request handlers
├── tests/                  # Integration tests
├── docs/                   # Documentation
├── Cargo.toml              # Manifest & deps
├── README.md               # Project landing page
└── .gitignore              # Git exclusions
```

**Annotation rules:**
- Every folder gets a `# comment` — 3-6 words max
- Files only get comments if their role isn't obvious from the name
- Use the exact `├──` / `└──` / `│` box-drawing characters
- Max 2 levels shown by default. Deeper = collapsed with `...`

## Quality Scoring — Structure Health Score (SHS)

### SHS Formula

```
SHS = Σ(wᵢ × sᵢ) / Σ(wᵢ) × 10
```

### Checklist Items

| # | Item | Weight | What to check |
|---|------|--------|---------------|
| 1 | Naming consistency | 5 | All folders follow same convention |
| 2 | Depth control | 4 | No folder deeper than 4 levels without justification |
| 3 | Standard files present | 4 | README, LICENSE, .gitignore exist at root |
| 4 | Archetype fit | 3 | Structure matches detected language/framework conventions |
| 5 | Separation of concerns | 4 | Source, tests, docs, config in distinct locations |
| 6 | No orphan files | 3 | No loose files in wrong directories |
| 7 | Entry point clarity | 3 | Main/index file is obvious |
| 8 | Test colocation | 2 | Tests near or mirroring source structure |

**Scoring:** 0.0 = absent/violated, 0.25 = poor, 0.5 = inconsistent, 0.75 = good, 1.0 = excellent

**Thresholds:** 8+ clean, 6-8 minor issues, 4-6 needs reorganization, <4 structural problems

Output the SHS table at the end of the tree analysis.

## Output

- **Visualize**: always show the annotated tree in conversation
- **Scaffold**: create directories and placeholder files on the filesystem
- **Audit**: list issues + suggested fixes, then show the "ideal" tree side-by-side
- If the `readme` skill is also being used, feed the annotated tree into Tier 3 "Project Structure"

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Files in wrong directories | `/cli-audit-sync` | Check if docs reference old paths |
| No CONTRIBUTING.md found | `/cli-forge-doc` | Generate contributing guide |
| Deep nesting detected | `/cli-audit-tangle` | Check if structure reflects code coupling |

**Rule:** Recommend, don't auto-execute.

## Integration with other cli-* skills

| Skill | Relation |
|-------|----------|
| `/cli-forge-readme` | Feed the "Project Structure" section of the README |
| `/cli-forge-doc` | Reference structure for generating the docs |
| `/cli-audit-tangle` | Compare the physical structure against the logical couplings |
| `/cli-audit-code` | Verify naming conventions aligned with the structure |
| `/cli-forge-chef` | Assign worktrees based on the structure |
| `/cli-cycle` | Included in the cycle's structural audit |
