---
name: genie-rooms
description: Query internal Databricks Genie Rooms and author or update Databricks Genie spaces programmatically with REST, CLI, and helper resources.
---

# Genie Rooms Skill

Use this skill for two related workflows:

1. Query an existing Genie room, especially the known internal GTM rooms.
2. Author, export, update, and validate Genie spaces programmatically.

Keep the existing query flow on `resources/genie_rooms.py`. For authoring, use the helper resources and references in this skill rather than extending the conversation CLI.

## Workflow 1: Query Existing Rooms

### Quick Start (Interactive)

Run the script without arguments to see available Genie Rooms:

```bash
python3 resources/genie_rooms.py
```

This displays a menu of known Genie Rooms. Select one or enter a custom room ID.

### Known Genie Rooms

The following internal Genie Rooms are pre-configured:

| # | Name | go/ Link | Description |
|---|------|----------|-------------|
| 1 | Global Genie | go/global_genie | GTM data - accounts, consumption, forecasting |
| 2 | Emerging Genie | go/emerging_genie | Emerging segment data |
| 3 | CME Genie | go/cme_genie | Commercial/Mid-Enterprise data |
| 4 | Retail Genie | go/retail_genie | Retail industry vertical |
| 5 | Global Retail Genie | go/global_retail_genie | Global retail data |
| 6 | HLS Genie | go/hls_genie | Healthcare & Life Sciences |
| 7 | Global HLS Genie | go/global_hls_genie | Global HLS data |
| 8 | FINS Genie | go/fins_genie | Financial Services |
| 9 | Regional FINS Genie | go/reg_fins_genie | Regional Financial Services |
| 10 | MFG Genie | go/mfg_genie | Manufacturing |
| 11 | LATAM Genie | go/latam_genie | Latin America region |
| 12 | CAN Genie | go/can_genie | Canada region |

