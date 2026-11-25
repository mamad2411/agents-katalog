---
name: "reference-noise"
description: "Use this skill when Codex needs to verify SkillForge ignores placeholder words and external URLs while checking references."
---

# Reference Noise

This skill mentions placeholder values like `url`, `title`, and `path`.

External links should not be checked:

- [OpenAI](https://openai.com/)
- [Mail](mailto:test@example.com)
- [Anchor](#local-heading)

Non-file examples should not fail:

- Use the value `url` from the response.
- Replace `path` with your install folder.
