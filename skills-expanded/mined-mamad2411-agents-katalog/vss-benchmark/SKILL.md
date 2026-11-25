---
name: vss-benchmark
description: Run VSS video summarization performance benchmarks. User specifies VLM + LLM models; skill auto-selects the right pack.
user-invocable: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, Agent
argument-hint: "[vlm] [llm] — e.g., 'gpt-4o gpt-5.2' or omit to be prompted"
---

# VSS Performance Benchmark Skill

Runs video summarization benchmarks against a deployed VSS stack. The user specifies VLM and LLM models; the skill auto-selects the appropriate pack (POC/small/medium) based on each pack's capabilities.

## Step 0: Gather Configuration

Use `AskUserQuestion` to collect:

1. **VLM model** — what vision model to use for captioning (e.g., `gpt-4o`, `cosmos-reason1`, `maverick`)
2. **LLM model** — what language model to use for summarization (e.g., `gpt-5.2`, `llama-3.1-8b`, `maverick`)
3. **Frontend URL** — the deployed VSS frontend
4. **Video source** — local file path, bucket + object key, or existing file ID
5. **Number of runs** (default: 1)
6. **Ground truth CSV** (optional) — for accuracy evaluation

### Auto-Select Pack

Use the model inputs to determine which pack to deploy/use. Match against this capability matrix:

| Pack | VLM Capability | LLM Capability | Audio | CV | LLM Proxy | VLM Mode |
|------|---------------|----------------|-------|-----|-----------|----------|
| **POC** | Any OpenAI-compat model via LlamaStack (gpt-4o, maverick, etc.) | Any OCI GenAI model via LlamaStack (gpt-5.2, maverick, etc.) | Yes (Riva) | Yes | LlamaStack → OCI GenAI | `openai-compat` |
| **Small** | Cosmos Reason 1 only (local NIM, fp8) | Llama 3.1 8B only (local NIM) | No | Yes | NIM (on-prem) | local model |
| **Medium** | Cosmos Reason 1 only (HuggingFace) | Llama 3.1 8B only (local NIM) | Yes (Riva) | Yes | NIM (on-prem) | local model |

**Selection logic:**
1. If VLM is an OCI GenAI / OpenAI-compat model (gpt-4o, maverick, etc.) → **POC** (only pack with LlamaStack proxy)
2. If VLM is cosmos-reason1 AND audio is needed → **Medium** (has Riva)
3. If VLM is cosmos-reason1 AND no audio needed → **Small** (lighter footprint)
4. If the combination doesn't match any pack, **ask the user** which pack to use and explain the constraints

**After selecting the pack**, confirm with user:
> "Based on your models (VLM: X, LLM: Y), I'll use the **Z** pack. This pack supports: [capabilities]. Proceed?"

### Derive parameters from selection:

| Parameter | POC | Small | Medium |
|-----------|-----|-------|--------|
| `model` (request body) | `oci/openai.gpt-4o` | `cosmos-reason1` | `cosmos-reason1` |
| `enable_audio` | `true` | `false` | `true` |
| `enable_cv_metadata` | `true` | `true` | `true` |
| VLM endpoint | LlamaStack `/v1/` | Local NIM | Local NIM |
| LLM endpoint | LlamaStack → OCI GenAI | NIM LLM | NIM LLM |

**Override rules:**
- User can override `enable_audio` and `enable_cv_metadata` regardless of pack
- For POC, if user specifies a non-default VLM (e.g., maverick instead of gpt-4o), the `VIA_VLM_OPENAI_MODEL_DEPLOYMENT_NAME` env var in the blueprint must match — verify this against the running pod's env, or warn the user that a redeployment may be needed
- Temperature is always forced to 0.0 for benchmark reproducibility (override with `--temperature`)

## Step 1: Pre-flight Checks

Verify the stack is healthy:

```bash
# Check frontend is reachable
curl -sk -o /dev/null -w '%{http_code}' "${FRONTEND_URL}/api/vss/config"

# Check backend config to confirm capabilities match selected pack
curl -sk "${FRONTEND_URL}/api/vss/config" | jq .

# Verify pods are Running
kubectl get pods | grep -E "vss|llamastack|nim"

# For POC: verify the registered model matches user's VLM
curl -sk "${FRONTEND_URL}/api/vss/models" 2>/dev/null || \
  kubectl exec <llamastack-pod> -- curl -s http://localhost:8321/v1/models
```

If the registered model doesn't match what the user requested, warn them and ask how to proceed (may need redeployment with different model config).

## Step 2: Upload Video (if needed)

If user provided a local file path or bucket+object (not a file ID):

```bash
curl -sk -X POST -H 'Content-Type: application/json' \
  -d '{"bucketName":"'"${BUCKET}"'","objectName":"'"${OBJECT_KEY}"'"}' \
  -o "${OUTPUT_DIR}/upload.json" -w '%{http_code} %{time_total}' \
  "${FRONTEND_URL}/api/download-and-upload"
```

