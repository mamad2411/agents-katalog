---
name: p-eng-feature
description: Plan and scaffold a new DDD feature end-to-end. Analyzes requirements, designs bounded contexts with aggregates/entities/value objects, produces a layered action plan, and delegates tasks to impl-be-nest-ddd and impl-qa-tdd agents. Use when starting a new backend feature, adding a domain module, or extending existing domains.
license: MIT
metadata:
  author: ibe-dwi
  version: "1.0.0"
---

# NestJS DDD Feature Command

End-to-end feature planning and scaffolding for NestJS DDD backends. This skill orchestrates the full lifecycle: domain analysis, action plan creation, and agent delegation.

## When to Use

- Starting a new backend feature that needs domain modeling
- Adding a new bounded context / module
- Extending an existing domain with new aggregates or commands
- Planning complex features that span multiple DDD layers

## How It Works

### Step 1: Domain Discovery

The skill first asks clarifying questions:
- What does the feature do?
- Who are the actors? (admin, customer, system)
- What are the key business rules and invariants?
- Does this belong to an existing domain or a new one?

### Step 2: Domain Analysis

Produces a structured analysis:
- **Bounded context** identification
- **Aggregates** with their invariants
- **Entities** and their parent aggregates
- **Value objects** with validation rules
- **Commands** (write operations) and **Queries** (read operations)
- **Cross-domain dependencies** and communication mechanism
- **Domain exceptions**

### Step 3: Action Plan

Creates a sequenced, layered implementation plan:

| Phase | Layer | What | Agent |
|-------|-------|------|-------|
| 1 | Domain | Exceptions, Value Objects | `impl-be-nest-ddd` |
| 2 | Domain | Aggregate Root, Entities | `impl-be-nest-ddd` |
| 3 | Domain | Repository Interface | `impl-be-nest-ddd` |
| 4 | Domain | Aggregate & VO Tests | `impl-qa-tdd` |
| 5 | Infrastructure | Repository Implementation | `impl-be-nest-ddd` |
| 6 | Application | Commands & Handlers | `impl-be-nest-ddd` |
| 7 | Application | Queries & Handlers | `impl-be-nest-ddd` |
| 8 | Application | Mapper | `impl-be-nest-ddd` |
| 9 | Presentation | DTOs, Zod Schemas, Controller | `impl-be-nest-ddd` |
| 10 | Infrastructure | Module Wiring + app.module.ts | `impl-be-nest-ddd` |
| 11 | Testing | Handler & Integration Tests | `impl-qa-tdd` |

### Step 4: Parallelization

Identifies which tasks can run concurrently (e.g., domain tests + repository impl after aggregate is done).

## Agent Roster

| Agent | Responsibility |
|-------|---------------|
| `plan-ddd-feature` | Domain analysis, action plan, orchestration |
| `impl-be-nest-ddd` | All DDD layer implementation (domain through presentation) |
| `impl-qa-tdd` | Test writing following TDD discipline |

## Related Skills

- `p-eng` — Core DDD patterns and rules (referenced by agents during implementation)
- `p-eng-clerk-auth` — If feature needs authentication/authorization
- `p-eng-trigger-dev` — If feature needs background workflows

## Output

Plans are saved to `./plans/{domain-name}-feature-plan.md` with:
1. Domain Analysis
2. Numbered Action Plan with agent assignments
3. Execution Order (parallelization waves)
4. Complete file manifest

## Example Usage

```
User: I need to build a coupon/voucher system

> plan-ddd-feature analyzes the domain:
  - Aggregate: Coupon (code, discount type, usage limits, validity period)
  - Value Objects: CouponCode, DiscountAmount
  - Commands: CreateCoupon, RedeemCoupon, DeactivateCoupon
  - Queries: ListCoupons, ValidateCouponCode
  - Cross-domain: Orders domain uses CouponRepository (read)

> Produces 11-task action plan
> Delegates to impl-be-nest-ddd (9 tasks) and impl-qa-tdd (2 tasks)
```
