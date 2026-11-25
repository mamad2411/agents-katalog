---
name: check-android-lint
description: Runs Android lint, groups the findings by impact and fixes the ones that affect users, crashes or Play Store releases.
disable-model-invocation: true
---

Run and triage Android lint for module: $ARGUMENTS (app if empty).

1. Run `./gradlew :<module>:lintDebug` (use lintRelease when preparing a release). Read the XML at `<module>/build/reports/lint-results-*.xml`, not the console summary.
2. Group issues by severity, then by id. Ignore anything already in lint-baseline.xml.
3. Fix first: Fatal and Error items, plus these warnings when present: MissingPermission, NewApi, ObsoleteSdkInt, HardcodedText on user-facing strings, Overdraw, UnusedResources in large assets, ExportedWithoutPermission, and missing translations.
4. For each fix, make the change in Kotlin, XML or the manifest, and keep it small. Never add a @SuppressLint or edit the baseline to hide an issue without asking.
5. Re-run lint and compare counts before and after.

Report a table: issue id, count, action (fixed, deferred, needs decision) and example file:line. End by asking whether the deferred group should go into the baseline or become tickets.
