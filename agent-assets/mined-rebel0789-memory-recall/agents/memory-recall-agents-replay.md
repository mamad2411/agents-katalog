# Replay and Learning Instructions

- Replays disable external side effects by construction.
- A replay never reuses an approval for a consequential action.
- Compare recorded inputs and version fingerprints before interpreting outcomes.
- Learning proposals are diffs with evidence, tests, rollout, and rollback—not automatic mutations.
