---
name: soul-audit
description: GBrain-inspired identity and cadence setup for Codex. Use when defining the package's identity files, access posture, user context, or operational cadence.
---

# Soul Audit

Use this skill when the user wants to define or update identity, access, user-profile, or cadence files for a Codex package.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain writes `SOUL.md`, `USER.md`, `ACCESS_POLICY.md`, and `HEARTBEAT.md` into a brain-oriented setup. In this repo, the same idea ports cleanly as local config documents when the package needs explicit identity and operational stance.

## Workflow

1. Decide which identity files are needed.
2. Generate them from the user's stated preferences and goals.
3. Keep each file separately editable and re-runnable.
4. Make the resulting cadence and access posture explicit.

## Guardrails

- Do not invent sensitive personal details.
- Keep each generated file grounded in the user's stated preferences.
- Avoid overcomplicating the first pass; the files should be easy to revise.
