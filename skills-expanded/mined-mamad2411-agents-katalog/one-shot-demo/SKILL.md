---
name: one-shot-demo
description: "Creates production-grade Databricks demos end-to-end in a single shot. Use when building customer demos, POCs, or showcase applications. Triggers on 'build a demo', 'create a Databricks demo', 'demo for [customer]', 'one-shot demo', 'POC application'."
---

# One-Shot Demo

> **Version 1.2.0** | 2026-03-11 | Phase 10 data grounding, SP permissions for all endpoint types, security fixes (user_email scoping), value formatting standards, follow-up chip styling. Version 1.1: 2026-03-02. Version 1.0: 2026-02-24

Expert guidance for creating production-grade Databricks demos that follow enterprise best practices. Orchestrates the complete demo creation workflow from customer research through deployment.

## Capabilities

- **Customer-aligned story planning** with realistic business context
- **Automated brand extraction** — scrapes customer's website for colors, logo, fonts (free, no API keys)
- **Automated resource creation** via AI Dev Kit MCP tools
- **Multi-persona appeal** (Executive, Analyst, Technical)
- **Production-grade UI/UX** standards
- **Deterministic data generation** matching story metrics exactly
- **Databricks Asset Bundle** packaging for reproducibility
- **Agent Bricks automation** (Knowledge Assistant, Genie Space, Multi-Agent Supervisor)

## Core Principles

1. **AI Dev Kit is MANDATORY** — Primary tool for all Databricks work
2. **MCP tools first** — Execute operations programmatically, never manually
3. **Story-driven** — Every element reinforces a curated business narrative
4. **Automate everything** — Data generation, Agent Bricks, dashboards, deployment
5. **Native Databricks** — Use platform capabilities before external tools
6. **Bundle everything** — Reproducible with single `databricks bundle deploy`

## Workflow Execution Protocol

**MANDATORY: On skill invocation, IMMEDIATELY create a task tracker:**

```
TaskCreate: "Phase 0: Pre-flight verification"    (activeForm: "Verifying MCP tools")
TaskCreate: "Phase 1: Customer research"           (activeForm: "Researching customer")
TaskCreate: "Phase 2: Story planning"              (activeForm: "Planning demo story")
TaskCreate: "Phase 3: Story approval gate"         (activeForm: "Awaiting user approval")
TaskCreate: "Phase 4: App template selection"      (activeForm: "Selecting app template")
TaskCreate: "Phase 5: Data generation"             (activeForm: "Generating data")
TaskCreate: "Phase 6: User identity & Lakebase"    (activeForm: "Configuring user identity")
TaskCreate: "Phase 7: Resource creation & deploy"   (activeForm: "Creating resources")
TaskCreate: "Phase 8: Asset Bundle packaging"      (activeForm: "Packaging Asset Bundle")
TaskCreate: "Phase 9: Post-deploy verification"    (activeForm: "Testing every feature")
TaskCreate: "Phase 10: Data grounding & handover"  (activeForm: "Verifying data integrity")
```

**Rules:**
- Mark each task `in_progress` BEFORE starting it
- Mark each task `completed` ONLY when fully done
- NEVER skip a task or work on a later task while an earlier one is pending

---

### Phase 0: Pre-Flight Verification (CRITICAL — BLOCKING)

**MANDATORY: Complete ALL steps before ANY demo work.**

#### Step 0: Confirm Target Workspace (MUST DO FIRST)

The MCP tools connect to a **default workspace** which may NOT be the intended one. This has caused deployments to the wrong workspace.

**Actions:**
1. Run `get_current_user()` and `execute_sql("SELECT current_catalog()")` to identify the connected workspace
2. Check the host URL returned in MCP tool responses
3. **ASK the user explicitly:**

```
AskUserQuestion:
  "Which Databricks workspace should this demo be deployed to?"
  Options:
    - The workspace MCP tools are currently connected to: {detected_host}
    - A different workspace (specify profile name)
```

4. If the user wants a **different workspace**: tell them to update their default Databricks profile and restart Claude Code. **DO NOT proceed** until confirmed.
5. If confirmed correct, proceed to Step 1.

#### Step 1: Verify MCP Tools Available

```
ToolSearch query="databricks"
```

**If tools found** (`mcp__plugin_databricks-ai-dev-kit_databricks__*`):
- Verify connectivity: `execute_sql("SELECT 1 as test")`
- If succeeds, proceed to Step 2

**If NO tools found:** HARD STOP. The `databricks-ai-dev-kit` plugin is required. Tell the user to install it from the fe-vibe marketplace and restart Claude Code. DO NOT proceed with CLI workarounds.

#### MCP Tools Discipline (APPLIES TO ENTIRE SESSION — NOT JUST PHASE 0)

> **CRITICAL: This rule applies from Phase 0 through Phase 9 and beyond. In long sessions,
> there is a pattern of silently drifting to CLI commands. Undocumented drift to CLI MUST NOT happen.**

**Before EVERY Databricks operation, ask yourself: "Can an MCP tool do this?"**

| Operation | MCP Tool (USE THIS) | CLI Fallback (ONLY if MCP fails) |
|-----------|--------------------|---------------------------------|
| Run SQL | `execute_sql()` | `databricks sql` |
| Upload files | `upload_file()` / `upload_folder()` | `databricks workspace import` |
| Deploy app | `deploy_app()` | `databricks apps deploy` |
| Get app status | `get_app()` | `databricks apps get` |
| Create Lakebase | `create_or_update_lakebase_database()` | N/A |
| Generate Lakebase cred | `generate_lakebase_credential()` | N/A |
| List volume files | `list_volume_files()` | `databricks volumes list` |
| Run Python | `run_python_file_on_databricks()` | N/A |

**If you catch yourself typing `databricks` in a Bash command**: STOP. Check the table above. Only proceed with CLI if the MCP tool genuinely failed (timeout, connection error) — and LOG why you fell back so the user knows.

#### Step 2: Load Required Skills

Load the following skills. Names come from the `databricks-ai-dev-kit` plugin and `fe-databricks-tools` — if a skill name is not found, search for the closest match (e.g., search "synthetic data" or "agent bricks") and use whatever the current skill name is.

```
Skill skill="databricks-apps"
Skill skill="databricks-lakeview-dashboard"
Skill skill="databricks-authentication"
Skill skill="databricks-synthetic-data-generation"
Skill skill="databricks-agent-bricks"
```

#### Step 3: Confirm Automated Capabilities

- MCP tools loaded and verified
- Synthetic data generation via MCP tools + `dbldatagen`
- Agent Bricks automation (KA, Genie, MAS) via MCP tools
- Dashboard creation programmatically via MCP tools
- All deployable via Asset Bundles

---
**GATE: Phase 0 → Phase 1** — User confirmed target workspace AND `execute_sql("SELECT 1")` succeeded. Mark Phase 0 `completed`, Phase 1 `in_progress`.

