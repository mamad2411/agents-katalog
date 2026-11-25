---
name: deploy-pricing-optimization
description: "Deploy a pricing optimization demo app — RGM pricing, customer-branded pricing demo, multi-dataset pricing analysis"
---

# RGM Pricing Optimization — Deployment Guide

Deploy a multi-dataset pricing optimization application with React frontend, FastAPI backend, Lakebase PostgreSQL, Genie Spaces, and Knowledge Assistants. This demo showcases Revenue Growth Management pricing analytics on Databricks.

**Source repo:** `https://github.com/databricks-field-eng/rgm-pricing-optimization-demo-app.git`

**Built with fe-app-toolkit:** This demo uses `/configurable-react-template` for the frontend and `/chat-app-utilities` for the backend routers. Refer to those skills for component-level details.

## Architecture Overview

- **Frontend:** React (Vite) with configurable branding via CSS variables
- **Backend:** FastAPI on port 8000 (required — proxy forwards to 8000)
- **Database:** Lakebase PostgreSQL (autoscaling) for app state + synced tables for analytics
- **AI Services:** 4 Genie Spaces (2 per dataset) + 4 Knowledge Assistants (2 per dataset)
- **Data:** Unity Catalog with dataset-specific schemas (`gold_beverages`, `gold_snacks`)
- **Infra:** Terraform-managed (catalog, schemas, Lakebase, volumes, pipeline jobs)

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
| **App name** | Name for the Databricks App | `pricing-optimization` |
| **Catalog name** | Unity Catalog to use. If the user doesn't know, check their workspace default catalog with `databricks current-user me -p <profile>` — FEVM workspaces auto-create a catalog. Users may not have permissions to create new catalogs. | `my_workspace_catalog` |
| **Customer name** | For branding (or "Databricks" for default) | `Acme Corp` |

Store these values and substitute them for all `<placeholder>` references in subsequent steps. If the user already has a CLI profile configured, skip the auth login step.

## Step 1: Clone the Repository

```bash
git clone https://github.com/databricks-field-eng/rgm-pricing-optimization-demo-app.git
cd rgm-pricing-optimization-demo-app
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

Terraform creates the catalog, schemas, Lakebase instance, volumes, and pipeline jobs.

```bash
cd terraform
terraform init
terraform plan -var="databricks_profile=<profile-name>"
terraform apply -var="databricks_profile=<profile-name>"
cd ..
```

This provisions:
- Unity Catalog and dataset-specific schemas (`gold_beverages`, `gold_snacks`)
- Lakebase PostgreSQL instance (autoscaling)
- Unity Catalog volumes for docs and reports
- DLT pipeline job definitions

## Step 4: Run Pipeline Jobs

Each pipeline has 5 tasks: synthetic data generation, feature engineering, model training, batch inference, and prepare app tables with Change Data Feed (CDF).

```bash
# Run beverages pipeline
databricks jobs run-now <beverages-job-id> -p <profile-name>

# Run snacks pipeline
databricks jobs run-now <snacks-job-id> -p <profile-name>
```

Wait for both pipelines to complete before proceeding. CDF must be enabled on the output tables for synced tables to work.

## Step 5: Create Synced Tables + PG Grants

Sync Delta tables from Unity Catalog into Lakebase for low-latency app serving. Source tables must have Change Data Feed enabled (`delta.enableChangeDataFeed = true`).

The repo includes a script that syncs all gold tables for both datasets, waits for them to come online, creates the SP PG role, and grants access — all in one command:

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

If `psycopg2` is not installed, the script prints manual SQL commands and exits cleanly.

## Step 6: Upload Volume Content

Upload pricing documentation and generated reports for each dataset:

```bash
# Upload docs
databricks fs cp -r ./data/beverages/docs/ \
  /Volumes/<catalog>/gold/ka_pricing_docs_beverages/ -p <profile-name>

databricks fs cp -r ./data/snacks/docs/ \
  /Volumes/<catalog>/gold/ka_pricing_docs_snacks/ -p <profile-name>

# Upload generated reports
databricks fs cp -r ./data/beverages/reports/ \
  /Volumes/<catalog>/gold/ka_generated_reports_beverages/ -p <profile-name>

databricks fs cp -r ./data/snacks/reports/ \
  /Volumes/<catalog>/gold/ka_generated_reports_snacks/ -p <profile-name>
```

## Step 7: Create Genie Spaces and Knowledge Assistants

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
| Beverages Product Reviews | `/Volumes/<catalog>/gold/ka_pricing_docs_beverages` |
| Beverages Generated Reports | `/Volumes/<catalog>/gold/ka_generated_reports_beverages` |
| Snacks Product Reviews | `/Volumes/<catalog>/gold/ka_pricing_docs_snacks` |
| Snacks Generated Reports | `/Volumes/<catalog>/gold/ka_generated_reports_snacks` |

Record the Genie Space IDs and KA endpoint names for the next step.

## Step 8: Configure app.yaml

Set environment variables in `app.yaml`:

```yaml
command:
  - "uvicorn"
  - "server.app:app"
  - "--host"
  - "0.0.0.0"
  - "--port"
  - "8000"

