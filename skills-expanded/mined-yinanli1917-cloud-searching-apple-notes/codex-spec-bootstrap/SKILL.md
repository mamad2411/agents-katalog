---
name: codex-spec-bootstrap
description: "Analyze a codebase and generate durable spec files from existing patterns, architecture, and conventions. Use to initialize or refresh .codex/spec/ for a project. Also use when the lifecycle hook reminds you to run spec-bootstrap, when a project has empty or template-only specs, when the user says 'generate specs', 'initialize specs', 'bootstrap specs', or 'make the codebase context durable'."
---

# Spec Bootstrap

Scan the current project's codebase and generate `.codex/spec/project/` files that capture durable knowledge — architecture decisions, module contracts, conventions, performance constraints, and operational rules.

## Process

### 1. Discover Project Shape

```bash
# File tree (depth 3)
find . -maxdepth 3 -type f \( -name "*.swift" -o -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.rs" \) | head -80

# Existing documentation
cat CLAUDE.md 2>/dev/null
cat README.md 2>/dev/null
cat AGENTS.md 2>/dev/null

# Existing specs (don't duplicate)
ls .codex/spec/project/ 2>/dev/null
ls .codex/spec/guides/ 2>/dev/null

# Package/module structure
find . -maxdepth 2 -name "Package.swift" -o -name "package.json" -o -name "pyproject.toml" -o -name "Cargo.toml" 2>/dev/null

# Git history for major patterns
git log --oneline -30
git log --oneline --all --diff-filter=A -- "*.swift" "*.py" "*.ts" | head -20
```

### 2. Identify Spec-Worthy Knowledge

Read key source files to find:

- **Architecture boundaries** — what modules exist, what are their responsibilities, how do they communicate
- **Data flow patterns** — how state moves through the app (e.g., MusicKit → ViewModel → View)
- **Performance constraints** — any throttling, caching, batching, or real-time requirements
- **Platform conventions** — API patterns, error handling, naming, file organization
- **Integration contracts** — external services, APIs, system frameworks, their constraints
- **Hard-won lessons** — patterns that exist because of past bugs (check git blame for "fix" commits)

Skip knowledge that is:
- Already in existing spec files
- Trivially derivable from reading one file
- Ephemeral (version numbers, current bugs, in-progress work)

### 3. Generate Spec Files

For each distinct knowledge area, create a spec file:

```
.codex/spec/project/<topic-slug>.md
```

Format:
```markdown
# <Topic Name>

## Architecture
<How this area is structured>

## Contracts
<What must remain true — invariants, interfaces, constraints>

## Patterns
<Established patterns to follow when modifying this area>

## Constraints
<Performance, platform, or design constraints>

## Lessons
<Hard-won knowledge from past incidents — reference git commits if relevant>
```

Not every section is needed for every spec — only include sections with real content.

### 4. Update Index

After generating specs, update the index:

```
.codex/spec/project/index.md
```

Format:
```markdown
# Project Specs

| Spec | Scope | Key Constraint |
|------|-------|----------------|
| [topic-slug](topic-slug.md) | One-line scope | Most important constraint |
```

### 5. Record to Journal

```bash
python3 scripts/codex_harness.py record-session --title "Spec bootstrap" --summary "Generated N spec files from codebase analysis: <list>"
```

## Rules

- Never generate generic advice. Every statement must reference real files, real patterns, real constraints from THIS codebase.
- If an existing spec already covers a topic, UPDATE it (merge new findings) rather than creating a duplicate.
- Projected template files (cross-session-continuity.md, spec-update-protocol.md, geb-documentation.md) are harness infrastructure — don't touch them.
- One spec per distinct knowledge area. Don't create a single mega-spec.
- Max 150 lines per spec file. If longer, split into sub-topics.
- After generating, verify by reading back each file and checking that every claim is traceable to source.
