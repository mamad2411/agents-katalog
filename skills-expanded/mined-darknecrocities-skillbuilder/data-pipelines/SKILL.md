---
name: data-pipelines
description: Data pipeline engineering, streaming ETL with backpressure, Apache Arrow memory structures, DuckDB in-process analytics, schema validation, and dead-letter queues (DLQ).
---

# Data Pipelines, Streaming Ingest & Embedded Analytics (`/data-pipelines`)

> **Philosophy**: *Unbounded in-memory aggregation is an architectural failure. Stream large datasets with backpressure. Validate schemas at every record boundary. Enforce idempotency on batch runs. Route poisoned records to Dead-Letter Queues (DLQ) without crashing the pipeline.*

This skill establishes defensive engineering standards for data pipelines, batch ETL, and embedded analytical workloads using **DuckDB**, **Apache Arrow**, **Polars**, and **Pandas**.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/streaming-etl-and-arrow.md](references/streaming-etl-and-arrow.md) | Columnar memory, zero-copy RecordBatches, bounded queue backpressure. |
| **Reference** | [references/duckdb-and-dlq-patterns.md](references/duckdb-and-dlq-patterns.md) | Vectorized in-process analytics, Parquet queries, DLQ quarantine schemas. |
| **Utility** | [scripts/verify_pipeline_integrity.py](scripts/verify_pipeline_integrity.py) | Scans pipeline code for unbounded reads, missing DLQ handling, and unindexed joins. |

---

## 2. The Core Pipeline Architecture Gates

```mermaid
flowchart TD
    A["Raw Ingestion Stream (CSV / JSONL / Parquet)"] --> B["Gate 1: Streaming Ingest with Backpressure (Chunked IO)"]
    B --> C["Gate 2: Schema Validation (Pydantic / Zod / Arrow Types)"]
    C --> D["Gate 3: Dead-Letter Routing (Quarantine Poisoned Rows)"]
    D --> E["Gate 4: In-Process Analytical Queries (DuckDB / Arrow Vectors)"]
    E --> F["Gate 5: Idempotent Sink & Checkpointing (ACID Commit)"]
```

1. **Gate 1: Chunked Streaming IO**: Prohibit loading entire multi-megabyte datasets into memory with unbuffered reads. Process records in bounded chunks (e.g., 5,000–10,000 rows).
2. **Gate 2: Strict Record Boundary Validation**: Validate all incoming payloads against typed schemas before executing transformations.
3. **Gate 3: Dead-Letter Queue (DLQ) Isolation**: When an individual record fails transformation, route it with failure metadata to a DLQ table or storage path rather than terminating the entire pipeline batch.
4. **Gate 4: High-Performance In-Process Analytics**: Use **DuckDB** or **Apache Arrow** zero-copy columnar buffers for local aggregations, filtering, and analytical queries.
5. **Gate 5: Idempotent Delivery & Deduplicated Pre-Sink Snapshot**: Every pipeline batch run must use an idempotency key (`batch_id` / `hash(data)`) to prevent duplicate writes during retries, and maintain a single SHA-256 deduplicated backup slot (`manage_deduplicated_backup.py`) before overwriting analytical tables. Never purge Dead-Letter Queues (DLQ) or target sinks without notifying the user first.

---

## 2. Resilient Streaming Pipeline with DLQ (Python)

```python
import io
import csv
from typing import Generator, Dict, Any, List, Tuple
from pydantic import BaseModel, ValidationError

class TransactionRecord(BaseModel):
    transaction_id: str
    amount: float
    account_id: str

def process_stream_chunk(
    csv_stream: io.TextIOBase,
    chunk_size: int = 5000
) -> Generator[Tuple[List[TransactionRecord], List[Dict[str, Any]]], None, None]:
    """Streams CSV chunks with schema validation and dead-letter queue routing."""
    reader = csv.DictReader(csv_stream)
    valid_batch: List[TransactionRecord] = []
    dead_letter_batch: List[Dict[str, Any]] = []

    for row in reader:
        try:
            valid_batch.append(TransactionRecord(**row))
        except ValidationError as err:
            dead_letter_batch.append({"raw_row": row, "error": str(err)})

        if len(valid_batch) + len(dead_letter_batch) >= chunk_size:
            yield valid_batch, dead_letter_batch
            valid_batch = []
            dead_letter_batch = []

    if valid_batch or dead_letter_batch:
        yield valid_batch, dead_letter_batch
```

---

## 3. High-Performance Embedded DuckDB Analytics (Python)

```python
import duckdb

def compute_tenant_summary(parquet_path: str) -> list:
    """Executes vectorized SQL over Parquet files without loading data into Python memory."""
    con = duckdb.connect(database=":memory:")
    query = """
        SELECT 
            account_id,
            count(*) AS total_transactions,
            sum(amount) AS gross_volume,
            avg(amount) AS average_ticket
        FROM read_parquet(?)
        WHERE amount > 0
        GROUP BY account_id
        ORDER BY gross_volume DESC
        LIMIT 50;
    """
    return con.execute(query, [parquet_path]).fetchall()
```

---

## 4. Pipeline Integrity Verification CLI

Audit pipeline scripts for unbuffered in-memory loading and missing dead-letter queues:

```bash
python3 skills/data-pipelines/scripts/verify_pipeline_integrity.py --path . --strict
```

Audited Rules:
- `PIPELINE-UNBOUNDED-READ`: Flags `read_csv()` without `chunksize` or unbuffered `f.read()` on large streams.
- `PIPELINE-MISSING-DEAD-LETTER-QUEUE`: Flags batch pipelines discarding failed records silently without DLQ routing.
- `PIPELINE-MISSING-SCHEMA-VALIDATION`: Flags pipelines passing raw string dictionaries directly to analytical sinks.
