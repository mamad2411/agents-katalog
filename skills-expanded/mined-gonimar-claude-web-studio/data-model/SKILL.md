---
name: data-model
description: "Designs or extends the data model — entities and relations, PostgreSQL DDL with constraints and indexes justified by queries, expand/contract migration strategy, PII classification, backup/restore — into docs/architecture/data-model.md and migration drafts. Run after /api-contract and before build, or for 'design the schema', 'add a table', 'write the migration'."
argument-hint: "[feature F-NNN or 'full']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
---

# Data Model

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

Template `.claude/docs/templates/data-model.md`; reference `database.md`; rules `database.md`. This skill delegates nothing: the schema, the DDL and the migration drafts are the database engineer's own work, so `Task` is not among its tools. In the commands below, `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode.

## Phase 1: Context
1. **Scope** from the argument: `F-NNN` → that feature spec's section 4. No such feature spec → verdict `BLOCKED (no feature spec — run /feature-spec first)`; write nothing. `full` → every feature spec and the whole schema.
   **No argument** → nothing is assumed. Read `production/session-state/active.md`: when its `Task:` names a story (`S-NNN`) whose feature spec exists, propose that feature; then one `AskUserQuestion`: that `F-NNN` (Recommended when proposed) · another feature from `docs/specs/features/` (listed) · `full`. With no feature specs at all the answer can only be `full` or `BLOCKED` as above.
2. **Read** the current schema (migrations, `schema.sql`, AR/entity classes), the API contract (which fields we expose), the threat model (PII).

## Phase 2: Entities and queries
1. ER (mermaid) and a query table (frequency, read/write).
2. Questions: volumes, retention, invariants.
3. **Personal data** (template §6), per PII field:
   - its class (identity, contact, behavioural, financial, special category);
   - its **retention period** and what ends it (account deletion, inactivity, legal term);
   - the deletion or anonymisation method per table (hard delete, tombstone + anonymise, crypto-shredding), and what happens in backups and logs.
   Export on request is described as the template asks (what is included, format, identity check). A deletion path that does not exist becomes the "Data deletion" story (`/create-stories`).

## Phase 3: DDL and migrations
1. DDL with CHECK/UNIQUE/FK/indexes, each index justified by a query from the Phase 2 table.
2. Migrations in the project's tool (the stack reference names it: e.g. golang-migrate, yiisoft/db-migration, Doctrine Migrations, Drizzle); expand/contract when changing existing tables.
3. With a DB available (compose): `EXPLAIN ANALYZE` on test data.

## Phase 4: Write
1. When valuable data is added, the draft includes the updated backup section (template §7).
2. "May I write `docs/architecture/data-model.md` and the migration files?" — one `AskUserQuestion`: write (Recommended) · show the draft/diff first · not now. After the "write" answer: `touch .claude/.write-consent` (rule 7 — the consent-guard hook checks the marker).

## Phase 5: Commit (documents lane)
Right after the write, one commit gate (rule 7 (4), `.claude/docs/git-workflow.md` § Documents): one `AskUserQuestion` offering `docs: data model <F-NNN | full>`, staging exactly the written files — `docs/architecture/data-model.md`. Record the gate before asking — `<hooks>session-state.sh set Gate "/data-model Phase 5: commit?"` — and clear it after the answer (`<hooks>session-state.sh set Gate "—"`).
- On the default branch when no story work is in progress.
- When HEAD is a story branch, name it and offer: switch to the default branch and commit there (Recommended — a pipeline-wide document) · commit here (the document belongs to this story) · leave uncommitted.
- Code, configs, workflows and scripts never ride the `docs:` commit: the migration drafts are code and stay out of it — name them in the result; they land in the branch of the story that applies them (`/dev-story`).

Nothing is committed without the answer.

Verdict: `APPROVED` | `NEEDS REVISION` | `BLOCKED`. Next step — one `AskUserQuestion`: `/create-stories` (Recommended) · `/api-contract` (if the contract changes) · revise the model; on `BLOCKED`: `/feature-spec` (Recommended) · stop here.
