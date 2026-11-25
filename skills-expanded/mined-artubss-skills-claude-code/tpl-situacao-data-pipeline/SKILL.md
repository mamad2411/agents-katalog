---
name: tpl-situacao-data-pipeline
description: Template do pack (situacao/15-data-pipeline.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/15-data-pipeline.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Building a Data Pipeline

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/15-data-pipeline.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when building ETL/ELT pipelines, data ingestion systems, transformation flows, event streaming consumers, batch processing jobs, or any automated system that moves and transforms data from source to destination. Data pipelines fail silently in unique ways — data can be wrong, missing, duplicated, or stale without triggering any error. This configuration prevents those failure modes.

## OBJECTIVES
- Build pipelines that are idempotent and safe to re-run
- Never mutate or destroy source data
- Catch data quality failures before they reach the destination
- Make pipeline failures loud, specific, and actionable
- Enable full reprocessing (backfill) from any point in history

## APPROACH RULES

1. **Immutability of source is sacred.** Never write to, modify, or delete source data. Always read-only. Create your own layer for transformed data. If you must archive source data, move → verify → delete, never overwrite.

2. **Idempotency is required, not optional.** Running the same pipeline twice (or 100 times) must produce the same result. Design for: unique keys on destination inserts, upsert semantics, checkpointing. A pipeline that creates duplicates on re-run is a liability.

3. **Schema evolution is a first-class concern.** Source data schemas change. Your pipeline must handle: new fields (ignore safely), removed fields (use defaults), type changes (explicit coercion with error on failure). Never deploy a pipeline that crashes on new schema versions.

4. **Validation gates are mandatory.** Add explicit quality checks at ingress: expected row counts, null checks on required fields, value range checks, referential integrity checks. Reject bad data early — downstream systems cannot clean up garbage.

5. **Data pipeline failures must be loud.** A failed pipeline that logs an error and continues is worse than one that stops. Configure: alerting on job failure, data freshness monitoring (alert if output not updated in N hours), row count anomaly detection.

6. **Backfill strategy must exist before production.** "What happens if we need to reprocess the last 90 days?" must have a clear answer before go-live. Design partition schemes and checkpointing to make backfill straightforward.

7. **Timestamps in UTC, always.** Never store timezone-ambiguous timestamps. Convert to UTC at ingestion. Store timezone information as a separate field if needed.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Duplicate records in destination | Add idempotency key. Use upsert (INSERT ... ON CONFLICT DO UPDATE) or deduplication step. |
| Missing records (silent data loss) | Add row count reconciliation. Expected rows from source vs actual rows in destination. Alert on mismatch. |
| Source schema changed unexpectedly | Schema registry or schema evolution strategy needed. Add schema validation at pipeline entry. |
| NULL values in required fields | Reject the record at validation gate. Send to dead-letter queue for investigation. |
| Pipeline taking too long | Profile: is it I/O-bound (batching too small)? CPU-bound (transformation logic)? Add parallelism at bottleneck stage. |
| Backfill required after bug fix | Use partition-based reprocessing. Never backfill the entire table if you can target a date range. |
| External API as source (rate limits) | Implement checkpointing. On rate limit: save progress, wait, resume. Don't re-fetch already-processed records. |
| Large files (GB+) | Stream processing, never load to memory. Use chunked reads. Process → emit → discard chunk. |
| Transformation failure on 1 bad record | Send to dead-letter queue. Continue processing valid records. Alert on DLQ growth. |
| Data freshness degrading | Instrument and alert on lag: time between event occurrence and destination visibility. |

## Pipeline Architecture Patterns

```
Batch Pipeline (pull):
Source → Extract → Validate → Transform → Load → Verify

Streaming Pipeline (push):
Source Events → Kafka/SQS → Consumer → Validate → Transform → Sink

Lambda Architecture (both):
Streaming: realtime estimates (approximation)
Batch: reprocessing for accuracy (ground truth)
```

## Checkpoint Template

```python
class PipelineCheckpoint:
    """Track pipeline progress for resume-on-failure and backfill."""
    
    def __init__(self, pipeline_id: str, storage: CheckpointStorage):
        self.pipeline_id = pipeline_id
        self.storage = storage
    
    def save(self, last_processed_id: str, processed_count: int) -> None:
        self.storage.set(self.pipeline_id, {
            "last_processed_id": last_processed_id,
            "processed_count": processed_count,
            "updated_at": datetime.utcnow().isoformat()
        })
    
    def load(self) -> Optional[dict]:
        return self.storage.get(self.pipeline_id)
    
    def reset(self) -> None:
        """Clear checkpoint to trigger full reprocessing."""
        self.storage.delete(self.pipeline_id)
```

## Data Validation Gates

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]

