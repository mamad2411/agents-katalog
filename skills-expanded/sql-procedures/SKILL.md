---
name: sql-procedures
description: "Use when the work is the SQL Server backend of a Power Apps app: writing, reviewing or fixing a procedure called by Power Automate (\"Table1 comes back empty\", NOCOUNT, XACT_ABORT, status/description/id/url return, result code), the data model (Id_/Flg_/Dt_ prefixes, role flags, keys, collation), a computed column for delegation (\"date filter does not delegate\", \"CountRows does not delegate\", Ref_DtInclusao), unit scope with a @Filtros JSON, the package and DDL request to the DBA (frozen database, environment proofs), the connector account GRANT EXECUTE, or migrating legacy data to SQL Server. Do not use for Power Fx, screens or app-side delegation (use `powerapps-canvas`), the flow, Try/Catch or authorization in the flow (use `power-automate`), Dataverse (use `dataverse`), nor architecture and the work protocol (use `power-platform`)."
argument-hint: "[procedure|model|delegation|scope|dba|migration|audit] [target]"
user-invocable: true
---

# sql-procedures

Produces the SQL Server backend of Power Apps apps: write and read procedures called by Power
Automate, the data model they and the app use, the computed columns that make the filter delegate, the
package and DDL request to the DBA, and the legacy data migration. Decided standards (return
contract, database, names) live in
[default-decisions.md](../power-platform/references/default-decisions.md); this skill teaches the
**how** and checks it with `scripts/lint-procedure.py`. The flow that calls the procedure and the
authorization inside it belong to `power-automate`; the formula that consumes the computed column
belongs to `powerapps-canvas`.

## Non-negotiable rules

1. **A write procedure opens with `SET NOCOUNT ON; SET XACT_ABORT ON;`**, with a transaction wherever
   there is more than one statement, and always with `dbo.` in references.
   Why: without `NOCOUNT`, the rowcount of each DML can become a result set and the return silently
   disappears; without `XACT_ABORT`, a runtime error leaves a partial write. (B1; `lint P001/P002/P003`)
2. **The return is 1 result set, 1 row, 4 columns** (`status`, `description`, `id`, `url`), in every
   outcome, including zero rows written; `id` is text, nothing is `NULL`.
   Why: the flow reads `ResultSets/Table1[0]`; only the first result set arrives and one row fewer
   breaks the whole contract without an error. (C1; `lint P004`)
3. **`description` is an ASCII code from a closed vocabulary**; the sentence belongs to the flow.
   Why: the procedure does not build text; an unknown code in the flow answers `error` and never goes
   raw to the user. (C2; [procedure-standard.md](references/procedure-standard.md) §4)
4. **Every DML `OUTPUT` uses `INTO @table`.**
   Why: `OUTPUT` without `INTO` returns rows to the client (it steals the return) and fails on a table
   with a trigger. (`lint P011`)
5. **The flow decides, the procedure executes** (A2): **declarative** variant by default; the
   **classic** one (`IF` + `TRY/CATCH` + `THROW`) or the defensive authorization block only with an ADR
   and one of the signals in `security-and-permissions.md` §4.
   Why: the database tends to freeze and the rule has to stay editable without a DBA; the cost is that
   the database stops being the last barrier, and that has to be written down.
6. **The audit date comes from the database** (`SYSUTCDATETIME()` in the procedure, `Dt_Alteracao` in
   the trigger), never by parameter.
   Why: the client clock makes the row be born hours ahead of the others.
7. **Date filter for the app: column `Ref_<col> AS DATEDIFF(day, 0, <col>) PERSISTED`**, never
   `CAST(<date> AS INT)`.
   Why: a direct date filter does not delegate behind a gateway, and `CAST` rounds (1 pm becomes the
   next day). (B2; `lint P006`)
8. **An exact number does not come from `CountRows`:** count on the server (count procedure) or use
   `Sum` of a constant column; otherwise show the ceiling (`2,000+`).
   Why: `CountRows` does not delegate on the SQL connector and is silently wrong above the ceiling. (B3)
9. **Scope is a parameter resolved by the flow; the database obeys and fails closed:** `NULL` = all,
   code = one unit, `''` matches nothing; scope in `AND` with the user filter.
   Why: the connector account is shared and the screen filter is UX, not control (A3).
10. **The connector account has `GRANT EXECUTE` and `SELECT` where the app reads; no DML.**
    Why: this is what closes, by construction, a direct `Patch` on the table.
11. **Object and column names come from the environment** (`sys.procedures`, `sys.columns`), with the
    exact spelling: `AS-BUILT-NAMES` wins over the plan. (N1; `lint P005`)
    Why: the real name diverged from the documented one and the connector is case-sensitive: it fails
    at run time.
12. **Frozen database: the criterion is "does the object hold its own data?"**; a computed column is
    usually accepted, a table/column that holds data, a view or a signature change is usually refused. (B4)
    Why: planning the schema before the first deploy costs one request; afterwards, a negotiation.
