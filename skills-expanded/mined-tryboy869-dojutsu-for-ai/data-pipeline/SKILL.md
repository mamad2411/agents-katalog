---
name: data-pipeline
description: "Apply when building ETL pipelines, data processing workflows, batch jobs, or streaming data systems. Covers: chunking, idempotency, error handling, progress tracking, schema validation. Trigger for: ETL, pipeline, batch, data processing, CSV, transform, extract, load."
---

# DATA PIPELINE — Production ETL Patterns

## Core Principles
- **Idempotent**: running twice produces same result (no duplicates)
- **Resumable**: checkpoint progress, restart from last success
- **Observable**: log every step with counts and timing
- **Validated**: check schema before processing

## Chunked Processing (never load all in memory)
```python
async def process_large_file(filepath: str, chunk_size: int = 1000):
    checkpoint = await load_checkpoint(filepath)
    processed = checkpoint.get("rows_done", 0)
    
    async with aiofiles.open(filepath) as f:
        reader = csv.DictReader(f)
        chunk = []
        
        for i, row in enumerate(reader):
            if i < processed:
                continue  # skip already processed
            
            chunk.append(validate_row(row))
            
            if len(chunk) >= chunk_size:
                await process_chunk(chunk)
                processed += len(chunk)
                await save_checkpoint(filepath, {"rows_done": processed})
                chunk = []
                log.info("pipeline.progress", rows=processed)
        
        if chunk:
            await process_chunk(chunk)
```

## Schema Validation
```python
from pydantic import BaseModel, validator

class InputRow(BaseModel):
    id: str
    amount: float
    currency: str
    date: datetime
    
    @validator("currency")
    def valid_currency(cls, v):
        if v not in ["USD", "EUR", "XOF"]:
            raise ValueError(f"Unknown currency: {v}")
        return v

def validate_row(raw: dict) -> InputRow:
    try:
        return InputRow(**raw)
    except ValidationError as e:
        log.error("pipeline.validation_error", row=raw, errors=e.errors())
        raise
```

## Idempotent Upsert
```python
# Always upsert, never blind insert
await db.execute("""
    INSERT INTO processed_records (source_id, data, processed_at)
    VALUES (:id, :data, NOW())
    ON CONFLICT (source_id) DO UPDATE
    SET data = EXCLUDED.data, processed_at = NOW()
""", {"id": row.id, "data": row.dict()})
```

## Monitoring
```python
# Every pipeline run logs start/end/errors
@contextmanager
def pipeline_run(name: str):
    start = time.time()
    log.info(f"pipeline.start", name=name)
    try:
        yield
        log.info(f"pipeline.success", name=name, duration=time.time()-start)
    except Exception as e:
        log.error(f"pipeline.failed", name=name, error=str(e))
        raise
```

## Forbidden
❌ Loading entire file into memory
❌ No checkpointing for long-running pipelines
❌ Inserting without checking for duplicates
❌ No validation before transformation
❌ Silent failures (swallowed exceptions)
