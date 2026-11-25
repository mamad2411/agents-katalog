---
name: deploying-airflow
description: Deploy Airflow DAGs and projects. Use when the user wants to deploy code, push DAGs, set up CI/CD, deploy to production, or asks about deployment strategies for Airflow.
---

# Deploying Airflow

This skill covers deploying Airflow DAGs and projects to production, whether using Astro (Astronomer's managed platform) or open-source Airflow on Docker Compose or Kubernetes.

**Choosing a path:** Astro is a good fit for managed operations and faster CI/CD. For open-source, use Docker Compose for dev and the Helm chart for production.

---

## Astro (Astronomer)

Astro provides CLI commands and GitHub integration for deploying Airflow projects.

### Deploy Commands

| Command | What It Does |
|---------|--------------|
| `astro deploy` | Full project deploy — builds Docker image and deploys DAGs |
| `astro deploy --dags` | DAG-only deploy — pushes only DAG files (fast, no image build) |
| `astro deploy --image` | Image-only deploy — pushes only the Docker image (for multi-repo CI/CD) |
| `astro deploy --dbt` | dbt project deploy — deploys a dbt project to run alongside Airflow |

### Full Project Deploy

Builds a Docker image from your Astro project and deploys everything (DAGs, plugins, requirements, packages):

```bash
astro deploy
```

Use this when you've changed `requirements.txt`, `Dockerfile`, `packages.txt`, plugins, or any non-DAG file.

### DAG-Only Deploy

Pushes only files in the `dags/` directory without rebuilding the Docker image:

```bash
astro deploy --dags
```

This is significantly faster than a full deploy since it skips the image build. Use this when you've only changed DAG files and haven't modified dependencies or configuration.

### Image-Only Deploy

Pushes only the Docker image without updating DAGs:

```bash
astro deploy --image
```

This is useful in multi-repo setups where DAGs are deployed separately from the image, or in CI/CD pipelines that manage image and DAG deploys independently.

### dbt Project Deploy

Deploys a dbt project to run with Cosmos on an Astro deployment:

```bash
astro deploy --dbt
```

### GitHub Integration

Astro supports branch-to-deployment mapping for automated deploys:

- Map branches to specific deployments (e.g., `main` -> production, `develop` -> staging)
- Pushes to mapped branches trigger automatic deploys
- Supports DAG-only deploys on merge for faster iteration

Configure this in the Astro UI under **Deployment Settings > CI/CD**.

### CI/CD Patterns

Common CI/CD strategies on Astro:

1. **DAG-only on feature branches**: Use `astro deploy --dags` for fast iteration during development
2. **Full deploy on main**: Use `astro deploy` on merge to main for production releases
3. **Separate image and DAG pipelines**: Use `--image` and `--dags` in separate CI jobs for independent release cycles

### Deploy Queue

When multiple deploys are triggered in quick succession, Astro processes them sequentially in a deploy queue. Each deploy completes before the next one starts.

### Reference

- [Astro Deploy Documentation](https://www.astronomer.io/docs/astro/deploy-code)

---

## Open-Source Deployment (Docker Compose & Kubernetes)

> **For Docker Compose setup (LocalExecutor + CeleryExecutor), Kubernetes Helm chart values.yaml, DAG deployment strategies, and operational commands, see:**
> `references/open-source-deployment.md`

---

## Related Skills

- **setting-up-astro-project** — Initialize a new Astro project
- **managing-astro-local-env** — Local development with `astro dev`
- **authoring-dags** — Writing DAGs before deployment
- **testing-dags** — Testing DAGs before deployment

