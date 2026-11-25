---
name: fm-debug
description: Debug a FileMaker script by capturing runtime state. At Tier 1 the agent instruments the script and gives the developer run instructions. At Tier 3 the agent can autonomously look up the script source, generate a debug-instrumented copy, deploy it via AppleScript, trigger it via the companion, and read the results — no human intervention required. Triggers on phrases like "debug this", "script not working", "wrong output", "script error", or when a script produces unexpected behavior that cannot be diagnosed from source alone.
compatibility: Tier 3 requires the companion server and macOS Accessibility permission for AppleScript deployment.
---

# fm-debug

Debug a FileMaker script by capturing runtime variable state, error codes, and error locations. The agent's level of autonomy depends on the deployment tier configured in `agent/config/automation.json`.

---

## Step 1: Determine the automation tier

Read `agent/config/automation.json` and check `project_tier` (preferred) or `default_tier`:

- **Tier 1** — the developer runs scripts manually. The agent instruments the script and provides run instructions.
- **Tier 3** — the agent can autonomously deploy and trigger scripts. The agent instruments, deploys, runs, and reads results without developer intervention.

Tier 2 follows the Tier 3 workflow for running scripts (via `/trigger`) but cannot create new scripts autonomously.

---

## Step 2: Identify the diagnosis gap

Before generating any instrumentation:

1. **State specifically what runtime information is needed** — variable values, error codes, script result, which conditional branch was taken, etc.
2. **Check for existing debug output** at `agent/debug/output.json`. If it exists and is recent, read it and skip to Step 5.
3. **Look up the script source** — read the human-readable version from `agent/xml_parsed/scripts_sanitized/` to understand the script's logic and identify where to insert debug instrumentation.

---

## Step 3: Instrument the script

### Critical: error data capture pattern

`Get ( LastError )` resets the error state as a side effect. Once evaluated, `Get ( LastErrorLocation )` and `Get ( LastErrorDetail )` can no longer return data for that error. **All three must be captured in a single expression within one `Set Variable` step:**

```
Set Variable [ $errData ; JSONSetElement ( "{}" ;
    [ "lastError" ; Get ( LastError ) ; JSONNumber ] ;
    [ "lastErrorDetail" ; Get ( LastErrorDetail ) ; JSONString ] ;
    [ "lastErrorLocation" ; Get ( LastErrorLocation ) ; JSONString ]
) ]
```

When this pattern is used, `Get ( LastErrorLocation )` returns `"ScriptName\rStepName\rLineNumber"` (carriage-return separated).

**Never capture error data in separate steps** — the first `Set Variable` clears the error for subsequent ones. See `agent/docs/knowledge/error-data-capture.md` for full details.

Additionally, `Perform Script` resets `Get ( LastError )` to 0 when it successfully begins executing the subscript. The Agentic-fm Debug script's own error capture always sees `lastError = 0`. **Callers must capture error data in the calling script and pass it as part of the JSON parameter.**

### Building the instrumented script

Look up the target script's ID from CONTEXT.json or the scripts index:

```bash
grep "ScriptName" "agent/context/{solution}/scripts.index"
```

Read the human-readable source from `agent/xml_parsed/scripts_sanitized/` to understand the logic. Identify where to insert debug capture points — typically immediately after steps that might fail or at decision points.

Generate a modified copy of the script as fmxmlsnippet XML in `agent/sandbox/` that includes debug instrumentation at the identified points. Each debug point should:

1. Capture error data in a single expression (the `$errData` pattern above)
2. Capture any relevant local variables
3. Call `Perform Script [ "Agentic-fm Debug" ]` with the captured state as a JSON parameter

Example debug instrumentation to insert after a risky step:

```
# Capture error data in ONE expression — Get(LastError) resets the error state
Set Variable [ $errData ; JSONSetElement ( "{}" ;
    [ "lastError" ; Get ( LastError ) ; JSONNumber ] ;
    [ "lastErrorDetail" ; Get ( LastErrorDetail ) ; JSONString ] ;
    [ "lastErrorLocation" ; Get ( LastErrorLocation ) ; JSONString ]
) ]
Perform Script [ "Agentic-fm Debug" ; Parameter: JSONSetElement ( "{}" ;
    [ "label" ; "after the risky step" ; JSONString ] ;
    [ "vars"  ; JSONSetElement ( "{}" ;
        [ "errData"  ; $errData  ; JSONRaw ] ;
        [ "myVar"    ; $myVar    ; JSONString ] ;
        [ "otherVar" ; $otherVar ; JSONString ]
    ) ; JSONRaw ]
) ]
```

