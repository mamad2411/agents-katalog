---
user-invocable: true
description: Add field definitions to existing research outline.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---
> **Attribution:** Originally authored by [Weizhena](https://github.com/Weizhena/Deep-Research-skills). Included with attribution for use in the Deep query workflow.

# Research Add Fields - Add Research Fields

## Trigger Method
`/research-add-fields`

## Execution Flow

### Step 1: Auto-locate Fields File
Search for `*/fields.yaml` file in the current working directory and automatically read existing field definitions.

### Step 2: Get Supplement Source
Ask user to choose:
- **A. Direct User Input**: User provides field names and descriptions
- **B. Web Search**: Launch web-search-agent to search for commonly used fields in this domain

### Step 3: Display and Confirm
- Display the list of suggested new fields
- User confirms which fields need to be added
- User specifies field categories and detail_level

### Step 4: Save Updates
Append confirmed fields to fields.yaml and save the file.

## Output
Updated `{topic}/fields.yaml` file (in-place modification, requires user confirmation)