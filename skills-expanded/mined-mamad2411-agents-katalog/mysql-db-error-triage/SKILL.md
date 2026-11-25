---
name: mysql-db-error-triage
description: "Pouzi pri MyAgeVolt DB chybach, FK constraint problemoch, InnoDB statuse, DB error analyze, OCPP/nabijacich DB anomaliach a P1 incidente cez AgeVolt database repo. Nepouzivaj na bezne zmeny rutin, lookupy, cistenie dat, vykon ani handoff."
---

# Triage MySQL DB Chyb

Tento skill sluzi na analyzu DB chyb a incidentov.

## Kontext

Precitaj:

- `../../kb/database-repo-workflow.md`
- `../../kb/mysql-agevolt-environment.md`
- `../../kb/mysql-schema-inventory.md`
- `../../kb/mysql-safety-boundaries.md`
- `../../kb/mysql-production-ddl-safety.md`
- `../../kb/fk-error-checklist.md`

V `database` repo citaj relevantne `exports/**`, `exports/_metadata/foreign_keys.tsv`,
`knowledge_base/database/error-handling.md`, `knowledge_base/database/security.md`
a suvisiace topic pravidla. `triggers cistenie` pouzi iba ako legacy kontext.

Pred fixom alebo diffom vykonaj `Repo Sync Gate` z `database-repo-workflow.md`.
Ak je repo na feature branchi alebo ma lokalne zmeny, zastav a ukaz blocker
namiesto fixu zo stareho snapshotu.

## Postup

1. Zachyt presnu chybu, objekt, SQL ukazku a cas, ak su dostupne.
2. Zarad problem: FK/constraint, typ/collation mismatch, chybajuci index,
   runtime chyba rutiny, OCPP/nabijacia anomalia alebo neznama pricina.
3. Over latest-main sync stav, DDL, FK, indexy a relevantne pravidla v `database` repo.
4. Pri OCPP/nabijacich anomaliach oddel biznis symptom od DB dokazu.
5. Vystup ma obsahovat potvrdene fakty, hypotezy, precitane repo subory, dalsie
   kontroly iba na citanie a riziko.
6. Ak treba column/index/FK/table DDL fix, rozdel ho podla
   `mysql-production-ddl-safety.md` a pomenuj metadata lock risk.
7. Ak treba fix, priprav branch + diff + changelog kandidat v `database` repo a
   ukaz zmenene subory.
8. Spytaj sa na commit; po commite sa samostatne spytaj na push.

## Hranice

- Nenavrhuj destruktivne opravy pred kontrolami iba na citanie.
- DB apply nikdy nerob bez exact `APPROVE WRITE` alebo `APPROVE WRITE PROD`.
- Nerob z jednej incidentnej hodnoty globalne pravidlo.
