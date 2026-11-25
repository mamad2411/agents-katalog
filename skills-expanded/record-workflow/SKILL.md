---
name: record-workflow
description: >
  Record an automation workflow by performing actions, then replay it later as a playbook.
  Capture clicks, typing, navigation into reusable sequences. Use when: "record this",
  "capture steps", "make repeatable", "save automation", "create playbook", "record and replay",
  "macro", "record workflow".
disable-model-invocation: true
allowed-tools:
  - mcp__sh__playbook_record
  - mcp__sh__export_playbook
  - mcp__sh__platform_guide
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_query_patterns
  - mcp__sh__job_create
  - mcp__sh__job_run
  - mcp__sh__job_status
---

# Workflow Recording & Replay

You are recording a desktop or browser automation workflow into a reusable playbook, then replaying it via the job system.

## Intelligence Wrapper

Every tool call returns automatic hints. The recording system (`playbook_record`) works with the intelligence wrapper — when recording is active, `mcpRecorder.captureToolCall()` captures each tool call as a playbook step. Watch for `[HINT]`, `[WARNING]`, and `[STRATEGY]` lines for guidance.

## Existing Playbooks

Before recording a new workflow, check if one already exists:
- `memory_recall(task="record {workflow}")` — check past recordings
- `memory_query_patterns(scope="{platform}")` — check verified patterns

**Available playbooks**: x-twitter, linkedin, instagram, reddit, threads, youtube, discord, davinci-color-grade, davinci-edit-timeline, davinci-render, google-flow-create-project, google-flow-generate-image, google-flow-generate-video, google-flow-edit-image, google-flow-edit-video, google-flow-open-project, google-flow-search-assets, codex-desktop.

## Recording a Workflow

### Start Recording
```
playbook_record(action="start", platform="{platform_name}")
```
- `platform` is a label (e.g., "gmail-compose", "slack-message", "figma-export")
- From this point, tool calls made within the SAME MCP server session are captured as playbook steps via the intelligence wrapper's `mcpRecorder.captureToolCall()`.

**Important**: Recording works within a single MCP server session. Because Claude Code may restart the MCP server between tool calls, recording is best suited for workflows done in quick succession. For long multi-step workflows, consider using `export_playbook` after the session instead — it reconstructs the playbook from session memory (actions.jsonl).

### Perform the Workflow
Now execute the workflow normally using any ScreenHand tools. For example:
- `browser_navigate` → captured as `navigate` step
- `browser_click` → captured as `browser_click` step
- `browser_fill_form` → captured as `browser_type` step
- `ui_press` → captured as `press` step
- `key` → captured as `key_combo` step
- `menu_click` → captured as `menu_click` step
- `type_text` → captured as `type_into` step

### Check Recording Status
```
playbook_record(action="status")
```
Shows how many steps have been captured so far.

### Stop Recording & Save
```
playbook_record(action="stop", name="{workflow_name}")
```
- Saves to `playbooks/{workflow_name}.json`
- The playbook is immediately available for replay

## Replaying a Workflow

### As a Job (recommended)
```
job_create(task="Replay: {description}", playbookId="{workflow_name}")
job_run(jobId="{id}")
```

The job system executes each playbook step through the PlaybookEngine with:
- Variable substitution (`{VAR_NAME}` in step fields)
- Optional popup detection (if observer is running)
- Automatic verification after each step
- Error handling with retry

### Check Replay Progress
```
job_status(jobId="{id}")
```
Shows which steps completed, which are pending, any errors.

## Exporting Platform Knowledge

After exploring a platform (manually or via `platform_explore`), export what you learned:

```
export_playbook(platform="{name}", domain="{domain.com}")
```

This extracts from your session memory:
- URLs visited
- Selectors that worked
- Errors encountered and resolutions
- Strategies used

Output is saved to `references/{platform}.json` — usable by `platform_guide` in future sessions.

## Editing Playbooks

The saved playbook JSON can be hand-edited. Structure:

```json
{
  "platform": "my-workflow",
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com",
      "description": "Open the site"
    },
    {
      "action": "press",
      "target": "Login",
      "description": "Click login button"
    },
    {
      "action": "type_into",
      "target": "input[name='email']",
      "text": "{EMAIL}",
      "description": "Enter email"
    },
    {
      "action": "key_combo",
      "keys": "enter",
      "description": "Submit form"
    }
  ]
}
```

### Supported Action Types
`navigate`, `press`, `type_into`, `extract`, `key`, `key_combo`, `menu_click`, `scroll`, `wait`, `screenshot`, `browser_js`, `browser_click`, `browser_type`, `browser_human_click`, `cdp_key_event`

### Variables
Use `{VAR_NAME}` in any step field. Pass values via `job_create(vars={VAR_NAME: "value"})`.

### Optional Steps
Add `"optional": true` to a step — failure continues instead of aborting.

### Verification
Add `"verify": "selector"` to a step — after execution, checks if the selector exists.

## Best Practices

1. **Name playbooks descriptively**: `slack-send-message`, `figma-export-png`, `gmail-compose-reply`
2. **Use variables for dynamic data**: `{POST_TEXT}`, `{EMAIL}`, `{FILE_PATH}`
3. **Add descriptions to each step**: Makes the playbook readable and debuggable
4. **Record on a clean state**: Start from a known state (fresh page load, app just launched)
5. **Test replay immediately**: After recording, replay once to verify it works

$ARGUMENTS
