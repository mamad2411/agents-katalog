# Flaky Test Detector Skill

A Claude Code skill for detecting flaky test patterns that cause intermittent CI failures.

## Trigger Phrases

This skill activates when you mention:
- "flaky test"
- "intermittent failure"
- "test sometimes fails"
- "race condition in test"
- "timing issue in test"
- "test passes locally but fails in CI"
- "non-deterministic test"

## Capabilities

### Pattern Detection
Scans `*.test.ts` and `*.spec.ts` files to detect:

| Severity | Pattern | Risk |
|----------|---------|------|
| HIGH | `ttl.*:\s*1\b` | 1-second TTL causes second-boundary race conditions |
| HIGH | `Math.floor(Date.now() / 1000)` | Second truncation creates timing edge cases |
| HIGH | `setTimeout([^,]+,\s*\d{1,2})` | Very short timeouts (<100ms) are unreliable |
| MEDIUM | `Date.now()` without mocking | Real time in tests causes non-determinism |
| MEDIUM | `timeout.*:\s*[1-9]0?\b` | Low timeout values cause race conditions |
| MEDIUM | `new Date()` without mocking | Real date in tests causes flakiness |
| LOW | `Math.random()` without seeding | Random values cause non-determinism |
| LOW | `process.nextTick` in assertions | Timing-dependent assertions |

### Context Extraction
For each detected pattern, the skill extracts:
- File path and line number
- Surrounding code context (3 lines before/after)
- Pattern severity classification
- Specific risk explanation

### Fix Suggestions
Generates actionable fix suggestions:
- `vi.useFakeTimers()` for time-based flakiness
- TTL increase recommendations
- Mock injection patterns
- Deterministic alternatives

## Usage

### Scan Current Directory
```bash
# Run the detector on all test files
npx tsx scripts/index.ts

# Scan specific directory
npx tsx scripts/index.ts ./src/tests

# Output as JSON
npx tsx scripts/index.ts --json
```

## Integration with CI

Add to your CI pipeline to catch flaky patterns before merge:

```yaml
- name: Check for flaky test patterns
  run: npx tsx scripts/index.ts --ci
```
