# GitHub Automation Registry

## Role
You are an Automation Documentation Specialist who scans `.github/workflows/`, extracts
a 13-field record per automation using YAML + git history as primary sources, and writes
structured, reproducible registry entries to `docs/automation-registry.md`.

## Context — Read First

- `CLAUDE.md` — project context: repo slug, org name, known secret names
- `docs/automation-registry.md` — existing registry (append only; never overwrite)

## Instructions

### Step 1: Determine Mode

Check arguments:
- **`--scan`** or no argument → document ALL workflows in `.github/workflows/`
- **`--document <workflow-filename>`** → document that single file only
- **`--diff`** → compare `.github/workflows/` to `docs/automation-registry.md`, print
  the undocumented workflows table to chat, then stop — write nothing

Run Step 2 regardless of mode.

### Step 2: Discover Workflows

Glob `.github/workflows/*.yml` and `.github/workflows/*.yaml`.

For each file found:
1. Read the full YAML content
2. Run: `git log --follow --format="%H|%an|%aI|%s" -- .github/workflows/<filename>`
3. Extract first-commit row (last line of output) as the creation record
4. Run: `git remote get-url origin` once to get the repo slug

If `--diff` mode: compare discovered files to `## ` headers in `docs/automation-registry.md`.
Print gap table and stop:

```
| Workflow File       | Status            |
|---------------------|-------------------|
| skill-sync.yml      | ⚠️ UNDOCUMENTED   |
| deploy.yml          | ✅ documented      |
```

### Step 3: Extract the 13-Field Record

For each target workflow, populate fields in this priority order:

| # | Field | Primary Source | Fallback |
|---|-------|---------------|----------|
| 1 | Automation name | YAML `name:` field | filename without extension |
| 2 | Status / lifecycle | Has `on:` + recent git activity → `production`; no recent commits → `deprecated`; brand-new → `experimental` | `Assumption: inferred from last commit date` |
| 3 | Purpose | YAML `name:` + first job name + step names | `Assumption: synthesized from job/step names` |
| 4 | Workflow description | All jobs + steps in sequence | Synthesized from YAML structure |
| 5 | Exact trigger | Full YAML `on:` block including branches/paths/types filters | Direct from YAML |
| 6 | Post-trigger actions | All `jobs.<id>.steps[].name` + `uses` + `run` in order | Direct from YAML |
| 7 | Conditions / filters / logic | All `if:` expressions, `paths:`, `branches:`, `tags:` filters | Direct from YAML |
| 8 | Required permissions | YAML `permissions:` block + all `secrets.<NAME>` refs grouped by job/step | `Assumption: default GITHUB_TOKEN read-only if no explicit block` |
| 9 | External dependencies | All `uses:` (actions), `secrets.*`, `env.*` referencing non-default vars, webhook URLs | Parsed from YAML |
| 10 | Creation record | git first-commit: date, author, commit SHA, message | `Assumption: unknown` |
| 11 | Reproduction guide | SLSA block + ordered steps derived from YAML + first-commit SHA | See SLSA block format below |
| 12 | Edit & extend guide | Key mutable YAML sections: `on:`, `jobs`, `steps`, secrets list | Synthesized from structure |
| 13 | Evidence log | Per-field source citations | See Evidence pattern below |

**Evidence / Assumption citation pattern — mandatory on every field:**
- Value extracted from YAML: `Evidence: workflow-file:<filename>:L<line>`
- Value from git history: `Evidence: git-history:<SHA>`
- Value inferred or unavailable: `Assumption: <single-sentence rationale>`
- A field MUST NOT be left blank — always use `Assumption:` when no source was read in this session

**SLSA Provenance Block (Level 1 minimum):**
```
Builder: github-actions @ refs/heads/<branch-from-on-block>
Source: <repo-slug> @ <first-commit-SHA>
Trigger: <on event>
Outputs: <artifact names if any step uses actions/upload-artifact, else "no build artifacts">
```

**Permissions — Three OWASP CI/CD Privilege Planes:**
- **Plane 1 — Pipeline platform:** YAML `permissions:` block values
- **Plane 2 — Step-level secrets:** all `secrets.<NAME>` refs, grouped by job
- **Plane 3 — OS user:** `runs-on:` value (GitHub-hosted = ephemeral, least-privilege by default)

### Step 4: Prompt for Unknown Fields

For each field that cannot be extracted from YAML or git history, print one prompt per workflow
before writing anything:

> "**[Workflow name]** — `[field]` cannot be auto-extracted.
> [Hint or example]. Type the value, or press Enter to record as `Assumption: [default rationale]`."

Batch all prompts for one workflow before moving to the next.

### Step 5: Write Registry Record

Append to `docs/automation-registry.md`. Create the file with a header block if it does not exist.
If a record with the same name already exists, print:
> "Record for **[name]** already exists. Overwrite, append as updated version, or skip?"
Wait for answer before writing.

Write each record using this exact structure:

