# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a learning and reference repository for building data analytics infrastructure on Google Cloud Platform (GCP). The primary focus is on creating a comprehensive data pipeline using BigQuery, dbt, and related tools for marketing analytics.

## ⚠️ IMPORTANT: Learning Mode Required

**This repository is designed to be used with Claude Code's `/output-style learning` mode.**

### Output Style Setup

Users should set up the learning output style before starting:

```
/output-style learning
```

Or create a persistent learning output style configuration (see `learning-mode-guide.md`).

### Why Learning Mode?

This repository contains:

- **Educational content**: Step-by-step tutorials and hands-on exercises
- **Conceptual explanations**: 3-layer architecture, dbt patterns, LTV calculations
- **Practice-oriented**: Users need detailed explanations while executing commands
- **Progressive complexity**: From basic GCP CLI to advanced SQL and dbt

Claude Code should:

- Provide detailed explanations for each concept
- Break down complex topics into digestible pieces
- Suggest related readings and resources
- Ask clarifying questions to ensure understanding
- Encourage hands-on practice with guided instructions
- Review and explain command outputs
- Connect new concepts to previously learned material

## Repository Structure

This repository contains learning materials written in Japanese for data engineering:

### Documentation

- `GETTING-STARTED.md` - Quick start guide (5 minutes to begin)
- `multi-account-setup.md` - Multiple GCP account management guide
- `sample-data-guide.md` - Guide for using BigQuery public dataset (thelook_ecommerce)

### Setup Scripts

- `switch-to-learning.sh` - Switch to learning configuration (creates if not exists)
- `quickstart-sample-data.sh` - Quick test with sample queries
- `setup-learning-data.sh` - Setup learning dataset (copies data to your project)

### Utility Files

- `.aliases.example` - Bash/Zsh aliases for quick configuration switching

## Key Technologies Covered

The roadmap document covers a multi-phase learning approach:

### Phase 0: Preparation & Verification

- GCP CLI tools (gcloud, bq)
- BigQuery advanced features (partitioning, clustering, external tables, IAM)
- Data modeling (3-layer architecture: Raw, Staging, Mart)
- Service accounts and IAM design
- Terraform for infrastructure as code

### Phase 1: Data Integration

- dbt (data transformation tool)
- AppsFlyer PBA (People-Based Attribution for mobile/web analytics)
- Data integration tools (Databeat/Fivetran)

### Phase 2: Analytics Templates

- Advanced SQL (LTV calculations, window functions)
- BI tools (Metabase/Looker Studio)
- Cloud Scheduler
- Monitoring and alerting (Datadog/Cloud Monitoring)

## Architecture Concepts

### Three-Layer Data Architecture

The repository teaches a standard data warehouse pattern:

1. **Raw Layer** - Immutable source data from APIs and services
   - Partition by date
   - 90-day retention
   - Example: `raw_marketing_ads_platform_a.daily_report`

2. **Staging Layer** - Cleaned and standardized data
   - Managed by dbt
   - Unified schema across sources
   - 180-day retention
   - Example: `staging_marketing_ads.stg_ads_platform_a`

3. **Mart Layer** - Business logic and aggregated analytics
   - Pre-aggregated for performance
   - Connected to BI tools
   - Unlimited retention
   - Example: `mart_marketing_creative_performance`

### Data Flow

```
[External APIs (Databeat/AppsFlyer)]
    ↓
[Raw Layer: GCS/BigQuery]
    ↓ (dbt transformations)
[Staging Layer: Standardization]
    ↓ (dbt transformations)
[Mart Layer: Business Analytics]
    ↓
[BI Tools: Metabase/Looker Studio]
```

## Multiple GCP Account Management

This repository assumes users may be working with multiple GCP accounts/projects (e.g., client work + personal learning).

### Key Files for Multi-Account Support

- **multi-account-setup.md**: Complete guide for managing multiple GCP accounts using `gcloud configurations`
- **switch-to-learning.sh**: Helper script to switch to learning configuration
- **.aliases.example**: Convenient aliases for quick switching between accounts

### Workflow with Multiple Accounts

Users should:

