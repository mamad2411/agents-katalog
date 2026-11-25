---
name: debug
description: Systematic root-cause debugging for any codebase — frontend, backend, libraries, services, CLIs, browser extensions, GitHub apps, data pipelines, infra. Use whenever something is broken, failing, flaky, slow, or behaving unexpectedly - a bug report, stack trace, failing or flaky test, regression, crash, hang, memory leak, wrong output, CI-only failure, production incident, or "works on my machine". Also use when asked to add logs, add console.log or print statements, instrument a code path, or trace execution from A to Z. Replaces guess-and-patch with reproduce, trace, localize, root-cause, minimal fix, and proof.
license: MIT
---

# Debug

A debugging procedure that works the same way in every codebase, because it operates on
**evidence and search space**, not on framework trivia.

The failure mode this exists to prevent: reading a symptom, pattern-matching a plausible
cause, editing code, and declaring victory. That produces fixes that don't hold, fixes for
bugs that were never there, and three new bugs. Follow the phases.

> **If the user asks you to "add logs", "instrument this", "trace the flow", or "put console.log
> everywhere from A to Z" — go straight to `references/trace-first.md` and follow that protocol.**
> It is phase 3 of this procedure done properly: map the path, predict every checkpoint,
> instrument in one pass, then **stop and wait for the output** instead of guessing a fix.

---

## Prime directives

1. **Reproduce before you diagnose. Diagnose before you fix.** No repro means no feedback
   signal, and every subsequent step is guesswork wearing a lab coat.
2. **The bug is where the evidence points, not where it would be convenient.** Your intuition
   is a hypothesis generator, never a conclusion.
3. **One variable at a time.** Change one thing, observe, record. Simultaneous changes destroy
   causality — if it starts working you won't know why, which is barely better than broken.
4. **Binary search beats reading.** Halve the search space — in code, in git history, in the
   input, in the config, in the timeline. Ten halvings cover a thousand candidates.
5. **A root cause explains 100% of the observed evidence.** If your theory doesn't explain
   every detail — including the weird ones you'd rather ignore — it is incomplete, not close.
6. **Prove the fix by toggling it.** Revert the fix, watch the bug return; reapply it, watch it
   go. Anything less and you may have fixed nothing, or fixed it by accident.
7. **Never suppress a symptom you don't understand.** Empty `catch` blocks, `try/except: pass`,
   retries, `?.` chains, timeout bumps, and `# type: ignore` are how a small bug becomes a
   silent one that resurfaces later, further from its cause.
8. **State what you know vs. what you assume.** Label every claim `[observed]`, `[inferred]`,
   or `[assumed]`. Most long debugging sessions are one unexamined `[assumed]` wearing an
   `[observed]` badge.

---

## The six phases

Work them in order. Skipping ahead is the most common cause of a long session.

### 1. Reproduce

Goal: a **deterministic, minimal, fast** command that shows the failure.

- Restate the bug precisely: expected vs. actual, exact input, exact environment.
  Vague reports ("login is broken") get pinned down before anything else — *which* user,
  *which* step, *what* did the screen/log actually say.
- Get it failing **locally and on demand**. If it only fails in CI/staging/prod, that
  environment difference is now your primary lead → `references/heisenbugs.md`.
- Shrink it: fewest steps, smallest input, fastest loop. A 2-second repro lets you run 50
  experiments; a 5-minute one lets you run 6, and you will start guessing to save time.
- Record the exact repro command in your notes. You will run it dozens of times.

If you cannot reproduce it after a genuine attempt, **say so and switch strategy** — go to
logs/telemetry from the real failure, or add instrumentation and wait for a recurrence. Do
not "fix" an unreproduced bug on spec; that is a guess with extra steps.

### 2. Observe

Collect evidence. **Resist all theorizing until you've looked.**

- Read the **entire** error output, not the first line. Stack traces are read bottom-up to
  find the deepest frame *you own* — that is usually where the truth is.
- Check the obvious channels before the clever ones: app logs, server logs, browser console,
  network tab, exit codes, `stderr`, CI job output, database state.
- Establish what **actually** ran: correct branch, correct build, no stale cache, correct
  process, correct config. See the assumption audit below.
- Note anything surprising, even if it seems unrelated. Unrelated weirdness is usually the
  same bug seen from another angle.

### 3. Localize

Narrow "somewhere in this system" to "this function, on this input, in this state."

**Default strategy — trace the whole path in one pass.** If the code can be re-run, don't probe
one spot at a time. Instrument *every* checkpoint from entry to symptom at once, **write down
what each one should print**, run once, and find the first checkpoint where actual ≠ expected.
One round trip instead of eight, and everything upstream of the divergence is proven innocent
for free. Number the checkpoints (`CP01…CPnn`) so a missing ID instantly shows where execution
stopped. Full protocol, including what to log and how to avoid a useless log flood:
**`references/trace-first.md`** — read it before writing the first log line.

