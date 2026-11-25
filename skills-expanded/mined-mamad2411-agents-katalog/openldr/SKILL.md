---
name: openldr
description: >
  Use when working with OpenLDR laboratory data systems — SQL views,
  analytics datasets, or API queries for HIV VL, HIV EID, TB GeneXpert,
  CD4, CrAg, TB-LAM. Routes to the correct openldr sub-skill.
  TRIGGER: user mentions OpenLDR, LIMS, panel codes, observation codes,
  viral load, VL, EID, GeneXpert, CD4, CrAg, TB-LAM, analytics dataset,
  OpenLDR API, database schema, table columns, or data model.
metadata:
  author: openldr
  version: "1.0"
---

# OpenLDR Skills

OpenLDR skills automate laboratory data workflows. Invoke the correct sub-skill based on the user's intent.

## Routing Table

| User Intent | Skill to Invoke |
|-------------|----------------|
| Create, modify, or improve SQL views that pivot LabResults observation codes into columns | `openldr:create-view` |
| Generate analytics dataset tables, table-valued functions, CREATE TABLE DDL, population scripts, or Python ORM models from existing views | `openldr:create-dataset` |
| Query the OpenLDR Analytics API — find endpoints, build parameters, execute requests, explain results | `openldr:query-api` |
| Ask questions about OpenLDR — database schema, panel codes, table columns, relationships, data model, HL7 codes | `openldr:explore` |
| Generate HTML report to visualize data in the browser, export results as HTML | `openldr:report` |

## When to Use Each Skill

**`openldr:create-view`** — User mentions: creating views, viewVL_Info, viewTbGenexpert, pivot observation codes, LIMSObservationCode, LIMSPanelCode, VIRAL panel, HIVVL panel, add columns to a view, improve a view.

**`openldr:create-dataset`** — User mentions: analytics dataset, VlData, EIDMaster, TBMaster, table-valued function, populate dataset, ORM model, SQLAlchemy model, analytics table.

**`openldr:query-api`** — User mentions: VL suppression, EID positivity, TB results, tested samples, registered samples, rejected samples, TAT, turnaround time, lab performance, facility data, OpenLDR API, dashboard data.

**`openldr:explore`** — User mentions: OpenLDR schema, table columns, what does X mean, panel codes, observation codes, data model, relationships, facility hierarchy, HL7 codes, LOINC, how are tables connected, what tables exist, database structure.

**`openldr:report`** — User mentions: HTML report, visualize in browser, export as HTML, show in browser, open in browser, generate report, report page.

## Setup — Database & API Credentials

The skills work **offline-first** using built-in knowledge, but connecting to the live database and API unlocks full capabilities (discovering new panels, querying live data, executing API calls).

Credentials are loaded automatically from `.env` files — **no shell restart needed**.

### Global Setup (recommended — works from any directory)

Create `~/.openldr.env`:

```
# OpenLDR Database (used by openldr:create-view and openldr:explore)
OPENLDR_DB_HOST=localhost
OPENLDR_DB_USER=your_db_username
OPENLDR_DB_PASSWORD=your_db_password
OPENLDR_DB_DICT=OpenLDRDict
OPENLDR_DB_DATA=OpenLDRData
OPENLDR_DB_PORT=1433

# OpenLDR API (used by openldr:query-api)
OPENLDR_API_URL=https://dev.openldr.org.mz
OPENLDR_API_USER=your_api_username
OPENLDR_API_PASSWORD=your_api_password
```

### Project-Specific Setup (overrides global for a specific project)

Create `.env` in your project's working directory:

```
# Override the database host for this project
OPENLDR_DB_HOST=192.168.1.50
OPENLDR_DB_USER=project_user
OPENLDR_DB_PASSWORD=project_password
```

### Priority Order

| Priority | Location | Scope |
|----------|----------|-------|
| 1st | `.env` in current working directory | This project only |
| 2nd | `~/.openldr.env` | All projects (global default) |
| 3rd | Shell environment variables | From `~/.bashrc` if loaded |

Higher-priority values are never overridden by lower-priority ones. This means you can set global defaults in `~/.openldr.env` and override specific values per-project with a local `.env`.

**Important:** Never commit `.env` files to git — they contain credentials. Add `.env` to your `.gitignore`.

### Test Connectivity

```bash
# Test database connection
skills/openldr-create-view/scripts/query-db.sh test

# Test API connection
skills/openldr-query-api/scripts/query-api.sh test
```

## How to Invoke

After identifying the correct sub-skill from the table above, invoke it using the Skill tool:

```
Skill: openldr:create-view
Skill: openldr:create-dataset
Skill: openldr:query-api
Skill: openldr:explore
Skill: openldr:report
```

Do NOT attempt to do the work yourself. Always delegate to the sub-skill.