---

### Phase 1: Customer Research

**Input Required**: Customer name

**Actions**:
1. Research thoroughly: industry, size, revenue, key business lines, recent news, tech stack
2. Use web search for current information (include current year in searches)
3. If company name is ambiguous, verify with user BEFORE proceeding
4. All story elements must reflect the company's ACTUAL business reality

**Output**: Customer context document for story planning

---
**GATE: Phase 1 → Phase 2** — Share research summary with user
---

### Phase 2: Story Planning (MANDATORY — Must Get Approval Before Code)

> **Load now:** [story-template.md](references/story-template.md), [agent-bricks-decision-tree.md](references/agent-bricks-decision-tree.md)

**CRITICAL**: Present full story plan and receive explicit approval BEFORE any code, data, or assets.

**Use the story structure template from** [story-template.md](references/story-template.md). The story must include:

- Summary, company context, key metrics, baseline behavior
- Event to capture with timeline following company's fiscal calendar
- Narrative business story with step-by-step walkthrough
- 15-minute demo flow (4 acts + closing)
- Validation questions (max 6, answerable with demo data)
- Transformations (Bronze/Silver/Gold — one-line descriptions ONLY)
- Agent Bricks architecture (follow the decision logic below)

**Agent Bricks Decision Logic (MANDATORY):**

```
Unstructured data (PDFs, docs)? → CREATE Knowledge Assistant (KA)
Structured data queries (SQL)?  → CREATE Genie Space
Using 2+ agents?                → CREATE Multi-Agent Supervisor (MAS)
```

See [agent-bricks-decision-tree.md](references/agent-bricks-decision-tree.md) for full details including all 5 MAS agent types.

**Story Rules**: No @ symbols in headers. Transformations = one-line only. Questions max 6. Agent Bricks before Foundation Model Serving.

---
**GATE: Phase 2 → Phase 3** — Present complete story plan to user. STOP and WAIT.
---

### Phase 3: User Validation (GATE — NO PROCEEDING WITHOUT APPROVAL)

**STOP HERE**: Wait for explicit user approval of story plan.

- If approved ("looks good", "go ahead") → Proceed to Phase 4
- If changes requested → Revise, re-present, and WAIT again
- Do NOT generate data or create assets until approved

---
**GATE: Phase 3 → Phase 4** — User has explicitly approved the story
---

### Phase 4: App Template Selection & Branding

> **Load now:** [app-design-philosophy.md](references/app-design-philosophy.md), [app-design-checklist.md](references/app-design-checklist.md), [brand-extraction.md](references/brand-extraction.md)

1. **Extract customer branding** (AUTOMATIC — no user action needed):
   - Follow [brand-extraction.md](references/brand-extraction.md) to extract brand colors, logo, and fonts
   - **Logo (CRITICAL — NEVER skip, NEVER hand-draw)**:
     - **PRIMARY method**: Screenshot the customer's actual website header, crop just the logo, scale 3x for retina, save to `frontend/public/customer-logo.png`
     - **Fallback**: Search for `"{company} logo transparent png"` and download from logo databases
     - Display with `<img src="/customer-logo.png" style={{ mixBlendMode: 'lighten' }}>` in Layout.tsx
     - NEVER hand-draw SVG logos, NEVER base64-encode into source files, NEVER use text-only placeholders
   - **Colors**: Derive ALL `${COLOR_*}` placeholder values using the brand-tinting formula in `brand-extraction.md` (backgrounds, cards, borders must be visibly tinted with the brand color — NOT generic dark)
   - Apply via `setup.sh` or direct replacement — every color in the app should echo the customer's brand
   - **Audit ALL components for hardcoded hex colors**: Run `grep -rn '#[0-9a-fA-F]\{6\}' frontend/src/` and replace any generic colors with brand-tinted equivalents. This includes FloatingAssistant, KPICard, Dashboard, modals — every `.tsx` file, not just `index.css`
2. **Ask**: "Do you have an existing reference app to use as a base, or an existing deployed app to revamp? If so, provide the path." (If revamping, follow the **Revamp/Upgrade Flow** below instead of steps 4-7.)
3. **If existing app to revamp**: Follow the **Revamp/Upgrade Flow** below
4. **If reference app provided**: Validate directory, check for valid app structure
5. **If none — use the starter template**: Copy [templates/app/](templates/app/) as the base. It includes a floating AI chat widget (FloatingAssistant.tsx with multi-chat isolation), Lakebase pool, MAS integration, routing animation, and 2 pages + floating chat (Dashboard, Architecture, FloatingAssistant overlay). Follow [CUSTOMIZE.md](templates/app/CUSTOMIZE.md) to replace `${PLACEHOLDER}` variables with your demo values.
6. **Alternative — build from APX scaffold**: Load the `databricks-app-apx` skill for a fresh FastAPI + React template. Follow [app-design-philosophy.md](references/app-design-philosophy.md) for UX standards.
7. **Customization**: Apply extracted brand (colors, logo, fonts), swap MAS endpoint, dashboard/Genie IDs, workspace host, Lakebase connection, schema name, SQL queries. Rebuild and deploy.

#### Revamp/Upgrade Flow (Existing Apps)

> **When the user says "revamp", "upgrade", "fill in gaps", or "bring up to standard" for an existing app,
> this flow applies INSTEAD of building from scratch. The compliance checklist below is STILL MANDATORY.**

1. **Read the existing app structure** — understand what's already built (components, routes, backend)
2. **Read ALL reference files** — even if you think you know the patterns:
   - `templates/app/frontend/src/components/FloatingAssistant.tsx` (canonical chat pattern)
   - `templates/app/CUSTOMIZE.md` (placeholder reference + chat architecture rules)
   - `references/brand-extraction.md` (logo + color rules)
   - `references/app-design-checklist.md` (full UI/UX checklist)
   - `references/patterns-ui-frontend.md` (design system + gotchas)
   - `references/patterns-mas-chat.md` (MAS integration patterns)
3. **Run the Pre-Code Compliance Checklist** below against the existing app
4. **Present gap analysis** to user with specific items that don't match the framework
5. **Fix all gaps** — using the template components as reference, not from memory

#### Pre-Code Compliance Checklist (MANDATORY — Run Before Writing ANY Code)

> **This checklist MUST be completed before writing or modifying any code — whether building
> from scratch, revamping an existing app, or "just filling in gaps". NEVER skip this.
> The #1 cause of framework violations is skipping this step and coding from memory.**

Read each reference file and verify the app matches. For each item, mark PASS or FAIL:

**Chat Architecture** (source: CUSTOMIZE.md "Chat Architecture: Floating Widget"):
- [ ] Chat is a **floating assistant overlay** (fixed bottom-6 right-6), NOT a page/tab in nav
- [ ] FloatingAssistant uses pill button that expands on hover with "Ask Assistant" text
- [ ] Panel is fixed-size (~420x600px), NOT full-height drawer or full-page
- [ ] 6 suggestion chips visible on empty state as rounded pills
- [ ] Chips are story-aligned business questions (not technical/generic)
- [ ] Chat/History toggle within the same panel (not separate sidebar)

**Branding** (source: brand-extraction.md, patterns-ui-frontend.md §1b):
- [ ] Logo is a **real downloaded image** (PNG from customer website), NOT hand-drawn SVG
- [ ] Logo file exists at `frontend/public/customer-logo.png` (or equivalent)
- [ ] Theme colors are **brand-tinted** (derived from brand primary), NOT generic dark
- [ ] No hardcoded generic hex colors in components (`grep -rn '#[0-9a-fA-F]{6}' frontend/src/`)

**Routing Animation** (source: app-design-checklist.md, patterns-mas-chat.md §4):
- [ ] Loading state shows stepper with **live elapsed timer** (not static spinner)
- [ ] Stepper shows **agent names** from actual route (Supervisor → Genie Space, etc.)
- [ ] Dynamic status text updates (analyzing → routing → executing)

**AI Response Format** (source: app-design-philosophy.md, app-design-checklist.md):
- [ ] Responses are **narrative summaries** (not raw SQL tables, JSON, or document excerpts)
- [ ] 4-part structure: summary + supporting data + insights + suggested next question

**Navigation & Layout** (source: app-design-philosophy.md):
- [ ] Nav follows **business narrative** (Portfolio → Detail → Architecture), not technical categories
- [ ] User email displayed in sidebar (from `/api/me`)
- [ ] Loading skeletons on all data-fetching pages

