# Skill: Spec Syncer
**Description**: Updates the agent's internal state when a Markdown specification is modified.
**Triggers**: "/sync", "updated the spec for", "spec changed"

## Instructions
When this skill is triggered, you MUST:
1.  **Diff Analysis**: Compare the current input spec with the previously known `/docs/master-spec.md`, `GEMINI.md`, `001-slice-metadata-definition.md` and `docs/specs/overview.md`.
2.  **Impact Report**: List exactly which Slices (BKP/FRT) are affected by this change.
3.  **Validation**: Check if the change violates any "Hard Rules" defined.

**TERMINAL INSTRUCTION**: "Architecture synced. [List affected Slice IDs]. Ready for implementation update?"