---
name: corrupt_skill
version: 1.0.0
license: MIT
---

# corrupt_skill

**TEST FIXTURE — not a real skill.**

This skill is a deliberate trap for gateway robustness testing. The `tool.js`
served at `/skills/corrupt_skill/tool.js` is valid JavaScript, but the
`tool_sha256` declared for this skill in `/llms.txt` is intentionally wrong
(64 zero chars). A conforming gateway MUST detect the hash mismatch and
exclude this skill from discovery / execution.