---
name: harness-engineering
description: Apply Harness Engineering methodology to design agent-first development environments — build CLAUDE.md maps, progressive documentation, mechanical enforcement, golden principles, and agent legibility into any project.
---

# Harness Engineering

Harness Engineering is the discipline of designing environments, feedback loops, and control systems that enable AI coding agents (Codex, Claude Code, Cursor, etc.) to reliably build and maintain complex software.

**Core philosophy: Humans steer. Agents execute.**

The human engineer's primary job is no longer to write code, but to design environments, specify intent, and build feedback loops that allow agents to do reliable work.

## What this skill helps with

This skill helps you transform any project into an agent-first codebase by applying the principles from OpenAI's Harness Engineering methodology:

1. **Audit** your current project for agent-readiness
2. **Generate** an `CLAUDE.md` that acts as a map, not a manual
3. **Structure** progressive documentation (`docs/` knowledge base)
4. **Design** architectural constraints and mechanical enforcement (linters, structural tests)
5. **Define** golden principles for your codebase
6. **Build** agent-to-agent review loops
7. **Plan** garbage collection workflows for continuous code quality
8. **Create** execution plan templates for complex work
9. **Optimize** your project for agent legibility

## Core Principles (Verified)

These are the verified principles derived from the OpenAI Harness Engineering article:

### P1: Context is a Scarce Resource

A giant instruction file crowds out the task, the code, and the relevant docs. Agents either miss key constraints or optimize for the wrong ones.

**Application**: Keep `CLAUDE.md` under ~100 lines. Use it as a table of contents pointing to deeper sources of truth.

### P2: Too Much Guidance Becomes Non-Guidance

When everything is "important," nothing is. Agents end up pattern-matching locally instead of navigating intentionally.

**Application**: Prioritize constraints. Mark only the top 3-5 rules as critical. Everything else goes in supporting docs.

### P3: Documentation Rots Instantly

A monolithic manual turns into a graveyard of stale rules. Agents can't tell what's still true, humans stop maintaining it.

**Application**: Split knowledge into versioned, owned, cross-linked documents. Validate freshness mechanically with CI jobs or recurring agent tasks.

### P4: Progressive Disclosure

Agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front.

**Application**: `CLAUDE.md` → `docs/architecture.md` → domain-specific docs → inline code comments.

### P5: Enforce Invariants, Not Implementations

Specify what must be true, not how to write the code. Let agents ship fast without undermining the foundation.

**Application**: Custom linters that check layering rules, naming conventions, file size limits, logging format — not code style preferences.

### P6: Repository-Local Knowledge

Anything an agent can't access in-context effectively doesn't exist. Knowledge in Google Docs, Slack threads, or people's heads is invisible to the system.

**Application**: If a decision was made in a discussion, it must be captured in the repo as a document or code comment.

### P7: Boring Technology Wins

Technologies described as "boring" tend to be easier for agents to model due to composability, API stability, and representation in the training set.

**Application**: Prefer stable, well-documented libraries. In some cases, reimplement subsets of functionality rather than working around opaque upstream behavior.

### P8: Garbage Collection for Code

Technical debt is like a high-interest loan: pay it down continuously in small increments rather than letting it compound.

**Application**: Schedule recurring agent tasks that scan for deviations, update quality grades, and open targeted refactoring PRs.

### P9: Agent Legibility First

Optimize the codebase for the agent's ability to reason about it, not just for human readability.

**Application**: Make the app bootable per worktree. Wire observability (logs, metrics, traces) into the agent runtime. Expose DOM snapshots for UI validation.

### P10: Non-Blocking Workflows

In a system where agent throughput far exceeds human attention, corrections are cheap and waiting is expensive.

**Application**: Minimal blocking merge gates. Short-lived PRs. Flakes addressed with follow-up runs rather than blocking progress.

## Operating Rules

1. **Never generate a monolithic CLAUDE.md.** Always keep it under ~100 lines and use it as a map.
2. **Always reference the source.** When applying a principle, cite which principle (P1-P10) it derives from.
3. **Always validate existing state first.** Before generating any artifact, audit what already exists in the project.
4. **Prefer mechanical enforcement over documentation.** If a rule can be a linter, make it a linter. Documentation is for rules that cannot be encoded mechanically.
5. **Respect the depth-first approach.** Break larger goals into smaller building blocks. Enable the agent to construct those blocks before tackling more complex tasks.
6. **Never prescribe specific implementations.** Define constraints and boundaries. Let the agent choose how to satisfy them.
7. **Always include verification status.** Every document should track whether it's been verified against the actual codebase.

## Workflow

