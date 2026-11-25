---
name: shop
description: "Route substantive software-engineering work to the smallest useful set of specialized SkillShop playbooks before analysis or execution. Use for architecture, implementation, debugging, QA, performance, security, reliability, frontend, backend, delivery, migrations, production readiness, mobile, payments, or other engineering work where expert workflow guidance can materially change the result."
when_to_use: "Invoke for substantive engineering work after the deterministic hook detects engineering intent. Do not invoke merely because the current working directory is a project or because a trivial question mentions code."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/recommend.py *) Read Glob Grep"
---

# SkillShop router

Be a dispatcher, not another generic checklist.

## Route with a compact shortlist

Derive one concrete routing query from the user's task and lightweight repository context, then run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/recommend.py" \
  --query "<task in concrete engineering terms>" \
  --project "${CLAUDE_PROJECT_DIR}" \
  --top 6 \
  --json \
  --compact
```

The compact result intentionally omits playbook descriptions, trigger arrays, and paths. Do not rerun in verbose mode unless the shortlist is genuinely ambiguous.

If the turn is trivial or non-engineering, report that no specialist is needed and return to the request.

## Choose less

Load only playbooks that materially change the work:

- focused task: **1-2** playbooks by default;
- broad release/review: **2-4**;
- more than 4 only when the request truly spans independent risk domains.

Prefer complementary jobs over overlapping reviewers. Do not load a generic helper when the primary playbook already contains the needed procedure.

Examples:

```text
payment webhook bug
  -> payment-integrity + systematic-debugging

frontend redesign
  -> frontend-slop-obliterator
  -> add responsive-review only when breakpoint behavior is actually part of the risk

load-test release gate
  -> load-test + generator-sanity + capacity-plan
```

## Load on demand

For each selected playbook, read only:

`${CLAUDE_PLUGIN_ROOT}/library/playbooks/<name>/SKILL.md`

Read supporting files only when that playbook points to them or they are clearly required. Never open the whole catalog/library for context.

Reconcile conflicts rather than stacking instructions. User requirements and project facts win.

## Routing receipt

After loading selected playbooks, emit exactly one compact line before substantive work:

`SkillShop → <playbook>, <playbook>`

List only playbooks whose `SKILL.md` was actually read this turn. If none were loaded:

`SkillShop → no specialist needed`

Do not include scores, candidate lists, file paths, or router debug output unless the user asks.

When the task changes materially, route again. When it merely continues the same task, reuse the already-loaded specialist instead of paying the routing cost again.

A playbook is guidance, not permission: preserve tool permissions, authorization boundaries, production safeguards, and confirmation requirements.
