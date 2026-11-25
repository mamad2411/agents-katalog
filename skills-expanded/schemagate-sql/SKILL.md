---
name: schemagate-sql
description: Answer questions about data in a SQL database through the schemagate MCP server, using only the tables and columns the caller may read. Use when the user asks a question that needs a query against a database schemagate is connected to.
license: Apache-2.0
---

# Querying a database through schemagate

schemagate is a read-only MCP server. It holds the database's structure in
memory and, for each question, returns DDL for only the objects the caller
may read. Work from what it returns, not from guesses about the schema.

## Workflow

1. **Select the schema first.** Call `select_schema` with the user's question.
   Pass `principal` and `roles` when you know who is asking. A principal is
   namespaced, for example `okta:jdoe` or `db:APP_USER`. Without them the
   caller is anonymous and sees only unrestricted objects.
2. **Write one SELECT against that DDL only.** Use the tables and columns in
   the `ddl` field and nothing else. If the DDL starts with a note that the
   caller may read only part of the database and the question needs data that
   is not shown, tell the user the answer is not available to them instead of
   approximating it from other columns.
3. **Run it with `run_query`**, passing the same `principal` and `roles`. It
   accepts a single read-only SELECT and returns rows, capped by `max_rows`.
4. **Report refusals as refusals.** An error that says `not available to this
   caller` means the query named something outside the caller's scope. Say so;
   do not report it as "no results" and do not retry with other roles.

## Other tools

- `describe_object`: full DDL for one table or view when the compact DDL is
  not enough. A restricted object and a missing one give the same error.
- `list_objects`: everything this caller may read. Long on a large database;
  use `select_schema` to answer a question.
- `refresh_catalog`: re-read the structure after a migration or a grant change.
- `health`: server status, object count, and whether the catalog is stale.
- `answer`, `semantic_query`, `deep_answer`: need a model provider configured
  on the server. Without one, `answer` returns the scoped schema for you to
  write the SQL yourself, and the other two report that they are off.

## Limits

- Over stdio, the server trusts the `principal` and `roles` the client sends.
  It scopes what the model sees; it does not authenticate anyone.
- A table the selection left out cannot be queried from the prompt. If the
  DDL looks incomplete for the question, call `select_schema` again with a
  more specific question or use `describe_object`.
