---
name: security-review
description: Dedicated SECURITY review or audit of a component, module, service or design — threat surface, authz, secrets, dependencies, input handling — via the security-engineer role, recorded as a review handoff. Use whenever the request is about security, however deep — is this secure, find vulnerabilities, audit for security, threat-model a flow. A general deep audit for bugs or gaps is deep-review; a routine diff review is code-review.
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
---

# Security review (phase workflow)

A dedicated, deeper security pass over a whole target — a component, a design, or a change —
distinct from the per-diff security aspect inside `code-review`. It delegates the security
judgement to the [`security-engineer`](../../agents/security-engineer.md) role and records a
`review` handoff (security lens): findings with severity, location, and fix, aggregated into one
verdict. (Design: `docs/architecture/quality-ops.md` in the agentic-forge repository.)

## When to use

When the task is a deep, whole-target security audit or threat model — "is this secure?", "audit
this for vulnerabilities", "threat-model X". **Not** the inline security aspect of a routine
change review (`code-review` already runs `security-engineer` per diff), implementing fixes
(`develop`), or releasing (`release`).

## Process

1. **Scope the target.** Identify what is under review (component / design / change) and gather it
   — source, dependency manifest, the relevant config — plus the trust boundaries and entry points.
2. **Delegate the review.** Fork the `security-engineer` role (via `Task`) with the target and the
   threat surface to examine: input validation, authz/authn, injection, secrets handling,
   dependency risk, unsafe deserialization. The role brings the security expertise.
3. **Aggregate into a verdict.** Collect findings into a `review` handoff (frontmatter `type`
   (= `review`), `target`, `iteration`, `verdict`, `findings` with `severity`/`location`/`suggestion`),
   then validate it (the read-back below; see
   [handoff.md](../../patterns/handoff.md)). Any `blocker`/`major` finding makes the verdict
   `changes`; otherwise `approve`.
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type review` — and fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
4. **Report, don't fix.** Surface findings with concrete locations and remediations; do not modify
   code. Do not invent vulnerabilities on safe code — an approve with at most nits is a valid result.

## Output

A `review` handoff (security lens): the verdict plus severity-tagged findings with locations and
fixes. Hand off to `develop` to remediate — its `verdict`/`iteration` fields drive `develop`'s
bounded [review loop](../../patterns/review-loop.md) (the same `review` artifact `code-review`
emits). No files are modified.

## Definition of done

- Real vulnerabilities are flagged with a location, a severity, and a concrete fix.
- The verdict reflects the findings (`changes` if any blocker/major; else `approve`).
- A valid `review` artifact is produced; no code is modified; nothing is invented on safe code.
