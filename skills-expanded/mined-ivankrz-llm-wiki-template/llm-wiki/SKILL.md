---
name: llm-wiki
description: >
  Bootstraps and maintains a Karpathy-Style LLM Wiki Workspace — ein persistentes, markdown-basiertes
  Wissensartefakt, das ein LLM-Agent inkrementell aus unveränderlichen Rohquellen aufbaut.
  IMMER verwenden wenn Ivan einen LLM-Wiki aufbauen möchte, Sources einarbeiten will (ingest),
  das Wiki abfragen will (query), oder Health-Checks durchführen will (lint). Auch triggern bei
  "Karpathy Wiki", "LLM Wiki", "compile-once", "wiki workspace", "obsidian rag", "/ingest", "/query",
  "/lint", "/clip", "/file", "/search", "/reindex", "/bootstrap".
  Enthält 8 Slash-Commands, ein vollständiges Workspace-Bootstrap, und das Schema-Dokument (CLAUDE.md).
allowed-tools:
  - Read
  - Write(wiki/**)
  - Glob
  - Grep
  - Bash
---

# LLM Wiki Skill

Implementiert das **Karpathy LLM Wiki Pattern**: Ein persistentes, compoundierendes Wissens-Artefakt.
Der Agent schreibt das Wiki. Der User kuratiert die Rohquellen.

## WRITE-MODEL

```
Agent writes the wiki, human curates the raw sources.
- raw/**  →  READ-ONLY für den Agent. NIEMALS schreiben, editieren, löschen.
- wiki/** →  Working Area des Agent. Agent pflegt es aktiv.
- Jeder Write in wiki/** MUSS einen Log-Entry in wiki/log.md erzeugen.
- Manuelle User-Edits in Wiki-Pages → im nächsten Log-Entry vermerken.
```

## Drei Schichten

| Schicht | Pfad | Owner |
|---|---|---|
| Immutable Sources | `raw/**` | User (nur additive) |
| Agent Wiki | `wiki/**` | Agent (primär) |
| Schema | `CLAUDE.md` | Co-Evolution |

## Drei Operations

| Operation | Command | Wann |
|---|---|---|
| Source einarbeiten | `/ingest <path>` | Neues Material |
| Frage stellen | `/query <question>` | Ad-hoc |
| Health-Check | `/lint` | Wöchentlich |

## Commands

Alle Commands liegen unter `.claude/commands/`. Referenz-Dokumentation:

- `references/index-format.md` → Struktur von `wiki/index.md`
- `references/log-format.md` → Struktur von `wiki/log.md`
- `references/page-conventions.md` → Frontmatter-Regeln, Link-Style
- `references/karpathy-gist.md` → Verbatim-Referenz des Original-Gist

## Bootstrapping

Beim ersten Start: `/bootstrap` ausführen. Legt die vollständige Ordnerstruktur an.
Idempotent — zweiter Run überschreibt keine existierenden Files.

## Scale-Limit

Optimiert für ≤ 100–200 Sources / ≤ 500 Wiki-Pages.
Darüber hinaus: `qmd` installieren oder zu GraphRAG migrieren. Siehe `TRADE-OFFS.md`.