env:
  # Use LAKEBASE_ENDPOINT for autoscaling Lakebase (projects/.../endpoints/primary)
  # Use LAKEBASE_INSTANCE for regular (non-autoscaling) Lakebase instances
  - name: LAKEBASE_ENDPOINT
    value: "projects/<project-id>/branches/production/endpoints/primary"
  # - name: LAKEBASE_INSTANCE
  #   value: "<lakebase-instance-name>"
  - name: GENIE_BEVERAGES_SPACE_ID
    value: "<beverages-genie-space-id>"
  - name: GENIE_SNACKS_SPACE_ID
    value: "<snacks-genie-space-id>"
  - name: KA_BEVERAGES_REVIEWS_ENDPOINT
    value: "<beverages-reviews-ka-endpoint>"
  - name: KA_BEVERAGES_REPORTS_ENDPOINT
    value: "<beverages-reports-ka-endpoint>"
  - name: KA_SNACKS_REVIEWS_ENDPOINT
    value: "<snacks-reviews-ka-endpoint>"
  - name: KA_SNACKS_REPORTS_ENDPOINT
    value: "<snacks-reports-ka-endpoint>"
```

See `references/customization-guide.md` for the full environment variable reference.

## Step 9: Build the React Frontend

```bash
cd client
npm install
./node_modules/.bin/vite build --outDir out
cd ..
```

Do NOT use `npm run build` if the system `npm` is broken — call `vite` directly.

## Step 10: Stage and Upload

Always use rsync with `--exclude='node_modules'` to stage. Never upload `node_modules` — it exceeds the 10MB file size limit.

```bash
# Stage to temp directory
rsync -av --exclude='node_modules' --exclude='.venv' --exclude='__pycache__' \
  --exclude='.git' --exclude='.env' \
  . /tmp/pricing-demo-deploy/

# Upload to workspace
databricks workspace import-dir /tmp/pricing-demo-deploy/ \
  /Workspace/Users/<user>/<app-name> \
  -p <profile-name>
```

## Step 11: Deploy the App

```bash
databricks apps deploy <app-name> \
  --source-code-path=/Workspace/Users/<user>/<app-name> \
  -p <profile-name>
```

Verify the deployment:

```bash
databricks apps get <app-name> -p <profile-name>
```

The app URL will be `https://<app-name>-<workspace-id>.aws.databricksapps.com`. Append `/logz` to view application logs.

## Step 12: Grant SP Permissions and Attach Resources

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

## Step 13: Verify Deployment

Run the automated verification script to check all deployment components:

```bash
python3 scripts/verify_deployment.py \
  --profile <profile-name> \
  --app-name <app-name> \
  --verbose \
  --fix
```

This checks: Unity Catalog (schemas, tables, row counts, volumes), Lakebase (synced tables ONLINE, SP PG role, grants), SQL Warehouse, Genie Spaces, Knowledge Assistants, and App status. The `--fix` flag auto-creates missing PG roles and grants (idempotent).

## Step 14: Post-Deploy Customization

### Import Default Branding

The default Databricks branding preset is available in two locations: `branding-default.json` at the root of the source repo, and `resources/branding-default.json` within this plugin (`fe-rgm-demos`). Import it via the admin panel in the app UI.

### Custom Branding

Create a new preset JSON with customer-specific colors and logo. See `references/customization-guide.md` for all available branding keys and how to create customer-branded versions.

## Guardrails

- **NEVER delete existing apps or shared resources** without explicit user confirmation — these are shared workspaces
- **Port 8000 is REQUIRED** — the Databricks Apps proxy forwards to port 8000. Using 8080 causes 502 errors.
- **Always use rsync with `--exclude='node_modules'`** for staging
- **Python 3.9 compatibility** — use `Optional[X]` not `X | None`, `Dict[str, Any]` not `dict[str, Any]`
- **CDF required on source tables** — synced tables will fail without `delta.enableChangeDataFeed = true`
- **Lakebase PG grants** — multi-SP environments need `GRANT CREATE ON SCHEMA public TO PUBLIC` and `GRANT ALL ON ALL TABLES IN SCHEMA public TO PUBLIC`
- **`resources:` in app.yaml is NOT read by `deploy`** — must run `setup_app_permissions.py`
- **SP needs CAN_RUN on Genie Spaces** (not just warehouse CAN_USE)
- **After granting permissions, redeploy the app** to refresh cached credentials

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| 502 Bad Gateway | App not on port 8000 | Set `--port 8000` in app.yaml command |
| Synced table fails | No CDF on source | Add `TBLPROPERTIES (delta.enableChangeDataFeed = true)` |
| 10MB upload error | node_modules included | Use rsync with `--exclude='node_modules'` |
| OAuth token expired | 1-hour token lifetime | OAuthConnection pattern handles refresh automatically |
| SP can't create tables | Missing PG grants | Run GRANT CREATE/ALL statements |

## Related Skills

- `/configurable-react-template` — Frontend component library used by this demo
- `/chat-app-utilities` — Backend router utilities used by this demo
- `/databricks-apps` — General Databricks Apps development patterns
- `/databricks-lakebase` — Lakebase database management
