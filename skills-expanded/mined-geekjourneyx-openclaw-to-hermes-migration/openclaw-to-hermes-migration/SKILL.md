---
name: openclaw-to-hermes-migration
description: Use this skill whenever the user wants to migrate from OpenClaw to Hermes Agent, upgrade an OpenClaw workspace into Hermes, preserve skills/memory/cron/messaging/provider settings, debug Feishu or Weixin gateway issues after migration, or validate that Hermes is ready to replace OpenClaw. This skill is especially relevant for requests mentioning OpenClaw, Hermes Agent, `hermes claw migrate`, Feishu/Lark, Weixin/WeChat, model providers, API keys, cron jobs, gateway services, or “确保迁移成功”.
---

# OpenClaw to Hermes Migration

This skill turns an OpenClaw installation into a verified Hermes Agent installation without losing identity, memory, skills, model settings, messaging access, or scheduled automation intent.

Use a conservative migration posture: freeze the source, dry-run first, migrate user data before secrets, validate each capability, then start Hermes gateway only after OpenClaw gateway is stopped.

## Core Principles

- Treat migration as state transfer, not file copying. Preserve behavior: identity, memory, execution defaults, skills, messaging, model auth, and automation.
- Do not print secrets. Report secret presence as booleans or key names only.
- Keep OpenClaw available until Hermes passes acceptance checks.
- Do not run two gateways against the same bot/app/session token.
- Prefer `--preset user-data` first. Migrate secrets only after the dry-run proves it will not duplicate or overwrite unrelated state.
- Keep the original workspace path during cutover if memories, skills, or cron prompts reference it.

## Inputs To Identify

Ask or infer:

- OpenClaw home, usually `~/.openclaw`.
- Hermes home, usually `~/.hermes`.
- Target workspace, often `~/.openclaw/workspace` during initial cutover.
- Required messaging platforms: Feishu/Lark, Weixin/WeChat, Telegram, Discord, etc.
- Desired model provider: z.ai/BigModel, OpenRouter, Gemini, Anthropic, custom OpenAI-compatible endpoint, or another supported provider.
- Whether secrets may be migrated or must be manually re-entered.
- Whether cron jobs should be recreated immediately, paused, or left archived.

## Bundled Resources

- Read `references/migration-session-summary.md` only when you need a concrete prior migration example, known Hermes/OpenClaw paths, Feishu/z.ai troubleshooting notes, or a record of commands that worked in one real migration.
- Use `evals/evals.json` when changing this skill to check that the SOP still covers safe migration, Feishu debugging, provider replacement, and cron generalization.

## Phase 1: Freeze OpenClaw

Before migrating, stop active OpenClaw writers. Runtime files can otherwise change during checksum capture.

```bash
systemctl --user is-active openclaw-gateway.service || true
systemctl --user stop openclaw-gateway.service
lsof +D ~/.openclaw 2>/dev/null | head -80 || true
```

If OpenClaw is not systemd-managed, inspect processes:

```bash
ps -eo pid,ppid,etime,cmd | grep -Ei 'openclaw|weixin|wechat|feishu|hermes' | grep -v grep || true
```

Only stop confirmed OpenClaw runtime components. Do not kill generic `node`, `python`, or shell processes without proving they own OpenClaw files.

Capture a manifest:

```bash
mkdir -p /tmp/openclaw-migration
find ~/.openclaw -type f | sort > /tmp/openclaw-migration/source-files.txt
find ~/.openclaw -type f -print0 | sort -z | xargs -0 sha256sum > /tmp/openclaw-migration/source-sha256.txt
```

Capture a non-secret summary:

```bash
{
  echo "date_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "openclaw_size=$(du -sh ~/.openclaw | awk '{print $1}')"
  echo "workspace_files=$(find ~/.openclaw/workspace -type f 2>/dev/null | wc -l)"
  echo "main_sessions_glob=~/.openclaw/agents/main/sessions/*.jsonl"
  echo "main_sessions=$(find ~/.openclaw/agents/main/sessions -type f -name '*.jsonl' 2>/dev/null | wc -l)"
  echo "global_skills=$(find ~/.openclaw/skills -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)"
  echo "workspace_skills=$(find ~/.openclaw/workspace/skills -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)"
  echo "cron_jobs=$(jq '.jobs | length' ~/.openclaw/cron/jobs.json 2>/dev/null || echo 0)"
  jq -c '{top_keys: keys, channels: (.channels // {} | keys), providers: (.models.providers // {} | keys), default_workspace: .agents.defaults.workspace}' ~/.openclaw/openclaw.json
} > /tmp/openclaw-migration/source-summary.txt
touch /tmp/openclaw-migration/source-summary.txt
find ~/.openclaw -type f -newer /tmp/openclaw-migration/source-summary.txt -print
```

