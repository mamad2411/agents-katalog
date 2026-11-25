---
name: ollama-sync
version: 1.0.0
description: 'Synchronizes the list of available models in the ''opencode.json'' configuration
  file''s ''ollama'' provider models list with the actual models available on the
  system via the ''ollama list'' command.

  '
license: MIT
compatibility: opencode
allowed-tools:
- bash
- read
- edit
---

# Ollama Model Synchronizer

## Your Task
When asked to synchronize the local Ollama configuration, your primary goal is to ensure that the model list in the `opencode.json` file is an accurate reflection of the models available on the host system.

The process must involve three main steps:

1. **Fetch Live List:** Execute `ollama list` via the bash tool to retrieve all currently available model names and tags on the machine.
2. **Parse and Extract:** Parse the output of `ollama list` to extract only the clean list of model names (e.g., `llama2`, `mistral`).
3. **Update Config:** Use the `edit` tool to replace the existing model list in `opencode.json` (specifically the `ollama` provider section) with the newly fetched, accurate list.

## Workflow Details

1. **Primary Command Execution:**
   - Run `ollama list` using the `bash` tool.
2. **Parsing Logic (Internal):**
   - The output of `ollama list` needs to be parsed to isolate model names. Assume the output format is reliable enough to grep for model names.
3. **File Manipulation:**
   - Use the `read` tool on `opencode.json` to understand the current structure.
   - Use the `edit` tool to modify the specific section containing the model list.

### Step-by-step Logic
1. **Check Dependency:** Confirm if the `ollama` command is available in the execution environment.
2. **Get System Models:** Execute `ollama list` to get the current list of models.
3. **Isolate Names:** Programmatically parse the output to create a comma-separated string of model names.
4. **Write Back:** Use the `edit` tool to replace the old model list with the new comma-separated list in `opencode.json`.

## Examples & Edge Cases
*   **Empty List:** If `ollama list` returns no models, the `opencode.json` model list should be cleared or set to an empty array, and the user should be warned.
*   **Error Handling:** If the `ollama` command fails or is not found, the process must stop, and the user should be informed that the synchronization failed due to environment issues.

## Target File Structure (Conceptual)
The target file is `opencode.json`. The relevant section looks like this (structure for context):

```json
"providers": {
    "ollama": {
        "models": ["model-a", "model-b", "model-c"], // <-- This list must be updated
        "base_url": "http://localhost:11434"
    },
    // ... other providers
}
```

Always prioritize using the `bash` tool for OS interactions (`ollama list`) and the `edit` tool for configuration management.
---