Validate the instrumented script with `validate_snippet.py` before proceeding.

---

## Step 4: Deploy and run

### Tier 3 (autonomous)

The agent has the full deploy → run → read loop available:

1. **Load clipboard** — `POST {companion_url}/clipboard` with the XML
2. **Deploy via raw AppleScript** — `POST {companion_url}/trigger` with a `raw_applescript` payload that:
   - Activates FM Pro and switches to standard menus
   - Opens Script Workspace
   - Uses Cmd+N → Rename to create the debug script (if new), OR uses AXPress to open the existing script tab and Cmd+A → Delete → Cmd+V to replace (if modifying)
   - Saves with Cmd+S
3. **Run the script** — `POST {companion_url}/trigger` with `fm_app_name`, `script`, and optionally `target_file`
4. **Read the output** — read `agent/debug/output.json` (allow 2–3 seconds for the script to execute and the companion to write the file)

**Prerequisites for Tier 3 autonomous debugging:**
- `fmextscriptaccess` extended privilege must be enabled on the active account's privilege set in the frontmost FM document (required for `/trigger` `do script` calls)
- The companion server must be running on the host and reachable at `companion_url`
- Agentic-fm Debug script must be installed in the solution

**Important**: if deploying an instrumented copy of an existing script, use `--replace` mode (Cmd+A → Delete → Cmd+V) rather than creating a new script. After debugging, deploy the original script back to restore it.

### Tier 1 (developer-assisted)

Give the developer clear instructions:

> To debug this, I need runtime variable state. Please do the following:
>
> 1. The instrumented script is on your clipboard. Open **"Script Name"** in Script Workspace
> 2. **Cmd+A** — select all existing steps and delete
> 3. **Cmd+V** — paste the instrumented version
> 4. Run the script as you normally would
> 5. Let me know when it's done — I'll read `agent/debug/output.json` directly.

After debugging, provide the original script back on the clipboard for the developer to restore.

---

## Step 5: Read and analyze the output

Read `agent/debug/output.json`:

```bash
cat agent/debug/output.json
```

The output contains:
- **`vars`** — the variables and error data captured by the instrumented script. **This is the authoritative diagnostic data.** The `errData` object within `vars` contains `lastError`, `lastErrorDetail`, and `lastErrorLocation` as captured by the calling script.
- **Top-level `lastError`/`lastErrorLocation`** — captured by the debug script itself. Always 0/empty because `Perform Script` resets the error state. Ignore these for diagnosis.
- **`timestamp`** — when the debug script ran
- **`label`** — description of the debug point

Parse the error data and identify the root cause. Explain the issue clearly and propose the fix.

---

## Fallback: $$DEBUG Global Variable

If the solution does not have an Agentic-fm Debug script, the developer can add a temporary `Set Variable` step to collect debug state into a `$$DEBUG` global:

```
Set Variable [ $$DEBUG ; JSONSetElement ( "{}" ;
    [ "errData" ; JSONSetElement ( "{}" ;
        [ "lastError" ; Get ( LastError ) ; JSONNumber ] ;
        [ "lastErrorDetail" ; Get ( LastErrorDetail ) ; JSONString ] ;
        [ "lastErrorLocation" ; Get ( LastErrorLocation ) ; JSONString ]
    ) ; JSONRaw ] ;
    [ "varName1" ; $varName1 ; JSONString ] ;
    [ "varName2" ; $varName2 ; JSONString ]
) ]
```

The developer retrieves the value from the Data Viewer (Tools > Data Viewer) and pastes it into the conversation.

---

## After diagnosis

1. Explain the root cause clearly
2. Propose and generate the fix
3. **Restore the original script** — if the script was modified for debugging, deploy the original version back (Tier 3: autonomous restore; Tier 1: clipboard with paste instructions)
4. If the Agentic-fm Debug script doesn't exist yet, offer to help create it (see `agent/docs/AGENTIC_DEBUG.md`)