Proceed only when the newer-file check is empty, or when the user explicitly accepts online migration risk.

## Phase 2: Install Hermes

Install from the official script:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
command -v hermes
hermes doctor
```

If the installer exits after creating Hermes because setup wizard cannot open `/dev/tty`, verify with `command -v hermes` and `hermes doctor`. A no-TTY wizard failure is not a blocker if the CLI, config, venv, and directories exist.

## Phase 3: Dry-Run Migration

Run a safe preview:

```bash
hermes claw migrate \
  --source ~/.openclaw \
  --workspace-target ~/.openclaw/workspace \
  --preset user-data \
  --skill-conflict rename \
  --overwrite \
  --dry-run
```

Inspect:

- `Would migrate`: `soul`, `workspace-agents`, `memory`, `user-profile`, `model-config`, `agent-config`, skills, custom providers.
- `Skipped`: messaging settings, raw config, sensitive runtime data, cron jobs, provider keys.
- `Conflicts`: should be resolved by `--overwrite` for template files and `--skill-conflict rename` for duplicate skills.

If Hermes reports OpenClaw PIDs during dry-run, verify independently:

```bash
ps -fp <pid-list> || true
systemctl --user is-active openclaw-gateway.service || true
lsof +D ~/.openclaw 2>/dev/null | head -80 || true
```

Migration detector warnings can be transient if it matches command lines containing `openclaw`. Do not ignore the warning until service state and open files are checked.

## Phase 4: Execute User-Data Migration

Execute only after dry-run is clean:

```bash
hermes claw migrate \
  --source ~/.openclaw \
  --workspace-target ~/.openclaw/workspace \
  --preset user-data \
  --skill-conflict rename \
  --overwrite \
  --yes
```

Validate:

```bash
test -s ~/.hermes/SOUL.md
test -s ~/.hermes/memories/MEMORY.md
test -s ~/.hermes/memories/USER.md
test -d ~/.hermes/skills/openclaw-imports
hermes skills list
hermes doctor
```

Review the migration report:

```bash
find ~/.hermes/migration/openclaw -maxdepth 3 -type f | sort | tail -80
sed -n '1,180p' ~/.hermes/migration/openclaw/<timestamp>/summary.md
```

## Phase 5: Provider Migration

After user data is migrated, wire the desired provider. Avoid assuming the source has any particular provider, and avoid leaving obsolete provider entries that the user no longer wants.

### General Provider Cleanup Pattern

Use this pattern when the user wants to replace one provider with another:

1. Identify source providers and credentials without printing values.
2. Confirm the target provider and model ID.
3. Back up `~/.hermes/.env` and `~/.hermes/config.yaml`.
4. Add the target provider key to `~/.hermes/.env`.
5. Remove only provider env vars and `custom_providers` entries that the user explicitly wants removed.
6. Update `model.default`, `model.provider`, `model.base_url`, and `model.api_key` to the target provider.
7. Validate with `hermes config check`, `hermes doctor`, and a one-shot `hermes chat` smoke test.

Non-secret discovery commands:

```bash
jq '{default_model: .agents.defaults.model, provider_names: (.models.providers // {} | keys)}' ~/.openclaw/openclaw.json
python3 - <<'PY'
import json
from pathlib import Path
p = Path("~/.openclaw/agents/main/agent/auth-profiles.json").expanduser()
if p.exists():
    data = json.loads(p.read_text())
    print("auth_profiles=", sorted(data.get("profiles", {}).keys()))
PY
```

### Generic OpenAI-Compatible Provider Template

Use this when the target provider exposes an OpenAI-compatible chat completions endpoint. Replace placeholder values and remove old providers only when explicitly requested:

```bash
TARGET_PROVIDER="provider-name"
TARGET_MODEL="provider-name/model-id"
TARGET_BASE_URL="https://provider.example.com/v1"
TARGET_API_KEY_ENV="PROVIDER_API_KEY"
export TARGET_PROVIDER TARGET_MODEL TARGET_BASE_URL TARGET_API_KEY_ENV

python3 - <<'PY'
import os
from pathlib import Path
import yaml

provider = os.environ["TARGET_PROVIDER"]
model = os.environ["TARGET_MODEL"]
base_url = os.environ["TARGET_BASE_URL"]
api_key_env = os.environ["TARGET_API_KEY_ENV"]
config = Path("~/.hermes/config.yaml").expanduser()
env_file = Path("~/.hermes/.env").expanduser()
backup = config.with_name(config.name + f".bak-before-{provider}")

