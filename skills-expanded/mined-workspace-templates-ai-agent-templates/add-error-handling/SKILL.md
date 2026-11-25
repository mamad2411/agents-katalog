---
name: add-error-handling
description: "Adds real error handling to one function: lists its failure modes, handles each with a clear message and cleans up resources."
disable-model-invocation: true
---

Add error handling to: $ARGUMENTS

1. Locate the function and read it, its callers and its tests. Note how this codebase reports errors already (exceptions, Result types, error codes, HTTP responses) and copy that style.
2. List every failure mode before editing: invalid input, null or missing data, I/O and network errors, timeouts, partial writes, permission problems, and errors thrown by each dependency.
3. For each one decide: recover, retry with a limit, translate into a domain error, or let it propagate. Say which and why.
4. Write messages that name the operation and the offending value, never secrets or full payloads.
5. Make cleanup unconditional (finally, defer, using, context managers).
6. Never add an empty catch or a blanket catch that hides bugs. Do not change the function's successful behavior.

Add a test for each failure mode that can be triggered. Show the failure table and the diff, run the tests, then ask before changing any caller's signature.
