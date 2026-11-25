---
name: speckit.backlog
description: Backlog Manager - Manage Ideas, Pending Requests and scan TODO/FIXME from codebase.
---

## Mission
Organize, triage, and prioritize unfulfilled requirements, technical debt, and prospective features, ensuring no ideas or defect signals are lost during long-term development.

## Inputs and Outputs
- Read `.agents/memory/constitution.md`, existing backlog files (`.agents/backlog/IDEAS.md`, `TECHNICAL_DEBT.md`), recent specs, and codebase search results.
- Preserve stable item IDs, maintain prioritization rationale, and record dated state transitions when promoting or resolving items.

## Protocol

### 1. Intake & Deduplication
- Capture problem statement, user value, reproducibility evidence, affected component, priority, and clear acceptance criteria.
- Deduplicate against existing items by linking related IDs; categorize as Feature Idea, Bug, Technical Debt, or Security Risk. Never silently discard an item.

### 2. Automated Debt & Marker Scan
- Scan targeted scope for source markers (`TODO:`, `FIXME:`, `HACK:`, `BUG:`) using `rg`; record file, line number, actionable context, and severity.
- Persist scanned debt findings in `.agents/backlog/TECHNICAL_DEBT.md` with timestamp and query command.

### 3. Grooming & Promotion
- Periodically review stale or blocked backlog items, establish minimal next actionable steps, and promote ready items to formal feature specs (`spec.md`).
- Ensure priority changes have explicit rationale; never close or mark items resolved without verified test or acceptance evidence.

## Completion Gate
Backlog entries are categorized with stable IDs, technical debt logs reflect current codebase reality, and promoted items link to corresponding specifications.

## Guard Rails
- DO NOT arbitrarily delete the backlog without asking the user.
- DO NOT overflow the context by listing thousands of TODOs. Only list tasks related to the area you are working on.
- DO NOT mark items resolved without verified test, review, or user acceptance evidence.
