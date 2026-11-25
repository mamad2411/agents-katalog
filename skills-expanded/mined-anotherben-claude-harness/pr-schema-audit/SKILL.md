---
name: pr-schema-audit
description: "Audit GitHub pull requests against the live Helpdesk Postgres schema. Use when asked to check a PR, merged PR, open PR, schema drift, SQL call coverage, database variables, or PR review failures against live database shape; publishes bug-labeled issues for merged or closed failing PRs and PR conversation comments for open failing PRs when publication is explicitly requested."
---

# PR Schema Audit

Use this skill to run an audit-only schema check for a Helpdesk GitHub PR. It reads the PR diff and changed files from GitHub, resolves database calls and SQL variables, compares referenced tables, columns, indexes, and constraints against the live dev Postgres schema, and reports coverage gaps as failures instead of guessing.

## Guardrails

- Never paste or store the database URL in this skill.
- Read the URL from `HELPDESK_SCHEMA_AUDIT_DATABASE_URL` or from `~/.codex/secrets/helpdesk-schema-audit-db-url`.
- Keep the secret file owner-only. The script refuses group or world-readable secret files.
- Use the full skill body and bundled scripts from the invoked skill directory.
  Keep the Codex and Claude copies in sync; do not create a second secret or
  replace either copy with a redirect-only wrapper.
- Do not edit repo code, run migrations, execute application write workflows, or fix findings.
- Default to dry-run. Add `--publish` only when the user asked for GitHub publication or the current task explicitly authorizes it.
- For open PRs, publication creates a PR conversation comment. For merged or closed PRs, publication opens a GitHub issue labeled `bug`.

## Workflow

1. Restate the target PR, repo, and whether publication is authorized.
2. Confirm `gh` is authenticated and run from a Helpdesk checkout or pass `--repo anotherben/helpdesk`.
3. Confirm a secret reference exists without printing its value:

```bash
test -n "$HELPDESK_SCHEMA_AUDIT_DATABASE_URL" || test -f "$HOME/.codex/secrets/helpdesk-schema-audit-db-url"
```

4. Run the audit. For proof or exploration, keep dry-run:

```bash
/Users/ben/.codex/skills/pr-schema-audit/scripts/pr-schema-audit.cjs --repo anotherben/helpdesk --pr 123 --dry-run --output /tmp/pr-schema-audit-123.md
```

5. For an authorized audit that should post findings:

```bash
/Users/ben/.codex/skills/pr-schema-audit/scripts/pr-schema-audit.cjs --repo anotherben/helpdesk --pr 123 --publish --output /tmp/pr-schema-audit-123.md
```

6. Evaluate any residual `DB call is not statically resolved` finding before trusting the verdict. The script already auto-handles the common false positives (see Edge-Case Handling), so a surviving one is either a real gap or a new construct the resolver does not yet model. For each such finding, do not report it blindly — evaluate it:

   - Read the exact source span at the PR head (`gh api repos/<repo>/contents/<file>?ref=<headSha>` decoded from base64, or the local checkout). The finding's `Detail` column already quotes the offending source line to point you there.
   - Classify the construct:
     - **Wrapper / callback** (`.transaction`, `.task`, `.tx`, or any DB method whose argument is a function): no SQL of its own; its nested `.query`/`.execute` calls are scanned independently. Not a real gap. If the resolver still flagged it, note the new wrapper shape so the script can be extended.
     - **No-SQL builder** (query-builder / ORM chain with no raw SQL string): no schema surface to verify. Note and clear.
     - **SQL from an imported constant or helper** in another file: follow the import, resolve the SQL text, and verify its tables/columns against the live schema yourself. Report the result of that verification.
     - **Genuinely dynamic / concatenated SQL** with table or column surface: this remains a real HIGH coverage gap. Keep it and quote the source proof.
   - Reflect the evaluation in your written summary: either reclassify with cited source proof, or confirm the HIGH with the quoted span. Never downgrade without direct source proof.

7. Treat the report verdict mechanically, after the evaluation in step 6:

- `DO NOT MERGE` means at least one critical or high finding exists.
- `NEEDS REVIEW` means at least one medium finding exists.
- `PASS` means all resolved database references matched the live schema and no required publication was needed.

## Coverage Standard

The script scans every changed source file with a JavaScript, TypeScript, or SQL extension. It records:

- DB calls such as `.query`, `.execute`, `.raw`, `.many`, `.one`, `.none`, `.transaction`, and `sql` templates.
- SQL strings assigned to variables in changed files.
- SQL files in the PR.
- `process.env` variables in changed files.
- Secret-shaped literals.

