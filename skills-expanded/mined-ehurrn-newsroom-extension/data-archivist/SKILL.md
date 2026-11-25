---
name: data-archivist
description: "Transform raw OSINT into queryable databases. Ingest PDFs, CSVs, scraped records, and court filings into structured schemas (BigQuery, PostgreSQL, SQLite). Reproducible queries, not ad-hoc summaries. Chain of custody for evidence."
---

# Data Archivist Skill

## Overview

The Data Archivist transforms raw OSINT (PDFs, CSVs, scraped web records, court filings, FOIA dumps) into **queryable, reproducible databases** that serve as the foundation for investigative analysis.

This is NOT data analysis (that's downstream). This IS:

- **Ingestion standardization:** Converting diverse formats (PDF tables, hand-typed CSVs, HTML scrapes, XML feeds) into uniform schema
- **Schema design:** Star schema patterns for investigative queries (facts, dimensions, timelines)
- **Data provenance tracking:** Chain of custody for evidence (where did it come from? when? how was it extracted? by whom?)
- **Reproducible queries:** Saved SQL patterns, not ad-hoc summaries
- **Resource optimization:** Free tier awareness (BigQuery free tier limits, PostgreSQL disk constraints, SQLite for local-first)

**Binding protocol:** This desk operates under `skills/investigative-journalist/evidence-preservation-protocol.md`. Originals in the write-once `evidence/` directory are never modified — all transformation outputs (OCR text, cleaned CSVs, database loads) are derived copies in `working/` that cite their source `DOC-` ID and hash. Every ingest, transform, and export is an entry in the master file's append-only `collection_log[]`. Nothing is deleted while `legal_hold` is true (the default).

---

## Data Ingestion Standardization

### Supported Input Formats

| Format | Typical Source | Challenges | Standardization Approach |
|---|---|---|---|
| **PDF (tabular)** | Government reports, court filings, financial statements | Text extraction loses formatting; columns mis-aligned | OCR + manual table mapping; extract to CSV; validate row counts |
| **PDF (unstructured)** | News articles, regulations, correspondence | OCR errors; no structured fields | Extract text; keyword search for extraction; manual review |
| **CSV** | FOIA dumps, export from legacy systems, aggregated data | Missing headers; inconsistent delimiters; encoding issues (UTF-8 vs. Latin-1) | Validate headers; detect delimiter; convert encoding; document source URL |
| **XLS/XLSX** | Spreadsheets, financial records, surveys | Multiple sheets; merged cells; formulas (not values) | Extract all sheets separately; flatten merged cells; export formulas as values |
| **JSON** | API exports, web scrapes (JavaScript-heavy sites), config files | Nested structures; missing fields; null vs. empty string inconsistency | Flatten nested JSON; standardize nulls; document schema version |
| **HTML Tables** | Scraped web pages, cached legislative records | Cells span multiple columns/rows; colspan/rowspan confusion | Parse colspan/rowspan; extract as CSV; validate row integrity |
| **XML/RSS** | News feeds, structured government data, legal databases | Namespace confusion; CDATA sections; encoding issues | Strip namespaces; unescape CDATA; standardize date formats |
| **SQL Dumps** | Database exports from legacy systems, web platform backups | Encoding issues; proprietary SQL syntax; no schema documentation | Parse generic SQL (CREATE TABLE, INSERT); document assumed data types |

### Standardization Workflow

**Phase 1: Source Documentation (required before ingestion)**

For every data source collected, you must immediately register its provenance parameters, download metadata, custody events, and SHA-256 hashes directly into the `evidence` array and append-only `collection_log[]` inside `master-file.json`. Do not write standalone or detached YAML files outside the central schema ecosystem.

---

## Platform-Agnostic Schema Design

### The Investigative Star Schema

Most investigative databases follow a **star schema** pattern:

```
                    ┌─────────────┐
                    │   TIMELINE  │
                    │  (dim_date) │
                    └─────────────┘
                           ▲
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
┌─────────┐          ┌──────────┐          ┌──────────┐
│ PEOPLE  │          │ FACTS    │          │ ENTITIES │
│(dim_    │          │(fact_    │          │(dim_     │
│people)  │──────────│events)   │──────────│entities) │
└─────────┘          └──────────┘          └──────────┘
     │                     │                     │
     └─────────────────────┼─────────────────────┘
                           │
                    ┌─────────────┐
                    │  DOCUMENTS  │
                    │  (dim_docs) │
                    └─────────────┘
```

### Table Definitions

**Fact Table: fact_events (central)**

```
CREATE TABLE fact_events (
  event_id          BIGINT PRIMARY KEY,
  person_id         BIGINT REFERENCES dim_people(person_id),
  entity_id         BIGINT REFERENCES dim_entities(entity_id),
  document_id       BIGINT REFERENCES dim_documents(document_id),
  event_date        DATE,
  event_type        VARCHAR(50),  -- "meeting", "payment", "filing", "communication"
  amount_usd        DECIMAL(14,2),
  description       TEXT,
  source_url        VARCHAR(2048),
  source_page       INT,
  confidence_level  VARCHAR(20),  -- Aligns with Admiralty alphanumeric keys (e.g., 'A1', 'B2') from evidence-grading.md
  FOREIGN KEY (person_id) REFERENCES dim_people(person_id),
  FOREIGN KEY (entity_id) REFERENCES dim_entities(entity_id),
  FOREIGN KEY (document_id) REFERENCES dim_documents(document_id),
  FOREIGN KEY (event_date) REFERENCES dim_date(date_key)
);
```

**Dimension Table: dim_people**

```
CREATE TABLE dim_people (
  person_id       BIGINT PRIMARY KEY,
  full_name       VARCHAR(255) NOT NULL,
  last_name       VARCHAR(100),
  first_name      VARCHAR(100),
  aliases         TEXT,  -- JSON array of known aliases
  titles          TEXT,  -- JSON array: "Mayor", "CEO", etc.
  birth_date      DATE,
  dob_confidence  VARCHAR(20),  -- "confirmed", "estimated", "unknown"
  gender          VARCHAR(20),
  address         VARCHAR(255),
  phone           VARCHAR(20),
  email           VARCHAR(255),
  linkedin_url    VARCHAR(255),
  notes           TEXT,
  source_urls     TEXT,  -- JSON array of URLs where info confirmed
  created_date    TIMESTAMP,
  updated_date    TIMESTAMP
);
```

**Dimension Table: dim_entities**

```
CREATE TABLE dim_entities (
  entity_id           BIGINT PRIMARY KEY,
  entity_name         VARCHAR(255) NOT NULL,
  entity_type         VARCHAR(50),  -- "LLC", "Corporation", "Government Agency", "Non-profit"
  formed_date         DATE,
  dissolved_date      DATE,
  jurisdiction        VARCHAR(100),  -- "Delaware", "New York", etc.
  address             VARCHAR(255),
  registered_agent    VARCHAR(255),
  ucc_number          VARCHAR(50),
  tax_id              VARCHAR(50),
  notes               TEXT,
  source_urls         TEXT,  -- JSON array
  created_date        TIMESTAMP,
  updated_date        TIMESTAMP
);
```

**Dimension Table: dim_documents**

```
CREATE TABLE dim_documents (
  document_id     BIGINT PRIMARY KEY,
  title           VARCHAR(255),
  document_type   VARCHAR(50),  -- "PDF", "CSV", "Court Filing", "Article"
  source_url      VARCHAR(2048),
  date_accessed   DATE,
  date_published  DATE,
  hash_md5        VARCHAR(32),  -- For version control
  file_path       VARCHAR(500),  -- Local archive path
  page_count      INT,
  ocr_confidence  DECIMAL(3,2),  -- 0.0–1.0 for OCR documents
  notes           TEXT,
  created_date    TIMESTAMP,
  updated_date    TIMESTAMP
);
```

**Dimension Table: dim_date**

```
CREATE TABLE dim_date (
  date_key        DATE PRIMARY KEY,
  year            INT,
  quarter         INT,
  month           INT,
  day             INT,
  week            INT,
  day_of_week     VARCHAR(10),
  is_weekend      BOOLEAN,
  day_name        VARCHAR(10)
);
```

---

## Reproducible Query Generation

### Query Library (not ad-hoc analysis)

Every common question gets a **saved, documented SQL pattern**:

**Query 1: "Show all payments from Person X to Entity Y"**

```sql
-- query_id: q001
-- purpose: Trace financial relationships between individuals and entities
-- created: 2025-03-15
-- author: alice@newsroom.org

SELECT
  fe.event_date,
  fe.amount_usd,
  fe.description,
  doc.title AS source_document,
  CONCAT(
    'https://source-archive.newsroom.org/',
    doc.file_path
  ) AS primary_source
FROM fact_events fe
LEFT JOIN dim_documents doc ON fe.document_id = doc.document_id
WHERE
  fe.person_id = ?  -- parameter: person_id
  AND fe.entity_id = ?  -- parameter: entity_id
  AND fe.event_type = 'payment'
ORDER BY fe.event_date DESC;
```

**Query 2: "Timeline of Person X's roles/titles"**

```sql
-- query_id: q002
-- purpose: Establish professional/political timeline
-- created: 2025-03-15
-- author: alice@newsroom.org

SELECT
  dd.date_key AS event_date,
  fe.event_type,
  fe.description,
  COALESCE(dp.titles, 'N/A') AS titles_at_time,
  doc.title AS source,
  doc.source_url
FROM fact_events fe
LEFT JOIN dim_date dd ON fe.event_date = dd.date_key
LEFT JOIN dim_people dp ON fe.person_id = dp.person_id
LEFT JOIN dim_documents doc ON fe.document_id = doc.document_id
WHERE fe.person_id = ?
ORDER BY fe.event_date ASC;
```

**Query 3: "Web of connections: Entity X connected to Persons A–Z"**

```sql
-- query_id: q003
-- purpose: Network analysis; identify co-conspirators or related parties
-- created: 2025-03-15
-- author: alice@newsroom.org

WITH entity_connections AS (
  SELECT
    fe.entity_id,
    fe.person_id,
    COUNT(*) AS event_count,
    MIN(fe.event_date) AS first_event,
    MAX(fe.event_date) AS last_event,
    SUM(fe.amount_usd) AS total_usd
  FROM fact_events fe
  GROUP BY fe.entity_id, fe.person_id
)
SELECT
  de.entity_name,
  dp.full_name,
  ec.event_count,
  ec.first_event,
  ec.last_event,
  ec.total_usd
FROM entity_connections ec
LEFT JOIN dim_entities de ON ec.entity_id = de.entity_id
LEFT JOIN dim_people dp ON ec.person_id = dp.person_id
WHERE ec.entity_id = ?
ORDER BY ec.total_usd DESC;
```

### Query Library Maintenance

Store all queries in a version-controlled file (`queries.sql` or directory):

```yaml
queries:
  q001:
    name: "Payments between person and entity"
    file: "queries/q001_payments_person_entity.sql"
    parameters: [person_id, entity_id]
    outputs: [event_date, amount_usd, description, source_document]

  q002:
    name: "Timeline of person's roles"
    file: "queries/q002_timeline_person_roles.sql"
    parameters: [person_id]
    outputs: [event_date, event_type, description, titles, source]

  q003:
    name: "Entity's connections to persons"
    file: "queries/q003_entity_connections.sql"
    parameters: [entity_id]
    outputs: [entity_name, full_name, event_count, first_event, last_event, total_usd]
```

---

## Data Provenance & Chain of Custody

### Evidence Tracking for Legal Defense

Every row in `fact_events` must be traceable to its source. This protects the newsroom if a claim is challenged:

| Field | Purpose | Example |
|---|---|---|
| `document_id` | Foreign key to source document | 847 (links to court filing PDF) |
| `source_url` | URL where data came from | https://courts.state.gov/filings/case-2024-001234 |
| `source_page` | Page number (if PDF or scanned) | 5 |
| `confidence_level` | Aligns with Admiralty scale keys | "A1", "B2", "C3" |

**Chain of Custody Log (required for sensitive claims):**

```yaml
claim: "ABC Corp paid $50,000 to Mayor Jane Smith"
evidence:
  - step: 1
    date: "2025-03-10"
    action: "Downloaded campaign finance disclosure (Form XYZ) from state website"
    url: "https://elections.state.gov/disclosures/2024/mayor-smith-jane.pdf"
    by: "alice@newsroom.org"
    hash_md5: "abc123def456..."

  - step: 2
    date: "2025-03-10"
    action: "OCR extraction of page 3, table 'Contributions Over $1,000'"
    ocr_tool: "AWS Textract"
    ocr_confidence: 0.98
    result: "Extracted row: date=2024-06-15, contributor=ABC Corp (LLC), amount=$50,000"
    by: "archive@newsroom.org"

  - step: 3
    date: "2025-03-10"
    action: "Manual verification: cross-referenced against ABC Corp registered agent in Secretary of State database"
    verified: true
    by: "alice@newsroom.org"

  - step: 4
    date: "2025-03-15"
    action: "Added to database table: fact_events, event_id=9847"
    database: "newsroom_investigations"
    document_id: 512
    by: "archive@newsroom.org"

  - step: 5
    date: "2025-04-01"
    action: "Publication in article 'Mayor Smith's Undisclosed Corporate Donations'"
    article_url: "https://newsroom.org/articles/2025-04-01-mayor-smith-donations.html"
    by: "alice@newsroom.org"
```

If a legal challenge arises: **every step from source to publication is documented and repeatable.**

---

## Platform Selection & Implementation

### BigQuery (GCP)

**Best for:** Large datasets (>1M rows), frequent queries, collaborative analysis, free tier (1 TB/month query)

**Pros:**
- Handles investigative star schemas elegantly
- SQL pricing: pay for bytes scanned, not compute
- Built-in ML (anomaly detection for suspicious patterns)
- Shareable query results; audit log for FOIA

**Cons:**
- Needs GCP account; learning curve
- Costs accumulate if queries are inefficient
- Data stored in cloud (privacy considerations)

**Setup:**
```bash
# Install gcloud CLI
gcloud auth login
gcloud config set project my-newsroom-project

# Create dataset
bq mk newsroom_investigations

# Load CSV
bq load \
  newsroom_investigations.fact_events \
  data/fact_events.csv \
  --autodetect \
  --source_format=CSV

# Run saved query
bq query --use_legacy_sql=false < queries/q001_payments_person_entity.sql
```

### PostgreSQL (Self-Hosted)

**Best for:** Medium datasets (10K–100M rows), local-first, full control, no cloud dependencies

**Pros:**
- Free and open-source
- Full-text search, JSON support, advanced indexing
- Data stays on your server (better privacy)
- Complex queries (CTEs, window functions) well-supported

**Cons:**
- Requires database admin; backup responsibilities
- Performance depends on hardware
- Requires VPN/SSH for remote access

**Setup:**
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
createdb newsroom_investigations

# Connect
psql newsroom_investigations

# Run schema from schema.sql
\i schema.sql

# Load data
\COPY fact_events FROM 'data/fact_events.csv' CSV HEADER;
```

### SQLite (Local, Zero Infrastructure)

**Best for:** Smaller datasets (<10M rows), single reporter, no server dependencies, prototyping

**Pros:**
- Single file; no setup required
- Perfect for local version control (commit .db to git)
- Queryable via CLI, Python, web interface
- Zero cost, zero admin

**Cons:**
- Doesn't scale to enterprise size
- No remote access; file-based (disk I/O bottleneck)
- Concurrent writes limited

**Setup:**
```bash
# Create database
sqlite3 newsroom_investigations.db < schema.sql

# Load data
sqlite3 newsroom_investigations.db
> .mode csv
> .import data/fact_events.csv fact_events

# Query
sqlite3 newsroom_investigations.db "SELECT * FROM fact_events LIMIT 10;"
```

---

## Resource Constraint Awareness

### Free Tier Limits (as of 2025)

| Platform | Monthly Free Allowance | Hard Stop | Overflow Cost |
|---|---|---|---|
| **BigQuery** | 1 TB query scan, 10 GB storage | Yes, at 1 TB | $6.25 per TB scanned |
| **PostgreSQL (RDS)** | None; pay-as-you-go starting at ~$10/month | No; scales with usage | Varies by instance size |
| **SQLite** | Unlimited; single file on disk | Limited by disk space | None (self-hosted) |

**Recommendation for startups/small newsrooms:**

1. **Prototype with SQLite** (zero cost, instant setup)
2. **Scale to PostgreSQL** when dataset >5M rows or multiple reporters
3. **Migrate to BigQuery** only if you need shared access + no infrastructure burden

---

## Common Mistakes & Red Flags

### Ingestion Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| **No source manifest** | Can't verify data origin; chain of custody broken | Create source-manifest.yaml for EVERY source before ingestion |
| **CSV uploaded directly without validation** | Missing headers; encoding issues; silent data loss | Run validation script: check row count, detect delimiter, test encoding |
| **PDF table extracted as text (no structure)** | Can't query; numbers stuck in paragraphs | Use OCR + table detection (AWS Textract, Google Vision); extract to structured CSV |
| **Null values mixed: NULL, "N/A", empty string, "unknown"** | Queries fail; counts off | Standardize: NULL for missing, "unknown" for intentional non-disclosure |
| **Duplicate rows (same fact ingested twice)** | Inflated counts; double-counted payments | Add UNIQUE constraints to database; run deduplication check post-ingestion |
| **No hash verification** | Can't detect if data was corrupted in transit | Generate MD5 hash of source file; store in source_manifest; re-verify post-upload |

### Schema Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| **No date_key in fact table** | Can't join with dim_date; temporal analysis impossible | Always include event_date in fact table; join to dim_date for calendar calculations |
| **Foreign keys not enforced** | Orphaned rows; referential integrity breaks | Add FOREIGN KEY constraints; PostgreSQL/BigQuery will prevent invalid inserts |
| **Mixing of data types (amount_usd as VARCHAR)** | Sorting/summing fails; string "100" != numeric 100 | Use DECIMAL/NUMERIC for amounts; DATE for dates; INT for IDs |
| **No confidence_level field** | Can't distinguish primary source from inferred | Add confidence_level to every fact; use during analysis ("primary_source" only) |
| **Overly wide tables (100+ columns)** | Slow queries; hard to maintain; unclear what fields mean | Break into normalized tables; use lookups (dim_people, dim_entities) |

### Query Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| **Ad-hoc queries; no saved pattern** | Analysis not repeatable; other reporters can't replicate | Document every query pattern; save to version control; name logically (q001, q002...) |
| **Hardcoded IDs ("WHERE person_id = 123")** | Not portable; brittle; other reporters can't use | Use parameters ("WHERE person_id = ?") or variables |
| **No LIMIT on exploratory queries** | Scans entire table; costs skyrocket on BigQuery | Always test with LIMIT 100 first; understand row count before full scans |
| **LEFT JOIN without clarifying missing data** | Includes null rows; double-counted facts | Use INNER JOIN for core facts; LEFT JOIN only when absence is meaningful |
| **No ORDER BY** | Results appear random; hard to verify accuracy | Always ORDER BY primary key or date; makes results deterministic |

### Provenance Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| **No source_url in fact_events** | If claim is challenged, can't show original source | Every row must link to document_id, which links to source_url |
| **"OCR'ed from PDF" with no confidence score** | Can't distinguish high-confidence vs. low-confidence extractions | Include ocr_confidence (0.0–1.0) and flag low-confidence rows for manual review |
| **Deleting intermediate work (raw PDFs, extraction scripts)** | Archive destroyed; chain of custody lost | Never delete raw data or extraction scripts; version control all SQL schemas |
| **No date_accessed or date_published** | Can't determine if data is stale or superseded | Every source_manifest must include date_accessed, date_published, and publication date |

---

## Checklist for Publication

Before publishing claims based on archived data:

- [ ] **Source manifest complete** for every data source (URL, date accessed, schema documented)
- [ ] **Chain of custody log** created (if high-stakes claim)
- [ ] **Data validation** passed: row count matches source, encoding correct, no silent truncation
- [ ] **Foreign key constraints** enforced; no orphaned rows
- [ ] **Confidence levels** assigned using Admiralty scale alphanumeric keys (e.g., A1, B2); only single A1/A2 or corroborated sources can back definitive claims
- [ ] **Queries saved** and documented (not ad-hoc)
- [ ] **Query results repeatable** (others can run same query, get same results)
- [ ] **Hash verification** done (MD5 of source files stored and re-verified)
- [ ] **No hardcoded IDs** in production queries (use parameters)
- [ ] **Null handling** standardized (NULL vs. "unknown")
- [ ] **All intermediate work** archived (raw CSVs, extraction scripts, OCR output)

---

## Example: Full Workflow

**Scenario:** Investigative reporter discovers that municipal contract awards are going disproportionately to one vendor. Wants to prove it with data.

**Step 1: Source Collection**
- Download municipal contracts CSV from city procurement website
- Scrape vendor bids from city council meeting minutes (HTML)
- Extract vendor payment records from annual audit (PDF table)

**Step 2: Source Documentation**
Create `source-manifest.yaml` for each:
```yaml
source:
  name: "Municipal Contracts 2020–2024"
  url: "https://procurement.city.gov/contracts/export"
  date_accessed: "2025-03-15"
  ...
```

**Step 3: Ingestion**
- Validate CSV: check headers, detect delimiter, verify encoding
- Scrape HTML → parse tables → export to CSV
- OCR PDF → extract table → validate against audit report

**Step 4: Load into Database**
- Create dim_entities (vendors), dim_people (decision-makers), fact_events (contracts)
- Load cleaned CSVs
- Run integrity checks: no orphaned rows, all amount_usd are numeric

**Step 5: Query & Analyze**
```sql
-- Which vendor got the most contracts?
SELECT
  de.entity_name,
  COUNT(*) AS contract_count,
  SUM(fe.amount_usd) AS total_awarded
FROM fact_events fe
LEFT JOIN dim_entities de ON fe.entity_id = de.entity_id
WHERE fe.event_type = 'contract_award'
  AND YEAR(fe.event_date) BETWEEN 2020 AND 2024
GROUP BY de.entity_name
ORDER BY total_awarded DESC;
```

**Step 6: Document Findings**
- Save query as `q_contracts_by_vendor.sql`
- Link results to source documents
- Create chain of custody log

**Step 7: Publish**
- Editor verifies using saved queries (reproducible)
- Archive all intermediate work
- Article published with links to data sources

---

## Tools & Resources

| Tool | Purpose | Cost | Learning Curve |
|---|---|---|---|
| **BigQuery** | Cloud data warehouse; scalable analysis | Free tier: 1 TB/month query | Medium |
| **PostgreSQL** | Self-hosted relational DB; full-featured | Free | Medium–High |
| **SQLite** | Lightweight local DB; no setup | Free | Low |
| **AWS Textract** | PDF/image OCR; table extraction | ~$1.50 per page | Low–Medium |
| **Google Sheets** | Quick CSV import, pivot tables, sharing | Free; 5M cells limit | Very Low |
| **DuckDB** | In-process SQL; analyze CSVs directly | Free | Low |
| **Apache Airflow** | Automated data pipeline scheduling | Free (self-hosted) | High |

---

## Escalation

If during ingestion you discover **conflicting data** (same entity listed twice with different details):

1. Document both versions with sources
2. Flag for editorial review
3. Do NOT arbitrate; let editor decide which version to use
4. Update confidence_level accordingly ("confirmed" vs. "disputed")
