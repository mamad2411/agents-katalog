---
name: repo-to-notion-architect
description: >
  Run this skill whenever a user asks you to "map this repo to Notion", "design
  a Notion workspace for this project", "set up Notion for this codebase", or
  "figure out what should go in Notion vs the repo". Also trigger when the user
  says "I want to use Notion to track this project" and you are inside a local
  repository. Do NOT trigger on generic Notion questions unrelated to a local
  codebase. This skill produces a structured Notion workspace design grounded in
  shell-discovered repo topology, explicit classification heuristics, and a
  canonical-source decision matrix — never a naive folder mirror.
---

# Repo-to-Notion Architect

Analyze a local repository and produce a structured Notion workspace design.
Maps semantic roles (Project, Module, Service, Surface, Library, Infra, Shared,
Docs-source, Tooling) onto Notion databases, pages, relations, and views.
Does NOT mirror the filesystem 1:1 into Notion.

## Input Contract

### Required
- `REPO_ROOT` — absolute path to repository root (default: current working directory)
- `DOCS_DIR` — primary docs directory (default: `./docs`)

### Optional flags (ask user if ambiguous, otherwise use defaults)

| Flag | Default | Effect |
|------|---------|--------|
| `--extra-docs <path>` | none | additional docs directories |
| `--ignore <glob>` | `node_modules,.git,dist,build,.cache` | paths to skip |
| `--impl-plan` | off | include Section 6: Implementation Plan |
| `--metadata-file` | off | include Section 7: Metadata File Proposal |
| `--scale solo\|team` | `solo` | tune Notion complexity |
| `--design-only` | off | output design only, no Notion creation spec |

---

## Phase 1: Discovery

Run these exact commands in sequence. Capture all output before proceeding to
classification. Do not interpret yet — collect first.

### 1.1 Root structure
```bash
ls -1 "$REPO_ROOT"
```

### 1.2 Workspace config detection
```bash
for f in package.json pnpm-workspace.yaml turbo.json nx.json lerna.json \
          yarn.lock bun.lockb Cargo.toml go.work pyproject.toml; do
  [ -f "$REPO_ROOT/$f" ] && echo "FOUND: $f"
done
```

### 1.3 Git submodule detection
```bash
[ -f "$REPO_ROOT/.gitmodules" ] && cat "$REPO_ROOT/.gitmodules" || echo "NO_SUBMODULES"
```

### 1.4 Apps / packages / services enumeration
```bash
for dir in apps packages services libs modules; do
  [ -d "$REPO_ROOT/$dir" ] && echo "DIR: $dir" && ls -1 "$REPO_ROOT/$dir"
done
```

### 1.5 Infra / deployment signals
```bash
for sig in supabase infra terraform k8s docker .github/workflows; do
  [ -e "$REPO_ROOT/$sig" ] && echo "INFRA_SIGNAL: $sig"
done
```

### 1.6 Docs discovery
```bash
[ -d "$REPO_ROOT/docs" ] && find "$REPO_ROOT/docs" -maxdepth 2 -type f -name "*.md" | sort
[ -f "$REPO_ROOT/README.md" ] && head -5 "$REPO_ROOT/README.md"
```

### 1.7 Workspace member package.json (monorepo only)
If workspace config was found in 1.2, run:
```bash
find "$REPO_ROOT" -name "package.json" -not -path "*/node_modules/*" \
  -not -path "*/.git/*" | head -30
```
For each result, extract `name`, `version`, `private`, `scripts.dev`, `scripts.build`.

### 1.8 Deployed URL signals
```bash
grep -r "homepage\|VITE_APP_URL\|NEXT_PUBLIC_URL\|site_url\|BASE_URL" \
  "$REPO_ROOT" --include="*.json" --include="*.env*" --include="*.toml" \
  -l 2>/dev/null | head -10
```

---

## Phase 2: Classification

After collecting all discovery output, apply the decision table in
`references/classification-heuristics.md`. Do not invent new types.

### Classification types (exactly these, no others)
`Project` | `Module` | `Service` | `Surface` | `Library` | `Infra` |
`Shared` | `Docs-source` | `Tooling`

### Quick-reference decision table

| Observed signal | Classification |
|----------------|----------------|
| `pnpm-workspace.yaml` or `turbo.json` or `nx.json` at root | repo type = Monorepo |
| `.gitmodules` present | each submodule → evaluate individually |
| Has `apps/` + workspace config | each `apps/*` → evaluate individually |
| `package.json` with `version` + deployed URL signal + UI entrypoint | Surface |
| `package.json` with `version` + deployed URL signal + server entrypoint | Service |
| `supabase/` or `terraform/` or `k8s/` at root or in `infra/` | Infra |
| `packages/*` or `libs/*` with `"private": false` + `version` | Library |
| `packages/*` or `libs/*` imported by ≥2 other workspace members | Shared |
| `src/` at root + no workspace config + single `package.json` | Project |
| `scripts/` or `tools/` or `.github/` | Tooling |
| `docs/` with `adr/`, `plans/`, or `architecture.md` | Docs-source |
| Has own HTTP server entrypoint + deployment config | Service |
| Has UI entrypoint (`pages/`, `app/`, `index.html`) | Surface |

