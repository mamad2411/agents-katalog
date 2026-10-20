---
name: aeolus
description: "Query Aeolus BI — three independent capability groups: (1) dashboard chart queries, (2) dataset/SQL queries, (3) Query Editor ad-hoc SQL. Use whenever the user mentions Aeolus, BI dashboards, datasets, dimensions, metrics, dashboard URLs, chart queries, ad-hoc SQL, Query Editor,hive query ,clickhouse query, or needs to inspect Aeolus data across cn/sg/va regions. The skill does NOT auto-guess which capability the user wants — clarify intent first, then read exactly one reference document."
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Aeolus Skill

This skill exposes three **independent** capability groups. You MUST pick the
right group before calling any action — nothing is auto-inferred from URL shape
or field presence.

## Trigger

Use this skill whenever the user mentions Aeolus, BI dashboards, datasets,
dimensions/metrics, dashboard URLs, chart queries, ad-hoc SQL, or Query Editor.
If the user only provided a link or a vague request, go to
**[Disambiguation](#disambiguation)** first — do not call an action yet.

## Capability groups

| # | Group | Detail doc (read ONLY this one) | Auth |
|---|-------|---------------------------------|------|
| 1 | **Dashboard chart queries** — list charts/filters of a dashboard, fetch data for one chart | [references/dashboard.md](./references/dashboard.md) | Titan Passport |
| 2 | **Dataset / SQL queries** — find datasets, inspect fields, run SQL against a dataset | [references/dataset.md](./references/dataset.md) | OAuth credentials |
| 3 | **Query Editor ad-hoc SQL** — run SQL directly without picking a dataset | [references/query_editor.md](./references/query_editor.md) | Titan Passport |

## Routing rule (MUST follow, in order)

1. **Identify the group** using the table below.
2. **Read exactly one** reference document — the one matching that group.
   Do NOT read all three; this skill is designed as progressive disclosure.
3. Build the call using only the actions/params documented there.

| User asks for… | Group | First action |
|----------------|:----:|---------------|
| "What charts are on this dashboard?" / dashboard URL + "列出图表/筛选器" | 1 | `get_dashboard` |
| "Give me the data for chart X" / "查这个图表的数据" | 1 | `query_report` |
| "列出筛选器的候选值" / "这个 filter 能选什么" | 1 | `get_filter_candidates` |
| "Find the dataset for project X" / "这个项目底下有哪些 dataset" | 2 | `list_apps` → `search_datasets` |
| "这个 dataset 有哪些字段" / "dimensions/metrics" | 2 | `dataset_fields` |
| "这个 dataset 是哪些 Hive 表 join 来的" / "虚拟表的物理组成" / "底层表 / 分区 / join 关系" | 2 | `get_fabric_data_info` |
| "run this SQL against dataset N" / "在 dataset 上跑 SQL" | 2 | `query` |
| "跑一段 SQL" / "ad-hoc SQL" / "Query Editor" with no dataset context | 3 | `qe_query` |
| "多表 join / 临时分析 / 探索性 SQL" | 3 | `qe_query` |
| "看一下 QE task 的状态/日志" | 3 | `qe_status` / `qe_logs` |

### `query` vs `qe_query` — do NOT confuse them

They both "run SQL", but their semantics are completely different. If you pick the
wrong one you will either get an auth/permission error or a meaningless result.

| Dimension | `query` (group 2) | `qe_query` (group 3) |
|-----------|-------------------|----------------------|
| Scope | Single, **known** `dataset_id` | Arbitrary — no dataset required |
| Required inputs | `region`, `dataset_id`, `sql` | `sql` only |
| Auth | OAuth credentials per region | Titan Passport (`gdpa-cli login`) |
| Good for | Reading one dataset's fields, partition-filtered queries | Multi-table joins, exploratory/ad-hoc SQL, cross-source investigation |
| **Not** for | Multi-table joins, exploratory SQL, "I just have a SQL" | Targeting one specific Aeolus dataset when you already have the `dataset_id` |

Decision tree:

1. User gave you a `dataset_id` **and** the SQL is clearly against that single
   dataset → `query` (group 2).
2. User gave you a SQL string and **no** `dataset_id`, or the SQL joins tables,
   or the user is "just exploring" → `qe_query` (group 3). This is the default
   for generic SQL.
3. If neither is clear, ask via `AskUserQuestion` — see
   [Disambiguation](#disambiguation) below.

## Disambiguation

If the user only provided an ambiguous input (URL / a name / just a SQL), DO
NOT call this skill yet. Use `AskUserQuestion` to pick the group first.

| Input you received | Ask the user |
|--------------------|--------------|
| Only a dashboard URL | 列图表？查某个图表数据？还是只想找底层 dataset？ |
| Only a dataset URL/ID | 看字段？搜索 dataset？还是直接跑 SQL？ |
| Only a SQL string (no `dataset_id`) | 默认走 Query Editor (`qe_query`) ad-hoc 执行即可；仅当用户明确指定了某个 dataset_id 时才确认是否改走 `query`。 |
| SQL + `dataset_id` but it looks like multi-table / exploratory | 这是针对该 dataset 的查询 (`query`)，还是临时多表分析（改用 `qe_query`）？ |
| Just "Aeolus 看板" with no details | 给一个看板 URL，以及想做什么？ |

Skip the clarification only when the user clearly stated the verb (查图表 / 查数据 / 跑 SQL / 列表 / …).

If you call without a concrete `action`, the skill will reject the request
with a structured error listing all three groups and echo back any detected
hints — treat that as a signal to ask the user, not to retry with a guess.

## Invocation shape

```bash
gdpa-cli run aeolus --session-id "$SESSION_ID" --input '{"action": "<action_name>", ...other params}'
```

Common params across groups: `action` (required), `region` (`cn` default for
groups 1/3, required for group 2). Group-specific params live in the
corresponding reference document — read that one and only that one.

Authentication: run `gdpa-cli login` once. Group 2 additionally needs OAuth
credentials configured (see [references/dataset.md](./references/dataset.md)).

## Cross-cutting reminders

- **Partial dashboard failures are normal.** When summarizing a dashboard,
  query each chart and surface its `code`/`msg` per chart — don't collapse a
  mixed result into "everything failed". A `aeolus/clickhouse/...` error on
  one chart usually means a server-side dataset schema drift (the browser UI
  also fails on it); see the dashboard reference's "Errors you may see"
  section for what's actionable vs what needs the dashboard owner.
- **Use `dry_run: true` first** for any non-trivial `query_report` override
  (`filters` / `params` / `dynamic_fields`). It returns the exact request body
  without sending the query, surfaces typos as `unmatched_filters`, and lets
  the model self-correct cheaply before paying for a real query.
- **Do not retry server-side schema errors blindly.** `Missing columns: …`,
  `aeolus/clickhouse/sqlParseFailed`, and friends are not fixed by re-tweaking
  filters — escalate to the dashboard / dataset owner.
