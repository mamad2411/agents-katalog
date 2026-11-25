---
name: state-audit
description: Audits React state management - finds prop drilling, redundant state, and suggests improvements
argument-hint: [directory]
user-invocable: true
allowed-tools: Read Grep Glob
effort: medium
---

## State Management Audit

Target: **$1** (or `src/` if not specified)

### 1. Detect State Management
```bash
cat package.json | grep -E '"zustand"|"jotai"|"recoil"|"redux"|"@tanstack/query"|"swr"'
grep -rn "useState\|useReducer\|createStore\|create(" ${1:-src/} --include="*.tsx" | wc -l
```

### 2. Find Prop Drilling
Look for props passed more than 2 levels deep without being used in intermediate components:
```bash
grep -rn "Props {" src/ --include="*.tsx" | head -20
```
Read component trees to identify drilling patterns.

### 3. Find Redundant State
- Derived state stored instead of computed: `const [fullName, setFullName]` when `firstName` and `lastName` exist
- Server data stored in `useState` when a query library is available
- Duplicate state in parent and child

### 4. Find Missing Memoization
- Expensive computations in render without `useMemo`
- Callbacks recreated every render passed to memoized children

### 5. Recommendations
For each issue, recommend the fix:
- Prop drilling → Context, Zustand slice, or composition
- Derived state → remove and compute inline
- Over-fetching → React Query/SWR with proper cache keys

Report severity and effort for each item.
