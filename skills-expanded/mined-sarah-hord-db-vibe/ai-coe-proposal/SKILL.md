---
name: ai-coe-proposal
description: AI-powered GTM Copilot that detects opportunities, runs proven GTM plays, designs architectures, and generates world-class customer proposals. Orchestrates a Strategic Expert Council and Solution Architecture Council to produce executive-ready AI COE transformation proposals with Golden Path docs, SOWs, project plans, and executive slide decks. Backed by a persistent Strategic Memory Graph (Lakebase), Vector Search retrieval, and a 5-play GTM Play Library. Every output aligns to Customer Outcomes → Databricks Data Intelligence Platform → People | Process | AI Tools.
user-invocable: true
---

# Databricks AI CoE GTM Copilot

An AI-powered GTM copilot that enables field teams to detect opportunities, run proven GTM plays, design architectures, generate proposals, plan delivery, and accelerate enterprise AI adoption.

**Every output answers:** Why this matters · Why now · Why Databricks · How we deliver

---

## System Architecture

```
Enterprise Signal Layer (Drive, Slack, Gmail, Calendar, SFDC, logfood, Databook)
        ↓
Strategic Memory Graph (Lakebase) → Graph Intelligence Brief
        ↓
Context Routing Engine → 6-category Context Brief
        ↓
GTM Play Detection Engine → Activated plays ranked by signal strength
        ↓
Vector Search Retrieval → Similar proposals, architectures, accelerators
        ↓
Strategic Expert Council (5 personas) → Strategic Transformation Brief
        ↓
Solution Architecture Council (5 personas) → Technical Blueprint + Delivery Plan
        ↓
Proposal Generator → Golden Path + SOW + Project Plan + Executive Deck
        ↓
Memory Write-Back → Update graph with new proposal, signals, architectures
```

**Framework:** Customer Outcomes → Databricks Data Intelligence Platform → People | Process | AI Tools

---

## Path Resolution (Run Once at Start)

**IMPORTANT:** The plugin cache may contain multiple versions. Resolve paths once:

```bash
# Resolve to the latest installed version of each plugin
GOOGLE_TOOLS=$(ls -d ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/ 2>/dev/null | sort -V | tail -1)
WORKFLOWS=$(ls -d ~/.claude/plugins/cache/fe-vibe/fe-workflows/*/ 2>/dev/null | sort -V | tail -1)
CMEG_GTM=$(ls -d ~/.claude/plugins/cache/fe-vibe/fe-cmeg-gtm/*/ 2>/dev/null | sort -V | tail -1)
[ -z "$CMEG_GTM" ] && CMEG_GTM="$HOME/.claude/plugins/cache/fe-vibe/fe-cmeg-gtm/"

# Core resource paths
GOOGLE_AUTH="${GOOGLE_TOOLS}skills/google-auth/resources/google_auth.py"
MARKDOWN_TO_GDOCS="${GOOGLE_TOOLS}skills/google-docs/resources/markdown_to_gdocs.py"

# GTM Copilot resources
RESOURCE_DIR="${CMEG_GTM}skills/ai-coe-proposal/resources"
DELIVERY_PLAN_SQL="${RESOURCE_DIR}/coe_delivery_plan_query.sql"
SLIDES_BUILDER="${RESOURCE_DIR}/coe_slides_builder.py"
INSTRUCTIONS_PRIMARY="${RESOURCE_DIR}/instructions_primary.txt"
INSTRUCTIONS_SECONDARY="${RESOURCE_DIR}/instructions_secondary.txt"
INSTRUCTIONS_TERTIARY="${RESOURCE_DIR}/instructions_tertiary.txt"
MEMORY_GRAPH_PY="${RESOURCE_DIR}/memory_graph.py"
MEMORY_GRAPH_SQL="${RESOURCE_DIR}/memory_graph_schema.sql"
GTM_PLAYS_YAML="${RESOURCE_DIR}/gtm_plays.yaml"
PLAY_DETECTOR_PY="${RESOURCE_DIR}/play_detector.py"
CONTEXT_ROUTER_PY="${RESOURCE_DIR}/context_router.py"
VECTOR_RETRIEVAL_PY="${RESOURCE_DIR}/vector_retrieval.py"
RESOURCE_PLANNER_PY="${RESOURCE_DIR}/resource_planner.py"
ACCELERATOR_SQL="${RESOURCE_DIR}/accelerator_lookup.sql"
EXPERT_COUNCILS_TXT="${RESOURCE_DIR}/expert_councils.txt"
DECK_ORCHESTRATOR="${RESOURCE_DIR}/deck_orchestrator.py"
DECK_BUILDER="${RESOURCE_DIR}/deck_builder.py"
SLIDE_GRAPH="${RESOURCE_DIR}/slide_knowledge_graph.yaml"
ARCH_DIAGRAMS_PY="${RESOURCE_DIR}/build_arch_diagrams.py"
USECASE_ARCH_PY="${RESOURCE_DIR}/build_usecase_arch.py"
GANTT_SLIDE_PY="${RESOURCE_DIR}/build_gantt_slide.py"
VALUE_SLIDE_PY="${RESOURCE_DIR}/build_value_slide.py"
WHY_DB_SLIDE_PY="${RESOURCE_DIR}/build_why_databricks_slide.py"
MSP_SLIDE_PY="${RESOURCE_DIR}/build_msp_slide.py"
AGENDA_SLIDE_PY="${RESOURCE_DIR}/build_agenda_slide.py"
SUCCESS_METRICS_PY="${RESOURCE_DIR}/build_success_metrics_slide.py"
CHALLENGE_SOLUTION_PY="${RESOURCE_DIR}/build_challenge_solution_slide.py"
PHASE1_CARDS_PY="${RESOURCE_DIR}/build_phase1_cards_slide.py"
HERO_NUMBERS_PY="${RESOURCE_DIR}/build_hero_numbers_slide.py"

# Chained skill resource paths (optional)
BATTLECARD_REGISTRY="${WORKFLOWS}skills/competitive-analysis/resources/competitive/battlecard-registry.yaml"
RENEWAL_RISK_PY="${WORKFLOWS}skills/renewal-risk-analyzer/resources/renewal_risk_analyzer.py"
QUICKSIZER_PY="${WORKFLOWS}skills/databricks-sizing/resources/quicksizer_api.py"

# Infrastructure config (Lakebase + Vector Search)
LOGFOOD_HOST="adb-2548836972759138.18.azuredatabricks.net"
LOGFOOD_WAREHOUSE="74b037a3a9ec9847"
MEMORY_CATALOG="home_zach_relli"
MEMORY_SCHEMA="gtm_copilot"
VS_ENDPOINT="gtm-copilot-vs"
VS_INDEX_PREFIX="${MEMORY_CATALOG}.${MEMORY_SCHEMA}"
```

---

## Step 0: Resolve User Identity

Pull user identity from `~/.vibe/profile.yaml` (`name`, `title`, `team`). If not available, ask for name, title, and team.

Store as:
- `USER_NAME` — full name
- `USER_TITLE` — role title
- `USER_TEAM` — team/region

---

## Step 1: Collect Input (MANDATORY — DO NOT SKIP)

**BLOCKING:** Ask these questions and wait for answers. The EM's input drives positioning and use case prioritization.

```
I'll generate your full AI COE proposal package. Need 5 inputs:

1. Account name?
2. Primary use cases (2-4 — rough is fine, e.g. "RAG chatbot, recommendation engine, MLflow migration"):
3. Customer team structure (optional — e.g. "Data Foundations team, ML Platform team, Central Analytics"):
4. Situation: new proposal / renewal / QBR follow-up / expansion?
5. Any extra context? (paste Slack threads, meeting notes, email snippets — anything helps)
```

Store as:
- `ACCOUNT` — account name
- `USE_CASES` — list of 2-4 use cases
- `CUSTOMER_TEAMS` — their internal team names (default: "data/analytics/ML teams")
- `SITUATION` — new / renewal / qbr / expansion
- `CONTEXT` — freeform context

---

## Step 2: Strategic Memory Graph Query

**Run immediately after collecting input. Non-blocking — proceed to Step 3 in parallel.**

Query the persistent Strategic Memory Graph (Lakebase) for prior intelligence on this account. The graph stores structured relationships between accounts, initiatives, architectures, stakeholders, competitors, use cases, and prior proposals.

```bash
# Get graph intelligence brief
if [ -f "$MEMORY_GRAPH_PY" ]; then
  LOGFOOD_TOKEN=$(databricks auth token --profile logfood 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

  GRAPH_BRIEF=$(python3 "$MEMORY_GRAPH_PY" brief \
    --host "$LOGFOOD_HOST" \
    --token "$LOGFOOD_TOKEN" \
    --warehouse "$LOGFOOD_WAREHOUSE" \
    --catalog "$MEMORY_CATALOG" \
    --schema "$MEMORY_SCHEMA" \
    --account "ACCOUNT_NAME" 2>/dev/null)
fi
```

### What the Graph Intelligence Brief Contains (~500 tokens)

```
=== GRAPH INTELLIGENCE BRIEF: [ACCOUNT] ===
Account: [name] | Tier: [X] | Annual: $[X] | Region: [X]
Contract: $[X] | Remaining: $[X] | Expiry: [date]

ACTIVE INITIATIVES:
- [Initiative 1]: [status] — [description]
- [Initiative 2]: [status] — [description]

CURRENT ARCHITECTURE:
- Stack: [Snowflake, Spark on EMR, Databricks SQL, ...]
- Migration targets: [from → to]
- Architecture gaps: [identified gaps]

KEY STAKEHOLDERS:
- Champion: [name, title] — [influence level]
- Sponsor: [name, title]
- Blocker: [name, title] — [reason]

COMPETITIVE LANDSCAPE:
- Primary: [Snowflake] — [displacement status]
- Secondary: [Fabric] — [evaluation status]

USE CASES (U1-U5): [N] active
- [UC1]: [stage], $[X]/mo, [products], [health]
- [UC2]: [stage], $[X]/mo, [products], [health]

PRIOR PROPOSALS: [N] generated
- [Date]: [Play type] — [outcome]
- [Date]: [Play type] — [outcome]

RELATIONSHIPS:
- [Account] → has_initiative → [AI Transformation]
- [Account] → competes_with → [Snowflake]
- [Initiative] → enabled_by → [Mosaic AI]
```

If the graph is not set up or has no data for this account, proceed without — the research phase (Step 3) provides sufficient context. The graph brief enriches but is not required.

---

## Step 3: Enterprise Signal Ingestion (Run ALL in Parallel)

Launch all research streams simultaneously. Do NOT block on any single source.

### 3a: Google Drive Search

