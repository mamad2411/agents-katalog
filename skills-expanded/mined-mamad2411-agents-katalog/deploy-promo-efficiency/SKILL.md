---
name: deploy-promo-efficiency
description: "Deploy a promo efficiency demo app — trade promotion analysis, RGM promo optimization, promotional ROI"
---

# RGM Promo Efficiency Engine — Deployment Guide

Deploy a dual-dataset promotional efficiency application with causal inference analytics, scenario optimization, React frontend, FastAPI backend, Lakebase PostgreSQL, Genie Spaces, and Knowledge Assistants. This demo showcases Revenue Growth Management trade promotion analysis on Databricks.

**Source repo:** `https://github.com/databricks-field-eng/rgm-promo-efficiency-demo-app.git`

**Built with fe-app-toolkit:** This demo uses `/configurable-react-template` for the frontend and `/chat-app-utilities` for the backend routers. Refer to those skills for component-level details.

## Architecture Overview

- **Frontend:** React (Vite) with configurable branding via CSS variables
- **Backend:** FastAPI on port 8000 (required — proxy forwards to 8000)
- **Database:** Lakebase PostgreSQL (autoscaling) for app state + synced tables for analytics
- **AI Services:** Genie Spaces for promo data analysis per dataset + Knowledge Assistants for product reviews and reports per dataset
- **Data:** Unity Catalog with dataset-specific schemas, 4 gold tables per dataset
- **Analytics:** Causal inference pipeline for promotional lift measurement

See `references/architecture.md` for a detailed architecture breakdown.

## Prerequisites

1. **Databricks CLI** >= 0.230 — authenticated to the target workspace
2. **Terraform** >= 1.5
3. **Python** 3.9+ (use `Optional[X]` not `X | None` for 3.9 compatibility)
4. **Node.js** 18+
5. **Target workspace** — must support Lakebase (serverless/FE-VM workspace)

## Step 0: Gather Deployment Configuration

Before starting, collect these values from the user. Use `AskUserQuestion` to prompt for each:

| Variable | Description | Example |
|----------|-------------|---------|
| **Workspace URL** | Target Databricks workspace | `https://my-workspace.cloud.databricks.com` |
| **CLI profile name** | Databricks CLI profile (or `DEFAULT`) | `my-workspace` |
| **App name** | Name for the Databricks App | `promo-efficiency` |
| **Catalog name** | Unity Catalog to use. If the user doesn't know, check their workspace default catalog with `databricks current-user me -p <profile>` — FEVM workspaces auto-create a catalog. Users may not have permissions to create new catalogs. | `my_workspace_catalog` |
| **Customer name** | For branding (or "Databricks" for default) | `Acme Corp` |

Store these values and substitute them for all `<placeholder>` references in subsequent steps. If the user already has a CLI profile configured, skip the auth login step.

## Step 1: Clone the Repository

```bash
git clone https://github.com/databricks-field-eng/rgm-promo-efficiency-demo-app.git
cd rgm-promo-efficiency-demo-app
```

## Step 2: Configure Databricks CLI Profile

```bash
databricks auth login --host <workspace-url> --profile <profile-name>
```

Verify connectivity:

```bash
databricks current-user me -p <profile-name>
```

## Step 3: Provision Infrastructure with Terraform

```bash
cd terraform
terraform init
terraform plan -var="databricks_profile=<profile-name>"
terraform apply -var="databricks_profile=<profile-name>"
cd ..
```

This provisions:
- Unity Catalog and dataset-specific schemas
- Lakebase PostgreSQL instance (autoscaling)
- Unity Catalog volumes
- Bundle and pipeline job definitions

## Step 4: Deploy Bundles

Deploy Databricks Asset Bundles — one per dataset:

```bash
databricks bundle deploy --target demo -p <profile-name>
databricks bundle deploy --target demo-beverages -p <profile-name>
```

## Step 5: Run Pipeline Jobs

Each pipeline has 3 core tasks: generate promo data, causal inference, and prepare gold tables.

