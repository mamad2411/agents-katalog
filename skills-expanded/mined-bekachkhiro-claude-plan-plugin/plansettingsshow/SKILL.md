---
name: planSettingsShow
description: Display current plugin configuration
---

# Plan Settings Show

Display current plugin configuration including language, cloud status, and auto-sync settings.

## Usage

```bash
/planSettingsShow
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
const cloudConfig = config.cloud || {}
const isAuthenticated = !!cloudConfig.apiToken
const autoSync = cloudConfig.autoSync || false

// Also load both configs for display
const localConfig = fileExists("./.plan-config.json")
  ? JSON.parse(readFile("./.plan-config.json")) : null
const globalConfig = fileExists(expandPath("~/.config/claude/plan-plugin-config.json"))
  ? JSON.parse(readFile(expandPath("~/.config/claude/plan-plugin-config.json"))) : null

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Display Settings

```javascript
const languageNames = {
  "en": "English",
  "ka": "ქართული (Georgian)",
  "ru": "Русский (Russian)"
}

const currentLanguageName = languageNames[config.language] || "English"
```

**Output:**
```
⚙️ {t.commands.settings.title}

📊 Active Configuration:
🌍 {t.commands.settings.language}: {currentLanguageName} ({config._source})
```

**If authenticated:**
```
☁️ Cloud: Connected ({cloudConfig.userEmail || "user"})
📁 Linked Project: {cloudConfig.projectId || "None"}
🔄 Auto-sync: {autoSync ? "Enabled" : "Disabled"}
```

**If not authenticated:**
```
☁️ Cloud: Not connected
```

**If local config exists:**
```
📁 Project Settings (./.plan-config.json):
  🌍 {t.commands.settings.language}: {localLangName}
  📅 {t.commands.settings.lastUsed}: {localConfig.lastUsed || "N/A"}
```

**If global config exists:**
```
🌐 Global Settings (~/.config/claude/plan-plugin-config.json):
  🌍 {t.commands.settings.language}: {globalLangName}
  📅 {t.commands.settings.lastUsed}: {globalConfig.lastUsed || "N/A"}
```

**Available commands:**
```
{t.commands.settings.availableCommands}:
- /planSettingsLanguage           # Change global language
- /planSettingsLanguage --local   # Change project language
- /planSettingsAutoSync           # Manage auto-sync
- /planSettingsReset              # Reset global settings
- /planSettingsReset --local      # Remove project settings
```

## Error Handling

If config corrupted:
```
⚠️ Warning: Config file was corrupted, using defaults
```
