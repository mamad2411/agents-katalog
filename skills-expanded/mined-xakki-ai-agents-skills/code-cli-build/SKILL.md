---
name: code-cli-build
description: 'Implement or review command-line behavior: parsing, output, state, operator actions and subprocess results. Use when a command or terminal workflow changes. RU: консольная утилита, CLI.'
license: MIT
disable-model-invocation: true
---

# CLI contracts

Use when a command or terminal workflow changes parsing, output, state, operator actions or external-command results. Trace the real entrypoint from startup and argument parsing to validation, dispatch, process output, exit status, persistence and cleanup. Decide whether the request authorizes implementation or only read-only acceptance.

Honor the actual machine/human output contract and preserve safe, useful failure stages without revealing credentials, untrusted raw values or tracebacks that must remain private. A wrapper or shell quote is not an authorization or injection boundary; validate at the real command before privileged effects. Distinguish help, dry-run, read-only status and mutation modes.

Use [behavior and state](references/behavior-and-state.md) and [subprocess outcomes](references/subprocess-outcomes.md) for the relevant mode. Test invalid arguments and valid controls through the real process or sanctioned fixture, asserting exit, streams, state and absent forbidden effects. Do not invoke production actions merely to test help or error handling.
