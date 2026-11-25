---
name: planSettingsAutoSync
description: Manage automatic synchronization after planUpdate commands
---

# Plan Settings Auto-Sync

Manage automatic synchronization after /planUpdate commands.

## Usage

```bash
/planSettingsAutoSync           # Show auto-sync status
/planSettingsAutoSync on        # Enable auto-sync
/planSettingsAutoSync off       # Disable auto-sync
```

## Step 0: Load Configuration

```javascript
function getConfig() {
  const localConfigPath = "./.plan-config.json"
  let localConfig = {}
  if (fileExists(localConfigPath)) {
    try { localConfig = JSON.parse(readFile(localConfigPath)) } catch {}
  }

  const globalConfigPath = expandPath("~/.config/claude/plan-plugin-config.json")
  let globalConfig = {}
  if (fileExists(globalConfigPath)) {
    try { globalConfig = JSON.parse(readFile(globalConfigPath)) } catch {}
  }

  return { ...globalConfig, ...localConfig }
}

const config = getConfig()
const language = config.language || "en"
const cloudConfig = config.cloud || {}
const isAuthenticated = !!cloudConfig.apiToken
const autoSync = cloudConfig.autoSync || false

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Parse Arguments

```javascript
const autoSyncValue = commandArgs.trim().toLowerCase() || null  // "on", "off", or null
```

## Step 2: Check Authentication

**If not authenticated:**
```
❌ {t.commands.settings.autoSyncNotAuthenticated}

💡 {t.commands.settings.autoSyncLoginFirst}
   /pfLogin
```

## Step 3: Handle Based on Value

### If null (show status)

```
🔄 {t.commands.settings.autoSyncTitle}

{statusIcon} {t.commands.settings.autoSyncStatus}: {statusText}

{t.commands.settings.autoSyncUsage}:
  /planSettingsAutoSync on     # {t.commands.settings.autoSyncEnableHint}
  /planSettingsAutoSync off    # {t.commands.settings.autoSyncDisableHint}

{t.commands.settings.autoSyncDescription}
```

### If "on" (enable)

1. Read `./.plan-config.json`
2. Set `cloud.autoSync = true`
3. Update `lastUsed`
4. Write back

**Success:**
```
✅ {t.commands.settings.autoSyncEnabledSuccess}

🔄 {t.commands.settings.autoSyncNowEnabled}

{t.commands.settings.autoSyncWhatHappens}:
  • /planUpdate T1.1 done → {t.commands.settings.autoSyncAutoUpload}

💡 {t.commands.settings.autoSyncDisableHint}: /planSettingsAutoSync off
```

### If "off" (disable)

1. Read `./.plan-config.json`
2. Set `cloud.autoSync = false`
3. Update `lastUsed`
4. Write back

**Success:**
```
✅ {t.commands.settings.autoSyncDisabledSuccess}

🔄 {t.commands.settings.autoSyncNowDisabled}

{t.commands.settings.autoSyncManualSync}:
  /pfSyncPush

💡 {t.commands.settings.autoSyncEnableHint}: /planSettingsAutoSync on
```

### If invalid value

```
❌ {t.commands.settings.autoSyncInvalidValue}

{t.commands.settings.autoSyncUsage}:
  /planSettingsAutoSync on
  /planSettingsAutoSync off
```