Save `fileId` and upload time.

## Step 3: Run Summarization Benchmark

For each run (1..N):

### Request body:

```json
{
  "fileId": "<from step 2>",
  "model": "<derived from pack selection>",
  "temperature": 0.0,
  "top_p": 0.0,
  "top_k": 1,
  "max_tokens": 2048,
  "seed": 42,
  "enable_audio": "<derived from pack>",
  "enable_cv_metadata": "<derived from pack>",
  "summarize_temperature": 0.0,
  "summarize_top_p": 0.0,
  "summarize_max_tokens": 2048,
  "chat_temperature": 0.0,
  "chat_top_p": 0.0,
  "chat_max_tokens": 2048,
  "notification_temperature": 0.0,
  "notification_top_p": 0.0,
  "notification_max_tokens": 2048
}
```

**Include the standard CA-RAG prompts** (from the blueprint's `ca_rag_config.yaml`):
- `caption_summarization_prompt` — the warehouse caption→timeline format prompt
- `summary_aggregation_prompt` — the warehouse aggregation/clustering prompt

### Execute:

```bash
START=$(date +%s.%N)
HTTP_CODE=$(curl -sk -X POST -H 'Content-Type: application/json' \
  --max-time 2100 \
  -d '@request.json' \
  -o "${OUTPUT_DIR}/run_${N}.json" \
  -w '%{http_code}' \
  "${FRONTEND_URL}/api/vss/summarize")
END=$(date +%s.%N)
```

### Monitor progress:
While waiting (10-30 min), check logs every 2-3 minutes:

```bash
kubectl logs <vss-engine-pod> --tail=20 | grep -i "chunk\|caption\|summariz"
```

Report milestones: "VLM captioning: 45/87 chunks", "Summarization started", etc.

## Step 4: Collect Results

Save to `${OUTPUT_DIR}/benchmark_results.json`:

```json
{
  "benchmark_id": "<timestamp>",
  "config": {
    "pack": "<auto-selected>",
    "vlm_model": "<user-specified>",
    "llm_model": "<user-specified>",
    "audio_enabled": true,
    "cv_enabled": true,
    "temperature": 0.0,
    "num_runs": 1
  },
  "video": {
    "file_id": "<id>",
    "source": "<path or bucket/key>",
    "upload_time_seconds": 0.0
  },
  "runs": [
    {
      "run_number": 1,
      "status": "success|failure",
      "http_code": 200,
      "total_time_seconds": 0.0,
      "result_length": 0,
      "num_events": 0,
      "error": null
    }
  ],
  "summary": {
    "avg_time_seconds": 0.0,
    "min_time_seconds": 0.0,
    "max_time_seconds": 0.0,
    "success_rate": "1/1"
  }
}
```

Also save raw output: `${OUTPUT_DIR}/run_${N}_output.txt`

## Step 5: Accuracy Evaluation (if ground truth provided)

If the user provided a ground truth CSV:

1. Read CSV (expected columns: `start_time`, `end_time`, `category`, `event_description`)
2. Parse summarization timeline into structured events
3. Compute:
   - **Event detection rate**: % of ground truth events found
   - **False positive rate**: predicted events not in ground truth
   - **Temporal accuracy**: avg time offset (seconds)
   - **Category accuracy**: % correct category labels
4. Save to `${OUTPUT_DIR}/accuracy_results.json`

## Step 6: Report

```
═══════════════════════════════════════════════════════
 VSS BENCHMARK — <timestamp>
═══════════════════════════════════════════════════════
 Pack:     <auto-selected> (auto-selected from models)
 VLM:      <user-specified model>
 LLM:      <user-specified model>
 Audio:    enabled/disabled
 CV:       enabled/disabled
 Video:    <source>
───────────────────────────────────────────────────────
 Run  Status   Time (s)   Events   Result Length
───────────────────────────────────────────────────────
  1   PASS     1234.5     42       8923
───────────────────────────────────────────────────────
 Avg: 1234.5s | Success: 1/1
═══════════════════════════════════════════════════════
```

If accuracy results available, append accuracy table.

Save to `${OUTPUT_DIR}/benchmark_report.txt`.

## Output Directory

`/tmp/vss-benchmark/<vlm>-<llm>-<timestamp>/`

## Notes

- Summarization takes 10-30 minutes per run. Use `--max-time 2100`.
- Temperature 0.0 + seed 42 for reproducibility.
- The `model` request param must match a registered model in the LLM service's `/models` endpoint.
- POC model param: `oci/openai.gpt-4o`. Small/medium: `cosmos-reason1`.
- If the user wants a model combo that no pack supports natively, explain the constraint and suggest the closest option or a custom deployment.
