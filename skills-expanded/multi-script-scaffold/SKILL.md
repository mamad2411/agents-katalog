---
name: multi-script-scaffold
description: Implements the Untitled Placeholder Technique for multi-script systems. Guides the developer through creating N placeholder scripts in FM, captures their IDs via Push Context, then generates all scripts with correct Perform Script wiring in one pass. Use when the user wants to scaffold a set of interdependent scripts. Triggers on phrases like "multi-script", "scaffold scripts", "placeholder technique", "untitled placeholder", or "build a script system".
---

# Multi-Script Scaffold

Implements the Untitled Placeholder Technique: create N placeholders → capture IDs → generate all scripts with correct wiring → deploy → rename.

---

## Step 1: Understand the script system

If the developer has not already described the scripts to build, ask:

- How many scripts are needed?
- What does each script do (name + purpose)?
- Which scripts call which (the dependency graph)?

Build a simple dependency table, e.g.:

| # | Script Name | Calls |
|---|---|---|
| 1 | Process Invoice | Invoice - Validate, Invoice - Save |
| 2 | Invoice - Validate | — |
| 3 | Invoice - Save | — |

Confirm this with the developer before proceeding.

---

## Step 2: Read CONTEXT.json

Read `agent/CONTEXT.json`. Extract:
- `solution` — for resolving automation config
- `scripts` — check if any of the target scripts already exist (by name); if so, note their IDs — those scripts do NOT need placeholders
- `current_layout` — for context during generation

Identify how many **new** placeholders are needed (exclude any scripts that already exist in CONTEXT.json).

---

## Step 3: Instruct placeholder creation (Tier 1/2) or auto-create (Tier 3)

Read `agent/config/automation.json` to determine the active deployment tier.

### Tier 1 or Tier 2

Tell the developer:

> In FileMaker Script Workspace, click the **+** button **N** times. FileMaker will name each one `New Script`.
> **Before running Push Context**, rename each placeholder to its final name:
>
> | New Script # | Rename to |
> |---|---|
> | 1st | Script Name A |
> | 2nd | Script Name B |
> | … | … |
>
> Once all N scripts are renamed, run **Push Context** (Scripts menu → agentic-fm → Push Context) with the task description:
> `"Scaffold: [brief description]"`
>
> **Why rename first?** FileMaker names every new script `New Script`. Push Context keys scripts by name — if multiple scripts share the same name, only the last one's ID is captured.

Wait for the developer to confirm Push Context has run.

### Tier 3

Confirm with the developer before proceeding:

> I'll use AppleScript to create **N** placeholder scripts in the Script Workspace with their final names, then run Push Context automatically. Ready to proceed?

If confirmed, trigger placeholder creation via `POST {companion_url}/trigger` with:
```json
{ "fm_app_name": "...", "script": "AGFMScriptBridge", "parameter": "{\"script\": \"...\", \"parameter\": \"...\"}" }
```
(Consult `SKILL_INTERFACES.md` for the full Tier 3 AppleScript path. At Tier 3, AppleScript creates scripts with their final names directly — no rename step needed.)

---

## Step 4: Re-read CONTEXT.json (capture placeholder IDs)

After the developer confirms Push Context has run, re-read `agent/CONTEXT.json`.

Locate the newly created `Untitled`, `Untitled 2`, … `Untitled N` scripts in the `scripts` object and extract their IDs.

Build the assignment map — which placeholder ID maps to which target script:

| Placeholder | ID | Will become |
|---|---|---|
| Untitled | 301 | Process Invoice |
| Untitled 2 | 302 | Invoice - Validate |
| Untitled 3 | 303 | Invoice - Save |

Confirm the mapping with the developer if there is any ambiguity (e.g. more Untitled scripts than expected).

---

## Step 5: Generate all scripts

With all IDs resolved, generate every script as fmxmlsnippet XML written to `agent/sandbox/`.

**Naming convention**: `{Script Name}.xml` (spaces replaced with underscores or hyphens, developer preference).

Rules:
1. Use the real numeric IDs from the placeholder map for all `<Script id="N" name="..."/>` references in Perform Script steps.
2. Follow all conventions in `agent/docs/CODING_CONVENTIONS.md`.
3. Grep the step catalog for every step type used.
4. Validate each file with `python3 agent/scripts/validate_snippet.py agent/sandbox/<file>.xml` before proceeding to deployment.

Fix any validation errors before continuing.

---

## Step 6: Webviewer output (if available)

Check webviewer availability:
```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://localhost:8080
```

If reachable (HTTP 200), push each script as a `preview` payload:
```bash
curl -s -X POST http://local.hub:8765/webviewer/push \
  -H "Content-Type: application/json" \
  -d '{"type": "preview", "content": "<HR script text>"}'
```

Push scripts sequentially so the developer can review each in Monaco before deployment begins.

If not reachable, output each script in HR format to the terminal.

---

## Step 7: Deploy

Deploy each script using `agent/scripts/deploy.py`, targeting its corresponding placeholder by script name.

**Tier 1**: For each script:
```bash
python3 agent/scripts/deploy.py agent/sandbox/<Script Name>.xml "<Placeholder Name>"
```
Present instructions in the standard format:

> The script is on your clipboard. To install it:
>
> 1. Open **Untitled [N]** in Script Workspace
> 2. **⌘A** — select all existing steps
> 3. **⌘V** — paste

Repeat for each script. Present all paste instructions up front so the developer can work through them in sequence without waiting.

**Tier 2**: `deploy.py` auto-pastes into each placeholder. Confirm success for each before moving to the next.

**Tier 3**: `deploy.py` handles everything. Report result per script.

---

## Step 8: Final verification (optional)

Suggest running a context refresh after renaming to confirm all script IDs are correctly wired:

> Once you've renamed all scripts, run **Push Context** again and I can verify the IDs match the wiring in the generated scripts.

---

## Notes

- **Always confirm** the placeholder-to-script mapping before generating code — a wrong assignment means all Perform Script calls in that script will target the wrong script.
- If the developer has already created scripts in a prior session and knows the IDs, skip Steps 3–4 and use those IDs directly.
- Scripts with no inter-script dependencies can be generated without placeholders — use existing IDs from CONTEXT.json directly.
- The webviewer push is per-script, not a batch — send one preview per script so the developer can review them in sequence.