def validate_payment_record(record: dict) -> ValidationResult:
    errors = []
    
    # Required fields
    for field in ['transaction_id', 'amount', 'currency', 'created_at']:
        if field not in record or record[field] is None:
            errors.append(f"Missing required field: {field}")
    
    # Type checks
    if 'amount' in record and not isinstance(record['amount'], (int, float)):
        errors.append(f"amount must be numeric, got: {type(record['amount'])}")
    
    # Range checks
    if 'amount' in record and record.get('amount', 0) <= 0:
        errors.append(f"amount must be positive, got: {record['amount']}")
    
    # Enum checks
    valid_currencies = {'USD', 'EUR', 'BRL'}
    if record.get('currency') not in valid_currencies:
        errors.append(f"Invalid currency: {record.get('currency')}")
    
    return ValidationResult(passed=len(errors) == 0, errors=errors)
```

## Dead Letter Queue Pattern

```python
def process_record(record: dict, dlq: DeadLetterQueue) -> None:
    validation = validate_record(record)
    
    if not validation.passed:
        dlq.send(record, reason=validation.errors, pipeline_version=PIPELINE_VERSION)
        metrics.increment('pipeline.records.rejected')
        return  # Continue with next record, don't stop pipeline
    
    try:
        transformed = transform(record)
        destination.upsert(transformed, key='transaction_id')
        metrics.increment('pipeline.records.processed')
    except Exception as e:
        dlq.send(record, reason=str(e), exception_type=type(e).__name__)
        metrics.increment('pipeline.records.failed')
        logger.error({'event': 'record_failed', 'record_id': record.get('id'), 'error': str(e)})
```

## DO NOT

- **DO NOT** write to source tables — ever, for any reason
- **DO NOT** design a pipeline that can't be re-run safely (idempotency is mandatory)
- **DO NOT** load entire large files into memory — use streaming/chunked processing
- **DO NOT** ignore records that fail validation — route to dead-letter queue, alert on DLQ growth
- **DO NOT** hardcode transformation logic that depends on specific record counts or positions
- **DO NOT** store timezone-naive timestamps — use UTC everywhere
- **DO NOT** run backfill during peak traffic hours — it will compete with production workloads
- **DO NOT** skip the row count reconciliation step — it catches silent data loss

## OUTPUT FORMAT

For each pipeline, produce:

**Pipeline Specification:**
```markdown
## Pipeline: [Name]

### Source
- System: PostgreSQL production DB (read replica)
- Table: transactions
- Extraction method: poll by updated_at (watermark)
- Schedule: every 15 minutes

### Transformations
1. Normalize currency codes to ISO 4217
2. Convert timestamps to UTC
3. Enrich with user country from users table
4. Filter out test transactions (amount = 0.01)

### Destination
- System: BigQuery
- Dataset: analytics.transactions_processed
- Load method: UPSERT on transaction_id
- Partitioned by: created_at DATE

### Validation Gates
- Required fields: transaction_id, amount (>0), currency, user_id, created_at
- Row count reconciliation: source count vs destination count within 0.1%
- Latency SLO: data visible in destination within 30 minutes of source

### Failure Handling
- Validation failures → DLQ bucket: gs://pipelines-dlq/transactions/
- Alert: PagerDuty if DLQ > 100 records in 1 hour
- Alert: PagerDuty if data freshness > 45 minutes
```

## QUALITY GATES

- [ ] Pipeline is idempotent: running twice produces identical destination state
- [ ] Source data is read-only: zero write traffic to source system
- [ ] Validation gates implemented with dead-letter queue for failed records
- [ ] Row count reconciliation runs after every batch
- [ ] Data freshness alert configured and tested
- [ ] Backfill tested for a 30-day date range on staging
- [ ] All timestamps stored in UTC
- [ ] Schema evolution tested: adding a new column to source doesn't crash pipeline
- [ ] Dead-letter queue has alert on accumulation (data quality monitoring)
- [ ] Checkpoint mechanism enables resume without reprocessing from beginning
