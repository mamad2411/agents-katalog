---
name: onboarding-sherpa
description: Use when joining, returning to, or inheriting an undocumented codebase — maps architecture, key patterns, and the files to start with.
metadata:
  added: 2026-06-27
  last_reviewed: 2026-06-27
  type: meta
  status: draft
  related: [technical-writing, architecture-essentials]
  owns: codebase-onboarding
---

# Onboarding Sherpa

This skill makes an unfamiliar codebase navigable in minutes. Use it when someone is
joining a new project, returning after time away, inherited a codebase with no docs, or
needs to understand a codebase well enough to make a specific change.

The goal is not comprehensive documentation — it's a MENTAL MODEL. The 20% of knowledge
that gives 80% of understanding. It answers: "Where do I start? What matters? What can I
ignore?"

Use read-only commands only (`git log/blame/show/diff/status`, `wc`, `find` for listing).
Never run a write or delete operation (`git push`, `git reset --hard`, `find -delete`,
`find -exec rm`).

## Discovery process

### Phase 1: Structure scan (30 seconds)

```bash
# What's here?
find . -maxdepth 2 -type f | head -50
# How big is it?
find . -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" | wc -l
# What's the tech stack?
ls package.json Cargo.toml go.mod requirements.txt pyproject.toml Gemfile 2>/dev/null
```

Read package.json (or equivalent) for dependencies, scripts, project name.

### Phase 2: Architecture map (2 minutes)

Identify the architecture pattern:

- **Monolith**: single deployable, everything in src/
- **Monorepo**: multiple packages in packages/ or apps/
- **Microservices**: multiple services with separate configs
- **Framework app**: Next.js, Rails, Django, etc. (follow framework conventions)

Map the key directories: where code lives (src/, app/, lib/), where tests are, where
config is, where types/schemas are, and the entry point (index.ts, main.py, cmd/).

### Phase 3: Pattern recognition (2 minutes)

Read 3-5 representative files to identify coding style (functional vs OOP, verbose vs
terse), error handling pattern (try/catch, Result type, error codes), data flow (REST,
GraphQL, tRPC, message queue), state management (Redux, Context, Zustand, none), and
testing approach (unit-heavy, integration-heavy, E2E, none).

### Phase 4: Tribal knowledge (1 minute)

Look for undocumented but critical knowledge:

- Grep for `IMPORTANT`, `NOTE`, `WARNING`, `CAREFUL` in comments
- Check for `.env.example` — what secrets are needed?
- Check CI/CD config — what runs on deploy?
- Check for migration files — database schema history
- Read the most-recently-modified files — what's actively being worked on?

## Output: codebase brief

```markdown
# Codebase Brief: [project name]

## In One Sentence

[What this project does, who it's for]

## Tech Stack

- **Language:** [primary] · **Framework:** [main] · **Database:** [if any]
- **Key dependencies:** [3-5 most important]

## Architecture

[2-3 sentences describing the high-level architecture pattern]

## Directory Map

[key directories with one-line descriptions]

## Key Files (start here)

1. [file] — [why it matters]
2. [file] — [why it matters]
3. [file] — [why it matters]

## Patterns to Know

- **Data flow:** [how data moves through the system]
- **Error handling:** [the convention used]
- **Testing:** [approach and where tests live]

## Gotchas

- [Non-obvious thing that will bite you]

## To Start Working

1. [First setup step]
2. [How to run locally]
3. [How to run tests]
```

## Rules

- Speed over completeness. A rough map NOW beats a perfect map LATER.
- Prioritize what you'd need to make your FIRST change, not everything.
- If there's no documentation, that IS the finding — note it.
- Don't read every file. Read representative files from each layer.
- Name specific files. "The auth system is in..." not "there's an auth system."
- If the codebase is a mess, say so diplomatically but clearly.
