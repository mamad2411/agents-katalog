---
name: agent-browser-policy
description: Apply consent, secret-safe authorized login, session ownership, profile, CDP, and harness-versus-CLI boundaries whenever agent-browser is used, including test-persona reauthentication.
compatibility: Supplements the installed agent-browser core skill; it does not replace it.
---

# agent-browser policy

## Consent and privacy

- An explicit agent-browser request authorizes the managed Chromium runtime. Confirm immediately before externally visible or account-affecting actions not already explicitly authorized. Ordinary inspection, navigation, snapshots, and reads need no repeated confirmation. Authorized login follows the rule below.
- Explicit authorization to use an existing test persona permits login and reauthentication to the named application/environment during that task. Prefer a configured credential provider or existing auth profile. If unavailable, a repo-maintained credential reference may be consumed by a bounded local helper and entered into the verified login form. Do not provision a duplicate account because a session expired.
- The helper must keep credential values out of model/tool output, shell history, tracing, logs, reports and tracked artifacts. Use structured subprocess arguments rather than shell interpolation, suppress output and sanitized failure reporting, and minimize secret lifetime. Raw command arguments can be visible to local processes: use a supported stdin/provider mechanism where available, otherwise use only a trusted local execution environment. Never print source lines or exceptions containing credentials. Record credential references and successful identity checks, not values.
- Recheck origin before credential entry and authenticated identity, role and tenant/event afterward. Stop on unexpected redirects, login failure, MFA or a profile/membership gate. Login authorization does not approve account creation, password resets, privilege changes, onboarding writes or operational mutations.
- Never export or report passwords, cookies, tokens, one-time codes, recovery codes or local-storage credentials. Do not extract browser cookies or private session storage to bypass login. Access to shared cookies remains limited to an explicitly approved upstream mechanism.
- Treat an existing private profile as sensitive. Load a user-approved private context path only when the user names or approves the exact path. Do not copy, migrate, or expose profile data.

## Runtime boundaries

- The CLI and a harness-provided browser are separate tools. Report CLI evidence separately from harness evidence. Do not translate one tool's profile or target controls into the other.
- Use Firefox defaults only through the environment's browser provider. An explicit agent-browser CLI Chromium target, profile, or executable requires approval only when it is external to agent-browser's managed runtime.
- Use `--cdp` only with an explicitly approved endpoint. Never probe ports or attach to an unapproved browser.
- When several sessions share CDP, pass `--pin-tab` so each session remains bound to its own tab. Do not use shared-cookie state unless the user explicitly requests the supported upstream feature and its handling remains secret-safe.

## Profiles and sessions

- Before loading a private profile, verify the approved path is an existing directory owned by the same user. Do not create missing profile directories.
- A profile lock means another browser may be using the profile. Stop and report it, or wait for the owner to close it. Never delete lock files.
- A profile may open as a temporary snapshot and appear signed out. Treat that as a runtime limitation, not evidence that the source profile is logged out. Never extract cookies to diagnose it.
- Derive a task-unique session prefix, then create one stable named session and reuse it. Never use the unnamed shared session.
- Cleanup means closing only sessions, tabs, and temporary profiles created by this task. For an attached browser, detach the owned automation and close only owned tabs. Keep the human-owned browser process alive. Do not close, delete, or alter another agent's or the user's browser state.

## Completion

Preserved host-specific context belongs in a user-selected private path outside the repository. Report that path, never its contents, when preservation provenance matters. Load it only as private context, not as portable instructions.

Report the runtime, owned session, visible result, confirmation points, and limitations. Omit private profile contents and all secrets. If the CLI, skill, approved endpoint, private context, or confirmation is unavailable, stop and report the boundary instead of guessing or launching a browser.
