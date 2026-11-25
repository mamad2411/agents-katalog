---
name: jsonl-converter
description: "Use when converting uploaded documents to .jsonl format for AI training, fine-tuning, or data processing pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jsonl, data-conversion, fine-tuning, training-data, preprocessing]
---

# JSONL Converter

## Overview

Convert documents (CSV, JSON, TXT, Parquet, Excel) into JSONL (JSON Lines) format for AI training, fine-tuning datasets, and data processing pipelines. Covers format detection, schema mapping, validation, and output generation meeting the requirements of popular fine-tuning platforms (OpenAI, Together, Anyscale, etc.).

## When to Use

- "Convert this CSV to JSONL for fine-tuning" — training data preparation
- "I need to format my data for OpenAI fine-tuning" — platform-specific formatting
- "Transform this document into JSONL format" — general conversion
- "Validate my JSONL file" — format checking and error detection
- "Merge multiple data sources into one JSONL" — data consolidation

**Don't use for:** converting JSONL back to other formats (one-way conversion focus), streaming real-time data (this is batch-oriented), or non-JSONL output formats.

## How It Works

**Detect Format → Map Schema → Convert → Validate → Output**

## Steps

### 1. Detect Input Format
- Read the first few bytes or the file extension to determine format
- Supported inputs: CSV, TSV, JSON, JSON array, Parquet, Excel (.xlsx), plain text
- Handle encoding detection (UTF-8, UTF-16, Latin-1)

### 2. Understand the Target Schema
- For OpenAI fine-tuning, each line needs a `"messages"` array with `{"role": "...", "content": "..."}` objects
- For general JSONL, each line is a complete, valid JSON object
- Confirm the required fields with the user

### 3. Schema Mapping
Map source columns to the target JSONL schema:

**OpenAI Chat Format:**
```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is AI?"}, {"role": "assistant", "content": "AI stands for Artificial Intelligence..."}]}
```

**General Format:**
```jsonl
{"id": 1, "text": "example content", "label": "positive"}
```

### 4. Conversion Script Template (Python)
```python
import json
import csv

def csv_to_jsonl(input_path, output_path, mapping):
    """Convert CSV to JSONL with flexible schema mapping.
    
    mapping = {
        "user": "input_column_name",
        "assistant": "output_column_name",
        "system": "system_prompt_text"  # optional static value
    }
    """
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        for row in reader:
            messages = []
            if mapping.get("system"):
                messages.append({"role": "system", "content": mapping["system"]})
            if mapping.get("user") and row.get(mapping["user"]):
                messages.append({"role": "user", "content": row[mapping["user"]].strip()})
            if mapping.get("assistant") and row.get(mapping["assistant"]):
                messages.append({"role": "assistant", "content": row[mapping["assistant"]].strip()})
            if messages:
                outfile.write(json.dumps({"messages": messages}, ensure_ascii=False) + '\n')
```

### 5. Validation
- Every line is valid JSON (no trailing commas, no multi-line records)
- No empty lines or whitespace-only lines
- Required fields present in every record
- No duplicate entries (based on content hash or ID)
- File encoding is UTF-8

**Validation script:**
```python
import json

def validate_jsonl(path):
    errors = []
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if "messages" not in obj:
                    errors.append(f"Line {i}: missing 'messages' key")
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: invalid JSON — {e}")
    return errors
```

### 6. Output
- Write to `.jsonl` file with one JSON object per line
- Use `ensure_ascii=False` to preserve Unicode characters
- Verify line count matches input record count (minus skipped rows)
- Offer to split into train/validation sets (typically 80/20 or 90/10)

## Common Pitfalls

1. **Multi-line JSON values.** JSONL requires exactly one JSON object per line. If source data contains newlines in text fields, escape them (`\n`) or strip them.

2. **Missing encoding handling.** Files from Excel or legacy systems may be in non-UTF-8 encodings. Always detect and convert to UTF-8.

3. **Empty or whitespace-only lines.** Some platforms reject files with blank lines. Strip and skip empty lines during conversion and validation.

4. **Truncated content.** OpenAI fine-tuning has token limits per example. Flag or truncate examples exceeding context limits (typically ~4096 tokens for gpt-3.5, ~8192+ for gpt-4).

5. **Trailing comma in JSON.** The most common JSON error. Always validate before delivering the output file.
