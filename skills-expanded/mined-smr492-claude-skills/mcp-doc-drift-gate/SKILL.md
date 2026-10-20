---
name: mcp-doc-drift-gate
description: Read-only T1-Gate gegen Consumer-Sycophancy bei MCP-Tools. Lädt einen MCP-Server (Konvention `export const TOOLS = [...]`) per dynamic import und prüft für jedes Tool, dass alle `inputSchema.properties.*` und alle deklarierten `outputContract`-Felder in der Tool-`description` als Token vorkommen. Verhindert die Klasse Halluzination, bei der ein LLM-Konsument ein undokumentiertes Feld sieht und sich seine Bedeutung selbst erfindet. Use bei „mcp doc check", „tool description drift", VOR jedem MCP-Slice-Merge.
---

# mcp-doc-drift-gate (CDP5 T1-Gate)

## Warum

Aus Retro-ADR 0016 (NSAI-Edge UC-VPS): wird ein neues Output-Feld eingeführt **ohne** dass die MCP-Tool-Description es erwähnt, liest ein LLM-Konsument das Feld im Output, findet keinen Anker und **erfindet sich eine Bedeutung**. „Consumer-Sycophancy" — strukturell vergleichbar zur klassischen Sycophancy (Tests grün, Halluzination im Output). Stefans Auftrag aus Tages-Retro: „Backlog-Idee `mcp-doc-drift-gate` priorisieren".

Dieser Skill macht das **deterministisch** und ohne LLM-Aufruf zu einem Pre-Merge-Gate.

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/mcp-doc-drift-gate/mcp-doc-drift-gate.mjs" --mcp=<path-to-mcp-server.mjs> [--json]
```

Exit: `0` keine Drift · `1` Drift gefunden · `2` Nutzungsfehler.

## Konvention

Der MCP-Server-Pfad muss ein ES-Modul sein und `TOOLS` als Array exportieren (Standard-Pattern in den NSAI-Edge-Servern):

```js
export const TOOLS = [
  {
    name: 'graph__verify',
    description: '... supported / contradicted / unknown ... physical_status ...',
    inputSchema: { type: 'object', properties: { subject: {...}, predicate: {...}, ... } },
    outputContract: ['verdict', 'contested', 'physical_status'],  // OPTIONAL — wenn nicht da: nur Input-Drift geprüft
  },
];
```

`outputContract` ist optional, aber stark empfohlen — er macht das Gate erst für die ADR-0016-Klasse wirksam.

## Checks

1. **Tool-Struktur**: jedes TOOL hat `name`, `description`, `inputSchema`.
2. **Input-Drift**: jedes Feld in `inputSchema.properties` muss im Description-Text als Token vorkommen (case-insensitive Substring-Match auf Wortgrenzen).
3. **Output-Drift** (wenn `outputContract` deklariert): jedes Feld muss in der Description vorkommen.
4. **Whitespace-Tolerant**: Tokenisierung normalisiert Whitespace.

## Beispiel-Output

```
mcp-doc-drift-gate — 13 Tools geprüft, 2 Drift-Stellen

  ✗ graph__verify — Output-Feld `physical_status` nicht in description
  ✗ graph__search — Input-Feld `max_hops` nicht in description

2 Drift  ·  Exit 1
```

## Was es NICHT prüft (bewusst Scope-Grenze)

- Bedeutungs-Korrektheit der Description (Judgment-Task → `konzept-reviewer` o. ä.).
- Vollständigkeit der `outputContract`-Deklaration. Wenn der Skill weder Output-Drift findet noch eine `outputContract` sieht, gibt er eine **Hinweis-Notiz** aus, kein Fail.
- Wire-Vertrag / Föderation (anderer Skill: `mcp-config-lint`).
