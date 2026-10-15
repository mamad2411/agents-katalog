---
name: calicat-cli-operator
description: Use when an AI agent needs to operate the local Calicat CLI to extract design data, interaction data, PRD data, canvas/page structure, or screenshots from Calicat links or file ids. Trigger especially when the user provides a Calicat design URL, asks the agent to parse file_id, canvas id, or layer id correctly, or asks for whole-canvas frontend implementation that must fetch page data progressively instead of loading all design JSON at once. Also use when the agent needs to verify whether the local Calicat CLI is installed, check its version, or decide whether CLI update/install guidance is needed before continuing.
---

# Calicat CLI Design Data

Use this skill when the user wants data from a Calicat file and the local `calicat` CLI is the execution path.

## Read This File For

- skill trigger conditions
- link-form detection
- progressive retrieval rules
- task routing by user intent

## Read Extra References Only When Needed

- If the task depends on making sure the CLI is installed, checking its version, updating it, or telling another agent/user how to install/update it, read [references/cli-lifecycle.md](references/cli-lifecycle.md).

## Link Parsing

Calicat design links commonly appear in three forms.

### File only

```text
https://www.calicat.cn/design/2066708151519244288
```

Parse as:

- `file_id = 2066708151519244288`
- `canvas_id = unknown`
- `selected_layer_id = unknown`

Meaning:

- The user identified the file, but not a specific canvas or layer.
- If the task is canvas-specific, call `get_canvas_list` first.

### Canvas link

```text
https://www.calicat.cn/design/2066708151519244288?node-id=2066708151531827200&node-type=canvas
```

Parse as:

- `file_id = 2066708151519244288`
- `canvas_id = 2066708151531827200`
- `selected_layer_id = unknown`

Meaning:

- Here `node-id` is the canvas id.
- Do not send this `node-id` to `get_meta_data` or `get_design_data` as if it were a layer id.
- For canvas-wide work, go straight to `get_design_page_list` with that `canvas_id`.

### Layer link

```text
https://www.calicat.cn/design/2066708151519244288?node-id=21c84811-08c9-42f6-9dc7-82c6992a6ae8&node-type=group
```

Parse as:

- `file_id = 2066708151519244288`
- `selected_layer_id = 21c84811-08c9-42f6-9dc7-82c6992a6ae8`
- `canvas_id = unknown`

Meaning:

- Here `node-id` is a layer id.
- `node-type=group` is a strong hint that this is a layer-like object, not a canvas.
- Start with `get_meta_data`, then decide whether to read full design data.

## Parsing Rules

- Always extract `file_id` from `/design/{file_id}` first.
- If `node-type=canvas`, treat `node-id` as `canvas_id`.
- If `node-type` exists and is not `canvas`, treat `node-id` as `selected_layer_id`.
- If `node-id` exists but `node-type` is missing, do not guess immediately:
  - if the id looks like a UUID, it is usually a layer id
  - if the id is a long numeric string, it may be a canvas id
  - but when the next step matters, verify by choosing the lightest safe API path

## Safe Resolution Strategy

When the link is ambiguous:

- Parse `file_id`.
- Inspect `node-type`.
- If still ambiguous, prefer canvas discovery before large reads.
- Do not force a layer workflow on a probable canvas link.

## Core Rule

Prefer progressive retrieval.

Large `get_design_data` payloads can easily blow up context. Start with the lightest structure endpoint that answers the next decision:

- `get_canvas_list`
- `get_design_page_list`
- `get_meta_data`
- `get_design_data`
- `get_interaction_design_data`

Treat this as directory first, full content later.

### API Selection: get_meta_data vs. get_design_data

