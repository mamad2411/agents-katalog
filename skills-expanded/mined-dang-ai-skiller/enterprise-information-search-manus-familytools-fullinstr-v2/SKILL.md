---
name: enterprise-information-search-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for enterprise-information-search using latest full-instruction v2 family injection.
allowed-tools:
  - aggregate_records
  - data_catalog
  - fuzzy_search_records
  - json_record_query
  - list_dir
  - read_file
  - read_table
  - run_python
  - search_text
  - write_file
  - write_json
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Enterprise Information Search

## When to use this skill
Use this skill for `enterprise-information-search` tasks in SkillLearnBench. It helps inventory enterprise data, identify requested organizations, join metadata with source records, and write an evidence-backed result file.

## Visible input and artifact inventory
- **Inputs**: Data directory at `/root/DATA` (JSON metadata/products) and question file at `/root/question.txt`.
- **Output**: Answer file at `/root/answer.json` formatted as a dictionary.

## Execution procedure for the current task
1. **Inventory**: Read instructions and inventory files in `/root/DATA`.
2. **Extract**: Get output paths, schemas, and constraints from visible files.
3. **Process**: Use allowed tools to read questions and data. Join metadata with records.
4. **Format**: Create the artifact with deterministic transformations. Ensure `answer` is a list (even for single items) and `tokens` is a positive number.
5. **Check**: Run sanity checks using visible files. Repair mismatches.
6. **Finalize**: Submit only when the artifact exists and matches the instruction shape.

## Family tool routing and useful placeholder snippets
- `list_dir`: Explore `/root/DATA`.
- `read_file`: Read `/root/question.txt`.
- `json_record_query` / `read_table`: Query JSON data.
- `fuzzy_search_records` / `search_text`: Find specific info.
- `aggregate_records`: Combine data sources.
- `write_json`: Write to `/root/answer.json`.
- `run_python`: Complex data manipulation.

## Validation checks before final submission
- Output exists at `/root/answer.json`.
- Output is a valid JSON dictionary.
- Every question key is present.
- Each value is a dict with `answer` (list) and `tokens` (number).

## Common failure modes and repair actions
- **Missing File**: Verify path in `write_json`.
- **Bad Format**: Ensure output is a dict and answers are lists.
- **Missing Questions**: Iterate over all input questions.
- **Bad Token Type**: Cast `tokens` to int/float.

## Finalizer capsule
To restore the minimum required artifact shape near max-step:
```python
import json
def finalize(qs, ans, toks, path):
    res = {q: {"answer": ans.get(q, []), "tokens": toks.get(q, 0)} for q in qs}
    with open(path, 'w') as f: json.dump(res, f)
```
