---
name: portfolio-demo-health
description: Check public demo repos for live reachability, CI health, and docs/runtime drift, then summarize no-op status or prepare targeted fixes.
---

# Portfolio Demo Health

## What this skill is for

Use this skill when you want to verify whether the public demo fleet is still healthy and whether the website or repo docs need adjustments.

## When to use it

Use this skill when:
- checking live demo availability
- checking whether demo repos still pass their latest visible CI run
- deciding whether website wording should be downgraded because a demo broke

## When not to use it

Do not use this skill when:
- the task is to add a brand-new repo
- the task is a full website sync after code changes
- there is no public demo involved

## Required inputs

- [`.codex/automations/repo-registry.yml`](C:/Users/tcmk_/Downloads/Adredes-weslee.github.io/.codex/automations/repo-registry.yml)
- network access
- local repo clone only when deeper inspection is needed

## Required workflow

1. Read the repos in `repo-registry.yml` where `has_public_demo: true`.
2. Use `public_demo_url` as the canonical live surface.
3. Check:
   - demo reachability
   - whether the live surface is only a Streamlit shell or sleep screen versus a fully interactive loaded app
   - latest visible GitHub Actions or CI status when available
   - obvious docs/runtime/demo-entrypoint drift
4. If all demos are healthy, return a visible summary table and stop.
5. If a repo is degraded, inspect the real repo and classify the issue:
   - docs drift
   - runtime failure
   - dependency or environment drift
   - hosting-only issue
6. Draft only the minimum repo or website changes needed.

## Expected outputs

- a visible summary table with:
  - repo
  - demo reachable yes/no
  - live surface status: loaded / shell / sleep / error
  - CI healthy yes/no/unknown
  - action needed yes/no
  - short note
- when needed:
  - repo-level issue summary
  - recommended fix
  - website impact summary

## Validation and stop condition

Stop when:
- every public-demo repo was checked against the registry
- the result is either a clean no-op summary or a targeted issue report
- no repo edits are proposed without an actual degraded signal

Do not auto-merge or auto-push by default.
