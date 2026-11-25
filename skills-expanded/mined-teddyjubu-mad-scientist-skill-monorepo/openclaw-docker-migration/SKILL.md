---
name: openclaw-docker-migration
description: Migrate OpenClaw to Hermes when OpenClaw runs inside Docker (no host ~/.openclaw). Covers data extraction from Docker, running the migration script, verifying coexistence, and porting custom skills. Use when a VPS has OpenClaw containerized and the user wants Hermes alongside or instead.
version: 1.0.0
tags: [openclaw, migration, docker, hermes, coexistence]
---

# OpenClaw Docker Migration + Coexistence

Use this skill when OpenClaw is running inside a Docker container on a VPS and
`~/.openclaw` is empty or missing on the host. The standard migration script
(`hermes claw migrate`) expects `~/.openclaw` on the host — this skill covers
the pre-flight to make that work, plus coexistence setup if both systems stay running.

## What This Skill Does

This skill Migrate OpenClaw to Hermes when OpenClaw runs inside Docker (no host ~/.openclaw). Covers data extraction from Docker, running the migration script, verifying coexistence, and porting custom skills. Use when a VPS has OpenClaw containerized and the user wants Hermes alongside or instead.

## Step 1 — Find the container and confirm data

```bash
docker ps -a --format "{{.Names}}"
# Look for something like openclaw-mm3f-openclaw-1 or missioncontrol-app

docker exec <container> find / -maxdepth 4 -name ".openclaw" -type d 2>/dev/null
# Expect: /data/.openclaw
```

## Step 2 — Seed ~/.openclaw on the host

Do NOT `docker cp <container>:/data/.openclaw /root/.openclaw` on a live
workspace — it will time out (workspace can be several GB).
Always tar inside the container first, then copy the single archive.

```bash
mkdir -p ~/.openclaw/workspace

# Core memory/persona files (fast individual copies)
docker cp <container>:/data/.openclaw/workspace/MEMORY.md ~/.openclaw/workspace/
docker cp <container>:/data/.openclaw/workspace/SOUL.md   ~/.openclaw/workspace/
docker cp <container>:/data/.openclaw/workspace/USER.md   ~/.openclaw/workspace/ 2>/dev/null || true
docker cp <container>:/data/.openclaw/workspace/AGENTS.md ~/.openclaw/workspace/ 2>/dev/null || true

# Skills directory — tar first, then copy
docker exec <container> tar -czf /tmp/oc-skills.tar.gz \
    -C /data/.openclaw/workspace skills
docker cp <container>:/tmp/oc-skills.tar.gz /tmp/oc-skills.tar.gz
tar -xzf /tmp/oc-skills.tar.gz -C ~/.openclaw/workspace/
rm /tmp/oc-skills.tar.gz
```

## Step 3 — Run dry run, then migrate

```bash
python3 ~/.hermes/hermes-agent/optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py
# Review output, then execute:
python3 ~/.hermes/hermes-agent/optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py \
    --execute --preset full --migrate-secrets --skill-conflict rename --overwrite
```

Follow the interactive decisions in the SKILL.md for that script (soul conflict,
skill conflicts, workspace instructions, migration mode).

## Step 4 — Fix post-migration issues

After migration, check and fix these known issues:

### MESSAGING_CWD points to Docker path
The migration copies `/data/.openclaw/workspace` from openclaw.json — that path
only exists inside the container, not on the host.

```bash
grep MESSAGING_CWD ~/.hermes/.env
# If it shows /data/.openclaw/workspace, fix it:
sed -i 's|^MESSAGING_CWD=.*|MESSAGING_CWD=/root|' ~/.hermes/.env
```

### ANTHROPIC_API_KEY is an OpenClaw portal key
OpenClaw portal keys start with `sk-cp-`. They will fail `hermes doctor`'s
direct Anthropic check. This is harmless — Hermes uses OpenRouter as primary
provider. Tell the user to ignore it or set a real `sk-ant-` key if they want
direct Anthropic access.

### Model ID has wrong prefix after migration
The migration copies the OpenClaw model string (e.g. `openrouter/anthropic/claude-opus-4.6`)
verbatim into Hermes config. Hermes on the OpenRouter provider expects the ID
WITHOUT the `openrouter/` prefix. Symptom: Telegram bot replies with
`HTTP 400 — not a valid model ID`.

Fix:
```bash
hermes config set model.default anthropic/claude-sonnet-4.6
hermes gateway restart
```

Use `claude-sonnet-4.6` rather than `claude-opus-4.6` as the default —
same quality for everyday conversation, lower API cost. Opus is available
for explicit heavy-lifting tasks via `/model`.

### USER.md is empty template after migration
The migration script copies MEMORY.md entries but leaves USER.md as the
default blank template. Populate it immediately after migration with everything
known about the user so context carries across sessions:

