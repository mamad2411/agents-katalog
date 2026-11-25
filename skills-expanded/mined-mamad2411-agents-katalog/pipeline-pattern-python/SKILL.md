---
name: pipeline-pattern-python
description: Implements the Pipeline design pattern in Python for data transformation. Use when the user mentions pipeline pattern, or when you need a fixed sequence of stages that each transform data and pass to the next—ETL, parsing, data processing, or any linear transformation flow that runs to completion.
---

# Pipeline (Python)

**Why:** Pipeline runs data through a fixed sequence of stages. Each stage receives input, transforms it, and passes the result to the next. All stages run in order; there is no conditional “skip” or early exit (barring errors). You avoid one big function and keep each transformation in its own class.

**Hard constraints:** Stages share a single interface (e.g. `process(data)` returning transformed data). A pipeline composes stages in a fixed order and runs them one after another. Flow is linear—no branching or handler-driven termination.

---

## When to use

- **Data transformation:** Parse → normalize → enrich → serialize, where every step must run.
- **ETL / data processing:** Ingest, transform, load; or parse log lines, extract fields, aggregate.
- **Raw JSON sanitization:** Transform/sanitize JSON with one stage per field (or concern) to remove; build the pipeline conditionally from the request (e.g. add removal stages by response type or flags).
- **Parsing pipelines:** Raw input → tokenize → parse → build AST → emit.
- You need a fixed, mandatory sequence (unlike Chain of Responsibility, where handlers can short-circuit).

---

## Structure

| Role | Responsibility |
|------|-----------------|
| **Stage (protocol/ABC)** | Declares `process(data) => result`. Each stage receives data, returns transformed data. |
| **Concrete stages** | Implement the interface; one transformation per class. No “pass or stop” decision—always return result for next. |
| **Pipeline** | Holds an ordered list of stages; runs them in sequence, passing each stage’s output as the next stage’s input. |
| **Client** | Builds the pipeline (e.g. `Pipeline([ParseStage(), NormalizeStage(), ...])`) and runs it with initial input. |

Data flows in one direction; each stage’s output is the next stage’s input. The pipeline runs to completion (or raises at a stage).

---

## Real example: access-log ETL pipeline

A pipeline that **justifies** the pattern: raw access log text → parse → filter → enrich → normalize → aggregate → serialize. Each stage has real logic; one big function would be hard to test and extend.

**Pipeline payload:** Input `{"raw": str}`. After Parse, add `"records": list[dict]`. After Filter/Enrich/Normalize, same list refined. After Aggregate, add `"summary": {by_endpoint, total_requests, error_count, error_rate}`. After Serialize, final JSON string (or a dedicated output field).

### ❌ ANTI-PATTERN: One big function

```python
# Parsing, filtering, enrichment, aggregation, and output all in one place.
def process_access_logs(raw: str) -> str:
    lines = raw.strip().splitlines()
    records = []
    for line in lines:
        m = re.match(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\w+) ([^"]+)" (\d+)', line)
        if not m:
            continue
        ip, time, method, path, status = m[1], m[2], m[3], m[4], int(m[5])
        if status < 400:
            continue
        geo = lookup_geo(ip)
        records.append({"ip": ip, "method": method, "path": path, "status": status, "country": geo.get("country")})
    by_path = {}
    for r in records:
        key = (r["path"].split("/") or ["root"])[1] if r["path"].startswith("/") else "root"
        by_path[key] = by_path.get(key, 0) + 1
    return json.dumps({"byEndpoint": by_path, "total": len(records)})
```

Problems: parse/filter/enrich/aggregate/serialize are tangled; can’t unit-test parsing or aggregation alone; adding a stage (e.g. normalize timestamps) forces edits everywhere.

### ✅ TOP-CODER PATTERN: One stage per concern, pipeline runs all

**Stage protocol and pipeline:**

```python
# pipeline/base.py
from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class Stage(Protocol):
    def process(self, data: Any) -> Any: ...

class Pipeline:
    def __init__(self, stages: list[Stage]) -> None:
        self.stages = stages

    def run(self, input_data: Any) -> Any:
        data = input_data
        for stage in self.stages:
            data = stage.process(data)
        return data
```

**ParseStage** — split lines, parse combined log (or JSONL), skip malformed:

```python
# pipeline/stages/parse.py
import re
COMBINED_LOG = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\w+) ([^"]+)" (\d+)')

class ParseStage:
    def process(self, data: dict) -> dict:
        raw = (data.get("raw") or "").strip()
        lines = [ln for ln in raw.splitlines() if ln]
        records = []
        for line in lines:
            m = COMBINED_LOG.match(line)
            if m:
                records.append({
                    "ip": m[1], "timestamp": m[2], "method": m[3], "path": m[4],
                    "status": int(m[5]),
                })
        return {**data, "records": records}
```

**FilterStage** — configurable min status and path prefix:

```python
# pipeline/stages/filter_stage.py
class FilterStage:
    def __init__(self, min_status: int = 400, path_prefix: str | None = None) -> None:
        self.min_status = min_status
        self.path_prefix = path_prefix or ""

    def process(self, data: dict) -> dict:
        records = data.get("records", [])
        records = [r for r in records if r.get("status", 0) >= self.min_status]
        if self.path_prefix:
            records = [r for r in records if (r.get("path") or "").startswith(self.path_prefix)]
        return {**data, "records": records}
```

**EnrichStage** — add geo from IP, derive endpoint group:

