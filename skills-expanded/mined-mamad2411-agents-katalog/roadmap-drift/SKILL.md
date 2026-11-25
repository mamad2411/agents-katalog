---
name: roadmap-drift
description: Read-only Roadmap↔Code-Drift-Check. Prüft deterministisch, ob jedes als FERTIG markierte Artefakt einer Roadmap/Plan-Datei wirklich im Code existiert. Use bei „Roadmap gegen Code prüfen", vor Sprint-Planung, „sind die geplanten Sachen wirklich gebaut".
---

# roadmap-drift (CDP5 T1-Gate)

Verhindert das Anti-Pattern „Plan führt schon-gebauten Code als nicht-begonnen" bzw. „Plan behauptet Symbole, die es nicht gibt" (CDP5 §25 / §28.5).

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/roadmap-drift/roadmap-drift.mjs" --roadmap=<roadmap.md> --repo=<root> [--json]
```

Exit: `0` kein Drift · `1` ≥1 FERTIG-Artefakt fehlt · `2` Nutzungsfehler.

## Konvention

Eine Zeile zählt als FERTIG bei einem Marker (`✅`, `GESCHLOSSEN`, `EXISTIERT`, „umgesetzt", „geliefert", „gelandet"); die `` `…` ``-Tokens darin (Pfade, Klassen, Routes) werden gegen das Repo geprüft. Nicht verifizierbare Tokens (CLI-Befehle, Flags, snake_case) werden übersprungen.
