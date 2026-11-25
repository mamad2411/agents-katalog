---
name: query
description: "Ask natural language questions about your data and get answers with evidence"
argument-hint: "[dataset-name] [your question]"
risk: "safe"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: claude-sonnet-4-6
context: fork
agent: general-purpose
---

# 10x Analyst — Data Query

Ask any question about your data in plain English and get a precise answer backed by numbers.

## Overview

Loads data from `input/<dataset>/`, interprets your question, writes and executes the exact pandas query needed, and returns the answer with supporting evidence. No dashboard, no report — just the answer.

## When to Use

- User asks a specific question about data: "What are our top 5 products?", "What's the average order value?", "Which customers churned?"
- User wants a quick answer without the full analysis pipeline
- User wants to explore data interactively with follow-up questions

## Path Resolution

Parse `$ARGUMENTS`:
- First word: dataset name → reads from `input/<dataset-name>/`
- Remaining text: the user's question

## Instructions

1. Parse `$ARGUMENTS`:
   - First word = dataset name (e.g., `shopify-data`)
   - Everything after = the question
   - Input path: `input/<dataset>/`
2. Find and load all data files at `input/<dataset>/`
3. Clean column names: `df.columns = df.columns.str.strip().str.lower().str.replace(r'[^a-z0-9]+', '_', regex=True).str.strip('_')`
4. If multiple files, join on common keys (columns ending in `_id` or named `id`)
5. Read the user's question and determine what pandas operations are needed
6. Write and execute a Python script that:
   - Loads the data from `input/<dataset>/`
   - Runs the query (groupby, filter, aggregate, sort, etc.)
   - Prints the result as a formatted table or value
7. Present the answer in this format:

```
## Answer

{Direct answer to the question with specific numbers}

### Supporting Data

{Table or list with the evidence}

### How This Was Computed

{1-2 sentences explaining the pandas operations used}

### Follow-Up Questions You Might Ask
- {Suggested question 1}
- {Suggested question 2}
```

## Examples

```bash
# Specific metric
/10x-analyst:query shopify-data "What is the average order value?"

# Top-N question
/10x-analyst:query shopify-data "What are the top 10 products by revenue?"

# Segment question
/10x-analyst:query shopify-data "Which customer segment has the highest lifetime value?"

# Trend question
/10x-analyst:query shopify-data "Is revenue growing or declining month over month?"
```

## Limitations

- One question at a time — for multi-question analysis use `:analyze`
- Cannot query external APIs or databases — file-based data only
- Complex multi-step questions may need to be broken down

---
*Developed by [10x.in](https://10x.in) | 10x-Analyst v1.0.0*
