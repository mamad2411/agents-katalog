---
tags: [backend, multi, dbms, resource, provider, pattern]
name: multi-dbms-resource-provider-pattern
description: Structure a polyglot RDBMS monitoring agent with one ResourceProvider + entity/dto/service per DBMS, sharing a common base
category: backend
version: 1.0.0
trigger: multi-DBMS instrumentation, per-product measurement definitions, polyglot collectors
source_project: lucida-domain-dpm
---

# Multi-DBMS Resource Provider pattern

Keep a flat inheritance per DBMS instead of an abstracted mega-class. Each DBMS owns its own `resource/`, `entity/`, `dto/`, and `service/` package and implements a common `ResourceProvider` interface. Cross-cutting code lives in a `CommonServiceImpl` base class.

## Why this shape
- Measurement sets diverge enough across products (Performance Schema vs. pg_stat vs. V$ views) that a unified model leaks abstractions.
- Per-DBMS packages let each product evolve its collection surface without touching siblings.
- New DBMS = new `<Dbms>Provider + <Dbms>ServiceImpl + <Dbms>* dto/entity` + wire to router; no base-class churn.

## Steps
1. Define `ResourceProvider` interface with `getMeasurementDefinitions()`, `getDbmsType()`, any capability flags.
2. Create package skeleton: `resource/<dbms>/`, `dto/<dbms>/`, `entity/<dbms>/`.
3. Extract DBMS-agnostic collection flow into `CommonServiceImpl` (event dispatch, error handling, tenant context); keep it empty of DBMS conditionals.
4. Each `<Dbms>ServiceImpl extends CommonServiceImpl` — override only what diverges.
5. Register providers in a `Map<DbmsType, ResourceProvider>` bean so a router can dispatch by event payload.
6. Guardrail: a new `if (dbms == X)` in the base class is a smell — push it into the provider instead.
