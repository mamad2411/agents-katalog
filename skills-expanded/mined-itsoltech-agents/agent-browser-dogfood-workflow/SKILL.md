---
name: agent-browser-dogfood-workflow
description: "Test browser user flows, responsive states, or accessibility when broader QA coverage is needed."
---

# Agent Browser Dogfood Workflow

Use this skill to run or plan frontend dogfood with `agent-browser` before QA handoff, after bug fixes, for preview deployments, or when collecting evidence for UI findings.

## Trigger boundary

Use it for scoped black-box coverage of user flows, responsive states, accessibility, preview deployments, or fix verification before QA handoff.

Do not load it for a small local interaction check or one deterministic visible assertion that does not need flow coverage; use the browser directly.

## Process

1. Confirm the session contract: target URL, environment, scope, acceptance criteria, user role, allowed destructive operations, test data, setup and cleanup, deployment identifier, feature flags, and time limit.
2. Before actual `agent-browser` command work, check the installed tool version and available command surface:
   ```bash
   agent-browser --version
   agent-browser --help
   ```
3. If the installed CLI supports versioned local guidance such as `agent-browser skills get core` or `agent-browser skills get dogfood`, load it and prefer that output when syntax differs. Older versions may not provide those commands; in that case use `--help` and the official documentation for the installed version.
4. Treat static command snippets in this skill as patterns, not permanent CLI truth.
5. Create a short test charter and isolated artifact directory before interacting with the app.
6. Run the black-box loop first: observe, state expectation, act like a user, wait for a condition, verify UI behavior, inspect diagnostics when relevant, record coverage, refresh snapshot after state changes.
7. Use diagnostics only after black-box evidence exists. Do not read source code to justify user-visible behavior during the black-box phase.
8. Stop full dogfood if smoke test fails. Record blocker evidence and the untested scope instead of continuing through invalid results.
9. End with a compact handoff: findings with evidence, coverage, blocked areas, unexpected console/network errors, artifact paths, limitations, and recommended regression tests.

## Coordination

Use with UI, accessibility, security, or framework-specific review skills when the dogfood session uncovers implementation risks. Do not use `agent-browser` dogfood as the only quality layer for repeated critical paths; convert stable high-risk findings into deterministic regression tests.

## Reference Routing

- Session contract, charter, artifact layout, current CLI guidance, and safety boundaries: read [01-session-charter-setup.md](./references/01-session-charter-setup.md).
- Black-box model, diagnostics boundary, core interaction loop, and dogfood phases 1-6: read [02-black-box-loop-user-flows.md](./references/02-black-box-loop-user-flows.md).
- Responsive checks, accessibility checks, cache behavior, optimistic updates, and live events: read [03-viewports-accessibility-cache-live.md](./references/03-viewports-accessibility-cache-live.md).

## Command Version Policy

- Before command work, run `agent-browser --version` and `agent-browser --help` to confirm the installed command surface.
- If the installed CLI supports versioned local guidance such as `agent-browser skills get core` or `agent-browser skills get dogfood`, load it and prefer that output when syntax, flags, output paths, or behavior differ. Older versions may not provide those commands.
- Treat command snippets here as patterns.
- Record the `agent-browser` version in session metadata and do not update the tool during an active session.
