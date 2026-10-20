---
name: astro-cli
description: 'Expert-level guide for using the Astro CLI to manage Astronomer projects, develop locally, interact with Airflow APIs, and manage cloud deployments. You MUST load this skill when asked to use the astro command.'
license: MIT
---

# Astro CLI Skill

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- When initializing, configuring, or validating Astro/Airflow projects.
- When managing local Airflow environments (Docker or Standalone mode).
- When interacting with Astronomer cloud deployments, workspaces, and deployments.
- When calling the Airflow REST API via the `astro api airflow` wrapper.
- When troubleshooting production deployments by viewing logs or managing environment variables.

## WHEN NOT TO USE

- When writing generic Apache Airflow DAGs not specific to Astronomer CLI operations.

## Prerequisites

- Astro CLI (`astro`) must be installed.
- Docker must be running (for standard local development).
- `uv` must be installed (for Standalone local development).

## Core Process

1. Use `astro login` to authenticate before attempting cloud API or deployment commands.
2. For local development, use `astro dev start` to launch Airflow.
3. Use `astro api airflow` for authenticated API requests to both local and cloud environments.

## Step-by-Step Workflows

### Project Setup & Configuration

- **Initialize project**: `astro dev init`
- **Validate DAGs locally**: `astro dev parse`
- **Export connections/variables**: `astro dev object export --connections --variables`
- **Import connections/variables**: `astro dev object import --connections --variables --file <path>`

### Managing Local Environment

- **Start (Docker)**: `astro dev start`
- **Start (Standalone)**: `astro dev start --standalone`
- **Stop/Kill**: `astro dev stop` / `astro dev kill` (kill removes volumes/venv)
- **View local logs**: `astro dev logs --scheduler` (or `--webserver`, `--workers`)
- **Run Airflow CLI**: `astro dev run dags list`
- **Check proxy status**: `astro dev proxy status` (for multi-project routing)

### Astro CLI Commands for Local Dev

- **Get tab completions**: `astro completion <shell>` (script to get tab completions for Astro CLI cmds)
- **Get registry info**: `astro api registry` (Get info from the Airflow registry API)
- **Run bash in scheduler**: `astro dev bash` (Enter the scheduler container to run bash cmds)
- **Remove all containers**: `astro dev kill` (Remove all containers incl metab, connections)
- **Get stream/logs**: `astro dev logs` (Get logs -s / -d / -t / -a, -f for a stream)
- **Check import errors**: `astro dev parse` (Check for import errors)
- **Run tests in container**: `astro dev pytest` (Run tests in /tests in a container)
- **Run Airflow CLI command**: `astro dev run` (Run any Airflow CLI command!)
- **Force reparsing of DAGs**: `astro dev run dags reserialize` (Force reparsing of all Dags incl new ones)
- **Start locally with cloud connections**: `astro dev start --deployment-id [deployment-id]` (For Astro customers start locally with the same AF connections as your deployment)

### Cloud Deployment Management

- **Switch workspace**: `astro workspace switch <WORKSPACE_ID>`
- **List/Inspect deployments**: `astro deployment list` / `astro deployment inspect <DEPLOYMENT_ID>`
- **Create deployment**: `astro deployment create --label <NAME> --executor celery`
- **Deploy code (Full)**: `astro deploy <DEPLOYMENT_ID>`
- **Deploy DAGs only**: `astro deploy <DEPLOYMENT_ID> --dags` (requires `dag-deploy-enabled`)
- **Manage variables**: `astro deployment variable create --deployment-id <ID> --key <KEY> --value <VAL> --secret`

### Troubleshooting Cloud Deployments

- **View deployment logs**: `astro deployment logs <DEPLOYMENT_ID> --error`
- **Filter logs by component**: `astro deployment logs <ID> --scheduler` (or `--workers`, `--triggerer`)
- **Search logs**: `astro deployment logs <ID> --keyword "ImportError"`

### Executing Airflow REST API calls via Astro CLI

The `astro api airflow` command automatically handles authentication for your current context.

Examples:
- **List DAGs**: `astro api airflow get_dags`
- **Get DAG details**: `astro api airflow get_dag -p dag_id=<dag_id>`
- **Trigger DAG run**: `astro api airflow trigger_dag_run -p dag_id=<dag_id> -F conf[key]=value`
- **List task instances**: `astro api airflow get_task_instances -p dag_id=<dag_id> -p dag_run_id=~`
- **Filter with jq**: `astro api airflow get_dags -q '.dags[].dag_id'`

## Common Pitfalls

- **Missing Authentication**: Forgetting to run `astro login` before cloud operations.
- **Context Mismatch**: Running commands in the wrong workspace or against the wrong deployment. Always check `astro workspace list` or `astro deployment list`.
- **Standalone Version Pinning**: Standalone mode requires Airflow 3.x/Runtime 13.x+.
- **Interactive Hangs**: Avoid running interactive commands like `astro login` in non-interactive environments without appropriate flags.

## Related Skills

- **astronomer-llms**:
  Read and navigate Astronomer documentation using llms.txt context.
- **apache-airflow-api**:
  Execute Apache Airflow Stable REST API queries, manage DAGs, backfills, connections, variables, and assets.
- [Managing Astro Local Environment](https://github.com/astronomer/agents/blob/main/skills/managing-astro-local-env/SKILL.md)
- [Troubleshooting Astro Deployments](https://github.com/astronomer/agents/blob/main/skills/troubleshooting-astro-deployments/skill.md)

## References

- [Astro CLI llms.txt index](https://www.astronomer.io/docs/astro/cli/llms.txt)
- [Astronomer platform llms.txt](https://www.astronomer.io/llms.txt)
