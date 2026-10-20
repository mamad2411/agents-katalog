---
name: retro-memory-loop-check
description: Read-only Check, ob jeder in Retro-/ADR-Dokumenten zitierte Memory-Slug (feedback_*/project_*/[[slug]]) real angelegt ist und einen Pointer im Memory-Index hat. Use bei „Retro-Memory-Loop prüfen", nach Retro-ADRs, „verdampfen unsere Lessons".
---

# retro-memory-loop-check (CDP5 T1-Gate)

Schließt den in CDP5 §32.6 geforderten Lern-Loop: zitierte Lehren müssen real existieren, sonst verdampfen sie (Praxis-Befund: Retros zitierten Slugs, die nie angelegt wurden).

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/retro-memory-loop-check/retro-memory-loop-check.mjs" \
  --retro=<retro-dir> --memory=<memory-dir> [--json]
```

Exit: `0` Loop dicht · `1` ≥1 zitierter Slug fehlt oder hat keinen Pointer · `2` Nutzungsfehler.

## Prüfung

Sammelt aus allen `.md` unter `--retro` die Slug-Referenzen (`[[slug]]`, `feedback_x`, `project_x`, `(slug.md)`). Für jeden: existiert `<memory>/<slug>.md`? und enthält `<memory>/MEMORY.md` einen Pointer? Beides nötig — sonst Befund.
