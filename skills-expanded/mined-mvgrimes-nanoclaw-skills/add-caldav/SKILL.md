---
name: add-caldav
description: Add CalDAV calendar access to NanoClaw. Supports iCloud, Nextcloud, Fastmail and other CalDAV providers via Basic Auth. Guides through app-specific password setup and configures environment variables. Triggers on "add caldav", "icloud calendar", "nextcloud calendar", "fastmail calendar", "caldav setup".
---

# Add CalDAV Calendar Access

CalDAV integration for NanoClaw agent containers via `cal-cli` (a TypeScript CLI supporting iCloud, Nextcloud, Fastmail, and any CalDAV server).

## Preflight

Before installing, verify NanoClaw is set up:

```bash
[ -d node_modules ] && echo "DEPS: ok" || echo "DEPS: missing"
docker image inspect nanoclaw-agent:latest &>/dev/null && echo "IMAGE: ok" || echo "IMAGE: not built"
(grep -q "ANTHROPIC_API_KEY\|CLAUDE_CODE_OAUTH_TOKEN" .env 2>/dev/null || [ -f ~/.claude/.credentials.json ]) && echo "AUTH: ok" || echo "AUTH: missing"
```

If any check fails, tell the user to run `/nanoclaw-setup` first and stop.

## Install

1. Check existing configuration:
   ```bash
   (grep -rq "^CALDAV_ACCOUNTS=" .env groups/*/.env 2>/dev/null) && echo "CALDAV: CONFIGURED" || echo "CALDAV: NOT SET"
   ```
   If already configured, ask the user if they want to add another provider or reconfigure.

2. Gather account details:
   - **Provider name** (e.g., "iCloud", "Nextcloud", "Fastmail")
   - **CalDAV server URL**:
     - iCloud: `https://caldav.icloud.com`
     - Nextcloud: `https://YOUR_SERVER/remote.php/dav`
     - Fastmail: `https://caldav.fastmail.com`
   - **Username** (usually email address)
   - **App-specific password**

   App-specific password instructions:

   **iCloud:**
   > 1. Go to https://appleid.apple.com/account/manage
   > 2. Sign in > "Sign-In and Security" > "App-Specific Passwords"
   > 3. Click + > Name it "NanoClaw" > Create
   > 4. Copy the password (format: xxxx-xxxx-xxxx-xxxx)

   **Nextcloud:**
   > 1. Settings > Security > "Devices & Sessions"
   > 2. Enter "NanoClaw" > "Create new app password"

   **Fastmail:**
   > 1. Settings > Privacy & Security > Integrations
   > 2. "New app password" > Select CalDAV > Name it "NanoClaw"

3. Save to `.env`:
   ```bash
   sed -i '/^CALDAV_ACCOUNTS=/d' .env
   echo 'CALDAV_ACCOUNTS=[{"name":"iCloud","serverUrl":"https://caldav.icloud.com","user":"user@icloud.com","pass":"xxxx-xxxx-xxxx-xxxx"}]' >> .env
   ```

### Group Scoping

Ask the user which groups should have access to CalDAV:

- **All groups** (default) -- every group's agent can read and manage calendar events
- **Specific groups only** -- e.g., only `main` and `family-chat`

If the user wants to restrict access, update `plugins/caldav/plugin.json` after copying (next step) to set `"groups"` to the list of group folder names:

```json
"groups": ["main", "family-chat"]
```

If all groups (or the user doesn't care), leave as `"groups": ["*"]`.

### Deploy Plugin

Copy plugin files:
```bash
mkdir -p plugins/caldav/container-skills plugins/caldav/cal-cli/src
cp ${CLAUDE_PLUGIN_ROOT}/files/plugin.json plugins/caldav/
cp ${CLAUDE_PLUGIN_ROOT}/files/container-skills/SKILL.md plugins/caldav/container-skills/
cp ${CLAUDE_PLUGIN_ROOT}/files/Dockerfile.partial plugins/caldav/
cp ${CLAUDE_PLUGIN_ROOT}/files/cal-cli/package.json ${CLAUDE_PLUGIN_ROOT}/files/cal-cli/tsconfig.json plugins/caldav/cal-cli/
cp ${CLAUDE_PLUGIN_ROOT}/files/cal-cli/src/*.ts plugins/caldav/cal-cli/src/
```

Rebuild and restart:
```bash
./container/build.sh
systemctl restart nanoclaw 2>/dev/null || launchctl kickstart -k gui/$(id -u)/com.nanoclaw 2>/dev/null || echo "Restart the NanoClaw service manually"
```

## Verify

Tell the user:
> CalDAV access is configured. Test via WhatsApp: "list my calendars" or "what's on my calendar today?"

## Troubleshooting

- **"401 Unauthorized"**: Use an app-specific password, not your account password.
- **"CALDAV_ACCOUNTS not defined"**: Check it's in both `.env` and `plugin.json` containerEnvVars.
- **Nextcloud connection refused**: Verify the server URL includes `/remote.php/dav`.

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
   echo 'CALDAV_ACCOUNTS=[{"name":"Work","serverUrl":"https://caldav.example.com","user":"work@example.com","pass":"app-password"}]' >> groups/{folder}/.env
   ```
   These values override the global `.env` for that group's containers only.

5. Restart NanoClaw:
   ```bash
   sudo systemctl restart nanoclaw
   ```

## Remove

1. `rm -rf plugins/caldav/`
2. Remove env vars from `.env`:
   ```bash
   sed -i '/^CALDAV_ACCOUNTS=/d' .env
   ```
3. Rebuild the container image:
   ```bash
   ./container/build.sh
   ```
4. Restart the service.
5. Revoke app-specific passwords in provider security settings.
