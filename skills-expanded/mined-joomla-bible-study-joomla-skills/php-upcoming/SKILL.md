---
name: php-upcoming
description: Check a Joomla extension or PHP project against the next, not-yet-released PHP version by executing its test suite on that PHP with full error reporting — the only method that works, since static analysis has no sniff data for an unreleased version. Use when preparing for an upcoming PHP release or chasing deprecations that PHPCompatibility cannot see. For released PHP versions use php-conservative instead.
---

# Address upcoming PHP version compatibility

You are an experienced PHP developer proactively addressing deprecations in the **upcoming** PHP
version — the one at the top of <https://php.watch/versions>, whose pages cover its new and modified
behaviour.

## The goal

The software must run without warnings or notices from deprecated or obsolete PHP features across
its whole supported range, **including the version that has not shipped yet**.

## Static analysis cannot do this job

Start here, because it determines the entire approach.

**The compatibility sniffs have no data for a PHP version that has not been released.**
PHPCompatibility gains support for a version some time *after* it ships. Worse, it does not validate
`testVersion` — ask it about a version it knows nothing about and it reports **nothing at all**,
which is indistinguishable from a pass.

So the PHPCompatibility sweep (`php-conservative`) cannot answer this question, and a clean run from
it is not evidence of anything here. If that sweep's range had to be clamped below the installed
release's data ceiling, **the clamp names exactly the versions this workflow is about**.

Rector cannot answer it either — it rewrites code *to* a target version, breaking the bottom of the
supported range rather than reporting on it. Ignore any `rector.yaml` in the repository.

**Executing the code on the upcoming PHP is the only real check.** Everything below follows from
that.

## Workflow

### Step 1 — Identify the target version and the gap

Determine the upcoming PHP version from php.watch, and the maximum the project declares in
`composer.json` (`require.php`).

Run the `php-conservative` sweep once to find the installed PHPCompatibility release's sniff-data
ceiling: it names the versions static analysis cannot reach. Confirm the upcoming version is among
them. If the sniffs have since gained support for it, say so — the job is then largely
`php-conservative`'s and this workflow adds little.

### Step 2 — Run the test suite on the upcoming PHP

**If the project has the Dockerised E2E harness** described by the `e2e-tests` skill, use its runner
with a deprecations mode: provision the usual site on an image pinned to the upcoming version (the
`-rc` tag while it is in development), run the whole suite with `error_reporting = E_ALL`, and report
every deprecation, notice, and warning the run provoked **from the project's own code**. Any such
line fails the run — a suite that passes while emitting deprecations has not demonstrated
compatibility. If the harness pins a PHP version for this mode and it names an older release than
the one you are targeting, update it.

**If the project has no such harness**, run whatever suite it does have on an upcoming-PHP container
with `error_reporting = E_ALL` and `log_errors = On`, and read the log. Say plainly in your findings
which code paths that suite does and does not cover — the answer is only as good as the suite.

Two things routinely go wrong here, and both make a run look clean when it is not:

- **The site's `php.ini` may silence `E_DEPRECATED` deliberately**, so notices do not leak into
  response bodies and break tests asserting on what the browser received. Do not simply switch
  `display_errors` on — that breaks the suite. Route diagnostics to a log file outside the web root
  instead.
- **A pre-release PHP image may be broken in ways unrelated to the project** — a missing shared
  library making an extension fail to load, for instance, which then emits a startup warning on every
  request straight into the log you are trying to read. Fix the image before trusting the log.

### Step 3 — Filter the results to the project's own code

A pre-release PHP makes the framework and its bundled dependencies emit enormous numbers of
diagnostics; tens of thousands of lines is normal. Those are real, but they are not this project's to
fix, and reporting them buries the handful that are.

Filter to paths inside the extension or application under test, and keep the unfiltered log for
reference.

### Step 4 — Cover what the suite does not exercise

A test suite only reports deprecations on code paths it actually runs. Read the upcoming version's
deprecation and RFC list on php.watch and check the codebase for the ones that would not surface in a
test run — rarely-taken branches, administrator-only features, error handlers, console commands.

Where a fix would break an already-supported version, gate it on `PHP_VERSION_ID`; if that is not
possible, flag it for manual review.

### Step 5 — Feedback round

The user is a subject matter expert and will evaluate the findings and give further guidance.

### Step 6 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

Re-run the suite on the upcoming PHP after the fixes land and report the result. **A run that reports
nothing from the project's own code is the only thing that closes this out.**

---

*Adapted for this suite from the `php-upcoming` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. Upstream's Step 2 hard-codes one harness's `run.sh
--deprecations` invocation and `.env` variable; here that is described by capability so the workflow
also works on a project with an ordinary test suite. The MIT permission notice accompanies this
adaptation; full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
