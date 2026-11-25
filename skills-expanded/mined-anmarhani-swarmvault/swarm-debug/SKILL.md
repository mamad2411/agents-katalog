---
name: swarm-debug
description: Systematic debugging — evidence before hypotheses, hypotheses before fixes, root cause before patches, and the diagnosis saved to the vault. Use for any real bug, test failure, regression, crash, or unexplained behavior — before proposing any fix.
---

# swarm-debug — systematic debugging

No fix without a reproduced cause. Shotgun patching is how the same bug costs twice.

## The loop

1. **Reproduce** — a command/test that shows the bug, or record explicitly why
   reproduction is impossible. This is the entry gate for everything below.
2. **Evidence** — read the FULL error, stack, and surrounding logs (not the first line);
   note what changed recently (git log, new deps, config).
3. **Locate** — binary-search the causal chain: which layer last had correct data?
   Instrument with targeted prints/asserts if needed; remove them after.
4. **Hypothesize** — ranked list, cheapest-to-test first. State each as a falsifiable
   claim ("the cache returns stale X when Y").
5. **Verify** — one targeted experiment per hypothesis. Evidence kills or confirms;
   opinion does neither.
6. **Fix the root cause** — not the symptom, when the root is reachable. If you must ship
   a symptom patch, say so in the code-note and open a ticket for the root.
7. **Regression test** — must fail on the pre-fix code, pass on the fix. No test, no fix.
8. **Record (J1)** — non-trivial diagnosis → memory note (the footgun, compact,
   ≤ 15 lines) + code-note link on the affected file, so no future session pays for this
   twice. Check the vault FIRST next time: `swarmvault.py query --search "<symptom>"` —
   someone may already have paid.

## Hard rules

- Three dead hypotheses → stop, step back, re-examine assumptions — including the spec
  and design ("is the requirement itself contradictory?").
- A diagnosis that reveals a spec/design gap → route it to the question queue / SRS
  change management (swarm-spec), don't silently patch around it.
- Performance bugs: measure before and after; a fix without numbers is a guess.

---
*Influences: superpowers systematic-debugging; Pocock's diagnosing-bugs; Jeffallan's
debugging-wizard — see CREDITS.md.*