if not config.exists():
    raise SystemExit("Hermes config.yaml not found; run hermes doctor/setup first.")
env_has_key = os.environ.get(api_key_env) or (
    env_file.exists() and any(line.startswith(api_key_env + "=") for line in env_file.read_text().splitlines())
)
if not env_has_key:
    raise SystemExit(f"{api_key_env} is not set; add it to ~/.hermes/.env or export it before configuring.")
if not backup.exists():
    backup.write_text(config.read_text())

cfg = yaml.safe_load(config.read_text()) or {}
cfg.setdefault("model", {})
cfg["model"].update({
    "default": model,
    "provider": "auto",
    "base_url": base_url,
    "api_key": "${" + api_key_env + "}",
})

remove_provider_names = set()  # Fill only with user-approved removals.
providers, found = [], False
for item in cfg.get("custom_providers") or []:
    if not isinstance(item, dict) or item.get("name") in remove_provider_names:
        continue
    if item.get("name") == provider:
        item.update({"base_url": base_url, "api_key": "${" + api_key_env + "}", "api_mode": "chat_completions"})
        found = True
    providers.append(item)
if not found:
    providers.append({"name": provider, "base_url": base_url, "api_key": "${" + api_key_env + "}", "api_mode": "chat_completions"})
cfg["custom_providers"] = providers
config.write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False))
print(f"{provider} configured.")
PY
```

### Example: z.ai / BigModel Domestic Endpoint

If OpenClaw stores z.ai auth profiles:

```bash
python3 - <<'PY'
import json
from pathlib import Path

src = Path("~/.openclaw/agents/main/agent/auth-profiles.json").expanduser()
env = Path("~/.hermes/.env").expanduser()
backup = env.with_name(env.name + ".bak-before-zai")

if not src.exists():
    raise SystemExit("No OpenClaw auth-profiles.json found; set ZAI_API_KEY manually.")
data = json.loads(src.read_text())
profile = data.get("profiles", {}).get("zai:default")
if not profile or not profile.get("key"):
    raise SystemExit("No zai:default key found; set ZAI_API_KEY manually.")
key = profile["key"]

if env.exists() and not backup.exists():
    backup.write_text(env.read_text())

lines = env.read_text().splitlines() if env.exists() else []
out, seen = [], False
for line in lines:
    if line.startswith("ZAI_API_KEY="):
        out.append(f"ZAI_API_KEY={key}")
        seen = True
    else:
        out.append(line)
if not seen:
    out.append(f"ZAI_API_KEY={key}")
env.write_text("\n".join(out).rstrip() + "\n")
print("ZAI_API_KEY configured.")
PY
```

Update `~/.hermes/config.yaml`:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml

path = Path("~/.hermes/config.yaml").expanduser()
backup = path.with_name(path.name + ".bak-before-zai")

if not path.exists():
    raise SystemExit("Hermes config.yaml not found; run hermes doctor/setup first.")
if not backup.exists():
    backup.write_text(path.read_text())

cfg = yaml.safe_load(path.read_text()) or {}
cfg.setdefault("model", {})
cfg["model"]["default"] = "zai/glm-5-turbo"
cfg["model"]["provider"] = "auto"
cfg["model"]["base_url"] = "https://open.bigmodel.cn/api/coding/paas/v4"
cfg["model"]["api_key"] = "${ZAI_API_KEY}"

remove_provider_names = set()  # Example: {"old-provider"} only when user asked to remove it.
providers, found = [], False
for item in cfg.get("custom_providers") or []:
    if not isinstance(item, dict):
        continue
    if item.get("name") in remove_provider_names:
        continue
    if item.get("name") == "zai":
        item["base_url"] = "https://open.bigmodel.cn/api/coding/paas/v4"
        item["api_key"] = "${ZAI_API_KEY}"
        item["api_mode"] = "chat_completions"
        found = True
    providers.append(item)
if not found:
    providers.append({
        "name": "zai",
        "base_url": "https://open.bigmodel.cn/api/coding/paas/v4",
        "api_key": "${ZAI_API_KEY}",
        "api_mode": "chat_completions",
    })
cfg["custom_providers"] = providers
path.write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False))
print("z.ai provider configured.")
PY
```

Validate:

```bash
hermes config check
hermes doctor
timeout 90 hermes chat -q '只回复 OK' --provider zai -m zai/glm-5-turbo -Q --max-turns 1 --ignore-rules
```

Expected: `hermes doctor` shows `✓ Z.AI / GLM`, and the smoke test returns `OK`.

