---
name: "build-verification-audit"
description: "Verify that a build actually does what the agent claimed, before calling it done. Use when a build, app, feature, or workflow is wrapping up, when {{USER}} asks to audit or \"actually check\" something built with an AI agent, or at the natural end of any coding/build run — especially SBDC or client-facing tools. Triggers on \"audit this build\", \"did Claude actually do it\", \"verify this works\", \"is this production-ready\", \"check the auth/tests\", or end of a build run."
---

# Build Verification Audit

At the end of a build run — or whenever {{USER}} asks to verify something built with an AI agent — do not trust the building session's own report that the work is done. An AI agent produces the *plausible* next action, not a *verified* one; "I added authentication" is the likely sentence to emit after that task, not evidence the auth exists. This skill re-derives evidence and checks it against what was actually asked for.

This is the sibling to the Durable Learning Protocol: same "end of run" hook, same ledger, but it verifies the build instead of consolidating learnings. Run it before declaring a build production-ready, especially for SBDC or anything that touches real client data.

## The Core Rule

**Verification must sit outside the system that produced the work.** Never satisfy this audit by asking the building session "did you do it?" — it will say yes. Re-derive the evidence independently: run the app and walk the flow, read the actual code and tests yourself, or spawn a separate subagent to check. If none of those are possible in-session, say so plainly and mark the item unverified rather than passing it.

## The Contract Frame

Audit each deliverable against four questions. Treat the agent as an untrusted contractor bound by a contract.

1. **Agreed delivery** — What exactly was this supposed to do? If the spec was one big blob, break it into the discrete behaviors that were promised.
2. **Constraints** — What was it told *not* to do (don't store PII in plaintext, don't touch payment logic, don't fake tests)? Check these as hard as the delivery — how something was built often matters as much as whether it works.
3. **Proof** — Is there a concrete artifact showing the behavior working in the live app (a walked-through flow, a screenshot, real output) — not just a claim in prose?
4. **Verification** — Was that proof checked independently, outside the building agent? (See Core Rule.)
5. **Ownership** — Is this a task an agent could actually complete, or one only a human can (needs access the agent lacks, real credentials, a real send)? Human-owned items can't be marked done by the agent — flag them for {{USER}}.

## The Standing Failure Checklist

These are the failures that recur in AI-built apps. Check every one that applies; do not assume any is fine because the agent said so.

- **Auth that doesn't authenticate.** Can you register with an email you don't own? Is there real verification that the email/identity belongs to the user? Does password reset actually work end to end?
- **Access control that doesn't control.** Does "suspend" / "remove" / "revoke" actually cut off access? Can one logged-in user reach another user's data?
- **Tests written to pass, not to test.** Read the tests. Do they assert the *intended* behavior, or just whatever the code currently does? A green "100% passing" run proves nothing if the assertions were reverse-engineered from the implementation.
- **Broken non-happy-path workflows.** The demo path works; the edge paths (bad input, empty state, error, back button, refresh mid-flow) were often never exercised.
- **Data handling.** For SBDC/client tools: is any client PII, financial detail, or identifier stored or logged where it shouldn't be? This is a constraint failure and matters most here.

## How To Run It

1. List the deliverables that were promised this run.
2. For each, run the Contract Frame + the relevant Failure Checklist items, re-deriving evidence independently.
3. Report per item: **verified** (with the evidence), **failed** (with what's broken), or **unverified** (couldn't check in-session, and why).
4. Do not call the build done while any critical item — auth, access control, client-data handling — is failed or unverified.

## Logging Findings

Per-build pass/fail is reported in-session, not stored — no new persistent file.

But when the audit surfaces a *recurring trap worth remembering* (a mistake pattern that would help future builds avoid it), record it as a Durable Learning Protocol pitfall. If the `durable-learning-protocol` skill is installed, record each durable finding with `py scripts/learnings.py add --namespace <ns> --key <kebab-key> --insight "..." --type pitfall|pattern|preference|tool|operational --confidence N --usefulness N --source observed --evidence "..."` from the workspace root. Otherwise list the findings at the end of the audit for the user to save.

If write access isn't available, list proposed pitfall learnings at the end for {{USER}} to save.

Example pitfall worth logging: `insight: "AI-built login flows default to no email-ownership verification — always test registering with an email you don't control before shipping."`, `namespace: "sbdc"`, `type: "pitfall"`.
