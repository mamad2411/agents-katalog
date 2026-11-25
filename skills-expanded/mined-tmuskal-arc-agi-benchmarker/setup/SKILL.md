---
description: Set up the LongMemEval benchmarking environment - guides user through conda env, upstream clone, dataset download, and initializes config
---

# LongMemEval Setup

You are setting up the LongMemEval benchmarking environment. The plugin does NOT clone or install upstream code itself — it gives the user the commands to run and verifies the outcome. Work through the steps below in order. Stop on failure with remediation guidance.

## Step 1: Check Python

```bash
python3 --version 2>/dev/null || python --version 2>/dev/null
```

LongMemEval upstream targets Python 3.9. Any 3.9+ works for this plugin, but 3.9 is recommended. If Python is missing, tell the user to install it (conda recommended: `conda create -n longmemeval python=3.9 -y`).

Record which Python command exists as `PYTHON_CMD`.

## Step 2: Create or Reuse Virtual Environment

```bash
ls -d .longmemeval-venv 2>/dev/null
```

If absent, create it:

```bash
$PYTHON_CMD -m venv .longmemeval-venv
```

Resolve the venv pip/python paths (do NOT source activate scripts):

```bash
if [ -f ".longmemeval-venv/bin/pip" ]; then
  VENV_PIP=".longmemeval-venv/bin/pip"
  VENV_PYTHON=".longmemeval-venv/bin/python"
elif [ -f ".longmemeval-venv/Scripts/pip.exe" ]; then
  VENV_PIP=".longmemeval-venv/Scripts/pip"
  VENV_PYTHON=".longmemeval-venv/Scripts/python"
fi
```

## Step 3: Clone Upstream (guidance only)

Ask the user to clone LongMemEval next to the project if not already present:

```
git clone https://github.com/xiaowu0162/longmemeval.git
```

Verify:

```bash
ls longmemeval/src/evaluation/evaluate_qa.py 2>/dev/null && echo "upstream: OK"
```

If missing, tell the user to run the clone command above and re-run this skill.

## Step 4: Install Dependencies

Install the lite deps plus `anthropic` (the plugin's addition):

```bash
$VENV_PIP install -r longmemeval/requirements-lite.txt
$VENV_PIP install anthropic
```

If `requirements-lite.txt` is missing, install explicitly:

```bash
$VENV_PIP install openai==1.35.1 tqdm==4.66.4 backoff==2.2.1 numpy==1.26.3 nltk==3.9.1 anthropic
```

## Step 5: Download Datasets (guidance)

Tell the user to download one or more dataset variants from HuggingFace (`xiaowu0162/longmemeval-cleaned`) into `longmemeval/data/`:

- `longmemeval_s.json` (default, ~115k tokens / item)
- `longmemeval_m.json` (~500 sessions / item; retrieval required)
- `longmemeval_oracle.json` (evidence-only)

Verify at least one exists:

```bash
ls longmemeval/data/longmemeval_*.json 2>/dev/null
```

## Step 6: API Keys

Check for `ANTHROPIC_API_KEY` (default judge + target) and optionally `OPENAI_API_KEY` (fallback):

```bash
echo "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:+SET}"
echo "OPENAI_API_KEY=${OPENAI_API_KEY:+SET}"
```

If neither is set, tell the user to set `ANTHROPIC_API_KEY` before running the benchmark.

## Step 7: Initialize Configuration

Create `.longmemeval-benchmarks/config.json` if missing:

```bash
mkdir -p .longmemeval-benchmarks
$VENV_PYTHON -c "
import json, os
from datetime import datetime, timezone
from pathlib import Path

p = Path('.longmemeval-benchmarks/config.json')
if p.exists():
    cfg = json.loads(p.read_text())
    cfg['updated_at'] = datetime.now(timezone.utc).isoformat()
else:
    cfg = {
        'version': '1.0.0',
        'longmemeval_root': 'longmemeval',
        'datasetVariant': 'longmemeval_s',
        'datasetPath': 'longmemeval/data/longmemeval_s.json',
        'runs_dir': '.longmemeval-benchmarks/runs',
        'maxEvals': 500,
        'seed': 0,
        'targetProvider': 'anthropic',
        'targetModel': 'claude-opus-4-6',
        'judgeProvider': 'anthropic',
        'judgeModel': 'claude-opus-4-6',
        'harness': 'claude-code',
        'harness_config': {'model': 'claude-opus-4-6', 'plugins': [], 'skills': [], 'mcp_servers': []},
        'cross_harness': {'result_schema_version': '1.0.0', 'supported_harnesses': ['codex', 'gemini', 'opencode']},
        'created_at': datetime.now(timezone.utc).isoformat(),
        'updated_at': datetime.now(timezone.utc).isoformat(),
    }
p.write_text(json.dumps(cfg, indent=2))
print('config:', p)
"
```

## Step 8: Detect Harness Configuration

Populate `harness_config` (model, plugins, skills, mcp_servers) best-effort from environment variables and `~/.claude/settings.json`. Mirror the logic from `arc-agi-benchmarker/skills/setup/SKILL.md` Step 7.

## Step 9: Print Summary

```
============================================
  LongMemEval Benchmarker - Setup Summary
============================================
  Python:          {version}
  Virtual Env:     .longmemeval-venv
  Upstream:        longmemeval/  [OK / MISSING]
  Dataset(s):      {list}
  ANTHROPIC_API_KEY: {SET / MISSING}
  OPENAI_API_KEY:    {SET / MISSING}
  Config:          .longmemeval-benchmarks/config.json
  Status:          READY / NOT READY ({reason})
============================================
```

READY requires: venv present, upstream clone present, at least one dataset file present, at least one API key set, config written.

## Idempotency

Safe to re-run. Venv reused, config timestamps updated, no runs touched.
