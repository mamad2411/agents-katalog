---
name: verify-llm-vendors
description: Run the Verify LLM Vendors benchmark using the PyPI-installed `agent-vendor-verifier` CLI; before each test run validate that config.yaml is complete, ask the user for any missing required config values, then read config and confirm with the user the list of models, vendors and baseline from config plus test-file-path, config-file-path, vendor-concurrency, request-concurrency, retries, timeout; before running, check whether `agent-vendor-verifier` is installed and install it from PyPI if missing; when the user asks to add or update a benchmark test plan, ask for model name, model id, vendor, api key, provider if needed, and write the entry into config.yaml; generate or edit config.yaml; check whether runs succeeded via summary.json; aggregate or report run data and final results. Use when the user wants to run the tool-call validation benchmark, add or update test plans, create or change benchmark config, inspect benchmark outcomes, verify success from summary files, or get a consolidated view of metrics (success rate, F1, schema accuracy, latency, throughput).
---

# Verify LLM Vendors Skill

Run the `verify-llm-vendors` benchmark, generate `config.yaml` when needed, validate that `config.yaml` is complete before each run by asking the user only for missing required values, verify run success from `*_summary.json` files, and summarize run data and final results.

## When to use

- User asks to run the benchmark, start a benchmark, or run verify-llm-vendors — **before running**, validate that the intended `config.yaml` is complete; if anything required is missing, ask the user only for the missing information, update the config, then confirm test-file-path, config-file-path, vendor-concurrency, request-concurrency, retries, timeout.
- User asks in natural language to add a new test model, add a vendor, create a benchmark plan, or update benchmark config; ask for model name, model id, vendor(s), API key(s), and provider for OpenRouter when needed, then update the skill’s config.yaml.
- User wants to create or update benchmark config (config.yaml); you must be able to generate it and, when necessary, ask for api_key, models to run, and vendors to run.
- User wants to check if a benchmark run succeeded or inspect summary.json outcomes.
- User wants a summary or report of benchmark results (by model/vendor), success status, and metrics.

---

## Add Or Update A Test Plan

When the user asks in natural language to add a test model, add a vendor, or update benchmark config for `verify-llm-vendors`:

1. **Ask the user** for:
   - Model name to add (or which existing model to add a vendor to).
   - Model ID to send to the vendor API.
   - Vendor(s) to add (e.g. `openrouter`, `vertex`, `bedrock`, `packyapi`, `foxcode`, `yunwu`).
   - API key(s) for each new vendor.
   - For OpenRouter: provider (e.g. `anthropic`, `google-ai-studio`, `openai`).
   - Endpoint URL only if they use a custom one; otherwise use default (e.g. `https://429.icu/v1`).
   - Whether the new vendor should become the baseline for that model.
2. **Read** the existing `config.yaml` in this skill directory if it exists.
3. **Confirm** with the user the exact values that will be written.
4. **Edit** the `config.yaml` in this skill directory directly:
   - If the model does not exist, create a new top-level model block.
   - If the model exists, add or update the vendor entry under `vendors`.
   - For `name: openrouter`, include `provider`.
   - Keep `url`, `validator: openai`, and `model_id` explicitly set on every vendor entry.
5. **Read back** the updated config and confirm what was added. Ensure exactly one vendor per model has `is_baseline: true`.

---

## 1. Generate config.yaml

You must be able to **autonomously write or edit directly** a valid `config.yaml` for the benchmark. Save the generated file in the **same directory as this skill**.

### When to generate

- User asks to “set up config”, “add a model/vendor”, or “run benchmark” but no suitable config exists in the skill dir.
- User specifies new models or vendors; update or create the skill’s `config.yaml` accordingly.

### What to ask the user (when information is missing)

Ask only what is needed. Typical questions:

- **API keys:** For each vendor (and for OpenRouter, per provider if needed), ask: “Please provide the API key for [vendor/provider].” Do not invent or reuse keys from examples.
- **Models to run:** “Which model(s) should we run?” (e.g. `claude-sonnet-4-5`, `gemini-2.5-flash`). Use the exact model names the user or the API expects.
- **Vendors to run:** “Which vendor(s) should we use for each model?” (e.g. `openrouter`, `vertex`, `bedrock`, `packyapi`, `foxcode`, `yunwu`). For OpenRouter, also ask or infer **provider** (e.g. `anthropic`, `google-ai-studio`, `openai`).
- **Endpoint URL:** If the user has a custom endpoint, ask for the base URL; otherwise you may use a default (e.g. `https://429.icu/v1`) if the project does.

