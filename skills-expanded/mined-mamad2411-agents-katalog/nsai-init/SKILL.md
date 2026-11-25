---
name: nsai-init
description: Verankert die nsai-edge-WISSENSDOKTRIN (Tier-1-Wissensbasis, read-before-act, Rückschreib-Pflicht, Two-Door, graph__-MCP-Tools) als EIGENEN idempotenten Marker-Block (<!-- nsai:start -->…<!-- nsai:end -->) in der CLAUDE.md eines Projekts — getrennt vom cdp5-Konzeptblock. Hybrid: deterministischer Merge/Diff-Kern + interaktive Bestätigung. Use bei „nsai-edge in CLAUDE.md verankern", „nsai init", nach Installation des nsai-edge-Plugins.
---

# nsai-init — Wissensdoktrin-Block für die Konsumenten-CLAUDE.md

Komplement zu `cdp5-init`: **cdp5-init verankert die Konzeptdoktrin (WIE)**, **nsai-init die Wissensdoktrin (WAS)**. Jedes Plugin besitzt + versioniert seinen eigenen CLAUDE.md-Block; nsai-edge ist dadurch unabhängig installierbar (keine Abhängigkeit auf cdp5-gates).

`nsai-init` merged einen **projektunabhängigen** Block zwischen `<!-- nsai:start -->…<!-- nsai:end -->` (Tier-1-Wissensbasis-Hierarchie, read-before-act-Tools, Rückschreib-Pflicht, Two-Door-Grenze, `graph__`-Tool-Namen). Erneuter Lauf = **Update** (Block ersetzt sich selbst, idempotent). Quelle des Blocks: `nsai-block.md`.

**Schreibt nur zwischen den Markern, nur mit `--write`, nur nach Operator-Bestätigung** (Mensch-Verantwortung).

## Workflow

1. **Vorschau (read-only Diff):**

   node "${CLAUDE_PLUGIN_ROOT}/skills/nsai-init/nsai-init.mjs" --target=<CLAUDE.md>

2. Diff zeigen, Operator fragen.
3. **Bei ja:** mit `--write` übernehmen (idempotenter Marker-Merge):

   node "${CLAUDE_PLUGIN_ROOT}/skills/nsai-init/nsai-init.mjs" --target=<CLAUDE.md> --write

4. **Bei Anpassungswunsch:** angepassten Block via `--block=<datei>` (muss `nsai-edge` + `graph__` enthalten, sonst Reject):

   node "${CLAUDE_PLUGIN_ROOT}/skills/nsai-init/nsai-init.mjs" --target=<CLAUDE.md> --block=<angepasst.md>

   Schleife bis „ja" oder Abbruch (Fallback: Operator editiert die CLAUDE.md manuell).

## Exit-Codes
`0` Diff gezeigt / geschrieben · `2` Nutzungs-/Input-Fehler (fehlendes `--target`, Verzeichnis statt Datei, inkonsistentes Marker-Paar, Block ohne `nsai-edge`/`graph__`).