```bash
TOKEN=$(python3 "$GOOGLE_AUTH" token 2>/dev/null)

# 3 parallel searches
# 1. General account docs
curl -s "https://www.googleapis.com/drive/v3/files?q=fullText+contains+'ACCOUNT_NAME'&fields=files(id,name,mimeType,modifiedTime,webViewLink)&pageSize=15&orderBy=modifiedTime+desc" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng"

# 2. Title matches
curl -s "https://www.googleapis.com/drive/v3/files?q=name+contains+'ACCOUNT_NAME'&fields=files(id,name,mimeType,modifiedTime,webViewLink)&pageSize=15&orderBy=modifiedTime+desc" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng"

# 3. COE-specific
curl -s "https://www.googleapis.com/drive/v3/files?q=fullText+contains+'ACCOUNT_NAME'+and+fullText+contains+'COE'&fields=files(id,name,mimeType,modifiedTime,webViewLink)&pageSize=10&orderBy=modifiedTime+desc" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Read 2-3 most relevant recent docs. Extract: customer challenges, stated priorities, team names, use cases, blockers, stakeholders, OKRs.

### 3b: Slack Search (MCP)

```python
# General account discussions (last 90 days)
mcp__slack__slack_read_api_call("search.messages", {
  "query": "ACCOUNT_NAME after:YYYY-MM-DD",
  "count": 20, "sort": "timestamp", "sort_dir": "desc"
})

# COE or proposal-specific
mcp__slack__slack_read_api_call("search.messages", {
  "query": "ACCOUNT_NAME COE OR proposal OR golden path",
  "count": 10, "sort": "timestamp", "sort_dir": "desc"
})

# Competitive intelligence
mcp__slack__slack_read_api_call("search.messages", {
  "query": "ACCOUNT_NAME Snowflake OR Fabric OR Redshift OR competitor",
  "count": 10, "sort": "timestamp", "sort_dir": "desc"
})

# Per use case
mcp__slack__slack_read_api_call("search.messages", {
  "query": "ACCOUNT_NAME USE_CASE_KEYWORD",
  "count": 10, "sort": "timestamp", "sort_dir": "desc"
})
```

Extract: customer satisfaction issues, deal history, strategic direction, technical landscape, champion asks, team alignment.

**Addressing customer sat issues:** If Slack reveals inherited service gaps, delayed proposals, or customer frustration, address HEAD-ON in the proposal. Frame AI COE as the structured fix. Reference Eric Winter: "I don't want it to be a bandaid, I want it to be tied to business value."

### 3c: Gmail Search

```bash
TOKEN=$(python3 "$GOOGLE_AUTH" token 2>/dev/null)
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=ACCOUNT_NAME+newer_than:90d&maxResults=10" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Read top 2-3 relevant threads. Extract: action items, customer requests, meeting follow-ups, proposal feedback.

### 3d: Google Calendar

```bash
TOKEN=$(python3 "$GOOGLE_AUTH" token 2>/dev/null)
START=$(date -v-30d +%Y-%m-%dT00:00:00Z 2>/dev/null || date -d '30 days ago' +%Y-%m-%dT00:00:00Z)
END=$(date -v+14d +%Y-%m-%dT23:59:59Z 2>/dev/null || date -d '14 days' +%Y-%m-%dT23:59:59Z)

curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=$START&timeMax=$END&q=ACCOUNT_NAME&maxResults=20&singleEvents=true&orderBy=startTime" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Extract: recent meeting context, upcoming meeting dates, attendee names.

### 3e: Salesforce — UCOs, ASQs, Account

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['username'])")

# UCOs
sf data query --query "
  SELECT Id, Name, Stages__c, MonthlyTotalDollarDBUs__c, Demand_Plan_Next_Steps__c,
         Implementation_Status__c, Implementation_Start_Date__c, Full_Production_Date__c,
         Primary_Solution_Architect__r.Name, DSA__r.Name, UCO_Type__c,
         Products_Utilized__c, Description__c, Business_Value__c,
         Customer_Exec_Sponsor__c, Customer_Tech_Lead__c,
         Metrics__c, MetricsNotes__c, Compelling_event_Urgency__c,
         CreatedDate, LastModifiedDate
  FROM UseCase__c
  WHERE Account__r.Name = 'ACCOUNT_NAME'
    AND Active__c = true
  ORDER BY Stages__c DESC, MonthlyTotalDollarDBUs__c DESC NULLS LAST
" --target-org "$SF_TARGET_ORG" --json

# ASQs
sf data query --query "
  SELECT Id, Name, Status__c, Specialist__r.Name, Type__c,
         Approved_Budget__c, Description__c, CreatedDate
  FROM ApprovalRequest__c
  WHERE Account__r.Name = 'ACCOUNT_NAME'
    AND Status__c NOT IN ('Closed - Cancelled', 'Closed - Rejected')
  ORDER BY CreatedDate DESC
" --target-org "$SF_TARGET_ORG" --json

# Account details
sf data query --query "
  SELECT Id, Name, AnnualRevenue, Industry, NumberOfEmployees,
         BillingCity, BillingState, AccountSource, Description,
         Owner.Name, Account_Tier__c
  FROM Account
  WHERE Name = 'ACCOUNT_NAME'
" --target-org "$SF_TARGET_ORG" --json

# Open blockers
sf data query --query "
  SELECT Id, Name, Type__c, Category__c, Blocker_Status__c,
         Description__c, DBU_Blocked__c, Use_Case__r.Name
  FROM Blocker__c
  WHERE Account__r.Name = 'ACCOUNT_NAME'
    AND Blocker_Status__c IN ('Open', 'In Progress')
  ORDER BY DBU_Blocked__c DESC NULLS LAST
" --target-org "$SF_TARGET_ORG" --json
```

Fallback to logfood if `sf` CLI not authenticated:

```bash
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{
  "statement": "SELECT * FROM main.sfdc_bronze.usecase__c WHERE Account_Name__c = '\''ACCOUNT_NAME'\'' AND Active__c = true AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)",
  "warehouse_id": "74b037a3a9ec9847",
  "format": "JSON_ARRAY",
  "wait_timeout": "50s"
}'
```

### 3f: Logfood Consumption & Adoption Data

```bash
# Consumption summary
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{
  "statement": "SELECT Account, SUM(Monthly_UCO_Dollar_DBUs) as total_monthly_dbus, COUNT(*) as uco_count, COUNT(CASE WHEN UCO_Stage IN ('\''U4-Confirming'\'','\''U5-Onboarding'\'') THEN 1 END) as late_stage, MAX(Account_Monthly_UCO_Dollar_DBUs) as account_monthly_dbus, MAX(yearly_contract_amount) as contract, MAX(DSA_AMOUNT) as dsa_investment, MAX(Tier) as tier FROM main.field_usage_dashboard.uco_data WHERE Account = '\''ACCOUNT_NAME'\'' GROUP BY Account",
  "warehouse_id": "74b037a3a9ec9847",
  "format": "JSON_ARRAY",
  "wait_timeout": "50s"
}'

# Product adoption heatmap (SKU breakdown, last 12 months)
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{
  "statement": "SELECT sku_category, ROUND(SUM(dollar_dbus_consumed), 0) as total_dbus, COUNT(DISTINCT workspace_id) as workspaces, COUNT(DISTINCT DATE_TRUNC('\''month'\'', usage_date)) as active_months FROM main.fin_live_gold.paid_usage_metering WHERE account_name = '\''ACCOUNT_NAME'\'' AND usage_date >= DATE_ADD(CURRENT_DATE(), -365) GROUP BY sku_category ORDER BY total_dbus DESC",
  "warehouse_id": "74b037a3a9ec9847",
  "format": "JSON_ARRAY",
  "wait_timeout": "50s"
}'

# Monthly consumption trend
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{
  "statement": "SELECT DATE_TRUNC('\''month'\'', usage_date) as month, ROUND(SUM(dollar_dbus_consumed), 0) as monthly_dbus, COUNT(DISTINCT workspace_id) as active_workspaces FROM main.fin_live_gold.paid_usage_metering WHERE account_name = '\''ACCOUNT_NAME'\'' AND usage_date >= DATE_ADD(CURRENT_DATE(), -365) GROUP BY 1 ORDER BY 1",
  "warehouse_id": "74b037a3a9ec9847",
  "format": "JSON_ARRAY",
  "wait_timeout": "50s"
}'
```

### 3g: Competitive Intelligence (Chained — Optional)

```bash
if [ -f "$BATTLECARD_REGISTRY" ]; then
  cat "$BATTLECARD_REGISTRY"
fi
```

Extract 3-5 key differentiators based on competitors identified in SFDC and Slack.

Fallback to Glean:
```python
mcp__glean__glean_read_api_call("search", {
  "query": "ACCOUNT_NAME competitive Snowflake OR Fabric OR Redshift",
  "pageSize": 5
})
```

### 3h: Renewal Risk Screen (Optional — If Renewal/Expiring)

```bash
if [ -f "$RENEWAL_RISK_PY" ] && [ "$SITUATION" = "renewal" ]; then
  python3 "$RENEWAL_RISK_PY" --account "ACCOUNT_NAME" --profile logfood 2>/dev/null
fi
```

### 3i: Accelerator Catalog Lookup

```bash
# Read the accelerator lookup SQL and execute against logfood
if [ -f "$ACCELERATOR_SQL" ]; then
  SQL=$(cat "$ACCELERATOR_SQL")
  # Replace parameters with use case keywords
  # Execute on logfood warehouse
fi
```

This queries `home_zach_relli.path_to_production.accelerator_catalog` for matching delivery accelerators. Prioritize field-engineered solutions and Databricks-endorsed architectures.

### 3j: Instruction Documents (Read in Parallel with Research)

```bash
cat "$INSTRUCTIONS_PRIMARY"    # 9-section executive story arc
cat "$INSTRUCTIONS_SECONDARY"  # CoE value proposition, 4 focus areas
cat "$INSTRUCTIONS_TERTIARY"   # Pitch best practices, anti-patterns
```

These define the narrative framework. Internalize before writing any content.

---

## Step 4: Context Routing Engine

**After all research returns, organize findings into 6 structured categories.**

Take all raw research from Step 3 + Graph Intelligence Brief from Step 2, and route into the Context Brief:

### Category 1: Customer Strategy
- Stated objectives and OKRs (from Drive docs, EM input)
- Strategic initiatives (from SFDC, Slack, Graph)
- Business priorities (from Calendar, Gmail action items)
- Executive sponsorship status (from SFDC stakeholders, Slack)

### Category 2: Technical Architecture
- Current platform stack (from SFDC Products_Utilized, Graph)
- Products utilized on Databricks (from logfood SKU heatmap)
- Architecture gaps (from adoption heatmap, UCO analysis)
- Migration targets (from SFDC Migration_Source, competitive intel)

### Category 3: Opportunity Context
- Deal stage and type (from EM SITUATION input)
- Contract value and consumption (from logfood)
- UCO pipeline: stages, iMRR, health status (from SFDC/logfood)
- ASQ and blocker status (from SFDC)
- Investment history: DSA, RSA, Training tiers (from logfood)

