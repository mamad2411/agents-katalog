---
name: planSettingsReset
description: Reset plugin settings to defaults
---

# Plan Settings Reset

Reset plugin settings to defaults.

## Usage

```bash
/planSettingsReset              # Reset global settings to defaults
/planSettingsReset --local      # Remove project-specific settings
```

## Step 0: Load Configuration

```javascript
function getConfig() {
  const localConfigPath = "./.plan-config.json"
  if (fileExists(localConfigPath)) {
    try {
      const config = JSON.parse(readFile(localConfigPath))
      config._source = "local"
      return config
    } catch {}
  }

  const globalConfigPath = expandPath("~/.config/claude/plan-plugin-config.json")
  if (fileExists(globalConfigPath)) {
    try {
      const config = JSON.parse(readFile(globalConfigPath))
      config._source = "global"
      return config
    } catch {}
  }

  return { "language": "en", "_source": "default" }
}

const config = getConfig()
const language = config.language || "en"
const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Parse Arguments

```javascript
const isLocal = commandArgs.includes("--local")
const scope = isLocal ? "local" : "global"
```

## Step 2: Execute Reset

### For local scope (--local)

1. Check if `./.plan-config.json` exists
2. If exists, remove it: `rm ./.plan-config.json`
3. Re-read config with hierarchy (will fall back to global or default)
4. Load new effective language translations

**Success:**
```
✅ {t_new.commands.settings.settingsUpdated}

📁 {t_new.commands.settings.projectSettingsRemoved}

{t_new.commands.settings.nowUsing}: {newConfig._source === "global" ? "🌐 Global settings" : "⚙️ Default (English)"}
```

**If no local config exists:**
```
ℹ️ No project-specific settings found
```

### For global scope (no flag)

1. Create default config:
```json
{
  "language": "en",
  "lastUsed": "2026-01-27T15:30:00Z"
}
```

2. Ensure directory exists: `mkdir -p ~/.config/claude`
3. Write default config to `~/.config/claude/plan-plugin-config.json`
4. Load English translations

**Success:**
```
✅ {t_en.commands.settings.settingsUpdated}

🌐 {t_en.commands.settings.globalSettingsReset}

Reset to defaults:
🌍 Language: English
```

## Error Handling

**Cannot delete/write file:**
```
⚠️ Warning: Couldn't save settings
Settings will apply for this session only
```
