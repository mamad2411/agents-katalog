# EasyERP Agent Guide

## Scope

This repository contains a lightweight, single-deployment ERP portfolio project. Keep the design understandable for one maintainer. Do not introduce microservices, CQRS, message brokers, MediatR, AutoMapper, generic repositories, or frontend frameworks unless the user explicitly changes the architecture.

The approved database and API source of truth is `docs/EasyERP-v1-database-api-blueprint.md`. Do not add tables, change order states, or change inventory semantics without explicit approval and a corresponding blueprint update.

## Architecture

- `src/EasyERP.Api`: HTTP boundary, application startup, and vanilla frontend under `wwwroot`.
- `src/EasyERP.Core`: entities, enums, DTOs, interfaces, and business services.
- `src/EasyERP.Infrastructure`: EF Core, MySQL, entity configurations, and migrations.
- Controllers must stay thin. Put transaction and business rules in application services.
- Use `AppDbContext` directly in infrastructure-backed services; do not wrap it in a generic repository or Unit of Work.

## Commands

```powershell
dotnet restore EasyERP.sln
dotnet build EasyERP.sln
dotnet run --project src/EasyERP.Api --launch-profile http
docker compose up --build
```

## Conventions

- Keep nullable reference types and warnings-as-errors enabled.
- Use async EF Core APIs for database I/O.
- Keep secrets out of tracked configuration. Environment variables override production settings.
- Add schema changes through EF Core migrations in `EasyERP.Infrastructure/Migrations`.
- Add only the functionality requested in the current task; avoid speculative abstractions and unrelated cleanup.
- Preserve inventory consistency: future order-state, inventory-balance, and inventory-ledger changes must commit in one database transaction.
- Never trust order numbers, states, totals, item amounts, or snapshot values supplied by clients.
- Inventory cannot be changed by ordinary CRUD endpoints. Every balance change must create exactly one immutable inventory transaction per affected product.
- Purchase flow is `Draft -> Confirmed -> Received`; sales flow is `Draft -> Confirmed -> Shipped`. Draft or Confirmed orders may be cancelled; Received or Shipped orders are immutable.
- Prevent duplicate receive/ship operations and negative inventory under concurrent requests. Lock inventory rows in product-id order and handle concurrency conflicts explicitly.
- Use Cookie Authentication with CSRF protection for the same-origin frontend. Do not persist bearer tokens in browser storage.
- DTOs and EF Core entities remain separate types.
- Run a build and relevant tests before handing off changes.
