---
name: data-flow-cartographer
description: "Traces data flow from input sources (API endpoints, events, files) through transformations to sinks (DB, APIs, logs, filesystem). Generates Mermaid flow diagrams per data flow with origin, schema changes, validation gaps, and security relevance. Read-only. Audience: Senior. Trigger: /dataflow"
trigger: /dataflow
---

## What this is for

Every data flow is a trust boundary. Input reaches a handler, is transformed, and ends up in a DB, an API call, a log, or a file. This skill traces each flow from source to sink - capturing intermediate assignments, validation gaps, and PII/payment exposure - then generates Mermaid diagrams for visualization.

**Audience:** Senior
- Security engineers use it to find unvalidated data paths.
- Architects use it to understand coupling between input and storage.
- Anyone debugging "where does this data actually go?"


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` / `-h` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/flow-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each data flow:

### Step 5

- **Data origin:** Identify the input source type and the field names extracted.

### Step 6

- **Schema changes:** What transformations occur between source and sink? (parsing, validation, renaming, aggregation, encryption)

### Step 7

- **Validation gaps:** Does the path contain `if`/`typeof`/`validate`/`zod`/`joi` checks? If not, flag as unvalidated.

### Step 8

- **Security relevance:** Does any field match PII patterns (email, iban, phone, address) or payment (card, cvc, amount, currency)? Mark as sensitive.

### Step 9

- **Mermaid diagram:** For each flow, generate a `flowchart LR` diagram: `Source -->|field names| Transformer -->|field names| Sink`. Include validation checkpoints as diamond nodes.

### Step 10

5. Write `dataflow-report.md` to the working directory with all Mermaid diagrams.

## Usage

```
/dataflow                          # interactive
/dataflow <dir>                    # scan project
/dataflow -help                    # show usage
```

Returns JSON with `flows[]`:
`{inputFile, inputLine, sinkFile, sinkLine, sourceType, sinkType, hops[], hasValidation}` plus summary counts.