If the user asks to remove a specific old provider, remove that provider explicitly. For example, to remove `old-provider`, delete its env var from `~/.hermes/.env` and add the provider name to `remove_provider_names`. Do not remove providers just because they were present in the source.

## Phase 6: Feishu / Lark Migration

Hermes supports Feishu/Lark gateway even if `hermes gateway --help` text is incomplete. Prefer WebSocket mode to avoid public webhook setup.

Migrate OpenClaw Feishu config. This script is intentionally safe to run when Feishu was not configured; it exits without changing Hermes.

```bash
python3 - <<'PY'
import json
from pathlib import Path

openclaw_path = Path("~/.openclaw/openclaw.json").expanduser()
env = Path("~/.hermes/.env").expanduser()
backup = env.with_name(env.name + ".bak-before-feishu")

if not openclaw_path.exists():
    raise SystemExit("No ~/.openclaw/openclaw.json found; skipping Feishu migration.")
openclaw = json.loads(openclaw_path.read_text())
feishu = (openclaw.get("channels") or {}).get("feishu")
if not isinstance(feishu, dict) or not feishu.get("appId") or not feishu.get("appSecret"):
    raise SystemExit("No complete OpenClaw Feishu config found; skipping Feishu migration.")

allow_path = Path("~/.openclaw/credentials/feishu-default-allowFrom.json").expanduser()
allow = json.loads(allow_path.read_text()) if allow_path.exists() else {}
allowed = allow.get("allowFrom", [])

updates = {
    "FEISHU_APP_ID": feishu.get("appId", ""),
    "FEISHU_APP_SECRET": feishu.get("appSecret", ""),
    "FEISHU_DOMAIN": "feishu",
    "FEISHU_CONNECTION_MODE": feishu.get("connectionMode", "websocket"),
    "FEISHU_GROUP_POLICY": feishu.get("groupPolicy", "allowlist"),
}
if isinstance(allowed, list) and allowed:
    updates["FEISHU_ALLOWED_USERS"] = ",".join(str(x) for x in allowed)

if env.exists() and not backup.exists():
    backup.write_text(env.read_text())
lines = env.read_text().splitlines() if env.exists() else []
out, seen = [], set()
for line in lines:
    if "=" in line and not line.lstrip().startswith("#"):
        key = line.split("=", 1)[0]
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
            continue
    out.append(line)
for key, value in updates.items():
    if key not in seen and value:
        out.append(f"{key}={value}")
env.write_text("\n".join(out).rstrip() + "\n")
print("Feishu config migrated.")
PY
```

Start in foreground for first test:

```bash
hermes gateway run --accept-hooks
```

Then install as a service:

```bash
hermes gateway install
hermes gateway start
hermes gateway status
journalctl --user -u hermes-gateway -f
```

If messages arrive but no reply:

```bash
journalctl --user -u hermes-gateway --since '10 minutes ago' --no-pager
```

Common Feishu issues:

- `Unauthorized user: <id>`: add that sender ID to `FEISHU_ALLOWED_USERS`, then `hermes gateway restart`.
- `Access denied ... im:chat:readonly`: open the Feishu developer console and grant `im:chat:readonly` or equivalent chat read scope.
- Group message ignored: the bot usually requires an explicit @mention in groups; check `FEISHU_GROUP_POLICY`.
- Card approval button errors: enable interactive card capability and subscribe to `card.action.trigger`.

## Phase 7: Weixin / WeChat Migration

Hermes supports personal Weixin via iLink Bot API. It is different from WeCom.

If OpenClaw has account files, migrate the first account file. This script exits without changing Hermes when no account exists.

```bash
python3 - <<'PY'
import json
from pathlib import Path

accounts_dir = Path("~/.openclaw/openclaw-weixin/accounts").expanduser()
env = Path("~/.hermes/.env").expanduser()
backup = env.with_name(env.name + ".bak-before-weixin")

if not accounts_dir.exists():
    raise SystemExit("No OpenClaw Weixin accounts directory found; skipping Weixin migration.")
accounts = sorted(accounts_dir.glob("*-im-bot.json"))
if not accounts:
    raise SystemExit("No OpenClaw Weixin account files found; skipping Weixin migration.")

account_file = accounts[0]
data = json.loads(account_file.read_text())
if not data.get("token") or not data.get("baseUrl"):
    raise SystemExit(f"{account_file} is missing token/baseUrl; skipping Weixin migration.")
updates = {
    "WEIXIN_ACCOUNT_ID": account_file.stem,
    "WEIXIN_TOKEN": data.get("token", ""),
    "WEIXIN_BASE_URL": data.get("baseUrl", ""),
    "WEIXIN_DM_POLICY": "open",
    "WEIXIN_GROUP_POLICY": "disabled",
}

if env.exists() and not backup.exists():
    backup.write_text(env.read_text())
lines = env.read_text().splitlines() if env.exists() else []
out, seen = [], set()
for line in lines:
    if "=" in line and not line.lstrip().startswith("#"):
        key = line.split("=", 1)[0]
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
            continue
    out.append(line)
for key, value in updates.items():
    if key not in seen and value:
        out.append(f"{key}={value}")
env.write_text("\n".join(out).rstrip() + "\n")
print("Weixin config migrated.")
PY
```

