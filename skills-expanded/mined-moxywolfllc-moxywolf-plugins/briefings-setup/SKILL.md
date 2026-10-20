---
name: briefings-setup
risk_tier: side-effectful-gated
description: >
  Set up the daily-briefings plugin for a person — write or update their briefings config in the vault, then register the recurring scheduled tasks that run the commitment calendar and the morning brief. Use when the user asks to set up briefings, configure the commitment calendar, schedule their morning brief, change the briefing time, add a venue or a noisy sender, or invokes /briefings-setup. Idempotent: it reads what already exists and updates rather than duplicating.
---

# Briefings setup

Two things live here: the config that makes the briefings someone's, and the scheduled tasks that make them arrive without being asked for.

Both are side effects. The config is shared team knowledge on a shared drive, and a scheduled task is an automation that will keep running long after this session ends. Neither gets created without the owner seeing exactly what will be written and saying yes.

Read `${CLAUDE_PLUGIN_ROOT}/references/briefing-config.md` first — it is the contract this skill writes against.

---

## Step 1 — Read what already exists

Before asking anything.

- Read `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/briefings.config.json`. If it is there, this is an **update**, not a first run, and the existing values are the defaults for every question.
- Call `mcp__claude-code-remote__list_triggers` and look for scheduled tasks already registered by this plugin. Match on name — `Commitment calendar`, `Morning brief`, `CRM sync health`. If one exists, note its id, cron, and enabled state.
- **Look for older hand-made tasks that do the same job under a different name.** A person who has been running one of these briefings from a hand-written scheduled task will end up with two tasks writing one file, which presents as a mystery rather than as a duplicate. Read the prompt of every enabled task, not just its name, and if one is clearly an earlier version of a briefing this plugin now owns, say so and offer to retire it. Do not delete it — deletion is the owner's call.

Announce what you found before you propose anything. A setup skill that asks a person to re-answer questions it could have read is a setup skill that will not be run twice.

## Step 2 — Resolve the config

Fill in what you can rather than asking for it:

- `owner.email` and `owner.name` — from the session's user context. Do not fabricate a name; if only an email is known, ask for the name rather than deriving one from the address.
- `owner.timezone` — from the session's stated timezone.
- `calendars.primary` — defaults to `owner.email`. Call `mcp__Google_Calendar__list_calendars` and show the real list, so `alsoCheck` and `expectedEmpty` are chosen from what exists instead of from memory.
- Everything else — the defaults in `briefing-config.md`.

Then ask, in one round, only about the things that cannot be derived:

- which of the listed calendars to also pull, and which are expected to be empty
- window length, if not 14
- any locally-anchored venues for location-clash detection, with address and city
- any senders or subject patterns that are newsletter or blast noise
- where the files should land, if not `~/Downloads`
- what times the briefings should arrive, in local time

## Step 2b — Resolve the work surfaces

The `surfaces` block decides how much of the owner's actual obligation set reaches the calendar. Defined in `${CLAUDE_PLUGIN_ROOT}/references/work-surfaces.md`; enabled here.

**Detect rather than interrogate.** Most of these can be answered by looking:

- which connectors are actually available in this session — a surface with no connector starts `off`, and setup says which and why
- the Jira cloud id and project from `getAccessibleAtlassianResources` and the visible projects
- the repositories from the project's own instructions or its surfaces file, when one exists
- decision-record and project-hygiene paths from the project's folder layout

Then show the owner the resolved surface table — surface, tier, and the parameters found — and ask only about the ones detection could not settle: which repositories, which competitor domains, which tracker file, and whether personal finance should be on at all. `personal` defaults to `off` and only moves on an explicit yes.

Say plainly what a `weekly` tier means before they accept it, and what a missing parameter means: **a surface with no parameters is reported as `not checked`, not as clean.** That is the sentence that stops a misconfigured surface from looking like good news for a month.

Two things worth telling them at this point, because they are the reason the sweep is safe to run wide:

- every surface is read-only, across the board — nothing in this plugin merges, sends, posts, pays, signs, or transitions anything
- a wide sweep costs time, which is what the tiers are for; the `always` set is the cheap high-yield core, and `--full` exists for the day the question is "what am I forgetting"

## Step 2c — Resolve the CRM health block, if that briefing is wanted

Only if the owner wants the CRM sync health check. It needs the Supabase project id, the schema, the list of pipeline sources, the two thresholds, and any known open issues.

Ask for the project id rather than discovering it — running a health check against the wrong database produces a confident, wrong answer, and this is the one place in the plugin where guessing has a real cost.

Offer to populate `crmHealth.baseline` by running the check once now. A baseline captured at setup is what lets every later run say *this changed* instead of reciting three numbers into the void.

