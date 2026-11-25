---
name: hermes-admin-inspection
description: "Inspect, verify, and troubleshoot Hermes Agent installation state — profiles, memory files, database integrity, configuration, and session logs."
version: 1.0.0
author: Chief
category: devops
license: MIT
platforms: [linux, macos, windows]
tags: [devops, administration, inspection, troubleshooting, profile-management]
tested: schema-only
tested_note: Frontmatter and docs validated; author is a persona label and needs manual attribution review.
metadata:
  hermes:
    tags: [devops, administration, inspection, troubleshooting, profile-management]
    related_skills: [memory-wiki-health, kanban-orchestrator, systematic-debugging]
---

# Hermes Admin Inspection

Inspect, verify, and troubleshoot Hermes Agent installation state — profiles, memory files, database integrity, configuration, and session logs.

## When to use

- Verifying multi-profile setups and memory isolation
- Auditing storage consumption (sessions, memory files, SQLite DB size)
- Debugging profile corruption or missing files
- Understanding Hermes file layout across `~/.hermes/`, `~/.local/`, and per-profile homes
- Checking installation health before/after upgrades
- Answering "where is X stored?" for profiles, memories, cron, sessions
- Comparing memory/session counts across profiles
- Validating that memory files, souls, and databases are present and non-empty

## Core principle

Hermes uses **per-profile isolation**:
- Each profile lives in `~/.hermes/profiles/<profile-name>/`
- Each profile has its own: `sessions/`, `skills/`, `memories/`, `state.db`, `memory_store.db`
- Active profile's HOME is symlinked/evaluated into a nested path (e.g., `profiles/chief/home/.hermes/`)
- Global storage (cron jobs, logs, models cache) may live in the active profile's root or `~/.local/`

## Procedure

### 1. Profile inventory (system-wide)

```bash
# List all profiles
ls -1 ~/.hermes/profiles/

# Per-profile summary table
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  sessions=$(ls -1 "$p/sessions" 2>/dev/null | wc -l)
  skills=$(ls -1 "$p/skills" 2>/dev/null | wc -l)
  echo "[$name] sessions=$sessions skills=$skills"
done
```

### 2. Active profile deep-dive

```bash
# Inspect the active profile (usually 'chief')
PROFILE="${1:-chief}"
PROFILE_DIR=~/.hermes/profiles/$PROFILE

echo "=== $PROFILE_DIR ==="
ls -la "$PROFILE_DIR"
echo -e "\n=== memories/ ==="
ls -la "$PROFILE_DIR/memories/"
echo -e "\n=== sessions/ (first 10) ==="
ls -1 "$PROFILE_DIR/sessions" | head -10
echo -e "\n=== skills/ ==="
ls -1 "$PROFILE_DIR/skills"
```

### 3. Memory file contents

```bash
PROFILE="${1:-chief}"
for file in MEMORY.md USER.md SOUL.md; do
  path="$PROFILE_DIR/memories/$file"
  if [[ -f "$path" ]]; then
    echo -e "\n--- $file ($(wc -c < "$path") bytes) ---"
    cat "$path"
  fi
done
```

### 4. Database health & size

```bash
PROFILE="${1:-chief}"
PROFILE_DIR=~/.hermes/profiles/$PROFILE

echo "=== state.db ==="
du -h "$PROFILE_DIR/state.db"
echo "=== memory_store.db ==="
du -h "$PROFILE_DIR/memory_store.db"

# Row counts (requires sqlite3)
if command -v sqlite3 &>/dev/null; then
  echo -e "\nstate.db sessions: $(sqlite3 "$PROFILE_DIR/state.db" 'SELECT COUNT(*) FROM sessions;')"
  echo "memory_store facts: $(sqlite3 "$PROFILE_DIR/memory_store.db" 'SELECT COUNT(*) FROM facts;')"
fi
```

### 5. Cross-profile memory diff

```bash
# Compare memory file sizes and char counts across all profiles
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  mem="$p/memories/MEMORY.md"
  if [[ -f "$mem" ]]; then
    size=$(wc -c < "$mem")
    chars=$(wc -m < "$mem")
    echo "[$name] MEMORY.md: $size bytes, $chars chars"
  fi
done
```

### 6. Installation health check

```bash
hermes doctor
```

## 7. Configuration file locations

Given the path evaluation quirk on macOS, configuration files may exist in two locations:

