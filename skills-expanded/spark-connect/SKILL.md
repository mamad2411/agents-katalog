---
name: spark-connect
description: "Knowledge base for Spark Connect (Apache Spark 3.4–3.5). Use when preparing for Sec 6 of the Databricks Certified Associate Developer for Apache Spark exam, configuring a Spark Connect client/server, or migrating PySpark code to the decoupled client-server architecture. Sources: spark.apache.org 3.5.7 docs + Databricks engineering blog."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, connection method, or chapter number]
---

# Spark Connect — Exam-Prep Knowledge Base
**Source Spark version**: **3.5.7** (latest 3.5.x docs) + **3.4 launch context** | **Chapters**: 5 | **Generated**: 2026-05-24

> **Scope rule**: Anything from **Spark 3.4 ≤ version ≤ 3.5.x** is **in scope** for the Databricks Certified Associate Developer for Apache Spark exam (Sec 6). Anything from **Spark 4.x** is flagged ⚠️ as **out of exam scope**. The skill is conservative — when 4.x docs were used, content is marked accordingly.

## How to Use This Skill

- **Without arguments** — loads the Core Frameworks below (Spark Connect at exam depth).
- **By topic** — ask about `gRPC`, `unresolved logical plan`, `sc:// URL`, `SPARK_REMOTE`, `start-connect-server.sh`, etc. → I find and read the relevant chapter.
- **By chapter** — `ch01`, `ch02`, `ch03`, `ch04`, `ch05`.

---

## Core Frameworks & Mental Models

### Spark Connect in one paragraph
**Spark Connect = decoupled client-server architecture for Apache Spark**, introduced in **Spark 3.4** and matured for Scala in **3.5**. The client (any language) builds a DataFrame query, serializes it as an **unresolved logical plan** in **protocol buffers**, ships it over **gRPC** to a Spark Connect server embedded in the Spark driver. The server resolves the plan against its Catalog, runs Catalyst + Tungsten as normal, and streams results back as **Apache Arrow** row batches. Result: thin clients, isolated client failures, independent upgrades.

### Why it exists (4 pain points it solves)
1. **Stability** — a misbehaving user app can't crash the shared driver
2. **Upgradability** — driver upgrades independently of clients (stable protobuf protocol)
3. **Debuggability** — client is a normal local process you can attach a debugger to
4. **Language flexibility** — protocol is language-agnostic; multiple language clients possible

### The wire protocol (memorize for the exam)
- **Unresolved logical plans** as the language-agnostic protocol
- Encoded with **Protocol Buffers**
- Transported over **gRPC** (HTTP/2)
- Results return as **Apache Arrow** row batches

### Connection URL format
```
sc://<host>[:<port>][/;token=<token>]
```
- Scheme: **`sc://`** (Spark Connect)
- **Default port: 15002**
- Optional `;token=...` parameter (opaque, forwarded to any HTTP/2 auth proxy in front)

### 3 ways to connect a client (all 3 in scope)

| # | Method | When to use |
|---|---|---|
| 1 | **`SPARK_REMOTE` env var** | Zero-code-change reuse of existing PySpark scripts |
| 2 | **`--remote` CLI flag** | Ad-hoc interactive shells |
| 3 | **`SparkSession.builder.remote("sc://...")`** | Standalone apps |

```python
# Method 3, Python:
from pyspark.sql import SparkSession
spark = (SparkSession.builder
         .remote("sc://localhost:15002")
         .appName("MyApp")
         .getOrCreate())
```

### Server start (memorize the exact command shape)
```bash
./sbin/start-connect-server.sh \
  --packages org.apache.spark:spark-connect_2.12:3.5.7
```
- Lives in `$SPARK_HOME/sbin/`
- `--packages` coordinate **must match** the Spark distribution version
- Default port **15002**
- Stop: `./sbin/stop-connect-server.sh`

### Client install (Python)
```bash
pip install "pyspark[connect]==3.5.7"
```
Pulls `grpcio>=1.48,<1.57`, `grpcio-status`, `googleapis-common-protos==1.56.4`, `pyarrow>=4.0.0,<13.0.0`, `pandas>=1.0.5`. Requires **Python 3.8+** and **Java 8/11/17**.

### Client install (Scala sbt)
```scala
libraryDependencies += "org.apache.spark" %% "spark-sql-api" % "3.5.7"
libraryDependencies += "org.apache.spark" %% "spark-connect-client-jvm" % "3.5.7"
```

### API support at a glance (Spark 3.5)

| Surface | PySpark | Scala |
|---|---|---|
| DataFrame / Functions / Column | ✅ (3.4) | ✅ (3.5) |
| Dataset (typed) | n/a | ✅ (3.5) |
| Catalog | ✅ | ✅ (3.5) |
| KeyValueGroupedDataset | n/a | ✅ (3.5) |
| Streaming (DataStreamReader/Writer/Query/Listener) | partial | ✅ majority (3.5) |
| UDFs | ✅ | ✅ in shell; standalone needs `ClassFinder` |
| **RDD** | ❌ | ❌ |
| **SparkContext** | ❌ | ❌ |

PySpark API reference labels supported APIs with **"Supports Spark Connect"** — always your authoritative check.

### Migration cost from classic PySpark
Only the **SparkSession creation line** changes. Everything DataFrame-based stays identical. Code using **`RDD` or `SparkContext` will not work** over Connect.

### Auth
- **No built-in auth.** Always front the server with an HTTP/2 proxy (TLS termination + token validation).
- Optional `;token=` URL parameter is **only metadata** — Spark Connect itself doesn't validate it.

