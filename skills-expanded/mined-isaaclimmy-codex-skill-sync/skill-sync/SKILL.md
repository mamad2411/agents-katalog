---
name: skill-sync
description: Simple sync flow for installed SKILL.md skills and Codex plugins. Use when the user says /skill-sync, check skills, update skills, run all skill updates, map skill repos, refresh Codex plugins, or create weekly skill maintenance.
---

# Skill Sync

Source: https://github.com/catalystsystemslab/codex-skill-sync/tree/main/skill-sync

Keep installed skills and Codex plugins current. `doctor` is read-only setup
diagnostics. `check`, `update`, and `run all` all start the same inventory and
mapping flow.

## Language

Reply in the user's language by default.

- If the user writes in English, respond in English.
- If the user writes in Chinese, respond in Simplified Chinese.
- If the user mixes English and Chinese, use the dominant language.
- Keep commands, file paths, JSON keys, status values, and shell commands unchanged.
- Translate explanations, summaries, warnings, and recommendations.

Important label translations:

- Official / 官方
- Community / 社区
- Needs Setup / 需要设置
- `current` / 已是最新
- `update_available` / 有可用更新
- `updated` / 已更新
- `skipped` / 已跳过
- `failed` / 失败

## Start Here

For `check`, `update`, and `run all`, first list what is installed:

```bash
python3 <skill-dir>/scripts/update_codex_assets.py --inventory --json --report skill-update-report.json
```

Show the result as three groups. Translate internal JSON groups this way:

- `official` -> Official
- `non_official` -> Community
- `unmapped` -> Needs Setup

Blank repo means the source is not confirmed. Do not guess.

## Beginner Response Style

Most users do not know Git, JSON, branches, or subpaths.

When showing inventory:

- Explain each group in plain language.
- Do not show raw JSON unless the user asks.
- Recommend the safest next action.
- Ask one decision at a time.

When mapping:

- Say that public GitHub search may use the skill name and description.
- Never ask the user to edit JSON manually unless they choose advanced mode.
- If editing the manifest, preserve existing entries and only add confirmed
  mappings.
- Show exactly what will be saved before saving it.

Before apply:

- Summarize what will change.
- List skipped skills separately.
- Remind the user that backups will be created.
- Ask for explicit confirmation.

## Commands

For `doctor`:

1. Run read-only diagnostics.
2. Explain warnings in plain language.
3. Recommend the safest next action.

```bash
python3 <skill-dir>/scripts/update_codex_assets.py --doctor --report skill-doctor-report.json
```

For `check`:

1. Run inventory.
2. If Needs Setup has anything, ask whether to map repos now or skip mapping for
   this run.
3. If the user maps repos, save only confident matches.
4. Run a dry update check. Do not apply.

```bash
python3 <skill-dir>/scripts/update_codex_assets.py --json --report skill-update-report.json
```

For `update` or `run all`:

1. Run inventory.
2. If Needs Setup has anything, ask whether to map repos now or skip mapping for
   this run.
3. If the user maps repos, save only confident matches.
4. Show the repo list with blanks for uncertain repos.
5. Ask for update confirmation.
6. Apply updates.
7. After the first successful update, ask whether to create a weekly check
   automation.

```bash
python3 <skill-dir>/scripts/update_codex_assets.py --apply --json --report skill-update-report.json
```

## Mapping

Use `~/.codex/skill-sources.json` as the default saved mapping so the user does
not need to map the same skills again. If the user supplies another manifest,
use that instead.

Only confirmed repo mappings persist. If the user skips mapping for this run,
do not mark those skills local unless they explicitly say the skill is private
or local-only.

If the user chooses Map, public GitHub/web search is already part of the task.
Proceed with search tools and only ask again if the runtime blocks network
access or a repo match is uncertain.

Read `references/manifest.example.json` before editing a manifest.

For each Needs Setup skill:

- Search public GitHub first. Use the exact skill name plus unique words from
  its frontmatter or heading.
- Prefer the upstream public repo with strong evidence: exact `SKILL.md`
  match, same description/name, active repo, and visible community use such as
  stars.
- Do not map Needs Setup skills to `catalystsystemslab/<skill>`,
  `isaaclim/<skill>`, or another user/org mirror unless the installed skill
  itself names that repo as its source or the user confirms it.
- Trust a repo only when it contains that skill's `SKILL.md` at the repo root or
  a clear subfolder.
- Save confirmed matches with `url`, `branch`, and `subpath`.
- If unsure, leave the repo blank or ask the user for the link.
- Mark private/local skills as local:

```json
{ "name": "my-private-skill", "root": "~/.codex/skills", "kind": "local" }
```

## Status Words

- `current`: already okay.
- `update_available`: update found, not applied yet.
- `updated`: replaced after backup.
- `skipped: unknown source`: needs a repo link or local marking.
- `failed`: inspect network, auth, branch, or subpath.

## Safety

- Default to dry-run unless the user clearly asks to update.
- Back up before replacing a skill folder.
- Never overwrite Needs Setup skills.
- Do not migrate a skill to a similar repo without confirmation.
- The script replaces whole skill folders; it does not merge local edits.
- Unsafe remote skill trees must be reported as failed and never installed.
- Do not ask the user to override unsafe symlink or size failures.
- Codex plugin updates are Codex-only.

## Automation

Offer weekly check automation only after a successful update. Weekly is the
default; bi-weekly is fine for stable setups.

Weekly automation must default to dry-run check mode. Do not create an
automation that runs `--apply` unless the user explicitly asks for automatic
updates and confirms they understand it will replace mapped skill folders.
