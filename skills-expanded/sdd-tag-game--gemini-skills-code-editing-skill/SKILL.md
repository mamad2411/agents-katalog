---
name: code-editing
description: MANDATORY for modifying existing files containing code, configuration, or documentation. Enforces the "Conflict Marker Injection" workflow to allow for safe, surgical, and reviewable changes using Git-style conflict markers. Trigger this whenever you are asked to change, refactor, or fix logic within an existing file.
---

# Code Editing (Conflict Marker Injection Protocol)

You are an automated coding assistant that prioritizes safety and reviewability. You NEVER destructively overwrite existing code. Instead, you propose changes using standard Git conflict markers directly inside the target file.

## ⚠️ Trigger & Scope (CRITICAL)

**Apply this workflow ONLY if ALL the following are true:**

1.  **Existing File:** The target file already exists in the file system.
2.  **Code Context:** The file contains executable code (e.g., `.py`, `.js`, `.ts`, `.go`), strict configuration (e.g., `.json`, `.yaml`), or documentation (`.md`).
3.  **Modification Request:** The user is asking to change, refactor, or fix logic within that file.

**For all other requests (e.g., writing new documentation, creating NEW files from scratch, explaining concepts, or general chat), DO NOT use conflict markers.** Simply overwrite or create the file as a standard assistant would.

## Operational Steps

1.  **Analyze the Request:** Identify the specific file and lines of code that require modification.
2.  **Scope the Block:** Isolate the smallest possible context window for the change. The conflict marker blocks must be **as small as possible**. Avoid wrapping large sections of unchanged code.
3.  **Construct the Injection:** Create the conflict block using this exact format:

```text
<<<<<<< HEAD
[Original Code currently in the file]
=======
[Your Proposed Change]
>>>>>>> [short-descriptive-slug-for-this-change]
```

4.  **Insertions Only:** If the change is **ONLY inserting lines**, the top half (between `<<<<<<< HEAD` and `=======`) **MUST be empty**.
5.  **Execute Injection:** Use your file editing tools (e.g., `replace`) to update the file with the conflict block. **Do not output or preview this code block in the chat.**
6.  **Await Review:** Confirm to the user that the injection is complete and wait for their input.

## Constraints & Rules

- **Zero Overwrites:** Never change code without wrapping it in conflict markers unless explicitly told to "force" a change.
- **Surgical Precision:** Conflict markers must cover **AS FEW LINES AS POSSIBLE**.
- **No Chat Previews:** Never print the code block in the chat window. The user will read it in their own editor.
- **One Block at a Time:** If multiple changes are needed in different parts of a file, propose them sequentially or ensure they are distinct, non-overlapping blocks.
- **Descriptive IDs:** Use a context-aware slug for the marker (e.g., `refactor-auth-logic`).

## Output Format

After injecting the code, your text output to the user must be strictly limited to this confirmation:

> "✅ **Change Injected:** `[File Name]`
>
> I have inserted a conflict marker for `[Short Description of Change]`. Please review the file, resolve the conflict, and let me know when to proceed or if adjustments are needed."

## Examples

### Example 1: Modifying a single line

```text
<<<<<<< HEAD
const MAX_RETRIES = 3;
=======
const MAX_RETRIES = 5;
>>>>>>> increase-max-retries
```

### Example 2: Inserting new code

```text
<<<<<<< HEAD
=======
function initializeService() {
  console.log("Service initialized.");
}

>>>>>>> add-initialize-service
```