Convert the local times to UTC cron yourself, and **show the conversion and the DST caveat**: `0 14 * * 1-5` is 7am Pacific on daylight time and 6am on standard time. The cron does not shift itself. Say which one they are choosing and that it drifts an hour twice a year.

## Step 3 — Show the config, then write it

Print the complete JSON that will be written, at the path it will be written to. Then get an explicit yes.

On yes, write it. On an update, write the merged document rather than a patch — read, apply, write the whole file — and say which keys changed.

If the vault is not mounted, request it before reading or writing. Do not write a config anywhere else as a fallback; a config the briefings cannot find is worse than no config, because the next run will silently use defaults.

## Step 4 — Show the scheduled tasks, then register them

Two tasks. For each, show the owner **the exact name, the exact cron, the resolved local time, and the exact prompt text** before creating anything.

Use `mcp__claude-code-remote__create_trigger`. Never `CronCreate` — that scheduler lives inside this session and dies with it, so anything it registers silently never runs.

**Commitment calendar**

- name: `Commitment calendar`
- `cron_expression`: `schedule.calendarCron`
- `notifications`: `schedule.notifications`
- prompt: a complete standalone instruction, because every firing is a fresh session with no memory of this one:

  > Run the `/commitment-calendar` skill from the `daily-briefings` plugin. This is an unattended scheduled run: work autonomously, do not ask clarifying questions, and do not offer connector suggestions. Read the owner config at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/briefings.config.json` and follow it. Build the window, sweep the inbox for dated commitments, detect the flags, render the self-contained HTML file, deliver it with SendUserFile, save it to the configured output path, and open it. Report in three or four sentences: what changed versus a normal day, any new clash, and any deadline now inside the window with no prep blocked. Name any source that could not be read.

**Morning brief**

- name: `Morning brief`
- `cron_expression`: `schedule.morningCron`
- `notifications`: `schedule.notifications`
- prompt:

  > Run the `/morning-brief` skill from the `daily-briefings` plugin. This is an unattended scheduled run: work autonomously, do not ask clarifying questions, and do not offer connector suggestions. Read the owner config at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/briefings.config.json` and follow it. Render today and tomorrow, what arrived overnight and still needs an answer, close deadlines, and today's flags, as one self-contained HTML page. Deliver it with SendUserFile, save it to the configured output path, and open it. Report in two or three sentences. Name any source that could not be read.

**CRM sync health** — only if `crmHealth` was configured in Step 2c.

- name: `CRM sync health`
- `cron_expression`: `schedule.crmHealthCron`
- `notifications`: `schedule.notifications`
- prompt:

  > Run the `/crm-sync-health` skill from the `daily-briefings` plugin. This is an unattended scheduled run: work autonomously and do not ask clarifying questions. Read the `crmHealth` block of the owner config at `MoxyWolf Vault/_Shared Knowledge/Agents and Plugins/briefings.config.json` for the project id, schema, pipeline sources, thresholds, known issues and baseline. Run the four checks, read each against the baseline, then make only the skill's two bookkeeping repairs (sweep running rows older than 2 hours; release a dead-lettered sync_tasks row at most once a day) and report them with counts. No other write, no code or config change, no direct sync-all call. If checks 1, 2 and 4 are clean, check 3 shows only known issues and nothing was repaired, reply in one line. Otherwise lead with the source name and check number, quote error_detail verbatim, and state plainly whether it is a known issue or something new. If the database could not be reached, say the pipeline state is unknown — never report an unreachable database as a healthy one.

**Idempotence.** If a task with that name already exists, `mcp__claude-code-remote__update_trigger` it — same id, same run history — rather than creating a second one. Two scheduled tasks writing the same file is a bug that presents as a mystery.

## Step 5 — Offer a dry run, then confirm

Offer to run `/commitment-calendar` once, immediately, so the first real output is seen while someone is around to say it is wrong. This is where a bad calendar id or an over-broad noise filter surfaces cheaply.

Then confirm in plain language: the config path, the two task names with their local times, and one line on how to change them later — this skill again, or the scheduled-tasks list.

---

## Boundaries

- **Nothing is created without the owner seeing it first.** The config JSON is shown in full before it is written; each scheduled task's name, cron, and prompt are shown in full before it is registered.
- **Never `CronCreate`.** Scheduled tasks go through `mcp__claude-code-remote__create_trigger` so they survive the session.
- **Never duplicate a task.** Read `list_triggers` first; update in place when the name matches.
- **Never write a credential into the config.** It holds no secrets. If one is ever needed, it goes in its own `.env` beside `github-pat.env` and the config holds only the variable name.
- **Never fabricate the owner's name.** Ask for it.
- Deleting a scheduled task is the owner's call, not this skill's. It may propose; it does not delete.
