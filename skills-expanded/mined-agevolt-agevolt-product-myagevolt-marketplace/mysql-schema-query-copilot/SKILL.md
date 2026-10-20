---
name: mysql-schema-query-copilot
description: "Pouzi pri MyAgeVolt SQL lookupoch iba na citanie, SELECT/count/join dotazoch a hladani v scheme cez AgeVolt database repo. Nepouzivaj na zmeny rutin, cistiace UPDATE/DELETE, vykonove review, triage incidentov ani handoff."
---

# Pomocnik Pre MySQL Schemu A Dotazy

Tento skill je pre SQL iba na citanie nad MyAgeVolt schemou.

## Kontext

Precitaj:

- `../../kb/database-repo-workflow.md`
- `../../kb/mysql-agevolt-environment.md`
- `../../kb/mysql-schema-inventory.md`
- `../../kb/mysql-safety-boundaries.md`
- `../../kb/mysql-access-gaps.md`

V `database` repo najprv hladaj v `exports/**`, `exports/_metadata/**`,
`knowledge_base/reference/**` a relevantnych `knowledge_base/database/**`
suboroch. `triggers cistenie` je len legacy kontext; konflikt vyhrava
`database`.

Pred schema lookupom, ktory bude podkladom pre implementaciu alebo odporucanie
diffu, vykonaj `Repo Sync Gate` z `database-repo-workflow.md`. Ak je repo na
feature branchi s lokalnymi zmenami, nahlas blocker namiesto tvrdenia, ze ide o
najnovsi main.

## Postup

1. Urci pozadovany vystup: pocet, lookup, join, hladanie, validacia alebo report.
2. Pomenuj latest-main sync stav, precitane database repo subory a potvrdene
   fakty o tabulkach/stlpcoch.
3. Vytvor `SELECT` iba na citanie.
4. Pri ambiguitach kvalifikuj stlpce a aliasy.
5. Pridaj kratke vysvetlenie joinov a filtrov.
6. Ak objekt alebo metadata v repo chybaju, nahlas access gap alebo potrebu
   refreshu; nepytaj pasted `SHOW CREATE` ako prvy krok.

## Hranice

- Ziadne `INSERT`, `UPDATE`, `DELETE`, DDL, upravy trigger/procedure ani
  produkcne akcie.
- DB apply nikdy nerob bez exact `APPROVE WRITE` alebo `APPROVE WRITE PROD`.
- Ak sa read-only poziadavka zmeni na DB zmenu, prepni na prislusny skill a
  pouzi database repo branch + diff + commit/push approval workflow.
- Ak pouzivatel chce opravit data, pouzi `mysql-data-cleanup-copilot`.
- Ak sa pyta, preco je dotaz pomaly, pouzi `mysql-performance-review`.
