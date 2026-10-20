---
name: fleet-doctor
description: Read a sanitized Fleet Core capability receipt and block unsupported Saga behavior before dispatch.
---

# Fleet Doctor

Use this skill before a Saga route whose behavior depends on a host capability.

1. Name the exact required and optional capability IDs from the calling
   contract. Do not infer requirements from prose.
2. Obtain the current sanitized receipt path from the operator or the approved
   workflow input. Do not run host observation from this skill.
3. Read `../../references/fleet-doctor-sources.md`.
4. Run:

   ```bash
   python3 plugins/saga/scripts/fleet_doctor.py \
     --receipt <sanitized-receipt.json> \
     --required <capability-id>
   ```

5. Stop on exit 1 or 2. Exit 1 means a declared requirement is blocked. Exit 2
   means the receipt or requirement set is invalid.
6. On a degraded report, preserve the exact optional capability and state.
   Never present the fallback as proof of the unavailable capability.

This skill is read-only. It does not prompt a model, inspect private host paths,
refresh credentials, install plugins, or change dispatch state.