After instrumenting, **stop and hand over the run command.** Do not propose a fix while waiting
for the trace; instrumenting and then guessing anyway wastes the entire technique.

**Fallback — bisect**, when you can't re-run on demand, when the path is unknown or enormous
(do one coarse pass first), or when logging perturbs the bug:

- **Bisect the code path.** Put a checkpoint at the midpoint of the suspected path. Is the
  state correct there? Yes → bug is downstream. No → upstream. Repeat.
- **Bisect history.** If it worked before, `git bisect` finds the commit mechanically — and
  strictly beats tracing here. Automate it: `git bisect run <your repro command>`.
- **Bisect the input.** Delete half the input/config/test data. Still fails? The cause is in
  what remains. Repeat until every remaining byte is load-bearing.
- **Differential debugging.** Compare a working case to a broken one — working env vs. broken
  env, passing input vs. failing input, last good release vs. current. Diff them, and the list
  of differences is your suspect list.
- Full technique catalog with commands: `references/techniques.md`.
  How to place probes without lying to yourself: `references/instrumentation.md`.

Do not leave this phase until you can point at a specific line/condition and say
"the wrong thing happens **here**."

### 4. Explain

Write the causal chain, root cause → symptom, in plain language:

> `parseConfig` returns `undefined` when the file has a BOM → `config.timeout` is `undefined`
> → `setTimeout(fn, undefined)` fires immediately → the retry loop spins → the API rate-limits
> us → users see a 429 page.

Then check it: does this explain *every* observed fact, including that it only happens on
Tuesdays, or only for one customer? If some evidence is unexplained, you have found *a* bug,
possibly not *the* bug. Keep going.

**Ask "why" until you hit something worth fixing.** The null check that crashes is rarely the
root cause; *why was it null* is. Stop when the next "why" leaves the code you control.

### 5. Fix

- Fix at the **root**, at the right layer. If bad data enters at the boundary, validate at the
  boundary — don't defend against it in fifteen call sites.
- **Minimal and targeted.** No opportunistic refactors, renames, or reformatting in a bug fix;
  they hide the one line that matters and make revert dangerous. Note them separately.
- Match the surrounding code's conventions, error handling, and logging style.
- Consider blast radius: what else calls this? What relied on the old (wrong) behavior?
- If the correct fix is large or risky, say so and offer the options — a scoped mitigation
  now plus the real fix tracked, or the real fix directly. That is the user's call, not yours.

### 6. Prove

A fix is not done because the code looks right.

- Run the original repro. It must pass.
- **Toggle test:** revert the fix → bug returns; reapply → bug gone. This is the single
  highest-value step and it takes 30 seconds.
- **Write a regression test** that fails without the fix and passes with it. Verify it fails
  on the old code — a test that passes both ways tests nothing.
- Run the broader suite / typecheck / lint for collateral damage.
- **Hunt siblings:** grep for the same mistake elsewhere. Bugs of a kind travel in packs.
- **Remove your instrumentation** — debug logs, prints, hardcoded values, commented-out code,
  loosened timeouts, disabled tests. Then diff your changes and read them line by line.

---

## The hypothesis ledger

Keep this in your working notes (in-context, or a scratch file for long sessions). It is the
difference between debugging and flailing, and it makes handoff to a human trivial.

```
BUG: <one line: expected vs actual>
REPRO: <exact command / steps>            STATUS: reliable | intermittent (n/10) | none

FACTS [observed]
- <evidence with source: log line, stack frame, test output>

H1: <hypothesis>  → predicts: <what I'd see if true>
    TEST: <the cheapest experiment that discriminates>
    RESULT: refuted — <what I actually saw>
H2: ...
    RESULT: CONFIRMED — <evidence>

RULED OUT: <things proven innocent, so nobody re-checks them>
ROOT CAUSE: <causal chain>
```

Rules: prefer the hypothesis whose test is **cheapest and most discriminating**, not the one
that's most likely. Design tests to *refute*, not confirm — a test that "passes" for three
different reasons taught you nothing. And record refutations; re-checking a ruled-out theory
at hour three is a rite of passage worth skipping.

---

## Assumption audit — run this when stuck

After **three refuted hypotheses**, stop generating a fourth. The problem is usually a false
premise, not a missing idea. Interrogate the foundations:

- Am I running the code I think I am? *(add a deliberate crash/log at the top — does it fire?)*
- Is the build fresh? Any stale cache, dist artifact, `node_modules`, `__pycache__`, Docker
  layer, service worker, CDN copy, or hot-reload that silently didn't reload?
