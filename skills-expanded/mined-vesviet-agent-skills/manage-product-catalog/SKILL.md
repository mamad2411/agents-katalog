---
name: manage-product-catalog
description: Build or maintain a product catalog including product creation, variant management (size, color, SKU), pricing, and inventory synchronization across channels. Use when adding, updating, or structuring product data in an e-commerce system.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, fetch]
---

# Manage Product Catalog

Use this skill when the task involves designing the data model or implementing the CRUD operations for products, product variants, categories, pricing, and stock levels in an e-commerce context.

## When to Use

- adding or updating product data
- variant management (size, color, SKU)
- pricing or inventory sync across channels
- structuring catalog data
- **semantic vector search layer (pgvector/Pinecone + RRF)**
- **AI content governance pipeline (review gate + audit metadata)**
- **event-sourced inventory (Kafka/Cloudflare Queues)**
- **knowledge graph + GraphRAG (Neo4j/Neptune/TigerGraph)**
- **Vietnam seller verification (Decree 248/2026)**

## Core Rules

- every sellable unit must have a unique SKU enforced at the **database constraint level**; never allow duplicate SKUs within the same catalog
- pricing changes must be versioned or timestamped — store `price`, `compare_at_price`, `effective_from`, and `effective_until`; never silently overwrite historical prices
- inventory counts are `confidential` data; do not expose raw warehouse stock levels to unauthenticated clients
- **Two-Phase Atomic Inventory Hold**: use atomic conditional SQL (`UPDATE inventory SET available = available - X, reserved = reserved + X WHERE available >= X`) or Redis Lua scripts with a TTL; convert reserved hold to hard commit on payment success; release via background sweeper on TTL expiry or payment failure — never naive read-then-write sequences
- **Optimistic Concurrency Control (OCC)**: reject stale out-of-order inventory updates using version stamps (`version`, `ETag`, or vector clocks) to prevent overselling under concurrent channel sync
- **Channel Safety Buffers**: when syncing to external marketplaces (Shopee, Lazada, TikTok Shop, Amazon), deduct dynamic virtual safety stock buffers (e.g., 5% or minimum 3 units) before publishing available quantities — never broadcast 100% of available stock
- use **CDC event streaming** (Debezium / Kafka) to broadcast real-time stock changes to downstream channels; prefer push events over polling for inventory sync
- product data changes that affect live checkout (price, availability) must go through an approval or review step before publishing; **AI-generated product content** requires a mandatory human-review gate before status is set to published
- treat inventory counts as confidential data; never expose raw warehouse stock levels to unauthenticated clients; classify with `data-classification.yaml` (OWASP ASI03)
- every catalog write must be schema-validated against the active product schema; reject schema-drifted entries to prevent downstream agent desync (OWASP ASI04)
- when AI tools generate product descriptions, track `generated_by`, `reviewed_by`, `generated_at`, and `generation_model`; treat unreviewed AI output as drafts (OWASP ASI09)
- **Semantic Vector Search Layer (Production Standard 2026)**: generate embeddings on write/update using `text-embedding-3-large` or Cohere `embed-v4`; store in `pgvector` (PostgreSQL) or Pinecone; hybrid search via BM25 + dense vector with Reciprocal Rank Fusion (RRF)
- **AI Content Governance Pipeline (Mandatory)**: generation → brand voice validation (banned words, claim accuracy, brand guidelines) → human review gate → publish; unreviewed AI output = `draft` status (never `published`)
- **Event-Sourced Inventory**: publish all inventory adjustments/reservations to Kafka/Cloudflare Queues immediately; consumers: search indexes, fulfillment dispatchers, AI shopping agents; no DB locking — eventual consistency via event stream
- **Knowledge Graph + GraphRAG**: Neo4j/Neptune/TigerGraph for recommendations, compatibility, bundles; GraphCypherQAChain for NL → Cypher → structured results + Qdrant vectors → cited reasoning; Pydantic schema enforcement for all entities/relations/LLM outputs
- **Vietnam Decree 248/2026/ND-CP Compliance**: seller verification gate before product publish; platform obligations for service standards, pricing, promotions, complaints; accurate product information required

## Output Contracts

When the catalog change is consumed by a storefront, a marketplace sync, or a downstream analytics system, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the catalog entity shape, variant structure, inventory model, vector search endpoints, content governance review workflows, and seller verification gates.
- **`contracts/schemas/data-pipeline-spec.json`** for Kafka event-sourced inventory adjustments, CDC feeds, knowledge graph ETL, and downstream consumer contracts.
- **`contracts/schemas/deployment-plan.json`** when the catalog change is part of a coordinated multi-role rollout.
- For human-readable reports, a markdown diff of the affected SKUs and the rationale.

Skip emission for read-only catalog queries that do not cross a role boundary.

