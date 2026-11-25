---
name: perform-clean-refactors
description: Use when removing, renaming, replacing, consolidating, or refactoring functionality, public or internal APIs, configuration, commands, files, or concepts when the requested change permits removal of the old interface. Enforces direct deletion and simplification, removal of obsolete callers and tests, and a default prohibition on compatibility shims and compatibility aliases. Do not use for ordinary additive feature work or diagnostic-only reviews.
---

# Perform Clean Refactors

## Refactor Directly

1. Confirm the requested end state. Inspect all references to the old functionality.
2. Remove or replace the old implementation completely, including obsolete callers, exports, configuration, documentation, fixtures, and tests.
3. Do not implement compatibility shims, compatibility aliases, deprecated forwarding paths, dual names, or silent fallbacks unless the user explicitly requests backward compatibility.
4. Use one clear concept and code path after the refactor.
5. Preserve tests for behavior that remains. Update tests affected by the new design.
6. Delete tests for removed behavior. Do not add tests whose sole purpose is proving that a removed symbol, command, file, or behavior no longer exists.
7. Run the repository's relevant validation. Report each intentional breaking change.

If an applicable repository policy explicitly requires backward compatibility and the user has not resolved that conflict, stop before you add a compatibility shim. Ask for direction.