13. **No dynamic SQL by concatenation** and no `NOLOCK`; `ERROR_MESSAGE()` never in the return.
    Why: injection, dirty reads and schema leakage. (`lint P009/P010`)
14. **Before delivering: `lint-procedure.py` with 0 errors** and the environment proofs run.
    Why: a validator that never flagged anything did not prove that it validates (P4); a procedure has
    already been delivered without ever having been compiled.

## Workflow

1. **Identify the task and load only its references:**

| Task | Load |
|---|---|
| Write or review a write procedure | `procedure-standard.md`, `assets/write-procedure-template.sql`, `proc-flow-contract.md` |
| Choose declarative vs classic | `procedure-standard.md` §5 and §7 |
| Read with filters, count, export | `procedure-standard.md` §9, `assets/read-function-template.sql`, `unit-scope.md` |
| Contract between procedure and flow, JSON parameter | `proc-flow-contract.md`, `assets/procedure-contract-template.md` |
| Table, column, key, flag, trigger, collation | `data-model.md` |
| "The date filter does not delegate", wrong counter, derived status | `computed-columns-delegation.md` |
| Unit scope, unit code | `unit-scope.md` |
| Connector account, GRANT, "does the procedure authorize?" | `security-and-permissions.md` |
| Package to the DBA, DDL request, frozen database, proofs | `deploy-and-dba.md`, `assets/dba-ddl-request-template.md` |
| Load from legacy into SQL Server | `data-migration.md` |
| Fictitious data in the DEV database to test screen and procedure (`mockup-load.sql`) | `skills/power-platform/references/mockup-load.md` §6 (orchestrator script `montar-carga-mockup.py`) |
| Understand what already went wrong in real projects | `field-lessons.md` |
| Audit existing procedures | run the lint (below) and `procedure-standard.md` §13 |

2. **Read the environment before writing** (N1, N3): procedure names (`sys.procedures`), tables and
   columns with type and nullability (`sys.columns`), PKs, nullable `Flg_*`, collation and
   compatibility level. Ready-made queries in `data-model.md` §10 and `deploy-and-dba.md` §3. A name
   that was not read from the environment is a **hypothesis**: mark it.
3. **Choose the variant** (`procedure-standard.md` §5). Without a signal to the contrary, declarative.
   Record in the contract which one it was and why.
4. **Write from the template**, one business action per procedure; parameters in five classes
   (a PK, b values, c caller, d trail, e flags); state literals in the body.
5. **Write the contract** (`assets/procedure-contract-template.md`): signature with class, code table,
   flow obligations, acceptance tests. Check it against the flow (`proc-flow-contract.md` §4).
6. **Run the lint and the proofs** (table below and `deploy-and-dba.md` §3). Fix at the source, not in
   the generated `.sql`.
7. **Deliver to the DBA** (`deploy-and-dba.md`): hand-written DDL, numbered procedures, `GRANT` last,
   items on hold marked.
8. **Close with the project gate** (`power-platform` skill).

## References

| File | When to read |
|---|---|
| [procedure-standard.md](references/procedure-standard.md) | envelope, return, code vocabulary, declarative vs classic, `UPDLOCK/HOLDLOCK`, parameters, `OUTPUT` |
| [proc-flow-contract.md](references/proc-flow-contract.md) | what the procedure promises, flow obligations, divergence checklist, JSON parameter |
| [data-model.md](references/data-model.md) | prefixes, audit, trigger, flags, role, collation, `CHAR`, unique indexes |
| [computed-columns-delegation.md](references/computed-columns-delegation.md) | date `Ref_`, count, derived status, index, delivery to the DBA |
| [unit-scope.md](references/unit-scope.md) | the three scope states, list via JSON, prefix-free codes, `StartsWith` and `NULL` |
| [security-and-permissions.md](references/security-and-permissions.md) | service account, what the procedure authorizes, when to disagree with A2, verification queries |
| [deploy-and-dba.md](references/deploy-and-dba.md) | script order, environment proofs, freeze, as-built names, final check |
| [data-migration.md](references/data-migration.md) | load playbook: staging, validation, trigger, reseed, reconciliation, rollback |
| [field-lessons.md](references/field-lessons.md) | defects the adversarial review found, the bridge between proposed and real schema, divergence that disappears |
| `assets/write-procedure-template.sql` | template for a state UPDATE and a guarded INSERT (passes the lint) |
| `assets/read-function-template.sql` | inline function with `@Filtros` JSON + scope, count and listing |
| `assets/procedure-contract-template.md` | contract per procedure, with parameter classes and codes |
| `assets/dba-ddl-request-template.md` | DDL request with criterion, proof, risk and rollback |

## Scripts

