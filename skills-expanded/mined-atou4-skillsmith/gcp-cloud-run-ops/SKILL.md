---
name: gcp-cloud-run-ops
description: >-
  Deploy, verify, roll back and diagnose Google Cloud Run services safely: image by digest,
  revisions created without traffic, traffic shifted only after they start, tags cleared, a
  read-only post-deploy check and a cost and traffic snapshot. Use when the user says "deploy to
  Cloud Run", "ship to staging/production", "did the deploy work", "roll back", "why is the
  service down/slow/erroring", "what is Cloud Run costing", "budget alert", "check traffic and
  logs", or "stale revision / tag still warm". Not for creating projects or writing Terraform from
  scratch.
---

# Cloud Run operations

For teams that run one or more Cloud Run services per environment (for example `staging` and
`production`) and deploy them from a container image. It covers the release loop and the questions
that follow it: is it healthy, what is it costing, what is calling it. It does not create projects,
networks or IAM, and it does not replace infrastructure-as-code: settings that live in Terraform
stay in Terraform.

Two read-only scripts ship with the skill (Python 3 standard library plus an authenticated
`gcloud`):

```bash
# After a deploy: Ready, latest created revision is ready, it serves 100%, no tags, no ERROR logs.
python3 -I <this skill's folder>/scripts/verify_deploy.py --project PROJECT --region REGION \
  --services SERVICE_A,SERVICE_B [--health-url https://HOST/health] [--minutes 15]
# Cost and traffic: scaling, instances per revision, requests by class, instance-hours,
# fixed-cost resources, Cloud Scheduler jobs, top 4xx/5xx paths, then WARN findings.
python3 -I <this skill's folder>/scripts/cloudrun_snapshot.py --project PROJECT --region REGION \
  [--days 7] [--service-prefix PREFIX]
```

`verify_deploy.py` exits 0 only if every check passes (1 = a check failed, 2 = could not read).

## Steps

1. **Establish the target.** Find the project, region, service names, health URL and which
   environment is production: the repo's deploy scripts, Terraform (`google_cloud_run_v2_service`),
   docs, or `gcloud run services list --project P --region R`. If the repo has a
   `.cloud-run-ops.json` (format in [references/profile.md](references/profile.md)), use it. Tell
   the user what you found and ask for anything missing. Never guess the production project.
2. **Read the current state** with `verify_deploy.py` for the environment. Write down, per service,
   the revision at `percent: 100`: this is the rollback target. Ignore 0% entries.
3. **Deploy** following [references/deploy.md](references/deploy.md): the repo's own deploy script
   if it has one, otherwise the generic sequence (build `linux/amd64`, push, deploy by digest with
   `--no-traffic`, then `update-traffic --to-latest --clear-tags`). Lower environments first.
   Database migrations, if any, run before the deploy and must be backward compatible.
4. **Verify** with `verify_deploy.py`; it must exit 0. Then make one real request through the
   public entry point (app, load balancer or domain).
5. **Roll back** if step 4 fails: route 100% to the step-2 revisions
   ([deploy.md](references/deploy.md#roll-back)), then run `verify_deploy.py` again.
6. **Diagnose** cost, traffic or errors with `cloudrun_snapshot.py` first, then
   [references/diagnose.md](references/diagnose.md) (SKU map, log recipes, metrics) and
   [references/troubleshooting.md](references/troubleshooting.md). Explain each WARN in plain words.
7. **Verification and report.** Quote the `verify_deploy.py` result (or the snapshot numbers),
   name the environment, revisions and image digest, and list anything you could not check.
   Label estimates as estimates.

## Rules

- **Production changes need the user's explicit yes in this conversation**: deploy, any
  `update-traffic`, rollback, migration, secret version change, `services update`, Terraform apply.
  Read-only commands (describe, list, `logging read`, monitoring queries, both scripts) do not.
  If users are being hurt right now, rolling back to the recorded revision is allowed; say so at once.
- **Lower environment first.** A change reaches staging and passes step 4 before production.
- **Images by digest** (`IMAGE@sha256:...`), never a mutable tag, so a revision is reproducible.
- **No tag left behind.** A tagged revision is still addressable, so it keeps its own minimum
  instances warm and billed even at 0% traffic. Clear tags when shifting traffic.
- **Never print secrets.** Read a secret only into a variable inside a subshell; never echo it,
  pass it on a logged command line, or write it to a file, PR or chat.
- **Settings belong to their source.** If scaling, CPU, memory, env vars or secrets are declared
  in Terraform or another tool, change them there, not with `gcloud run services update`.
- **Stop on surprises.** A failing gate, an unexpected revision, or "permission denied" is reported,
  not routed around.
- This skill never deletes services, revisions, images or secrets.

## Related skills (optional)

| Need | Skill | If missing |
|---|---|---|
| Alert policies (5xx, latency, saturation, billable instance time) as Terraform | `cloud-run-alert-configuration` from [google/skills](https://github.com/google/skills) | Use the metric list in diagnose.md and the Cloud Monitoring docs |
| A log query the recipes do not cover | `cloud-logging-query-generation` from google/skills | Cloud Logging query language docs |
| Permission denied | `iam-helper-for-troubleshooting` from google/skills | The error names the missing permission; ask the project admin |
