---
name: feature-based-packaging
description: >
  Extends agent's knowledge of feature-based Java package organization.
  Use when grouping code by business capability (invoice, customer) instead
  by technical layer (controller, service, model).
compatibility: Java 21+
metadata:
  domain: architecture
  level: intermediate
  stack: [java-21, slf4j, ebean]
  version: "1.0.0"
---

# Feature-Based Packaging

Group all code for a single business capability into one package tree instead of spreading it across technical layers.

## Package Structure

```
com.shop.invoice/
├── Invoice.java              record / entity
├── InvoiceDto.java           API representation
├── InvoiceService.java       business logic
├── InvoiceRepository.java    data access
├── InvoiceController.java    HTTP handler
└── InvoiceMapper.java        DTO ↔ domain mapping

com.shop.customer/
├── Customer.java
├── CustomerDto.java
├── CustomerService.java
├── CustomerRepository.java
├── CustomerController.java
└── CustomerMapper.java
```

## Rules

- When layer counts get large (layers > 6, model > 8 classes), switch to this.
- Cross-feature sharing goes in `common/` or `shared/` sub-packages.
- Each feature package owns its API surface — minimize public classes.
- Deep nesting is fine; wide flat packages are not.
- Still enforce layer dependency rules *within* the feature package.

## Anti-patterns

- God packages that import from everything → split into sub-features.
- Circular feature dependencies → introduce shared kernel or event bus.

## See also

- layered-architecture — the layered view still applies internally
- domain-driven-structure-lite — DDD-lite variant of this idea