### Config structure and schema

- Top-level keys = **model names**. Under each model: `vendors` = list of vendor entries.
- Each vendor: `name`, `model_id`, `api_key`, `url`, `validator: openai`, `is_baseline` (exactly one `true` per model).
- For `name: openrouter` only: add `provider` (e.g. `anthropic`, `google-ai-studio`).

Full field list and examples: see **`references/config_schema.md`** in this skill. Read it when generating or editing config so the YAML is valid.

### Output location

- **Always write the generated or updated config to:**  
  `config.yaml` in the same directory as `SKILL.md`.
- This is the default config location for the skill, but the user may explicitly specify a different `--config-file-path`.

---

## 2. Validate config before running

**Before every test run:** you **must** validate the intended config file before you confirm run parameters or execute the benchmark.

### Completeness checks

Read the intended `config.yaml` and verify:

- The file exists and is valid YAML.
- There is at least one top-level model entry.
- Each model has a non-empty `vendors` list.
- Each vendor entry includes `name`, `model_id`, `api_key`, `url`, `validator`, and `is_baseline`.
- If `name: openrouter`, the vendor entry also includes `provider`.
- Each model has **exactly one** vendor with `is_baseline: true`.

### If config is incomplete

- Do **not** run the benchmark yet.
- Ask the user only for the missing values.
- Update the config in the skill directory with those values.
- Read the config again and confirm it is now complete before moving on.

Typical follow-up questions for missing values:

- “Please provide the API key for `[vendor/provider]`.”
- “Which vendor should be the baseline for `[model]`?”
- “Please provide the `model_id` for `[model]` on `[vendor]`.”
- “Please provide the endpoint URL for `[vendor]`.” If they do not have a custom one, use the project default when appropriate.
- “Please provide the OpenRouter provider for `[model]`.”

---

## 3. Run benchmark (command)

**Before every test run:** you **must** confirm with the user the following.

1. **From the config file** (the intended `--config-file-path`): after validating completeness, **read** that YAML and list for the user:
   - Each **model** that will be tested
   - Under each model, each **vendor** (for OpenRouter, include provider, e.g. `openrouter (provider: minimax)`)
   - Which vendor is **baseline** per model (`is_baseline: true`)

2. **Run parameters** — present and confirm:
   - **Installation status** — before running, check whether `agent-vendor-verifier` is already installed; if not, install it from PyPI
   - **`--test-file-path`** — path to the JSONL test set
   - **`--config-file-path`** — path to the YAML config
   - **`--vendor-concurrency`** — max concurrent vendor requests
   - **`--request-concurrency`** — max concurrent requests per vendor
   - **`retries`** — retries per request
   - **`timeout`** — request timeout in seconds

Only after the user confirms (or provides different values) should you check installation and run the benchmark.

---

Before invoking the benchmark, the agent must verify that `agent-vendor-verifier` is installed in the active `python3` environment. Use this check:

```bash
python3 -m pip show agent-vendor-verifier >/dev/null 2>&1 || python3 -m pip install agent-vendor-verifier
```

Do not rely on a local source checkout of `agent_vendor_verifier/` or require a project root path for normal benchmark runs.

To start the benchmark in the background (no proxy, log to file), run the installed CLI:

```bash
nohup env -u all_proxy -u http_proxy -u https_proxy agent-vendor-verifier \
  --test-file-path tool-call/samples_filtered_tiny.jsonl \
  --config-file-path skills/verify-llm-vendors/config.yaml \
  --vendor-concurrency 1 \
  --request-concurrency 2 \
  --retries 2 \
  --timeout 60 \
  > benchmark.log 2>&1 &
```

Optional arguments:
`--test-file-path`, `--config-file-path`, `--vendor-concurrency`, `--request-concurrency`, `--retries`, `--timeout`, `--temperature`, `--max-tokens`.

Example with custom concurrency and log file:

```bash
nohup env -u all_proxy -u http_proxy -u https_proxy agent-vendor-verifier \
  --test-file-path tool-call/samples_filtered_tiny.jsonl \
  --config-file-path skills/verify-llm-vendors/config.yaml \
  --vendor-concurrency 1 \
  --request-concurrency 4 \
  --retries 2 \
  --timeout 60 \
  > my.log 2>&1 &
```

**Parameters:**

