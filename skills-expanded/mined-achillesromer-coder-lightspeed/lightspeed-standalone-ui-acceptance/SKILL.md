---
name: lightspeed-standalone-ui-acceptance
description: Prove that an installed LightSpeed desktop package opens a responsive local UI while preserving separate source-currentness and release gates.
---

# LightSpeed Standalone UI Acceptance

Use when dependency/import tests are insufficient and the task requires evidence that the installed desktop application actually opens.

This complements `lightspeed-runtime-productization`; it does not replace install/update/config/rollback handling and it does not create another runtime.

## Preconditions

- Record the current Git/provider head separately from installed-package identity.
- Identify the installed executable by path, size, modification time, and SHA-256.
- Check for an already-running LightSpeed desktop session and avoid launching a duplicate over a user-owned session.
- Preserve existing Drive/CGX/Recovery authority boundaries.

## Acceptance workflow

1. Record baseline desktop-shell process identities.
2. Launch the installed executable without exercising application controls.
3. Observe only the newly created desktop-shell processes.
4. Require a responsive LightSpeed window within a bounded timeout.
5. Record executable hash, observed title, responsive state, process topology, installed timestamp, and current Git head.
6. Close only the processes created by the acceptance probe.
7. Write and read back a receipt.

## Result classes

- `PASS_INSTALLED_UI`: exact installed package produced a responsive LightSpeed UI.
- `FAIL_NO_UI`: no responsive UI appeared inside the timeout.
- `HOLD_EXISTING_SESSION`: an existing user-owned LightSpeed UI was already running.
- `PASS_STALE_PACKAGE_ONLY`: UI launch passed but no evidence binds the executable to the current source head.

## Evidence boundary

A local UI pass does not prove the executable was built from the current Git head, clean-machine installability, installer portability, update-channel correctness, signing/notarisation, deployment/public release, semantic authority, or physical/legal/financial/engineering readiness.

Current-source package acceptance requires a build receipt that binds the executable hash to the exact source head plus the relevant packaging/install checks.

## Failure behaviour

Fail closed on a missing executable, ambiguous existing session, unverifiable process ownership, missing hash, timeout, or cleanup failure. Do not terminate unrelated processes and do not bypass release or authority gates.
