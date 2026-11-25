---
name: json-data-transform
description: Parse, extract, and transform JSON data with JSONPath queries
---

# JSON Data Transform

Parse, extract, and transform JSON data with JSONPath queries

## When to Use

- User wants to json transform
- User wants to parse json
- User wants to extract json
- Keywords: json, transform, parse, extract

## Required Parameters

- **input_json** (string): JSON string to process
- **jsonpath** (string): JSONPath expression to extract

## Output

- **extracted** (string): Extracted value
- **type** (string): Type of extracted value

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `parse` -> 5 steps -> Exit: `ret_ok`, `ret_fail`
