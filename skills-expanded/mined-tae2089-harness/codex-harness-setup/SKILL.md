---
name: codex-harness-setup
description: "Configure the shared tracker and explanation profile before generating a Codex harness, or update those project preferences. Reuses to-spec and to-issues .scratch/.tracker; writes the chosen audience profile and harness policy pointers into AGENTS.md. Does not execute work or publish issues merely because setup was requested."
---

# Codex Harness Setup

Configure project preferences for `codex-harness`. Use the existing shared tracker contract rather than a separate harness publication backend.

## Procedure

1. Read existing AGENTS.md and, when present, `.scratch/.tracker`. Reuse decisions already made in the conversation. Do not inspect credential values or infer a tracker from the Git remote.
2. Load `../codex-harness/references/project-policy.md`. If the companion skill is unavailable, report that dependency before generating an incomplete harness.
3. For tracker setup, locate the installed `to-issues/references/tracker-config.md`, also used by `to-spec`. Use its supported keys and publication-tool rules. If missing, report the dependency; do not invent a replacement configuration.
4. Preserve valid existing tracker settings unless the user requests a change. For a missing configuration, explain the shared local fallback or collect the user's explicit destination. Do not create tickets or publish documents during setup. Issue-free execution does not require a tracker.
5. Reuse the existing explanation profile; otherwise ask for domains and familiarity with suggested beginner/ELI5, practitioner, and specialist options plus free text. Support mixed expertise.
6. Prepare the concrete configuration and AGENTS.md changes, then apply them within the user's authorization and project safety rules. Write only `.scratch/.tracker` when selected and the relevant AGENTS.md sections. Keep the shared configuration trackable. Preserve unrelated content and existing work.
7. Set model and effort preferences from the companion `codex-harness/references/schemas/models.md` during harness generation, not in the tracker. An unavailable model requires an explicit replacement decision.
8. Do not generate a local execution-state engine or a state-management agent. The main Orchestrator records progress on the selected work record and resumes from that record plus actual artifacts. Preserve legacy project files without automatic cleanup.
9. Report changed paths and any missing publication tools or dependencies. Setup success is not a claim that a remote issue or document was created.

## AGENTS.md policy

- Tracker and publication contract: `.scratch/.tracker`, shared with `to-spec` and `to-issues`.
- Ask existing issue / new issue / no issue for actionable work unless already specified.
- One issue per work unit with completion criteria; agent steps and retries stay internal.
- Close issues only on user request.
- Use the selected domain-specific explanation profile; explicit task-level requests take precedence.
- Explanation style does not weaken code quality or verification.
- The main Orchestrator coordinates native Codex subagents; no separate agent-team runtime.

## Validation

- Existing choices and unrelated project instructions are preserved.
- Tracker format matches the installed shared contract; no credentials or extra harness keys.
- No second tracker configuration, per-agent issue mirroring, or automatic closure.
- AGENTS.md contains the selected explanation profile without placeholders.
- No issues, labels, Epics, or documentation pages are created merely by running setup.

## References

- `references/tracker-backends.md` — shared publication dependency and backend behavior
- `references/integration-points.md` — generation and runtime integration
- `templates/harness-tracker.template.md` — shared tracker examples, not a separate output file
