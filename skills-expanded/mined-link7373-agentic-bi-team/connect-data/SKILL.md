---
name: connect-data
description: Connect the team to a data source and prove it works — walks through MCP, CLI, or file access one source at a time, runs a live test query, and records only what actually succeeded in knowledge/data-sources.md. Use during setup, when adding a source, or when a connection breaks.
---

# Connect Data — One Source, Actually Tested

Everything the team does depends on reaching the data. This skill gets one source
connected and **proves it**, then writes the evidence down.

The rule that makes this skill worth having: **a source is not connected until a query
you ran returned rows.** Not when the credentials look right, not when the CLI is
installed, not when the user says it works. An untested ✅ in `data-sources.md` is worse
than an honest ❌ — it produces agents that plan confidently against data they cannot
reach, and the failure surfaces three steps later inside somebody's analysis.

Read `knowledge/connections.md` first. It is the plain-English cookbook this skill
automates; the user may already have read it.

## Procedure

### 1. Take one source at a time

Ask which source, and what the user already has. Don't try to connect everything at
once — partial success is normal and useful, and batching hides which thing broke.

Establish which of the three patterns applies (`knowledge/connections.md` covers all
three in detail):

| Pattern | Looks like | Test method |
|---|---|---|
| **MCP server** | a warehouse connector configured in Claude Code | call the MCP query tool directly |
| **CLI client** | `psql`, `bq`, `snowsql`, `duckdb`, `sqlite3`, `mysql` in the shell | `scripts/test_connection.py` |
| **Files** | CSV/Parquet exports in the repo | read one and count rows |

If none apply yet, say so plainly and offer the file path or demo mode
(`python demo/generate_demo_data.py`) rather than leaving the team unconnected. Working
against a small export beats waiting a week for warehouse access.

### 2. Find the command that works

For the CLI pattern, construct the smallest possible read-only query and iterate with
the user until it runs:

```bash
python scripts/test_connection.py --name "prod-replica" \
  --cmd 'psql "$PROD_REPLICA_URL" -c "SELECT 1"'
```

The script refuses any command containing a write or DDL keyword, times out, and treats
"succeeded with no output" as a failure — a command that prints nothing has not proved
anything.

**Credentials go in environment variables, never in the command you record and never in
a tracked file.** `.env.example` lists the variables each warehouse family expects; the
user copies it to `.env` (gitignored) or sets them in their shell profile. If a
credential is missing, stop and ask — do not invent a connection string, and do not ask
the user to paste a password into the chat.

**Ask for read-only.** A read replica or a read-only role is the right default. Say why
when you ask: the team runs exploratory queries constantly, and a read-only credential
turns a whole class of accident into an error message.

**Ask for scoped, too.** The best credential reads the curated marts the team needs and
nothing else — no raw tables of personal data, no grant on sensitive columns. That is a
stronger control than anything in this repo: the query guard in
`scripts/hooks/guard_data_access.py` only matches names in text, while a role the
warehouse refuses is refused. If a narrower role is not available yet, record that as an
open item rather than a preference.

### 3. Register it so it can be re-tested

Add the source to `scripts/connections.json` so `/health-check` and future runs can
re-verify it without rediscovering the command:

```json
[
  {"name": "prod-replica",
   "cmd": "psql \"$PROD_REPLICA_URL\" -c \"SELECT 1\"",
   "expect": "1"}
]
```

The file holds commands and **variable names**, never values. If a connection genuinely
cannot be expressed without a secret, leave it out of the registry and note in
`data-sources.md` that it must be tested manually.

### 4. Go past "SELECT 1"

A connection that can run `SELECT 1` may still be unable to see the tables that matter.
Before recording success, confirm:

- **Tables are visible:** list schemas and tables the credential can actually read.
- **A real table returns rows:** query one row from a table the team will use.
- **Row counts look plausible:** an empty or suspiciously tiny core table means the
  credential is pointed at the wrong database or a sandbox — a very common and very
  expensive mistake to find later.
- **Cost and size:** how big are the core tables, and does a scan cost anything? Record
  the cost guardrail in `data-sources.md` so agents can estimate before they scan.
- **What is sensitive:** list the columns from the schema — names and types, not values —
  and hand them to `governance-officer` to classify. Anything personal gets a row in the
  Column Registry of `knowledge/governance-policy.md` *before* anyone queries the table,
  because the guard cannot protect a column it has not been told about. A source that
  holds personal data the team has not handled before goes through `/privacy-review`.

### 5. Record what you proved

Update `knowledge/data-sources.md`:

```bash
python scripts/test_connection.py --write
```

That fills in the status cell of each Connection Summary row. Then write, by hand, the
parts a script can't know:

- the **exact working command**, so nobody rediscovers it next session
- **what the credential can and cannot see** (which schemas, read-only or not)
- for a blocked source, **what specifically is needed to unblock it** and who can grant
  it — "needs the `analytics_ro` role on the replica, IT ticket" is actionable; "no
  access" is not
- the **expected refresh window** per major table — `data-quality-engineer`'s freshness
  monitoring has nothing to compare against without it
- any **quirk** you tripped over, in the known-quirks section, while it's fresh
- the **classification** of each documented column in the Data Dictionary, matching the
  Column Registry — then `python scripts/check_governance.py` to confirm the two agree

### 6. Hand back

Report which sources are live, which are blocked and why, and what the team can now do
that it couldn't before. If this was the first working connection, suggest schema
discovery (`/setup-team` step 8) or a first `/analyze` to shake out anything the test
query didn't reach.

## When a connection breaks

Same procedure, shorter: re-run `python scripts/test_connection.py`, read the actual
error rather than guessing, and check the usual suspects in order — expired credential,
rotated password, changed host, revoked role, network or VPN, quota exhausted. Flip the
row to ❌ with the real error text immediately, so no agent trusts it in the meantime,
and log it in `knowledge/data-quality-log.md` if the outage affected reported numbers.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