If the session is expired, run:

```bash
hermes gateway setup
```

Select Weixin and scan the QR code.

## Phase 8: Cron Jobs

OpenClaw cron is often archived rather than directly migrated. Never assume `jobs[0]` is the only job. Inspect all archived jobs first:

```bash
jq '.jobs[] | {id, name, enabled, schedule, delivery, state, payload_keys: (.payload | keys)}' ~/.hermes/migration/openclaw/<timestamp>/archive/cron-store/jobs.json
```

Generate reviewable recreate commands for every job. This does not execute anything:

```bash
CRON_ARCHIVE=~/.hermes/migration/openclaw/<timestamp>/archive/cron-store/jobs.json python3 - <<'PY'
import json, os, shlex
from pathlib import Path

path = Path(os.environ["CRON_ARCHIVE"]).expanduser()
data = json.loads(path.read_text())

def schedule_to_cli(value):
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, dict):
        for key in ("expression", "cron", "schedule"):
            if isinstance(value.get(key), str) and value[key].strip():
                return value[key].strip()
        minutes = value.get("intervalMinutes") or value.get("interval_minutes")
        if minutes:
            return f"every {int(minutes)}m"
        seconds = value.get("intervalSeconds") or value.get("interval_seconds")
        if seconds and int(seconds) % 60 == 0:
            return f"every {int(seconds) // 60}m"
    return None

def prompt_from(job):
    payload = job.get("payload") or {}
    for key in ("message", "prompt", "task", "instruction", "text"):
        value = payload.get(key) or job.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None

for index, job in enumerate(data.get("jobs") or [], 1):
    schedule = schedule_to_cli(job.get("schedule"))
    prompt = prompt_from(job)
    if not schedule or not prompt:
        print(f"# SKIP job {index}: missing schedule or prompt; inspect manually")
        continue
    name = job.get("name") or job.get("id") or f"openclaw-cron-{index}"
    delivery = job.get("delivery") or job.get("deliver") or "local"
    if not isinstance(delivery, str) or delivery in {"", "auto", "origin"}:
        delivery = "local"
    skills = job.get("skills") or (job.get("payload") or {}).get("skills") or []
    if isinstance(skills, str):
        skills = [skills]
    args = ["hermes", "cron", "create", schedule, prompt, "--name", str(name), "--deliver", delivery]
    for skill in skills:
        args += ["--skill", str(skill)]
    print(shlex.join(args))
    print("# After creation, immediately run: hermes cron pause <new-job-id>")
PY
```

Recreate selected jobs one by one, then pause each created job before enabling the next. Use the id printed by `hermes cron create`; if the CLI output is unclear, run `hermes cron list --all` and pause the new id before creating more jobs.

```bash
hermes cron create "<schedule>" "<prompt>" --name "<name>" --deliver local
hermes cron list --all
hermes cron pause <new-job-id>
hermes cron list --all
```

Pause cron until model auth and delivery channel are proven.

## Acceptance Checklist

Migration is not complete until:

- `hermes doctor` has no blocking install/config issues.
- `SOUL.md`, `MEMORY.md`, and `USER.md` exist in `~/.hermes`.
- `hermes skills list` shows imported skills under `openclaw-imports`.
- The desired provider passes a real smoke test.
- The messaging gateway connects and responds to a real user message.
- Old OpenClaw gateway is stopped.
- Cron jobs are either recreated and paused, or intentionally deferred with a written reason.
- The migration report under `~/.hermes/migration/openclaw/<timestamp>/` is reviewed.

## Rollback

Keep rollback simple:

```bash
hermes gateway stop || true
systemctl --user start openclaw-gateway.service
```

If Hermes state must be set aside:

```bash
mv ~/.hermes ~/.hermes.failed-$(date -u +%Y%m%dT%H%M%SZ)
```

Do not run OpenClaw cleanup until Hermes has survived at least one real work session.
