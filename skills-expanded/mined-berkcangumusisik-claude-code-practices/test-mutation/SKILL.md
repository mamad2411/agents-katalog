---
name: test-mutation
description: Analyzes test quality by identifying mutations your tests would NOT catch
argument-hint: <file-path>
user-invocable: true
allowed-tools: Read Grep Glob
effort: medium
---

## Mutation Testing Analysis

Target: **$1**

Since we can't run Stryker/mutmut directly, do a manual mutation analysis:

1. Read the source file and its test file.

2. Apply common mutations mentally and check if existing tests would catch them:
   - Change `>` to `>=` (boundary condition)
   - Negate boolean conditions (`!`)
   - Remove a function call
   - Change `&&` to `||`
   - Return early / return null instead of computed value
   - Off-by-one in loops

3. For each mutation that would NOT be caught:
   - Describe the mutation
   - Explain why it would go undetected
   - Write a test that catches it

4. Report:
```
Surviving mutations found: N
Tests added: N
Estimated mutation score: X% → Y%
```