1. Create a dedicated `learning-gcp` configuration for this repository
2. Switch to learning configuration before running scripts: `../scripts/switch-to-learning.sh`
3. All setup scripts display current configuration/account/project before execution
4. Production environment protection: Scripts warn if project ID contains "prod" or "production"

### Configuration Commands

```bash
# Create learning configuration
gcloud config configurations create learning-gcp
gcloud config configurations activate learning-gcp

# Set learning account and project
gcloud config set account YOUR_LEARNING_ACCOUNT@gmail.com
gcloud config set project YOUR_LEARNING_PROJECT_ID

# List all configurations
gcloud config configurations list

# Switch between configurations
gcloud config configurations activate learning-gcp    # For learning
gcloud config configurations activate client-a        # For client work
```

## Common Commands

This repository is documentation-focused, but here are common commands for the technologies it covers:

### BigQuery CLI (bq)

**IMPORTANT: Configure `.bigqueryrc` first to avoid repeating `--use_legacy_sql=false`**

```bash
# One-time setup: Create ~/.bigqueryrc
echo '[query]' > ~/.bigqueryrc
echo 'use_legacy_sql = false' >> ~/.bigqueryrc
```

After this setup, you can omit `--use_legacy_sql=false` from all `bq query` commands.

```bash
# List datasets
bq ls --project_id=PROJECT_ID

# Show table schema
bq show --schema --format=prettyjson PROJECT_ID:dataset.table

# Run query (no --use_legacy_sql=false needed with .bigqueryrc)
bq query 'SELECT * FROM `project.dataset.table` LIMIT 10'

# Create dataset
bq mk --dataset --location=asia-northeast1 PROJECT_ID:dataset_name

# Delete dataset
bq rm -r -f PROJECT_ID:dataset_name
```

### GCP CLI (gcloud)

```bash
# Authenticate
gcloud auth login

# Set project
gcloud config set project PROJECT_ID

# List service accounts
gcloud iam service-accounts list

# Create service account
gcloud iam service-accounts create SA_NAME --display-name="Display Name"
```

### dbt Commands

```bash
# Initialize project
dbt init project_name

# Test connection
dbt debug

# Run models
dbt run

# Run specific model
dbt run --models model_name

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

### Terraform Commands

```bash
# Initialize
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply

# Destroy resources
terraform destroy
```

## Important Concepts

### BigQuery Optimization

- **Partitioning**: Tables are partitioned by date to minimize scan costs
  - `PARTITION BY date`
  - Automatic partition expiration (e.g., 90 days)

- **Clustering**: Physical ordering of data by commonly filtered columns
  - `CLUSTER BY account_id, campaign_id`
  - Improves query performance for filtered queries

- **External Tables**: Query data in GCS without loading into BigQuery
  - Used for AppsFlyer Parquet files
  - Hive partitioning support

### IAM Design Principles

The repository teaches least-privilege access:

- **databeat-ingestion**: Write-only to Raw Layer
- **dbt-transformation**: Read from Raw, write to Staging/Mart
- **metabase-viewer**: Read-only from Staging/Mart

### dbt Project Structure

```
marketing_analytics/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── staging/
│   │   ├── ads/
│   │   │   ├── _ads__sources.yml
│   │   │   └── stg_ads_platform_a.sql
│   │   └── mobile_analytics/
│   └── marts/
│       └── marketing/
│           ├── mart_creative_performance.sql
│           └── mart_user_journey.sql
└── macros/
```

### Incremental Models

dbt incremental materialization processes only new data:

```sql
{{ config(materialized='incremental', unique_key='id') }}

