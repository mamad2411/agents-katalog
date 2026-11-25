---
name: scheduled-agent-doctor
version: "1.0"
description: Audit, debug, trigger, and repair scheduled (cron) agents from chat — list what exists, verify cron and timezone really mean what the user intended, manually run one to test, disable or delete-and-recreate broken ones. Encodes the known failure modes (timezone double-conversion, zombie agents from older runtimes, cron-mode credential 403, DM-vs-group visibility) so users can self-serve.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - scheduled
    - cron
    - agents
    - diagnostics
    - self-service
---

# Scheduled Agent Doctor

Use this when someone says "我的定时任务没跑 / 跑错时间了 / 帮我看看有哪些定时任务 / 先手动跑一次试试 /
把它删了重建".

**You (the agent) drive the diagnosis yourself** with `agent_builder` (actions: `list_agents`,
`run_agent`, `disable_agent`, `delete_agent`) and `scheduled_agent_creator` (params: `schedule_cron`,
`schedule_timezone`, `skill_ref`, `execution_prompt`). Tool errors are findings — quote them
verbatim, never fail the run.

## How to run it

1. **Inventory.** `agent_builder` `{action:"list_agents"}` — show: agent id, skill, cron, timezone,
   status, last run. If the list is EMPTY but the user swears one exists: agents are owned per
   (user, platform, bot registration, conversation scope) — listing in a DM can miss agents created
   in a group and vice versa. Tell the user to run the doctor in the SAME chat where the agent was
   created.

2. **Sanity-check the schedule.** Read back the cron + timezone in plain words ("每周一 09:00
   Asia/Shanghai"). Known trap: stating a local time AND a timezone while the cron was already
   converted — double timezone shift. The contract is `schedule_cron` interpreted IN
   `schedule_timezone`, no extra conversion. If the user reports "提前/晚了 8 小时", this is almost
   always it → fix by recreating with the cron written in local wall-clock time + the right tz.

3. **Test-fire.** `agent_builder` `{action:"run_agent", agent_id}` triggers one manual run now
   (owner-only). Use it to separate "schedule wrong" from "run broken": if the manual run fails
   too, the problem is the skill/credentials, not cron.

4. **Credential reality check.** A scheduled run uses a minted key whose service grant is NARROWER
   than interactive chat: skills calling extra services (search/enrichment) can work via `::skill`
   but 403 on cron fire. If the manual interactive run works and the cron run 403s, report exactly
   that and suggest `nyxid-service-doctor` for the binding fix; do not blame the skill.

5. **Repair = delete + recreate.** There is no in-place edit. Agents created before
   creation-time cron/timezone validation existed can be zombies (bad cron persisted, never fire).
   Flow: confirm with the user → `{action:"delete_agent", agent_id}` (or `disable_agent` to keep it
   paused) → `scheduled_agent_creator` with corrected `schedule_cron` + `schedule_timezone` +
   `skill_ref` + `execution_prompt` → **verify**: `list_agents` again and show the new entry.
   "Creator said ok" is NOT proof — only the new list entry is.

6. **Report.** One block per agent touched: before → action taken → after (from the post-action
   list), plus the next expected fire time in the user's local words.

## Guardrails

- `delete_agent` only after the user confirms the specific agent id in this conversation; prefer
  `disable_agent` when intent is ambiguous.
- Never create duplicates: before recreating, check the inventory for an existing agent with the
  same skill + cron and point it out.
- Only use real returned data; never invent agent ids, crons, or run results.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
