---
name: start-draft
description: Open Draft for this portable workspace folder (experiment.json). Prefer the repo skill use-draft for full setup; here open the current workspace only.
---

# Start Draft for this workspace

The working directory is a **workspace** (`experiment.json` or `frames/`), not the Draft tool repo.

Follow [use-draft](../../../../.cursor/skills/use-draft/SKILL.md) steps 1–3 to find or build the viewer, then run `draft open .` (or `node <draft-clone>/dist/runtime/cli.js open .`) on **this folder**. Report the URL and keep the server running. Do not modify `frames/` unless asked.

Before editing any frame, follow the contract in [AGENTS.md](../../../AGENTS.md): `draft context .`, claim, edit only `frames/<id>/`, `draft feedback resolve`, clear the claim.
