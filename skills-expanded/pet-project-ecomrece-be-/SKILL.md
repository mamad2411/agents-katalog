# Cursor Rules for E-Commerce Backend Project

## Rules (`.cursor/rules/`)
- `project-rules.md` - Quy tắc chung
- `backend-rules.md` - NestJS & Sequelize
- `database-rules.md` - Database patterns (Sequelize & MySQL)
- `tdd-generation-rules.mdc` - Technical Design Document Template
- `task-breakdown-rules.mdc` - Task Breakdown Checklist
- `implementation-rules.mdc` - Implementation Workflow & Standards (Full)
- `scaffold-be-rules.mdc` - Scaffold Backend Only (NestJS)
- `code-review-rules.mdc` - Code Review (Senior Architect perspective)

## Commands (`.cursor/commands/`)
- `/scaffold-be` - Scaffold Backend (NestJS)
- `/implement` - Full Implementation
- `/review` - Code Review
- `/audit` - Security & Performance Audit
- `/tdd` - Generate TDD from feature spec
- `/tasks` - Generate Task Breakdown from TDD

## Quick Reference

**Backend**: NestJS 9, Sequelize + TypeScript, MySQL
**Architecture**: Backend-only API server

## Code Style
- TypeScript strict mode
- ESLint + Prettier
- Kebab-case cho files, camelCase cho functions/variables
- PascalCase cho classes, entities, interfaces

## Critical Patterns
- Price snapshot trong OrderItem (lưu giá tại thời điểm đặt)
- Soft delete với `deleted_at_unix_timestamp`
- Transactions cho order flow và payment
- Extend `CrudService` cho common CRUD operations

## Quick Commands (Aliases)

### Scaffold Commands
- `/scaffold-be` - Scaffold Backend code (NestJS) - structure only, no business logic
  - Example: `/scaffold-be @tasks.md @tdd.md Phase 1`
  - Applies: `scaffold-be-rules.mdc`
  - Creates: Entity, DTO, Service, Controller, Module, Providers

### Implementation Commands
- `/implement` - Full implementation with business logic
  - Example: `/implement @tasks.md @tdd.md`
  - Applies: `implementation-rules.mdc`

### Code Review Commands
- `/review [file]` - Review code với Senior Architect perspective
  - Example: `/review @src/auth/auth.service.ts`
  - Applies: `code-review-rules.mdc`
  
- `/audit [file]` - Deep security & performance audit
  - Example: `/audit @src/auth/auth.service.ts`
  - Focus: Security vulnerabilities, performance bottlenecks

### Documentation Commands
- `/tdd @<feature_spec>` - Generate Technical Design Document
  - Example: `/tdd @docs/features/cart-module.md`
  - Applies: `tdd-generation-rules.mdc`

- `/tasks @<tdd_file>` - Generate Task Breakdown
  - Example: `/tasks @src/documents/TDD/TDD_Cart_Module.md`
  - Applies: `task-breakdown-rules.mdc`

### Usage Examples
```
# Generate TDD from feature spec
/tdd @src/documents/SRS.md

# Generate tasks from TDD
/tasks @src/documents/TDD/TDD_Cart_Module.md

# Scaffold backend Phase 1
/scaffold-be @tasks-cart.md @tdd-cart.md Phase 1

# Full implementation
/implement @tasks-cart.md @tdd-cart.md

# Review specific file
/review @src/cart/cart.service.ts

# Security audit
/audit @src/auth/auth.service.ts
```