### Category 4: Industry Trends
- Industry-specific AI pressures (from account industry, Glean, Drive docs)
- Competitive dynamics (from battlecard registry, Slack)
- Regulatory or compliance factors (from research context)
- Market timing signals (from earnings reports, strategic initiatives)

### Category 5: Competitive Threats
- Primary competitors identified (from SFDC Primary_Competitor, Slack)
- Displacement opportunities (from architecture analysis)
- Competitive evaluation status (from Slack, Drive)
- Key differentiators to leverage (from battlecard registry)

### Category 6: Delivery Constraints
- Resource availability (from ASQ status, current DSA assignment)
- Timeline pressures (from Calendar, EM context, renewal dates)
- Technical prerequisites (from UCO blockers, architecture gaps)
- Partner ecosystem status (from SFDC partner field, Slack)
- Prior engagement outcomes (from Graph, Slack)

### Extract Canonical Signals

From the categorized context, extract canonical signals for play detection:

```python
# Signal extraction mapping
signals = {
  "sfdc_signals": [],      # has_ai_ucos, multiple_teams, genai_experimentation, migration_active, etc.
  "architecture_signals": [],  # snowflake_present, separate_ml_platform, legacy_dw, etc.
  "consumption_signals": [],   # high_sql_warehouse, low_model_serving, growing_consumption, etc.
  "competitive_signals": [],   # snowflake_primary, evaluating_fabric, vendor_consolidation, etc.
  "strategic_signals": []      # ai_transformation_stated, cto_champion, board_pressure, etc.
}
```

Map research findings to signal names using these rules:
- SFDC UCOs with `UCO_Type LIKE '%AI%'` → `has_ai_ucos`
- Multiple distinct `Products_Utilized` values → `multiple_teams`
- `Primary_Competitor = 'Snowflake'` → `snowflake_primary`
- Low Model Serving in SKU heatmap → `low_model_serving`
- Drive docs mentioning "AI strategy" or "transformation" → `ai_transformation_stated`
- Customer exec sponsor identified in SFDC → `cto_champion`
- Multiple UCOs across different `UCO_Type` → `fragmented_ml_tooling`

---

## Step 5: GTM Play Detection

**Run the Play Detection Engine to identify which GTM plays to activate.**

```bash
# Read the play library
cat "$GTM_PLAYS_YAML"

# Run detector with extracted signals
if [ -f "$PLAY_DETECTOR_PY" ]; then
  echo '$EXTRACTED_SIGNALS_JSON' > /tmp/coe_ACCOUNT/signals.json
  python3 "$PLAY_DETECTOR_PY" \
    --plays "$GTM_PLAYS_YAML" \
    --signals /tmp/coe_ACCOUNT/signals.json
fi
```

### Play Library (5 Core Plays)

| Play | Key Signals | Primary Platform | Typical Tier |
|---|---|---|---|
| **AI CoE Establishment** | enterprise AI initiative, fragmented ML, multiple AI teams | Mosaic AI, MLflow, Unity Catalog | T3-T6 |
| **Snowflake Displacement** | Snowflake architecture, high warehouse costs, separate ML | Delta Lake, Lakehouse, SQL Warehouse | T3-T7 |
| **Enterprise AI Platform** | GenAI adoption, ML scaling, model deployment delays | Agent Framework, Model Serving, AI Gateway | T2-T5 |
| **Lakehouse Migration** | legacy DW, ETL complexity, data silos | Lakeflow Connect, DLT/SDP, Unity Catalog | T2-T6 |
| **GenAI Factory** | LLM experimentation, RAG use cases, GenAI pilots | Foundation Model API, Vector Search, Apps | T2-T5 |

### Play Activation Rules

- Multiple plays CAN activate simultaneously (e.g., AI CoE + Snowflake Displacement)
- Prioritize by: **deal size potential** > **strategic impact** > **customer urgency** > **technical feasibility**
- Primary play drives the proposal narrative spine
- Secondary plays become workstreams within the proposal
- If no play activates with high confidence, default to **AI CoE Establishment** (the most general)

### Store Activated Plays

```
PRIMARY_PLAY: [play_id] (confidence: high/medium)
SECONDARY_PLAYS: [play_id, play_id] (if activated)
PLAY_NARRATIVE: [from play definition — headline, problem, vision, why_now, why_databricks]
PLAY_PLATFORM: [primary and secondary platform products]
PLAY_ACCELERATORS: [matched accelerators from PathToProduction]
```

---

## Step 6: Vector Search Retrieval (Optional — Non-Blocking)

**Query Vector Search for similar prior proposals, architecture patterns, and accelerators.**

```bash
if [ -f "$VECTOR_RETRIEVAL_PY" ]; then
  LOGFOOD_TOKEN=$(databricks auth token --profile logfood 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

  VS_CONTEXT=$(python3 "$VECTOR_RETRIEVAL_PY" \
    --host "$LOGFOOD_HOST" \
    --token "$LOGFOOD_TOKEN" \
    --index-prefix "$VS_INDEX_PREFIX" \
    --query "ACCOUNT_NAME INDUSTRY USE_CASES SITUATION" 2>/dev/null)
fi
```

### What Vector Search Returns (~2000 tokens)

```
=== SIMILAR PRIOR PROPOSALS ===
[1] Account: FanDuel | Play: AI CoE | Outcome: 23x ROI
    Key patterns: agent framework, Genie Spaces, partner ecosystem
    Doc: [url]
[2] Account: Riot Games | Play: AI CoE | Outcome: 6 Genie Spaces
    Key patterns: ABAC governance, Genie at scale, AI/BI
    Doc: [url]

=== RELEVANT ARCHITECTURE PATTERNS ===
[1] Streaming + ML Pipeline → Lakeflow → Feature Store → Model Serving → AI Gateway
[2] GenAI Stack → Agent Framework → RAG → Vector Search → Foundation Model API

=== MATCHING ACCELERATORS (PathToProduction) ===
[1] AI Gateway Setup — production-ready, 2-day deploy
[2] Genie Space Builder — 1-week to first room
[3] MLflow 3 Migration Kit — 3-day upgrade path
```

If Vector Search is not set up, proceed without. The system works without VS but produces richer proposals with it.

---

## Step 7: Strategic Expert Council

**Simulate a consulting board of 5 strategic experts analyzing the customer context.**

Read the expert council prompts:
```bash
cat "$EXPERT_COUNCILS_TXT"
```

Run each expert sequentially, feeding prior outputs forward. Each produces a focused brief (~150-200 words). The combined output forms the **Strategic Transformation Brief**.

### 7a: Market Analyst

Analyze the customer's industry context:
- Industry disruption vectors affecting `ACCOUNT`
- Technology inflection points relevant to their business model
- Competitive landscape: who is winning, who is losing, and why
- Market timing: why AI/data transformation is urgent NOW for their industry

**Input:** Context Brief (Category 4: Industry Trends)
**Output:** Market Intelligence Brief (3 disruption signals, 2 inflection points, 1 competitive urgency factor, 1 "why now" catalyst) — ~150 words

### 7b: Strategy Partner

Define the transformation vision:
- What does `ACCOUNT` look like in 3 years with a mature AI platform?
- What 3-5 strategic initiatives bridge current state to target state?
- What business capability gaps exist?
- What is the quantified cost of inaction?

**Input:** Context Brief (Categories 1+4) + Market Intelligence Brief
**Output:** Strategic Transformation Brief (vision, 3-5 initiatives, top 3 gaps, cost of inaction) — ~200 words

### 7c: Transformation Economist

Quantify the value creation potential:
- Direct cost savings (infrastructure, licensing, operational)
- Productivity gains (time-to-insight, model deployment velocity)
- Revenue acceleration (new AI products, better decisions)
- Risk reduction (governance, compliance, vendor concentration)

**Input:** Context Brief (Category 3: Opportunity) + Strategic Brief + Account consumption data
**Output:** Value Creation Model (3-year value estimate, ROI multiple, payback period, top 3 value drivers) — ~150 words

### 7d: AI Workforce Futurist

Describe the organizational transformation:
- AI-enabled operating model for `ACCOUNT`'s teams
- Human + AI collaboration patterns specific to their industry
- Productivity acceleration: what 10x improvements are realistic?
- Organizational readiness and change management needs

**Input:** Context Brief (Categories 1+6) + Strategic Brief
**Output:** AI Workforce Brief (target operating model, 2 collaboration patterns, productivity multiplier, change management actions) — ~150 words

### 7e: Industry Operating Executive

Assess execution feasibility:
- Can `ACCOUNT` actually execute this transformation?
- What operating model changes are required?
- Process transformation priorities
- Executive sponsorship requirements
- Common failure modes and how to avoid them

