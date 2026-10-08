---
name: data-pipelines-ai
description: Data pipelines for AI workflows — Airflow DAGs, Prefect flows, Kafka streaming, batch vs streaming, data versioning, chunking, idempotent design, dataset curation, and pipeline monitoring.
origin: AI Dev Kit
---

# Data Pipelines for AI

Design, implement, and operate robust data pipelines that feed AI/ML systems: orchestration with Airflow and Prefect, streaming with Kafka, data versioning, dataset curation, embedding backfills, idempotent design, and production monitoring.

## When to Use

- Building ingestion, transformation, and embedding pipelines for RAG or ML training
- Need reliable orchestration with retries, backfills, and dependency management
- Processing document collections at scale with chunking, embedding, and vector store updates
- Streaming real-time data into AI systems with exactly-once or at-least-once semantics
- Curating and versioning datasets with quality gates, PII scrubs, and synthetic augmentation
- Monitoring pipeline health: data freshness, drift, failure rates, and SLA compliance

## Core Concepts

### 1. Airflow DAG Design

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import pendulum

default_args = {
    "owner": "ml-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
}

dag = DAG(
    "rag_embedding_pipeline",
    default_args=default_args,
    description="Ingest, chunk, embed, and load documents into vector store",
    schedule="@daily",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["rag", "embeddings", "production"],
)

def ingest_documents(**kwargs):
    """Pull documents from source, write to staging."""
    ti = kwargs["ti"]
    docs = fetch_from_cms(api_key=Variable.get("CMS_API_KEY"))
    staged_path = f"/data/staging/docs_{kwargs['ds']}.jsonl"
    write_jsonl(docs, staged_path)
    ti.xcom_push(key="staged_path", value=staged_path)
    return {"count": len(docs), "path": staged_path}

def chunk_documents(**kwargs):
    """Read staged docs, split into chunks, write chunked output."""
    ti = kwargs["ti"]
    staged_path = ti.xcom_pull(task_ids="ingest", key="staged_path")
    docs = read_jsonl(staged_path)
    chunks = recursive_chunk(docs, chunk_size=512, overlap=128)
    chunked_path = f"/data/staging/chunks_{kwargs['ds']}.jsonl"
    write_jsonl(chunks, chunked_path)
    ti.xcom_push(key="chunked_path", value=chunked_path)
    return {"chunk_count": len(chunks)}

def embed_and_load(**kwargs):
    """Generate embeddings and upsert into vector store."""
    ti = kwargs["ti"]
    chunked_path = ti.xcom_pull(task_ids="chunk", key="chunked_path")
    chunks = read_jsonl(chunked_path)
    embeddings = generate_embeddings(chunks, model="text-embedding-3-small")
    upsert_to_pinecone(chunks, embeddings, namespace="production")

wait_for_docs = FileSensor(
    task_id="wait_for_source_files",
    filepath="/data/incoming/*.jsonl",
    poke_interval=60,
    timeout=3600,
    dag=dag,
)

ingest = PythonOperator(task_id="ingest", python_callable=ingest_documents, dag=dag)
chunk = PythonOperator(task_id="chunk", python_callable=chunk_documents, dag=dag)
embed = PythonOperator(task_id="embed_and_load", python_callable=embed_and_load, dag=dag)

ingest >> chunk >> embed
wait_for_docs >> ingest
```

**Custom Operator** for vector store upsert:

```python
from airflow.models import BaseOperator

class PineconeUpsertOperator(BaseOperator):
    """Upsert embeddings into Pinecone with idempotent writes."""
    template_fields = ("chunks_path", "embeddings_path", "namespace")

    def __init__(self, chunks_path, embeddings_path, namespace, **kwargs):
        super().__init__(**kwargs)
        self.chunks_path = chunks_path
        self.embeddings_path = embeddings_path
        self.namespace = namespace

    def execute(self, context):
        chunks = read_jsonl(self.chunks_path)
        embeddings = np.load(self.embeddings_path)
        client = get_pinecone_client()
        index = client.Index("rag-index")
        upsert_batch(index, chunks, embeddings, namespace=self.namespace, batch_size=100)
        self.log.info(f"Upserted {len(chunks)} vectors to {self.namespace}")
