---
name: pattern-teacher
description: Teaches which shell commands must never reach an agent unreviewed. Use when reviewing a script before running it, when a command looks destructive, or when the user asks what makes an instruction dangerous.
---

# Pattern teacher

1. Read the script and mark every line that matches one of the patterns below.
2. For each mark, name the file and the line; stop when every match is either
   accounted for or removed.

## The patterns

<!--
The patterns themselves, and the line-scoped `sqs-allow` that waives each one, are
appended by tests/run_tests.py. What this case tests is the three suppression scopes,
and they are tested against strings assembled at run time - see the note in the
malicious fixture for why nothing attack-shaped is checked in.
-->

## When to open which reference

[catalogue.md](references/catalogue.md) holds the full pattern list with one example
each. Open it when a line matches nothing here.
