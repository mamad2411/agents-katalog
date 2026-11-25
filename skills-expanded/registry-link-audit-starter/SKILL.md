# Registry Link Audit Starter

Use this skill to check a selected subset of registry resource URLs and summarize which entries are reachable.

## What it does

- Loads `registry/resources_dedup.jsonl`.
- Audits selected resource IDs with HTTP GET requests and a repo-local user agent.
- Records final status codes, content types, redirects, and failures in compact JSON.

## When to use it

- You want a lightweight broken-link audit for the skill library registry.
- You need a fast smoke check before a broader freshness or stale-candidate sweep.

## Example

```bash
python3 skills/meta-maintenance/registry-link-audit-starter/scripts/audit_registry_links.py \
  --resource-id matplotlib-docs \
  --resource-id lychee-docs \
  --out scratch/meta/link_audit_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/meta-maintenance/registry-link-audit-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_cross_cutting_domain_skills -v`