Read `references/classification-heuristics.md` for the full signal list,
tie-breaking rules, and per-topology classification workflows before
classifying any ambiguous component.

---

## Phase 3: Canonical-Source Decision

Apply this matrix to each classified component:

| Classification | Stays canonical in REPO | Canonical in NOTION |
|---------------|------------------------|---------------------|
| Project | code, configs, scripts | planning, status, milestones |
| Module | code, interfaces, tests | ownership, dependencies, status |
| Service | code, infra config, env schema | deployment status, incidents, runbooks |
| Surface | code, assets, feature flags | UX specs, design links, launch tracking |
| Library | code, types, changelog | API surface registry, consumers list |
| Infra | IaC code, migration files | environment registry, secrets inventory |
| Shared | code, types | consumer registry, version matrix |
| Docs-source | all `.md` files, ADRs, plans | index page, cross-links, status dashboard |
| Tooling | scripts, configs | nothing (keep in repo only) |

**Hard rule:** Notion is NEVER the primary edit surface for files that LLMs read
directly — CLAUDE.md, AGENTS.md, architecture.md, ADRs. Notion indexes them;
the repo owns them.

---

## Phase 4: Notion Architecture

### Default database model

```
Workspace Root
├── [DB] Projects          — one record per Project/Surface/Service component
├── [DB] Features          — one record per feature, linked to Projects
├── [DB] Tasks             — one record per task, linked to Features
├── [DB] Docs Index        — one record per significant doc file
├── [DB] ADRs              — one record per architecture decision record
├── [DB] Plans             — one record per implementation/rollout plan
└── [DB] Reviews           — one record per design/code/post-mortem review
```

Add for monorepos with >3 apps:
```
├── [DB] Modules Registry  — one record per workspace member with type + consumers
```

Add for repos with deployed services:
```
├── [DB] Environments      — staging, prod, preview entries per service
```

Read `references/notion-templates.md` for full property schemas, relation
directions, and recommended views per database.

**DB caps:** ≤ 7 databases for `--scale solo`, ≤ 12 for `--scale team`.

---

## Output Format

Produce sections in this exact order. Use these exact headers.

```
# Notion Architecture: [repo name or path]

## 1. Repo Analysis Summary

| Signal | Inferred value |
|--------|---------------|
| ...    | ...           |

**Inferred repo type:** [Normal | Monorepo | Monorepo+Submodules | Submodule-only | Mixed]

### Detected components
| Path | Inferred role | Key signals |
|------|--------------|-------------|

### Product boundaries
[1-3 bullets, or "Single product"]

---

## 2. Classification Model

| Path | Type | Signals observed | Reasoning |
|------|------|-----------------|-----------|

---

## 3. Canonical-Source Strategy

| Component | Stays in REPO | Moves to NOTION | Notes |
|-----------|--------------|----------------|-------|

---

## 4. Proposed Notion Architecture

### Databases
| DB name | Purpose | Key properties | Linked to |
|---------|---------|----------------|-----------|

### Page structure
[nested bullet list]

### Relations
| From DB | Relation | To DB | Direction |
|---------|----------|-------|-----------|

### Views to create per DB
| DB | View name | Type | Filter/Sort |
|----|-----------|------|-------------|

---

## 5. Mapping Table

| Repo path / concept | → | Notion object | Notes |
|---------------------|---|---------------|-------|

---

## 6. Implementation Plan
[ONLY if --impl-plan flag set]

### Phase 1: Foundation (Day 1)
[numbered steps]

### Phase 2: Seeding (Day 2-3)
[numbered steps]

### Phase 3: Relations and views (Day 4-5)
[numbered steps]

### Phase 4: Automation (optional)
[numbered steps]

---

## 7. Metadata File Proposal
[ONLY if --metadata-file flag set]

**Recommended filename:** `.project-tools.json`

[1-paragraph rationale]

[JSON code block with example schema]
```

---

## Phase 5: Anti-Pattern Checklist

Before finalizing output, verify each item. Fix any violation before outputting.

- [ ] No Notion DB maps 1:1 to a filesystem directory
- [ ] Every component has an explicit canonical-source decision
- [ ] No LLM-read files (CLAUDE.md, AGENTS.md, ADRs) are Notion-canonical
- [ ] Monorepo members have individual classification, not treated as one blob
- [ ] Git submodules are listed separately from monorepo workspace packages
- [ ] `src/` alone is NOT classified as a Module
- [ ] `scripts/` and `.github/` are classified as Tooling, not Module/Service
- [ ] `supabase/` is classified as Infra, not Service
- [ ] Implementation plan (if produced) starts with minimal viable setup, not full migration
- [ ] Metadata file (if produced) uses `.project-tools.json` filename
- [ ] Total databases: ≤ 7 for solo, ≤ 12 for team
- [ ] Section 6 and Section 7 omitted unless their respective flags were set

---

## Related Skills

- `get-api-docs` — fetch Notion API docs before automating workspace creation
- `lesson-decision-records` — record architectural decisions made during Notion setup