```

### 2. Prefect Flows

```python
from prefect import flow, task, get_run_logger
from prefect.deployments import Deployment
from prefect.blocks.system import Secret

@task(retries=3, retry_delay_seconds=30, timeout_seconds=600)
def ingest_documents(source_url: str) -> list[dict]:
    logger = get_run_logger()
    logger.info(f"Ingesting from {source_url}")
    docs = fetch_documents(source_url)
    logger.info(f"Ingested {len(docs)} documents")
    return docs

@task(retries=2, retry_delay_seconds=15)
def chunk_documents(documents: list[dict], chunk_size: int = 512) -> list[dict]:
    return recursive_chunk(documents, chunk_size=chunk_size, overlap=128)

@task
def generate_embeddings(chunks: list[dict], model: str = "text-embedding-3-small") -> np.ndarray:
    return embed_chunks(chunks, model=model)

@task
def upsert_to_vector_store(chunks: list[dict], embeddings: np.ndarray, namespace: str):
    index = get_pinecone_client().Index("rag-index")
    upsert_batch(index, chunks, embeddings, namespace=namespace)

@flow(name="rag-pipeline", version="2.0", log_prints=True)
def rag_embedding_pipeline(
    source_url: str = "s3://docs-bucket/latest/",
    chunk_size: int = 512,
    namespace: str = "production",
):
    """Main RAG embedding pipeline flow."""
    docs = ingest_documents(source_url)
    chunks = chunk_documents(docs, chunk_size=chunk_size)
    embeddings = generate_embeddings(chunks)
    upsert_to_vector_store(chunks, embeddings, namespace)
    print(f"Pipeline complete: {len(chunks)} chunks embedded and upserted")

# Deployment
Deployment.build_from_flow(
    flow=rag_embedding_pipeline,
    name="daily-rag-pipeline",
    schedule={"cron": "0 2 * * *", "timezone": "America/New_York"},
    work_pool_name="default-agent-pool",
    parameters={"source_url": "s3://docs-bucket/latest/", "chunk_size": 512},
)
```

### 3. Kafka Streaming for Real-Time RAG Updates

```python
from confluent_kafka import Producer, Consumer, KafkaError
import json

# Producer — stream new documents into the pipeline
producer = Producer({
    "bootstrap.servers": "kafka-1:9092,kafka-2:9092",
    "acks": "all",
    "retries": 5,
    "enable.idempotence": True,
})

def deliver_new_document(doc: dict, topic: str = "documents.raw"):
    """Publish new document to Kafka with partitioning by source."""
    key = doc["source_id"].encode("utf-8")
    producer.produce(
        topic=topic,
        key=key,
        value=json.dumps(doc).encode("utf-8"),
        callback=delivery_callback,
    )
    producer.poll(0)

def delivery_callback(err, msg):
    if err:
        print(f"Failed to deliver: {err}", flush=True)

# Consumer — process documents through the pipeline
consumer = Consumer({
    "bootstrap.servers": "kafka-1:9092,kafka-2:9092",
    "group.id": "rag-ingestion-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,  # Manual commit for exactly-once
})
consumer.subscribe(["documents.raw"])

# Schema Registry for type safety
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

schema_client = SchemaRegistryClient({"url": "http://schema-registry:8081"})
doc_schema = """
{
  "type": "object",
  "properties": {
    "source_id": {"type": "string"},
    "content": {"type": "string"},
    "metadata": {"type": "object"},
    "timestamp": {"type": "string", "format": "date-time"}
  },
  "required": ["source_id", "content", "timestamp"]
}
"""
serializer = JSONSerializer(schema_str=doc_schema, schema_registry_client=schema_client)

# Dead-letter queue for malformed messages
dlq_producer = Producer({"bootstrap.servers": "kafka-1:9092"})

def process_with_dlq():
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            print(f"Consumer error: {msg.error()}")
            continue

        try:
            doc = json.loads(msg.value().decode("utf-8"))
            validate_document(doc)
            process_document(doc)
            consumer.commit(msg)  # Commit only after successful processing
        except Exception as e:
            # Send to dead-letter queue
            dlq_producer.produce(
                topic="documents.dlq",
                key=msg.key(),
                value=msg.value(),
                headers=[("error", str(e).encode()), ("original_topic", msg.topic().encode())],
            )
            dlq_producer.poll(0)
            consumer.commit(msg)  # Commit to avoid infinite reprocessing
