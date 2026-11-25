# @stateproof/core — AgentSkill

## Description

Formal specification testing for TypeScript. Define state machines → compile to TLA+ → exhaustive model checking → generated tests.

## When to Use

- Designing state machines that need correctness guarantees
- Verifying concurrent/distributed system invariants
- Generating test traces from specifications
- Creating runtime state machines from specs

## Quick Reference

### Define a Machine

```typescript
import { machine } from '@stateproof/core'

const m = machine('Name')
  .states('a', 'b', 'c')
  .initial('a')
  .context({ count: 0 })
  .transition('go', {
    from: 'a',
    to: 'b',
    guard: (ctx) => ctx.count > 0,
    action: (ctx) => {
      ctx.count += 1
    }
  })
  .invariant('bounded', (ctx) => ctx.count <= 10)
  .liveness('eventually b', 'a', ['b'])
```

### Verify

```typescript
import { verify } from '@stateproof/core'
const result = await verify(m, { maxStates: 100000, workers: 4 })
// result.ok, result.violations, result.statesExplored
```

### Generate Tests

```typescript
import { generateTests } from '@stateproof/core'
const traces = await generateTests(m, { strategy: 'coverage' })
// traces[].steps[].action, .expectedState
```

### Runtime

```typescript
import { createRuntime } from '@stateproof/core'
const rt = createRuntime(m)
rt.send('go') // returns boolean
rt.state // current state
rt.context // current context
```

### Concurrent

```typescript
import { concurrent } from '@stateproof/core'
const c = concurrent('Pool')
  .instances('worker', workerMachine, { count: 3 })
  .shared('queue', [])
  .invariant('bounded', 'Len(queue) <= 10')
```

### Diagrams

```typescript
import { toMermaidStateDiagram } from '@stateproof/core'
const mermaid = toMermaidStateDiagram(m)
```

## Constraints

- Guards/actions must use the constrained JS subset (no closures, no async, no arbitrary calls)
- TLC requires Java to be installed for model checking
- Without TLC, compilation and test generation still work
