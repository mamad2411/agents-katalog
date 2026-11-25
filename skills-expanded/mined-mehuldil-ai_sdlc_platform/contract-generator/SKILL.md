---
name: contract-generator
description: Generate OpenAPI, DB schema, and message schema contracts from design specifications
model: sonnet-4-6
token_budget: {input: 4000, output: 3000}
---

# Contract Generator Skill

Generate contracts (OpenAPI, DB schema, message schemas) from architecture and design specs.

## Contracts Generated

### OpenAPI 3.0 Specification
- Base path and server configuration
- Endpoint definitions with full request/response schemas
- Status codes and error responses
- Authentication and security definitions
- Request examples and response examples

### Database Schema
- Entity definitions with columns and constraints
- Foreign key relationships
- Index strategy
- Sequence/auto-increment configuration
- Migration SQL scripts

### Message Schema (Kafka)
- Topic definitions
- Message format (Avro, JSON Schema)
- Partition strategy
- Retention policy
- Dead Letter Queue configuration

## Triggers

Use this skill when:
- Architect provides system design
- Need API contract before implementation
- DB design complete and ready for scripts
- Event/message structure defined

## Inputs

- Architecture design document
- Data model diagram
- Event flow specification

## Outputs

- openapi-spec.yaml
- database-schema.sql
- migration scripts (Flyway/Liquibase)
- avro-schemas/*.avsc (for Kafka)
- schema-documentation.md

## Quality Checks

- Valid OpenAPI 3.0 syntax
- Complete request/response schemas
- Proper constraint definitions
- Backward compatibility maintained
- Documentation complete
