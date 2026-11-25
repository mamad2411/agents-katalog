---
name: e2e-verification
description: "Verifies real functionality across a running application and its relevant services. Use when asked to test a feature end to end, reproduce a user journey, or verify composed behavior beyond mocks."
---

# Verify real functionality end to end

Read AGENTS.md and the repository's docs. They own startup, routes, authentication, synthetic fixtures,
service boundaries and approved browser tooling. Reuse existing tests and tools.

1. **Define the claim.** Read the request and original acceptance criteria.
   Trace each changed behavior through its entry point, real service calls,
   persistence and external effects. Select observable success, relevant failure
   and regression assertions. A UI claim starts in the UI; an API or event claim
   starts at its actual public entry point.
   Complete when every in-scope criterion has an assertion or an explicit gap.
2. **Verify the environment.** Record worktree/revision, dirty state, service
   revisions, endpoints and listener ownership. Use the configured background
   supervisor or the repository's stack lifecycle. Confirm the running web calls the
   intended backend. Reuse approved authentication and synthetic, test-owned data.
   Match actions to existing task authority; customer writes, real messages,
   deletion and external provider effects need their applicable authorization.
3. **Exercise the real path.** Drive actual application controls or requests and
   observe the resulting state at the relevant service boundary. Verify persisted
   changes survive a reload or fresh read when persistence is claimed. For async
   work, observe the worker/consumer outcome, not only request acceptance. Read
   [boundary examples](references/boundaries.md) for browser, event or provider work.
   Any substituted dependency is named; claims stop at that boundary. A passing
   mock suite remains useful separate evidence, not proof of the real path.
4. **Test failures and recovery.** Exercise the selected negative cases with
   existing safe controls. Recheck prior state and absence of unintended effects.
   Record an unavailable case as untested with its reason. Fix in-scope defects
   and rerun affected assertions; preserve existing data and unrelated processes.
5. **Deliver the evidence.** Use [evidence](../evidence/SKILL.md) for revision-specific
   captures and passed/failed/untested assertions. Record actions, observed results,
   real/substituted boundaries and residual gaps. Publish only to the task's
   authorized destination. Functional verification is complete when every selected
   assertion has a result and every claimed boundary was actually exercised.

Use [testing](../testing/SKILL.md) when adding regression tests. A missing fixture
or environment is an explicit verification gap, not a reason to invent a second
harness. Report pre-merge verification separately from deployed verification.
