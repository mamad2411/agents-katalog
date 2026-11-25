---
description: when creating synchronizations between concepts
alwaysApply: false
---
# Synchronization Rules

## Synchronization Design Principles

### Flow-Based Composition
- Synchronizations connect independent concepts through declarative rules
- Actions that trigger other actions share a **flow token** (UUID) for grouping
- Each sync conditions on action completions and produces new action invocations

### TypeScript Synchronization Pattern
```typescript
const SyncName = ({ variable1, variable2 }: Vars) => ({
    when: actions(
        [Concept1.action, { input: "pattern" }, { output: variable1 }],
        [Concept2.action, { input: variable2 }, {}],
    ),
    where: (frames: Frames): Frames => {
        return frames
            .query(Concept3._queryFunction, { input: variable1 }, { result: variable2 })
            .filter(($) => $[variable2] > threshold);
    },
    then: actions(
        [Concept4.action, { input: variable2 }],
    ),
});
```

### Sync Structure
- **when**: Match action completions with input/output patterns
- **where**: Filter and enrich frames using pure queries
- **then**: Invoke new actions with bound variables

### Variable Binding
- Destructure variables from `Vars` object: `({ count, user }: Vars)`
- Use variables in patterns to create bindings between actions
- Variables are symbols that carry values through the sync execution

### Frame Processing
- Frames represent execution contexts with variable bindings
- `where` clause takes `Frames` and returns `Frames`
- Use `.query()` to call concept query functions and enrich frames
- Use `.filter()` to apply conditional logic

### Registration
```typescript
// Register all synchronizations
const syncs = { SyncName1, SyncName2, SyncName3 };
Sync.register(syncs);
```

## Engine Setup
```typescript
import { actions, Frames, SyncConcept, Vars } from "./engine/mod.ts";

// Initialize engine
const Sync = new SyncConcept();

// Register and instrument concepts
const concepts = { Concept1: new Concept1(), Concept2: new Concept2() };
const { Concept1, Concept2 } = Sync.instrument(concepts);
```

## Best Practices
- Keep synchronizations focused and granular
- Condition on multiple actions when you need causal relationships
- Use descriptive sync names that capture the business logic
- Test synchronizations with realistic data flows

## Reference Implementation
See [Synchronization Implementation Guide](@docs/synchronization-implementation.md) for complete examples and patterns.