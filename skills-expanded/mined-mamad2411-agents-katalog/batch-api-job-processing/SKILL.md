---
name: batch-api-job-processing
description: "Organize asynchronous evaluation, audit, or dataset workloads for a provider's batch API when immediate responses are unnecessary."
category: efficiency
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["batch-api", "async-processing", "cost-reduction", "rate-limits", "openai-batch", "anthropic-batches"]
tools: ["claude", "cursor", "gemini", "codex", "lmstudio"]
---

# Asynchronous Batch API Processing (The 50% Cost Discount Protocol)

## Overview
When engineering teams run non-real-time agentic workloads (*e.g., overnight test suite generation, security audits across 2,000 files, or bulk customer feedback classification*), executing sequential synchronous HTTP requests (`/v1/chat/completions` or `/v1/messages`) is financially wasteful and prone to **HTTP 429 Rate Limit Errors**.

Leading AI providers (OpenAI, Anthropic) offer **Asynchronous Batch APIs** that process requests within a 24-hour SLA at an **automatic 50% flat discount** on all input and output tokens, while providing dedicated, massive rate limit pools.

The **Asynchronous Batch Processing Protocol** automates the packaging, dispatch, and ingestion of bulk LLM tasks.

---

## Synchronous Sequential Loop vs. Asynchronous Batch Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Workload Routing Comparison                 │
│                                                             │
│  Synchronous HTTP Loop (1,000 Items):                       │
│  • 1,000 individual REST calls                              │
│  • Hits TPM/RPM rate limits $\rightarrow$ HTTP 429 retries  │
│  • Standard Pricing: $100.00                                │
│  • Requires dedicated worker process to remain alive        │
│                                                             │
│  Asynchronous Batch API Pipeline (1,000 Items):             │
│  1. Pack 1,000 requests into a single `requests.jsonl` file │
│  2. Dispatch via Batch API (OpenAI / Anthropic)             │
│  3. Automatic 50% Flat Discount: $50.00                     │
│  4. Dedicated batch compute pool (Zero 429 rate limits)     │
│  5. Retrieve completed `results.jsonl` via webhook or cron  │
└─────────────────────────────────────────────────────────────┘
```

---

## Production Python Batch Dispatch Pipeline

### 1. OpenAI Batch API Client Implementation

```python
import json
import time
from pathlib import Path
from openai import OpenAI

client = OpenAI()

def create_batch_job(items: list, system_prompt: str, output_jsonl: Path) -> str:
    """Packages prompts into JSONL and dispatches an OpenAI Batch Job."""
    with output_jsonl.open("w", encoding="utf-8") as f:
        for idx, item in enumerate(items):
            task = {
                "custom_id": f"task-{idx}-{item['id']}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": item["content"]}
                    ],
                    "temperature": 0.0
                }
            }
            f.write(json.dumps(task) + "\n")

    # 1. Upload the batch file
    batch_file = client.files.create(
        file=output_jsonl.open("rb"),
        purpose="batch"
    )

    # 2. Create the batch job
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    print(f"Batch Job Dispatched: {batch_job.id} (Status: {batch_job.status})")
    return batch_job.id

def download_batch_results(batch_id: str, results_path: Path) -> None:
    """Polls batch status and downloads completed output file."""
    while True:
        job = client.batches.retrieve(batch_id)
        print(f"Current Status: {job.status} (Completed: {job.request_counts.completed}/{job.request_counts.total})")
        
        if job.status == "completed":
            content = client.files.content(job.output_file_id).text
            results_path.write_text(content, encoding="utf-8")
            print(f"Results saved to {results_path}")
            break
        elif job.status in ["failed", "expired", "cancelled"]:
            raise RuntimeError(f"Batch Job Failed with status: {job.status}")
            
        time.sleep(30)
```

---

## When to Use Synchronous vs. Batch APIs

| Workload Type | Optimal Route | Why |
| :--- | :--- | :--- |
| **Interactive User Chat / CLI Prompting** | Synchronous Streaming | User is actively waiting for response. |
| **Nightly Security Code Scan (2,000 files)** | **Asynchronous Batch API** | 50% discount; results needed by morning. |
| **Offline Test Case Generation** | **Asynchronous Batch API** | Bypasses standard TPM quotas. |
| **Model Evaluation / Benchmark Scoring** | **Asynchronous Batch API** | Eliminates 429 throttling on large test datasets. |

---

## Real-World Cost Analysis

### Scenario: Auditing 5,000 Code Files for Security Flaws

- **Workload**: 5,000 files $\times$ 2,000 tokens input + 500 tokens output = **12.5 Million Tokens**.
- **Model**: Claude 3.5 Sonnet / GPT-4o.
- **Synchronous Execution**: ~$43.75 + Risk of 429 throttling during business hours.
- **Asynchronous Batch API**: **$21.87 (50% Instant Savings)** + Guaranteed zero rate-limiting.

---

## Agent Operational Directive
> **MANDATORY**: Any autonomous background task, benchmark evaluation, or bulk file transformation spanning $> 50$ items that does not require an immediate interactive user response MUST be packaged as an Asynchronous Batch Job.