1. **Canonical location**: `~/.hermes/` (or `/Users/<user>/.hermes/`)
2. **Active profile evaluated location**: `~/.hermes/profiles/<active-profile>/home/.hermes/`

To ensure you find the correct configuration file, check both locations:

```bash
# Check canonical location first
if [ -f ~/.hermes/.env ]; then
  echo "Found .env in canonical location: ~/.hermes/.env"
  cat ~/.hermes/.env
elif [ -f ~/.hermes/profiles/*/home/.hermes/.env ]; then
  # Find the active profile's evaluated location
  ACTIVE_PROFILE=$(ls -d ~/.hermes/profiles/*/home/.hermes/.env | head -1 | xargs dirname | xargs dirname | xargs basename)
  echo "Found .env in active profile location: ~/.hermes/profiles/$ACTIVE_PROFILE/home/.hermes/.env"
  cat ~/.hermes/profiles/$ACTIVE_PROFILE/home/.hermes/.env
else
  echo ".env not found in either location"
fi
```

Apply this pattern to other configuration files like:
- `.env`
- `config.yaml`
- Any custom configuration files

This ensures you capture configuration that may be actively being used versus stale copies.

### 8. API Key Management

When setting up API keys for GitHub, Anthropic, and OpenRouter, follow this procedure:

1. **Locate existing credentials**:
   - GitHub token: Check `gh auth token` or look for `GITHUB_TOKEN` in environment
   - Anthropic token: Check `~/.claude/.credentials.json` for `claudeAiOauth.accessToken`
   - OpenRouter token: Check environment for `OPENROUTER_API_KEY`

2. **Create secure storage**:
   ```bash
   mkdir -p ~/.hermes/secrets
   chmod 700 ~/.hermes/secrets
   ```

3. **Store tokens with restricted permissions**:
   ```bash
   # GitHub
   echo "$GITHUB_TOKEN" > ~/.hermes/secrets/gh_token
   chmod 600 ~/.hermes/secrets/gh_token
   
   # Anthropic (extract from Claude credentials if needed)
   echo "$ANTHROPIC_TOKEN" > ~/.hermes/secrets/anthropic_key
   chmod 600 ~/.hermes/secrets/anthropic_key
   
   # OpenRouter
   echo "$OPENROUTER_API_KEY" > ~/.hermes/secrets/openrouter_key
   chmod 600 ~/.hermes/secrets/openrouter_key
   ```

4. **Configure Hermes to use these files**:
   Add to your ~/.hermes/config.yaml:
   ```yaml
   github:
     token_file: ~/.hermes/secrets/gh_token
   
   anthropic:
     api_key_file: ~/.hermes/secrets/anthropic_key
   
   openrouter:
     api_key_file: ~/.hermes/secrets/openrouter_key
   ```

5. **Update all profiles**:
   Ensure each profile's config.yaml references these shared secret files instead of inline keys.

## Pitfalls

- **Config schema drift can break provider routing hard**: Three specific shape errors cause runtime failures even when API keys are valid:
  1) `custom_providers` written as a mapping (dict) instead of the expected list shape can fail validation and block provider selection.
  2) `model.fallback_model` accidentally stored as a string instead of an object (with `provider` + `model`) causes crashes like `AttributeError: 'str' object has no attribute 'get'` in chat startup.
  3) `fallback_providers` stored as a list of strings (e.g., `['openrouter', 'mistral']`) instead of a list of objects causes startup/provider-override crashes in current Hermes builds that expect each fallback entry to be a dict with `provider` and `model`.

  **Canonical shape:**
  ```yaml
  fallback_providers:
    - provider: ollama-cloud
      model: glm-5.1
    - provider: openrouter
      model: deepseek/deepseek-v4-flash:free
    - provider: mistral
      model: mistral-small-latest
  ```

  **Inspection pattern:**
  - Run `hermes doctor` first to catch structural warnings.
  - Open `config.yaml` and verify data types, not just values.
  - If chat crashes during startup, inspect `model.fallback_model` and `fallback_providers` before rotating keys.
  - Confirm provider keys separately with direct API probes (`/models`) so you can distinguish credential failures from config-shape failures.


