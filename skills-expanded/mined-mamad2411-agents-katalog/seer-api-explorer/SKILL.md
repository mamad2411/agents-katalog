---
name: seer-api-explorer
version: 0.2.0
description: Discover and explore Seer API commands via schema introspection
metadata: {"requires":{"bins":["seer-q"]}}
---

# Seer API Explorer

> Read [seer-shared](../seer-shared/SKILL.md) for response format and common rules.

Use this skill when the user's need is **not covered by existing Seer skills**. Before using this skill, check if `seer-market` already has the command you need.

## When to Use

- User asks about a command you don't recognize
- User needs data that existing skills don't document
- You want to discover what commands are available
- You need to understand a command's exact input/output contract

## Discovery Flow

### Step 1: Check existing skills first

If the user's question maps to a known command in `seer-market`, use that skill directly. Only proceed here if it doesn't.

### Step 2: List all commands

```bash
seer-q schema
```

Returns every registered command with its description, arguments, and flags. Use this to find the right command for the user's need.

### Step 3: Inspect a specific command

```bash
seer-q schema <command>
```

Returns the full contract for one command: positional arguments, flags with defaults, and response shape description. Use this to understand exactly what to pass and what to expect.

### Step 4: Call with raw output

```bash
seer-q <command> [args] [flags] --raw
```

The `--raw` flag bypasses the envelope and returns the API response directly. This is useful for:
- Inspecting the full response structure when the envelope obscures it
- Debugging unexpected output
- Exploring fields not documented in skills

### Step 5: Interpret and synthesize

After receiving the response:
1. Parse the JSON (remember: `.data` contains the payload if not using `--raw`)
2. Identify the relevant fields for the user's question
3. Synthesize into natural language
4. Include any `view_url` found in the response

## Example

User: "what stages does Seer use for processing?"
1. Not covered by seer-market → use API explorer
2. `seer-q schema decisions` → discover `--stage` flag and its allowed values
3. `seer-q decisions --limit 5` → see real stage names in output
4. Summarize the processing stages found
