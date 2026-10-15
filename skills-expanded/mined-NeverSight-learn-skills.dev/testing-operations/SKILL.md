---
name: testing-operations
description: Contract and regression testing workflows. Use when writing tests, validating contract compliance, or creating regression test suites.
---

# Testing Operations

Testing operations cover writing contract compliance tests, regression tests, and validating test coverage for 3Lens.

## When to Use

- Writing contract compliance tests
- Creating regression tests from traces
- Validating test coverage
- Debugging test failures
- Understanding test patterns

## Test Types

### Contract Compliance Tests

Tests that validate contract invariants:

```typescript
// tests/contracts/inspector.test.ts
import { describe, it, expect } from 'vitest';
import { createLens } from '@3lens/runtime';

describe('Inspector Contract', () => {
  it('answers the 5 questions for any entity', async () => {
    const lens = createLens();
    const entityId = 'mesh:main:myMesh';
    
    // Question 1: What is this?
    const info = await lens.inspect(entityId, { include: ['info'] });
    expect(info).toBeDefined();
    
    // Question 2: Dependencies?
    const deps = await lens.inspect(entityId, { include: ['dependencies'] });
    expect(deps.dependencies).toBeArray();
    
    // Question 3: What depends on it?
    const dependents = await lens.inspect(entityId, { include: ['dependents'] });
    expect(dependents.dependents).toBeArray();
    
    // Question 4: Cost?
    const cost = await lens.inspect(entityId, { include: ['cost'] });
    expect(cost.cost).toHaveProperty('attribution');
    
    // Question 5: How has it changed?
    const diffs = await lens.inspect(entityId, { include: ['diffs'] });
    expect(diffs.diffs).toBeArray();
  });
});
```

### Regression Tests

Tests that detect regressions:

```typescript
// tests/regression/baseline.test.ts
import { describe, it, expect } from 'vitest';
import { loadTrace } from '@3lens/kernel';

describe('Regression: Baseline Performance', () => {
  it('maintains frame time budget', async () => {
    const trace = await loadTrace('./traces/baseline.json');
    const frames = trace.getFrames();
    
    const avgFrameTime = frames.reduce((sum, f) => sum + f.duration, 0) / frames.length;
    expect(avgFrameTime).toBeLessThan(16.67); // 60fps budget
  });
  
  it('maintains memory budget', async () => {
    const trace = await loadTrace('./traces/baseline.json');
    const peakMemory = trace.getPeakMemory();
    
    expect(peakMemory).toBeLessThan(100 * 1024 * 1024); // 100MB budget
  });
});
```

### Snapshot Tests

Tests for stable outputs:

```typescript
// tests/snapshots/entity-graph.test.ts
import { describe, it, expect } from 'vitest';
import { createEntityGraph } from '@3lens/kernel';

describe('Entity Graph Snapshots', () => {
  it('generates consistent graph structure', () => {
    const graph = createEntityGraph();
    // ... build graph
    
    expect(graph.snapshot()).toMatchSnapshot();
  });
});
```

## Commands

### Run Contract Tests

```bash
# Run all contract tests
3lens test contracts

# Test specific contract
3lens test contracts --contract inspector

# Show coverage
3lens test contracts --coverage

# Watch mode
3lens test contracts --watch
```

### Generate Regression Tests

```bash
# Generate regression test from trace
3lens test:generate-regression baseline.json --out tests/regression/baseline.test.ts
```

### Check Test Coverage

```bash
# Check contract test coverage
3lens test:coverage contracts
```

## Test Patterns

### Fidelity Testing

```typescript
it('labels fidelity for all metrics', async () => {
  const result = await client.query('top_hotspots');
  result.items.forEach(item => {
    expect(item).toHaveProperty('fidelity');
    expect(['EXACT', 'ESTIMATED', 'UNAVAILABLE']).toContain(item.fidelity);
  });
});
```

### Attribution Testing

```typescript
it('provides attribution path for metrics', async () => {
  const metric = await client.query('top_hotspots');
  expect(metric.attribution).toBeArray();
  expect(metric.attribution.length).toBeGreaterThan(0);
  expect(metric.attribution[0]).toHaveProperty('entityId');
  expect(metric.attribution[0]).toHaveProperty('weight');
});
```

### Live/Offline Parity Testing

```typescript
describe('Live and Offline Parity', () => {
  it('works in live mode', async () => {
    const lens = createLens();
    // Test live mode
  });
  
  it('works with offline traces', async () => {
    const trace = await loadTrace('./traces/test.json');
    // Test offline mode
  });
});
```

## Agent Use Cases

1. **New feature**: "Generate tests for my new panel"
2. **Contract compliance**: "Write tests for the inspector contract"
3. **Regression**: "Create regression test from this trace"
4. **Coverage**: "Check test coverage for contracts"

## Test Requirements

Every test MUST:

1. **Validate Contract Invariants**
   - Test all contract requirements
   - Include degradation scenarios

2. **Include Fidelity Checks**
   - Verify fidelity labeling
   - Test fidelity propagation

3. **Include Attribution Checks**
   - Verify attribution paths
   - Test attribution weights

4. **Test Live/Offline Parity**
   - Test both modes
   - Verify consistent results

## Post-Scaffold Steps

After writing tests, follow the playbook:
- [.cursor/playbooks/write-tests.md](../../../.cursor/playbooks/write-tests.md)

## Additional Resources

- Contract: [.cursor/contracts/testing.md](../../../.cursor/contracts/testing.md) (if exists)
- Rule: [.cursor/rules/test-standards.mdc](../../../rules/test-standards.mdc)
- Use `vitest` for tests; [validate-contracts](../../../commands/validate-contracts.md) for contract validation
- Subagent: [.cursor/agents/test-generator.md](../../../agents/test-generator.md)