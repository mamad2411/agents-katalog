---
name: flutter-ci-debugging
description: >-
  Diagnose Flutter CI builds that fail, stall or get killed on GitHub Actions, without burning CI
  runs on guesses. Read the evidence with gh, classify the failure signature, size Gradle for the
  runner, and check whether Jetifier can be turned off. Use when the user says "the CI build
  failed", "runner shutdown signal", "exit code 143", "Java heap space", "JetifyTransform",
  "No space left on device", "job exceeded the maximum execution time", "gradle cache is not
  found", or "why is Android CI slow". Not for setting up a pipeline from scratch.
---

# Flutter CI debugging

For a Flutter app whose Android (or monorepo matrix) build on GitHub-hosted runners fails, stalls to
a timeout or is killed. The rule that saves the most time: every guessed change costs a full CI run,
so read the evidence and measure before changing anything.

It does not create pipelines (the upstream `flutter-cicd` skill covers that; without it, write the
workflow by hand), and it does not change workflow files, `gradle.properties` or secrets without
asking.

## Steps

1. **Read the evidence, read-only.** Get the failing job and step, its annotations, and where the
   output stopped, using the `gh` commands in
   [references/android-ci-troubleshooting.md](references/android-ci-troubleshooting.md#read-the-failure-signature-before-changing-anything).
   If the log is gone (`BlobNotFound`), use the job page with timestamps. Do not re-run the job yet.
2. **Know the machine.** Check the repo's visibility (`gh repo view --json visibility`): a private
   repo's `ubuntu-latest` has 2 CPUs, 8 GB RAM and 14 GB disk; a public repo's has 4 and 16 GB.
3. **Classify the signature** with the table in the reference: disk full, runner killed (exit 143),
   silent stall to timeout, `Java heap space` in `JetifyTransform`, or a cache that never saves.
   Say which one it is and which line of the log shows it.
4. **Check the docs and known issues** for the exact error text before proposing a fix: runner
   specs, the tool's own checks (`checkJetifier`), the project's issue tracker.
5. **Measure locally, for free.** Follow "Measure locally before pushing" in the reference. It
   changes `~/.gradle/gradle.properties` and kills Gradle daemons on the user's machine: say so,
   back the file up first, ask, and restore it afterwards.
6. **Push one change that both fixes and measures** (for example Gradle sized for the runner plus a
   temporary memory monitor), ask before pushing it, and remove the instrumentation once green.
7. **Verification and report.** Give the run id of the green build, the before and after evidence
   (peak memory, duration, the signature that disappeared), confirm the temporary monitor and local
   Gradle changes are removed, and list anything you could not check.

## Rules

- **Never raise `timeout-minutes` to fix a stall.** A silent stall is usually memory pressure; a
  longer timeout only burns more minutes.
- **Never give Gradle or the Kotlin daemon an `-Xmx` near the runner's total RAM.** Flutter's
  template ships `-Xmx8G`, sized for a developer machine.
- **Prefer turning Jetifier off over raising heap for it**, but only after `:app:checkJetifier`
  reports no legacy support libraries for that app.
- **CI-only settings go in the workflow**, written to `~/.gradle/gradle.properties` on the runner,
  so local builds keep their own.
- **Read-only first.** `gh run view`, `gh api` reads and local measurement are free; edits to
  workflows, pushes and re-runs need the user's yes.
- **The "free disk space" snippet deletes tools from the runner image.** Use it in a workflow only;
  never run it on a developer machine.
- **Never delete `~/.gradle` or caches** to "start clean" without asking; say what it costs.
