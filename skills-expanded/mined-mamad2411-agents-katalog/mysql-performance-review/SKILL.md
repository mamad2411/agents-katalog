---
name: mysql-performance-review
description: "Pouzi pri MyAgeVolt pomalych dotazoch, EXPLAIN analyze, index coverage a optimalizacii SQL cez AgeVolt database repo. Pri zmene priprav branch + diff + changelog kandidat. Nepouzivaj na lookupy, rutiny, cistenie dat, triage ani handoff."
---

# Kontrola Vykonu MySQL

Tento skill je pre pomale dotazy a pracu s indexmi.

## Kontext

Precitaj:

- `../../kb/database-repo-workflow.md`
- `../../kb/mysql-agevolt-environment.md`
- `../../kb/mysql-schema-inventory.md`
- `../../kb/mysql-performance-index-rules.md`
- `../../kb/mysql-production-ddl-safety.md`
- `../../kb/mysql-safety-boundaries.md`
- `../../kb/slow-query-report-template.md`

V `database` repo citaj `exports/_metadata/table_sizes.tsv`, FK/index metadata,
relevantne DDL exporty, `knowledge_base/database/data-access.md`,
`knowledge_base/database/mysql-style.md` a `knowledge_base/quality/testing.md`.
`triggers cistenie` je iba legacy kontext; pri konflikte vyhrava `database` repo.

Pred analyzou, ktora moze skoncit diffom, vykonaj `Repo Sync Gate` z
`database-repo-workflow.md`. Branch vytvaraj iba z hlavnej branche po
`git fetch origin` a `git pull --rebase --ff-only`.

## Postup

1. Pomenuj latest-main sync stav, zoskup opakovane vzory dotazov a pomenuj pouzivatelsky dopad.
2. Rad podla frekvencie, rows examined, latencie, horucej cesty a rizika.
3. Pred navrhom indexu pomenuj existujuce indexy alebo metadata, ktore dotaz
   pokryvaju alebo nepokryvaju.
4. Preferuj upravu dotazu alebo predikatu, ked problem vyriesi s mensim dopadom.
5. Ak treba produkcny index alebo table DDL, rozdel ho podla
   `mysql-production-ddl-safety.md`; index nesmie byt v tom istom `ALTER TABLE`
   ako column alebo FK zmena.
6. Ak treba DB zmenu, priprav v `database` repo novu branchu, export/config diff
   a changelog kandidat.
7. Ukaz precitane subory, diff, DDL lock risk a overovaci plan.
8. Spytaj sa na commit; po commite sa samostatne spytaj na push.

## Hranice

- Nevymyslaj nazvy indexov ani kardinalitu bez repo metadata alebo EXPLAIN.
- DB apply nikdy nerob bez exact `APPROVE WRITE` alebo `APPROVE WRITE PROD`.
- Ak ide o constraint/runtime chybu, pouzi `mysql-db-error-triage`.
