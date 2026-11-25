---
name: konzept-lint
description: Read-only Konzept-Struktur-Lint + deterministischer Teil-Score. Prüft die entscheidbaren CDP5-§2-Pflichtelemente (UCs, AC-Tabellen, Fehlerfälle, Glossar, Kopf), binär/verifizierbare AC (kein „should/ideally"), bedingt LLM-UC-/RAG-Felder — und berechnet den deterministischen Anteil des Reife-Scores. Use VOR dem konzept-reviewer (fängt mechanische Lücken in 0-Token), bei „konzept lint", „ist die spec strukturell vollständig".
---

# konzept-lint (CDP5 T1-Gate)

Der **deterministische Vorlauf** zum `konzept-reviewer`: fängt die entscheidbaren §2/§4-Lücken (fehlende AC-Tabelle, Fehlerfälle, vage AC …) in 0-Token/Sekunden, sodass der opus-Agent nur noch die Judgment-Dimensionen (Sachbearbeiter-Test, semantische Vollständigkeit) bewertet. Macht den Konzept-Schritt schneller, billiger und den Score **reproduzierbar**.

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/konzept-lint/konzept-lint.mjs" --konzept=<konzept.md> [--rubric=<rubric.json>] [--json]
```

Exit: `0` keine strukturelle Lücke · `1` Lücke · `2` Nutzungsfehler.

## Checks

- **Pflicht-Struktur:** ≥1 `## UC-`, Kopf (Version/Scope), Glossar; je UC AC-Tabelle + Fehlerfälle + nummerierte Schritte.
- **AC binär/verifizierbar:** flaggt vage Sprache in AC-Zeilen (`should`, `ideally`, `sollte`, `möglichst`, `ca.`, `etc.` …) — nicht testbar.
- **Bedingt:** LLM-UC erkannt → Probabilistik-Statement + §13.1-Felder (Kontext/Ausgabe/Validierung/Fallback/Cutoff); RAG erkannt → §20.3-Felder (Chunking/Embedding/Retriever/Caching/Invalidierung).
- **Teil-Score:** gewichteter 0–10-Wert über die deterministischen Rubrik-Dimensionen; Gewichte via `--rubric=<json>` (`{"weights":{…}}`) überschreibbar (Default = §4). Judgment-Anteil bleibt dem `konzept-reviewer`.
