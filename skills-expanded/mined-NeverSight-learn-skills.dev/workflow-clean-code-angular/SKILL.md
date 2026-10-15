---
name: workflow-clean-code-angular
description: "Deep Angular 21 clean code audit with parallel specialist agents and senior team lead. Scans architecture, signals, stores, AI slop, ViewModel patterns, and more. Guarantees craftsman-level output. Use whenever the user says 'clean code', 'audit Angular', 'review frontend', 'check quality', 'anti-patterns', wants Angular code reviewed, or needs senior-level code standards enforced — even if they don't say 'clean code' explicitly."
argument-hint: "<scope> [-a auto] [-e economy] [-s save] [--quick] [--deep] [--arch] [--signals] [--styling] [--testing] [--slop] [--vm]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion, mcp__plugin_context7_context7__*
---

<objective>
Guarantee that Angular code in the target scope meets the standard of a senior developer who crafted it by hand — clean, clear, no AI slop, proper architecture, correct signal patterns, and clear ViewModel separation.
</objective>

<philosophy>
This isn't a linter. Linters catch syntax. This skill catches **design decisions** — the kind of issues only a senior engineer spots during code review.

Three things that separate senior-crafted code from AI-generated code:
1. **Nothing unnecessary** — no defensive checks for impossible scenarios, no abstractions with one consumer, no comments that restate the code
2. **Right responsibility in the right place** — stores own data transformations, components coordinate UI, templates just bind
3. **Consistent patterns** — every store follows the same anatomy, every component follows the same structure, no surprise conventions
</philosophy>

<quick_start>

```bash
/clean-code-angular feature/budget/          # Standard audit
/clean-code-angular -a --deep feature/       # Deep audit, auto mode
/clean-code-angular --quick core/            # Quick surface scan
/clean-code-angular --slop --vm feature/     # Focus: AI slop + ViewModel
/clean-code-angular diff main                # Audit changes vs main
/clean-code-angular pending                  # Audit uncommitted changes
```

</quick_start>

<parameters>

| Flag | Description |
|------|-------------|
| `-a` | Auto mode — skip confirmations |
| `-e` | Economy mode — no subagents, direct analysis only |
| `-s` | Save — output reports to `.claude/output/clean-code-angular/` |
| `-r` | Resume — continue from a previous run |
| `--quick` | Surface scan only (grep patterns, no semantic analysis) |
| `--deep` | Full depth: all domains including AI slop + ViewModel + cross-file |
| `--arch` | Force architecture analysis |
| `--signals` | Force signal patterns analysis |
| `--styling` | Force styling analysis |
| `--testing` | Force testing analysis |
| `--slop` | Force AI slop detection |
| `--vm` | Force ViewModel/DataModel analysis |
| `--adv` | Adversarial review — after team lead, a devil's advocate agent challenges every finding for false positives, missed issues, and severity inflation |
| `--ultra` | Maximum depth: 15 specialists in 5 clusters, each with a cluster lead, plus grand tech lead and adversarial review. The nuclear option for critical code. |

Default depth (no flag): grep + targeted semantic analysis of key files.
`--deep` enables all specialist domains.

</parameters>

<workflow>
```
SCAN ─────────────────► APPLY ─────────────► VERIFY
  │                       │                     │
  ├─ Parse scope          ├─ Load docs/refs     ├─ Lint + type-check
  ├─ Launch specialists   ├─ Apply fixes        ├─ Run tests
  │  (up to 10 agents)    │  (parallel agents)  ├─ Team lead final
  ├─ Team lead review     ├─ Team lead          │  craftsman review
  ├─ Adversarial review   │  coherence check    ├─ Adversarial final
  │  (if --adv)           └─ Track progress     │  challenge (if --adv)
  └─ Consolidated issues                        └─ Commit
```
</workflow>

<agent_model>

## Agent Architecture

The skill scales agent count based on flags:

| Mode | Agents | Structure |
|------|--------|-----------|
| Economy (`-e`) | 0 | Direct tools only, no subagents |
| Standard | 3-10 + lead | Flat: specialists → team lead |
| Deep (`--deep`) | 14 + lead | 8 single + 3 signal lenses + 3 slop lenses → consensus → team lead |
| Deep + Adv (`--deep --adv`) | 14 + lead + adv | Deep + adversarial review |
| **Ultra (`--ultra`)** | **15 + 5 leads + grand lead + adv = 22** | **5 clusters → 5 cluster leads → grand tech lead → adversarial** |

### Standard/Deep Mode — Flat Architecture

Up to 10 domain-focused specialists launched in parallel. Count scales with scope size:

| Scope | Agents | Coverage |
|-------|--------|----------|
| 1-4 files | 3 + lead | Architecture, Angular/Signals, TypeScript/Styling |
| 5-15 files | 5 + lead | + Store patterns, Component design |
| 16-30 files | 7 + lead | + Templates, AI slop |
| 31+ files | 10 + lead | All 10 domains |

### The 10 Domains

| # | Domain | Focus |
|---|--------|-------|
| 1 | Architecture & Dependencies | Layer violations, cross-feature imports, dependency direction |
| 2 | Signals & Reactivity | `effect()` misuse, `computed()` opportunities, `linkedSignal()`, cleanup |
| 3 | Store Patterns | 6-section anatomy, cache-first, optimistic updates, resource usage |
| 4 | Component Design | OnPush, responsibility, size, `input()`/`output()`, `inject()` |
| 5 | Template Quality | Control flow, expression complexity, wrapper bloat, accessibility |
| 6 | TypeScript Quality | `any` types, `#` fields, modern APIs, dead code |
| 7 | Styling | `::ng-deep`, Material M3 tokens, Tailwind v4, `!important` |
| 8 | AI Slop | Over-engineering, unnecessary comments, defensive theater, verbose naming |
| 9 | ViewModel & Data Flow | DataModel vs ViewModel, transformation location, duplicate derivations |
| 10 | Security, Performance & Code Health | XSS, workarounds/hacks, design smells, `@defer`, lazy loading |

**Testing quality** is checked when `--testing` or `--deep` or `--ultra` is enabled. The testing specialist reads `.spec.ts` files in scope and evaluates against `references/testing-patterns.md`.

### Ultra Mode — Multi-Tier Cluster Architecture

15 specialists organized in 5 clusters, each with a dedicated cluster lead. Each specialist loads exactly the reference files it needs — no bloat.

**Cluster 1: Architecture** → Architecture Lead
| Agent | Focus | Loads |
|-------|-------|-------|
| 1a | Layer violations, cross-feature imports | `references/angular-architecture.md` |
| 1b | DI patterns, functional interceptors, providers | `references/angular-clean-code.md` §3 |
| 1c | Lazy loading, routing, `@defer` boundaries | `references/angular-anti-patterns.md` §19-20 |

**Cluster 2: Signals & State** → Reactivity Lead
| Agent | Focus | Loads |
|-------|-------|-------|
| 2a | Signal patterns, computed, effect, afterRenderEffect | `references/angular-clean-code.md` §2 |
| 2b | Store anatomy, mutations, resource API | `references/angular-clean-code.md` §2 + §13 |
| 2c | RxJS valid vs anti-pattern, Observable/Signal bridge | `references/angular-anti-patterns.md` §2 + Valid RxJS table |

**Cluster 3: Code Quality** → Quality Lead
| Agent | Focus | Loads |
|-------|-------|-------|
| 3a | TypeScript, types, modern APIs (toSorted, structuredClone) | `references/angular-anti-patterns.md` §6 |
| 3b | AI slop detection (all 9 categories) | `references/ai-slop-detection.md` |
| 3c | Error handling, catch typing, resource error state | `references/angular-clean-code.md` §13 |

**Cluster 4: UI & Templates** → Frontend Lead
| Agent | Focus | Loads |
|-------|-------|-------|
| 4a | Control flow, @defer, template expressions | `references/angular-clean-code.md` §4 |
| 4b | Styling, accessibility, NgOptimizedImage | `references/angular-anti-patterns.md` §7 + §20-21 |
| 4c | Pipes, ViewModel separation, formatting | `references/viewmodel-patterns.md` + `references/angular-clean-code.md` §15 |

**Cluster 5: Testing & Security** → Security Lead
| Agent | Focus | Loads |
|-------|-------|-------|
| 5a | Test quality, harnesses, coverage | `references/testing-patterns.md` |
| 5b | Security, workarounds, zoneless violations | `references/angular-anti-patterns.md` §8 + §15-16 |
| 5c | Signal Forms, API validation, forms patterns | `references/angular-clean-code.md` §14 + §9 |

**Flow:**
```
15 specialists (parallel) → 5 cluster leads (parallel) → Grand Tech Lead → Adversarial
```

### Team Lead (Standard/Deep)

Launched after specialists complete. A senior Angular architect who:
- Merges all specialist reports into one deduplicated list
- Removes false positives by reading the actual code
- Resolves contradictions between specialists
- Adds cross-cutting observations no single specialist caught
- Prioritizes the final issue list
- Verifies fix coherence in step-02
- Does final craftsman review in step-03

### Cluster Leads (Ultra)

