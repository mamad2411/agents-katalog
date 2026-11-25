---
name: audit-sql-filtering
description: Audit Joomla filter, user-state, and user-input values that reach SQL queries for unsafe validation, escaping, or parameterisation. Use for SQL injection reviews of a Joomla extension, or when explicitly invoked for SQL filtering analysis. For missing authentication/authorisation/CSRF checks see audit-authz; for privilege mismatches, backend-task leakage, or unsafe uploads see audit-controller-exposure.
---

# Audit SQL filtering

Audit this repository's Joomla extensions for unsafe validation or escaping of data that ends up in
SQL queries.

## Context

Filter values — from filter subforms, from user state via `getUserStateFromRequest()`, or straight
from user input — flow into the Model and build the queries that count and select records. Unsafe
values there are a prime source of SQL injection, including blind and bit-oracle attacks where a
record either appears or does not, leaking one bit at a time.

Severity follows attack surface:

- **Administrator views** — requires an authenticated administrator. Lowest.
- **Site (frontend)** — may be guest-accessible or low-privilege. More severe.
- **Api application** — comparable to the frontend, depending on how the site is configured.

### What correct looks like in Joomla

- Retrieve each value with the appropriate filter: `$app->getInput()->getInt()`,
  `->getCmd()`, `->getWord()`, `->getUint()` — not `->get()` with no filter, and not `->getString()`
  for something that will be compared as a number.
- Type-cast non-string values explicitly, e.g. `(int)`.
- **Always use prepared queries with explicit named parameters** for every value originating from a
  filter, from user state, or from user input:

  ```php
  $query->where($db->quoteName('a.catid') . ' = :catid')
        ->bind(':catid', $catid, ParameterType::INTEGER);
  ```

Watch specifically for:

- `$db->quote()` / `$db->escape()` used as the only defence on a value that is then concatenated into
  the query. Escaping is not parameterisation, and it is wrong outright for identifiers.
- Values interpolated into `ORDER BY`, `GROUP BY`, column lists, or `LIMIT` — these cannot be bound,
  so they must be validated against an allow-list of known-good column names and directions.
  `list.fullordering` from a filter form is the classic case.
- `$db->quoteName()` receiving an unvalidated value.
- Raw SQL fragments assembled in a helper or a `Table` subclass, away from the model where you were
  looking.

## Scope of this audit

This audit is scoped to SQL injection specifically.

For missing authentication, authorisation, or anti-CSRF checks see `audit-authz`. For checks that
exist but target the wrong permission, backend-only tasks leaking into the frontend or api, and
unsafe uploads, see `audit-controller-exposure`.

## Workflow

### Step 1 — Audit

Report each vulnerable location with file, line, the path the value takes from its source to the
query, which application it is reachable from, and an estimated severity by that surface. Follow it
with a comprehensive itemised list of proposed mitigations.

Present the list for the user's review before applying anything.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context — a validating layer you did not read, or a value that cannot in fact be attacker-controlled.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-sql-filtering` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
