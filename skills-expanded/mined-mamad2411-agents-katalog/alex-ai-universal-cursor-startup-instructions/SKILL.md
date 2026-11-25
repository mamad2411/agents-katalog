# 🖖 Alex AI Cursor Startup - Manual Activation Required

**After computer restart, Cursor AI may not automatically run startup tasks.**

## ⚠️ Known Issue

Cursor AI does not reliably execute VS Code tasks with `runOn: "folderOpen"` automatically. This is a known limitation.

## ✅ Solution: Manual Activation

After opening Cursor AI workspace, run one of these commands:

### Option 1: Quick Startup (Recommended)
```bash
npm run cursor:startup
```

This will:
1. Load crew memories from Supabase
2. Generate the startup prompt
3. Save everything to `.cursor/alex-ai/cursor-startup-prompt.md`

### Option 2: Command Palette
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type: "Alex AI"
3. Select: "🖖 Alex AI Full Startup"

### Option 3: Individual Steps
```bash
# Load memories
npm run cursor:memories

# Generate prompt
npm run cursor:prompt
```

## 🎯 After Running Startup

1. **Open Cursor AI chat**
2. **Copy the prompt** from `.cursor/alex-ai/cursor-startup-prompt.md`
3. **Paste into chat** to activate Alex AI with full crew context

## 🔍 Diagnose Issues

If startup isn't working, run diagnostics:

```bash
npm run cursor:diagnose
```

This will check:
- Configuration files
- Scripts
- Environment variables
- Task configuration
- Prompt freshness

## 💡 Quick Reference

| Command | Purpose |
|---------|---------|
| `npm run cursor:startup` | Full startup (memories + prompt) |
| `npm run cursor:memories` | Load crew memories only |
| `npm run cursor:prompt` | Generate startup prompt only |
| `npm run cursor:diagnose` | Diagnose startup issues |

## 🚀 Future Solution

We're working on a more reliable automatic startup mechanism. For now, use the manual activation above.

---

**Last Updated**: 2025-11-27  
**Status**: Manual activation required after restart

