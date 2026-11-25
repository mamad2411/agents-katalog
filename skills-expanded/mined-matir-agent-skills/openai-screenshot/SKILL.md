---
name: openai-screenshot
description: Captures desktop or system screenshots of full screens, specific windows, or pixel regions. Useful when application-level capture is unavailable.
allowed-tools:
- Bash
- Read
- Grep
- Glob
- Write
- Edit
metadata:
  version: 0.2.0
  category: utility
---
# Screenshot Capture

## Quick Start
```bash
# Capture full screen to temporary directory (for agent visual check)
python3 ../scripts/take_screenshot.py --mode temp

# Capture specific app by name (macOS only)
python3 ../scripts/take_screenshot.py --app "the agent" --mode temp
```

## Workflow
1. **Permission Check**: (macOS) Run `ensure_macos_permissions.sh` preflight.
2. **Target Identification**: Identify the required capture scope (full screen, app, window, or pixel region).
3. **Capture Mode**: Choose destination: user-specified path, OS default, or `--mode temp` for internal agent checks.
4. **Execution**: Run `take_screenshot.py` (macOS/Linux) or `take_screenshot.ps1` (Windows) with appropriate flags.
5. **Path Verification**: Confirm the saved file path(s) and view sequentially.

## Rules & Constraints
- **Save Hierarchy**: User path > OS default > Temp (for internal use).
- **Tool Priority**: Prefer app-specific capture (Figma skill, Playwright) over general system capture.
- **Privacy**: Do not capture sensitive areas; use `--region` or `--app` for scoped captures.
- **Reporting**: Always state the exact saved file path in the final response.

## When to Use
- User explicitly requests a desktop or system screenshot.
- Application-level capture (e.g., browser-only) cannot capture the required system state.
- Inspecting non-web desktop applications without integrated capture tools.

## When NOT to Use
- Without explicit user request or clear internal visual validation requirement.
- When tool-specific capture (e.g., Figma MCP) is available.

## References
- [Skill Manual](references/openai-screenshot-manual.md)
- [Python Helper Scripts](../scripts/take_screenshot.py)
- [PowerShell Helper Scripts](../scripts/take_screenshot.ps1)