- Right branch, right commit, right file? *(uncommitted changes? a shadowing duplicate file?)*
- Right process/instance/port/container/region? Am I reading logs from the box that failed?
- Right environment and config? Which `.env` actually loaded? Is the env var set where the
  *process* can see it, or only in my shell?
- Is the error even from my code — or from a dependency, proxy, browser extension, or the
  platform?
- Is the **test** wrong? Is it asserting the wrong thing, or passing for the wrong reason?
- Did I misread the requirement — is this behavior actually correct?
- Has this dependency/API/schema changed under me? *(lockfile diff, changelog, deprecation)*

Then: re-read the error message literally, word for word. Explain the failure out loud to
someone (or to the user) — most people find the bug mid-sentence.

**Escalate rather than thrash.** If you're past ~6 refuted hypotheses or repeating experiments,
report: what's confirmed, what's ruled out, the top remaining hypotheses, and what you need
(access, logs, a repro, a decision). Continuing to guess wastes the user's money and trust.

---

## Symptom → first move

| Symptom | First move |
|---|---|
| Stack trace / exception | Read it whole, bottom-up; find the deepest frame you own |
| Wrong value | Trace the value *backwards* to where it was born, not forwards |
| Nothing happens at all | Prove the code runs — canary log at entry; check wiring/registration |
| Worked yesterday | `git bisect run <repro>` |
| Works locally, fails in CI | Diff the environments (versions, env vars, TZ, locale, FS, network, parallelism) |
| Intermittent / flaky | Loop it to get a failure rate; suspect order, time, concurrency, shared state → `references/heisenbugs.md` |
| Hang / timeout / deadlock | Dump stacks of the *stuck* process; find who holds the lock or awaits what |
| Slow | Measure first — profile, never guess. The bottleneck is somewhere boring |
| Memory growth | Heap snapshot diff over time; find what retains the biggest set |
| Crash / segfault / OOM-kill | Core dump, sanitizers, `dmesg`/exit code; check the boundary layer |
| Only for one user/tenant | Diff their data and permissions against a working one |
| Silent wrong output | Assert invariants at each stage to find where truth was lost |
| Works in isolation, fails in the suite | Shared state, ordering, leaked globals, unclosed resources |

---

## Stack-specific playbooks

Load only what matches the codebase in front of you.

| File | Covers |
|---|---|
| `references/stacks/frontend.md` | Browser/UI/SPA: rendering, state, hydration, events, CSS, network, mobile web |
| `references/stacks/backend.md` | Servers/APIs/services: HTTP, DB, auth, caching, queues, deploys, prod incidents |
| `references/stacks/library.md` | Packages/SDKs consumed by others: build/publish, types, versions, "works for me" |
| `references/stacks/browser-extension.md` | Chrome/Firefox extensions: MV3 service workers, content scripts, messaging, permissions |
| `references/stacks/github-app.md` | GitHub apps/bots/webhooks/Actions: delivery, auth tokens, permissions, CI |
| `references/stacks/cli.md` | CLIs, scripts, jobs: args, stdio, exit codes, PATH, cron, packaging |
| `references/stacks/data.md` | Pipelines/ETL/ML: schema drift, nulls, silent corruption, nondeterminism |
| `references/stacks/mobile-desktop.md` | iOS/Android/Electron/desktop: lifecycle, permissions, native bridges, release-only bugs |

Cross-cutting:

| File | Covers |
|---|---|
| `references/trace-first.md` | **Full-path instrumentation in one pass** — the default way to localize. Read it whenever you're about to add log statements, or the user asks for logs/tracing |
| `references/techniques.md` | Bisection, delta minimization, differential debugging, tracing back from the symptom |
| `references/instrumentation.md` | Logging that pays off, debuggers, tracing, profilers, snapshots — and cleanup |
| `references/heisenbugs.md` | Flaky, racy, timing-, order- and environment-dependent bugs |
| `references/postmortem.md` | Regression tests, sibling bugs, blast radius, and the write-up |

---

## Working with the human

- Report findings **as you go** if the session is long — a confirmed fact is worth sharing
  before the whole thing is solved.
- Be honest about confidence. "This is confirmed by the log line at X" and "this is my best
  guess, unverified" are different sentences. Never merge them.
- If it turns out the code is correct and the *expectation* was wrong, say that plainly.
- If you fixed the reported symptom but found a deeper problem, report both; don't silently
  expand the scope of your changes.

**Closing report:**

```
ROOT CAUSE   <one or two sentences, the causal chain>
EVIDENCE     <what proves it — the log line, the bisect result, the toggle test>
FIX          <file:line, what changed and why it's at the right layer>
VERIFIED     <repro now passes; toggle test done; regression test added at file:line; suite green>
NOT FIXED    <anything out of scope, related bugs found, follow-ups worth filing>
```