### Phase 1: Audit

When the user invokes this skill, first audit the current project:

1. Check for existing `CLAUDE.md`, `CLAUDE.md`, or similar agent instruction files
2. Scan the `docs/` directory structure (if it exists)
3. Identify the project type (language, framework, architecture)
4. Look for existing linters, CI jobs, and structural tests
5. Check for `README.md` and existing documentation quality
6. Identify the architectural pattern (monolith, microservices, etc.)

### Phase 2: Assess

Based on the audit, assess:

1. **Agent-readiness score** (0-10) across dimensions:
   - Context management (P1, P2, P3)
   - Documentation structure (P4, P6)
   - Mechanical enforcement (P5)
   - Agent legibility (P9)
   - Workflow design (P8, P10)
2. **Top 3 gaps** — the most impactful improvements
3. **Quick wins** — changes that can be made immediately

### Phase 3: Generate

Based on the assessment, generate the requested artifacts:

- `CLAUDE.md` — map-style entry point
- `docs/` structure — progressive documentation layout
- Linter configurations — mechanical enforcement rules
- Golden principles — opinionated rules for the codebase
- Execution plan templates — for complex work
- CI job configurations — for documentation validation and quality checks

### Phase 4: Validate

After generating artifacts:

1. Cross-reference generated docs with actual codebase structure
2. Verify all links and references are valid
3. Ensure principles are internally consistent
4. Generate a verification checklist

## Intent Mapping

### Audit my project for agent-readiness

```
→ Execute Phase 1 (Audit) + Phase 2 (Assess)
→ Output: Agent-readiness score with top 3 gaps and quick wins
```

### Generate CLAUDE.md

```
→ Execute Phase 1 (Audit)
→ Analyze existing codebase structure
→ Generate concise CLAUDE.md (~100 lines) as table of contents
→ Include pointers to docs/, architecture, and core principles
→ Apply P1, P2, P4 (context scarcity, non-guidance, progressive disclosure)
```

### Design documentation structure

```
→ Execute Phase 1 (Audit)
→ Design progressive docs/ layout
→ Create index documents with verification status
→ Apply P3, P4, P6 (freshness, progressive disclosure, repo-local knowledge)
```

### Create golden principles

```
→ Analyze codebase patterns and team preferences
→ Generate opinionated, mechanical rules
→ Encode them as linters where possible
→ Apply P5, P8 (enforce invariants, garbage collection)
```

### Set up mechanical enforcement

```
→ Identify architectural constraints
→ Generate custom linter rules
→ Create structural tests
→ Apply P5 (enforce invariants, not implementations)
```

### Design agent review loops

```
→ Configure agent-to-agent review workflow
→ Set up PR automation
→ Apply P10 (non-blocking workflows)
```

### Full harness setup

```
→ Execute all phases (Audit → Assess → Generate → Validate)
→ Generate complete agent-first environment
→ Include: CLAUDE.md, docs/ structure, linters, golden principles, CI jobs
```

## Safety Boundaries

1. **Never overwrite existing CLAUDE.md or CLAUDE.md** without explicit user confirmation
2. **Never modify production code** — this skill generates scaffolding, documentation, and tooling only
3. **Never prescribe a specific language or framework** — adapt to what the project already uses
4. **Never assume the project is a greenfield** — always respect existing conventions
5. **Never generate more than 100 lines for CLAUDE.md** — if it's getting long, restructure into docs/

## Verified Artifacts

This skill can generate the following verified artifacts:

| Artifact | Description | Key Principle |
|----------|-------------|---------------|
| `CLAUDE.md` | Agent entry point map (~100 lines) | P1, P2, P4 |
| `docs/architecture.md` | Top-level architecture map | P4, P6 |
| `docs/principles.md` | Golden principles and beliefs | P5, P8 |
| `docs/quality.md` | Quality grades per domain/layer | P5, P8 |
| `.linters/` | Custom linter configurations | P5 |
| `docs/plans/` | Execution plan templates | P4, P6 |
| `docs/decisions/` | Architecture decision records | P6 |
| CI job configs | Documentation freshness validation | P3 |

## Example Triggers

- "Audit my project for agent-readiness"
- "Generate an CLAUDE.md for my codebase"
- "Set up harness engineering for my project"
- "Create golden principles for my codebase"
- "Design progressive documentation structure"
- "Set up mechanical enforcement for architecture constraints"
- "帮我审查项目的 Agent 就绪度"
- "生成 CLAUDE.md 文件"
- "设计分层架构约束"
- "建立代码垃圾回收机制"

## Cross-Reference

For detailed worked examples, see [examples.md](./examples.md).