**Input:** All prior briefs + Context Brief (Category 6: Delivery Constraints)
**Output:** Execution Feasibility Assessment (feasibility score 1-5, top 3 risks, organizational changes, sponsorship recommendation, #1 failure mode to avoid) — ~150 words

### Combine into Strategic Transformation Brief

Merge all 5 expert outputs into a single **Strategic Transformation Brief** (~800-1000 words). This brief feeds into the Solution Architecture Council and directly informs the proposal narrative.

---

## Step 8: Solution Architecture Council

**Translate strategy into technical architecture and delivery plan.**

### 8a: Databricks Field CTO

Define the reference architecture:
- Lakehouse architecture layers mapped to customer use cases
- Databricks product recommendations per layer
- Integration patterns with customer's existing systems
- Architecture decision records for key choices

**Input:** Context Brief (Category 2) + Strategic Brief + Activated Play(s)
**Output:** Architecture Blueprint (4-layer architecture, 3 integration points, 2 ADRs, migration path) — ~200 words

### 8b: Enterprise Data Architect

Design the data foundation:
- Data ingestion patterns (Lakeflow Connect, SDP, streaming)
- Data quality and governance (DQX, Unity Catalog, lineage)
- Semantic layer (Metric Views, Feature Store)
- Data mesh/federation strategy if multi-team

**Input:** Architecture Blueprint + Context Brief (Category 2)
**Output:** Data Foundation Design (ingestion strategy, governance model, semantic layer, DQ approach) — ~150 words

### 8c: AI Platform Architect

Design the AI/ML layer:
- MLOps pipeline (MLflow 3, experiment tracking, model registry)
- GenAI stack (Agent Framework, AI Gateway, Foundation Model API)
- Evaluation and monitoring (agent eval, guardrails, observability)
- Serving infrastructure (Model Serving, Databricks Apps)

**Input:** Architecture Blueprint + Use Cases + activated play platform mapping
**Output:** AI Platform Design (MLOps pipeline, GenAI stack, eval framework, serving architecture) — ~200 words

### 8d: GTM Strategy Leader

Design the commercial approach:
- Pricing strategy using 7-tier model
- Co-investment and partner funding
- Expansion path (entry tier → target tier)
- Competitive displacement strategy
- Proof points and reference accounts

**Input:** Context Brief (Category 3) + Account data + Activated Play
**Output:** GTM Strategy Brief (tier, pricing, co-invest, expansion path, competitive positioning, 2 references) — ~150 words

### 8e: Delivery COO

Plan execution:
- Resource model (DSA, RSA, AI FDE, Training, GDC, TPM)
- Delivery timeline (60-day Jumpstart → 12-month partnership)
- Accelerator selection from PathToProduction catalog
- Risk mitigation plan
- Success metrics and exit criteria

**Input:** All council outputs + Accelerator matches + Context Brief (Category 6)
**Output:** Delivery Execution Plan (team composition, timeline, top 3 accelerators, 3 success metrics, 2 risks) — ~200 words

### Combine into Solution Architecture Package

Merge all 5 technical expert outputs. This package directly feeds proposal generation.

---

## Step 9: AI Delivery Plan Model (logfood ai_query)

**Run the data-driven delivery plan generator on logfood.**

```bash
SQL=$(cat "$DELIVERY_PLAN_SQL")
SQL_FINAL=$(echo "$SQL" | sed "s/:customer_name/'ACCOUNT_NAME'/g" | sed "s/:is_renewal/'true_or_false'/g")

TOKEN=$(databricks auth token --profile logfood 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")

curl -s -X POST "https://adb-2548836972759138.18.azuredatabricks.net/api/2.0/sql/statements" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "warehouse_id": "74b037a3a9ec9847",
    "statement": "'"$(echo "$SQL_FINAL" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read())[1:-1])")"'",
    "wait_timeout": "120s"
  }'
```

### What the model returns (6 sections)

1. **Executive Hook** — Challenge/solution table from actual blockers, friction, stuck stages
2. **AI COE Delivery Roadmap** — OKRs, Priority, Capability, SME, 60-Day MVP, 2026 Outcomes, Estimated Value
3. **Gantt Chart Data** — Google Sheets-ready timeline with parallel tracks
4. **Business Case** — Investment table with co-invest breakdown + ROI summary
5. **Internal EM Table** — SKU mapping for rate card cross-reference (not customer-facing)
6. **Narrative** — Exec summary, partnership economics, expansion path

### Optional: Workload Sizing Supplement

```bash
if [ -f "$QUICKSIZER_PY" ]; then
  python3 "$QUICKSIZER_PY" \
    --cloud aws \
    --messages-file /tmp/coe_ACCOUNT/quicksizer_messages.json \
    "For ACCOUNT_NAME, estimate monthly DBU costs for: [USE_CASE_1], [USE_CASE_2]"
fi
```

---

## Step 10: Synthesize & Confirm (MANDATORY — DO NOT SKIP)

**BLOCKING:** Present this synthesis and wait for "go" before generating assets.

Present a structured context block that includes the NEW intelligence from the GTM Copilot:

```
═══════════════════════════════════════════════════
   AI COE GTM COPILOT — PROPOSAL SYNTHESIS
═══════════════════════════════════════════════════

Account: [ACCOUNT]
Situation: [new / renewal / qbr / expansion]
Use Cases: [1, 2, 3, 4]
Customer Teams: [team names]

──── ACTIVATED GTM PLAY(S) ────
Primary: [PLAY NAME] (confidence: high/medium)
  Narrative: [1-sentence strategic headline]
Secondary: [PLAY NAME] (if activated)
  Narrative: [1-sentence]

──── STRATEGIC EXPERT COUNCIL FINDINGS ────
Market Analyst: [1-sentence key insight]
Strategy Partner: [transformation vision — 1 sentence]
Economist: [value at stake — $ range]
Workforce Futurist: [operating model change — 1 sentence]
Operating Exec: Feasibility [X/5] — [top risk]

──── SOLUTION ARCHITECTURE COUNCIL ────
Field CTO: [reference architecture — 1 sentence]
Data Architect: [data foundation — key pattern]
AI Architect: [AI stack — key components]
GTM Leader: Tier [X], $[range] customer net cost
Delivery COO: [team composition], [timeline]

──── ENTERPRISE SIGNALS ────
Sources used:
  Drive: [N docs read — list titles]
  Slack: [N threads — key themes]
  Gmail: [N emails — key action items]
  Calendar: [upcoming meetings with dates]
  Salesforce: [N UCOs, N ASQs, N blockers]
  Logfood: [$X annual spend, Tier X]
  Memory Graph: [account history — or "new account"]
  Vector Search: [N similar proposals found — or "not configured"]
  Competitive: [competitors — top differentiators]
  Adoption Heatmap: [top SKUs, readiness score]
  Renewal Risk: [score, category — or "N/A"]
  Accelerators: [N matches from PathToProduction]

──── CUSTOMER THEMES ────
- [theme 1 from research — with source]
- [theme 2]
- [theme 3]

──── COMPETITIVE LANDSCAPE ────
- Primary: [competitor] — [positioning angle]
- Top differentiators: [3 from battlecard]

──── PROPOSED COE PILLARS ────
1. [Pillar name] (P0): [capabilities]
2. [Pillar name] (P1): [capabilities]
3. [Pillar name] (P1): [capabilities]
4. [Pillar name] (P2): [capabilities]
5. Reliability & Governance: [capabilities]
6. COE Operations & Training: [cross-cutting]

──── DELIVERY PLAN MODEL ────
Tier: T[X] ($[range])
Staffing: DSA + [RSA if T3+] + [AI FDE if AI UCs] + Training
Co-invest: [summary]
Customer net cost: $[X]
Quicksizer: [aligned / adjusted / skipped]

Type "go" to generate all assets, or correct anything.
═══════════════════════════════════════════════════
```

Wait for EM confirmation before proceeding.

---

## Steps 11-14: Asset Generation

**IMPORTANT: Sequential workflow — docs first, then slides.**

```
Steps 11 + 12 + 13 → Run IN PARALLEL (3 agents: Golden Path, SOW, Project Plan)
         ↓
Step 14 → Run AFTER docs complete (slides depend on doc content)
```

---

## Step 11: Generate Document 1 — Golden Path to Enterprise AI (Google Doc)

Write markdown to `/tmp/coe_ACCOUNT/golden_path.md` then convert to Google Doc.

### Narrative Voice — Read Instructions Before Writing

**CRITICAL:** The instruction files define the narrative spine:
1. **Problem** — "We're spending on AI but not shipping it" (customer-specific evidence)
2. **The Shift** — From experiments to AI products on one platform
3. **Golden Path** — Data Foundation → Semantics → AI Apps → Govern
4. **AI COE MVP** — 1 domain, 1 AI product, 1 KPI in 60 days
5. **Why This Wins** — Clear path, unified platform, reusable COE

### Document Structure — Enhanced with Council Intelligence

```markdown
# [ACCOUNT] — Golden Path to Enterprise AI
## AI Center of Excellence | Databricks Field Engineering

**Account:** [ACCOUNT]
**Prepared by:** ${USER_NAME}, ${USER_TITLE}, ${USER_TEAM}
**Date:** [today]
**Engagement Type:** [from activated play narrative]
**GTM Play:** [PRIMARY_PLAY name]

———

## Executive Context

[4 DENSE PARAGRAPHS — now enriched by Strategic Expert Council outputs]

**Paragraph 1 — Platform Foundation & Business Context:**
[Account relationship, consumption, champions — enriched by Graph Intelligence Brief and Market Analyst findings]

**Paragraph 2 — The Strategic Imperative:**
[AI fragmentation problem — enriched by Strategy Partner's transformation vision and capability gaps. Include the Economist's cost-of-inaction estimate.]

**Paragraph 3 — Revenue/Strategic Expansion Opportunity:**
[Business-side expansion — enriched by AI Workforce Futurist's operating model vision and GTM Strategy Leader's commercial approach]

**Paragraph 4 — The AI COE as Delivery Vehicle:**
[COE as the answer — enriched by Delivery COO's execution plan and Operating Executive's feasibility assessment. Address the #1 failure mode to avoid.]

———

## Industry Context & Market Intelligence

[NEW SECTION — from Market Analyst. 3-4 paragraphs on:]
- Industry disruption signals affecting [ACCOUNT]
- Technology inflection points creating urgency
- Competitive landscape: peers who have moved, peers who are stuck
- The "why now" catalyst specific to this account

———

## Transformation Vision

[NEW SECTION — from Strategy Partner. Define:]
- What [ACCOUNT] looks like in 3 years with a mature AI platform
- The 3-5 strategic initiatives that bridge today to that future
- Value creation model: 3-year value estimate with ranges (from Economist)
- AI workforce transformation: how teams work differently (from Futurist)

———

## Partnership Phasing Overview

| Phase | Name | Duration | Focus | Success Gate | Investment |
|---|---|---|---|---|---|
| Phase 0 | Discovery & Architecture | Weeks 1-2 | ... | ... | $0 (included) |
| Phase 1 | 60-Day Jumpstart | Weeks 3-10 | ... | ... | $[X]K net |
| Phase 2 | Revenue Scale | Months 3-6 | ... | ... | $[X]K net |
| Phase 3 | Platform Independence | Months 7-12 | ... | ... | $[X]K net |

———

## Golden Path Capability Mapping

| Golden Path Workstream | Capability | [ACCOUNT] Workstreams | [ACCOUNT] Priorities | Databricks COE Resources | 60-Day Jumpstart Outcomes | FY27 Scale Outcomes |
|---|---|---|---|---|---|---|
[5-7 ROWS — enriched by Solution Architecture Council outputs]

———

## Target Architecture

[NEW SECTION — from Field CTO + Data Architect + AI Architect]
- 4-layer Lakehouse architecture with specific Databricks products per layer
- Data foundation design (ingestion, governance, semantic layer)
- AI platform design (MLOps, GenAI stack, evaluation, serving)
- Integration points with existing customer systems
- Migration path from current architecture

———

## Delivery Accelerators

[NEW SECTION — from PathToProduction catalog + Delivery COO]

| Accelerator | Source | Category | Deploy Time | Relevance |
|---|---|---|---|---|
| [Accelerator 1] | PathToProduction | AI/ML | 2 days | [why it fits] |
| [Accelerator 2] | Field Engineering | Data Foundation | 1 week | [why it fits] |
| ... | ... | ... | ... | ... |

These field-engineered solutions form the foundation of the recommended architecture. Each has been validated in production environments.

———

## COE Engagement Model

**Duration:** 60 days (Jumpstart) → 12-month partnership
**Staffing:** [from Delivery COO + Resource Planner]
**Governance:** Weekly COE steering, bi-weekly executive check-in
**SI Partner:** [from research]

———

## COE Operating Model

| Role | Responsibility | Allocation |
|---|---|---|
[From Delivery COO output + resource planner]

———

## Success Metrics

| Metric | 60-Day Target | FY27 Target |
|---|---|---|
[Enriched by Economist's value creation model]

———

## Why Databricks — Minimum Required Capabilities

| Capability | What [ACCOUNT] Needs | Why Only Databricks | Alternative Gap |
|---|---|---|---|
[Enriched by competitive intelligence from play definition + battlecard registry]

———

## Value Creation & ROI

[NEW SECTION — from Transformation Economist]
- 3-year value creation estimate with confidence ranges
- ROI multiple and payback period
- Top value drivers ranked by magnitude
- Cost of inaction comparison

———

## Execution Feasibility

[NEW SECTION — from Industry Operating Executive]
- Feasibility score with rationale
- Top execution risks and mitigations
- Required organizational changes
- Executive sponsorship requirements
- Common failure modes to avoid
```

### Create the Google Doc

```bash
python3 "$MARKDOWN_TO_GDOCS" \
  --input /tmp/coe_ACCOUNT/golden_path.md \
  --title "[ACCOUNT] — Golden Path to Enterprise AI"
```

---

## Step 12: Generate Document 2 — AI COE Statement of Work (Google Doc)

Write to `/tmp/coe_ACCOUNT/sow.md` then convert.

### SOW Structure (same as existing, enriched with council outputs)

```markdown
# [ACCOUNT] — AI COE MVP: Statement of Work
## DRAFT | [today's date]

---

## Overview

This Statement of Work describes professional services to be performed by Databricks, Inc.
for [ACCOUNT] to establish an AI Center of Excellence (AI COE) MVP.

---

## Engagement Summary

| | |
|---|---|
| **Customer** | [ACCOUNT] |
| **Engagement Type** | [from activated play] |
| **Duration** | ~[8-12] calendar weeks |
| **Estimated Person-Days** | Up to [50-60] total |
| **Start Date** | [from calendar research] |
| **Primary Contact** | ${USER_NAME}, ${USER_TITLE} |

---

## Scope of Work

[N] primary workstreams + cross-cutting enablement:
[LIST from delivery plan model + Solution Architecture Council]

---

## [1. USE CASE NAME]

**Objective:** [1-2 sentences — enriched by Strategy Partner's initiative mapping]

### In-Scope Activities

**Use case definition & success criteria**
- [from Delivery COO's execution plan]

**Architecture & design**
- [from Field CTO + AI Architect outputs]

**MVP implementation**
- [from delivery plan model + accelerator matches]

**Testing & validation**
- [from AI Architect's evaluation framework]

**Handover & documentation**
- Architecture diagrams, configuration guidelines, runbook notes

### Deliverables
- [Specific artifacts with measurable definitions of done]

---

[REPEAT FOR EACH USE CASE]

---

## [N+1]. Training, Knowledge Transfer, and COE Operating Model

**Objective:** Ensure [ACCOUNT] teams can operate and scale the AI COE independently.

### In-Scope Activities
[From Workforce Futurist + Delivery COO]

---

## Out of Scope
[Customer-specific exclusions from research]

---

## Assumptions
[From Operating Executive's feasibility assessment]

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
[From Operating Executive's top 3 risks + Delivery COO's risk plan]

---

## Exit Criteria (60-Day Jumpstart)

| Deliverable | Definition of Done |
|---|---|
[From Delivery COO's success metrics]

---

## Investment Summary

[FROM Delivery Plan Model + GTM Strategy Leader + Resource Planner]

| Resource | Duration | List Price | Net Price |
|---|---|---|---|
[Full breakdown with co-invest]

### ROI Summary

| Metric | 60-Day Jumpstart | Full Year |
|---|---|---|
[From Transformation Economist's value model]

---

## Acceptance

| | Name | Title | Date |
|---|---|---|---|
| [ACCOUNT] | | | |
| Databricks, Inc. | | | |

*Draft for discussion purposes. Final terms in Order Form and Services Agreement.*
```

### Create the Google Doc

```bash
python3 "$MARKDOWN_TO_GDOCS" \
  --input /tmp/coe_ACCOUNT/sow.md \
  --title "[ACCOUNT] — AI COE MVP Statement of Work (DRAFT)"
```

---

## Step 13: Generate Document 3 — Project Plan & Gantt (Google Sheets)

Create a Google Sheet with three tabs: **Project Plan**, **Gantt Chart**, **Milestones**.

### Data Source

Use delivery plan model Section 3 (Gantt Data) + Delivery COO's execution plan + accelerator timeline.

### Tab 1: Project Plan (30-35 tasks)

Generate 30-35 tasks spanning W1-W35:
- **60-Day Jumpstart** (W1-W8, ~14 tasks)
- **Full Year / SCALE** (W9-W35, ~21 tasks)

Column structure:
```
| Workstream | Task | Owner (DB Role) | Start Week | Duration (Weeks) | Dependencies | Phase | Status |
```

### Tab 2: Gantt Chart (W1-W35)

Visual timeline with conditional formatting:
- `#2272B4` (DB_BLUE) for Jumpstart cells
- `#00A972` (DB_GREEN) for SCALE cells

### Tab 3: Milestones (7-8 milestones)

```
| Milestone | Week | Description | Success Criteria | Owner |
```

### Create and Format

```bash
TOKEN=$(python3 "$GOOGLE_AUTH" token 2>/dev/null)

curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -d '{
    "properties": {"title": "[ACCOUNT] — AI COE Project Plan"},
    "sheets": [
      {"properties": {"title": "Project Plan", "sheetId": 0}},
      {"properties": {"title": "Gantt Chart", "sheetId": 1}},
      {"properties": {"title": "Milestones", "sheetId": 2}}
    ]
  }'
```

---

## Step 14: Generate Executive Slide Deck (Google Slides)

**Run AFTER Steps 11-13 complete.** The deck is generated FROM the Golden Path doc — the doc is the single source of truth for slide content.

### Deck Generation Pipeline

The deck orchestrator chains 5 modules in sequence:

```
Golden Path Doc → EXTRACT → ROUTE → COMPOSE → VALIDATE → TRANSFORM → RENDER
```

| Stage | Module | What It Does |
|---|---|---|
| 1. EXTRACT | deck_orchestrator | Reads Golden Path Google Doc, parses all tables/sections/metrics |
| 2. ROUTE | slide_router + slide_knowledge_graph | Selects 8-25 slides from 148-slide library based on play, industry, architecture |
| 3. COMPOSE | narrative_engine | Applies SCR consulting reasoning: Title=Insight, Bullets=Evidence, Visual=Implication |
| 4. VALIDATE | slide_validator | Quality checks (word limits, consulting reasoning, brand), auto-fixes violations |
| 5. TRANSFORM | deck_orchestrator | Converts enriched slides to deck_builder spec JSON |
| 6. RENDER | deck_builder | Creates Google Slides on deep teal background with Databricks 2025 design system |

### Consulting Slide Reasoning (Every Slide)

Every slide follows: **Insight → Evidence → Implication**
- **Title** = Insight (6-12 words, account-specific, NOT generic like "Executive Summary")
  - GOOD: "MGM's $3.4M Platform Is Ready for AI — Google Competes for the Win"
  - BAD: "Executive Summary"
- **Bullets** = Evidence (3-5 items, each ≤15 words, each with specific metric or fact)
- **Visual** = Implication (what should the audience do with this information?)

### Narrative Structure (SCR)

Slides follow the consulting storytelling arc:

| Stage | Purpose | Typical Slides |
|---|---|---|
| SITUATION | Set the stage — what's true today | Executive Summary, Industry Context |
| COMPLICATION | The problem — why this can't continue | Strategic Imperative, Challenges |
| RESOLUTION | The answer — transformation vision + outcomes | Transformation Vision, Business Outcomes |
| ARCHITECTURE | How — platform design + operating model | Architecture, Operating Model |
| VALUE | The economics — ROI, investment, payback | Value Creation, Investment |
| ROADMAP | When — phased delivery plan + milestones | Roadmap, Delivery Model |
| CLOSE | What's next — prescriptive actions with dates | Next Steps |
| APPENDIX | Supporting detail — tables, differentiation | Phasing, Capability Mapping, Why Databricks |

### Deck Sizes

| Size | Slide Count | When to Use |
|---|---|---|
| compact | 8-12 | Simple proposals, focused scope |
| standard | 12-18 | Mid-range engagements |
| strategic | 18-25 | Large AI COE, full program (like JLL, MGM) |

### Build and Run

```bash
# Step 14a: Write routing context from Steps 1-10
cat > /tmp/coe_ACCOUNT/routing_context.json << 'EOF'
{
  "account": "ACCOUNT_NAME",
  "play": "PRIMARY_PLAY",
  "secondary_plays": ["SECONDARY_PLAY"],
  "industry": "INDUSTRY",
  "architecture_signals": ["signal1", "signal2"],
  "proposal_size": "strategic",
  "engagement_type": "AI COE — [Engagement Description]",
  "date": "[Month Year]",
  "prepared_by": "${USER_NAME}, ${USER_TITLE}, ${USER_TEAM}"
}
EOF

# Step 14b: ONE COMMAND — full pipeline
python3 "$DECK_ORCHESTRATOR" \
  --doc-id "GOLDEN_PATH_DOC_ID" \
  --context /tmp/coe_ACCOUNT/routing_context.json \
  --size strategic

# The orchestrator:
# 1. Reads the Golden Path doc
# 2. Selects slides from 148-slide knowledge graph
# 3. Applies consulting reasoning (SCR)
# 4. Validates quality (auto-fixes if score < threshold)
# 5. Transforms to deck spec
# 6. Renders to Google Slides
# Returns: Presentation URL + quality report
```

### Quality Gating

| Score | Action |
|---|---|
| >= 0.85 | Auto-rendered, no review needed |
| 0.5-0.85 | Rendered with warnings — review suggestions |
| < 0.5 | Stopped before render — review spec, fix, re-run |

### Two-Pass Workflow (Optional — For High-Stakes Decks)

```bash
# Pass 1: Dry run — generates spec + quality report, no render
python3 "$DECK_ORCHESTRATOR" \
  --doc-id "GOLDEN_PATH_DOC_ID" \
  --context /tmp/coe_ACCOUNT/routing_context.json \
  --dry-run

# Review checkpoint output — slide selections, titles, quality score
# Adjust spec at /tmp/coe_ACCOUNT/slides_spec.json if needed

# Pass 2: Render from reviewed spec
python3 "$DECK_BUILDER" --spec /tmp/coe_ACCOUNT/slides_spec.json
```

### Override Slide Selections

If the router's auto-selection doesn't match the narrative you want:

```bash
# Create override selections JSON
python3 "$DECK_ORCHESTRATOR" \
  --doc-id "GOLDEN_PATH_DOC_ID" \
  --context /tmp/coe_ACCOUNT/routing_context.json \
  --overrides /tmp/coe_ACCOUNT/slide_overrides.json
```

---

## Step 14c: Build Complete Slide Deck (Canonical 17-Slide Flow)

**This is the definitive deck build pipeline. Every customer proposal follows this exact structure.**

### Canonical Slide Order (17 main + appendix)

| # | Slide | Builder | Config |
|---|---|---|---|
| 1 | Title | Branded template COPY | replaceAllText |
| 2 | Agenda (hexagon) | Template COPY | replaceAllText |
| 3 | Platform Momentum | `layout_title_bullets` | inline |
| 4 | Challenge / Solution | `build_challenge_solution_slide.py` | challenge_solution_config.json |
| 5 | Use-Case Architecture | `build_usecase_arch.py` | inline customization |
| 6 | DEMO | Template COPY | — |
| 7 | Hero Numbers | `build_hero_numbers_slide.py` | hero_numbers_config.json |
| 8 | Phase 1 Cards | `build_phase1_cards_slide.py` | phase1_cards_config.json |
| 9 | Current State Bullets | `layout_title_bullets` | inline |
| 10 | Current State Arch | `build_arch_diagrams.py` | inline customization |
| 11 | Future State Bullets | `layout_title_bullets` | inline |
| 12 | Future State Arch | `build_arch_diagrams.py` | inline customization |
| 13 | Gantt Timeline | `build_gantt_slide.py` | gantt_config.json |
| 14 | Value Bridge | `build_value_slide.py` | value_config.json |
| 15 | Why Databricks | `build_why_databricks_slide.py` | why_db_config.json |
| 16 | Success Metrics | `build_success_metrics_slide.py` | success_metrics_config.json |
| 17 | MSP | `build_msp_slide.py` | msp_config.json |
| 18 | Appendix separator | Template COPY | — |
| 19 | Investment Summary | `layout_table` | inline |
| 20 | Cost of Inaction | `layout_table` | inline |
| 21+ | COE Framework + backups | Template slides | backup appendix |

### Build Steps

```bash
# 1. Copy branded template
TEMPLATE="1abn8VFYaQeMbQUY_MuAkhgKYrBffN7s0airkwASMc7Y"
# Copy via Drive API, get PRES_ID

# 2. Build bullet slides (3, 9, 11) using narrative_deck_builder
python3 "$NARRATIVE_DECK_BUILDER" ...  # layout_title_bullets for each

# 3. Build LOCKED slides (4, 5, 7, 8, 10, 12, 13, 14, 15, 16, 17)
python3 "$CHALLENGE_SOLUTION_PY" --pres-id "$PRES_ID" --config challenge_solution_config.json
python3 "$USECASE_ARCH_PY" ...  # inline customization
python3 "$HERO_NUMBERS_PY" --pres-id "$PRES_ID" --config hero_numbers_config.json
python3 "$PHASE1_CARDS_PY" --pres-id "$PRES_ID" --config phase1_cards_config.json
python3 "$ARCH_DIAGRAMS_PY" ...  # current + future state
python3 "$GANTT_SLIDE_PY" --pres-id "$PRES_ID" --config gantt_config.json
python3 "$VALUE_SLIDE_PY" --pres-id "$PRES_ID" --config value_config.json
python3 "$WHY_DB_SLIDE_PY" --pres-id "$PRES_ID" --config why_db_config.json
python3 "$SUCCESS_METRICS_PY" --pres-id "$PRES_ID" --config success_metrics_config.json
python3 "$MSP_SLIDE_PY" --pres-id "$PRES_ID" --config msp_config.json

# 4. Build appendix tables
python3 "$NARRATIVE_DECK_BUILDER" ...  # layout_table for Investment, Cost of Inaction

# 5. Reorder slides to canonical order (1-17 main, 18+ appendix)

# 6. Update branded text
# replaceAllText: {{COMPANY}}, {{ENGAGEMENT}}, {{DATE}}, {{PREPARED_BY}}
```

### Text Padding Rule (ALL builders)

Google Slides text boxes have 0.1" default top padding that the REST API cannot zero.
- `pad_compensate=True` (default): shifts Y up 0.1" for free-standing text boxes
- `pad_compensate=False`: text inside containers (badges, shaped headers), titles, and full-height row text using `valign=MIDDLE`

### Color Rules for Hero Numbers
- Dollar amounts: WHITE (grayscale — neutral)
- ROI multiples: GREEN (positive)
- Payback period: GREEN or WHITE (neutral-to-positive)
- Phase counts: WHITE (neutral)
- Auto-shrink: values >5 chars → 36pt, >8 chars → 28pt

### Bottom Margin Consistency
All slides with panels/trays: bottom at Y=5.24"

### Appendix Strategy
The template provides ~15 COE Framework slides and backup versions of customized slides.
These stay in the appendix as a safety net — if any programmatic slide needs fixing,
the flat-table backup can be swapped in from the appendix.

---

## Step 14c-legacy: Architecture Diagrams Reference

**Architecture diagrams (slides 5, 10, 12) use the self-contained builders.**

**After the executive deck, generate visual architecture diagrams using the self-contained builders.**

Two architecture diagram types are available as plugin resources:

### Current/Future State Architecture (`build_arch_diagrams.py`)

Generates a 2-slide Google Slides deck:
- **Slide 1 — Current State**: Shows the customer's existing data architecture layers with pain points highlighted
- **Slide 2 — Future State**: Shows the Databricks-powered target architecture with Bronze/Silver/Gold medallion layers

The script uses its own positioning helpers (no safe-frame clamping) for precise architectural diagram layout with alternating context tray backgrounds.

```bash
ARCH_BUILDER="$RESOURCES/build_arch_diagrams.py"

# Before running: customize the LAYERS, CURRENT_STATE_BOXES, FUTURE_STATE_BOXES
# data structures in the script to match the customer's actual architecture.
# The MGM example shows the pattern — adapt labels, components, and pain points.

python3 "$ARCH_BUILDER"
# Returns: presentation URL + thumbnail PNGs in /tmp/coe_ACCOUNT/arch_diagrams/
```

### Use-Case Architecture (`build_usecase_arch.py`)

Generates a single-slide 6-stage left-to-right pipeline architecture:
- Stages flow from data ingestion through to business outcomes
- Each stage column shows 2-3 component boxes
- New/Databricks components get a green left border accent
- Right panel shows Key Metrics and Known Limitations
- Flow arrows connect stages horizontally

```bash
USECASE_BUILDER="$RESOURCES/build_usecase_arch.py"

# Before running: customize STAGES (6 stages with boxes), KEY_METRICS,
# and KNOWN_LIMITATIONS in the script to match the specific use case.
# The CLV example shows the pattern — adapt for the customer's use case.

python3 "$USECASE_BUILDER"
# Returns: presentation URL + thumbnail PNG in /tmp/coe_ACCOUNT/usecase_arch/
```

### Architecture Diagram Rules

1. **Always customize before running** — The scripts contain example data (MGM). Update all customer-specific labels, components, metrics, and limitations before execution.
2. **Self-contained rendering** — Both scripts handle Google Slides API auth and batch updates internally. No external dependencies beyond `narrative_deck_builder.py` (for `build_arch_diagrams.py` only).
3. **Include in final deliverable** — Link the architecture diagram presentations in the customer's Golden Path doc and reference them in the executive deck appendix.
4. **Export thumbnails** — Both scripts auto-export PNG thumbnails for embedding in other documents.

---

## Step 14d: Generate Gantt Timeline Slide (Google Slides)

**After architecture diagrams, generate a 12-month partnership timeline using the Gantt builder.**

The Gantt slide shows phase-colored workstream bars, milestone markers, a KEY MILESTONES panel, and a team mapping table — all on a single slide. It uses the locked format from the Rockstar Games iteration.

### How to invoke

```bash
GANTT_BUILDER="$RESOURCES/build_gantt_slide.py"

# Write config JSON with customer-specific data
cat > /tmp/coe_ACCOUNT/gantt_config.json << 'GANTT_EOF'
{
  "title": "Partnership Timeline",
  "subtitle": "12-month roadmap: urgency first, platform second, self-sufficiency by month 12",
  "phases": ["Phase 1: Game Launch", "Phase 2: Platform Build", "Phase 3: Scale & Mature"],
  "months": ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"],
  "workstreams": [
    {"name": "Telemetry Platform", "start_col": 0, "span": 3, "phase": 1, "label": "Streaming + Health Dashboards"},
    {"name": "AI Copilot",         "start_col": 1, "span": 3, "phase": 1, "label": "NL Triage: 'What's failing?'"},
    {"name": "Migration",          "start_col": 2, "span": 5, "phase": 2, "label": "Legacy exit → Lakehouse"},
    {"name": "Feature Platform",   "start_col": 3, "span": 6, "phase": 2, "label": "Shared features cross-BU"},
    {"name": "Trust & Safety",     "start_col": 4, "span": 3, "phase": 3, "label": "Anti-fraud + compliance"},
    {"name": "COE Operations",     "start_col": 0, "span": 12, "phase": 2, "label": "War room → Self-sufficient"}
  ],
  "milestones": [
    {"col": 2, "month_label": "Month 3 (Jun)", "title": "MVP", "desc": "Health dashboard + first streams live"},
    {"col": 4, "month_label": "Month 5 (Aug)", "title": "Migration Tooling", "desc": "Framework + first 50 tables"},
    {"col": 7, "month_label": "Month 8 (Nov)", "title": "Go-Live", "desc": "Full war-room support"},
    {"col": 8, "month_label": "Month 9 (Dec)", "title": "Feature GA", "desc": "Cross-BU features in production"},
    {"col": 8, "month_label": "Month 9 (Dec)", "title": "Legacy Exit", "desc": "All workloads on Databricks"},
    {"col": 11, "month_label": "Month 12 (Mar)", "title": "COE Handoff", "desc": "Customer owns platform, thin DB bridge"}
  ],
  "teams": [
    {"cells": ["Launch Phase", "60 days", "Launch Team", "DSA + RSA", "Lakeflow, DQX, Metrics", "Copilot | WAF"]},
    {"cells": ["Migration + Features", "9 months", "DE Lead + DS Lead", "RSA + AI FDE", "UC Iceberg, Feature Store", "Lakebridge | UCX"]},
    {"cells": ["COE & Trust", "12 months", "C-Suite + Security", "DSA (bridge)", "GenAI, Training", "Dev Kit | FinOps"]}
  ],
  "team_headers": ["WORKSTREAM", "DURATION", "CUSTOMER LEAD", "DB SME", "CAPABILITY", "ACCELERATORS"],
  "team_col_widths": [1.40, 0.70, 1.50, 1.10, 2.20, 2.60]
}
GANTT_EOF

python3 "$GANTT_BUILDER" --pres-id "$PRES_ID" --config /tmp/coe_ACCOUNT/gantt_config.json
```

### Key customization points

Before running, update the config JSON with customer-specific data:
- **workstreams**: Map to the customer's actual engagement phases. `start_col` is 0-indexed (0=first month). `span` is number of months. `phase` determines bar color (1=black, 2=teal, 3=dark).
- **milestones**: `col` is 0-indexed month. Include 4-6 major milestones with concise titles and descriptions.
- **teams**: Each row has `cells` matching the `team_headers` columns. Customize column count/widths as needed.
- **months**: Default is Apr-Mar. Adjust to match the customer's fiscal year or engagement start.

### Notes

1. **Self-contained rendering** — The script handles Google Slides API auth and batch updates internally. No external dependencies.
2. **Month labels are CENTER-aligned** — Each label is exactly 0.50" wide matching its column, with CENTER paragraph alignment.
3. **No safe-frame clamping** — Unlike `narrative_deck_builder.py`, this builder places elements at exact coordinates (title at Y=0.10", grid at Y=1.07").
4. **6-column team table** — Default headers: WORKSTREAM, DURATION, CUSTOMER LEAD, DB SME, CAPABILITY, ACCELERATORS. Override via `team_headers` and `team_col_widths`.

---

### Text Box Padding Compensation (ALL programmatic slides)

Google Slides text boxes have a default 0.1" top internal padding that the REST API cannot set to 0. All slide builders use `pad_compensate=True` in `_txt()` to shift text box Y up 0.1", so text renders at intended coordinates.

**Exceptions** (use `pad_compensate=False`):
- Title/subtitle text boxes (natural padding is fine for headers)
- Text inside round_rect badges (positioned by container, not top edge)
- Tray header labels positioned tight to tray top (e.g. "EVIDENCE", "KEY ASSUMPTIONS")

This pattern must be applied to ALL new slide builders. See `build_why_databricks_slide.py` for the reference implementation.

---

## Step 14e: Generate Value Bridge Slide (Google Slides)

**After the Gantt timeline, generate a Value Bridge waterfall showing cumulative partnership value.**

This slide answers "what do we get from executing the timeline on slide 13?" in the customer's voice — defensible, calculated, and ready for their leadership.

### How to invoke

```bash
VALUE_BUILDER="$RESOURCES/build_value_slide.py"

cat > /tmp/coe_ACCOUNT/value_config.json << 'VALUE_EOF'
{
  "title": "Projected 12-Month Value from AI Center of Excellence",
  "subtitle": "Value estimates developed jointly with ACCOUNT and Databricks Field Engineering",
  "value_bars": [
    {"name": "Telemetry\nPlatform", "value": 1.2, "phase": 1, "method": "$6.48M platform × 18% efficiency gain", "category": "hard_savings"},
    {"name": "Migration", "value": 0.8, "phase": 2, "method": "$800K/yr dual-platform cost eliminated", "category": "hard_savings"},
    {"name": "AI/ML\nActivation", "value": 0.6, "phase": 2, "method": "3 models × $200K revenue/model", "category": "revenue"},
    {"name": "Governance\n+ Sharing", "value": 0.4, "phase": 2, "method": "20 FTEs × 15% productivity gain", "category": "productivity"},
    {"name": "Live-Ops\nIntelligence", "value": 0.3, "phase": 3, "method": "MTTR 4hr→30min × $50K/incident", "category": "revenue"}
  ],
  "methodology": [
    {"category": "Hard Savings", "amount": "$1.6M", "desc": "Infrastructure consolidation + reduced vendor licensing", "color_key": "hard_savings"},
    {"category": "Productivity Gains", "amount": "$0.7M", "desc": "20 engineers × $85/hr × 40% efficiency gain", "color_key": "productivity"},
    {"category": "Revenue Acceleration", "amount": "$1.0M", "desc": "Faster TTM, real-time personalization, reduced incidents", "color_key": "revenue"}
  ],
  "assumptions": [
    "Loaded labor rate: $85/hr (customer HR data)",
    "Legacy platform annual spend (customer finance)",
    "Efficiency gains: Forrester TEI benchmark (417-482% ROI)",
    "25% risk adjustment applied to all estimates",
    "Values reflect Year 1 run-rate after Phase 1 MVP",
    "Incident cost: $50K/critical incident (customer ops data)"
  ],
  "hero_total": "$3.3M",
  "hero_roi": "6.6x",
  "hero_payback": "<60d",
  "risk_adjustment": "25%"
}
VALUE_EOF

python3 "$VALUE_BUILDER" --pres-id "$PRES_ID" --config /tmp/coe_ACCOUNT/value_config.json
```

### Key design decisions (locked format)

- **Waterfall bars** stack additively left-to-right from $0 to total value. Colors match Gantt phase colors.
- **Scale**: 0.807"/\$1M (absolute, not relative). Bars can extend above the highest gridline.
- **Baseline** ($0) at Y=3.87". **Labels** at Y=3.88". **Bottom margin** at Y=5.24" (matches Gantt).
- **VALUE METHODOLOGY panel** (right, Y=0.75", H=4.49"): extends to 5.24" bottom margin. Description text indented 0.10" from amounts for readability.
- **KEY ASSUMPTIONS strip** (Y=4.39", H=0.85"): 2-column bullet layout with source attribution footnote.
- **Hero metrics** (12pt) at top right: Total Value (coral), ROI (green), Payback (gold).
- **Total bar** (coral): spans full chart height, 20pt hero number, ROI + Payback left-aligned inside.
- **Risk adjustment**: called out in coral within the methodology panel.

### Customization

- **value_bars**: Map to customer workstreams. `value` is in millions. `category` determines the accent strip color (hard_savings=green, productivity=teal, revenue=gold). `method` is the 1-line calculation.
- **methodology**: 3 categories that sum to total. Each has amount, description, and color_key.
- **assumptions**: Source-tag each one (customer-provided vs. industry benchmark). Include risk adjustment.
- **hero_total/roi/payback**: Must be consistent with the Hero Numbers slide (slide 7).

---

## Step 14f: Generate Why Databricks Slide (Google Slides)

**After the value slide, generate an outcome-mapped competitive differentiation slide.**

This replaces flat comparison tables with outcome cards in the customer's voice. Each card maps a project outcome to the platform capability that delivers it and the risk of choosing alternatives.

### How to invoke

```bash
WHY_DB_BUILDER="$RESOURCES/build_why_databricks_slide.py"

cat > /tmp/coe_ACCOUNT/why_db_config.json << 'WDB_EOF'
{
  "title": "We selected Databricks because it's the only platform that unifies our data, AI, and governance",
  "subtitle": "Platform selection rationale — ACCOUNT AI Center of Excellence",
  "outcome_cards": [
    {
      "outcome": "Project Outcome Name",
      "need": "What we need technically",
      "capability": "Databricks Capability Stack",
      "why": "Why ONLY Databricks delivers this natively",
      "risk": "What we lose if we choose the alternative",
      "phase": 1
    }
  ],
  "alternatives": [
    {"name": "Snowflake", "note": "Strong warehousing but no native streaming, ML bolted on"},
    {"name": "AWS Native", "note": "Would fragment across 4+ services, no unified governance"}
  ],
  "proof_points": [
    "Forrester TEI: 417-482% ROI, <6 month payback",
    "IDC MarketScape Leader: Unified AI Governance 2025-2026",
    "Peer win: Gaming company, 23x ROI"
  ]
}
WDB_EOF

python3 "$WHY_DB_BUILDER" --pres-id "$PRES_ID" --config /tmp/coe_ACCOUNT/why_db_config.json
```

### Design principles

- **Action title** = the conclusion ("We selected Databricks because..."), not a topic ("Platform Comparison")
- **3-4 outcome cards max** — executives remember 3 things, not 5
- **Customer voice**: "WE NEED" / "RISK WITHOUT" framing, not "Databricks offers"
- **Competitors referenced neutrally**: "alternatives required additional tooling"
- **Proof points strip** (bottom): analyst recognition + peer wins
- **ALTERNATIVES EVALUATED panel** (right): concise, fair, 1-line assessments
- **Phase colors match Gantt** — visual continuity across the deck

### Content sourcing

Pull competitive differentiators from the battlecard registry (`battlecard-registry.yaml` in fe-workflows competitive-analysis skill). Key competitors:
- **Snowflake**: Unified data+AI vs warehouse-only, streaming, open formats, MLflow
- **Fabric**: Open multi-cloud vs Azure-only, depth vs bundled convenience
- **Redshift**: Full platform vs AWS-native warehouse, multi-cloud
- **AWS Native**: Unified governance vs fragmented services

Always frame as outcome-mapped: "For THIS project outcome, only Databricks delivers X natively."

---

## Step 14g: Generate Mutual Success Plan Slide (Google Slides)

**After the Why Databricks slide, generate a phased Mutual Success Plan roadmap.**

Replaces flat action tables with a 4-phase horizontal roadmap showing dual ownership, decision gates, and governance cadence. Customer voice throughout.

### How to invoke

```bash
MSP_BUILDER="$RESOURCES/build_msp_slide.py"

cat > /tmp/coe_ACCOUNT/msp_config.json << 'MSP_EOF'
{
  "title": "Our Mutual Path to [Customer Outcome]",
  "subtitle": "Mutual Success Plan — ACCOUNT × Databricks AI COE",
  "shared_objective": "Success = [60-day MVP outcome], [war-room/ops outcome], and Phase 2 roadmap approved",
  "phases": [
    {
      "name": "Foundation", "duration": "Weeks 1-3",
      "milestones": [
        {"text": "Customer validates architecture approach", "owner": "customer"},
        {"text": "Databricks delivers blueprint", "owner": "databricks"},
        {"text": "SOW reviewed and approved", "owner": "joint"}
      ],
      "outcome": "SOW signed, architecture validated"
    },
    {
      "name": "Mobilization", "duration": "Weeks 3-4",
      "milestones": [
        {"text": "Steering Committee formed", "owner": "customer"},
        {"text": "DSA + RSA onboarded", "owner": "databricks"},
        {"text": "Office hours cadence established", "owner": "joint"}
      ],
      "outcome": "Team staffed, cadence running"
    },
    {
      "name": "Sprint", "duration": "Months 2-3",
      "milestones": [
        {"text": "MVP deliverables completed", "owner": "databricks"},
        {"text": "Customer ops team validates", "owner": "customer"},
        {"text": "60-day checkpoint with leadership", "owner": "joint"}
      ],
      "outcome": "MVP accepted"
    },
    {
      "name": "Scale & Transfer", "duration": "Month 3+",
      "milestones": [
        {"text": "Team trained on operations", "owner": "databricks"},
        {"text": "Phase 2 scope defined", "owner": "joint"},
        {"text": "Quarterly COE Review", "owner": "joint"}
      ],
      "outcome": "Phase 2 approved, customer owns platform"
    }
  ],
  "gates": ["SOW\nSigned", "Env\nReady", "MVP\nAccepted"],
  "cadence": [
    {"frequency": "Weekly", "forum": "Office Hours", "purpose": "Hands-on technical unblocking"},
    {"frequency": "Bi-weekly", "forum": "Sprint Demo", "purpose": "Progress review with stakeholders"},
    {"frequency": "Monthly", "forum": "Steering Committee", "purpose": "Strategic alignment + resource decisions"},
    {"frequency": "Quarterly", "forum": "COE Review", "purpose": "Portfolio performance + expansion"}
  ],
  "footer_text": "This plan succeeds when both teams commit. Databricks is investing alongside ACCOUNT — mutual skin in the game."
}
MSP_EOF

python3 "$MSP_BUILDER" --pres-id "$PRES_ID" --config /tmp/coe_ACCOUNT/msp_config.json
```

### Design principles

- **HOME_PLATE arrow headers** show left-to-right timeline cascade
- **Owner legend in top banner** (coral=customer, green=Databricks, teal=joint) — visible before reading milestones
- **Decision gates below phases** (Y=3.88") — coral diamonds between columns
- **Outcome bars** (coral, Y=3.33") with text below — what's true when phase completes
- **Governance cadence strip** (Y=4.28") — Weekly/Bi-weekly/Monthly/Quarterly with forum + purpose
- **Partnership footer** (Y=4.90") — mutual commitment statement
- **Customer voice**: "Your team validates..." not "Databricks delivers..."

---

## Step 15: Memory Write-Back

**After generating all assets, persist new intelligence back to the Strategic Memory Graph.**

```bash
if [ -f "$MEMORY_GRAPH_PY" ]; then
  LOGFOOD_TOKEN=$(databricks auth token --profile logfood 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

  python3 "$MEMORY_GRAPH_PY" write-back \
    --host "$LOGFOOD_HOST" \
    --token "$LOGFOOD_TOKEN" \
    --warehouse "$LOGFOOD_WAREHOUSE" \
    --catalog "$MEMORY_CATALOG" \
    --schema "$MEMORY_SCHEMA" \
    --account "ACCOUNT_NAME" \
    --proposal-data /tmp/coe_ACCOUNT/proposal_metadata.json 2>/dev/null
fi
```

### What Gets Written Back

```json
{
  "account": "ACCOUNT_NAME",
  "proposal": {
    "play_type": "PRIMARY_PLAY",
    "secondary_plays": ["PLAY_2"],
    "doc_urls": {
      "golden_path": "URL",
      "sow": "URL",
      "project_plan": "URL",
      "slides": "URL"
    },
    "created_date": "2026-03-13",
    "tier": "T4",
    "customer_net_cost": 325000,
    "status": "draft"
  },
  "initiatives_discovered": [
    {"name": "AI Transformation", "status": "active", "priority": "P0"}
  ],
  "architecture_snapshot": {
    "current_stack": ["Snowflake", "Spark on EMR", "Databricks SQL"],
    "target_stack": ["Databricks Lakehouse", "Mosaic AI", "Unity Catalog"],
    "migration_path": "Snowflake → Databricks Lakehouse"
  },
  "stakeholders_identified": [
    {"name": "Jane Smith", "title": "CTO", "role_type": "champion"},
    {"name": "Bob Jones", "title": "VP Data", "role_type": "sponsor"}
  ],
  "competitors_identified": [
    {"name": "Snowflake", "products": ["Cortex", "Snowpark"], "displacement_status": "evaluating"}
  ],
  "signals": {
    "sfdc": ["has_ai_ucos", "multiple_teams"],
    "architecture": ["snowflake_present"],
    "strategic": ["ai_transformation_stated", "cto_champion"]
  }
}
```

This enables future proposals for the same account (or similar accounts) to start from a richer baseline.

---

## Step 16: Return All Links

```
═══════════════════════════════════════════════════
   AI COE GTM COPILOT — PROPOSAL PACKAGE READY
═══════════════════════════════════════════════════

Account: [ACCOUNT]
GTM Play: [PRIMARY_PLAY] + [SECONDARY if applicable]

1. Golden Path to Enterprise AI
   [URL — Google Doc]
   [N] workstreams, [N] council insights, [PLAY]-aligned narrative
   Enriched by: Market Analyst, Strategy Partner, Field CTO, AI Architect

2. AI COE SOW Draft
   [URL — Google Doc]
   [N]-week / [N] person-day engagement
   Investment: $[customer net] (after $[co-invest] Databricks co-investment)
   Enriched by: Delivery COO, Economist, Resource Planner

3. Project Plan & Gantt
   [URL — Google Sheets]
   [N] tasks, [N] parallel tracks, [N] milestones
   Accelerators deployed: [N] from PathToProduction

4. Executive Slide Deck
   [URL — Google Slides]
   [N] slides — council-enriched Priorities→Outcomes, [N] appendix tables
   Enriched by: All 10 council experts

5. Architecture Diagrams
   Current/Future State: [URL — Google Slides] (2 slides)
   Use-Case Architecture: [URL — Google Slides] (1 slide)
   Thumbnails: /tmp/coe_ACCOUNT/arch_diagrams/, /tmp/coe_ACCOUNT/usecase_arch/

Intelligence sources:
  Drive: [N docs]  |  Slack: [N threads]  |  Gmail: [N emails]
  Calendar: [N meetings]  |  SFDC: [N UCOs, N ASQs, N blockers]
  Logfood: $[X] annual, Tier [X]  |  Graph: [status]
  Vector Search: [N similar proposals]  |  Accelerators: [N matches]
  Competitive: [competitors]  |  Play Detection: [plays activated]

Memory Graph: Updated with new proposal, signals, and architecture snapshot.

Quick tips:
- All assets in My Drive — share after review
- SOW: legal review required before external sharing
- Golden Path + Slides: shareable with customer champion
- Project Plan: share with customer PM for joint planning
- Internal pricing at /tmp/coe_ACCOUNT/em_pricing.md

Optional: /exec-messaging-coach for CTO/CFO talking points
═══════════════════════════════════════════════════
```

---

## Positioning & Voice — CRITICAL

### Core Framing: Outcome-Based Partnership Model

The AI COE is an **outcome-based partnership** where Databricks embeds alongside the customer's teams to deliver **proven, measurable AI success in 60 days** and then **partners on the annual roadmap**.

**Every output must answer:**
1. **Why this matters** — Customer-specific business impact
2. **Why now** — Market timing + competitive urgency (from Market Analyst)
3. **Why Databricks** — Platform differentiation (from play definition + battlecard)
4. **How we deliver** — Concrete plan with named roles and accelerators (from councils)

### Narrative Principles

From the instruction documents:
- **9-section story arc** (Primary): Problem → Shift → Architecture → Program → MVP → Framework → Model → Why This Wins → Pitch
- **4 CoE focus areas** (Secondary): Blueprint, Operations, Acceleration, Enablement
- **Maturity model** (Secondary): Establish → Scale → Autonomy
- **Anti-patterns** (Tertiary): No pre-tech-win selling, no governance police, no generic decks, no tool-only stories

### What Lands

- "One domain, one data product, 60 days — prove the pattern, replicate at scale"
- Customer OKRs mapped to concrete 60-day deliverables
- People + Process + AI Tools framework
- ROI framing with payback period
- Customer's own language for themes and priorities
- Named stakeholders, teams, specific metrics
- "$X net cost (after $Y Databricks co-investment, Z%)" — skin in the game

### What Doesn't

- Leading with "lakehouse migration" or "data platform modernization"
- Generic capability maps without customer outcomes
- Technology-first positioning
- Vague timelines or "it depends" scoping
- Open-ended SOWs without exit criteria

### Tone

Consultative, specific, outcome-focused. First-person plural ("we/Databricks will"). No marketing fluff. Partnership, not vendor engagement. CTO level for themes, one level down for platform leaders.

---

## Quality Standards

**Golden Path:** 60-day outcomes are single-domain, specific, measurable. Official Databricks product names. Customer team naming conventions. Council intelligence woven into every section.

**SOW:** Objective → Activities → Deliverables per workstream. Active voice. Specific artifacts. Investment with ROI and co-invest.

**Project Plan:** Weekly-trackable tasks. Explicit dependencies. Clear milestone criteria. Parallel tracks maximize velocity. Accelerators named.

**Slide Deck:** Slide 3 uses customer theme names + council insights. Slide 9 uses customer OKR language. Slide 11 has named individuals and dates. Appendix includes new council-generated content.

---

## Reference Documents

| Document | ID | Purpose |
|---|---|---|
| Template3 AI COE (Slides) | 12jCXNxSrkWaZqsIGDSxulYaal3VuV62sHuKtAZUruGE | 19-slide deck template |
| AI COE Knowledge Base | 15bazLGL4t1FZkf0jQOgR-4KnNcg1WgxVWTLAQwoHfyE | Positioning framework |
| Riot Games Golden Path | 16Z-ZI0-yN0QoYiYw4T9GR9evzBgmT5lDtg8pw7ADl8g | Table structure reference |
| FanDuel SOW | 1vYULmy1QkH7P_Z1N3GxR_LkWgrTB-0OARtLd74Pb1so | SOW format reference |
| Live Template: Golden Path | 1ENG4we-VsofN-IXPgcFpaqydQekaCW4DyTgz8sE0xyI | Gold standard output |
| Live Template: SOW | 1N09DcQUMdjrm0HB5vb_46dTe8pBvGg5grHie599b0tk | Gold standard output |
| Live Template: Project Plan | 1FjwLQ1Nd8ogcBTJlwO180qrRPYIyaenNzYBonAktgJw | Gold standard output |
| Live Template: Slides | 1qMu1Acfhc7UqZftuoOYhzfMEVkXjq0WSGnUKxv7ZBQg | Gold standard output |
| Template Folder | 1LMvPxXNxjKYuG32jzbVC1__1yvNmo0Mw | All templates + instructions |

---

## Pre-Requisites

- **Google auth:** `/google-auth` (Docs, Slides, Sheets, Drive, Gmail, Calendar)
- **Salesforce auth:** `/salesforce-authentication` (UCOs, ASQs, Accounts)
- **Databricks auth:** `/databricks-authentication` with logfood profile
- **Slack MCP:** Optional but recommended
- **Glean MCP:** Optional

The skill gracefully degrades if any source is unavailable. Drive + logfood are minimum required.

**New infrastructure (optional, enhances quality):**
- **Lakebase Memory Graph:** Run `python3 memory_graph.py setup` to create tables
- **Vector Search:** Run `python3 vector_search_setup.py` to create indexes
- Without these, the system works using live research only. With them, proposals improve via cross-account learning.

---

## Invocation Examples

```
/ai-coe-proposal
→ Full GTM Copilot pipeline with play detection, dual councils, memory graph

/ai-coe-proposal
Account: FanDuel
Use cases: Racing Agent v2, Recommendation Engine, Multi-agent compliance
Teams: DS team (Mosaic AI trained), Data Engineering, Platform Governance
Situation: expansion
Context: Expanding existing COE. DS team already trained on Mosaic AI.

/ai-coe-proposal
Account: AT&T
Use cases: GenAI customer service agents, network anomaly detection, data quality at scale
Situation: renewal
Context: Major renewal Q2. FOTI available. Previous DSA ended last quarter.

/ai-coe-proposal
Account: Disney
Use cases: Content recommendation AI, streaming analytics, ad yield optimization
Teams: Streaming Tech, Ad Sales Analytics, ML Platform
Situation: new
Context: CTO wants unified AI platform. Currently Snowflake + separate ML infra.
```
