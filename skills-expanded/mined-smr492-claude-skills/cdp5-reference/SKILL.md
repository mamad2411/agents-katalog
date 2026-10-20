---
name: cdp5-reference
description: CDP5-Doktrin als abfragbares Nachschlagewerk. Liefert per §-Nummer oder Schlagwort genau den nötigen Doktrin-Ausschnitt (statt der ganzen 2000-Zeilen-Datei) — just-in-time-Retrieval. Use wenn du eine CDP5-Regel/einen Paragraphen brauchst (z. B. „§32.9", „Lethal Trifecta", „Threat-Modeling", „TDD-First"), oder als Pflicht-Vorlauf vor Agent-Aufgaben.
---

# cdp5-reference

Die vollständige CDP5-Doktrin (`konzept-design-pattern-v5.md`) ist hier gebündelt. Statt sie ganz zu laden, holst du dir **gezielt** den relevanten Teil — kontext-sparsam (CDP5 §28.6).

## Abfrage

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/cdp5-reference/cdp5.mjs" --section=33.1
node "${CLAUDE_PLUGIN_ROOT}/skills/cdp5-reference/cdp5.mjs" --keyword="lethal trifecta"
node "${CLAUDE_PLUGIN_ROOT}/skills/cdp5-reference/cdp5.mjs" --list
```

- `--section=<X>` — die Sektion inkl. Untersektionen (`33`, `33.1`, `32.8`, `19.4`, `0.3` …).
- `--keyword=<term>` — alle Blöcke, deren Überschrift/Text den Begriff enthält, mit Snippet.
- `--list` — Inhaltsverzeichnis aller Sektionen.
- `--doctrine=<path>` — alternative Doktrin-Datei (Default: die gebündelte).

Exit: `0` Treffer · `1` kein Treffer · `2` Nutzungsfehler.

## Ohne Bash

Agenten ohne Bash lesen/grepen die gebündelte `konzept-design-pattern-v5.md` direkt (Read/Grep). Die `§`-Anker sind stabil; Teil-Überschriften gliedern die Lese-Reihenfolge (Teil 0 Mission · 1 Grundprinzipien · 2 Arbeitsweg · 3 Sicherheit · 4 Authoring · 5 LLM · 6 Erkenntnisse).
