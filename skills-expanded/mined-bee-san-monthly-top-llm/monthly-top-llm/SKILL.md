---
name: monthly-top-llm
description: Use when maintaining one local download of the best whichllm-recommended model for the current machine, changing files only after a successful replacement download.
version: 1.0.0
author: Autumn (Bee) Skerritt and Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [whichllm, huggingface, llm, cron]
    related_skills: []
---

# Monthly Top LLM

## Overview

Use `update_top_llm.py` to refresh `whichllm` recommendations, resolve a runnable model or GGUF, download it through Hugging Face, and keep a small state file. Unchanged runs stay silent.

## When to Use

- A workstation should keep one current best-fit local model.
- A monthly job should update models without accumulating old downloads.
- Selection needs configurable context, quantisation, speed, task, or RAM constraints.

Do not run without checking disk capacity. Model downloads can be many gigabytes.

## Run

```bash
python3 update_top_llm.py
```

If dependencies are missing, the helper re-executes through `uv` with `whichllm` and `huggingface_hub`.

## Safety Contract

1. Rank against current detected hardware unless explicitly overridden.
2. Download the new recommendation before changing state.
3. Atomically replace the state JSON.
4. Remove the old model directory only after a successful new download.
5. Print nothing when the recorded recommendation and local file are unchanged.
6. Never store downloaded models inside a Hermes configuration directory.

## Useful Overrides

- `WHICHLLM_CONTEXT_LENGTH`
- `WHICHLLM_QUANT`
- `WHICHLLM_CPU_ONLY`
- `WHICHLLM_TOP_N`
- `WHICHLLM_TASK_PROFILE`
- `WHICHLLM_MIN_SPEED_TOK_PER_SEC`
- `WHICHLLM_MIN_PARAMS_B`
- `WHICHLLM_TOP_LLM_DIR`
- `WHICHLLM_TOP_LLM_STATE`
- `HF_TOKEN`

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile update_top_llm.py
```

- [ ] State identifies the selected repository and file.
- [ ] The selected file exists under the configured model directory.
- [ ] An unchanged second run produces no stdout.
- [ ] Tests do not contact Hugging Face or download models.
