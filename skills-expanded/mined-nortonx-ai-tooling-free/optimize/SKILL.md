---
name: optimize
description: "Analyze code for performance bottlenecks and recommend optimizations. Supports Vue SFCs. Args: [branch | backend | frontend | <path>]"
argument-hint: "[branch | backend | frontend | <path>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[branch | backend | frontend | <path>]`

- Optional. Picks the analysis scope; the skill prompts with a numbered menu if omitted.
- **Examples**: `/optimize branch`, `/optimize backend`, `/optimize src/services/payments.ts`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Optimize: $ARGUMENTS

Analyze code for performance bottlenecks. **Only flag a finding when the fix meets BOTH of these criteria:**

1. The fix removes a measurable cost: algorithmic complexity drop (e.g., O(n^2) -> O(n)), one fewer DB/HTTP round-trip per call, one fewer reactive re-render per interaction, >= 5% bundle-size reduction, or eliminated memory allocation in a hot path.
2. The fix is <= 30 lines of code change OR is a one-line config/index change.

Skip:
- Stylistic-only changes (rename, reorder, reformat).
- Micro-optimizations whose impact you cannot estimate.
- "Defensive" caching of values that are not measured to be hot.
- Anything that adds a new dependency unless the dependency replaces >= 100 lines of in-repo code.

## Scope

If `$ARGUMENTS` is empty, **stop and ask the user** which scope to analyze before doing anything else. Present this numbered menu verbatim and wait for a reply:

```
Which scope should I analyze?
  1. branch       : diff between this branch and main/master
  2. backend      : server-side code only (API, DB, services)
  3. frontend     : client-side code only (components, bundles, assets)
  4. <file path>  : a specific file (e.g. src/foo.ts)
  5. <component>  : a component or module name
```

Otherwise interpret `$ARGUMENTS` as:

- **`branch`**: diff between this branch and `main`/`master`
- **`backend`**: server-side code only
- **`frontend`**: client-side code only
- **`full`**: entire codebase under the current working directory
- **file path**: analyze that specific file (stop if file does not exist)
- **anything else**: treat as a component or module name and locate it

## Analysis Areas

Apply the categories relevant to the detected scope:

- **Algorithms**: O(n^2) or worse, redundant calculations, memory leaks
- **Database**: N+1 queries, missing indexes, query optimization, caching strategies
- **API**: response times, chatty interfaces, pagination, caching headers
- **Frontend**: unnecessary re-renders or reactive computations, Vue SFC reactivity pitfalls (computed vs watch, missing shallowRef, v-memo), missing memoization (React useMemo/useCallback/React.memo, Svelte/Angular fine-grained signals), large bundle contributions, code-splitting, lazy loading, inefficient state management, expensive computations in render path, unoptimized assets
- **Async**: await misuse in loops, missing parallelism (Promise.all), missed caching opportunities

## Output Format

For each finding:

```markdown
### <Severity: Critical | High | Medium>

- **Location**: `path/to/file.ext:line`
- **Category**: Algorithms | Database | API | Frontend | Async
- **Expected Improvement**: <Concrete impact, Big-O reduction, or latency metric>
- **Complexity**: Easy | Medium | Hard

#### Current Code
```<language>
// Current snippet
```

#### Optimized Code
```<language>
// Optimized snippet
```
```

If no bottlenecks meet the criteria, output:

> "No performance bottlenecks meeting the severity criteria were identified in the scoped code."

## Rules

- **DO NOT implement fixes. DO NOT edit any files. Report only.**
- Technical facts and data overrule opinions and personal preferences.
- Match the codebase conventions and framework style (React, Vue, Svelte, Angular, Node, Go, Python).
- Address the code, not the developer.
- If the target file or component cannot be found, report that it does not exist and stop.
