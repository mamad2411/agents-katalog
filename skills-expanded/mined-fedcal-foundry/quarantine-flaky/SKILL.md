---
name: quarantine-flaky
description: Detect, quantify, quarantine and actually fix flaky tests. Use when CI is red for no reason, when people re-run builds to get them green, when retries are hiding instability, or before adding tests to a suite nobody trusts. Every quarantine entry gets a named owner, a 14-day deadline and one of exactly three exits. Do not use to make a build green by disabling tests.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[--detect] [--quarantine <spec>] [--audit]"
user-invocable: true
model: sonnet
effort: medium
metadata:
  foundry.vertical: quality
  foundry.io: "ci history -> quarantine.json + finding.v1"
license: Apache-2.0
---

# Quarantine and fix flaky tests

A flaky test is one that passes and fails on the same code. It is worse than no test: it costs
runtime, it costs attention, and it teaches the team that red means "try again" — which is how a
real regression gets merged.

Quarantine is a **loan against trust**. This skill makes sure every loan is recorded, owned and
repaid.

## When not to use this

- The test fails consistently → it is not flaky, it found something. Use
  `superpowers:systematic-debugging`.
- You want a green build before a deadline → quarantining without the record below is just
  deleting tests slowly. Refuse.
- The whole suite fails intermittently → that is infrastructure, not flakiness. Look at the CI
  runner, the shared environment, or a dependency, and file a `finding.v1` against ops.

## The one rule

**Never fix a flake by adding a sleep, raising a global timeout, or adding a retry.** All three
convert a flaky suite into a slow flaky suite and destroy the signal you need to find the cause.

## Step 1 — Detect, mechanically

Flakiness is a property of runs, not of opinions. Two detection sources:

**A. Retry telemetry.** If your runner retries, it already knows. Extract the tests that failed
then passed within the same run, over the last 20 runs. Most runners emit JUnit XML.

For a full report (per-test rates, windows, correlations) use the bundled script:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/flake-report.mjs ci-results/
```

Or, inline with no dependencies:

```bash
node -e '
const fs=require("node:fs"),path=require("node:path");
const dir=process.argv[1]; const counts=new Map();
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".xml"))){
  const xml=fs.readFileSync(path.join(dir,f),"utf8");
  // handles both <testcase .../> (pass) and <testcase ...>...</testcase> (pass or fail)
  for(const m of xml.matchAll(/<testcase\b([^>]*?)(\/)?>(?:([\s\S]*?)<\/testcase>)?/g)){
    const attrs=m[1];
    const name=(attrs.match(/(?:^|\s)name="([^"]*)"/)||[])[1];   // \s guard: classname contains "name="
    const cls=(attrs.match(/(?:^|\s)classname="([^"]*)"/)||[])[1]||"";
    if(!name) continue;
    const failed=/<(failure|error)\b/.test(m[3]||"");
    const key=cls+"::"+name;
    const c=counts.get(key)||{pass:0,fail:0}; failed?c.fail++:c.pass++; counts.set(key,c);
  }
}
const flaky=[...counts].filter(([,c])=>c.pass>0&&c.fail>0)
  .map(([k,c])=>({test:k,fails:c.fail,runs:c.pass+c.fail,ratePercent:+(100*c.fail/(c.pass+c.fail)).toFixed(1)}))
  .sort((a,b)=>b.ratePercent-a.ratePercent);
console.log(JSON.stringify(flaky,null,2));
' ci-results/
```

**B. Deliberate repetition.** When there is no history, produce it. Run the suite 20 times on an
**unchanged commit**:

```bash
mkdir -p .foundry/scratch/flake && FAILS=0
for i in $(seq 1 20); do
  <your test command> > .foundry/scratch/flake/run-$i.log 2>&1 || FAILS=$((FAILS+1))