- **Symlinked/evaluated path confusion**: The `~/.hermes` path often resolves into a nested `profiles/<profile>/home/.hermes` tree (the active profile's home directory is bound there). Always use `realpath` to see actual storage locations.
- **Per-profile isolation**: Memories, sessions, skills, and state databases are strictly per-profile. Comparing `chief` to `builder` shows independent databases and no shared state.
- **Lock files**: `.lock` files in `memories/` are normal (concurrency control). Do not delete manually while Hermes is running.
- **Database WAL files**: `state.db-wal` and `memory_store.db-wal` are normal Write-Ahead Logging files. Size grows with activity but is checkpointed automatically by SQLite.
- **Hidden `.hermes_history`**: Terminal command history stored in profile root; not memory but useful for audit.
- **Cron storage**: Cron jobs live in `~/profiles/<profile>/cron/` as individual JSON files, not in system crontab.
- **Gateway state**: `gateway_state.json` and `.pid/.lock` files are runtime state, not user memory — safe to inspect but don't edit while running.
- **Skills snapshot**: `.skills_prompt_snapshot.json` is a serialized prompt snapshot; large (~50–100 KB) and safe to ignore for daily ops.
- **macOS path evaluation quirk**: On macOS, `~/.hermes/` may evaluate to `/Users/<user>/.hermes/profiles/<profile>/home/.hermes/` when accessed via relative paths in Hermes commands. This creates a **divergent copy** of files inside `profiles/<profile>/home/.hermes/` alongside the canonical files in `profiles/<profile>/.hermes/`. **Always use absolute paths** (`/Users/<user>/.hermes/...`) when reading/writing files via Hermes tools, and verify both copies are in sync after edits.
  
  **Administrative Tip**: When performing system administration tasks (like finding configuration files, checking secrets, or auditing files), always check both locations:
  1. The canonical location: `~/.hermes/` (or `/Users/<user>/.hermes/`)
  2. The active profile's evaluated location: `~/.hermes/profiles/<active-profile>/home/.hermes/`
  
  For example, to find the actual `.env` file, check both:
  - `~/.hermes/.env`
  - `~/.hermes/profiles/$(cat ~/.hermes/active_profile 2>/dev/null || echo "chief")/home/.hermes/.env`

- **Google AI Pro OAuth ≠ AI Pro subscription quota**: `hermes auth add google-gemini-cli` authenticates against Cloud Code Assist endpoint (`cloudcode-pa://google`) which has its own low per-minute quota (~60-100 req/day). The AI Pro subscription's 1,500 RPD only applies to the `generativelanguage.googleapis.com` endpoint with an API key. These are separate quota buckets. To use AI Pro rates, set up a custom provider pointing to the generativelanguage endpoint with your `GOOGLE_API_KEY`. See `references/google-ai-pro-oauth-quota.md` for full diagnosis and fix options.
- **API key location assumptions**: Don't assume API keys are in environment variables. They may be stored in:
  - Claude credentials: `~/.claude/.credentials.json` (look for `claudeAiOauth.accessToken`)
  - GitHub CLI: `gh auth token`
  - Application-specific config files
  Always verify the actual location before assuming.

## 8-Step Global Health Check Pattern

A systematic inspection routine covering all critical Hermes subsystems. Execute sequentially, confirming each step before proceeding.

**Procedure:**

1. **Plugin Installation** — Check if `~/.hermes/plugins/<plugin-name>` exists. If not, install via git clone. Verify it loads on next gateway boot.

2. **Compressor Threshold** — Open `~/.hermes/config.yaml`, locate `context:` section. If threshold ≤ 0.5, set to `0.70`. If no threshold exists, add: `context: threshold: 0.70`.

3. **MEMORY.md Audit** — Read current MEMORY.md. Remove project-specific details (belong in TASKS/), entries >30 days stale, target <2000 chars (1800 max). Show final version before saving.

4. **USER.md Audit** — Same process as MEMORY.md. Remove stale preferences, target <1300 chars. Show final version before saving.

5. **Coding Delegation Setup** — Verify OpenCode: `which opencode && opencode --version`. Verify Codex: `which codex && codex --version`. These are the preferred coding delegates (OpenCode for everyday, Codex for premium/escalation). Do NOT check for or configure Claude Code.

6. **max_turns Guard** — In config.yaml, under Claude Code delegation defaults, ensure `max_turns: 15`. If no such setting, note for skill-level configuration.

7. **Wiki Retrieval Mode** — If LLM-Wiki skill active, verify scan-first mode in USER.md: "For wiki lookups, always do a scan-only pass first. Only open full page bodies if scan doesn't resolve the query."

8. **Usage Baseline** — Run `hermes sessions list --limit 5`. If unavailable, check logs at `~/.hermes/logs/` and extract token usage from recent gateway entries.

**Report Format:** Numbered checklist with ✅ or ❌ per item. Do not skip steps.

**Session Meta-Learning:** This pattern emerged from user demand for systematic verification. Capture procedural knowledge in skills; memory stores state, skills store how-to.

- **Confirm each step before moving to the next** — Do not batch operations; verify success at each checkpoint
- **Numbered checklist reporting** — Use `1. ✅ item` for completed items, `1. ❌ item (reason)` for blocked items
- **Stop on critical failures** — If a step cannot be completed and blocks downstream work, report it immediately and halt
- **macOS path handling** — Always use absolute paths (`/Users/<user>/.hermes/...`) when reading/writing files via Hermes tools to avoid path resolution into nested profile homes
**Report Format:** Numbered checklist with ✅ or ❌ per item. Do not skip steps.

**Session Meta-Learning:** This pattern emerged from user demand for systematic verification. Capture procedural knowledge in skills; memory stores state, skills store how-to.

- **Confirm each step before moving to the next** — Do not batch operations; verify success at each checkpoint
- **Numbered checklist reporting** — Use `1. ✅ item` for completed items, `1. ❌ item (reason)` for blocked items
- **Stop on critical failures** — If a step cannot be completed and blocks downstream work, report it immediately and halt
- **macOS path handling** — Always use absolute paths (`/Users/<user>/.hermes/...`) when reading/writing files via Hermes tools to avoid path resolution into nested profile homes
**Session evidence:** 2026-05-14 crew alignment audit — user demanded Phase 1 audit first, Phase 2 fixes after approval.

## Manual Skill Installation

When `hermes skills install <skill-name>` is unavailable or fails, install manually from upstream:

```bash
# Create skill directory structure
mkdir -p ~/.hermes/skills/<category>/<skill-name>

# Download SKILL.md from source
curl -o ~/.hermes/skills/<category>/<skill-name>/SKILL.md \
  https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/<category>/<skill-name>/SKILL.md

# Verify download
ls -lh ~/.hermes/skills/<category>/<skill-name>/SKILL.md
head -5 ~/.hermes/skills/<category>/<skill-name>/SKILL.md
```

**Common upstream patterns:**
- Built-in skills: `~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md`
- GitHub raw: `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/<category>/<skill-name>/SKILL.md`

**When to use:**
- `hermes skills install` CLI unavailable
- Network-restricted environments
- Skill not yet in registry
- Need specific version from source

## Verification checklist

- [ ] All profiles listed under `~/.hermes/profiles/`
- [ ] Each profile contains: `sessions/`, `skills/`, `memories/`
- [ ] `memories/MEMORY.md` and `memories/USER.md` exist per profile
- [ ] `SOUL.md` exists at profile root (persona definition)
- [ ] `state.db` and `memory_store.db` are present and non-zero
- [ ] `hermes doctor` reports all checkmarks green for the active profile
- [ ] Active profile's home path resolves correctly via `realpath ~/.hermos`

## References

- `references/profile-layout.md` — detailed directory tree and file purpose reference
- `references/sample-memory-files.md` — example `MEMORY.md`, `USER.md`, `SOUL.md` structures per-profile
- `references/google-ai-pro-oauth-quota.md` — Google AI Pro OAuth vs Code Assist quota pitfall and fix options
- `references/provider-model-alignment.md` — multi-profile model provider alignment (May 2026 reference)
- `references/provider-config-shape-vs-key-validity.md` — distinguish config schema drift from bad API keys during provider onboarding
- `references/fallback-providers-dict-shape.md` — fallback chain must be list-of-dicts (`provider` + `model`), not list-of-strings
- `references/crew-alignment-audit.md` — POD v1.0 crew profile alignment audit pattern
- `references/8-step-health-check-pattern.md` — global health check workflow
- `references/provider-model-alignment.md` — multi-profile model provider alignment (May 2026 reference)
- `references/ttyd-web-terminal.md` — ttyd web terminal setup, pitfalls, and plist template
- `templates/verification-report.md` — template for system verification reports
