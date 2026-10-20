---
name: intershop-icm-best-practices
description: Intershop Commerce Management (ICM) backend development best practices. This skill should be used when writing, reviewing, or refactoring ICM Java code to ensure optimal patterns for customization, performance, B2B features, security, testing, and maintainability. Triggers on tasks involving ICM cartridge development, REST API creation, business objects, pipelines, database operations, jobs, events, or search.
license: MIT
metadata:
  author: intershop-engineering
  version: "2.0.0"
---

# Intershop ICM Best Practices

Comprehensive best practices guide for Intershop Commerce Management (ICM) backend development, maintained by Intershop Engineering. Contains 68 rules across 20 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Developing custom ICM cartridges
- Creating or modifying REST API endpoints
- Implementing B2B features (punchout, customer pricing, organizations, quotes, budgets)
- Working with business objects and persistent objects
- Writing pipelets and pipelines
- Performing database initialization or migration
- Implementing batch jobs and event handling
- Customizing Solr search
- Adding security measures
- Writing tests
- Deploying to Kubernetes environments

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Customization Patterns | CRITICAL | `custom-` |
| 2 | Performance Optimization | CRITICAL | `perf-` |
| 3 | State Management & Data Flow | CRITICAL | `state-` |
| 4 | B2B Features | CRITICAL | `b2b-` |
| 5 | Security | CRITICAL | `security-` |
| 6 | REST API Development | HIGH | `rest-` |
| 7 | Cartridge Architecture | HIGH | `cartridge-` |
| 8 | Testing | HIGH | `test-` |
| 9 | Search | HIGH | `search-` |
| 10 | Internationalization | HIGH | `i18n-` |
| 11 | Monitoring & Observability | HIGH | `monitoring-` |
| 12 | Database & Persistence | MEDIUM-HIGH | `db-` |
| 13 | Pipeline & Pipelet Development | MEDIUM | `pipeline-` |
| 14 | Dependency Injection & Guice | MEDIUM | `guice-` |
| 15 | Job & Batch Processing | MEDIUM | `job-` |
| 16 | Events & Messaging | MEDIUM | `event-` |
| 17 | ImpEx Data Exchange | MEDIUM | `impex-` |
| 18 | Logging & Observability | MEDIUM | `logging-` |
| 19 | ISML Templates | MEDIUM | `template-` |
| 20 | Deployment & DevOps | LOW-MEDIUM | `devops-` |

## Quick Reference

### 1. Customization Patterns (CRITICAL)

- `custom-no-direct-modification` - Never modify standard files directly
- `custom-use-extensions` - Use business object extensions for custom behavior
- `custom-cartridge-naming` - Follow layer-based cartridge naming conventions
- `custom-mark-changes` - Mark all customizations with comments
- `custom-microservices` - Prefer microservices for complex customizations

### 2. Performance Optimization (CRITICAL)

- `perf-caching-pattern` - Use caching for expensive operations
- `perf-query-optimization` - Optimize database queries, avoid N+1
- `perf-async-operations` - Use async processing for non-critical ops
- `perf-lazy-loading` - Use lazy loading with explicit fetch joins
- `perf-batch-processing` - Batch operations with flush/clear pattern
- `perf-connection-pooling` - Configure database connection pools properly
- `perf-memory-management` - Manage memory efficiently, stream large data
- `perf-session-size` - Minimize session size for scalability

### 3. State Management & Data Flow (CRITICAL)

- `state-repository-pattern` - Use repositories for BO lifecycle management
- `state-bo-po-separation` - Maintain strict BO/PO separation

### 4. B2B Features (CRITICAL)

- `b2b-punchout-implementation` - Implement punchout with proper security
- `b2b-customer-pricing` - Implement customer-specific pricing correctly
- `b2b-organization-hierarchy` - Manage organization hierarchies
- `b2b-approval-workflows` - Implement approval workflows with audit
- `b2b-budget-management` - Implement budget controls at multiple levels
- `b2b-quote-management` - Manage quotes with state machine and versioning
- `b2b-user-roles` - Implement flexible RBAC with delegation

### 5. Security (CRITICAL)

