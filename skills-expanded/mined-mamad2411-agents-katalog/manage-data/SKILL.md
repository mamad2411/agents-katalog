---
name: manage-data
description: Create, load, push, version, and manage benchmark datasets with the ZeroEval Python SDK or git. Use when adding data to a benchmark, creating a dataset from code or CSV, pushing data to the backend, managing subsets, pulling existing benchmarks, converting data to Parquet, or setting up a git-based data workflow. Triggers on "add data", "create dataset", "push dataset", "upload data", "manage benchmark data", "dataset versioning", "subsets", "pull dataset", "parquet", "multimodal dataset".
---

# Manage Data

Guide users through the full dataset lifecycle: create, modify, push, pull, version, and organize benchmark data.

## When To Use

- Creating a new benchmark dataset from Python dicts, CSV, or existing data.
- Pushing data to the ZeroEval backend.
- Pulling an existing benchmark dataset for evaluation.
- Working with dataset versions and subsets.
- Setting up git-based data management for a benchmark.
- Adding multimodal data (images, audio, video) to datasets.
- Converting CSV/JSONL to Parquet for git workflows.

## Execution Sequence

Follow these steps in order. Load reference files only when the current step requires detailed API usage.

### Step 1: Install and Initialize

Check if the SDK is installed. If not, install it:

```bash
pip install zeroeval
```

Verify the CLI is available:

```bash
zeroeval --help
```

Set the API key (if not already configured):

```bash
export ZEROEVAL_API_KEY="sk_ze_..."
# or use the interactive setup:
zeroeval setup
```

Initialize in code:

```python
import zeroeval as ze

ze.init()  # reads ZEROEVAL_API_KEY from env
```

Full setup guide: https://docs.llm-stats.com/python-sdk/installation

### Step 2: Determine the Data Workflow

Ask the user which scenario fits:

- **Pull an existing benchmark** — data already exists on LLM Stats. Go to Step 3a.
- **Create from Python** — data lives in code as dicts or a CSV file. Go to Step 3b.
- **Git-based workflow** — user wants to clone, add Parquet files, and push via git. Go to Step 3c.

### Step 3a: Pull an Existing Dataset

```python
dataset = ze.Dataset.pull("benchmark-name")

# Pin to a specific version
dataset = ze.Dataset.pull("benchmark-name", version_number=3)

# Pull a specific subset
dataset = ze.Dataset.pull("benchmark-name", subset="hard")
```

Rows are `DotDict` objects — access fields with dot notation (`row.question`) or dict syntax (`row["question"]`).

```python
for row in dataset:
    print(row.question, row.answer)

# Slice
subset = dataset[0:10]
print(dataset.columns)
```

Full reference: https://docs.llm-stats.com/python-sdk/datasets/loading

### Step 3b: Create from Python

```python
# From a list of dicts
dataset = ze.Dataset("my-benchmark", data=[
    {"row_id": "q1", "question": "What is 2+2?", "answer": "4"},
    {"row_id": "q2", "question": "Capital of France?", "answer": "Paris"},
], description="Math and geography questions")

# From a CSV file
dataset = ze.Dataset("/path/to/questions.csv")
```

Include a stable `row_id` column — it makes resume, comparison, and version diffing reliable.

Modify data before pushing:

```python
dataset.add_rows([{"row_id": "q3", "question": "...", "answer": "..."}])
dataset.update_row(0, {"row_id": "q1", "question": "Updated?", "answer": "Yes"})
dataset.delete_row(2)
```

Push to the backend:

```python
dataset.push()
print(dataset.version_number)  # auto-incremented
```

For multimodal data, read `references/dataset-lifecycle.md` for `add_image()`, `add_audio()`, `add_video()`, and `add_media_url()` usage.

Full reference: https://docs.llm-stats.com/python-sdk/datasets/creating

### Step 3c: Git-Based Workflow

This is the recommended approach for production benchmarks. Read `references/git-workflow.md` for the complete guide.

Quick summary:

```bash
git clone https://<user>:<api-key>@git.llm-stats.com/<org>/<slug>.git
cd <slug>

# Add Parquet files (each file = one subset)
mkdir -p data
cp questions.parquet data/default.parquet

git add . && git commit -m "Add benchmark data" && git push
```

Full reference: https://docs.llm-stats.com/python-sdk/datasets/uploading-data

### Step 4: Work with Versions and Subsets

Every `push()` or `git push` creates a new version automatically.

```python
# Pull a pinned version
v2 = ze.Dataset.pull("my-benchmark", version_number=2)

# Pull a specific subset
hard = ze.Dataset.pull("my-benchmark", subset="hard")
```

Default subset resolution order:
1. Benchmark's configured default
2. File named `default.parquet`
3. Single subset (if only one exists)
4. First alphabetically

Full reference: https://docs.llm-stats.com/python-sdk/datasets/versioning-and-subsets

### Step 5: Verify with the CLI

Use the CLI to inspect datasets without writing scripts:

```bash
# List your datasets
zeroeval datasets list

# Inspect a specific dataset
zeroeval datasets get my-benchmark

# Check versions
zeroeval datasets versions my-benchmark

# Preview rows
zeroeval datasets rows my-benchmark --subset default --limit 5

# JSON output for scripting
zeroeval --output json datasets get my-benchmark
```

Full CLI reference: https://docs.llm-stats.com/python-sdk/cli/using-the-cli

### Step 6: Validate

- [ ] `zeroeval datasets list` shows the dataset
- [ ] `zeroeval datasets rows <name>` returns expected data
- [ ] Rows have stable `row_id` or `id` column
- [ ] Version number incremented after push (`zeroeval datasets versions <name>`)
- [ ] Subsets are correctly detected (for git workflows)

## Key Principles

- **Git for production, SDK for prototyping.** Git handles large files, versioning, scorer scripts, and README alongside data. SDK is faster for small programmatic datasets.
- **Always include `row_id`.** Stable row identity enables resume, comparison, and version diffing.
- **Parquet only for subsets.** Only `.parquet` files in `data/` are auto-detected as subsets. CSV and JSONL are stored but not indexed.
- **Version everything.** Each push creates a new version. Pin versions in eval scripts for reproducibility.
- **Start small, scale up.** Test with a few rows before pushing large datasets, especially with multimodal assets.