## Failure Modes

- **Duplicate SKU**: a SKU collision is created at the application layer. Mitigation: enforce SKU uniqueness at the database constraint level; reject duplicate inserts.
- **Silent price overwrite**: a price change overwrites historical prices without a version or timestamp. Mitigation: store `price`, `compare_at_price`, `effective_from`, and `effective_until`; never silently overwrite.
- **Inventory oversell under concurrency**: two channels decrement the same stock in parallel and oversell. Mitigation: use Two-Phase Atomic Inventory Hold (atomic SQL or Redis Lua) with TTL; reject naive read-then-write sequences.
- **OCC version drift**: a stale inventory update overwrites a newer one. Mitigation: enforce Optimistic Concurrency Control via `version`/`ETag`; reject stale updates.
- **Channel over-broadcast**: 100% of available stock is published to external marketplaces, allowing oversell from marketplace surges. Mitigation: apply dynamic virtual safety stock buffers (5% or minimum 3 units) before publishing.
- **AI content published unreviewed**: an AI-generated product description is set to `published` without a human review gate. Mitigation: enforce the review gate; track `reviewed_by` and `reviewed_at`; treat unreviewed AI output as drafts.
- **Inventory leaked**: raw warehouse stock levels are exposed to unauthenticated clients. Mitigation: classify inventory as confidential; expose `is_in_stock` (a computed boolean) rather than raw counts.
- **Sync duplicate**: an idempotent upsert is missing, causing duplicates on re-run. Mitigation: implement upsert by SKU; log sync run counts (created, updated, failed).
- **Vector search hallucination**: semantic search returns irrelevant products. Mitigation: RRF fusion with BM25, relevance threshold tuning, human-in-the-loop evaluation.
- **AI content brand violation**: AI generates off-brand or inaccurate claims. Mitigation: automated pre-review validation, banned words list, claim accuracy checks.
- **Inventory event loss**: Kafka message lost, search index stale. Mitigation: idempotent consumers, event replay capability, CDC backup (Debezium).
- **Knowledge graph entity resolution error**: wrong product relationships. Mitigation: validated against labels, human review of graph changes, Pydantic schema enforcement.
- **GraphRAG citation failure**: LLM generates uncited recommendations. Mitigation: GraphCypherQAChain with mandatory citation, structured output validation.
- **Vietnam compliance gap**: unverified seller lists products. Mitigation: verification gate in publish workflow, platform audit trail.
- **Schema drift**: catalog write with new/changed fields breaks downstream. Mitigation: Pydantic validation in CI, schema registry, contract testing.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a catalog update may try to reframe a product's category or compliance status. Cross-check the update against the source-of-truth catalog; reject off-spec edits.
- **ASI03 Identity & Privilege Abuse**: inventory counts and pricing are confidential; never expose raw values to unauthenticated clients; expose computed booleans only.
- **ASI04 Supply Chain**: the catalog schema and any external marketplace connector must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI07 Inter-Agent Communication**: the catalog contract is consumed by storefront, marketplace, and analytics agents; emit a structured spec so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present AI-generated product copy as "ready to publish" without a human review gate; surface the AI provenance and the reviewer.

## Suggested Process

### 1. Define the Product Data Model

Clarify before building:

- what are the product types (simple, configurable/variant, bundle, digital)?
- which attributes are shared across variants (description, images) vs variant-specific (price, SKU, weight, stock)?
- what category taxonomy structure is required (flat list, nested tree)?
- what pricing model applies (fixed, tiered, time-limited sale)?

### 2. Implement Product and Variant Structure

- create a `Product` entity with shared fields: name, description, slug, images, category, status
- create a `ProductVariant` entity with: SKU, price, compare-at price, weight, stock quantity, and attribute options (e.g., `size: M`, `color: blue`)
- enforce uniqueness constraint on SKU at the database level
- generate URL-friendly slugs from product names; ensure uniqueness

### 3. Implement Inventory Management

- store `quantity_on_hand` per variant — never per product
- implement `reserve_stock(variant_id, qty)` and `release_stock(variant_id, qty)` as atomic transactions
- expose `is_in_stock` as a computed property: `quantity_on_hand - reserved_quantity > 0`
- implement a low-stock threshold alert mechanism for operations teams

### 4. Implement Pricing and Promotions Support

- store `price` and `compare_at_price` (strike-through) separately to support sale display
- support scheduled price changes with `effective_from` and `effective_until` timestamps
- never compute price purely on the client side; always resolve from the server

### 5. Implement Multi-channel Sync (when applicable)

- if syncing from an external source (POS, ERP, supplier feed), treat the external system as source of truth
- implement idempotent upsert by SKU to safely re-run sync without duplicating products
- log sync runs with counts of created, updated, and failed records

