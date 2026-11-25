---
name: infer-upgrade
description: Use when the user says "update infer", "upgrade infer", invokes /infer-upgrade, or when another Infer skill detects outdated packages. Updates the SDK, MCP server, and skills to the latest versions.
allowed-tools:
  - AskUserQuestion
---

# Infer Upgrade

Updates all three Infer components to their latest versions.

## Step 1: Check current vs latest

Run these commands to detect what's installed and what's available:

```bash
# Latest versions on npm
echo "SDK_LATEST=$(npm view @inferevents/sdk version 2>/dev/null || echo 'not-published')"
echo "MCP_LATEST=$(npm view @inferevents/mcp version 2>/dev/null || echo 'not-published')"

# Installed SDK in current project
echo "SDK_INSTALLED=$(npm ls @inferevents/sdk --json 2>/dev/null | grep '"version"' | head -1 | sed 's/[^0-9.]//g' || echo 'not-installed')"

# Check if MCP config exists
echo "MCP_CONFIG=$(cat ~/.infer/config.json 2>/dev/null | head -1 || echo 'no-config')"

# Skills last install date (check file modification time)
echo "SKILLS_MTIME=$(stat -f '%Sm' -t '%Y-%m-%d' ~/.claude/skills/infer-setup/SKILL.md 2>/dev/null || stat -c '%y' ~/.claude/skills/infer-setup/SKILL.md 2>/dev/null | cut -d' ' -f1 || echo 'not-installed')"
```

## Step 2: Show status

Present a clear summary:

```
Infer Update Check
──────────────────────────────────────

SDK (@inferevents/sdk)
  Installed: [version or "not installed"]
  Latest:    [version]
  Status:    [Up to date / UPDATE AVAILABLE / Not installed]

MCP (@inferevents/mcp)
  Latest:    [version]
  Status:    [npx always fetches latest on restart]

Skills (infer-events/skills)
  Installed: [date or "not installed"]
  Status:    Re-installing to ensure latest
```

## Step 3: Update

Ask: "Ready to update? This will update [list what needs updating]."

### 3a: Update SDK (if installed in project)

```bash
npm install @inferevents/sdk@latest
```

If SDK is NOT in the current project's dependencies, skip with:
"SDK not found in this project's dependencies. Skipping."

### 3b: Update MCP server

The MCP runs via `npx @inferevents/mcp` which caches. Clear the cache:

```bash
# Clear npx cache for the MCP package
npx --yes @inferevents/mcp@latest --version 2>/dev/null || true
```

Check `.mcp.json` in the project root (and `~/.claude/.mcp.json` globally).
If the args contain a pinned version like `@inferevents/mcp@0.1.6` or any
`@inferevents/mcp@X.Y.Z`, replace it with `@inferevents/mcp` (no version).
This ensures npx always fetches the latest. A pinned version in .mcp.json
is the #1 cause of "Failed to reconnect" after an upgrade.

```bash
# Check and fix pinned versions
if [ -f .mcp.json ] && grep -q '@inferevents/mcp@' .mcp.json; then
  sed -i '' 's/@inferevents\/mcp@[0-9.]*/@inferevents\/mcp/g' .mcp.json
  echo "Fixed pinned MCP version in .mcp.json"
fi
```

After updating, reload the MCP server in-place so the user doesn't have to restart:

Tell the user: "MCP server updated. Type `/mcp` and restart the `infer` server to load the new version. No need to exit Claude Code."

### 3c: Update skills

```bash
npx skills add infer-events/skills
```

This always fetches latest from GitHub (no caching).

### 3d: Write cache

After a successful update, write the cache so other skills know we just checked:

```bash
mkdir -p ~/.infer
echo "{\"checked\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"sdk\":\"SDK_LATEST\",\"mcp\":\"MCP_LATEST\"}" > ~/.infer/last-update-check.json
```

## Step 4: Verify

1. Call `get_top_events(time_range="last_24h")` to verify MCP still works
2. If it fails: "MCP server needs a reload. Type `/mcp` and restart the `infer` server."
3. If it works: "All Infer components updated and verified."

## Summary format

```
Infer Upgrade Complete
──────────────────────────────────────

SDK     0.1.2 → 0.1.3   Updated
MCP     0.1.2 → 0.1.3   Updated
Skills  ────────────────  Re-installed from GitHub

Type /mcp → restart "infer" to load the new MCP server.
```

If everything was already up to date:

```
Infer — All Up to Date
──────────────────────────────────────

SDK     0.1.3   Latest
MCP     0.1.3   Latest
Skills  ──────  Re-installed (always pulls latest)
```

## Step 5: Suggest next steps

After upgrade completes, you MUST call the `AskUserQuestion` tool. Use AskUserQuestion:

> Upgrade complete. What do you want to do next?
>
> 💡 Tip: After upgrading, it's a good idea to verify your events are still flowing correctly.

Options:
- A) Verify events are flowing — Quick check that the SDK is sending data correctly after the upgrade
- B) Run a health check — See current insights and make sure nothing broke
- C) Check what's new — Show me what changed in the latest version
- D) Back to work — Everything looks good, I'll continue what I was doing
