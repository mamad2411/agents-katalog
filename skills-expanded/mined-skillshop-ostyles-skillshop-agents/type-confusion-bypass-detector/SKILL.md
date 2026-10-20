---
name: type-confusion-bypass-detector
description: "Type confusion bypass detector: traces validation paths from input source to storage/execution sink, tests edge-case input shapes (str/int/obj/null/array), and LLM judges which input shape circumvents each validator and what happens at the query/execution sink. Read-only. Audience: Senior. Trigger: /bypass-detector"
trigger: /bypass-detector
---

## What this is for

Validation checks like `typeof x === 'string' && x.length < 12` pass when the
attacker sends `{ '': '' }` (NoSQL injection) or `1234 OR 1=1` (SQL injection
via ORM). SAST tools detect type-confusion patterns but not the actual
bypass-availability. This skill traces every validation path from input source
to storage/execution sink, enumerates edge-case input shapes, and the LLM
judges which shapes bypass each validator.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/validation-trace.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- What input shapes pass each validation unexpectedly?

### Step 6

(string that looks like int, object with empty keys, array of primitives,

### Step 7

null, nested object matching schema-but-exploiting-query)

### Step 8

- Which query-construction breaks at the sink?

### Step 9

(MongoDB `where id = ?` with `{ '': '' }` becomes `where id = ''`,

### Step 10

SQL `WHERE id = 1234 OR 1=1` via unsanitized template)

### Step 11

- Multi-language check: is the sink JavaScript/Python/Go/etc and does the

### Step 12

query-builder or ORM offer type-coercion protection?

### Step 13

5. Write `type-confusion-bypass-report.md` to the working directory.

## Usage

```
/bypass-detector                            # interactive
/bypass-detector <dir>                      # scan project
/bypass-detector -help                      # show usage
```

Returns JSON with `findings[]`:
`{file, line, validationType, inputSource, sinkType, sinkFound, validated}`
plus summary counts.