```

### 4. Batch vs Streaming Trade-Offs

| Criteria | Batch | Streaming |
|----------|-------|-----------|
| **Latency** | Hours to days | Seconds to minutes |
| **Cost** | Lower (scheduled compute) | Higher (always-on consumers) |
| **Complexity** | Simpler, easier to debug | Ordering, watermarking, DLQ |
| **RAG Suitability** | Daily doc refreshes, reports | Real-time chat, live knowledge |
| **Idempotency** | Easier (rerun full batch) | Requires offset tracking |
| **Backfill** | Natural (re-run DAG) | Replay from offset |

**Recommendation**: Use batch for daily embedding backfills and streaming for real-time document ingestion. Hybrid: stream raw docs to storage, batch-process into embeddings.

### 5. Data Versioning

```bash
# DVC for dataset versioning
dvc add data/training/rag_qa_pairs.jsonl
dvc add data/embeddings/v2_embeddings.npy
git add data/*.dvc .gitignore
git commit -m "Version RAG training data v2"

# LakeFS for branching and promotion
lakectl branch create lakefs://rag-data/main@refs/branches/staging
# Work on staging, then merge
lakectl merge lakefs://rag-data/staging lakefs://rag-data/main
# Tag release
lakectl tag create lakefs://rag-data/main v2.1.0
```

**Hashing Strategy** for data integrity:

```python
import hashlib

def compute_data_hash(records: list[dict]) -> str:
    """Compute SHA-256 hash of sorted, serialized records for integrity."""
    serialized = json.dumps(sorted(records, key=lambda r: r.get("id", "")), sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()

# Verify at each pipeline stage
input_hash = compute_data_hash(raw_docs)
assert input_hash == expected_hash, f"Data integrity check failed: {input_hash}"
```

### 6. Dataset Curation

**PII Scrubbing**:

```python
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

def scrub_pii(text: str) -> tuple[str, dict]:
    """Detect and anonymize PII in text, return scrubbed text and metadata."""
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    results = analyzer.analyze(text=text, language="en", entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS"])
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)

    scrubbed_text = anonymized.text
    metadata = {
        "pii_detected": len(results),
        "entities": [r.entity_type for r in results],
        "scrubbed": True,
    }
    return scrubbed_text, metadata
```

**Synthetic Data Augmentation**:

```python
def augment_with_paraphrasing(qa_pairs: list[dict], llm_client) -> list[dict]:
    """Generate paraphrased questions to expand training dataset."""
    augmented = []
    for qa in qa_pairs:
        prompt = f"""Paraphrase this question 3 ways while keeping the same meaning:
Question: {qa['question']}
Return as a JSON array of strings."""
        response = llm_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        paraphrases = json.loads(response.choices[0].message.content)["paraphrases"]
        for paraphrase in paraphrases:
            augmented.append({
                "question": paraphrase,
                "answer": qa["answer"],
                "contexts": qa["contexts"],
                "source": "synthetic_paraphrase",
            })
    return qa_pairs + augmented
```

### 7. Idempotent Pipeline Design

```python
def upsert_with_idempotency(chunks: list[dict], embeddings: np.ndarray, index, namespace: str):
    """Idempotent upsert: same input always produces same output."""
    for chunk, embedding in zip(chunks, embeddings):
        doc_id = f"{chunk['source_id']}:{chunk['chunk_index']}"
        vector = {
            "id": doc_id,
            "values": embedding.tolist(),
            "metadata": {
                "source_id": chunk["source_id"],
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
                "data_hash": chunk.get("data_hash"),
                "updated_at": datetime.utcnow().isoformat(),
            },
        }
        # Upsert replaces existing vector with same ID
        index.upsert(vectors=[vector], namespace=namespace)

def process_pipeline(run_id: str):
    """Full pipeline with idempotent stages — safe to re-run."""
    # Stage 1: Ingest (idempotent — overwrites staging)
    raw_docs = ingest_documents()
    write_staging(raw_docs, run_id)

    # Stage 2: Chunk (idempotent — deterministic chunking)
    chunks = chunk_documents(raw_docs)
    for c in chunks:
        c["run_id"] = run_id
        c["data_hash"] = compute_data_hash([c])

    # Stage 3: Embed (idempotent — same model, same input → same output)
    embeddings = generate_embeddings(chunks)

    # Stage 4: Upsert (idempotent — replaces by doc_id)
    upsert_with_idempotency(chunks, embeddings, pinecone_index, "production")

    # Stage 5: Verify
    verify_counts(raw_docs, chunks, embeddings)
```

### 8. Pipeline Monitoring

```python
# Data Freshness SLA Monitoring
from prometheus_client import Counter, Histogram, Gauge

PIPELINE_DURATION = Histogram("pipeline_duration_seconds", "Pipeline end-to-end duration")
FRESHNESS_LAG = Gauge("data_freshness_lag_seconds", "Time since last successful pipeline run")
CHUNK_COUNT = Gauge("chunks_processed_total", "Total chunks processed", ["namespace"])
FAILURE_COUNT = Counter("pipeline_failures_total", "Pipeline failure count", ["stage"])
EMBEDDING_LATENCY = Histogram("embedding_latency_ms", "Embedding generation latency")

def monitor_freshness():
    """Alert if data is stale — call from monitoring job."""
    last_run = get_last_successful_run()
    lag = (datetime.utcnow() - last_run).total_seconds()
    FRESHNESS_LAG.set(lag)
    if lag > 86400:  # 24 hours
        send_alert(f"RAG data stale: {lag / 3600:.1f} hours since last run")

def monitor_data_drift(current_embeddings: np.ndarray, reference_stats: dict):
    """Detect embedding distribution drift using statistical tests."""
    current_mean = np.mean(current_embeddings, axis=0)
    ref_mean = np.array(reference_stats["mean"])
    drift = np.linalg.norm(current_mean - ref_mean)
    if drift > reference_stats["threshold"]:
        send_alert(f"Embedding drift detected: {drift:.4f} > {reference_stats['threshold']:.4f}")
```

## Anti-Patterns

- **Non-idempotent upserts** — appending instead of upserting, causing duplicate vectors on re-runs
- **No dead-letter queue** — silently dropping malformed Kafka messages without alerting or replay
- **Missing data contracts** — no schema validation at pipeline boundaries, allowing corrupt data downstream
- **No freshness monitoring** — embeddings silently stale for weeks because nobody tracks last run time
- **Chunking without overlap** — losing context at chunk boundaries, hurting retrieval quality
- **Backfilling without versioning** — overwriting production embeddings without tracking what changed
- **No PII scrubbing** — leaking sensitive data into vector stores and LLM contexts
- **Hard-coded credentials in DAGs** — secrets in Airflow variable definitions instead of Secret backends
- **Silent retries** — infinite retry loops without max attempts or exponential backoff
- **No pipeline-level timeouts** — a single slow stage blocks the entire DAG indefinitely

## Best Practices

1. **Design every stage to be idempotent** — safe to re-run any stage without side effects
2. **Use XComs sparingly** — pass only metadata (file paths, counts); store large data externally
3. **Implement data contracts** — validate schemas at every pipeline boundary with JSON Schema or Pydantic
4. **Set freshness SLAs** — alert if embeddings are older than your RAG system's staleness tolerance
5. **Always include a DLQ** — never silently drop messages; log errors and route to dead-letter topics
6. **Version datasets with DVC or LakeFS** — enable rollback and audit trail for training data
7. **Scrub PII at ingestion** — use Presidio or similar before data enters the pipeline
8. **Monitor embedding distribution drift** — compare rolling statistics against baselines weekly
9. **Use retry with exponential backoff** — configure `retry_delay` and `retry_exponential_backoff` in Airflow
10. **Test pipelines with production-like data** — run integration tests against sampled production data, not just fixtures

## Related Skills

- **mlops-rag** — evaluation and model versioning for the outputs of data pipelines
- **aws-devops** — deploying Airflow/Prefect on ECS, Lambda triggers, and Kafka on MSK
- **observability-telemetry** — metrics, logging, and alerting for pipeline health
- **multi-agent-git-workflow** — coordinating parallel development on pipeline features