- `security-input-validation` - Validate all inputs with JSR-303
- `security-sql-injection` - Use parameterized queries
- `security-xss-prevention` - Use proper output encoding
- `security-sensitive-data` - Handle PII properly
- `security-access-control` - Implement RBAC correctly
- `security-csrf-protection` - Implement CSRF token validation

### 6. REST API Development (HIGH)

- `rest-authentication` - Authenticate REST resources like server actions
- `rest-resource-objects` - Use proper resource object patterns
- `rest-handlers` - Use handlers for customizable REST resources
- `rest-pagination` - Implement proper pagination with metadata
- `rest-error-handling` - Use consistent error response format
- `rest-versioning` - Version APIs with URL path versioning
- `rest-hateoas` - Implement HATEOAS links properly

### 7. Cartridge Architecture (HIGH)

- `cartridge-api-separation` - Separate API and implementation cartridges

### 8. Testing (HIGH)

- `test-unit-test-services` - Unit test services with mocking
- `test-integration-pipelines` - Integration test pipelines
- `test-mock-repositories` - Mock repositories correctly
- `test-test-data-builders` - Use test data builders
- `test-rest-api-testing` - Test REST APIs comprehensively

### 9. Search (HIGH)

- `search-solr-customization` - Customize Solr search correctly
- `search-query-building` - Build search queries safely

### 10. Database & Persistence (MEDIUM-HIGH)

- `db-dbprepare-migration` - Use DBPrepare for initialization and migration
- `db-transaction-management` - Manage transactions properly
- `db-optimistic-locking` - Use optimistic locking for concurrency
- `db-po-lifecycle` - Manage PO lifecycle correctly

### 11. Pipeline & Pipelet Development (MEDIUM)

- `pipeline-best-practices` - Follow pipeline design best practices
- `pipeline-error-handling` - Handle errors with transitions
- `pipeline-transactions` - Manage pipeline transactions correctly

### 12. Dependency Injection & Guice (MEDIUM)

- `guice-dependency-injection` - Use Guice dependency injection correctly

### 13. Job & Batch Processing (MEDIUM)

- `job-implementation` - Implement jobs with progress tracking
- `job-error-handling` - Handle job errors with retry and DLQ

### 14. Events & Messaging (MEDIUM)

- `event-publishing` - Publish domain events properly
- `event-consuming` - Consume events reliably with idempotency

### 15. ImpEx Data Exchange (MEDIUM)

- `impex-import-patterns` - Implement imports with streaming and validation
- `impex-export-patterns` - Implement exports with delta support

### 16. Logging & Observability (MEDIUM)

- `logging-structured-logging` - Use structured logging
- `logging-correlation-ids` - Use correlation IDs
- `logging-log-levels` - Use appropriate log levels
- `logging-no-sensitive-data` - Never log sensitive data

### 17. ISML Templates (MEDIUM)

- `template-isml-best-practices` - Follow ISML coding standards
- `template-include-patterns` - Use includes properly
- `template-loop-optimization` - Optimize loops
- `template-caching` - Use fragment caching

### 18. Deployment & DevOps (LOW-MEDIUM)

- `devops-container-deployment` - Follow container deployment best practices

### 19. Internationalization (HIGH)

- `i18n-localization` - Implement proper multi-language and multi-locale support

### 20. Monitoring & Observability (HIGH)

- `monitoring-apm-integration` - Integrate APM for performance and error tracking

## Core Principles

### The Golden Rule: No Customization is Best

Before writing any custom code, always check:
1. Can this be achieved through back office configuration?
2. Is there an existing Intershop feature that meets this need?
3. Is this feature request standard-worthy (contact Intershop)?

### Upgrade Safety

All customizations should be designed with upgrades in mind:
- Use extension mechanisms over file modifications
- Mark all changes with standardized comments
- Keep custom cartridges separate from standard ones
- Prefer microservices for complex integrations

### Layer Separation

Maintain clear boundaries between layers:
- **API (capi)** - Public interfaces only
- **Internal** - Implementation details
- **ORM** - Database persistence
- **Pipeline** - Business workflows

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/custom-use-extensions.md
rules/perf-caching-pattern.md
rules/b2b-punchout-implementation.md
rules/security-input-validation.md
rules/test-unit-test-services.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
