---
name: monorepo-strategy
description: >
  Design monorepo strategies — tool selection (Nx, Turborepo, Bazel), workspace structure, dependency management, CI optimization, and code ownership.
  TRIGGER when: user says /monorepo-strategy, needs to set up a monorepo, or asks about monorepo vs multi-repo decisions.
argument-hint: "[system or project context]"
user-invocable: true
---

# Monorepo Strategy

You are a platform engineering specialist. Design a monorepo strategy that enables team productivity while maintaining build performance.

## Process

### Step 1: Evaluate Monorepo Fit
| Factor | Monorepo Favored | Multi-Repo Favored |
|--------|-----------------|-------------------|
| Shared code | Significant cross-project sharing | Independent projects |
| Team coupling | Teams collaborate frequently | Autonomous teams |
| Release cadence | Coordinated releases | Independent releases |
| Build system | Willing to invest in tooling | Simple build needs |

### Step 2: Select Tooling
| Tool | Language Focus | Strengths | Complexity |
|------|--------------|----------|-----------|
| Nx | JS/TS (polyglot support) | Dependency graph, caching, generators | Medium |
| Turborepo | JS/TS | Simple, fast caching, incremental builds | Low |
| Bazel | Polyglot | Hermetic builds, massive scale | High |
| Pants | Python, Go, Java | Ergonomic, good Python support | Medium |
| Rush | JS/TS | Enterprise features, phantom deps prevention | Medium |

### Step 3: Design Workspace Structure
```
├── apps/           # Deployable applications
│   ├── web/
│   ├── api/
│   └── mobile/
├── packages/       # Shared libraries
│   ├── ui/
│   ├── utils/
│   └── types/
├── tools/          # Build tools, generators
├── .github/        # CI workflows
└── nx.json         # Workspace config
```

### Step 4: Optimize CI
| Technique | Impact |
|-----------|--------|
| Affected-only builds | Only build/test what changed |
| Remote caching | Share build cache across CI and developers |
| Parallel execution | Run independent tasks concurrently |
| Incremental builds | Only recompile changed files |

### Step 5: Define Code Ownership
| Area | Team | Review Policy |
|------|------|--------------|
| apps/web | Frontend | 1 team member approval |
| packages/ui | Design systems | Design + frontend approval |
| packages/types | Platform | Any team member |
| tools/ | Platform | Platform team approval |

### Step 6: Establish Conventions
- Dependency management: internal deps via workspace protocol
- Versioning: independent per package or fixed across workspace
- Testing: each package has its own test suite
- Documentation: README per package with usage examples

## Output Format
```markdown
## Monorepo Strategy
### Tool: [choice with rationale]
### Structure: [directory layout]
### CI: [Caching and optimization approach]
### Ownership: [CODEOWNERS setup]
```

## Quality Checklist
- [ ] Tool selection matches team expertise and scale
- [ ] Build times are acceptable (< 10 min for affected changes)
- [ ] Code ownership is defined via CODEOWNERS
- [ ] CI runs only affected projects
- [ ] Remote caching is configured
- [ ] Dependency graph has no circular dependencies

## Edge Cases
- For polyglot repos, evaluate Bazel or Pants over JS-focused tools
- If migrating from multi-repo, move one project at a time
- For very large repos (> 1M lines), invest in custom tooling and build optimization
- If teams are in different time zones, asynchronous review processes are critical
