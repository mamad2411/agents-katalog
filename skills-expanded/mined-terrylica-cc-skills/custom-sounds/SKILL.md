---
name: custom-sounds
description: List or validate Pushover notification sounds (built-in plus this account's custom uploaded sounds) via the /1/sounds.json API. Use when choosing a notification sound, checking whether a custom sound exists, or picking a safe fallback before sending. TRIGGERS - pushover sounds, list sounds, validate sound, custom sound, which sounds.
---

# custom-sounds

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

Enumerate/validate sounds via the TS core `pushover_core.ts sounds`.

```bash
env -u HTTPS_PROXY -u HTTP_PROXY bun "$(cc-plugin-root pushover-commander)/skills/_lib/pushover_core.ts" sounds list                # name<TAB>label
env -u HTTPS_PROXY -u HTTP_PROXY bun "$(cc-plugin-root pushover-commander)/skills/_lib/pushover_core.ts" sounds has piano            # exit 0 if present
env -u HTTPS_PROXY -u HTTP_PROXY bun "$(cc-plugin-root pushover-commander)/skills/_lib/pushover_core.ts" sounds resolve piano pianobar  # echo first that exists
```

## Notes (verified 2026-05-30)

- Pushover **silently accepts invalid sound names** (no API error) — so always `resolve`/`has` before relying on a custom sound; a typo would just fall back to the user's default silently.
- `piano` is a **custom** sound on this account; `pianobar` is built-in. Custom sounds are per application token, so pass `--app main|test` to query the right app.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the sound upload succeed AND become selectable in a real notification?** A reported success with a missing sound means the validation is wrong.
2. **Were loudness/format constraints honoured?** If the device rejected the sound, fix the sourcing pipeline.

Only update if the issue is real and reproducible — not speculative.