- `get_meta_data`: Retrieves simplified page/layer structure (layer names, IDs, positions, dimensions) with the hierarchy represented in XML format. Use this to quickly inspect layer outlines, map out canvas structures, or locate specific nested elements without loading heavy style payloads.
- `get_design_data`: Retrieves the complete layout and deep CSS/styling values. Use this to generate precise code or perform styling analysis.
- **Direct Fetch Rule**: If the target page layer ID is already determined (e.g. from `get_design_page_list`) and your goal is frontend code implementation for that page, do not call `get_meta_data` first. Call `get_design_data` directly on the page ID.

### Payload Storage & Context Management

Large payloads from `get_design_data` can easily overwhelm the LLM's context window. Directly outputting massive JSON payloads to the terminal pollutes the context, causing slow responses, high token costs, and potential token overflow.

To keep the LLM context clean and performance optimal:

- **Redirect Output to File**: Always redirect large output payloads to a temporary file within the workspace (e.g., `scratch/page_design.json` or `temp_design.json`).
  - Unix Bash/Zsh:
    ```bash
    calicat tools-call --name get_design_data --args '{"file_id":"123","selected_layer_id":"xyz"}' > scratch/page_design.json
    ```
  - PowerShell:
    ```powershell
    $json = '{\"file_id\":\"123\",\"selected_layer_id\":\"xyz\"}'
    calicat tools-call --name get_design_data --args $json > scratch/page_design.json
    ```
- **Strict Data-Driven Implementation (No Guessing or Hallucinations)**:
  - Do not start implementing full frontend code based on incomplete design data or placeholders. Coding must strictly correspond to the actual page design data and user requirements. Guessing leads to design-code mismatches.
  - Implement design layouts page-by-page. A single page's `design_data` is typically small enough to not overflow the context. Alternatively, locate the target modular component/container, extract its specific node data first, and develop that segment.
- **Handling Giant JSON Files (Splitting to Prevent Harness Truncation)**:
  - If the output file is extremely large, do not attempt to read or display the entire file in a single turn. Reading huge files directly will trigger the agent harness truncation.
  - Write a simple parsing script (e.g., in Python or NodeJS) to split the giant JSON file into smaller, logical files (e.g., by single component, screen section, or layout tree depth) saved under `scratch/`.
  - Process and build code from these smaller split JSON files one by one.
- **Progressive and Targeted Reading**: Once saved, do not read the entire file into the context at once. Use standard workspace file-viewing tools with line limits (e.g., `view_file` with specific range offsets), or write a small script (e.g., Python/JS) to parse and filter the JSON down to the specific UI node details required for coding.

## Minimal CLI Surface

List tools:

```bash
calicat tools-list
```

### Windows Shell JSON Argument Escaping

If the execution environment is Windows (PowerShell or CMD), passing raw JSON objects inside single quotes can lead to argument parsing issues (such as quotes being stripped). Follow these escaping rules:

