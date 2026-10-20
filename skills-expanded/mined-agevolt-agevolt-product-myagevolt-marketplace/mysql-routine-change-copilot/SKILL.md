---
name: mysql-routine-change-copilot
description: "Pouzi pri MyAgeVolt MySQL trigger/procedure/function/event praci v AgeVolt database repo. Najprv hladaj v database/exports a knowledge_base; pri zmene priprav novu branchu, export diff a changelog kandidat. Nepouzivaj na lookupy iba na citanie, cistenie dat, vykon, triage ani handoff."
---

# Pomocnik Pre Zmeny MySQL Rutin

Tento skill sluzi na zmeny MyAgeVolt MySQL rutin: triggerov, procedur, funkcii
a eventov.

## Kontext

Najprv precitaj:

- `../../kb/database-repo-workflow.md`
- `../../kb/mysql-agevolt-environment.md`
- `../../kb/mysql-routine-style-rules.md`
- `../../kb/mysql-schema-inventory.md`
- `../../kb/mysql-safety-boundaries.md`
- `../../kb/mysql-production-ddl-safety.md`, ak ide o migracne DDL alebo table zmenu

V `database` repo potom precitaj `AGENTS.md`, `knowledge_base/index.md`,
`knowledge_base/registry.yaml` a relevantne pravidla, hlavne
`knowledge_base/database/db-change-workflow.md`,
`knowledge_base/database/mysql-style.md`, `knowledge_base/database/data-access.md`
a `knowledge_base/quality/testing.md`.

`triggers cistenie` pouzivaj ako legacy kontext. Pri konflikte vzdy vyhrava
`database/AGENTS.md` a `database/knowledge_base/**`.

Pred objektovym lookupom a branchou vykonaj `Repo Sync Gate` z
`database-repo-workflow.md`. Branch vytvor az po `git fetch origin`, cistom
hlavnom branchi a `git pull --rebase --ff-only`. Ak je repo na feature branchi
alebo ma lokalne zmeny, zastav a ukaz blocker.

## Postup

1. Vykonaj latest-main sync gate a uved branch/base commit.
2. Najdi DB objekt v `database/exports/<schema>/{routines,triggers,events}`.
3. Pred zmenou objekt refreshni cez `python scripts/refresh.py --object
   <schema>.<name>` alebo manualne over `SHOW CREATE ...` a zosulad export.
4. Ak objekt chyba, nahlas access gap alebo potrebu refreshu; nepytaj pasted
   `SHOW CREATE` ako prvy krok.
5. Ak sync gate presiel, priprav branch `codex/db-<kratky-slug>` z aktualneho
   mainu.
6. Pri existujucom objekte uprav iba dotknuty `label: BEGIN ... END;` blok alebo
   sustredeny diff v exporte.
7. Pri novom objekte priprav kompletny export a changelog kandidat s
   `DELIMITER //` a `DEFINER=\`dev_admin\`@\`%\``.
8. Vzdy priprav `changelog/YYYYMMDD_HHMMSS__<schema>__<short_description>.sql`
   pre DB zmenu.
9. Pri migracnom DDL pouzi produkcny DDL safety checklist.
10. Ukaz, ktore subory boli zmenene, relevantny diff a precitane KB.
11. Spytaj sa na commit. Bez potvrdenia necommituj.
12. Po commite sa samostatne spytaj na push. Bez potvrdenia nepushuj.

## Hranice

- DB apply nikdy nerob bez exact `APPROVE WRITE` alebo `APPROVE WRITE PROD`.
- Nepridavaj ochrany, audit polia, `SIGNAL` ani DDL bez explicitnej poziadavky.
- Komentare drz kratke a po slovensky.
- Ak ide o vykon, triage chyby, cistenie dat, lookup iba na citanie alebo
  zadanie pre agenta, pouzi prislusny susedny skill.