## 2026 Catalog Architecture Patterns

### Semantic Vector Search Layer (Production Standard)
- **Embeddings**: `text-embedding-3-large` or Cohere `embed-v4` on write/update
- **Storage**: `pgvector` (PostgreSQL) or Pinecone
- **Hybrid Fusion**: BM25 + dense vector via Reciprocal Rank Fusion (RRF)

### AI Content Governance Pipeline (Mandatory)
- **Review Gate**: Human review REQUIRED before `published` status
- **Audit Metadata**: `generated_by`, `reviewed_by`, `generated_at`, `generation_model`
- **Brand Voice Validation**: Automated banned words, claim accuracy, brand guidelines checks
- **Draft Status**: Unreviewed AI output = `draft` (never `published`)

### Event-Sourced Inventory
- **Publish Mutations**: Inventory adjustments/reservations → Kafka/Cloudflare Queues immediately
- **Consumers**: Search indexes, fulfillment dispatchers, AI shopping agents
- **No DB Locking**: Eventual consistency via event stream
- **CDC Alternative**: Debezium for database → Kafka

### Knowledge Graph + GraphRAG
- **Graph DBs**: Neo4j, Neptune, TigerGraph, Memgraph for recommendations, compatibility, bundles
- **GraphRAG Pattern**: Structured subgraphs → LLM chains for grounded recommendations
- **Entity Resolution**: Validated against labels, CDC from Salesforce/Jira/GitHub/ServiceNow/SQL via Kafka/Airbyte
- **Pydantic Schema Enforcement**: All entities/relations/LLM outputs validated — drift fails in CI
- **Cited Reasoning**: GraphCypherQAChain for NL → Cypher → structured results + Qdrant vectors → cited output

### Vietnam Seller Verification (Decree 248/2026)
- Seller verification gate before product publish (effective July 1, 2026)
- Platform obligations: service standards, pricing, promotions, complaints
- Electronic ID verification for sellers/livestreamers from Jan 1, 2027

## Checklist

- [ ] SKU uniqueness enforced at database level
- [ ] variant-level inventory tracked separately from product level
- [ ] stock decrement operations are atomic (transaction-safe)
- [ ] pricing stored with version or effective timestamp
- [ ] `is_in_stock` computed server-side, not client-side
- [ ] product publish/unpublish guarded by review or approval step
- [ ] catalog sync is idempotent by SKU if external source is used
- [ ] low-stock alerting threshold configured for ops team
- [ ] **semantic vector embeddings generated on product write/update** (`text-embedding-3-large` or Cohere `embed-v4`)
- [ ] **vector embeddings stored in pgvector or Pinecone** with proper indexing
- [ ] **hybrid search: BM25 + dense vector combined via Reciprocal Rank Fusion (RRF)**
- [ ] **AI-generated product content: mandatory human review gate before `published` status**
- [ ] **AI content audit metadata: `generated_by`, `reviewed_by`, `generated_at`, `generation_model` tracked**
- [ ] **brand voice validation: automated banned words, claim accuracy, brand guidelines checks**
- [ ] **unreviewed AI output status = `draft` (never `published`)**
- [ ] **inventory adjustments published to Kafka/Cloudflare Queues immediately**
- [ ] **downstream consumers: search indexes, fulfillment, AI agents consume inventory events**
- [ ] **product knowledge graph in Neo4j/Neptune/TigerGraph for relationships**
- [ ] **GraphRAG retrieval: structured subgraphs → LLM chains for grounded recommendations**
- [ ] **entity resolution with CDC from Salesforce/Jira/GitHub/ServiceNow/SQL via Kafka/Airbyte**
- [ ] **Pydantic models for all entity types, relations, LLM outputs — schema drift fails in CI**
- [ ] **LangChain GraphCypherQAChain for NL → Cypher → cited reasoning**
- [ ] **Vietnam seller verification gate before product publish**
- [ ] **platform obligations: service standards, pricing, promotions disclosed**
- [ ] channel safety buffers: dynamic virtual safety stock (5% or min 3 units) before marketplace publish
- [ ] CDC event streaming (Debezium) for real-time stock changes to downstream channels

## Related Skills

- **handle-checkout-flow**: Consumes product and stock data during checkout
- **manage-order-fulfillment**: Decrements inventory when an order ships
- **build-data-pipeline**: Synchronize product data from ERP, supplier feeds, or PIM systems
- **add-api-endpoint**: Expose catalog CRUD endpoints for admin and storefront consumers
- **database-maintenance**: Maintain catalog indexes and handle bulk data operations
- Companion reference: `references/semantic-vector-catalog-and-graphrag.md`
- Companion example: `examples/hybrid-search-and-governance-pipeline.ts`

Last updated: 2026-11-08