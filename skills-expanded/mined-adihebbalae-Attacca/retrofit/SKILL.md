---
name: retrofit
description: "Retrofit an existing project with Attacca. Audit project structure, generate CONTEXT.md from what you find, merge settings safely, suggest plugins. Never touches source code or existing deployments."
---

<!-- Delete when: native Claude Code project metadata extraction from existing repos is available -->

# Retrofit Skill

Integrate Attacca into an existing codebase. Audits the project, generates CONTEXT.md, merges settings safely, and suggests plugins.

## When to Use
- User runs `/retrofit` on an existing codebase
- Project already has source code but no Attacca scaffolding
- User wants to add agent workflow and documentation to an existing project

---

## Phase 1: Audit the Existing Project

Read the workspace and answer:

**Project basics**:
- Name (from `package.json` / `pyproject.toml` / `go.mod` / `Gemfile` / `Cargo.toml`)
- Language/stack (Node+React, Python+Django, Go, Rails, Rust, etc.)
- Age (first commit)
- Last active (most recent commit date)

**File structure** — scan and document:
```
project-root/
  src/ or app/ or lib/     ← source code
  tests/ or __tests__/     ← tests
  node_modules / venv      ← dependencies
  package.json / pyproject.toml ← manifest
  .github/workflows/       ← CI/CD
  docker-compose.yml       ← deployment
```

**Build & test commands** — verify what works:
```bash
npm run build   # or: python -m build, go build
npm test        # or: pytest, go test
npm run lint    # or: ruff check, golangci-lint
```

Document what works and what fails.

**Deployment pipeline**:
- CI system (GitHub Actions, GitLab CI, Jenkins)
- Deployment target (Vercel, Heroku, Lambda, Docker)
- Secrets strategy (GitHub Secrets, .env, Vault)
- Main branch: auto-deploy or manual?

**Existing code quality practices**:
- Pre-commit hooks?
- PR review standards?
- Branch protection rules?
- Testing coverage?

---

## Phase 2: Generate CONTEXT.md + .attacca/focus.md from Audit

Two files, split by rate of change (see `docs/CONTEXT-SCHEMA.md`). What you inferred about the codebase is stable; what you inferred from recent branches is not.

`CONTEXT.md` at project root:

```markdown
# [Project Name]

[One paragraph: what it is, who uses it, why it matters]

## Stack

- Language: [detected from package.json / manifest]
- Framework(s): [detected]
- Database: [if applicable]
- Testing: [detected test framework]
- Deployment: [detected CI/deployment target]

## Key Decisions

[Architectural patterns you observed. Mark each as OBSERVED, not decided —
 you're inferring intent from code and may be wrong. The team can confirm or
 correct; either way the bullet stays as the record.]
```

`.attacca/focus.md`:

```markdown
# Focus

## Current Focus

[Based on recent commits and branches, what's being worked on now]

## Next Steps

[Based on open issues and project stage]

## Blockers

[If any. "None" if clear.]
```

**If CONTEXT.md already exists**: merge new findings, never overwrite. Ask the user if any detected facts should update it.

**If it exists in the pre-4.3 single-file layout** (has `Current Focus` / `Next Steps` / `Blockers`): migrate it — move those three sections into `.attacca/focus.md`, drop them from `CONTEXT.md`, leave Project / Stack / Key Decisions untouched. Say that you did it. This is the one case where retrofit edits an existing `CONTEXT.md` structurally, and it is lossless.

---

## Phase 3: Merge Settings Safely

**Gitignore**:
- Read existing `.gitignore`
- Merge: combine both, no duplicates
- Never delete existing entries — with one exception: a bare `.attacca/` line must become `.attacca/audits/` + `.attacca/sbom/`, or the committed `focus.md` silently never reaches the remote. Narrowing an ignore is not deleting an entry; say you did it.

**Project config** (CLAUDE.md, etc.):
- If existing `CLAUDE.md` exists, show diff and ask before changing
- Add project-specific conventions (build commands, test framework, deploy target)
- Document any custom rules discovered during audit

---

## Phase 4: Suggest Plugins and Skills

Based on audit findings, recommend:

1. **Plugins for detected stack**:
   - Node.js project? → attacca-node (if available)
   - Python? → attacca-python
   - Rust? → attacca-rust
   - etc.

2. **Skills for common patterns**:
   - Database migrations? → suggest security review for schema changes
   - Deployed on Lambda? → suggest deployment verification skill
   - API-heavy? → suggest OpenAPI/contract testing docs
   - Team using TypeScript? → suggest type-coverage skill

3. **Quality integration**:
   - "Your project runs `npm test` — quality-gate can run that pre-push"
   - "You use GitHub Secrets — document how agents access them safely"
   - "Your CI checks lints — let agents use the same rules"

---

## Phase 5: Retrofit Readiness Checklist

Present to user before any changes:

```
## Retrofit Plan for [Project Name]

Stack: [detected]
Current status: [Active / Maintenance / Legacy]

What will be added:
  ✅ CONTEXT.md with project documentation
  ✅ Merged .gitignore (existing + boilerplate, no conflicts)
  ✅ Updated CLAUDE.md with project conventions
  ✅ Suggested plugins and skills

What will NOT change:
  ❌ Source code (untouched)
  ❌ Existing deployments (untouched)
  ❌ Existing CI/CD workflows (untouched)
  ❌ Existing settings (merged safely)

Recommended next steps:
  1. Review CONTEXT.md for accuracy
  2. Install suggested plugins
  3. Add skills relevant to your workflow

Ready to proceed?
```

---

## Phase 6: Execute Retrofit

When user confirms:

1. **Write CONTEXT.md** (or update if exists)
2. **Merge .gitignore** (combine both files)
3. **Update CLAUDE.md** with project conventions found in audit
4. **Git commit**:
   ```bash
   git add CONTEXT.md .attacca/focus.md .gitignore CLAUDE.md
   git commit -m "chore: retrofit Attacca documentation and settings

   - Added CONTEXT.md with project overview
   - Merged .gitignore (boilerplate + existing)
   - Updated CLAUDE.md with project conventions
   
   No changes to source code or deployments."
   ```

5. **Show installation path for plugins/skills** they picked

---

## Notes

- CONTEXT.md is a map, not a spec — keep it lightweight and update incrementally
- Never overwrite existing `.gitignore` — always merge
- If existing `CLAUDE.md` exists, show diff first
- Source code is never modified
- Existing CI/CD is never bypassed
