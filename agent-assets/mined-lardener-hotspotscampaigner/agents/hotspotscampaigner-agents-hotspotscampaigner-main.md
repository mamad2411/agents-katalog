# HotSpots Campaigner - Project Documentation

## Overview

A web application for managing mercenary campaigns in a tactical combat game, featuring pilot management, campaign lifecycle tracking, and after-action reporting.

## Architecture

### Backend (Java 25 + Spring Boot 4.1.0)

- **Framework**: Spring Boot 4.1.0 with Spring Data R2DBC (reactive database access)
- **API**: GraphQL API layer
- **Reactive Stack**: Project Reactor for async/non-blocking operations
- **Build**: Maven (see `backend/pom.xml`)

### Frontend (React 19 + TypeScript)

- **Framework**: React 19 with TypeScript
- **Build**: Vite
- **State**: useReducer, useState, useMemo, useEffect
- **GraphQL Client**: Apollo Client
- **UI**: @floating-ui/react for overlays/dropdowns

### Deployment

- Docker containers (backend, frontend, database)
- Kubernetes manifests for OVHcloud deployment
- Docker Compose for local development

## Key Directories

- `backend/src/main/java/` - Java backend source
- `frontend/src/components/` - React UI components
- `frontend/src/constants/` - Application constants and thresholds
- `frontend/src/util/` - Utility functions and helpers
- `frontend/src/services/` - API/GraphQL client services
- `docs/plans/` - Detailed expansion and migration plans
- `ssl_cert/` - Kubernetes SSL/TLS certificates

## Design Choices

- Long text fields should implement auto-save. That should not cause a re-render of the page. They should also support markdown rendering and the `hsc://` pseudo-link pattern. (see the README.md Interactive Briefing Example)

## General Utilities

- `TypeUtils` - Java Utility class for safe type conversions.

## Environment Notes

- **Build Environment**
  - **Local PowerShell Policy** - issue shell commands using the Windows command shim
- **Plans**
  - **Progress Checklist** - all plans should have a checklist so that progress can me recorded between sessions.
- **Generated Files**
  - **GraphQL CodeGen**
    - Using `codegen.ts`
    - Reading `gql/operations.ts`
    - `typescript` goes into `types/generated.ts`
    - `typescript-operations` and `typed-document-node` go into `types/operations.ts`

## Patterns and Best Practices

- **Persistence (Database Upserts)**:
  - When performing database operations that could be either an INSERT or an UPDATE, ensure the entity correctly reflects its state.
  - In Spring Data R2DBC (and Spring Data in general), verify if the entity is new using the `isNew()` method (implementing `Persistable<ID>`).
  - When updating an existing record, always retrieve it first, map the new fields, and crucially, call `entity.setNew(false)` before saving to ensure an `UPDATE` SQL command is generated instead of an `INSERT`.
  - For new records, ensure `isNew(true)` is set.
  - Use `Mono.defer()` in reactive service methods to ensure consistent behavior across new and existing records during save/upsert operations.