```bash
# Run snacks pipeline
databricks jobs run-now <snacks-job-id> -p <profile-name>

# Run beverages pipeline
databricks jobs run-now <beverages-job-id> -p <profile-name>
```

Wait for both pipelines to complete. The pipelines produce 4 gold tables per dataset:
- `app_products` — Product catalog
- `app_retailers` — Retailer information
- `app_promo_events` — Historical promotional events with outcomes
- `app_weekly_metrics` — Weekly performance metrics per product/retailer

## Step 6: Create Synced Tables + PG Grants

Sync the 4 gold tables per dataset from Delta to Lakebase, wait for online, create the SP PG role, and grant access — all automated:

```bash
python3 scripts/setup_synced_tables.py \
  --profile <profile-name> \
  --catalog <catalog-name> \
  --project-id <lakebase-project-uid> \
  --branch-id <lakebase-branch-uid> \
  --app-name <app-name>
```

The `--app-name` flag auto-fetches the app's SP client ID and creates the PG role via `databricks_create_role()`. This is the step that was previously manual and caused "no data visible" failures.

To run only the grants phase (e.g., after a redeploy to a new workspace):

```bash
python3 scripts/setup_synced_tables.py \
  --profile <profile-name> \
  --catalog <catalog-name> \
  --project-id <uid> \
  --branch-id <uid> \
  --app-name <app-name> \
  --phase grants
```

The script handles all PG grants automatically (synced schema USAGE/SELECT, public schema CREATE/ALL, pgvector extension). If `psycopg2` is not installed, it prints manual SQL commands and exits cleanly.

## Step 7: Upload Volume Content

Upload product review documents and generated reports for Knowledge Assistants:

```bash
databricks fs cp -r ./data/snacks/reviews/ \
  /Volumes/<catalog>/gold/ka_product_reviews_snacks/ -p <profile-name>

databricks fs cp -r ./data/snacks/reports/ \
  /Volumes/<catalog>/gold/ka_generated_reports_snacks/ -p <profile-name>

databricks fs cp -r ./data/beverages/reviews/ \
  /Volumes/<catalog>/gold/ka_product_reviews_beverages/ -p <profile-name>

databricks fs cp -r ./data/beverages/reports/ \
  /Volumes/<catalog>/gold/ka_generated_reports_beverages/ -p <profile-name>
```

## Step 8: Create Genie Spaces and Knowledge Assistants

Create 2 Genie Spaces (one per dataset) and 4 Knowledge Assistants (product reviews + generated reports per dataset).

The repo includes scripts that handle creation via the Databricks REST API and `databricks-tools-core`. Use these scripts — do NOT try to call REST APIs manually.

### Genie Spaces

```bash
python3 scripts/setup_genie_spaces.py \
  --profile <profile-name> \
  --catalog <catalog-name> \
  --warehouse-id <warehouse-id>
```

This creates both dataset Genie Spaces and outputs the space IDs. Record them for app.yaml.

### Knowledge Assistants

```bash
pip install databricks-tools-core  # if not already installed

python3 scripts/setup_knowledge_assistants.py \
  --profile <profile-name> \
  --catalog <catalog-name>
```

This creates 4 KAs (product reviews + generated reports for each dataset) and outputs the serving endpoint names. The script uses `databricks-tools-core` if available, with a REST API fallback.

**If the scripts fail** (e.g., Agent Bricks API not available on the workspace), create the KAs manually in the Databricks UI: Serving > Create > Knowledge Assistant. Point each at the corresponding UC Volume path:

| KA Name | Volume Path |
|---------|-------------|
| Snacks Product Reviews | `/Volumes/<catalog>/gold/ka_product_reviews_snacks` |
| Snacks Promo Reports | `/Volumes/<catalog>/gold/ka_generated_reports_snacks` |
| Beverages Product Reviews | `/Volumes/<catalog>/gold/ka_product_reviews_beverages` |
| Beverages Promo Reports | `/Volumes/<catalog>/gold/ka_generated_reports_beverages` |

Record the Genie Space IDs and KA endpoint names.

