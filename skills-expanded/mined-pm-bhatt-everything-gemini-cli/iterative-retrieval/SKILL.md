---
name: iterative-retrieval
description: Pattern for progressively refining context retrieval to solve the subagent context problem
---

# Iterative Retrieval Pattern

Solves the "context problem" in multi-step workflows where you don't know what context is needed until you start working.

## The Problem

When approaching complex tasks, you don't know:
- Which files contain relevant code
- What patterns exist in the codebase
- What terminology the project uses

Standard approaches fail:
- **Send everything**: Exceeds context limits
- **Send nothing**: Lacks critical information
- **Guess what's needed**: Often wrong

## The Solution: Iterative Retrieval

A 4-phase loop that progressively refines context:

```
┌─────────────────────────────────────────────┐
│   ┌──────────┐      ┌──────────┐            │
│   │ DISPATCH │─────▶│ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   LOOP   │◀─────│  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        Max 3 cycles, then proceed           │
└─────────────────────────────────────────────┘
```

### Phase 1: DISPATCH

Initial broad query to gather candidate files:

```javascript
const initialQuery = {
  patterns: ['src/**/*.ts', 'lib/**/*.ts'],
  keywords: ['authentication', 'user', 'session'],
  excludes: ['*.test.ts', '*.spec.ts']
};

const candidates = await retrieveFiles(initialQuery);
```

### Phase 2: EVALUATE

Assess retrieved content for relevance:

```javascript
function evaluateRelevance(files, task) {
  return files.map(file => ({
    path: file.path,
    relevance: scoreRelevance(file.content, task),
    reason: explainRelevance(file.content, task),
    missingContext: identifyGaps(file.content, task)
  }));
}
```

Scoring criteria:
- **High (0.8-1.0)**: Directly implements target functionality
- **Medium (0.5-0.7)**: Contains related patterns or types
- **Low (0.2-0.4)**: Tangentially related
- **None (0-0.2)**: Not relevant, exclude

### Phase 3: REFINE

Update search criteria based on evaluation:

```javascript
function refineQuery(evaluation, previousQuery) {
  return {
    patterns: [...previousQuery.patterns, ...extractPatterns(evaluation)],
    keywords: [...previousQuery.keywords, ...extractKeywords(evaluation)],
    excludes: [...previousQuery.excludes, ...evaluation
      .filter(e => e.relevance < 0.2)
      .map(e => e.path)
    ],
    focusAreas: evaluation.flatMap(e => e.missingContext).filter(unique)
  };
}
```

### Phase 4: LOOP

Repeat with refined criteria (max 3 cycles):

```javascript
async function iterativeRetrieve(task, maxCycles = 3) {
  let query = createInitialQuery(task);
  let bestContext = [];

  for (let cycle = 0; cycle < maxCycles; cycle++) {
    const candidates = await retrieveFiles(query);
    const evaluation = evaluateRelevance(candidates, task);

    const highRelevance = evaluation.filter(e => e.relevance >= 0.7);
    if (highRelevance.length >= 3 && !hasCriticalGaps(evaluation)) {
      return highRelevance;
    }

    query = refineQuery(evaluation, query);
    bestContext = mergeContext(bestContext, highRelevance);
  }

  return bestContext;
}
```

## Practical Example

```
Task: "Fix the authentication token expiry bug"

Cycle 1:
  DISPATCH: Search for "token", "auth", "expiry" in src/**
  EVALUATE: Found auth.ts (0.9), tokens.ts (0.8), user.ts (0.3)
  REFINE: Add "refresh", "jwt" keywords; exclude user.ts

Cycle 2:
  DISPATCH: Search refined terms
  EVALUATE: Found session-manager.ts (0.95), jwt-utils.ts (0.85)
  REFINE: Sufficient context (2 high-relevance files)

Result: auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts
```

## Best Practices

1. **Start broad, narrow progressively** - Don't over-specify initial queries
2. **Learn codebase terminology** - First cycle often reveals naming conventions
3. **Track what's missing** - Explicit gap identification drives refinement
4. **Stop at "good enough"** - 3 high-relevance files beats 10 mediocre ones
5. **Exclude confidently** - Low-relevance files won't become relevant
