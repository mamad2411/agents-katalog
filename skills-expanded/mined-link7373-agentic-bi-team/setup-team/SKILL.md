---
name: setup-team
description: Onboard or re-onboard the Agentic BI team — reads the user's plain-English START-HERE.md, interviews them about gaps, and propagates everything into CLAUDE.md and the knowledge/ files, replacing all placeholders. Run once at the start and again after major business changes.
---

# Setup Team — Charter Ingestion

You are configuring the entire Agentic BI team from the user's plain-English charter.
Be thorough: after this runs, the team should function without the user re-explaining
their business.

This is the highest-stakes skill in the kit. It rewrites around forty files in one pass,
and everything the team does afterwards is built on what you write here. Two consequences:
**take a snapshot before you write anything**, and **show the user your mapping before
you apply it** — a wrong company description quietly poisons every deliverable for
months.

## Procedure

### 0. Pre-flight — make this undoable

1. Check `git status`. If the working tree is dirty, say so and let the user decide
   whether to commit first; a clean tree means `git diff` alone will show them
   everything setup did.
2. Take a snapshot regardless of what git says:

   ```bash
   python scripts/setup_backup.py
   ```

   Note the snapshot id and tell the user the one command that undoes everything:
   `python scripts/setup_backup.py --restore <id> --yes`. Do this even on a re-run —
   *especially* on a re-run, when there is accumulated knowledge to lose.
3. Confirm the tooling is present: `python scripts/check_placeholders.py --list` should
   print an inventory. If Python is missing, setup can still proceed by hand — say so,
   and skip the script-based steps rather than pretending they ran.

### 1. Read the charter — or offer the demo

Read `START-HERE.md`.

- **Filled in:** continue to step 2.
- **Still the blank template:** offer three paths and let the user pick.
  1. *Fill it out* — they answer the questions and come back. Best result.
  2. *Interview* — you ask the charter questions conversationally, a few at a time,
     and write their answers into `START-HERE.md` as you go so the record exists.
  3. *Demo mode* — see below. Best for someone evaluating the kit.

**Demo mode.** The user gets a fully working team against a fictional B2B SaaS company
with no warehouse and no credentials, in about ten minutes:

```bash
python demo/generate_demo_data.py
```

Then use `demo/DEMO-CHARTER.md` as the charter for every step below, and record the data
connection as SQLite against `demo/demo.db` (query it with
`python demo/query_demo.py "<sql>"`, or the `sqlite3` CLI). Copy
`demo/domain-subscriptions.md` to `knowledge/domains/subscriptions.md` and add its row
to the index in `knowledge/domains/README.md` — it is the worked example of a domain
reference doc. Tell the user plainly that this
is synthetic data for evaluation, that `demo/demo.db` is gitignored, and that re-running
`/setup-team` with a real charter switches the team over. Suggest they try
`/scorecard weekly` and then `/investigate-metric` on churn — the demo data has real
findings planted in it.

### 2. Inventory the placeholders

```bash
python scripts/check_placeholders.py --list
```

This lists every placeholder, how often it appears, and where. Two forms, and they are
handled differently:

- `{{UPPER_SNAKE}}` — **you fill these.** They must all be gone when you finish.
- `{{lowercase prose}}` — a blank the user fills per entry when they write a log entry
  or a metric definition. **Leave these alone**; they are part of the templates.

### 3. Map charter → placeholders

Extract from the charter: company, industry, business model, products, priorities,
north-star metric, fiscal/timezone/currency, data sources and connection methods, data
sizes and known issues, existing metrics, audiences, scorecard cadence, BI tool,
deliverable formats, branding, ML interests, environment, privacy rules, never-do list,
pre-authorisations, jargon, and context notes.

**Governance answers map to `knowledge/governance-policy.md`** — the one file the query
guard, output scan, and audit log read, so get these right:

| Charter answer (section 6) | Policy value |
|---|---|
| Strictness: relaxed / careful / locked down | `enforcement:` `advisory` / `guarded` / `strict`. No answer → `guarded`. |
| Privacy or compliance rules named (GDPR, CCPA, HIPAA, PIPEDA) | `regimes: [...]`, lowercase. None named → `regimes: []`. Never enable a regime the user did not name. |
| Minimum group size, or none stated | `min_group_size:` their number, else `5` |
| Kinds of personal data they hold | Column Registry rows, completed in step 8 once the schema is known |
| Where reports may go; how long copies are kept | the export-destinations and retention placeholders in Standing Rules |
| Who decides privacy questions; who owns the data | the privacy-contact and data-owner placeholders in Roles |

If the charter names HIPAA, or says the data is health data, read
`standards/privacy/hipaa.md` section 2 now and raise its first point with the user before
connecting anything: the team reads no protected health information until they confirm the
deployment is covered by a business associate agreement.

### 4. Clarify gaps — efficiently

Collect everything ambiguous or missing into **one batched set of questions** (use
AskUserQuestion where available, max ~4 at a time, most important first). Apply sensible
defaults for the rest and say which defaults you chose. Reasonable defaults: weekly
scorecard Monday, monthly on 1st business day, Markdown + Excel deliverables, "ask
before anything destructive or external", calendar fiscal year, minimum group size 5.

### 5. Dry run — show the mapping before writing

Present the complete placeholder → value table to the user and get an explicit go-ahead.
Flag anything you inferred rather than read, and anything you defaulted. This is the last
cheap moment to catch a wrong answer; after this it's forty files of find-and-replace.

If the user asked for a dry run only, stop here and write nothing.

### 6. Verify data access — the make-or-break step

