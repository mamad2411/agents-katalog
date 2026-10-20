---
name: lyra-debug
description: Debugging discipline built on the scientific method — invoke when fixing any bug, crash, test failure, flaky behavior, or "it doesn't work" report.
compatibility: No tools required. Optional: language debuggers (node inspect, pdb, xdebug, delve, rust-gdb, jdb, dotnet-dbg, byebug), structured logging, distributed tracing.
---

# lyra-debug

## What it does

A bug is the gap between your mental model and the system's actual behavior; debugging is the disciplined closing of that gap. This skill applies the scientific method — observe, hypothesize, test, conclude — to every defect, from a unit-test failure to a prod-only race. It enforces one change per iteration, a regression test written before the patch, and root-cause analysis over symptom-fixing. It is tool-light and language-agnostic across TS, JS, Python, PHP, Go, Rust, Java, C#, and Ruby.

## The rules

### 1. Treat every bug as a hypothesis to falsify

State the cause: "the bug occurs because <X>." If you can't, you have a hunch — and panic-debugging a hunch without writing it down burns the hour you don't have.

```
// bad — "probably a caching issue, let me clear it"
// good — "DiscountService caches the promo rate 5 min; admin updates are
//         immediate. Disabling the cache should make the total correct
//         right after an admin update."
```

### 2. No reproduction, no fix

If you can't reproduce it, you can't prove the fix worked — "it stopped" is hiding, not fixing. A flaky repro is still a repro: capture the trigger conditions, and for races, amplify with stress runs or `loom`/`pytest-repeat` rather than re-running until green.

### 3. Reduce to the minimal reproducer

Strip inputs, dependencies, and code paths until removing one more thing makes the bug disappear. Ten lines of focused test beats 90 seconds of e2e.

### 4. Binary-search the location

If the bug exists in state A but not B, the cause is in the difference. Halve the difference repeatedly — `git bisect` over commits, print statements over execution.

```
git bisect start && git bisect bad HEAD && git bisect good v1.4.0
# ~7 steps for 100 commits, instead of reading every file hoping to spot it
```

### 5. Verbalize your mental model

Explain the triggering code path out loud, line by line, to a duck or a colleague. The act of verbalizing forces your model into a linear sequence and surfaces the gap you were skipping.

### 6. Rank hypotheses, don't anchor

List plausible causes, rank by likelihood × ease of test, and test the top one. Your first guess is one of N; the brain over-weights it. Your code is wrong 99% of the time — eliminate it before blaming the framework or the language.

### 7. Change exactly one thing per iteration

Two changes and the bug disappears leaves you unable to say which mattered — or which introduced the next bug. One change, one observation; revert if no effect.

```
// bad — "updated the lib, changed retry logic, tweaked the timeout, ship it"
// good — bump timeout → still fires → revert. Enable retry-on-reset → still
//        fires → revert. Pin lib to v2.3.1 → gone. Revert just that → returns.
//        Cause confirmed.
```

### 8. Confirm the cause, not the absence of the symptom

The fix removes the symptom, reverting it restores the symptom, and the mechanism matches your hypothesis. All three, or you have a coincidence — "I changed X and it went away" is correlation, not causation.

### 9. Write the failing regression test before the fix

The test is the executable form of the bug — it must fail before the patch and pass after. Without it, the fix is an opinion, and the bug will return.

```go
func TestOrderTotal_AppliesDiscountBeforeTax(t *testing.T) {
    order := Order{Subtotal: 100.00, Promo: "SAVE10"}
    if got := CalculateTotal(order); got != 97.00 {
        t.Fatalf("got %.2f, want 97.00", got)
    }
} // RED first, then patch until green
```

### 10. Log then trace, especially for prod-only bugs

When you can't attach a debugger, add structured logs at the boundary first; logs prove the path actually taken, a debugger proves the path you assumed. Never "works on my machine" your way out of a prod-only bug — ship a logging change, wait for recurrence, read the trace.

```ts
log.info("discount.lookup", { orderId, promoCode, cachedRate, liveRate });
// fires once an hour → cachedRate=0.10, liveRate=0.15 → hypothesis confirmed
```

### 11. 5 Whys to root cause

The proximate cause is rarely the root. Ask why five times — or until you hit a process, system, or missing safeguard, never a person. Fixing the proximate closes this bug; fixing the root closes the class.

```
1. Total wrong?      → DiscountService returned a stale rate.
2. Stale?            → 5-min cache TTL; admin updates are immediate.
3. TTL 5 min?        → Copied from a 2019 config; never revisited.
4. Never revisited?  → No alerting on stale-cache hits.
5. No alerting?      → Cache metrics aren't exported.
→ ship metrics + alert, not just a TTL bump.
```

### 12. Document the bug, the cause, and the fix

The commit or PR states the symptom, the minimal reproducer, the root cause, the fix, and the regression test that guards it. Undocumented fixes get re-introduced.

The whole loop, in order:

1. Reproduce.
2. Reduce.
3. Isolate via `git bisect`.
4. Verbalize the path.
5. Hypothesize, ranked.
6. Test one change.
7. Confirm the cause (revert restores).
8. Regression test first.
9. 5 Whys.
10. Document.

## Worked example

A prod order-total mismatch fires once an hour; can't reproduce locally. Ship a structured log at the discount-lookup boundary.

Next day's logs: `cachedRate=0.10` vs `liveRate=0.15`. Hypothesis: stale cache. Disable the cache on a canary — mismatch drops to zero. Re-enable — mismatch returns. Cause confirmed.

Write the regression test first: mock a 6-minute-old cache entry, assert the live rate is used. Red. Patch the lookup to bypass stale reads. Green.

5 Whys lands on missing cache-metrics export. Ship metrics plus an alert on stale reads — not just a TTL bump, which would re-break at a different rate.

PR: "fix: discount lookup reads stale promo rates (#412)" — body carries reproducer, trace, test, and root cause.

_Part of the [skill collection](../README.md)._