`<skill-folder>` is the *Base directory* shown when the skill is loaded. Run **from the project
root** (the script looks for `power-platform.config.json` from the current directory upward) or pass
`--config`. They only **read**; they do not write to disk.

| Command | What it checks | Exit |
|---|---|---|
| `python <skill-folder>/scripts/lint-procedure.py <folder or file>` | each `CREATE/ALTER PROCEDURE\|FUNCTION` in `.sql` and in ```` ```sql ```` blocks in `.md`: `P001` NOCOUNT, `P002` XACT_ABORT, `P003` TRAN without COMMIT, `P004` 4-column return, `P005` name, `P006` date CAST to INT, `P007` `SELECT *`, `P008` no schema, `P009` concatenated dynamic SQL, `P010` NOLOCK, `P011` OUTPUT without INTO | 0 no error · 1 with error · 2 incorrect use |
| `python <skill-folder>/scripts/lint-procedure.py` | with no argument uses `pastas.procedures` and `ignorar` from `power-platform.config.json` | same |
| `python <skill-folder>/scripts/lint-procedure.py x.sql --padrao-nome "^usp_\w+$"` | name regex (default accepts `usp_` and `SP_`); also `padrao_nome_procedure` in the config | same |
| `python <skill-folder>/scripts/lint-procedure.py x.sql --colunas-retorno ""` | turns `P004` off; also `colunas_retorno_procedure` in the config | same |

Output: `path:line: ERROR|WARNING P0xx message` and `N error(s), M warning(s)`. Comments and literals
are ignored when matching patterns. Dismiss a line with `-- lint-ok P009` and **one sentence saying
why**. The lint does not replace compiling on an instance: it resolves neither names nor types.

## Definition of done

Each item has executable evidence; "done" without a command and its output does not count. Commands from the project root (note in Scripts).

- [ ] `python <skill-folder>/scripts/lint-procedure.py <folder>` -> `0 error(s)`; remaining warnings have a written decision
- [ ] the procedure compiles on a DEV instance (`SET PARSEONLY ON` is not enough) and the N-1 test passes:
      `EXEC` of each write procedure returns **1** result set, **1** row, **4** columns, also
      when it writes zero rows
- [ ] environment proofs run and pasted (`deploy-and-dba.md` §3): `COMPATIBILITY_LEVEL >= 130` if there is
      JSON, `OUTPUT ... INTO` with an active trigger, app identity vs column, collation
- [ ] the queries in `security-and-permissions.md` §7 come back empty: account without DML (direct and by role); `NOCOUNT` in every
      procedure and trigger; no unreviewed dynamic SQL
- [ ] code vocabulary the same in the `.sql`, in the contract and in the flow `Switch`
      (`proc-flow-contract.md` §4, items 1 to 8)
- [ ] no nullable `Flg_*` column (query in `data-model.md` §4 empty) and prefix-free unit codes,
      if it uses `StartsWith` (query in `unit-scope.md` §5 empty)
- [ ] the four scope tests in `unit-scope.md` §8 give the expected results
- [ ] DDL request filled in with the real output of the queries, with no placeholder
- [ ] the contract says which variant, which obligations the flow has and what the trail does **not** prove

## Pitfalls

The ten most expensive:

1. **No `SET NOCOUNT ON`** (including in a trigger): the return changes without an error.
   [procedure-standard.md §2](references/procedure-standard.md), [data-model.md §3](references/data-model.md)
2. **`OUTPUT` without `INTO`**, or reading `Dt_Alteracao` through the `OUTPUT` of a table with a trigger.
   [procedure-standard.md §11](references/procedure-standard.md)
3. **`CAST(<date> AS INT)`** in a filter column: it rounds.
   [computed-columns-delegation.md §3](references/computed-columns-delegation.md)
4. **Scope `NULL` going through `coalesce`** in the flow: it becomes `''` and the report comes back empty.
   [unit-scope.md §2](references/unit-scope.md)
5. **A parameter the exact size of the value** (`NVARCHAR(36)` for a GUID): it truncates silently.
   [procedure-standard.md §10](references/procedure-standard.md)
6. **Nullable `Flg_*`**: `NULL` in a flag denies (or allows) everything, with no second line of defense.
   [data-model.md §4](references/data-model.md)
7. **Identity with two columns** (e-mail in the app, UPN in the procedure): every write denied.
   [security-and-permissions.md §5](references/security-and-permissions.md)
8. **`@Id_UsuarioChamador` treated as proof of authorship**: it is the caller's declaration.
   [security-and-permissions.md §5](references/security-and-permissions.md)
9. **Running the generator over a hand-corrected baseline**, or using a procedure name from the
   documentation instead of the real one. [deploy-and-dba.md §7](references/deploy-and-dba.md)
10. **Asking the DBA for a new table/view/column after the freeze** without the output that the screen
    or the flow would have without it. [deploy-and-dba.md §6](references/deploy-and-dba.md)
