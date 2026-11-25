---
name: debugging
description: Systematically diagnose and fix bugs using reproduction, isolation, root-cause analysis, and verification.
category: development
aliases:
- debug
- fix-bug
- troubleshoot
- diagnose
triggers:
- this isn't working
- help me debug
- find the bug
- why is this failing
- I have a bug
- something is broken
- trace this error
keywords:
- debug
- bug
- error
- fail
- fix
- trace
- exception
- stack
- traceback
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- bug
- debug
- debugging
- development
- error
- fail
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: write
credential_access: false
destructive_operations: false
---

# Debugging

## Purpose

Move from "this is broken" to a verified fix via structured debugging: reproduce, isolate,
form a hypothesis, test it, and verify.

## When to Use

- Code does not behave as expected
- An error or exception is raised
- Behavior is inconsistent or intermittent
- User asks "why is this failing?"

## When NOT to Use

- The issue is actually a design flaw, not a bug (route to `architecture` or `refactoring`)
- The user wants a security review (route to `secure-coding`)

## Capabilities

- Read stack traces and error messages
- Form and test hypotheses
- Use print/log debugging, debuggers, and bisection
- Suggest minimal reproductions
- Recommend tests to lock in the fix

## Inputs

- The failing code or traceback
- Expected vs actual behavior
- Steps to reproduce

## Workflow

1. **Reproduce.** Get a minimal, reliable reproduction. If you can't reproduce, you can't fix.
2. **Read the error.** Don't skim. Read the message, the type, the stack.
3. **Form a hypothesis.** Why might this happen? Write it down.
4. **Test it cheaply.** Use print, logs, debugger, or a small script. Don't guess 10 changes.
5. **Fix at root cause.** Not the symptom. If you're patching a symptom, name it and ask why the symptom exists.
6. **Verify.** Re-run reproduction, then run the broader test suite.
7. **Add a regression test.** So this exact bug doesn't return.

## Tools

- Language debugger
- Logging / print
- Bisect / git bisect
- Minimal reproduction script

## Examples

**User:** "Why is this Python code raising KeyError?"
**Response:** "Read the traceback top-down. Note the exact line. Hypothesis: key missing in dict. Test: print `dict.keys()` before access. Fix: use `.get()` or guard the access. Add a test for the missing-key case."

## Safety

- Don't change code without understanding it
- Don't add try/except to swallow errors silently

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `coding` (writing fix)
- `testing` (regression test)
- `code-review` (after fix)