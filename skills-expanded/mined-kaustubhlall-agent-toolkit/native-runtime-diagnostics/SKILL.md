---
name: native-runtime-diagnostics
description: Diagnose native crashes or deadlocks, loaded-code mismatches, and PyTorch CUDA, OOM or non-finite failures with matched artifacts and bounded runtime observations. Not generic bug fixes or benchmark acceptance.
license: CC-BY-SA-4.0
metadata:
  origin: local-adaptation
  upstream: stas00/the-art-of-debugging
---

# Native runtime diagnostics

Identify the actual process, executable/interpreter, loaded module, build/symbol
identity and environment before interpreting a trace. Use the project's current
runtime records and the smallest discriminating observation. A stale binary,
wrong Python import or mismatched symbols can mimic a source defect.

| Symptom | Useful first observation |
|---|---|
| Native crash or extension fault | Matching executable/core and symbol identity, crash stack and other-thread stacks |
| Hang or deadlock | Time-correlated thread stacks and waits; distinguish useful idle from a blocked critical path |
| Edits have no effect | Running binary/module path, interpreter and loaded-code identity |
| Async CUDA error | A small synchronized diagnostic reproduction; preserve the original async evidence |
| OOM | Allocation timeline and operation phase, device/process identity, live versus reserved/retained memory |
| NaN/Inf or wrong numeric result | First non-finite boundary, dtype/range, forward/loss/backward/optimizer stages |

Read [recipes](references/recipes.md) for the matching domain. Choose native
Windows tools for a Windows process and Linux tools for the verified Linux/WSL
target. A host/guest observation does not prove the other's state. An unavailable
debugger/profiler is a reported limit, not permission to install a service or
weaken tracing restrictions.

Prefer existing crash artifacts or a disposable short reproduction. Pin identity
and change one relevant variable. Synchronous mode can mask a timing race; CPU
fallback can change numerical/backend behavior. Re-widen only as the authorized
task requires. Attaching can pause a process, snapshots write memory-bearing
files, and tracing can perturb timing; scope duration, target and output paths.
Preserve existing authorization for live observations without asking again, but
do not alter host-wide kernel/ptrace/security settings or create disruptive load
merely to obtain a trace. Keep memory artifacts private and task-owned.

Report observations with commands, identities and timestamps, the supported
cause or remaining alternatives, and a discriminating next check. Unresolved
frames remain unresolved. A trace, successful transport or synthetic reproduction
does not establish live acceptance. For measured CPU/backend optimization use
`performance-engineering`; for experiment validity use `experiment-cycle` or
`scientific-critical-thinking` when applicable.

Adapted from Stas Bekman's [The Art of Debugging](references/source.md), with
Windows/WSL scope, matched-artifact checks, bounded output and permission-safe
recipes. The adaptation is CC BY-SA 4.0; the license and attribution are retained.