```python
# pipeline/stages/enrich.py
class EnrichStage:
    def __init__(self, geo_lookup=None) -> None:
        self.geo_lookup = geo_lookup or (lambda ip: {})

    def process(self, data: dict) -> dict:
        records = []
        for r in data.get("records", []):
            geo = self.geo_lookup(r.get("ip", ""))
            path = (r.get("path") or "").strip("/")
            parts = path.split("/") if path else []
            endpoint_group = parts[0] if parts else "root"
            records.append({
                **r,
                "country": geo.get("country") if isinstance(geo, dict) else None,
                "endpoint_group": endpoint_group,
            })
        return {**data, "records": records}
```

**NormalizeStage** — consistent types and snake_case keys:

```python
# pipeline/stages/normalize.py
class NormalizeStage:
    def process(self, data: dict) -> dict:
        records = []
        for r in data.get("records", []):
            records.append({
                "ip": str(r.get("ip", "")),
                "method": (r.get("method") or "GET").upper(),
                "path": str(r.get("path", "")),
                "status": int(r.get("status", 0)),
                "timestamp": r.get("timestamp"),
                "country": r.get("country"),
                "endpoint_group": r.get("endpoint_group") or "root",
            })
        return {**data, "records": records}
```

**AggregateStage** — group by endpoint, counts and error rate:

```python
# pipeline/stages/aggregate.py
from collections import defaultdict

class AggregateStage:
    def process(self, data: dict) -> dict:
        records = data.get("records", [])
        by_endpoint = defaultdict(int)
        error_count = sum(1 for r in records if r.get("status", 0) >= 400)
        for r in records:
            by_endpoint[r.get("endpoint_group", "root")] += 1
        total = len(records)
        return {
            **data,
            "summary": {
                "by_endpoint": dict(by_endpoint),
                "total_requests": total,
                "error_count": error_count,
                "error_rate": (error_count / total) if total else 0.0,
            },
        }
```

**SerializeStage** — JSON output:

```python
# pipeline/stages/serialize.py
import json

class SerializeStage:
    def process(self, data: dict) -> dict:
        summary = data.get("summary", data)
        return {**data, "output": json.dumps(summary, indent=2)}
```

**Client** wires and runs:

```python
# services/access_log_pipeline.py
pipeline = Pipeline([
    ParseStage(),
    FilterStage(min_status=400),
    EnrichStage(geo_lookup=lookup_geo_by_ip),
    NormalizeStage(),
    AggregateStage(),
    SerializeStage(),
])
result = pipeline.run({"raw": log_file_content})
# result["output"] is JSON string
```

Benefits: parse/filter/enrich/normalize/aggregate/serialize are separate and testable; you can add stages (e.g. dedupe, rate-limit detection) or swap implementations without touching others; fixed order and run-to-completion match the Pipeline pattern.

---

## Dynamic composition: raw JSON sanitization

**Transform raw JSON by removing/redacting fields** — **one stage per removal**, and **build the pipeline conditionally from the request** (response type, `includeX` flags, etc.). Each stage does one thing; the list of stages is chosen at runtime.

**Example:** Reusable `RemoveFieldStage(path)` or dedicated stages (`RemoveInternalIdStage`, `RemovePasswordStage`, `RemoveAuditFieldsStage`). Build stages list from request:

```python
def build_sanitize_pipeline(
    is_user: bool = False,
    is_payment: bool = False,
    include_audit: bool = True,
) -> Pipeline:
    stages: list[Stage] = [
        RemoveInternalIdStage(),
        RemoveFieldStage("_rev"),
    ]
    if is_user:
        stages.extend([RemovePasswordStage(), RemoveFieldStage("tokens")])
    elif is_payment:
        stages.extend([RemoveFieldStage("cardNumber"), RemoveFieldStage("cvv")])
    if not include_audit:
        stages.append(RemoveAuditFieldsStage())
    return Pipeline(stages)

pipeline = build_sanitize_pipeline(is_user=True, include_audit=False)
sanitized = pipeline.run(raw_json_from_db)
```

Pipeline stays linear; only the **composition** is conditional.

---

## Python notes

- **Sync vs async:** For async stages, use `async def process(self, data)` and `async for` or a simple loop with `await` in the pipeline runner.
- **Error handling:** Pipeline typically fails fast: if a stage raises, the pipeline stops. Handle in the runner or in stages.
- **Protocol vs ABC:** Prefer `typing.Protocol` for the stage contract so concrete classes need not inherit.
- **No overkill:** For two or three fixed steps, a simple composition of functions may be enough; use Pipeline when you have many steps or need to reuse/reorder stages.

---

## Chain of Responsibility vs Pipeline

| Feature | Pipeline | Chain of Responsibility |
|---------|----------|--------------------------|
| **Execution** | Fixed, mandatory sequence | Conditional; handler decides whether to pass to the next |
| **Flow** | Linear, no branching | Allows flexible termination and branching |
| **Termination** | Runs to completion (barring errors) | Can be terminated early by a handler |
| **Use cases** | Data processing, parsing, ETL | Event handling, approval workflows, validation, message filtering |

Use **Pipeline** when every stage must run in a fixed order (e.g. data transformation). Use **CoR** when handlers can short-circuit or decide not to pass (e.g. validation, approval chains).

---

## Reference

- Pipeline is a common architectural pattern; related to Unix pipes, middleware chains (with fixed flow), and ETL pipelines.
