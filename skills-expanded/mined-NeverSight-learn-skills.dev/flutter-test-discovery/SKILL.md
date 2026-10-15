---
name: flutter-test-discovery
description: Use when `flutter test` runs fewer tests than expected, or a test file seems silently skipped. `flutter test` only discovers files ending in `_test.dart` — `acceptance_tests.dart` is valid Dart but never runs under the default runner. Verify the naming, then the counter.
---

# Flutter test discovery

Ensure every intended test file actually runs. The runner is a **names filter**: only files matching `*_test.dart` are discovered by `flutter test` with no arguments.

## Steps

1. **When the test counter looks low**, list the test directory and check names:
   `ls test/` — any file ending in `_tests.dart` (plural) will be silently skipped.
   Completion: you can name every file and whether it ends in `_test.dart`.
2. **Rename non-conforming files** so the suite is discovered: `mv test/acceptance_tests.dart test/acceptance_test.dart`.
3. **Re-run the full suite** and compare the counter to the expected total. Completion: counter matches; the acceptance file's tests appear in the summary.
4. **Run a single case while debugging** with `flutter test test/<file>_test.dart --plain-name 'TEST-003'`.

## Reference

- Evidence from this project: `flutter test` reported `+14` while 28 tests existed; the 14 acceptance tests in `acceptance_tests.dart` were silently excluded until renamed to `acceptance_test.dart`.
- Per-file runs (`flutter test test/x.dart`) work with any name — the discovery gap only bites the full-suite run.
- If a full-suite run seems too fast, suspect a name, not the tests.