## Step 9: Configure app.yaml

```yaml
command:
  - "uvicorn"
  - "server.app:app"
  - "--host"
  - "0.0.0.0"
  - "--port"
  - "8000"

env:
  # ── Data location ──────────────────────────────────────────────
  - name: CATALOG
    value: "<catalog-name>"
  - name: SCHEMA
    value: "gold_snacks"

  # ── SQL Warehouse ──────────────────────────────────────────────
  - name: WAREHOUSE_ID
    value: "<warehouse-id>"

  # ── Lakebase ─────────────────────────────────────────────────────
  # Use LAKEBASE_ENDPOINT for autoscaling Lakebase (projects/.../endpoints/primary)
  # Use LAKEBASE_INSTANCE for regular (non-autoscaling) Lakebase instances
  - name: LAKEBASE_ENDPOINT
    value: "projects/<project-id>/branches/production/endpoints/primary"
  # - name: LAKEBASE_INSTANCE
  #   value: "<lakebase-instance-name>"

  # ── Serving Endpoints ──────────────────────────────────────────
  - name: VS_ENDPOINT
    value: "<vs-endpoint-name>"
  - name: VS_INDEX
    value: "<vs-index-name>"

  # ── Genie Spaces ───────────────────────────────────────────────
  - name: GENIE_SNACKS_SPACE_ID
    value: "<snacks-genie-space-id>"
  - name: GENIE_BEVERAGES_SPACE_ID
    value: "<beverages-genie-space-id>"

  # ── Knowledge Assistants — Snacks ──────────────────────────────
  - name: KA_SNACKS_REVIEWS_ENDPOINT
    value: "<snacks-reviews-ka-endpoint>"
  - name: KA_SNACKS_REPORTS_ENDPOINT
    value: "<snacks-reports-ka-endpoint>"
  - name: KA_SNACKS_SCENARIOS_ENDPOINT
    value: "<snacks-scenarios-ka-endpoint>"
  - name: KA_SNACKS_PORTFOLIOS_ENDPOINT
    value: "<snacks-portfolios-ka-endpoint>"

  # ── Knowledge Assistants — Beverages ───────────────────────────
  - name: KA_BEVERAGES_REVIEWS_ENDPOINT
    value: "<beverages-reviews-ka-endpoint>"
  - name: KA_BEVERAGES_REPORTS_ENDPOINT
    value: "<beverages-reports-ka-endpoint>"
  - name: KA_BEVERAGES_SCENARIOS_ENDPOINT
    value: "<beverages-scenarios-ka-endpoint>"
  - name: KA_BEVERAGES_PORTFOLIOS_ENDPOINT
    value: "<beverages-portfolios-ka-endpoint>"

  # ── Foundation Model ───────────────────────────────────────────
  - name: FM_ENDPOINT
    value: "<fm-serving-endpoint>"
  - name: EMBEDDING_ENDPOINT
    value: "<embedding-serving-endpoint>"
```

See `references/customization-guide.md` for the full environment variable reference.

## Step 10: Build the React Frontend

```bash
cd client
npm install
./node_modules/.bin/vite build --outDir out
cd ..
```

## Step 11: Stage and Upload

```bash
# Stage to temp directory (NEVER include node_modules)
rsync -av --exclude='node_modules' --exclude='.venv' --exclude='__pycache__' \
  --exclude='.git' --exclude='.env' \
  . /tmp/promo-demo-deploy/

# Upload to workspace
databricks workspace import-dir /tmp/promo-demo-deploy/ \
  /Workspace/Users/<user>/<app-name> \
  -p <profile-name>
```

## Step 12: Deploy the App

```bash
databricks apps deploy <app-name> \
  --source-code-path=/Workspace/Users/<user>/<app-name> \
  -p <profile-name>
```

Verify:

```bash
databricks apps get <app-name> -p <profile-name>
```

The app URL will be `https://<app-name>-<workspace-id>.aws.databricksapps.com`. Append `/logz` for logs.

## Step 13: Grant SP Permissions and Attach Resources

