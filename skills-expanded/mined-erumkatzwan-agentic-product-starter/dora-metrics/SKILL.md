---
name: dora-metrics
description: Use when someone asks how the team is delivering, wants DORA metrics or the delivery dashboard explained or changed, during a retro, after an incident, or when real production deployments are added. Covers the four keys, how they are measured here, and how to improve them.
---

# DORA metrics

Read [ADR-0010](../../../docs/adr/0010-dora-metrics.md) for the definitions.

## Where the numbers are

* **Dashboard:** the website's `dora/` page (GitHub Pages), updated every Monday.
* **Raw data:** `dora.json` on the `metrics` branch, with a year of weekly history.
* **Now:** `GITHUB_TOKEN=<token> node scripts/dora-metrics.mjs --repo <owner>/<repo> --days 30` (a token with read access to pull requests, issues and actions).
* **Re-run:** Actions → **DORA metrics** → Run workflow.

## Keep the data honest

* **Incidents:** when customers are affected in production, open an issue from the **Incident** template (label `incident`) straight away and close it when service is back. Do not use the label for ordinary bugs.
* **Reverts:** use GitHub's **Revert** button so the pull request title starts with "Revert"; it counts as a failed change.
* **Real deployments:** when an app deploys to production from a workflow, add that workflow file to `DEPLOY_WORKFLOWS` in `.github/workflows/dora.yml`. From then on, deployments are its successful runs on `main`.

## Read the dashboard in a retro

| Key | If it is not Elite or High, try |
|---|---|
| Deployment frequency | Smaller tickets (`to-tickets`), merging behind feature flags instead of long branches |
| Lead time for changes | Smaller pull requests, faster reviews, fixing slow or flaky CI jobs |
| Change failure rate | More tests at the right level (`tdd`), feature flags defaulting to off, the review checklist |
| Time to restore service | Observability alerts and dashboards (`observability`), quick rollback by revert or flag |

Use the trend lines, not a single week. Bring one concrete improvement into the next sprint (`retro`).

## Change the measurement

1. Update `scripts/dora-metrics.mjs` and its tests (`node --test scripts/dora-metrics.test.mjs`).
2. Update ADR-0010 if a definition changes (or write a new ADR that supersedes it), and the "How it is measured" section of `apps/website/dora/index.html`.
3. Outgrowing this setup (many repositories, a deployment pipeline, an incident tool)? Consider [Apache DevLake](https://devlake.apache.org), which has DORA dashboards built in.