- **PowerShell**: Declare the JSON string in a variable, escape internal double quotes with a backslash (`\`), and pass the variable.
  ```powershell
  $json = '{\"file_id\":\"2045068433773035520\",\"selected_layer_id\":\"e449643f-0bc3-4b75-9fa4-9db5c0b0e402\"}'
  calicat tools-call --name get_meta_data --args $json
  ```
- **CMD**: Wrap the entire arguments object in double quotes and escape internal double quotes with a backslash (`\"`).
  ```cmd
  calicat tools-call --name get_meta_data --args "{\"file_id\":\"2045068433773035520\",\"selected_layer_id\":\"e449643f-0bc3-4b75-9fa4-9db5c0b0e402\"}"
  ```

### CLI Command Examples (Unix-like Bash/Zsh)

Canvas list:

```bash
calicat tools-call --name get_canvas_list --args '{"file_id":"123456"}'
```

Page list:

```bash
calicat tools-call --name get_design_page_list --args '{"file_id":"123456","canvas_id":"canvas-id"}'
```

Layer meta:

```bash
calicat tools-call --name get_meta_data --args '{"file_id":"123456","selected_layer_id":"layer-uuid"}'
```

Layer design data:

```bash
calicat tools-call --name get_design_data --args '{"file_id":"123456","selected_layer_id":"layer-uuid"}'
```

Interaction design:

```bash
calicat tools-call --name get_interaction_design_data --args '{"file_id":"123456","selected_layer_id":"layer-uuid"}'
```

PRD list:

```bash
calicat tools-call --name get_prd_list --args '{"file_id":"123456"}'
```

PRD full content:

```bash
calicat tools-call --name get_prd_full_content --args '{"file_id":"123456","prd_id":"prd-id"}'
```

## Recommended Workflow By Task

### Single layer design analysis

Use when the user gives a design URL and asks for one layer's design or interaction data.

Workflow:

- Parse the link shape first.
- Confirm that the link actually points to a layer, not a canvas.
- Call `get_meta_data`.
- Confirm the layer looks like the target.
- Call `get_design_data`.
- If interaction matters, call `get_interaction_design_data`.

### Canvas-level work

Use when the user asks for “这个画布”, “当前画布”, or asks to process all pages inside a canvas.

Workflow:

- Parse the link shape first.
- If the URL contains `node-id` and `node-type=canvas`, treat `node-id` as `canvas_id`.
- If the URL does not contain `node-id` (e.g., file-only link) or `node-id` is ambiguous:
  - Call `get_canvas_list` to fetch the list of all canvases for the file.
  - Determine the target `canvas_id` from the list (ask the user to select, or infer based on context/defaults).
- Call `get_design_page_list` using the resolved `canvas_id` to fetch the list of pages.
- Process one page layer at a time.
- For each page:
  - If the goal is frontend code implementation, directly call `get_design_data` using the page ID (skip `get_meta_data`). Always redirect the output to a temporary JSON file to avoid polluting the prompt context.
  - Otherwise, call `get_meta_data` first if you only need to inspect page skeletal outlines or locate specific component layers before deciding what to fetch.

### Requirement card retrieval

Use when the user asks for requirements, PRDs, summaries, or requirement card content.

Workflow:

- Parse `file_id`.
- Call `get_prd_list`.
- Match by title or summary.
- Call `get_prd_full_content`.

Never guess `prd_id` first.

### Full canvas frontend implementation

Use when the user asks to build frontend code for “all designs”, “all pages”, or “the whole canvas”.

Workflow:

- Resolve `file_id`.
- Resolve `canvas_id` (if the URL does not contain `node-id`, call `get_canvas_list` first to list all canvases and select the target).
- Call `get_design_page_list` using the resolved `canvas_id` to fetch the list of pages.
- Process one page layer at a time.
- For each page, directly call `get_design_data` (always redirect the output to a temporary JSON file to avoid polluting the prompt context) to get the complete styling details, and then implement/summarize the code. Skip `get_meta_data`.
- Move to the next page only after finishing the current one.

Do not fetch all page design data in a single pass.

Default batch size:

- 1 page per step
- 2 pages only if payloads are clearly small

## Decision Heuristics

If the user says:

- “这个链接里的图层”
  use the layer path
- “这个链接里的画布”
  use the canvas path
- “这个文件里的 PRD”
  use `file_id`, then `get_prd_list`
- “这个画布里的所有页面”
  resolve `canvas_id`, then `get_design_page_list`
- “把整个设计做成前端”
  do not pull everything at once; page-by-page retrieval is mandatory

## Failure Handling

If data access fails:

- Run `calicat status`.
- If auth looks stale, run `calicat logout` then `calicat login`.
- Re-check parsed `file_id`, `canvas_id`, and `node-id`.
- If the task depends on install/update/version state, read `references/cli-lifecycle.md`.

## Output Style

When reporting back to the user:

- explicitly say which ids you parsed
- explicitly say which CLI calls you made
- explicitly say whether the link pointed to a file, canvas, or layer
- if you use progressive retrieval, explain that you are avoiding loading huge design JSON all at once
