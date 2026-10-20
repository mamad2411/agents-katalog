Find and fix all failing tests in the project:

1. Identify the test framework being used
2. Run all tests and capture failures
3. Fix each failing test while preserving its original intent
4. Re-run tests to verify all pass
5. Report what was fixed and why

If $ARGUMENTS is provided, focus on tests matching that pattern.

Never disable or skip tests unless they're truly obsolete. Always preserve test intent.