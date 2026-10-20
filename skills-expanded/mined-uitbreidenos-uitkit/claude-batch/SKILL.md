---
name: "claude-batch"
description: "Run large-scale batch processing with Claude API for bulk text analysis, classification, and generation"
---

# Claude Batch

## When to activate
Processing large volumes of prompts (10 or more), non-time-sensitive workloads, or when the user wants to reduce API costs for bulk operations like document processing, evaluations, or dataset annotation.

## When NOT to use
- Real-time or latency-sensitive applications — batch processing takes up to 24 hours
- Workflows where each result must feed the next request — use synchronous streaming instead
- Fewer than 10 requests — synchronous API overhead is negligible at that scale

## Instructions

### Batch API Overview
- Submit up to 10,000 requests per batch
- 50% cost discount vs synchronous Messages API
- Processing completes within 24 hours (usually much faster for small batches)
- Results delivered as a JSONL stream when processing completes
- Failed individual requests do not fail the batch

### Request Format
Each item in the batch has:
- `custom_id`: your identifier — used to match results back to inputs
- `params`: standard Messages API parameters (model, max_tokens, messages, system, tools, etc.)

```python
import anthropic

client = anthropic.Anthropic()

requests = [
    {
        "custom_id": f"doc-{i}",
        "params": {
            "model": "claude-opus-4-5",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": f"Summarize this document: {doc}"}
            ],
        },
    }
    for i, doc in enumerate(documents)
]
```

### Submitting a Batch
```python
batch = client.messages.batches.create(requests=requests)
print(batch.id)           # msgbatch_...
print(batch.processing_status)  # "in_progress"
```

### Polling for Completion
```python
import time

def wait_for_batch(batch_id: str) -> anthropic.MessageBatch:
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            return batch
        print(f"Status: {batch.processing_status} — waiting 30s")
        time.sleep(30)

batch = wait_for_batch(batch.id)
print(f"Request counts: {batch.request_counts}")
# RequestCounts(canceled=0, errored=1, expired=0, processing=0, succeeded=199)
```

### Retrieving Results
```python
# Results stream as JSONL — iterate without loading all into memory
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        message = result.result.message
        print(f"{result.custom_id}: {message.content[0].text[:100]}")
    elif result.result.type == "errored":
        error = result.result.error
        print(f"{result.custom_id}: ERROR {error.type} — {error.message}")
    elif result.result.type == "expired":
        print(f"{result.custom_id}: EXPIRED — resubmit")
```

### Result Types
| Type | Meaning | Action |
|---|---|---|
| `succeeded` | Normal completion | Use `result.message` |
| `errored` | API-level error (invalid params, content policy) | Log and skip or retry |
| `expired` | 24-hour window elapsed before processing | Resubmit the request |

### Canceling a Batch
```python
client.messages.batches.cancel(batch.id)
# Already-completed requests are not rolled back — partial results may exist
```

### Rate Limits
- 10,000 requests per batch
- 100 concurrent batches (in-progress at once)
- Batch rate limits are separate from synchronous API rate limits — submitting batches does not count against your synchronous quota

### Use Cases and Sizing

| Use case | Typical batch size | Est. turnaround |
|---|---|---|
| Document summarization | 100–5,000 | Minutes–hours |
| Eval run over test set | 500–10,000 | Hours |
| Dataset annotation | 1,000–10,000 | Hours |
| Bulk content generation | 50–2,000 | Minutes–hours |

### Production Pattern: Queue + Batch
For ongoing high-volume workloads, combine a job queue with the batch API:
1. Enqueue items as they arrive
2. Every N minutes (or when queue hits 500+), flush queue into a batch
3. Store `batch_id` → `custom_id[]` mapping in a database
4. Poll batch status on a cron, write results to DB when `processing_status == "ended"`
5. Expose results via an API to downstream consumers

## Example

Annotating 2,000 customer support tickets with sentiment and category:

```python
tickets = load_tickets_from_db()  # 2,000 rows

requests = [
    {
        "custom_id": str(ticket["id"]),
        "params": {
            "model": "claude-haiku-4-5",
            "max_tokens": 64,
            "system": "Respond with JSON only: {\"sentiment\": \"positive|neutral|negative\", \"category\": \"billing|technical|general\"}",
            "messages": [{"role": "user", "content": ticket["text"]}],
        },
    }
    for ticket in tickets
]

batch = client.messages.batches.create(requests=requests)
batch = wait_for_batch(batch.id)

results = {}
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        import json
        data = json.loads(result.result.message.content[0].text)
        results[result.custom_id] = data

save_annotations_to_db(results)
# Total cost: ~50% less than running 2,000 synchronous calls
```

---
