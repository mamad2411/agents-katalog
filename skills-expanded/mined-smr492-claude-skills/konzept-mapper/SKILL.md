---
name: konzept-mapper
description: Read-only Konzept↔Code-Mapping. Erzeugt eine deterministische Tabelle, welche UCs eines Konzept-Dokuments im Code vorhanden sind (✓/teilweise/fehlt). Use bei „Mapping Konzept gegen Code", „welche UCs sind umgesetzt", Sprint-Ende-Inventur, vor strategischen Entscheidungen.
---

# konzept-mapper (CDP5 T1-Gate)

Deterministischer Detektor — ersetzt den früheren `konzept-mapper`-Agent. Output ist der Beleg; **kein** LLM-Urteil im Kern. Der Main-Agent ruft das Programm und handelt auf den Report.

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/konzept-mapper/konzept-mapper.mjs" \
  --konzept=<pfad/zum/konzept.md> --repo=<repo-root> [--json]
```

Exit: `0` kein voll fehlender UC · `1` ≥1 UC „fehlt" (Drift) · `2` Nutzungsfehler.

## Konvention (worauf der Kern arbeitet)

- Ein **UC** ist eine `## UC-…:`-Sektion (andere `#`/`##`-Überschriften beenden sie).
- **Verifizierbare Artefakte** stehen in `` `…` ``-Backticks: Pfade (`src/Foo.php`), Klassen/Symbole (`Article`, `Foo\Bar`, `Class::method`), Routes (`/api/items`). CLI-Befehle / Flags / snake_case-Werte werden übersprungen (nicht verifizierbar).
- Status pro UC: **✓** alle Artefakte gefunden · **teilweise** einige · **fehlt** keine · **n/a** keine verifizierbaren.

## Danach (Main-Agent, nicht der Skill)

Der Skill detektiert nur. Lücken bewerten / Code nachziehen / Konzept aktualisieren bleibt LLM-/Mensch-Arbeit (CDP5 §32.9: deterministischer Kern, LLM als Interpretations-Schale).
