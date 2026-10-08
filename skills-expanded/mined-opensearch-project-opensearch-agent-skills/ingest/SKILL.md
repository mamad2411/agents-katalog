---
name: ingest
description: >
  Process unstructured documents into search-ready chunks. Use this skill when the
  user wants to process PDFs or unstructured documents into JSONL chunks using Docling.
  Activate even if the user says document processing, chunking, Docling, PDF processing,
  or chunk quality evaluation. For cloud-scale ingestion via OSIS pipelines, see
  cloud/managed-ingestion-service.
compatibility: Requires uv.
metadata:
  author: opensearch-project
  version: "1.0"
---

# Ingest

Category skill for local document processing — turning unstructured files into search-ready JSONL chunks.

## Skills

| Skill | Description |
|---|---|
| [document-processing](document-processing/SKILL.md) | Process PDF/DOCX/PPTX into JSONL chunks via Docling (local, no AWS needed) |

## Not Covered

This skill covers **local document processing** only (PDF/DOCX → JSONL chunks).
It does NOT cover:
- Cloud-scale ingestion via OSIS pipelines → see [managed-ingestion-service](../cloud/managed-ingestion-service/SKILL.md)
- Structured bulk-indexing (`_bulk` API)
- OpenSearch `_ingest` processor pipelines (grok, date, set, script)
- Log/metric shipping (Fluent Bit, Data Prepper, Logstash)

## When to Use

Read [document-processing/SKILL.md](document-processing/SKILL.md) when:
- User has PDFs/documents and needs JSONL chunks
- User wants to evaluate chunk quality before ingestion
- User mentions Docling, document processing, chunking

For cloud ingestion (JSONL → OSIS → OpenSearch index), see
[cloud/managed-ingestion-service](../cloud/managed-ingestion-service/SKILL.md).
