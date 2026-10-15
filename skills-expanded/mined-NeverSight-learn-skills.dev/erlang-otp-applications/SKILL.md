---
name: erlang-otp-applications
description: Guide for structuring and reviewing Erlang/OTP applications with `application`, `supervisor`, and `gen_server` behaviours, supervision trees, child specs, restart strategies, and crash/restart semantics. Use when designing, implementing, reviewing, or debugging Erlang services that should follow OTP principles such as process isolation, let-it-crash failure handling, and supervisor-managed recovery.
author: Sean Merriam
version: 1.0
---

# Erlang OTP Applications

## Overview

Use this skill to design or review Erlang systems as OTP applications rather than ad hoc process collections. Prefer small isolated processes, explicit supervision trees, and failure handling that crashes fast on unexpected errors and lets supervisors restore healthy state.

## Workflow

1. Identify the application boundary.
2. Design the supervision tree before filling in worker logic.
3. Assign one clear responsibility to each process.
4. Choose restart semantics and shutdown behavior deliberately.
5. Keep business logic separate from OTP callback glue.
6. Start from the bundled template when creating a new service.

## Application Shape

Model the system in this order:

1. `application` callback module: start the top-level supervisor only.
2. Top-level supervisor: own the stable root children.
3. Domain supervisors: group related workers that fail or restart together.
4. Worker processes: use `gen_server` only when a long-lived stateful process is needed.
5. Pure modules: keep calculations, validation, and transformations outside OTP behaviours when they do not need process state.

Read [references/structure.md](references/structure.md) when deciding how to break a service into supervisors, workers, registries, or helper modules.

## Failure Model

Assume unexpected errors should crash the current process. Do not bury faults behind catch-all error handling unless the failure is expected and part of the module contract.

Use supervisors to recover:

- Choose `one_for_one` when children are largely independent.
- Choose `rest_for_one` when later children depend on earlier ones.
- Choose `one_for_all` only when the whole sibling group must restart together.
- Use `permanent`, `transient`, and `temporary` child restart modes to express process intent.

Read [references/failure-model.md](references/failure-model.md) when deciding how processes should fail, restart, shut down, or escalate errors.

## Worker Selection Rules

Prefer:

- `gen_server` for stateful request/response services, resource ownership, and serialized access to mutable process state.
- `supervisor` for restart policy and child lifecycle management.
- Plain modules for pure logic.
- Short-lived spawned processes only when they have a clear lifecycle and supervision story.

Avoid:

- One large `gen_server` that owns unrelated responsibilities.
- Supervisors containing business logic.
- Swallowing exceptions and returning `{error, Reason}` for programmer bugs.
- Using process state as a substitute for clean module boundaries.

## New Service Bootstrap

Use the starter template in [assets/rebar3-otp-template](assets/rebar3-otp-template) for new services. It provides:

- `rebar.config`
- `.app.src`
- application callback module
- root supervisor
- sample `gen_server` worker

To materialize a copy with your application name, run:

```bash
python3 scripts/scaffold_rebar3_otp_app.py my_app /tmp/my_app
```

The script copies the template and rewrites `myapp` placeholders in file names and file contents.

## Output Expectations

When using this skill for implementation or review:

- Show the proposed supervision tree.
- Name each process and its single responsibility.
- State the chosen restart strategy and why.
- State what should crash versus what should return tagged errors.
- Keep OTP callbacks thin and move domain logic into plain modules.
