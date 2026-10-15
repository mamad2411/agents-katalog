---
name: agentic-test-driven-development
description: A visual test-driven development loop for Compose apps using Compose HotSwan for Android device testing. Navigates the live app, edits code, hot-reloads, and produces a markdown report that EMBEDS before/after screenshots so the change is shown, not just claimed.
---

# Agentic Test-Driven Development (Visual TDD via Compose HotSwan)

Use this skill when the user asks to implement and visually verify a change in a
Compose app. The whole loop runs through the **Compose HotSwan** tools built into Android Studio — no `screencapture`, no AppleScript, no asking the user to click things.

## Core principle: SHOW, don't tell
Trust comes from evidence. Every run MUST end with a markdown report that
**embeds the actual before and after pictures side by side**. Never report a
change as done on the basis of code edits or semantic-tree text alone — capture
the pixels and put them in the report.

**Report format (confirmed working in the JetBrains/IntelliJ Markdown preview,
where the user reads these):** The IDE's markdown preview drops HTML `<img>` tags. To provide a quick side-by-side view without requiring endless scrolling, we use a Markdown table at the top (which scales them down, despite adding some whitespace). We add explicit file links below the images in the table so the user can click to see the full-size images. Use absolute paths.

Two hard-won rendering rules:
- **Absolute paths are required.** Relative paths like `before.png` do NOT
  resolve in the preview. Always write the full `/Users/.../.agents/tdd-reports/<TS>/...png`.
- **HTML tags are dropped:** Do not use base64 or HTML `<img>` tags. Always use standard Markdown image syntax `![](...)`.

The helper `build_tdd_report.py` produces exactly this (and abspath-converts the
image paths for you).

## Setup
If the user's project is missing HotSwan setup, the agent should:
1. Ensure `libs.versions.toml` contains `composeHotReload = "..."` in `[versions]`, the library block, and the `[plugins]` block.
2. Apply the plugin in the root `build.gradle.kts`.
3. Apply the plugin in the relevant subproject `build.gradle.kts` (e.g. `:androidApp`, `:shared`).
4. Perform a Gradle Sync.
1. The Compose HotSwan plugin must be installed and active in Android Studio.
2. The app must be running on an Android emulator or device with HotSwan connected. Check using the `hotswan_get_status` tool. If it's not connected, use `hotswan_build_and_install` or ask the user to start the app via the HotSwan play button.
3. A `.agents/tdd-reports/` directory at the project root (create if missing).

## The HotSwan Toolbox
- `hotswan_get_status` — is the app connected and hot reload active?
- `hotswan_get_hierarchy` — the UI tree: composable node ids, roles, text, and structure. Use this to verify text changes.
- `hotswan_take_screenshot` — clean screenshot of the device. Note: this tool saves the PNG automatically and returns the absolute path to the saved file. You do NOT need a separate script to extract the image.
- `hotswan_reload` — pass the list of modified file paths to trigger a hot reload.

## Execution Strategy: Sub-Agent Delegation

Because this loop requires a sequence of tool calls, **you MUST delegate the entire workflow to a sub-agent using the `task` tool.** Do not execute it step-by-step in the main chat.

**Main Agent Instructions:**
1. Call the `task` tool. Your prompt to the sub-agent must be a self-contained ticket: tell it to follow the "agentic-test-driven-development" workflow, detail the specific code changes requested, and explicitly demand it returns the path to the generated TDD markdown report.
2. When the `task` tool returns, **verify** the markdown report was actually generated (e.g., use `read_file` to check the file on disk).
3. If the report is missing or incomplete, invoke the `task` tool again with the error and instruct the sub-agent to fix the issue and finish the workflow.

## Sub-Agent Workflow
*(The sub-agent will follow these steps autonomously)*

> **Example Report:** See `.agents/skills/agentic-test-driven-development/resources/report.md` for a complete example of what the generated output and layout should look like.

1. **Pick a timestamp** identifier: `TS=$(date +%Y%m%d_%H%M%S)`. Use it for all
   filenames this run. Create a new directory for this report: `mkdir -p .agents/tdd-reports/$TS`.

2. **Confirm connection:** call `hotswan_get_status`. Abort with guidance if not connected.

3. **Navigate to the target state.** Call `hotswan_get_hierarchy`. If the text/element
   you intend to change is not yet visible, use `adb_shell_input` or standard tools to drive the app to reveal it. Re-read the
   tree to confirm the target is present.

4. **Capture AS-IS:**
   - Call `hotswan_take_screenshot`.
   - Copy or move the returned screenshot file path to `.agents/tdd-reports/$TS/before.png`.
   - Read `.agents/tdd-reports/$TS/before.png` back to confirm it exists.

5. **Make the code change.** Edit the Kotlin source (e.g. files under
   `shared/src/commonMain/kotlin/...` or `androidApp/src/main/...`). Remember the absolute path of the modified file.

6. **Trigger hot reload.** Editing a file on disk does NOT auto-reload. Call the `hotswan_reload` tool and pass the absolute path of the file(s) you modified:
   `hotswan_reload(filePaths=["/absolute/path/to/modified/file.kt"])`

7. **Verify via the semantic tree.** Call `hotswan_get_hierarchy` and confirm the
   node text/state now reflects the change. If it still shows the old value, the
   reload did not land. Debug before continuing. Do not fake success.

8. **Capture CHANGED:**
   - Call `hotswan_take_screenshot`.
   - Copy or move the returned screenshot file path to `.agents/tdd-reports/$TS/after.png`.

9. **Write the report** `.agents/tdd-reports/$TS/report.md` with the helper. Pass the
   image args as the **PNG file paths** (the helper converts them to absolute
   paths in the markdown):
   ```bash
   python3 .agents/scripts/build_tdd_report.py \
     --out ".agents/tdd-reports/$TS/report.md" --ts "$TS" \
     --before ".agents/tdd-reports/$TS/before.png" \
     --after  ".agents/tdd-reports/$TS/after.png" \
     --goal "<one-line description of the change>" \
     --file "<path to edited file>" --line <n> \
     --old '<old source line>' --new '<new source line>' \
     --before-text "<old visible text>" --after-text "<new visible text>"
   ```
   Then **read the generated `.md` back** and confirm both `![]()` image links
   use absolute paths and that the referenced PNGs exist on disk.

10. **Report to the user:** point them to `.agents/tdd-reports/$TS/report.md` and confirm
    the change is shown in the embedded before/after images.

## Failure handling
- **Not connected:** ask the user to start the app via HotSwan; do not substitute a
  full-screen generic `screencapture`.
- **Reload didn't take:** check for compile errors. The hierarchy tree in step 7 is the gate.