After deploying the app, the service principal needs permissions on all resources. `databricks apps deploy` does NOT read the `resources:` block from app.yaml — permissions must be granted separately.

```bash
python3 scripts/setup_app_permissions.py \
  --profile <profile-name> \
  --app-name <app-name> \
  --catalog <catalog-name> \
  --warehouse-id <warehouse-id>
```

This single command handles:
1. **UC grants** — USE CATALOG, USE SCHEMA, SELECT, READ/WRITE VOLUME on all dataset schemas
2. **Genie Space CAN_RUN** — reads Genie space IDs from app.yaml, grants CAN_RUN to the app SP
3. **App resource attachments** — attaches serving endpoints (FM, embedding, KAs) and warehouse from app.yaml
4. **SQL Warehouse CAN_USE** — grants the SP permission to use the warehouse

All operations are idempotent. Use `--dry-run` to preview.

After running, redeploy the app to pick up new permissions:

```bash
databricks apps deploy <app-name> \
  --source-code-path=/Workspace/Users/<user>/<app-name> \
  -p <profile-name>
```

## Step 14: Verify Deployment

Run the automated verification script to check all deployment components:

```bash
python3 scripts/verify_deployment.py \
  --profile <profile-name> \
  --app-name <app-name> \
  --verbose \
  --fix
```

This checks: Unity Catalog (schemas, tables, row counts, volumes), Lakebase (synced tables ONLINE, SP PG role, grants), SQL Warehouse, Genie Spaces, Knowledge Assistants, and App status. The `--fix` flag auto-creates missing PG roles and grants (idempotent).

## Step 15: Post-Deploy Customization

### Lakebase App State Tables

On first startup, `init_db()` creates these tables in Lakebase:
- `app_scenarios` — Saved optimization scenarios
- `app_optimization_portfolios` — Portfolio optimization results
- `chat_history` — Conversation logs
- `reports` — Generated analysis reports
- `demo_config` — Active app configuration
- `demo_presets` — Branding presets

### Import Branding

Import the default Databricks branding via the admin panel. The branding file is at `branding-default.json` in the repo root (also available at `resources/branding-default.json` in the vibe plugin). Create customer-specific presets following the guide in `references/customization-guide.md`.

## Guardrails

- **NEVER delete existing apps or shared resources** without explicit user confirmation
- **Port 8000 is REQUIRED** — using 8080 causes 502 errors
- **Always use rsync with `--exclude='node_modules'`** for staging
- **Python 3.9 compatibility** — use `Optional[X]` not `X | None`, `Dict[str, Any]` not `dict[str, Any]`
- **CDF required on source tables** — synced tables fail without it
- **PG grants are mandatory** for synced table schemas — without them the app SP cannot read synced data
- **`resources:` in app.yaml is NOT read by `deploy`** — must run `setup_app_permissions.py`
- **SP needs CAN_RUN on Genie Spaces** (not just warehouse CAN_USE)
- **After granting permissions, redeploy the app** to refresh cached credentials

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| 502 Bad Gateway | App not on port 8000 | Set `--port 8000` in app.yaml |
| Synced table fails | No CDF on source | Add `TBLPROPERTIES (delta.enableChangeDataFeed = true)` |
| Permission denied on synced schema | Missing PG grants | Run GRANT USAGE/SELECT on the schema |
| SP can't create tables | Missing CREATE grant | Run `GRANT CREATE ON SCHEMA public TO PUBLIC` |
| 10MB upload error | node_modules included | Use rsync with `--exclude='node_modules'` |
| Causal inference OOM | Cluster too small | Increase pipeline cluster size |
| Bundle deploy fails | Wrong target name | Verify target matches bundle config |

## Related Skills

- `/configurable-react-template` — Frontend component library used by this demo
- `/chat-app-utilities` — Backend router utilities used by this demo
- `/databricks-apps` — General Databricks Apps development patterns
- `/databricks-lakebase` — Lakebase database management
- `/deploy-pricing-optimization` — Sibling RGM demo for pricing analytics