Unresolved dynamic SQL or unreadable changed files are high-severity coverage failures. Do not downgrade them without direct source proof.

## Edge-Case Handling

The script auto-resolves edge cases that previously produced false-positive HIGH findings, and surfaces the rest for evaluation instead of flagging them blind. Every class below was found auditing real Helpdesk PRs (2766–2797) and is locked by a case in the offline parser guard.

Call-site / resolution:
- **Transaction and callback wrappers** — `.transaction(async (client) => { ... })`, or any DB method whose first arg is a function (arrow/async/`function`, incl. the options-object-plus-callback form). No SQL of their own; nested `.query`/`.execute` calls are scanned independently. Counted as `wrapperDbCalls`.
- **Object arguments** — `db.query({ text|sql: '...' })` resolves to the embedded SQL; `service.execute({ ...non-SQL... })` is recognized as a non-DB call, not an unresolved one.
- **Ternary-of-literals** — `db.query(cond ? 'SELECT ...' : 'SELECT ...')` and `const q = cond ? '...' : '...'` resolve to a literal branch and are verified.
- **Same-file SQL functions** — `db.query(buildSelect())` resolves to the SQL returned by a same-file `function buildSelect() { return '...' }` / `const buildSelect = () => '...'`, and that SQL is verified.
- **Spread forwarding** — `client.query(...args)` is a pass-through wrapper, not a SQL site.
- **JS comments** are blanked before parsing, so a commented-out `// db.query(...)` is never treated as a real call.

SQL parsing:
- **Comments and string literals** inside SQL are stripped/masked, so prose in `-- ...` or keywords inside `'... from ...'` string values are not read as tables.
- **Non-SQL strings** (e.g. an HTML email template containing `<table>`/"from") are excluded — a value is treated as SQL only if it begins with a statement keyword.
- **Functions and keywords after FROM/JOIN** — set-returning functions (`UNNEST(...)`, `jsonb_to_recordset(...)`), `LATERAL`, `FOR UPDATE [SKIP LOCKED|OF ...]`, `EXTRACT(field FROM INTERVAL|CURRENT_DATE|...)` are not mistaken for tables.
- **Named arguments** — `make_interval(hours => ...)` is not mistaken for a `SET hours =` column.
- **System catalog and materialized views** — unqualified `pg_*` catalog relations resolve as system tables, and materialized-view columns are read from the catalog (they are absent from `information_schema.columns`).
- **CTE / derived-subquery aliases** — an alias bound to a CTE or `(SELECT ...) x` (even when the same alias name is reused for a base table in an inner scope) is treated as having computed columns, not flagged.
- **PR-created tables** — `CREATE [TEMP] TABLE` / `CREATE TABLE AS` names (test fixtures, not-yet-applied migrations) are excluded like CTE names.

Files and robustness:
- **Removed files** (deleted in the PR) are skipped, not reported as "could not be read".
- **Transient GitHub failures** (rate limit, flaky auth/401, 5xx, network) are retried; only a persistent read failure is reported.

Secrets:
- A connection-string credential that embeds a placeholder word (`dev-password`, `super-secret-password`, ...) is treated as a test fixture; a high-entropy real credential is still flagged CRITICAL.

**Genuinely unresolved calls** (dynamic builders, SQL read from a file at runtime, concatenated SQL, identifiers defined out of file) remain HIGH, but the finding's `Detail` quotes the offending source line so it can be evaluated from the report alone. Run the step 6 evaluation on each before trusting the verdict.

When the resolver meets a new wrapper shape it does not yet model, extend `isFunctionArg`/`calls` in `scripts/pr-schema-audit.cjs` rather than downgrading the finding by hand, and add a case to the offline parser guard so it stays fixed:

```bash
node /Users/ben/.codex/skills/pr-schema-audit/scripts/pr-schema-audit.test.cjs
```

## Output Requirements

A valid run produces:

- Zoom-out trace: PR metadata, changed files, source parsing, live schema read, and publication route.
- Blast radius counts: files, DB calls, resolved SQL, recognized wrapper calls, table refs, column refs, env vars, live schema size.
- Coverage ledger for every changed source file scanned or skipped.
- Live schema verification table for each resolved SQL statement.
- Findings table with stable `PSA-*` IDs.
- Publication plan and result.
- Trace boundaries that state what was not executed.

The report is the deliverable. Do not fix code from this skill.