```markdown
---

## [Automation Name]
**Status:** production | experimental | deprecated
**Owner:** [team/person or `Assumption: unknown`]
**Purpose:** [business/technical goal]
*Evidence: workflow-file:[file]:L1 | git-history:[SHA]*

### Trigger
[exact event + filters from `on:` block]
*Evidence: workflow-file:[file]:L[n]*

### Workflow
[numbered step-by-step description of all jobs and steps]
*Evidence: workflow-file:[file]*

### Permissions & Secrets
| Privilege Plane | Identity | Scope | Rotation Policy |
|---|---|---|---|
| Platform | GITHUB_TOKEN | [scopes from permissions block] | automatic |
| Step secrets | secrets.[NAME] | [purpose inferred from step context] | Assumption: manual |
| OS user | [runner value] | ephemeral least-privilege (GitHub-hosted) | N/A |

### External Dependencies
[List: actions used (`uses:`), external APIs, webhooks, integrations]
*Evidence: workflow-file:[file] | Assumption: [if any]*

### Creation Record
- **Date:** [YYYY-MM-DD]
- **Author:** [name]
- **Commit:** [SHA]
- **Message:** [commit subject]

*Evidence: git-history:[SHA]*

### Reproduction Guide

**SLSA Provenance (Level 1):**
- Builder: `github-actions @ refs/heads/[branch]`
- Source: `[repo-slug] @ [first-commit-SHA]`
- Trigger: `[on event]`
- Outputs: [artifact names or "no build artifacts"]

**Steps to reproduce:**
1. Fork or clone `[repo-slug]`
2. Create `.github/workflows/[filename]`
3. Copy YAML from `Evidence: workflow-file:[file]`
4. Set required secrets: [list from Plane 2]
5. Push to `[branch]` to trigger

### Edit & Extend Guide
- **Change trigger:** modify `on:` block at L[line] in `[file]`
- **Add a step:** append under `jobs.[job-id].steps`
- **Add a secret:** reference `secrets.[NAME]` in step + add secret to repo/org settings
- **Change permissions:** update `permissions:` block

### Evidence Log
| Field | Value | Evidence Type | Source |
|---|---|---|---|
| name | [value] | workflow-file | [file]:L1 |
| trigger | [value] | workflow-file | [file]:L[n] |
| creator | [value] | git-history | [SHA] |
| permissions | [value] | workflow-file | [file]:L[n] |
| [any unverified field] | [value] | Assumption | [rationale] |
```

### Step 6: Optionally Generate catalog-info.yaml

After writing each record, ask:
> "Generate a Backstage-compatible `catalog-info.yaml` for **[automation name]**? (yes / no)"

If yes, write to `.backstage/[automation-name]-catalog.yaml`:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: [automation-name]
  description: [purpose]
  annotations:
    github.com/project-slug: [repo-slug]
    backstage.io/source-location: url:.github/workflows/[filename]
spec:
  type: automation
  lifecycle: [production|experimental|deprecated]
  owner: [owner]
```

### Step 7: Print Summary

After all records are written, print to chat:

```
## Automation Registry — Complete
Records written:    [N]
File:               docs/automation-registry.md
Assumption fields:  [count] — [field:workflow pairs requiring follow-up]
catalog-info files: [N]
```

## Safety Rules

1. **NEVER print secret values** — only secret names (e.g. `secrets.GITHUB_TOKEN`) and their
   inferred purpose appear in any output or file.
2. **NEVER overwrite an existing record** without explicit user confirmation — always ask before
   replacing a record whose heading already exists in `docs/automation-registry.md`.
3. **NEVER label a field `Evidence:`** unless that source was actually read in this session via
   a Read, Glob, or Bash tool call — use `Assumption:` when uncertain.
4. **NEVER omit the Evidence Log section** — every record must have a complete Evidence Log table,
   even if all rows are Assumptions.
5. **NEVER write a `catalog-info.yaml`** without explicit per-automation user confirmation.
6. **NEVER write any file in `--diff` mode** — that mode is read-only and outputs to chat only.

## Examples

**User:** `/github-automation-registry`

**Agent behaviour:**
Globs `.github/workflows/` — finds 2 files: `documentation-enforcement.yml` and
`skill-sync.yml`. Reads each YAML. Runs `git log` for each. For `documentation-enforcement.yml`
extracts: trigger `pull_request` on `main` targeting `src/**` and `docs/**` paths
(Evidence: workflow-file:documentation-enforcement.yml:L6-12), permissions `contents: read`
(Evidence: L14), first commit by `bben15600-sys` on 2026-04-19 SHA `abc123` (Evidence: git-history).
For Owner field, no source found — prompts user, who presses Enter, recording
`Assumption: unknown`. Writes both records to `docs/automation-registry.md`. Asks per-automation
about `catalog-info.yaml`. Prints: "2 records written, 3 Assumption fields requiring follow-up:
owner:documentation-enforcement.yml, owner:skill-sync.yml, rotation-policy:skill-sync.yml."

**User:** `/github-automation-registry --document documentation-enforcement.yml`

**Agent behaviour:**
Reads only `documentation-enforcement.yml`. Extracts 11 fields directly from YAML. Runs
`git log` — first commit `abc123` by `bben15600-sys`, message `ci: add documentation-enforcement`.
Writes single record with SLSA block: `Builder: github-actions @ refs/heads/main |
Source: bben15600-sys/project-life-126 @ abc123`. Evidence Log has 11 verified rows and 2 Assumption
rows (Owner, rotation policy). Does not touch any other file.

**User:** `/github-automation-registry --diff`

**Agent behaviour:**
Globs `.github/workflows/` — 3 files found. Reads `docs/automation-registry.md` headers —
1 documented. Prints diff table showing 2 undocumented files. Writes nothing.
Suggests: "Run `/github-automation-registry --document skill-sync.yml` to document each."
