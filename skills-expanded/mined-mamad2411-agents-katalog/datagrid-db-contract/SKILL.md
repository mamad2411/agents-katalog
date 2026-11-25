---
name: datagrid-db-contract
description: "Pouzi pri MyAgeVolt DB/metadatovom kontrakte pre DataGrid alebo FE formular cez AgeVolt database repo: SQL pohlad, general_mysql_column, general_mysql_view, menu_view DB podklady, fe_select_sql, fe_default_sql, fe_hide_sql. FE render patri do agevolt-fe."
---

# DataGrid DB Kontrakt

Tento skill riesi iba DB a metadatovu vrstvu pre DataGrid/FE formular. FE render,
MUI, `renderCell`, frontendovy preset a UI pravidla patria do existujucich
`agevolt-fe` DataGrid skillov.

## Kontext

Precitaj:

- `../../kb/database-repo-workflow.md`
- `../../kb/mysql-agevolt-environment.md`
- `../../kb/mysql-safety-boundaries.md`
- `../../kb/mysql-schema-inventory.md`
- `../../kb/mysql-production-ddl-safety.md`, ak kontrakt vyzaduje table/index DDL

V `database` repo citaj `exports/agevolt/config_data/general_mysql_*`,
`exports/agevolt/config_data/menu_view*`, `exports/agevolt_fe_*_view/**`,
`exports/agevolt_fe_sp/**` a relevantne `knowledge_base/database/api-contracts.md`.
`triggers cistenie` je iba legacy kontext; pri konflikte vyhrava `database` repo.

Pred objektovym lookupom alebo diffom vykonaj `Repo Sync Gate` z
`database-repo-workflow.md`: `git fetch origin`, cisty hlavny branch,
`git pull --rebase --ff-only`, potom branch z aktualneho mainu. Ak je repo na
feature branchi alebo ma lokalne zmeny, zastav a ukaz blocker.

## Rozsah

Patri sem:

- SQL pohlad a DB kontrakt pre FE,
- `agevolt.general_mysql_column` metadata,
- `fe_select_sql`, `fe_default_sql`, `fe_hide_sql`,
- `general_mysql_view` / `menu_view` DB podklady,
- testovaci `CALL agevolt_fe_sp.general_fe_column_values_sp(...)`.

Mimo rozsahu:

- React/MUI/DataGrid renderer,
- frontendovy preset JSON,
- `componentMeta`, `renderCell`, onClick UI akcie.

## Nazvy DataGrid FE View

Pri DataGrid view, ktore je naviazane na `menu_view`, najprv odvod realny nazov
SQL view z automatickeho mechanizmu `menu_view_ensure_views` /
`menu_view.view_name`. Nevymyslaj paralelny manualny nazov.

Povinny postup:

1. Vytvor alebo uprav `menu_view.view_name` s cielovym automatickym nazvom,
   napriklad `agevolt_fe_master_view.general_broker_offers_data_fe`.
2. Spusti alebo priprav `agevolt_core.menu_view_ensure_views`, aby vznikol
   placeholder s rovnakym nazvom, ak este neexistuje.
3. Export SQL view vytvor pod tym istym nazvom ako automaticky placeholder a
   tymto exportom prepis SELECT. Nepouzivaj singular/plural variant bokom.
4. `general_mysql_view`, `general_insert_update_delete_table`,
   `general_mysql_view_column`, `menu_view.meta` a default preset musia ukazovat
   na ten isty nazov.
5. Ak sa opravuje omyl v nazve, neponechaj novy manualny view vedla
   automatickeho. Stary zly nazov iba cleanupni v changelogu a export presun
   pod automaticky nazov.

Kontrola pre commit: `menu_view.view_name`, `menu_view.meta.Prefer`,
`general_mysql_view.view`, IUD `view` a subor
`exports/agevolt_fe_*_view/views/<view>.sql` musia pouzivat presne rovnaky
`<schema>.<view>`.

## Postup

1. Pomenuj latest-main sync stav, precitane database repo subory a aktualny DB kontrakt.
2. Pri zmene config/reference data re-dumpni relevantny `exports/<schema>/config_data/` subor.
3. Ak treba table/index DDL, rozdel ho podla produkcneho DDL safety checklistu.
4. Ak treba zmena, priprav novu branchu, export/config diff a changelog kandidat.
5. Ukaz zmenene subory, relevantny diff a testovaci SQL plan.
6. Spytaj sa na commit; po commite sa samostatne spytaj na push.

## Hranice

- DB apply nikdy nerob bez exact `APPROVE WRITE` alebo `APPROVE WRITE PROD`.
- Ak treba FE implementaciu, odkaz na `agevolt-fe-datagrid-v4` alebo suvisiaci
  AgeVolt FE skill.
