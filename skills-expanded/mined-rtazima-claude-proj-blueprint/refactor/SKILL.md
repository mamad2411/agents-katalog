---
name: refactor
description: "Safe refactoring workflow. Activated when the user says \"refactor\", \"extract\", \"split module\", \"rename\", \"move\", \"restructure\", \"decouple\", \"simplify architecture\", or wants to change code structure without changing behavior."
allowed tools: Read, Write, Edit, Grep, Glob, Bash
---

# Refactoring

Change code structure without changing behavior. Tests must pass before AND after.
This is NOT the slop-cleaner (cosmetic). Refactoring is structural/architectural.

## Rules

1. **Tests green before starting** — if tests don't pass, fix them first (that's debugging, not refactoring)
2. **One refactoring at a time** — don't mix extract-function with rename with move-file
3. **Commit between refactorings** — each structural change gets its own commit
4. **Tests green after each change** — run tests after every refactoring step
5. **ADR for architectural changes** — if the refactoring changes module boundaries, create an ADR
6. **Update imports/references** — grep the entire codebase for references to moved/renamed items
7. **Update docs** — CLAUDE.md module map, README project structure if files moved

## Refactoring Catalog

### Extract
| What | When | How |
|---|---|---|
| Extract function | Logic repeated in 2+ places, or function > 30 lines | Identify the cohesive block, extract, name by intent |
| Extract module/file | File > 300 lines or has 2+ distinct responsibilities | Identify responsibility boundaries, split, update imports |
| Extract interface/type | Concrete type used in 3+ places, or to enable mocking | Define interface, make existing code implement it |
| Extract constant/config | Magic numbers or strings used in multiple places | Move to config or constants file, reference everywhere |

### Move
| What | When | How |
|---|---|---|
| Move function | Function is in the wrong module (called more from elsewhere) | Move, update all imports (`grep -r "functionName" src/`) |
| Move file | File doesn't belong in its current directory | Move, update all imports, update CLAUDE.md if module map changes |

### Rename
| What | When | How |
|---|---|---|
| Rename variable/function | Name doesn't describe intent, or naming convention changed | Rename in definition AND all references |
| Rename file | File name doesn't match its content or convention | Rename, update all imports |

### Simplify
| What | When | How |
|---|---|---|
| Inline function | Function is trivial wrapper with no added logic | Replace calls with the function body, remove function |
| Remove dead code | Code is unreachable or unused | Verify with grep, remove, run tests |
| Flatten nesting | 3+ levels of if/else or callback nesting | Early returns, extract helpers, or async/await |
| Replace conditional with polymorphism | Long switch/if-else on type | Extract interface + implementations |

### Restructure
| What | When | How |
|---|---|---|
| Dependency inversion | Module A directly imports Module B's internals | Extract interface, inject dependency |
| Split layer | Business logic mixed with I/O (DB, HTTP, file) | Separate pure logic from side effects |
| Consolidate duplicates | Same logic in 3+ places with slight variations | Extract shared function, parameterize the variations |

## Workflow

### Phase 1: Assess
1. Understand what needs refactoring and why (code review finding? tech debt? new feature prep?)
2. Run full test suite — confirm all green: `[SPEC] test command`
3. Check if the refactoring affects module boundaries → may need ADR
4. Estimate scope: how many files touched?

### Phase 2: Plan
1. Choose the refactoring type(s) from the catalog above
2. List the specific steps in order
3. Identify risky steps (file moves, interface changes, public API changes)
4. If > 5 files affected, break into multiple commits

### Phase 3: Execute (per step)
```
For each refactoring step:
1. Make the structural change
2. Update all references (grep -r "old_name" src/ tests/)
3. Run tests → must be green
4. Commit: "refactor: {what was done}"
```

### Phase 4: Verify
1. Run full test suite one final time
2. Check that no imports are broken: `[SPEC] compile command`
3. If files moved → update CLAUDE.md module map and README
4. If architecture changed → create ADR

## Anti-patterns (do NOT do these)
- Do NOT refactor and add features in the same commit
- Do NOT rename things without updating all references
- Do NOT skip tests between steps ("I'll test at the end")
- Do NOT refactor code you don't understand — read it first
- Do NOT remove "dead" code without verifying it's truly dead (`grep -r`)

## References
- Martin Fowler's Refactoring catalog
- `docs/architecture/` — existing ADRs
- CLAUDE.md — module map and conventions