SELECT * FROM {{ source('raw', 'table') }}
{% if is_incremental() %}
WHERE date > (SELECT MAX(date) FROM {{ this }})
{% endif %}
```

## LTV Calculation Pattern

A key business logic pattern taught in the roadmap:

```sql
-- Calculate 7-day, 30-day, 60-day, 90-day LTV
SUM(CASE
  WHEN DATE_DIFF(r.purchase_date, i.install_date, DAY) <= 7
  THEN r.total_revenue
  ELSE 0
END) AS revenue_7d
```

## Project Configuration

### BigQuery Location

- Primary region: `asia-northeast1` (Tokyo)

### Naming Conventions

- Raw datasets: `raw_marketing_*`
- Staging datasets: `staging_*`
- Mart datasets: `mart_*`
- Service accounts: `{purpose}-{action}@PROJECT.iam.gserviceaccount.com`

## Learning Progression

The recommended learning timeline is:

1. **Week 1-2**: GCP CLI, BigQuery basics, IAM
2. **Week 3-4**: dbt fundamentals and practice
3. **Week 5-6**: AppsFlyer, data integration tools
4. **Week 7-8**: Terraform, dashboards, monitoring

## Development Workflow

### Before Starting: Set Learning Mode

**CRITICAL**: Ensure learning output style is active:

```
/output-style learning
```

When working with this repository:

1. **Confirm learning mode is active**:
   - Check Claude Code's output style indicator
   - Learning mode should be providing detailed educational explanations

2. **Switch to learning configuration** (if using multiple accounts):

   ```bash
   ../scripts/switch-to-learning.sh
   # or
   gcloud config configurations activate learning-gcp
   ```

3. **Verify current settings** before running scripts:

   ```bash
   gcloud config list
   # Check: account, project
   ```

4. Read through the roadmap document to understand the architecture

5. Follow hands-on exercises in sequential order

6. Test concepts in a development dataset (`learning_dev`)

7. Use `--dry_run` with bq commands to verify queries before execution

8. Always clean up test resources to avoid costs

### Safety Features

- All scripts display current configuration/account/project before execution
- Production environment warning: Alerts if project ID contains "prod" or "production"
- Dedicated learning configuration prevents accidental operations on client projects

## Quick Start for Multiple Account Users

If the user is working with multiple GCP accounts:

1. **Set up Claude Code learning mode**:

   ```
   /output-style learning
   ```

   - This ensures Claude provides educational explanations
   - See `learning-mode-guide.md` for persistent configuration

2. **First time setup**:

   ```bash
   # Run the helper script (will create configuration if needed)
   ../scripts/switch-to-learning.sh

   # Authenticate
   gcloud auth login
   gcloud auth application-default login
   ```

3. **Daily workflow**:

   ```bash
   # Switch to learning
   ../scripts/switch-to-learning.sh

   # Run learning scripts
   ../scripts/setup-learning-data.sh

   # Switch back to client work
   gcloud config configurations activate client-a
   ```

4. **Verify before operations**:
   - All scripts display: Configuration, Account, Project
   - Check output before confirming any destructive operations
   - Scripts will warn if project ID contains "prod" or "production"

## Claude Code Interaction Guidelines for Learning Mode

When in learning mode, Claude Code should:

### Explaining Concepts

- Start with high-level overview before diving into details
- Use analogies to connect GCP concepts to familiar ideas
- Explain the "why" behind architectural decisions
- Relate new concepts to previous lessons

### Guiding Hands-On Practice

- **Present ONE task at a time** - Do not overwhelm with multiple commands
- **Let the user execute commands** - Only provide the command text, don't execute it yourself
- Provide step-by-step instructions with expected outputs
- Explain each command before the user executes it
- Review and interpret command outputs after the user shares results
- Suggest variations for deeper understanding

### Learning Notes and Progress Tracking

**IMPORTANT: Where to save learning notes**

- **Use `learning-log/YYYY-MM-DD.md`** for daily learning logs
- **Do NOT use individual `exercises.md` or `notes.md`** files in phase directories
- The `personal` branch is for personal learning, so `learning-log/*.md` files are tracked in Git
- Reference `learning-progress.md` to check completed topics
- Suggest next logical steps based on progress
- Review previous concepts before introducing new ones

**Files to avoid creating**:

- `phase*/exercises.md` (use `learning-log/` instead)
- `phase*/notes.md` (use `learning-log/` instead)
- Individual scattered note files (consolidate in `learning-log/`)

This keeps the repository clean and all learning materials in one organized location.

### Problem Solving

- When errors occur, explain root causes educationally
- Guide troubleshooting with learning objectives in mind
- Connect error messages to underlying concepts

### Assessment

- Ask comprehension questions periodically
- Suggest exercises to reinforce learning
- Encourage documentation in `learning-log/` and `exercises.md` files

## Language Note

The documentation is written in Japanese. When modifying or extending this repository, maintain consistency with the existing language unless specifically requested otherwise.