### Session class introspection (Python)
- Classic: `pyspark.sql.session.SparkSession`
- **Connect: `pyspark.sql.connect.session.SparkSession`**

---

## Exam Sec 6 — both objectives

1. **"Describe the features of Spark Connect"** → decoupled client/server + protocol stack (unresolved plans / protobuf / gRPC / Arrow) + the 4 benefits + supported APIs.
2. **"Describe the different deployment mode types (Client, Cluster, Local)"** → this is the **classic Spark deployment-modes question** (Local / Standalone / YARN client / YARN cluster / Kubernetes), covered in the **`apache-spark` skill, Ch 1**. Spark Connect is **orthogonal** to deployment modes: the Connect server itself runs in any deployment mode; from the client's perspective you just point `sc://...` at it.

---

## ⚠ Post-3.5 features — DO NOT memorize for the 3.5 exam

The book + 4.x docs surface these; treat as informational only:

- **`spark.api.mode=connect`** (Spark 4.0+) — config that routes classic `spark-submit` through Connect.
- **`spark.remote=local[*]`** (Spark 4.0+) — local-cluster shortcut for testing.
- **Go / Rust / Swift official clients** (Spark 4.0+) — live in `apache/spark-connect-go`, etc.
- **Spark Connect as default execution mode** (Spark 4.0+).

If a question mentions any of these, it's testing **Spark 4.x**, not 3.5. The current Databricks Associate exam (Oct 2025 guide) does not version-stamp on 3.5 explicitly but the syllabus aligns with 3.4–3.5 features.

---

## Chapter Index

| # | Title | Focus |
|---|---|---|
| [ch01](chapters/ch01-features-and-benefits.md) | Features & Benefits | The "what" and "why"; 4 benefits; in-scope vs out-of-scope features |
| [ch02](chapters/ch02-architecture-internals.md) | Architecture & Wire Protocol | gRPC, protobuf, Arrow, unresolved logical plans — 6-step request lifecycle |
| [ch03](chapters/ch03-server-setup-and-install.md) | Server Setup & Client Install | `start-connect-server.sh`, `pip install pyspark[connect]`, sbt deps |
| [ch04](chapters/ch04-client-connection-methods.md) | Client Connection (3 methods) | `SPARK_REMOTE`, `--remote`, `SparkSession.builder.remote(...)`, `sc://` URL |
| [ch05](chapters/ch05-api-support-matrix.md) | API Support Matrix | What works (DataFrame), what doesn't (RDD, SparkContext); PySpark vs Scala |

## Topic Index

- **Apache Arrow** → ch02
- **API support (what works/what doesn't)** → ch05
- **`builder.remote()`** → ch04
- **Catalog (Scala)** → ch05
- **ClassFinder / `registerClassFinder`** → ch04, ch05
- **Connection URL (`sc://`)** → ch04
- **Decoupled architecture** → ch01, ch02
- **Default port (15002)** → ch03, ch04
- **Dependencies (Python client)** → ch03
- **gRPC** → ch02
- **Migration from classic PySpark** → ch04, ch05
- **Monolithic driver (legacy)** → ch01
- **PySpark API support** → ch05
- **`pip install pyspark[connect]`** → ch03
- **Protocol Buffers** → ch02
- **RDD/SparkContext (not supported)** → ch05
- **Scala API support** → ch05
- **Session class (Python introspection)** → ch04
- **`SPARK_REMOTE` env var** → ch04
- **`sc://` URL scheme** → ch04
- **Spark Connect REPL (Scala)** → ch03, ch04
- **`spark-connect_2.12`** → ch03
- **`spark-connect-client-jvm`** → ch03
- **`spark-sql-api`** → ch03
- **`start-connect-server.sh`** → ch03
- **Streaming over Connect (Scala)** → ch05
- **Token (`;token=...` in URL)** → ch02, ch04
- **UDFs over Connect** → ch04, ch05
- **Unresolved logical plan** → ch02

## Supporting Files

- [glossary.md](glossary.md) — alphabetical terms with chapter pointers + post-3.5 entries clearly flagged
- [patterns.md](patterns.md) — concrete techniques (start server, migrate script, auth via proxy, Scala UDF artifact upload)
- [cheatsheet.md](cheatsheet.md) — single-page exam reference: URL format, 3 connection methods, API matrix, post-3.5 traps

## Sources used to build this skill

Spark 3.5 official (primary):
- https://spark.apache.org/docs/3.5.7/spark-connect-overview.html
- https://spark.apache.org/docs/3.5.6/api/python/getting_started/install.html

Databricks engineering blog (context):
- https://www.databricks.com/blog/2022/07/07/introducing-spark-connect-the-power-of-apache-spark-everywhere.html (motivations)
- https://www.databricks.com/blog/2023/04/18/spark-connect-available-apache-spark.html (3.4 GA facts)

Spark 4.1 docs (used ONLY for client-setup code patterns; everything 4.x-specific is flagged ⚠️):
- https://spark.apache.org/docs/latest/app-dev-spark-connect.html

> To regenerate local snapshots: `curl -sSL <url> -o source.html` (or use WebFetch with extraction prompts) for each URL above.

---

## Scope & Limits

This skill is calibrated for the **Databricks Certified Associate Developer for Apache Spark exam, Sec 6 (Spark Connect)**, anchored to **Spark 3.4–3.5**. For Spark 4.x features (multi-language clients, `spark.api.mode=connect`, etc.), see the latest Apache Spark docs — but don't expect them on the current exam form.
