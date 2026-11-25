---
name: add-google-calendar
description: Add Google Calendar access to NanoClaw via gog CLI with OAuth. Guides through credentials import, OAuth login, and environment variable configuration. Triggers on "add google calendar", "google calendar setup", "gog calendar".
---

# Add Google Calendar Access

Google Calendar integration for NanoClaw agent containers via `gog` (gogcli — Google Workspace CLI with OAuth).

## Preflight

Before installing, verify NanoClaw is set up:

```bash
[ -d node_modules ] && echo "DEPS: ok" || echo "DEPS: missing"
docker image inspect nanoclaw-agent:latest &>/dev/null && echo "IMAGE: ok" || echo "IMAGE: not built"
(grep -q "ANTHROPIC_API_KEY\|CLAUDE_CODE_OAUTH_TOKEN" .env 2>/dev/null || [ -f ~/.claude/.credentials.json ]) && echo "AUTH: ok" || echo "AUTH: missing"
```

If any check fails, tell the user to run `/nanoclaw-setup` first and stop.

## Install

1. Check existing configuration (credentials may be in global `.env` or any group's `groups/*/.env`):
   ```bash
   (grep -rq "^GOG_KEYRING_PASSWORD=" .env groups/*/.env 2>/dev/null) && echo "GOOGLE: CONFIGURED" || echo "GOOGLE: NOT SET"
   ```
   If already configured, ask the user if they want to reconfigure or add another account.

2. Install gog on the host if needed:
   ```bash
   which gog && echo "GOG_INSTALLED" || curl -sL "https://github.com/steipete/gogcli/releases/download/v0.9.0/gogcli_0.9.0_linux_amd64.tar.gz" | tar -xz -C /usr/local/bin gog
   ```

   gogcli is also installed automatically when the container image is built (via `plugins/google-calendar/Dockerfile.partial`). No manual Dockerfile changes needed.

3. Import OAuth credentials (user provides their client_secret.json path):
   ```bash
   gog auth credentials /path/to/client_secret.json
   ```

4. OAuth login (include gmail if the Gmail plugin is already installed to preserve its scopes):
   ```bash
   if [ -d plugins/gmail ]; then
     GOG_KEYRING_PASSWORD=$(grep GOG_KEYRING_PASSWORD .env | cut -d'=' -f2) gog auth login --services calendar,gmail
   else
     GOG_KEYRING_PASSWORD=$(grep GOG_KEYRING_PASSWORD .env | cut -d'=' -f2) gog auth login --services calendar
   fi
   ```

   On a headless server, add `--manual` to the gog command above.

   Verify: `GOG_KEYRING_PASSWORD=$(grep GOG_KEYRING_PASSWORD .env | cut -d'=' -f2) gog calendar calendars`

5. Configure environment:
   ```bash
   grep "^GOG_KEYRING_PASSWORD=" .env 2>/dev/null && echo "ALREADY_SET" || echo 'GOG_KEYRING_PASSWORD=THEIR_PASSWORD_HERE' >> .env
   ```

6. Copy gog config for containers:
   ```bash
   mkdir -p data/gogcli
   cp -r ~/.config/gogcli/* data/gogcli/
   chown -R 1000:1000 data/gogcli
   ```

### Group Scoping

Ask the user which groups should have access to Google Calendar:

- **All groups** (default) -- every group's agent can read and manage calendar events
- **Specific groups only** -- e.g., only `main` and `family-chat`

If the user wants to restrict access, update `plugins/google-calendar/plugin.json` after copying (next step) to set `"groups"` to the list of group folder names:

```json
"groups": ["main", "family-chat"]
```

If all groups (or the user doesn't care), leave as `"groups": ["*"]`.

### Deploy Plugin

Copy plugin files:
```bash
mkdir -p plugins/google-calendar/container-skills plugins/google-calendar/scripts
cp ${CLAUDE_PLUGIN_ROOT}/files/plugin.json plugins/google-calendar/
cp ${CLAUDE_PLUGIN_ROOT}/files/container-skills/SKILL.md plugins/google-calendar/container-skills/
cp ${CLAUDE_PLUGIN_ROOT}/files/Dockerfile.partial plugins/google-calendar/
cp ${CLAUDE_PLUGIN_ROOT}/files/scripts/gog-reauth.sh plugins/google-calendar/scripts/ && chmod +x plugins/google-calendar/scripts/gog-reauth.sh
```

Rebuild and restart:
```bash
./container/build.sh
systemctl restart nanoclaw 2>/dev/null || launchctl kickstart -k gui/$(id -u)/com.nanoclaw 2>/dev/null || echo "Restart the NanoClaw service manually"
```

## Verify

Tell the user:
> Google Calendar access is configured. Test via WhatsApp: "list my calendars" or "what's on my calendar today?"

## Refresh Google OAuth Token

Google OAuth tokens expire periodically. When the agent reports `"invalid_grant" "Token has been expired or revoked."`, use the helper script:

```bash
# Check which accounts need reauth (non-destructive)
./plugins/google-calendar/scripts/gog-reauth.sh --check

# Reauth — auto-detects expired accounts, prompts for selection
./plugins/google-calendar/scripts/gog-reauth.sh

# Reauth all expired accounts in sequence
./plugins/google-calendar/scripts/gog-reauth.sh --all

# Reauth a specific account
./plugins/google-calendar/scripts/gog-reauth.sh user@gmail.com
```

The script automatically:
1. Discovers all `GOG_ACCOUNT` values across `groups/*/.env` and `.env`
2. Tests each account's OAuth token against the Google Calendar API
3. Shows which accounts are healthy (✓) and which are expired (✗)
4. If multiple expired, offers to reauth all or pick specific ones
5. Uses the `GOG_KEYRING_PASSWORD` from the same env file as the account
6. Includes gmail scopes if the gmail plugin is installed
7. Runs `gog auth` via expect (handles the CSRF state matching that breaks with separate invocations)
8. Prompts for the redirect URL interactively
9. Syncs credentials to `data/gogcli/` for container access
10. Verifies each account after reauth

### From Claude Code (non-interactive)

Since Claude Code can't use `read`, run the script in the background and feed the redirect URL via file:

The approach uses `plugins/google-calendar/scripts/gog-reauth.sh`'s expect script but non-interactively:

1. First, discover which account needs reauth. If the agent reported the error, check which group it was for and find the `GOG_ACCOUNT` in that group's `.env`.

2. Write and run the expect script from `plugins/google-calendar/scripts/gog-reauth.sh` (the section between `EXPECT_EOF` markers) in the background, passing `$EMAIL`, `$SERVICES`, `$STATE_FILE`, and `$REDIRECT_FILE`.

3. Wait for `$STATE_FILE` to be written (contains the CSRF state token).

4. Show the user the OAuth URL containing the state from `$STATE_FILE`.

5. User authorizes and pastes redirect URL.

6. Write the redirect URL to `$REDIRECT_FILE` — the expect process picks it up and completes auth.

7. Sync: `cp -r ~/.config/gogcli/* data/gogcli/ && chown -R 1000:1000 data/gogcli/`

IMPORTANT: Each `gog auth` invocation generates a unique CSRF state token. The redirect URL from one invocation will NOT work with another — the state must match. This is why the expect approach keeps the same process alive throughout.

## Troubleshooting

- **gog "invalid_grant" / "Token has been expired or revoked"**: Follow the "Refresh Google OAuth Token" section above.
- **gog works on host but not in container**: Credentials not synced — run `cp -r ~/.config/gogcli/* data/gogcli/ && chown -R 1000:1000 data/gogcli/`.
- **gog config not found in container**: Ensure `data/gogcli/` exists and is chowned to 1000:1000.

## Per-Group Credentials

If this plugin is already installed and you want **different credentials for a specific group** (e.g., a work account for one group, personal for another):

1. Check which groups exist:
   ```bash
   ls -d groups/*/
   ```

2. Ask the user which group should get separate credentials.

3. Collect the new credentials for that group.

4. Write to the group's `.env` file (creates if needed):
   ```bash
   echo 'GOG_KEYRING_PASSWORD=new-password' >> groups/{folder}/.env
   echo 'GOG_ACCOUNT=other@gmail.com' >> groups/{folder}/.env
   ```
   These values override the global `.env` for that group's containers only.

5. Restart NanoClaw:
   ```bash
   sudo systemctl restart nanoclaw
   ```

## Remove

1. `rm -rf plugins/google-calendar/`
2. Remove env vars from `.env`:
   ```bash
   sed -i '/^GOG_KEYRING_PASSWORD=/d' .env
   sed -i '/^GOG_ACCOUNT=/d' .env
   ```
3. `rm -rf data/gogcli`
4. Rebuild the container image:
   ```bash
   ./container/build.sh
   ```
5. Restart the service.