```bash
cat > ~/.hermes/memories/USER.md << 'EOF'
Name: <name>
§
What to call them: <name>
§
Timezone: <tz>
§
Notes: <communication preferences, technical level>
§
Context: <background, business, projects, tools>
§
Context: <preferences, pet peeves, style>
EOF
```

## Step 5 — Coexistence verification (if keeping both)

If the user wants OpenClaw and Hermes running simultaneously, do NOT run
`hermes claw cleanup`. Instead verify:

```bash
# 1. Port conflict check — OpenClaw owns 18789, Hermes uses separate mechanism
ss -tlnp | grep 18789
# Should show openclaw-gateway only

# 2. Telegram token conflict
HERMES_TG=$(grep "^TELEGRAM_BOT_TOKEN=" ~/.hermes/.env | cut -d= -f2)
OC_TG=$(python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); \
    print(d.get('channels',{}).get('telegram',{}).get('accounts',{}).get('default',{}).get('botToken',''))")
[ "$HERMES_TG" = "$OC_TG" ] && echo "CONFLICT: same token" || echo "OK: different tokens"

# 3. Discord token conflict (same pattern)
HERMES_DS=$(grep "^DISCORD_BOT_TOKEN=" ~/.hermes/.env | cut -d= -f2)
OC_DS=$(python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); \
    print(d.get('channels',{}).get('discord',{}).get('token',''))")
[ "$HERMES_DS" = "$OC_DS" ] && echo "CONFLICT: same token" || echo "OK: different tokens"
```

If tokens conflict, one system needs a different bot. This is a user decision —
do not auto-resolve.

## Step 6 — Port custom OpenClaw skills to Hermes

The migration script copies skills from `~/.openclaw/workspace/skills/` but
on Docker setups the custom skills may still only be inside the container.
Port them individually using tar (bulk docker cp of skill dirs can hit tool
call limits in a loop):

```bash
mkdir -p ~/.hermes/skills/openclaw-imports

for skill in gohighlevel-api rei-ai-weekly-newsletter homedepot-repair-estimator \
             census-data rentcast-property-report copywriting sarah-outbound-caller \
             hr-hiring firecrawl apify-actor-finder yt-thumbnail-creator \
             content-repurposing-engine graphic-design seo-audit beautiful-websites \
             nova-youtube-agent youtube-opus-skill gemini-image-editor firehose; do
    docker exec <container> tar -czf /tmp/skill-${skill}.tar.gz \
        -C /data/.openclaw/workspace/skills ${skill} 2>/dev/null || continue
    docker cp <container>:/tmp/skill-${skill}.tar.gz /tmp/skill-${skill}.tar.gz
    tar -xzf /tmp/skill-${skill}.tar.gz -C ~/.hermes/skills/openclaw-imports/
    docker exec <container> rm /tmp/skill-${skill}.tar.gz
    rm -f /tmp/skill-${skill}.tar.gz
    echo "Installed: $skill"
done
```

If doing this programmatically (execute_code), process one skill at a time in
the loop — bulk parallel runs hit the 50-tool-call cap mid-loop and leave
partial results.

## Step 7 — Initialize skills hub and install hub skills

```bash
# This seeds the hub cache
hermes skills list

# Recommended hub installs for a VPS with Docker:
echo y | hermes skills install official/devops/docker-management
echo y | hermes skills install official/email/agentmail
```

## Verification checklist

```bash
hermes doctor          # All green except optional items
hermes config          # Model, Telegram, Discord configured
hermes gateway status  # Running, systemd-enabled
hermes skills list     # openclaw-imports category visible
cat ~/.hermes/memories/MEMORY.md   # Migration memories present
cat ~/.hermes/SOUL.md              # Persona migrated
```

## Pitfalls

- `docker cp` of full workspace always times out on live OpenClaw instances. Use tar-in-container pattern.
- Skills loop using execute_code hits 50-tool-call cap. Split into batches of ~12.
- `hermes claw cleanup` renames `~/.openclaw` to `.openclaw.pre-migration` — skip this if coexistence is desired.
- The migration script's `--execute` flag with `--overwrite` will replace SOUL.md. Back up first if the existing Hermes SOUL.md has custom content (the script backs it up automatically).
- Check MESSAGING_CWD after every migration from a Docker-based OpenClaw — it always migrates the container-internal path.
- Model ID will always have the wrong `openrouter/` prefix after migration — fix it before the user tries Telegram.
- USER.md is always a blank template after migration — populate it manually with known user context before finishing.
- Telegram pairing codes expire quickly. If the user tries to pair, approves too slowly, and the code is gone — just have them send `/start` again to get a new code, then approve immediately with `hermes pairing approve telegram <CODE>`.
