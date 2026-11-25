---
name: improve-architecture
description: "Periodically review and improve code architecture. Scan existing PRDs, find deepening opportunities and design debt based on domain language and decision records. Use for regular code health checks or proactive design debt cleanup. Trigger words: architecture, improve-architecture, 重构, 清理, 债务, 架构审查."
---

# Improve Architecture: Review and Improve Code Architecture

🥷 Periodically clean design debt, keep code healthy.

## Outcome Contract

- **Outcome**: Architecture improvement report with findings, priorities, and PRD alignment analysis
- **Done when**: All PRDs scanned, codebase analyzed, findings categorized with priorities and effort estimates
- **Evidence**: Collected code patterns, PRD analysis, architecture alignment assessment
- **Output**: Structured report with blocking/high/medium priority findings

## Prerequisites

Read available domain context before starting. If any are missing, proceed without them and note the limitation in the report:

- `CONTEXT.md` — domain glossary (if missing: scan code naming conventions instead)
- `docs/adr/` — architecture decisions (if missing: no historical decisions to check against)
- `docs/prd/*.md` — product requirements (if missing: report focuses on code patterns only, no PRD alignment analysis)

## Process Summary

**Step 1**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md) — it reads CONTEXT.md, ADRs, and PRDs. Code-level signals (duplication, coupling, long functions) don't strictly require domain context, so proceed even if docs are missing.

**Step 2**: Analyze current development direction — extract planned features, check compatibility with existing architecture

**Step 3**: Scan codebase using prioritized strategy — PRD-linked modules first, high-change-frequency modules next, cross-cutting concerns last. For each module, apply the objective detection heuristics in [REFERENCE.md §Design Debt Signals](REFERENCE.md) (code duplication, long functions, tight coupling, mutable shared state, leaked/missing abstractions, shallow modules, god objects, dead code, speculative generality, message chains, deep inheritance, stub implementations, magic values, swallowed errors, repeated type dispatch — each tagged with the principle it detects, defined in [../rules/engineering-principles.md](../rules/engineering-principles.md), and carrying a concrete grep/line-count threshold). Run the ADR compliance check (REFERENCE §3.3) against each ADR in `docs/adr/`.

**Step 4**: Analyze findings — categorize as blocking/high priority/medium priority with PRD links. Each finding must have specific location, evidence, and impact.

**Step 5**: Propose improvements — problem, suggestion, benefit, effort (Low/Medium/High with rationale), linked PRD

**Step 6**: Generate report — structured findings with next steps

See [REFERENCE.md](REFERENCE.md) for scanning strategy, detection heuristics, ADR compliance procedure, and extended examples.

## Gotchas

| What happened | Rule |
|---|---|
| Modify working code without verifying | Read and understand code before suggesting |
| Rename without improving structure | Deepen modules, don't just rename |
| Change too much at once | Small improvements, one at a time |
| Ignore domain language | Name based on CONTEXT.md terms |
| Violate historical ADR | Check ADRs, create new ADR if needed |
| Ignore PRD constraints | Check if improvement aligns with planned features |
| Introduce new concept without updating | Sync update to CONTEXT.md |

## Output

```
Improve Architecture complete.

Scan scope:       [PRDs: N, Code files: N, ADRs: N]
Alignment:        [✅ N, ⚠️ N, ❌ N]
Findings:         [Blocking: N, High: N, Medium: N]

Next: Review blocking issues → /story to decompose → /implement to orchestrate implementation
```

**PRD Traceability:** If findings link to a PRD, fill the `Arch reviewed by` field:
```markdown
- **Arch reviewed by**: `/improve-architecture` (<YYYY-MM-DD>) — <one-line finding + priority>
```

## Workflow Position

**Independent periodic activity**, not in main development flow:

```
New feature dev: think → grill → story → implement → review
Bug fix: debug → review (optional)
Independent periodic: improve-architecture (every 2-4 weeks)
```