done
echo "suite-level flake rate: $((FAILS * 5))%  ($FAILS/20 runs failed on unchanged code)"
grep -hoE '(✕|FAIL|FAILED) .*' .foundry/scratch/flake/run-*.log | sort | uniq -c | sort -rn | head -20
```

20 runs is the minimum that distinguishes a 5% flake from noise. Fewer runs is an anecdote.

## Step 2 — Quantify before acting

No test is quarantined without these six numbers/facts recorded. A quarantine entry without them
is rejected in review:

| Field | How to get it |
|---|---|
| `failureRatePercent` | from step 1, over ≥ 20 runs |
| `firstSeen` | the earliest run in the window where it failed |
| `errorClass` | normalised failure message, not the raw string |
| `correlations` | shard index, worker count, time of day, CI runner type, run order |
| `traceUrl` / artefact path | trace, video, screenshot, logs from a failing run |
| `hypothesis` | one sentence from the taxonomy below |

The `correlations` field is what makes fixes fast. Check them explicitly:

```bash
# Does it only fail with high parallelism? Then it is shared state, not timing.
<test command> --workers=1  # x10
<test command> --workers=8  # x10
# Does it fail only when run after another test? Then it is order dependence.
<test command> --shuffle    # if your runner supports it; otherwise reverse the file order
```

## Step 3 — Classify the cause

Use the taxonomy in `references/flake-taxonomy.md`. The short version, in the order these occur
in practice:

1. **Shared state** — two tests touch the same record, file, port, cache or global. Signature:
   fails only in parallel or only in a certain order.
2. **Timing / race** — asserting before the app finished. Signature: fails more on slow or busy
   runners; passes locally always.
3. **Time and timezone** — midnight, month end, DST, leap day, a test that assumes "today".
   Signature: fails at a specific hour or on specific dates.
4. **Ordering assumptions** — asserting an order the system never promised (map iteration,
   unordered SQL results, concurrent completions).
5. **External dependency** — a third party, DNS, a network blip. Signature: correlates with
   nothing internal.
6. **Resource exhaustion** — ports, file descriptors, memory, connection pool. Signature: the
   Nth test fails, whichever test is Nth.
7. **The product is genuinely racy** — the test is right and the code is wrong. This one is a
   `finding.v1`, not a test fix, and it is more common than teams assume.

Classifying before fixing matters because the fixes are disjoint: a shared-state flake is
unaffected by any amount of waiting work.

## Step 4 — Quarantine, with a due date

Tag the test (`@quarantine`, a tag/category/marker in your runner), exclude it from the
merge-blocking run, and **keep it running on a schedule** so data keeps accruing. A quarantined
test that stops running is a deleted test.

Append to `test/quarantine.json`:

```json
{
  "spec": "e2e/checkout.spec.ts::guest pays by card",
  "reason": "shared-state: two workers reuse the same seeded product sku",
  "owner": "amelia.rossi",
  "openedOn": "2026-08-27",
  "deadline": "2026-09-10",
  "failureRatePercent": 18.5,
  "runsObserved": 20,
  "errorClass": "expect(locator).toBeVisible() timeout 10000ms",
  "correlations": ["workers>=4", "shard 2"],
  "artefact": ".foundry/scratch/flake/trace-run-7.zip",
  "hypothesis": "product sku collision between workers",
  "exit": null
}
```

`owner` is a **person**, never a team. `deadline` is `openedOn + 14 days`, always.

## Step 5 — Enforce the quarantine budget in CI

Without enforcement, quarantine is a graveyard. Add this gate to the pipeline:

```bash
node -e '
const fs=require("node:fs");
const q=JSON.parse(fs.readFileSync("test/quarantine.json","utf8"));
const today=process.argv[1]; // pass the date in, do not read the clock in CI logic you want reproducible
const errs=[];
if(q.length>3) errs.push(`quarantine holds ${q.length} tests (max 3)`);
for(const e of q){
  if(!e.owner) errs.push(`${e.spec}: no owner`);
  if(!e.deadline) errs.push(`${e.spec}: no deadline`);
  else if(e.deadline < today) errs.push(`${e.spec}: overdue since ${e.deadline} (owner ${e.owner})`);
  if(e.failureRatePercent==null) errs.push(`${e.spec}: not quantified`);
}
if(errs.length){console.error("QUARANTINE GATE FAILED\n"+errs.join("\n"));process.exit(1)}
console.log(`quarantine OK: ${q.length}/3 entries, none overdue`);
' "$(date -u +%F)"
```

`quarantined > 3` fails the build. The cap is the point: an unbounded quarantine is a deleted
suite with extra ceremony.

## Step 6 — Exit, one of exactly three

| Exit | Condition | Evidence required |
|---|---|---|
| **fixed** | root cause named in the commit message; spec then passes **20 consecutive** scheduled runs with 0 retries | the 20-run log |
| **deleted** | the test failed the level-allocation criteria on re-examination, or a cheaper test now covers the failure mode | the id of the replacing test |
| **escalated** | the instability is in the product | a `finding.v1` id, owner and due date; deadline moves **once**, to the finding's due date |

There is no fourth exit. "It seems fine now" is not an exit — flakes that disappear without a
named cause come back, and the 20-run confirmation is what distinguishes the two.

Record the exit in the entry, keep the entry for 90 days as history, then archive it. The
history is how you find out that three flakes shared one cause.

## Fixes by cause

Full catalogue in `references/flake-taxonomy.md`. The high-yield moves:

- **Shared state** → give every test its own namespace derived from worker id + run id, seed via
  API not UI, and stop reusing a "test account". This single change resolves the largest share
  of flakes in most suites.
- **Timing** → assert the end state, not the elapsed time; wait for the specific network
  response or an app-emitted readiness signal; disable animations globally.
- **Time** → inject a fixed clock at the boundary; never assert values derived from "now"; add
  explicit unit tests for the DST and month-end boundaries so the E2E does not have to care.
- **Ordering** → assert set membership or sort before comparing; if order matters to a user,
  make the system promise it (an `ORDER BY`) rather than the test assume it.
- **External** → stub at the network boundary in the PR pipeline, keep a scheduled canary
  against the real vendor outside it.
- **Resources** → bind to port 0 and read the assigned port; close what you open in a
  `finally`; cap workers to measured capacity.

## Exit criteria

1. A flake rate is **measured** over ≥ 20 runs, never estimated.
2. Every quarantined test has a person, a `deadline` ≤ `openedOn + 14 days`, a recorded
   `failureRatePercent`, an `errorClass` and an artefact link.
3. `quarantined ≤ 3`, enforced by the CI gate above.
4. Zero flakes were "fixed" by adding a sleep, a retry or a global timeout increase — verify:
   ```bash
   git diff --unified=0 origin/main -- test/ e2e/ | grep -nE '^\+.*(sleep|waitForTimeout|setTimeout)\(\s*[0-9]|^\+.*retries\s*[:=]\s*[2-9]'
   ```
   Any output fails this criterion.
5. Every closed entry names one of the three exits with its required evidence.
6. Suite flake rate ≤ 1% after the work, measured over a fresh 20 runs.

## Degradation

- **No CI history and no artefact storage** → produce history with the 20-run loop locally;
  label the number `local-measured` and note that CI-specific causes (runner speed, parallelism)
  are not represented.
- **Runner cannot tag or exclude tests** → move quarantined specs to a separate directory
  excluded from the merge-blocking command, and schedule that directory. Same protocol.
- **`superpowers` absent** → use the reduced debugging loop in
  `${CLAUDE_PLUGIN_ROOT}/references/tdd-fallback.md` §"Debugging without superpowers". If it is
  present, delegate step 3 root-causing to `superpowers:systematic-debugging`.
- **Owner unavailable / nobody will take it** → that is a management finding, not a technical
  one. File it as `finding.v1` with `severity: high` and leave the entry overdue and visible
  rather than silently extending the deadline.

## Deliberately not covered

Writing new tests, choosing test levels (`test-plan`), E2E harness design (`e2e-engineer`),
performance regressions that look like flakes but are consistent slowdowns
(`performance-engineer`), and CI runner provisioning.

## Bundled assets

- `scripts/flake-report.mjs` — turns collected CI JUnit XML into per-test flake rates,
  so Step 2 is quantified rather than argued.
  `node scripts/flake-report.mjs <runs-dir> --runs 20`
  Expects `<runs-dir>/<zero-padded-run-id>/*.xml` with an optional
  `meta.json` containing `{"commit": "<sha>"}`. With commit metadata it reports true
  flakiness (the same commit producing both a pass and a fail); without it, it reports
  instability and says so, because a pass/fail split across different commits is a
  regression, not a flake.
  `--test "<id>" --require-clean` exits 0 only when the test was clean for the whole
  window — use it as the machine check for the **fixed** exit in Step 6.
- `references/flake-taxonomy.md` — signature, confirming experiment and fix per cause class.