Each cluster lead receives ONLY its 3 specialists' reports. They:
- Deduplicate within their domain
- Resolve contradictions between their specialists
- Add domain-specific cross-cutting observations
- Output a focused domain report (max 10 issues per cluster)

### Grand Tech Lead (Ultra)

Receives all 5 cluster lead reports. A principal Angular architect who:
- Merges all cluster reports into one unified list
- Resolves cross-cluster contradictions (e.g., Architecture says "move to core" but Quality says "inline it")
- Identifies systemic patterns across clusters (e.g., "every file has the same DI problem")
- Prioritizes by business impact, not just technical severity
- Caps at 30 issues, notes total if more
- Adds a "systemic diagnosis" section: what's the ROOT CAUSE behind the pattern of issues?

### Adversarial Reviewer (--adv or --ultra)

Launched after the team/grand lead. A skeptical senior engineer who:
- **Challenges each finding**: "Is this really wrong? Could there be a valid architectural reason?"
- **Hunts false positives**: reads the actual code for each flagged issue and checks if context was missed
- **Hunts missed issues**: reads ALL files in scope looking for issues that ALL specialists + leads missed
- **Questions severity**: "Is this really Critical or just Important? Would a production user notice?"
- **Checks RxJS false flags**: verifies that valid RxJS patterns aren't flagged as signal anti-patterns
- **Checks Angular version assumptions**: verifies recommendations match Angular 21+
- **Checks against project profile**: verifies that no finding contradicts the project's documented conventions from {project_profile}

Output: a correction table listing upgrades, downgrades, removals, and additions to the lead's findings.

</agent_model>

<state_variables>

| Variable | Type | Description |
|----------|------|-------------|
| `{task_description}` | string | Scope to analyze |
| `{task_id}` | string | Kebab-case identifier |
| `{auto_mode}` | boolean | Skip confirmations |
| `{economy_mode}` | boolean | No subagents |
| `{save_mode}` | boolean | Save reports |
| `{depth}` | quick / standard / deep | Analysis depth |
| `{force_*}` | boolean | Per-domain force flags |
| `{scoped_files}` | string[] | Files in scope |
| `{issues}` | array | Consolidated issue list |
| `{workspace_path}` | string | Path to angular.json |
| `{agent_count}` | number | Specialists to launch |
| `{adversarial_mode}` | boolean | Run adversarial review after team lead |
| `{ultra_mode}` | boolean | Full 22-agent multi-tier architecture |
| `{project_profile}` | object | Detected project conventions, libraries, and architecture decisions — used to filter false positives |

</state_variables>

<reference_files>

| File | When Loaded |
|------|-------------|
| `references/angular-anti-patterns.md` | Always (scanning checklist) |
| `references/angular-clean-code.md` | Always (correct patterns) |
| `references/angular-style-guide.md` | Always (official Angular conventions) |
| `references/angular-architecture.md` | Architecture issues or `--arch` |
| `references/ai-slop-detection.md` | Deep mode, `--slop` |
| `references/viewmodel-patterns.md` | Deep mode, `--vm` |
| `references/testing-patterns.md` | Testing issues or `--testing` |

</reference_files>

<entry_point>

Load `steps/step-01-scan.md`

</entry_point>

<step_files>

| Step | File | Purpose |
|------|------|---------|
| 01 | `step-01-scan.md` | Parse scope, launch specialists, team lead consolidation |
| 02 | `step-02-apply.md` | Load docs, apply fixes, team lead coherence check |
| 03 | `step-03-verify.md` | Quality gate, craftsman review, commit |

</step_files>

<execution_rules>
- Discover project context BEFORE scanning — read CLAUDE.md, package.json, angular.json, eslint config to build {project_profile}
- Filter ALL findings through {project_profile} — never flag patterns that match documented project conventions
- Load one step at a time
- Scale agent count to scope size (economy mode = 0 agents, direct tools only)
- Use the Grep tool for pattern detection (not bash grep)
- Scope-aware: only touch files within the specified scope
- Every finding: `file:line` reference required
- Every fix: source citation required
- Team lead reviews after scan AND after apply
</execution_rules>

<success_criteria>
After this workflow, the scoped code reads as if a senior Angular developer wrote it by hand:
- Zero architecture violations
- Modern signal patterns throughout
- Stores follow 6-section anatomy with proper ViewModel selectors
- No AI slop — no unnecessary comments, abstractions, or defensive code
- Clean ViewModel separation — stores transform, components bind, templates stay simple
- Consistent patterns across all files in scope
- Quality check passes (lint + type-check + format)
- Tests pass
- If --adv: adversarial review found no missed issues or false positives
</success_criteria>
