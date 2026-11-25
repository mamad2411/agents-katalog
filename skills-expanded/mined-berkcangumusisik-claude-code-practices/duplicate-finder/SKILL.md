---
name: duplicate-finder
description: Finds duplicated logic across the codebase and proposes shared abstractions
argument-hint: [directory]
user-invocable: true
allowed-tools: Bash Grep Read
effort: medium
---

## Find Duplicate Code

1. Look for structural duplication:
```bash
# Similar function signatures
grep -rn "async function\|const .* = async" ${1:-src}/ --include="*.ts" | sort | head -40

# Similar patterns (fetch calls, error handling, etc.)
grep -rn "try {" ${1:-src}/ --include="*.ts" -l
```

2. Read suspected duplicate files side by side.

3. Identify duplication categories:
   - **Identical blocks**: copy-pasted code
   - **Near-duplicates**: same logic, different variable names
   - **Structural similarity**: same pattern, different implementations

4. For each duplication cluster:
   - Show the duplicated sections
   - Propose a shared abstraction (utility function, custom hook, base class)
   - Show how call sites would look after extraction

5. Ask which ones to consolidate, then apply.

Focus on impactful duplications (3+ occurrences or > 20 lines).