**To request access:** [go/gtm_genie_access](http://go/gtm_genie_access)

### Prerequisites

1. **Databricks Authentication** - Run `/databricks-authentication` to configure credentials
2. **Genie Room Access** - Request access via [go/gtm_genie_access](http://go/gtm_genie_access)
3. **VPN** - Must be on Databricks VPN to access internal Genie Rooms

### Usage

#### Interactive Mode (Recommended)

```bash
python3 resources/genie_rooms.py
```

You'll see:
```
Available Genie Rooms:
  1. Global Genie (go/global_genie) - GTM data
  2. Emerging Genie (go/emerging_genie) - Emerging segment
  3. CME Genie (go/cme_genie) - Commercial/Mid-Enterprise
  ...
  c. Enter custom room ID

Select a room (1-12 or 'c' for custom):
```

After selecting a room, enter your question when prompted.

#### Direct Mode (with room ID)

```bash
python3 resources/genie_rooms.py --room-id <room-id> ask "Your question"
```

#### Using go/ Links

You can also use the go/ link name directly:

```bash
python3 resources/genie_rooms.py --room global_genie ask "What is ARR for Acme Corp?"
python3 resources/genie_rooms.py --room hls_genie ask "Top HLS accounts by consumption"
```

#### Follow-Up Questions

Genie maintains conversation context:

```bash
python3 resources/genie_rooms.py --room-id <room-id> follow-up <conversation-id> "Break that down by region"
```

#### Room Info

Look up room details and owner:

```bash
python3 resources/genie_rooms.py --room-id <room-id> info
```

#### Send Feedback to Room Owner

If you notice data quality issues, missing columns, or incorrect data in a Genie room, you can send feedback directly to the room owner:

```bash
python3 resources/genie_rooms.py --room-id <room-id> feedback "Your feedback message"
```

This will:
1. Look up the room metadata and owner
2. Ask how you'd like to send feedback (Slack DM or Email)
3. Prepare a formatted message for Claude to send

### Options

| Option | Description |
|--------|-------------|
| `--room` | Room name (e.g., `global_genie`, `hls_genie`) |
| `--room-id` | Full room ID (32-character hex string) |
| `--profile` | Databricks CLI profile (default: DEFAULT) |
| `--no-wait` | Submit question without waiting for results |

### Commands

| Command | Description |
|---------|-------------|
| `ask` | Ask a new question |
| `follow-up` | Ask a follow-up question in an existing conversation |
| `status` | Check the status of a message |
| `list` | List known Genie Rooms |
| `info` | Show room information and owner |
| `feedback` | Send feedback to the room owner |

### Example Workflows

#### Account Research with Global Genie

```bash
# Interactive
python3 resources/genie_rooms.py
# Select 1 (Global Genie)
# Enter: "What is the ARR and consumption trend for Acme Corp?"

# Direct
python3 resources/genie_rooms.py --room global_genie ask "What is the ARR and consumption trend for Acme Corp?"
```

#### Industry-Specific Queries

```bash
# Healthcare
python3 resources/genie_rooms.py --room hls_genie ask "Top 10 HLS accounts by GenAI consumption"

# Financial Services
python3 resources/genie_rooms.py --room fins_genie ask "Which FINS accounts have serverless adoption above 50%?"

# Retail
python3 resources/genie_rooms.py --room retail_genie ask "Retail accounts with highest MoM growth"
```

#### Custom Room ID

If you have a Genie Room not in the list:

```bash
# Get room ID from URL: https://adb-xxx.xx.azuredatabricks.net/genie/rooms/01ef...
python3 resources/genie_rooms.py --room-id 01ef336cd40b11f2b4931415636694eb ask "Your question"
```

#### Reporting Data Quality Issues

If you notice incorrect data in a Genie room:

```bash
# First, check room info and owner
python3 resources/genie_rooms.py --room-id 01eef9cd9a711b5d85bc76d49a281055 info

# Send feedback to the owner
python3 resources/genie_rooms.py --room-id 01eef9cd9a711b5d85bc76d49a281055 feedback "The emerging_data table includes Enterprise accounts like Anysphere and Block, not just Emerging segment accounts."
```

The feedback command will look up the room owner and let you send a Slack DM or email with your feedback.

### Query Best Practices

#### Copy Account Names from SFDC
Always copy/paste the exact SFDC account name to avoid pulling incorrect data.

#### Be Specific with Time Periods
- "in Q3 2024"
- "last 6 months"
- "between January and March 2024"

#### Pre-populate for Demos
Queries can take 30+ seconds. For demos, pre-populate a chat to verify accuracy first.

#### UC Data Lag
Unity Catalog adoption data has a 72-hour SLA. Exclude the last 2 days when querying UC metrics.

### Query Limitations

- **Query Timeout**: Complex queries may timeout after 120 seconds
- **Result Limit**: Responses limited to 5,000 rows
- **Rate Limits**: 5 queries per minute per workspace
- **VPN Required**: Must be on Databricks VPN for internal rooms
- **Data Not Included**: Users/logins, Contracts, AE Targets, UCOs, Pipeline Gen, Meetings, DAIS attendance

### Query Troubleshooting

#### "Error calling Databricks API"
Ensure you're authenticated and on VPN:
```bash
/databricks-authentication
```

#### "Permission denied"
Request access via [go/gtm_genie_access](http://go/gtm_genie_access)

#### Azure Spend Questions
For Azure accounts, do NOT ask spend questions - it pulls $DBUs which differ from customer-visible amounts.

## Workflow 2: Author or Update Genie Spaces

Use this workflow when the user wants to create a new Genie space, inspect `serialized_space`, patch an existing space, or produce helper code and payloads for a curated customer-facing space.

This workflow is not limited to the internal GTM rooms above.

### Default Workflow

#### 1. Inspect Unity Catalog inputs first

- Prefer business-facing Gold tables, documented views, or metric views over raw Bronze or Silver objects.
- Check comments, keys, joinability, time columns, and stable naming before adding objects to a space.
- Keep the first version small and high-signal.
- Write 3-5 benchmark questions before tuning instructions.

Use `/databricks-query` or direct SQL for inspection. When live Databricks validation is needed, prefer the Databricks MCP tools:

- `get_table_details()` for schema and comments
- `execute_sql()` for spot checks
- `get_best_warehouse()` when a warehouse is needed quickly

See [uc-readiness.md](references/uc-readiness.md) for the inspection checklist.

#### 2. Build or edit `serialized_space`

Use `resources/genie_space_builder.py` for the common authoring operations:

- `from_json(...)`
- `set_title(...)`
- `set_description(...)`
- `set_instructions(...)`
- `set_warehouse(...)`
- `add_table(...)`
- `add_view(...)`
- `add_metric_view(...)`
- `add_join_spec(...)`
- `add_example_sql(...)`
- `add_benchmark(...)`
- `add_function(...)`
- `validate()`
- `to_dict()` / `to_json()`

The helper intentionally models the stable, high-value parts of `serialized_space`. For richer spaces, round-trip a fetched export so unknown fields are preserved.

`set_warehouse(...)` manages the outer API metadata used for create and patch requests. It does not write `warehouse_id` into the inner `serialized_space`.

Example:

```python
from genie_space_builder import GenieSpaceBuilder

space = GenieSpaceBuilder(
    title="Revenue Operations Genie Space",
    description="Business-facing revenue and bookings analytics.",
    warehouse_id="WAREHOUSE_ID",
)

space.set_instructions(
    "Prefer the metric view for KPI rollups, call out grain, and state filters in the answer."
)
space.add_metric_view("main.revenue.gold.revenue_bookings_mv")
space.add_view("main.revenue.gold.sales_rep_quota_v")
space.add_table("main.revenue.gold.revenue_daily")
space.add_example_sql(
    title="Revenue by segment last quarter",
    sql=(
        "SELECT segment, SUM(revenue_usd) AS revenue_usd "
        "FROM main.revenue.gold.revenue_daily "
        "WHERE fiscal_quarter = '2026-Q1' "
        "GROUP BY segment "
        "ORDER BY revenue_usd DESC"
    ),
)
space.validate()

print(space.to_json())
```

Use `resources/example_genie_space.py` for a full end-to-end example.

Reference files:

- [api-workflows.md](references/api-workflows.md)
- [best-practices.md](references/best-practices.md)
- [example-rest-export.md](references/example-rest-export.md)
- [example-serialized-space.json](references/example-serialized-space.json)
- [space-iteration.md](references/space-iteration.md)

#### 3. Validate before publishing

- Keep `version = 2`
- Keep `data_sources.tables` sorted by `identifier`
- Preserve opaque IDs when round-tripping existing instructions, snippets, and benchmarks
- Confirm the warehouse and object identifiers match the target workspace
- Validate benchmark prompts against real user questions
- Prefer fixing metadata, joins, metric views, or example SQL before adding broad instructions

#### 4. Push or update the space, then round-trip verify

Create:

```bash
databricks api post /api/2.0/genie/spaces --profile <profile> --json @/tmp/create_genie_space.json
```

Fetch:

```bash
databricks api get \
  "/api/2.0/genie/spaces/<space-id>?include_serialized_space=true" \
  --profile <profile>
```

Patch:

```bash
databricks api patch /api/2.0/genie/spaces/<space-id> --profile <profile> --json @/tmp/update_genie_space.json
```

If the target space already exists and was not created in the current session, confirm with the user before patching it. Do not overwrite, replace, or delete pre-existing Genie spaces without explicit permission.

After create or update:

1. Fetch the space again.
2. Re-parse `serialized_space`.
3. Confirm the expected objects and instructions are present.
4. Run benchmark prompts and a few ad hoc validation questions.
5. Share with subject matter experts and refine based on concrete bad answers.

Optional Databricks MCP shortcuts:

- `create_or_update_genie()` when low-level payload control is not required
- `get_genie()` to inspect metadata after create
- `ask_genie()` and `ask_genie_followup()` for validation questions

## Related Skills

- **`/databricks-authentication`** - Configure Databricks credentials
- **`/logfood-querier`** - Query GTM data using direct SQL
- **`/databricks-query`** - Execute raw SQL queries
- **`/databricks-warehouse-selector`** - Pick a SQL warehouse for authoring or validation

## References

- [Genie Demo FAQ](http://go/genie_demo_faq)
- [Request Access](http://go/gtm_genie_access)
- [Genie Usage Dashboard](https://adb-2548836972759138.18.azuredatabricks.net/dashboardsv3/01ef1dcffe2b16a78107053e15cb2b2e/published)
- [Databricks Genie Conversation API](https://docs.databricks.com/en/genie/conversation-api.html)
