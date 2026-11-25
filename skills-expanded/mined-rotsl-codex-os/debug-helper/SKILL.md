# Debug Helper Plugin

## Purpose
Resolve failures through reproducible root-cause analysis.

## Use When
- runtime errors appear
- tests fail
- behavior regresses unexpectedly

## Rules
- reproduce before patching
- isolate root cause before changing code
- apply minimal targeted fixes
- verify the fix with a concrete check

## Output
- observed error
- likely cause
- fix steps
- verification steps

## Constraints
- avoid speculative broad changes
- keep fixes testable and bounded
