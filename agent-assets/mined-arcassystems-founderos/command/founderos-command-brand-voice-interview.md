---
description: Capture a brand's voice and positioning. Different from voice-interview, which is for the operator's personal voice. One run per brand.
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob"]
---

Read `skills/brand-voice-interview/SKILL.md` and run it.

The skill captures a single brand's voice and positioning. Output is two files under `brands/<slug>/`: `voice.yml` and `positioning.yml`.

If the user has not run `voice-interview` (personal voice at `core/voice-profile.yml`) yet, do not block - brand voice is independent of personal voice. The two layers serve different purposes.

If `brands/` does not exist yet, create it.

If a brand profile already exists at the slug the user names, ask whether to update specific fields or start over before overwriting.
