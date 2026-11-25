---
name: script-release-probe
description: Run an isolated release-component probe and report only its observed evidence.
---

# Release probe

Use `scripts/release_probe.py` through the available Skill script execution
Action. Pass `--release` and `--component` arguments from the task. The script
prints one JSON object containing the supplied values, a fresh hexadecimal
`probe_token`, and `status: success`.

Do not invent the token or claim success without a successful Action result.