Run `/connect-data` for each source named in the charter. It tests the connection with a
live query and records the result in `knowledge/data-sources.md` in a consistent format.

Do not mark a source as available without a query that actually returned rows. A source
recorded as working when it isn't produces an agent that confidently plans against data
it cannot reach — the single most expensive failure mode in this kit. ❌ with a clear
"what's needed to unblock" is a good outcome; an untested ✅ is not.

### 7. Write everything

- Replace every `{{UPPER_SNAKE}}` placeholder in `CLAUDE.md` (sections 1, 2, 6, and
  principle 9, plus any others).
- Replace placeholders inside `.claude/agents/*.md` and `.claude/skills/*/SKILL.md`
  (`{{SOURCE_SYSTEMS}}`, `{{BI_TOOL}}`, `{{ML_ENVIRONMENT}}`, `{{DELIVERABLE_FORMATS}}`,
  `{{COST_GUARDRAIL}}`, `{{MIN_GROUP_SIZE}}`, …).
- Populate `knowledge/business-context.md`, `knowledge/data-sources.md`, and
  `knowledge/stakeholders.md` fully from the charter and clarifications, including the
  stakeholder SLA table.
- Seed `knowledge/metrics-catalog.md`: enter the user's existing metrics, and draft 5–10
  recommended KPIs for their business model (marked DRAFT, for `metrics-steward` review
  via `/define-kpis`). **Every entry needs its machine-readable YAML block** — at minimum
  `name`, `definition`, `grain`, `owner`, and `generic_sql`. Write `generic_sql: TODO`
  rather than inventing a formula against tables you haven't confirmed exist.
- Fill in `knowledge/governance-policy.md`: the policy block, Standing Rules, and Roles,
  from the mapping in step 3. Write the `yaml` values bare (`enforcement: guarded`,
  `regimes: [gdpr, ccpa]`) — the guards parse that block, and a sentence where a value
  belongs resolves to the default.
- Fill in `knowledge/incident-runbook.md`: who to notify, and through what channel.
- Initialise `knowledge/decision-log.md` with a "Team onboarded" entry summarising the
  configuration decisions and the defaults you applied.
- Fill the standards files' placeholders (brand colours, semantic colours, load target,
  review cadences, tool-specific sections).

### 8. Schema discovery (if data access works)

Introspect the connected databases: list schemas and tables, row counts for the major
ones, and write a table inventory into `knowledge/data-sources.md`. Note anything that
looks like a core fact table (orders, events, customers, subscriptions), and record the
expected refresh window per table — `data-quality-engineer`'s freshness check has nothing
to compare against without it.

**Classify as you discover.** Hand the column list to `governance-officer`: every column
holding personal or otherwise sensitive data gets a row in the Column Registry of
`knowledge/governance-policy.md` (`restricted` unless there is a reason it is not), and a
matching entry in the Data Dictionary. Read column *names and types* for this — do not
select values from a column you are about to classify as restricted. Then start the
first domain reference doc in `knowledge/domains/` for the core fact tables.

### 9. Final sweep

```bash
python scripts/check_placeholders.py
```

Post-setup mode: every remaining `{{UPPER_SNAKE}}` is an error. Anything genuinely
unknowable right now becomes an explicit `> TODO (user): …` note, never a raw
placeholder — a placeholder reads as configuration, a TODO reads as a gap.

### 10. Smoke-test that the team is live

```bash
/health-check
```

It runs the repo lint, the placeholder sweep, the metrics-catalog check, and re-tests
every connection marked ✅, then reports knowledge-base staleness and inventory drift.
Read its output and fix what it finds. If `/health-check` is unavailable for any reason,
run the checks by hand:

```bash
python scripts/lint_repo.py
python scripts/check_placeholders.py
python scripts/check_metrics.py
python scripts/check_governance.py
python scripts/test_connection.py
```

In demo mode, also run `python scripts/run_evals.py --check-references`, and offer
`/eval` as the honest test of the setup: it measures whether the team gets the demo's
questions right, including the three findings planted in the data.

Additionally confirm by inspection:

- **Every agent loads:** the `.claude/` folder is at the workspace root. Tell the user to
  run `/agents` and confirm the full roster appears — the count is whatever
  `scripts/lint_repo.py` reports, so quote that number rather than a remembered one.
- **Inventories exist:** `analyses/`, `pipelines/`, `dashboards/`, `experiments/`,
  `models/`, `scorecards/`, and `deliverables/` each have a `README.md` (scaffold any
  that are missing).
- **Knowledge seeded:** `business-context.md`, `data-sources.md`, and `stakeholders.md`
  have no blank required fields, and `metrics-catalog.md` has at least the draft KPI set.

Report any failing check as a TODO. Never claim a clean setup you did not verify.

### 11. Report back

Cover: what was configured, which data sources are live versus blocked and why, the
smoke-test results verbatim, the draft KPI list, the defaults you applied, the snapshot
id for undo, and a suggested first task — usually `/define-kpis` to ratify the metrics,
then `/scorecard weekly` for a first baseline.

Offer to set up the recurring cadence with `scheduling/SCHEDULING.md`. A weekly scorecard
that depends on somebody remembering to ask for it lasts about three weeks.

## Re-running

Safe to re-run after major business changes, and after `/upgrade` pulls in a new release.
Take the snapshot (step 0), then **diff against the existing knowledge files rather than
overwriting them.** Accumulated knowledge — data quirks, decision rulings, table
inventories, stakeholder preferences, the data-quality log — is the most valuable thing
in the repo and the easiest thing to destroy in a re-run. Merge the new charter facts in;
where a new fact contradicts an old one, ask rather than assuming the charter is more
current.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
