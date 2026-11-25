---
name: chat-director
description: Turn a story into a shot list optimized for short GIF animations, stable characters, and cinematic edit points.
---
# Chat Director
Take premise, duration and aspect ratio. Produce numbered shots with durations, frame action, camera, scene description, prop/character bible, audio cues, and cut type. Prefer short shots and one major motion per GIF. State how each shot starts and ends. NEVER pretend an API output has been rendered.

Use schema version 1 from `docs/SCRIPT-FORMAT.md`. Specify the same recognizable
character, screen position, props and camera across related shots, with explicit pose
and action handoffs. `examples/consistent-film.proposed.json` was tested and failed
visual continuity at both joins; describe it as an experiment, not a character-lock
recipe. No paid requests without authorization.

For multi-scene mini cartoons and longer motion-design edits, use the root skill's
`references/storytelling.md` and `references/story-project.md`. Write distinct causal
beats and an explicit character/prop state ledger, then compile the storyboard with
its offline helper. The 14-action lantern example is a plan, not generated footage.
Do not pad a short loop with captions and call it a longer story.