**Workspace Hygiene** (source: gotcha #16):
- [ ] No `node_modules/`, `.venv/`, `__pycache__/` in workspace deploy path
- [ ] Only `frontend/dist/`, `server/`, config files uploaded

**If ANY item is FAIL**: Fix it BEFORE proceeding to write other code. Do NOT defer to "later".

---
**GATE: Phase 4 → Phase 5**
- CONDITION: User confirmed template approach AND branding applied AND Pre-Code Compliance Checklist all PASS
- VERIFY: `frontend/public/customer-logo.png` exists (real logo, NOT hand-drawn), theme colors are brand-tinted (NOT generic), chat is floating overlay with suggestion chips, no workspace bloat
- IF ANY CHECKLIST ITEM FAILS: STOP — fix it before proceeding
---

### Phase 5: Deterministic Data Generation

> **Load now:** Use `databricks-synthetic-data-generation` skill (loaded in Phase 0)

**MANDATORY: Use the synthetic data generation skill from `databricks-ai-dev-kit` — NEVER write custom data generation code.**

```
Skill skill="databricks-synthetic-data-generation"
```

**Data Requirements**:
- MUST match story metrics EXACTLY
- Deterministic and reproducible (fixed seeds)
- Realistic distributions (log-normal, exponential — NOT uniform)
- Realistic temporal patterns (weekday/weekend, holidays, seasonality)
- Referential integrity (master tables first, then foreign keys)
- Quality over quantity (10K-50K rows minimum)
- Include unstructured documents (policy docs, reports) for KA

**Medallion Architecture (MANDATORY — All 3 Layers Required)**:

All demos MUST create Bronze, Silver, AND Gold tables. Silver tables are NOT optional — they are the cleansing/enrichment layer that makes the Architecture page's medallion diagram truthful.

| Layer | Purpose | Pattern |
|-------|---------|---------|
| **Bronze** | Raw ingested data | Direct from source systems, minimal transformation |
| **Silver** | Cleansed & conformed | Joins across bronze tables, deduplication, type casting, enrichment with reference data, unified models (e.g., linear + digital delivery), variance flags |
| **Gold** | Business-level aggregates | KPIs, scores, summaries ready for dashboard consumption |

**Silver table patterns** (use as many as applicable):
- **Enriched joins**: Bronze fact table + bronze dimension table → add tier, region, AE, industry
- **Unified models**: Multiple bronze sources with different schemas → single conformed table (e.g., linear TV logs + digital delivery → `silver_delivery_unified`)
- **Reconciliation**: Match two bronze sources, compute variance, flag discrepancies
- **Scored/classified**: Add computed metrics like sentiment scores, variance flags, risk categories

**Execution**: Create Python script → Execute via `run_python_file_on_databricks` → Verify via SQL queries → Upload unstructured docs to UC volumes. NEVER ask user to run manually.

---
**GATE: Phase 5 → Phase 6** — All story metrics calculable from generated data AND all 3 medallion layers (bronze_*, silver_*, gold_*) exist as UC tables
---

### Phase 6: User Identity & Lakebase Configuration

> **Load now:** [patterns-auth-lakebase.md](references/patterns-auth-lakebase.md), [patterns-mas-chat.md](references/patterns-mas-chat.md)

> **User email display is MANDATORY for ALL demos — with or without chat.**
> Customers need to see that the app knows who they are. This is table-stakes for any enterprise demo.
>
> - **All apps**: Display user email (bottom-left sidebar) + `/api/me` endpoint
> - **Apps with AI/chat**: ALSO configure Lakebase for chat persistence (conversations + messages tables scoped to user)

#### Step 1: User Identity (ALL APPS — No Exceptions)

Every Databricks App gets the user's identity from proxy headers for free. Use it.

**Backend** — `/api/me` endpoint:
```python
@router.get("/me")
async def me(request: Request):
    email = (request.headers.get("X-Forwarded-Email")
            or request.headers.get("X-Forwarded-Preferred-Username")
            or request.headers.get("X-Forwarded-User")
            or "anonymous")
    return {"email": email}
```

**Frontend** — call on mount, display bottom-left of sidebar:
```typescript
useEffect(() => {
  fetch('/api/me').then(r => r.json()).then(d => setUserEmail(d.email));
}, []);
// In sidebar, bottom-left:
<span className="text-xs text-muted">{userEmail}</span>
```

**Why this matters**: Customers see their own email in the app → "this is a real enterprise app with SSO, not a toy". It's the single easiest trust signal.

> **If the app has NO chat/AI feature, Phase 6 is DONE after this step.** Mark Phase 6 `completed` and proceed to Phase 7.
> **If the app HAS chat/AI**: continue to Step 2 below.

---

#### Step 2: Create Lakebase Instance (Chat Apps Only)

```
create_or_update_lakebase_database(name="{demo_name}-chat", capacity=1)
```

Grant `CAN_USE` to `users` group on the database instance.

#### Step 3: Create Chat Schema and Tables

Via `execute_sql` (using the Lakebase connection):

```sql
CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY,
  user_email TEXT NOT NULL,
  title TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  route TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id, created_at);
CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_email, updated_at DESC);
```

**CRITICAL: `user_email` column is MANDATORY** — conversations must be scoped to the logged-in user.

#### Step 4: User-Token Auth Middleware

**DO NOT use `generate_database_credential()` for Databricks Apps** — the SP's token lacks Lakebase security labels. Instead, capture the USER's forwarded OAuth token from the Databricks Apps proxy:

```python
# In app.py — middleware captures x-forwarded-access-token on every request
class LakebaseTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        email = (request.headers.get("X-Forwarded-Email")
                or request.headers.get("X-Forwarded-Preferred-Username"))
        token = request.headers.get("x-forwarded-access-token")
        if email and token:
            pool.update_token(token)  # ALWAYS update token FIRST (tokens expire hourly)
            if not pool.available:
                pool.capture_user_token(email, token)
                await pool.init()
        return await call_next(request)
```

> **CRITICAL**: `update_token()` MUST be called BEFORE checking `pool.available`, not in an else branch. The old pattern (`if not available: init; else: update_token`) silently uses stale tokens — the pool stays "available" but all queries fail after ~1 hour when the OAuth token expires.

#### Step 5: Conversation CRUD API

Create these endpoints — all scoped to the authenticated user:
- `GET /api/conversations` — list conversations for current user
- `POST /api/conversations` — create new conversation
- `GET /api/conversations/{id}/messages` — get messages for a conversation
- `POST /api/conversations/{id}/messages` — save a message
- `DELETE /api/conversations/{id}` — delete a conversation

Conversations MUST be filtered by `user_email` in all queries.

#### Step 6: Verify Lakebase End-to-End

After deploying:
1. Hit `/api/health` — verify `pool_available: true`
2. Hit `/api/me` — verify user email is returned (not "anonymous")
3. Send a chat message → verify it appears in the `messages` table
4. Reload page → verify conversations persist

See [patterns-auth-lakebase.md](references/patterns-auth-lakebase.md) for full code patterns.
See [patterns-mas-chat.md](references/patterns-mas-chat.md) for multi-chat isolation patterns (FloatingAssistant ref-based or full-page stateMap).

---
**GATE: Phase 6 → Phase 7** — User email displayed in app (ALL demos). For chat apps: health=ok, Lakebase pool available, messages persisting, conversations survive reload
---

### Phase 7: Resource Creation & Deploy (All Automated via MCP Tools)

> **Load now:** [patterns-mas-chat.md](references/patterns-mas-chat.md), [patterns-ui-frontend.md](references/patterns-ui-frontend.md)

**Phase 7 has 4 mandatory sub-steps. Complete them IN ORDER and check each off before moving on.**

#### Step 1: Agent Bricks (KA / Genie / MAS)

Create Agent Bricks per the story plan (Phase 2). Use MCP tools (`manage_ka`, `create_or_update_genie`, `manage_mas`).
- [ ] Knowledge Assistant created and endpoint ONLINE
- [ ] Genie Space created with gold tables and sample questions
- [ ] Multi-Agent Supervisor created, routing tested
- [ ] Test each agent with a sample question from the story

#### Step 2: AI/BI Lakeview Dashboard (MANDATORY — DO NOT SKIP)

> **This step gets skipped most often.** Dashboard creation is NOT optional — it's the Analyst persona's
> primary experience and proves the gold layer works end-to-end in native Databricks.

Create a Lakeview dashboard programmatically using the `databricks-lakeview-dashboard` skill:

1. **Design**: 2 pages — Executive Overview (KPI counters + charts) and Detail (tables + drill-downs)
2. **Datasets**: One per gold table, all querying `{catalog}.{schema}.gold_*`
3. **Widgets**: KPI counters for headline metrics, bar/pie/line charts for breakdowns, table for detail
4. **Deploy**: `databricks api post /api/2.0/lakeview/dashboards` with `serialized_dashboard` JSON string
5. **Publish**: `databricks api post /api/2.0/lakeview/dashboards/{id}/published`
6. **Verify**: Open dashboard URL, confirm all widgets render with data

**Checkpoint**: Dashboard URL exists and all widgets show data. If not — fix before proceeding.

#### Step 3: App Deploy + MAS Integration

**MAS Integration**: MAS endpoints use `{"input": messages}`, NOT `{"messages": messages}`. Use async polling (NOT SSE — Databricks Apps proxy buffers streaming). Use ref-based multi-chat isolation (NOT AbortController). See [patterns-mas-chat.md](references/patterns-mas-chat.md) for complete code patterns.

**Routing Animation (MANDATORY)**: Every chat loading state MUST show a stepper with: elapsed time counter, agent routing path with names (Supervisor → Genie Space, etc.), and dynamic status text. Users wait 10-30s+ — without this they assume the app is broken. See [patterns-mas-chat.md](references/patterns-mas-chat.md) Section 4.

**Human-Readable Synthesis (MANDATORY)**: ALL chat responses — single agent or MAS — MUST be formatted, narrative summaries. Raw SQL tables, document excerpts, or JSON are NEVER acceptable. If a single agent can't produce readable output, either configure its instructions or wrap in MAS for synthesis. See [patterns-mas-chat.md](references/patterns-mas-chat.md) Section 5.

#### Step 4: Service Principal Permissions (CRITICAL — After First Deploy)

`app.yaml` resources grant SP access to serving endpoints and SQL warehouses only. Unity Catalog permissions require **explicit SQL GRANTs**. Without them, all SQL queries return empty results silently.

**After `databricks apps deploy`:**
1. Get SP client ID: `databricks apps get {app-name} | jq -r '.service_principal.client_id'`
2. Grant UC permissions via `execute_sql`:
   ```sql
   GRANT USE CATALOG ON CATALOG {catalog} TO `{sp_client_id}`;
   GRANT USE SCHEMA ON SCHEMA {catalog}.{schema} TO `{sp_client_id}`;
   GRANT SELECT ON SCHEMA {catalog}.{schema} TO `{sp_client_id}`;
   ```
3. No redeploy needed — GRANTs take effect immediately.

See [patterns-auth-lakebase.md](references/patterns-auth-lakebase.md) for full auth, Lakebase, and SP patterns.

---
**GATE: Phase 7 → Phase 8** — ALL 4 sub-steps verified:
- [ ] Agent Bricks (KA + Genie + MAS) created, endpoints ONLINE, tested with sample questions
- [ ] Lakeview Dashboard deployed, published, URL confirmed, all widgets rendering data
- [ ] App deployed, chat working (MAS responds, routing animation, conversation persistence)
- [ ] SP permissions granted (USE CATALOG, USE SCHEMA, SELECT)
---

### Phase 8: Asset Bundle Packaging (MANDATORY)

> **Load now:** [asset-bundle-guide.md](references/asset-bundle-guide.md)

Every demo MUST be a Databricks Asset Bundle. See [asset-bundle-guide.md](references/asset-bundle-guide.md) for full structure, databricks.yml template, deployment workflow, and static asset handling.

**Key requirements**: Parameterize everything, include all resources, environment targets (dev/prod), README with deployment instructions, `.gitignore` that does NOT exclude images.

---
**GATE: Phase 8 → Phase 9** — `databricks bundle validate` passes
---

### Phase 9: Post-Deploy Verification (MANDATORY)

> **Load now:** [validation-and-grading.md](references/validation-and-grading.md)

> **CRITICAL: This is the phase that gets skipped and causes demo failures.** Do NOT declare the demo
> complete until EVERY item below passes. Use Chrome DevTools MCP or the web-devloop-tester agent
> to test the live app. NEVER assume "it should work" — VERIFY.

#### Step 1: App Health

- [ ] App status is `SUCCEEDED` and `ACTIVE`
- [ ] `/api/health` returns `status: ok` and `pool_available: true`
- [ ] `/api/me` returns the logged-in user's email (not "anonymous")

#### Step 2: Every Tab/Page Works

Navigate to EVERY page/tab in the app and verify:
- [ ] **Dashboard page** — loads, charts render, data is visible
- [ ] **Data/Articles page** — table loads, rows visible, filters work
- [ ] **Floating AI chat** — pill button visible at bottom-right, opens to chat panel, suggestions visible, input enabled
- [ ] **Architecture page** — content renders (if applicable)
- [ ] **Navigation** — every sidebar link works, active state highlights correctly
- [ ] **User email** — displayed in sidebar/header on every page

#### Step 3: Chat Functionality (Most Bug-Prone — Test Thoroughly)

- [ ] Send a message → routing animation shows stepper with elapsed timer AND agent names
- [ ] Animation shows dynamic status text (analyzing → routing to [Agent Name] → executing)
- [ ] Response arrives → route badge shows (Supervisor → Agent), content renders as markdown
- [ ] Response is a human-readable synthesis (narrative summary + supporting data + insights)
- [ ] Response is NOT raw SQL tables, JSON, or unformatted document excerpts
- [ ] **Follow-up suggestion chip appears** below the response (visually distinct from user bubbles)
- [ ] Follow-up chip is clickable and sends the question
- [ ] No "Suggested follow-up:" text appears inline in the response body (stripped when chip shown)
- [ ] Send message in Conv A → switch to new Conv B while A is loading
- [ ] Conv B shows clean empty state (no animation bleed from A)
- [ ] Switch back to Conv A → user's question is still there
- [ ] Conv A → response arrived (or animation still running with correct elapsed time)
- [ ] Reload page → conversations persist in sidebar
- [ ] Click a persisted conversation → messages reload from Lakebase
- [ ] Delete a conversation → removed from sidebar and Lakebase
- [ ] Check console → zero JavaScript errors throughout all of the above

#### Step 4: Lakebase Data Integrity

- [ ] Query `conversations` table → rows exist with correct `user_email`
- [ ] Query `messages` table → user and assistant messages saved with correct `conversation_id`
- [ ] Messages have `route` field populated for assistant messages

#### Step 5: Multi-Persona Appeal

Verify demo provides value to 3+ personas:
- [ ] **Executive**: Business impact, KPIs, insights visible
- [ ] **Analyst**: Dashboards, SQL, Genie capabilities working
- [ ] **Technical**: Pipeline details, architecture, transformations accessible

#### Step 6: Edge Cases

- [ ] Send two questions rapidly in different conversations → both return correctly
- [ ] Very long response → renders without layout breakage
- [ ] Network interruption during poll → graceful error message (not stuck loading)

---
**GATE: Phase 9 → Phase 10** — ALL checkboxes above pass. Mark Phase 9 `completed`.
---

### Phase 10: Data Grounding & Handover Verification (MANDATORY — NEVER SKIP)

> **This phase treats the demo as a production prototype that a customer could deploy in their own
> environment. Every number, chart, KPI, and AI response MUST be traceable to the data we generated.
> Nothing fabricated. Nothing hardcoded. This phase CANNOT be skipped, abbreviated, or deferred.**

#### Why This Phase Exists

Every demo that skipped this phase had the same failure mode: customer opens the app, clicks a different tab,
sees a number that doesn't match the dashboard, asks "where does this come from?", and the AE has no answer.
The demo loses credibility instantly. This phase prevents that.

#### Step 1: Data Grounding Audit (Every Number Must Trace to SQL)

**For EVERY page in the app, systematically verify:**

1. **Take a snapshot** of the page (Chrome DevTools MCP or screenshot)
2. **List every visible number** — KPIs, chart values, table cells, percentages, counts
3. **For each number, run the backing SQL query** via `execute_sql` against the same catalog/schema
4. **Compare**: Does the SQL result match what the UI shows?
5. **Flag mismatches** — any number that doesn't match is either:
   - A hardcoded fallback value that was never replaced with live data
   - A column alias mismatch between SQL and frontend
   - A formatting bug (e.g., `$102983K` instead of `$103.0M`)
   - A stale cache or wrong data source

**Specific checks per component type:**

| Component | What to Verify | How |
|-----------|---------------|-----|
| **KPI cards** | Value matches `SELECT SUM/COUNT/AVG` on gold table | Run the exact query the backend uses |
| **Bar/line/pie charts** | Each bar/slice value matches grouped query | Run `GROUP BY` query, compare each category |
| **Tables** | Row count, column values, sort order | Run `SELECT` with same filters, compare first 5 rows |
| **Percentages** | Numerator and denominator are correct | Verify formula: `delivered/booked * 100` etc. |
| **Alert banners** | Threshold logic matches data | Query the anomaly condition, verify it triggers |
| **Chat responses** | Numbers cited in AI responses match SQL | Ask the same question via Genie Space directly, compare |

#### Step 2: Hardcoded Value Scan (MANDATORY)

Run these grep scans against the frontend source. Every match is a potential fabrication:

```bash
# Find hardcoded dollar amounts
grep -rn '\$[0-9]' frontend/src/ --include='*.tsx' --include='*.ts'

# Find hardcoded percentages
grep -rn '[0-9]\{2,\}%' frontend/src/ --include='*.tsx' --include='*.ts'

# Find hardcoded counts/numbers in JSX (not in CSS/styling)
grep -rn 'value={[0-9]' frontend/src/ --include='*.tsx'

# Find "Powered by" or attribution text
grep -rn -i 'powered by' frontend/src/ --include='*.tsx' --include='*.ts'
```

**Acceptable hardcoded values**: CSS sizes, animation durations, grid columns, array indices.
**Unacceptable**: Any business metric, KPI, dollar amount, percentage, or count that should come from data.

**For each unacceptable match**: Replace with dynamic data from the API, or remove if it's a fallback that's no longer needed.

#### Step 3: Tooltip & Formatting Consistency (MANDATORY)

Hover over EVERY chart tooltip in the app and verify:

- [ ] Dollar values use tiered formatting: `>= $1M` → `$X.XM`, `>= $1K` → `$XK`, else `$X`
- [ ] Percentages show one decimal: `94.1%` not `94.1000%` or `94`
- [ ] Counts use locale formatting: `1,178` not `1178`
- [ ] No tooltip shows raw unformatted numbers like `$102983000`
- [ ] All pages use the SAME formatter (shared `lib/format.ts`, not per-page copies)

#### Step 4: Chart Empty States (MANDATORY)

For each chart/table component, temporarily break the data source (e.g., wrong endpoint) and verify:

- [ ] Charts show "No data available" placeholder — NOT empty white space with orphaned axis labels
- [ ] Tables show "No results" message — NOT an empty table with only headers
- [ ] KPI cards show a dash or "—" — NOT `$0` or `$NaN` or `undefined`

#### Step 5: SP Permissions Completeness (ALL Serving Endpoints — Not Just MAS)

Verify the app's service principal has ALL required permissions. **ANY model serving endpoint the app calls — whether it's an Agent Brick, a custom model, a provisioned throughput endpoint, or a pay-per-token Foundation Model — needs `CAN_QUERY` granted to the SP.**

- [ ] UC: `GRANT USE CATALOG`, `USE SCHEMA`, `SELECT` on the demo schema
- [ ] SQL Warehouse: `CAN_USE` (via `app.yaml` resources or manual grant)
- [ ] Lakebase: `CAN_CONNECT` (via manual grant — `app.yaml` database resources are unreliable)
- [ ] Genie Space: `CAN_RUN` (via permissions API, object type: `genie`)

**For EVERY serving endpoint the app uses, grant `CAN_QUERY`:**

| Endpoint Type | Example | Permission |
|---------------|---------|-----------|
| MAS (Supervisor Agent) | `versant-ad-sales-supervisor` | `CAN_QUERY` on `serving-endpoints` |
| KA (Knowledge Assistant) | `versant-ka-ad-sales-policies` | `CAN_QUERY` on `serving-endpoints` |
| Foundation Model (pay-per-token) | `databricks-claude-sonnet-4-5` | `CAN_QUERY` on `serving-endpoints` |
| Provisioned Throughput | `my-llama-3-pt` | `CAN_QUERY` on `serving-endpoints` |
| Custom Model Serving | `fraud-classifier-endpoint` | `CAN_QUERY` on `serving-endpoints` |
| External Model (e.g., OpenAI via gateway) | `openai-gpt4-gateway` | `CAN_QUERY` on `serving-endpoints` |

```bash
# Grant CAN_QUERY for each endpoint — repeat for EVERY endpoint the app calls
curl -X PUT "https://{host}/api/2.0/permissions/serving-endpoints/{endpoint_name}" \
  -H "Authorization: Bearer {token}" \
  -d '{"access_control_list": [{"service_principal_name": "{sp_client_id}", "permission_level": "CAN_QUERY"}]}'
```

**How to find all endpoints the app uses**: `grep -rn 'SERVING_ENDPOINT\|endpoint' app.yaml server/` — list every endpoint name referenced in env vars and code.

**Test**: Send a chat message that exercises BOTH KA and Genie agents. If either returns "data warehouse connection temporarily unavailable" or empty results, SP permissions are incomplete. Also test any direct Foundation Model calls (e.g., summarization, classification endpoints).

#### Step 6: Follow-Up Chip Consistency (MANDATORY for chat apps)

Send at least 3 different questions across different agent types and verify:

- [ ] Every response has a follow-up suggestion chip below it
- [ ] Chip text is clean (no `**asterisks**`, no quotes, no "Suggested follow-up:" prefix)
- [ ] Chip is visually distinct from user message bubbles (different bg, shape, has label/icon)
- [ ] Clicking the chip sends the question and produces a valid response
- [ ] The "Suggested follow-up:" text does NOT appear inline in the response body

**If any response lacks a chip**: Check backend `_extract_followups()` — the system message may not be reaching the agent, or the extraction regex isn't matching the agent's format.

#### Step 7: Present Mismatch Report & Get Approval

**After completing Steps 1-6, compile a report:**

```
## Data Grounding Report

### Verified (PASS)
- Dashboard KPI: Q2 Booked Revenue = $173.4M ✓ (matches SELECT SUM(booked_amount) FROM gold_deals)
- ...

### Mismatches Found (FAIL)
1. [Page] [Component]: Shows [X], SQL returns [Y]
   - Root cause: [explanation]
   - Proposed fix: [what you'll change]
2. ...

### Hardcoded Values Found
1. [File:Line]: [value] — [acceptable/needs fix]
2. ...
```

**STOP and present this report to the user.** Do NOT fix anything until the user reviews and approves the proposed fixes. The user may have context about why a value differs or may want a different fix.

#### Step 8: Fix All Approved Issues

After user approval:
1. Fix each mismatch in order
2. Rebuild frontend (`npm run build`)
3. Upload and redeploy
4. Re-verify ONLY the fixed items (not full re-run)

#### Step 9: Final Handover Summary

**After ALL mismatches are fixed and re-verified, present the handover:**

```
## Demo Complete — Handover Summary

### App
- URL: https://{app-name}-{id}.aws.databricksapps.com/
- Status: ACTIVE, all pages verified

### Data
- Catalog: {catalog}
- Schema: {catalog}.{schema}
- Tables: bronze_* (X tables), silver_* (Y tables), gold_* (Z tables)
- Row counts: [list key tables with counts]

### Agent Bricks
- Knowledge Assistant: {name} (tile_id: {id}, endpoint: ONLINE)
- Genie Space: {name} (space_id: {id})
- Multi-Agent Supervisor: {name} (tile_id: {id}, endpoint: ONLINE)

### Dashboard
- Lakeview Dashboard: {name}
- URL: https://{workspace}/sql/dashboards/{id}
- Published: Yes

### Lakebase
- Instance: {name}
- Tables: conversations, messages
- Chat persistence: Verified

### Asset Bundle
- Path: {local path}
- Status: `databricks bundle validate` passes

All data is grounded. No hardcoded values. Ready for customer handover.
```

**This is the ONLY acceptable way to end a demo build.** Never say "done" without this summary.

---
#### Step 10: Demo Quality Grade (MANDATORY — Run AFTER Steps 1-9)

After ALL Phase 9 and Phase 10 checks pass, run the quality grade from [validation-and-grading.md](references/validation-and-grading.md).

**Grading inputs** (use results from Phase 9 + Phase 10):
- Phase 9 checklist results (app health, every tab, chat functionality, Lakebase, multi-persona, edge cases)
- Phase 10 data grounding report (mismatches found, hardcoded values, formatting, empty states, SP perms, follow-ups)

**Present the grade to the user as part of the handover summary:**

```
## Demo Quality Grade: [A/B/C/F]

### Phase 9 Results
- App health: PASS/FAIL
- All tabs working: X/Y passed
- Chat functionality: X/Y passed
- Edge cases: X/Y passed

### Phase 10 Results
- Data grounding: X mismatches found, Y fixed
- Hardcoded value scan: X found, Y acceptable
- Formatting consistency: PASS/FAIL
- SP permissions: PASS/FAIL
- Follow-up chips: PASS/FAIL

### Overall: Grade [A] — [Production-ready / Needs rework / ...]
```

**Demo MUST be Grade A to be considered complete.** If Grade B or below, fix all issues and re-grade before handover.

---
**COMPLETION** — ALL Phase 9 AND Phase 10 checkboxes pass, quality grade is A. Mark all tasks `completed`. Present handover summary (Step 9) with grade (Step 10) to user. **Demo is NOT complete until grade is presented and is Grade A.**
---

## Common Anti-Patterns to AVOID

| Anti-Pattern | Fix |
|-------------|-----|
| Loading skills but not MCP tools | Load MCP tools FIRST via ToolSearch, then skills |
| Using other tools before AI Dev Kit | AI Dev Kit is PRIMARY, everything else is FALLBACK |
| **Drifting to CLI in long sessions** | **Check MCP tool table in Phase 0 BEFORE every Bash `databricks` command** |
| Asking user to run data generation manually | Use `databricks-synthetic-data-generation` skill + MCP tools |
| Asking user to manually set up Agent Bricks | Create programmatically via MCP tools |
| Skipping workspace confirmation in Phase 0 | ALWAYS confirm target workspace before any work |
| Deploying without SP permissions on UC tables | `app.yaml` only covers endpoints/warehouses — UC needs explicit GRANTs |
| Using SSE for agent chat | Databricks Apps proxy buffers streaming — use async polling |
| Using AbortController to cancel MAS polls | Kills in-flight request — use ref-based multi-chat isolation (FloatingAssistant pattern) |
| Excluding images from deployment | NEVER exclude `*.png/*.jpg/*.svg` from sync or .gitignore |
| **Declaring done without testing every tab** | **Phase 9 checklist is MANDATORY — test every page, every feature, every edge case** |
| **Skipping Lakebase / chat persistence** | **Phase 6 is NEVER optional for chat apps — user email, persistence, CRUD all required** |
| **Using `generate_database_credential()` in Apps** | **SP tokens lack security labels — use user's forwarded OAuth token from proxy** |
| **Building multi-chat incrementally** | **Use FloatingAssistant template as-is (ref-based isolation) or full stateMap from patterns-mas-chat.md for full-page chat** |
| **Skipping Pre-Code Compliance Checklist** | **ALWAYS run the checklist in Phase 4 before writing ANY code — even for "quick" revamps or gap-fills** |
| **Coding chat/UI from memory instead of reading templates** | **Read `templates/app/frontend/src/components/FloatingAssistant.tsx` and reference files EVERY TIME — patterns drift in memory** |
| **Treating "revamp" as informal gap-fill** | **Revamps follow the same Phase 4 flow: read references → run compliance checklist → present gap analysis → fix all gaps** |
| **Uploading node_modules/.venv to workspace** | **Check workspace for bloat BEFORE deploying: `databricks workspace list` and delete any node_modules, .venv, src directories** |
| **Skipping silver tables (bronze → gold only)** | **All 3 medallion layers are MANDATORY. Silver tables demonstrate real transformations (joins, enrichment, unified models) — without them the Architecture page is misleading** |
| **App resources not attached after deploy** | **`create_or_update_app` MCP tool lacks `resources` param, and `apps deploy` may not apply `app.yaml` resources. ALWAYS verify with `get_app()` — if `resources: []`, patch via `databricks api patch /api/2.0/apps/{name}` with resources JSON, then redeploy** |
| **Skipping Lakeview Dashboard in Phase 7** | **Dashboard is the Analyst persona's primary deliverable and proves gold layer works in native Databricks. Phase 7 has 4 sub-steps — Agent Bricks, Dashboard, App Deploy, SP Permissions — complete ALL in order. Dashboard is the most commonly skipped.** |
| **Skipping Phase 10 data grounding** | **EVERY number in the app must trace to a SQL query. Phase 10 is MANDATORY — present mismatch report, get approval, fix, then handover summary with all asset links** |
| **Tooltip shows `$102983K` instead of `$103.0M`** | **MANDATORY: Use tiered formatter (`>= 1M` → `$X.XM`, `>= 1K` → `$XK`) in a shared `lib/format.ts` — never per-page copies** |
| **SQL alias doesn't match frontend field name** | **Charts silently show $0. ALWAYS use fallback: `Number(p.booked \|\| p.booked_revenue \|\| 0)`. Verify aliases match after writing SQL** |
| **Follow-up shows both inline AND as chip** | **Backend MUST strip "Suggested follow-up:" section from response text when chips are extracted. Never show same text twice** |
| **Some responses have no follow-up chip** | **Inject system message into MAS call: "Always end with Suggested follow-up:". Extract with 4 strategies. If extraction fails, check agent response format** |
| **Follow-up chip looks like user message** | **Chip MUST be visually distinct: transparent bg, border, italic, arrow prefix (→), "Suggested follow-up" label. NEVER solid primary bg like user bubbles** |
| **"Powered by..." visible in customer demo** | **NEVER include attribution text. `grep -rn 'powered by\|Powered by' frontend/src/` and remove ALL matches** |
| **SP can't query KA endpoint or Genie Space** | **Grant `CAN_QUERY` on EVERY serving-endpoint the app calls (MAS, KA, Foundation Models, provisioned throughput, custom endpoints) AND `CAN_RUN` on genie (object type: `genie`, NOT `genie-spaces`) after first deploy** |
| **Charts render empty with axis labels but no bars** | **MANDATORY: Every chart/table MUST have a "No data available" fallback. Check `data.length === 0` before rendering** |

## Battle-Tested Gotchas

| # | Gotcha | Solution |
|---|--------|----------|
| 1 | `server_settings` in asyncpg silently breaks pool | Set `search_path` per-connection |
| 2 | `DATABRICKS_HOST` has no `https://` in Apps | Always add `https://` prefix |
| 3 | `w.config.token` returns `None` for OAuth | Use `w.config.authenticate()` |
| 4 | MAS uses `{"input": msgs}` not `{"messages": msgs}` | Check endpoint type |
| 5 | SSE streaming fails through Apps proxy | Use async polling instead |
| 6 | Deploy fails with "pending deployment" | Wait ~20 min cooldown |
| 7 | App SP has no UC table permissions | GRANT USE CATALOG, USE SCHEMA, SELECT after first deploy |
| 8 | Token expires after 1 hour (Lakebase) | User-token middleware (Phase 6 Step 4) refreshes on every request; for non-Apps deployments use background refresh loop (50 min) |
| 9 | `requirements.txt` with uv markers fails | Clean format: `package>=version` |
| 10 | Frontend images excluded from deploy | Never exclude `*.png/*.jpg/*.svg` |
| 11 | `generate_database_credential()` fails for SP in Apps | SP lacks security labels — use user's forwarded token via middleware |
| 12 | `app.yaml` `database` resource type not processed | Framework only picks up `serving_endpoint` — grant Lakebase perms manually |
| 13 | Conversations not persisting after page refresh | Lakebase tables not created, or middleware not capturing user token |
| 14 | User email shows "anonymous" | Proxy headers not being read — check `X-Forwarded-Email` in middleware |
| 15 | Multi-chat: messages/animation lost on switch | Using global React state instead of ref-based isolation — use FloatingAssistant template pattern (pendingConvsRef, completedResponsesRef) |
| 16 | `node_modules` uploaded to workspace (deploy hangs) | NEVER `import-dir` the full project — upload only `dist/`, `server/`, config files |
| 17 | App resources (warehouse, endpoint, Lakebase) not attached | `create_or_update_app` MCP tool has no `resources` parameter, and `databricks apps deploy` may not apply `app.yaml` resources. After deploy, check `get_app()` or `databricks apps get {name}` — if `"resources": []`, patch via CLI: `databricks api patch /api/2.0/apps/{name} --json '{"resources": [...]}'`, then redeploy. This is a known AI Dev Kit gap. |
| 18 | Silver tables missing from medallion | Data gen jumps bronze→gold because gold powers the app. But Architecture page shows 3-layer diagram. ALWAYS create silver tables with real transformations (joins, enrichment, unified models, variance flags) |
| 19 | Recharts tooltip shows `$102983K` | Use tiered formatter in shared `lib/format.ts`: `>= 1M` → `$X.XM`, `>= 1K` → `$XK`. Apply to ALL pages via shared `CustomTooltip` component |
| 20 | SQL alias doesn't match frontend field name | Charts silently show $0. Use fallback: `Number(p.booked \|\| p.booked_revenue \|\| 0)`. After writing SQL, verify column aliases match frontend destructuring |
| 21 | Follow-up shows both inline AND as chip | Backend `_extract_followups()` extracts chip, but text remains in response. MUST call `_strip_followup_section()` to remove "Suggested follow-up:" block from response before returning |
| 22 | Some MAS responses have no follow-up chip | Inject system message: "Always end with Suggested follow-up: [question]". Extract with 4 strategies: (1) explicit block, (2) trailing numbered lines, (3) last question sentence, (4) "Would you like..." patterns |
| 23 | Follow-up chip looks identical to user message | Style distinctly: transparent bg, subtle border, italic, arrow prefix (`→`), "Suggested follow-up" label above. NEVER use solid primary bg |
| 24 | "Powered by X" visible in customer demo | `grep -rn 'powered by' frontend/src/` — remove ALL matches. Customer demos must feel like the customer's own product |
| 25 | SP has no permissions on serving endpoints or Genie Space | After first deploy, grant `CAN_QUERY` on EVERY serving-endpoint the app calls — KA, MAS, Foundation Models (`databricks-claude-sonnet-4-5` etc.), provisioned throughput, custom endpoints — AND `CAN_RUN` on genie spaces. Object type is `genie` (NOT `genie-spaces`). Use `grep -rn 'endpoint' app.yaml server/` to find all endpoint names |
| 26 | Charts render empty with orphaned axis labels | Every chart/table MUST check `data.length === 0` and show "No data available" placeholder instead of rendering empty SVG |
| 27 | Permissions API format error | Use flat `permission_level` format, NOT `all_permissions` array. Example: `{"access_control_list": [{"service_principal_name": "...", "permission_level": "CAN_QUERY"}]}` |

## Examples

### Example: Retail Customer Demo
**User says**: "Build a demo for Walmart around supply chain optimization"

**Result**: Research Walmart → Present story plan with supply chain narrative, KPIs, timeline → Wait for approval → Generate deterministic supply chain data → Create KA for policy docs + Genie for SQL + MAS to orchestrate → Build app with Executive/Analyst/Technical layers → Configure Lakebase → Package as Asset Bundle

### Example: Financial Services POC
**User says**: "Create a POC for JPMorgan Chase on fraud detection"

**Result**: Research JPMorgan → Present fraud detection story with metrics → Get approval → Generate synthetic transaction data → Create Agent Bricks for fraud reports + transaction queries → Build app with fraud dashboard + AI insights → Deploy via Asset Bundle

## References

- [story-template.md](references/story-template.md) — Full story planning template
- [app-design-philosophy.md](references/app-design-philosophy.md) — Three-persona model and design system
- [app-design-checklist.md](references/app-design-checklist.md) — UI/UX standards checklist
- [agent-bricks-decision-tree.md](references/agent-bricks-decision-tree.md) — When to create KA/Genie/MAS
- [patterns-auth-lakebase.md](references/patterns-auth-lakebase.md) — Authentication, Lakebase, and SP permissions
- [patterns-mas-chat.md](references/patterns-mas-chat.md) — MAS integration and async chat patterns
- [patterns-ui-frontend.md](references/patterns-ui-frontend.md) — Design system, CSS, and frontend libraries
- [asset-bundle-guide.md](references/asset-bundle-guide.md) — Asset Bundle packaging and deployment
- [validation-and-grading.md](references/validation-and-grading.md) — Quality checkpoints and grading
- [troubleshooting.md](references/troubleshooting.md) — Symptom-driven troubleshooting decision tree
- [quick-reference.md](references/quick-reference.md) — Quick reference checklists

## Templates

- [app/](templates/app/) — **Starter app template** (FastAPI + React, floating AI chat widget with multi-chat isolation, Lakebase, MAS routing animation). See [CUSTOMIZE.md](templates/app/CUSTOMIZE.md) for placeholder reference.
- [databricks.yml](templates/databricks.yml) — Asset Bundle config
- [README.md](templates/README.md) — Deployment instructions
- [STORY.md](templates/STORY.md) — Story document

## Key Reminders

1. **Pre-flight checklist is MANDATORY** — verify MCP tools FIRST, every time
2. **Story approval is a GATE** — no code until approved
3. **Automate everything** — never ask user to run manually
4. **AI Dev Kit is PRIMARY** — not optional, not one of many choices
5. **Bundle everything** — reproducibility is non-negotiable
6. **Production-grade UI** — no hackathon aesthetics
7. **Multi-persona value** — Executive, Analyst, Technical must all benefit