| Parameter | Meaning | Example |
|-----------|--------|--------|
| `--test-file-path` | JSONL test set path | `tool-call/samples_filtered_tiny.jsonl` |
| `--config-file-path` | YAML config (models, vendors, API keys) | Skill-generated `config.yaml` in the same directory as `SKILL.md`, or another user-specified path |
| `--vendor-concurrency` | Max concurrent vendor requests | `1` |
| `--request-concurrency` | Max concurrent requests per vendor | `2` |
| `--retries` | Retries per request | `2` |
| `--timeout` | Request timeout (seconds) | `60` |

Redirect and `nohup` are used so the run continues after the shell closes; logs go to `benchmark.log`.

After starting, note the process ID or use `jobs` / `tail -f benchmark.log` to monitor.

---

## 4. Check if a run succeeded (summary.json)

Benchmark writes one summary per (model, vendor) under `data/`:

- **OpenRouter:** `data/{model}_{vendor}_{provider}_summary.json`
- **Other vendors:** `data/{model}_{vendor}_summary.json`

**Success criteria for a single summary:**

- File exists and is valid JSON.
- `success_count` is not 0 (i.e. at least one request succeeded).

Use the bundled script to check all summaries and report status:

```bash
python3 skills/verify-llm-vendors/scripts/check_and_summarize.py --data-dir data
```

Or implement the same logic: list `data/*_summary.json`, parse each, and report per-file success/failure and key fields (`success_count`, `failure_count`, `schema_validation_error_count`, `schema_accuracy`).

---

## 5. Summarize run data and final results

After runs complete:

1. **Collect summaries**  
   All `*_summary.json` under `data/` (and any vendor-specific subdirs like `*_summary/*.json` if present).

2. **Per summary report**  
   For each file, report at least:
   - Identifier (e.g. `model` + vendor/provider from filename).
   - **Success:** whether the test run succeeded, using the summary result (`success_count` ≠ 0).

3. **Aggregated view**  
   - By model: list vendors and their success status together with the metric values from `rank/*.json`.
   - Present the aggregated results as a **Markdown table** whenever you summarize results for the user.
   - The table should include `Model`, `Vendor`, `TestSuccess`, plus the metric columns loaded from the files in `rank/` such as `f1_score`, `irf_score`, `success_rate`, `schema_accuracy`, `avg_tokens`, `avg_ttft_ms`, `avg_throughput`, and `irf_score_global` when present.
   - Do **not** keep the old summary-detail columns like `Success`, `Failure`, `SchemaErr`, `SchemaAcc`, `AvgTokens`, `AvgTTFT(ms)`, `Throughput`, `F1` unless they are being sourced from `rank/`.

Use the same script for a consistent report:

```bash
python3 skills/verify-llm-vendors/scripts/check_and_summarize.py --data-dir data
```

Output: a Markdown table (e.g. model × vendor) that merges `rank/` metrics with `TestSuccess`, followed by a brief overall pass/fail summary.

---

## 6. End-to-end workflow

1. **Config:** If no config exists or the user wants to change it, generate or edit the `config.yaml` in this skill directory; ask the user for api_key, models to run, and vendors (and provider for OpenRouter) as needed.
2. **Validate config completeness:** Before starting the test plan, read the intended config and verify all required fields are present. If any required value is missing, ask the user only for those missing values, update the config, and re-validate it. Do not proceed until the config is complete.
3. **Confirm run parameters:** After the config is complete, **read the config** at the intended config path and **confirm with the user**: (a) list from config the **models**, **vendors** per model, and **baseline** per model; (b) then confirm `--test-file-path`, `--config-file-path`, `--vendor-concurrency`, `--request-concurrency`, `retries`, `timeout`. Proceed only after user confirmation (or their chosen values).
4. **Check installation:** Before executing the benchmark, run `python3 -m pip show agent-vendor-verifier >/dev/null 2>&1 || python3 -m pip install agent-vendor-verifier` so the CLI is available from the active environment.
5. **Start:** Run the installed `agent-vendor-verifier` command with the confirmed parameters; optionally `tail -f benchmark.log` until completion.
6. **Check:** Run `check_and_summarize.py` on `data/` to verify which runs succeeded.
7. **Report:** Use the script output (and optionally `benchmark.log`) to summarize run data and final results for the user. The final user-facing summary should include a concise conclusion plus a Markdown table that combines `rank/` metrics with `TestSuccess`.

If the user only wants to “check” or “summarize” without starting a new run, use steps 6 and 7 only.
