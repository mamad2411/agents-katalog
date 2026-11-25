---
name: react-hook-authoring-fix
description: Audits custom React hooks for overengineering, memoization issues, consumer DX problems, and known antipatterns, then applies fixes. Use when the user wants to audit hooks, fix hook patterns, clean up memoization, or asks "audit hooks", "fix hooks", "check my hooks". Applies the react-hook-authoring principles.
metadata:
  author: b4r7x
  version: "1.0.0"
  argument-hint: <file-paths-or-globs>
---

# React Hook Authoring Fix

Audits custom hooks using the `react-hook-authoring` skill principles and applies fixes.

## Workflow

### Step 1 — Resolve files

Parse the argument as file paths or glob patterns. If no argument is provided, ask:
> "Which hook files should I audit? Pass file paths or glob patterns (e.g. `registry/hooks/*.ts`)."

### Step 2 — Load principles

Read `../react-hook-authoring/SKILL.md` for the decision tree and antipatterns.
Read `../react-hook-authoring/references/approaches.md` for Approach A/B details.

### Step 3 — Audit each hook

For each file containing a custom hook (function starting with `use` and using React hooks internally):

1. Read the file contents
2. Check for each antipattern:

| # | Check | What to look for |
|---|-------|-----------------|
| 1 | **Premature useCallback** | `useCallback` where any dep is unstable (props callback, filtered array, new object) — the memoization achieves nothing |
| 2 | **Side effect in state updater** | `onChange`/callback invoked inside `setState((prev) => { ... })` — fires 2x in Strict Mode |
| 3 | **Ref-during-render** | `ref.current = value` in component body without `useLayoutEffect` — tearing risk. OK only if no `"use client"` (SSR constraint) |
| 4 | **Forcing consumer memoization** | Callback from consumer in `useEffect`/`useCallback` deps — consumer must `useCallback` or hook misbehaves |
| 5 | **Overengineered pattern** | Multiple refs + useCallback + useLayoutEffect when plain function (Approach A) would suffice. Look for: no context consumers, no measured perf issue, hook used in <5 places |
| 6 | **useMemo on primitives** | `useMemo` returning string/number/boolean — pointless, compared by value |
| 7 | **useCallback without memo on child** | Function memoized but passed to non-`memo()` component |
| 8 | **Unstable context value** | Context Provider without `useMemo` on value object — all consumers re-render on every parent render |
| 9 | **Missing Object.is check** | `onChange` called without checking if value actually changed — unnecessary parent updates |

3. For each issue, record:
   - **Line number(s)**
   - **Check #** (1-9)
   - **Severity**: high (bug/DX problem), medium (unnecessary complexity), low (style)
   - **The offending code** (1-5 lines)
   - **Suggested approach** (A or B, or specific fix)

### Step 4 — Classify fixes

- **Auto-fixable** (mechanical, safe):
  - Remove `useCallback` with unstable deps → plain function (Check 1)
  - Remove `useMemo` on primitives (Check 6)
  - Add `useMemo` on context value object (Check 8)

- **Semi-auto** (likely safe, brief explanation before applying):
  - Move `onChange` out of state updater (Check 2)
  - Replace ref-during-render with `useLayoutEffect` (Check 3)
  - Simplify overengineered hook to Approach A (Check 5)
  - Add `Object.is` guard before `onChange` (Check 9)

- **Manual only** (report, don't fix):
  - Consumer memoization requirement (Check 4) — needs API change
  - useCallback without memo (Check 7) — needs consumer-side change
  - Switching from Approach B to A when context consumers exist — needs profiling

### Step 5 — Apply fixes

Process fixes **bottom-up within each file** (highest line number first).

For auto-fixable: apply silently, record change.
For semi-auto: state what changes and why, then apply.
For manual: list in report only.

### Step 6 — Output report

```
## Hook Authoring Audit Report

**Files audited:** N
**Issues found:** N (H high, M medium, L low)

---

### `path/to/hook.ts`

| Line | Severity | Check | Issue |
|------|----------|-------|-------|
| 23 | high | #2: Side effect in updater | `onChange?.(resolved)` inside `setInternal((prev) => ...)` |
| 40 | medium | #1: Premature useCallback | `useCallback([isControlled, onChange])` — onChange is unstable |

**Changes applied:**
- L23: Moved `onChange` call after `setInternal`
- L40: Replaced `useCallback` with plain function (Approach A)

**Manual review needed:**
- L67: Consumer must `useCallback` on `onFilter` prop or `useEffect` at L70 re-runs

---

### Summary

| Check | Count |
|-------|-------|
| 1. Premature useCallback | N |
| 2. Side effect in updater | N |
| ... | ... |

### Verify

Run type-check and tests to confirm nothing broke:
\`\`\`bash
pnpm type-check && pnpm test
\`\`\`
```

If zero issues found:
```
## Hook Authoring Audit Report

**Files audited:** N
**Issues found:** 0

Clean. No hook authoring issues detected.
```
