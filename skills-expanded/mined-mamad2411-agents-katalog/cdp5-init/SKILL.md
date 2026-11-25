---
name: cdp5-init
description: Bindet die CLAUDE.md eines Projekts an den claude-skills-Marketplace an — fügt einen projektunabhängigen Marker-Block (CDP5-Verweis, cdp5-reference-Gate, Trigger-Map, Skills/Agents-Liste) idempotent ein bzw. aktualisiert ihn. Hybrid: deterministischer Merge/Diff-Kern + interaktive Bestätigung. Use bei „CLAUDE.md an den Marketplace anbinden", „cdp5 init", nach Neuinstallation/Update der Plugins.
---

# cdp5-init (CDP5 Hybrid-Skill, §32.9)

Schließt die Lücke nach Marketplace-Installation: die `/plugin install`-Befehle verdrahten Skills + Agents, aber **nicht** die CLAUDE.md. `cdp5-init` merged einen **projektunabhängigen** Block zwischen `<!-- cdp5:start -->…<!-- cdp5:end -->` (CDP5-Verweis, **cdp5-reference-Gate**, Trigger-Map, Skills/Agents). Erneuter Lauf = **Update** (Block ersetzt sich selbst, idempotent). Quelle des Blocks: `cdp5-block.md`.

**Schreibt nur zwischen den Markern, nur mit `--write`, nur nach Operator-Bestätigung** (erster schreibender cdp5-gates-Skill — Mensch-Verantwortung §1.6/§23).

## Interaktiver Ablauf (vom Haupt-Agent zu fahren)

1. **Diff zeigen (read-only):**
   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/skills/cdp5-init/cdp5-init.mjs" --target=<CLAUDE.md>
   ```
   Gibt den Block-Diff aus (Anhängen bzw. Ersetzen), schreibt nichts.
2. **Eine ja/nein-Frage** an den Operator stellen: „Diesen Block übernehmen?"
3. **Bei ja:** mit `--write` übernehmen (idempotenter Marker-Merge):
   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/skills/cdp5-init/cdp5-init.mjs" --target=<CLAUDE.md> --write
   ```
4. **Bei nein:** fragen, *was* angepasst werden soll, den Block-Inhalt anpassen (Invarianten wahren: CDP5-Verweis **und** `cdp5-reference`-Gate müssen erhalten bleiben — sonst lehnt der Kern mit Exit 2 ab), als Datei übergeben und erneut Diff zeigen → zurück zu Schritt 2:
   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/skills/cdp5-init/cdp5-init.mjs" --target=<CLAUDE.md> --block=<angepasst.md>
   ```
   Schleife bis „ja" oder Abbruch (Fallback: Operator editiert die CLAUDE.md manuell).

## Exit-Codes (Kern)

`0` Diff gezeigt / geschrieben · `2` Nutzungs-/Input-Fehler (fehlendes `--target`, Verzeichnis statt Datei, inkonsistentes Marker-Paar, Block ohne CDP5-Verweis/Gate).

## Grenzen

Deterministisch ist nur der Merge/Diff. Die Inhalts-Anpassung in Schritt 4 ist KI-Arbeit; ihre Validierung ist der **erneute deterministische Diff + die Bestätigung** — die KI-Ausgabe wird nie ungeprüft geschrieben.
