---
name: package-github-dwh-blue
description: Provision and operate a single-host GitHub organization warehouse with ClickHouse, dlt, dbt, PocketBase, systemd, Vultr, and Cloudflare.
---

# GitHub DWH Package Skill

Use the bundled `blue` launcher. Desired state belongs in `colors.yml`; generated output belongs in `.colors/`; credentials are `COLORS_PAR_*` variables in an ignored `.envrc.private`.

Required credentials:

- `COLORS_PAR_VULTR_API_KEY`
- `COLORS_PAR_CLOUDFLARE_API_TOKEN`
- `COLORS_PAR_GITHUB_TOKEN`
- `COLORS_PAR_CLICKHOUSE_PASSWORD`
- `COLORS_PAR_POCKETBASE_SUPERUSER_PASSWORD`
- `COLORS_PAR_LIGHTDASH_ADMIN_PASSWORD`
- `COLORS_PAR_LIGHTDASH_SECRET`
- `COLORS_PAR_LIGHTDASH_POSTGRES_PASSWORD`
- `COLORS_PAR_LIGHTDASH_CLICKHOUSE_PASSWORD`
- `COLORS_PAR_LIGHTDASH_R2_ACCESS_KEY_ID`
- `COLORS_PAR_LIGHTDASH_R2_SECRET_ACCESS_KEY`
- `COLORS_PAR_R2_ACCESS_KEY_ID` and `COLORS_PAR_R2_SECRET_ACCESS_KEY` when `provider-backend` is `r2`

Never set `COLORS_PAR_PROFILE`, commit credentials, edit `.colors/`, or weaken `compute-prevent-destroy`.

Run safe checks first:

```sh
./blue build
./blue create --dry-run
./blue run --dry-run
```

With explicit authorization, `./blue create` provisions and converges the host. `./blue run` performs a real GitHub load and dbt build. `./blue delete` is guarded and destructive.

PocketBase stores whole-run control-plane records only. Do not add task DAGs, step queues, sensors, or retry policy to it.
