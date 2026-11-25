---
name: adversarial-verification
description: Use when verifying implementation work and the failure mode is superficial approval, code-reading in place of execution, or over-trusting a passing test suite without trying to break the change
---

# Adversarial Verification

## Overview

Your goal is not to confirm the implementation works. Your goal is to try to break it.

This skill follows the built-in verification agent in `src/tools/AgentTool/built-in/verificationAgent.ts` and the coordinator guidance in `src/coordinator/coordinatorMode.ts`.

## Opening Stance

Start from skepticism:

- a passing test suite is context, not proof
- polished UI is not proof
- code review is not proof
- implementer-provided evidence is not enough

Verification begins when you execute the change directly.

## Mandatory Baseline

1. Read the local build and test conventions.
2. Run the build if applicable.
3. Run the test suite if applicable.
4. Run linters or type-checkers if configured.
5. Exercise the changed behavior directly.

Do not stop at step 4. The direct exercise is the whole point.

## Required Adversarial Probe

Every verification pass must include at least one probe aimed at failure, not success:

- concurrency
- boundary values
- idempotency
- malformed input
- missing or orphaned references
- restart or persistence behavior

If all you checked was the happy path, verification is incomplete.

## Rules

- Reading code is not verification. Run it.
- "Tests already pass" is not verification. Verify independently.
- "Looks correct" is not verification. Run it.
- Do not issue PASS without command evidence.
- If a check has no executed command and observed output, it is a skip, not a pass.

## Evidence Format

For each significant check, record:

- what you are verifying
- exact command run
- output observed
- expected versus actual when relevant
- PASS or FAIL

## Common Probes

### API or backend

- parallel requests
- invalid payloads
- duplicate mutation
- nonexistent resource identifiers

### Frontend

- real browser or automation when available
- console errors
- broken subresources
- refresh persistence
- controls that render but do nothing

### CLI

- malformed input
- empty input
- boundary flags
- stdout, stderr, and exit code

## Failure Discipline

Before reporting FAIL, make sure the issue is real and actionable.

Check whether it is:

- already handled elsewhere
- documented as intentional
- impossible to change without breaking a hard external contract

Do not use those checks to excuse real bugs. Use them to avoid false alarms.

## Anti-Patterns

- PASS based on code reading
- PASS based only on unit tests
- PARTIAL because you felt unsure
- re-running only the implementer's happy-path steps
- waving away suspicious output as unrelated without evidence

## Done Condition

You have applied this skill correctly when your verification includes direct execution, at least one adversarial probe, and evidence strong enough that another reviewer could reproduce your conclusion.
