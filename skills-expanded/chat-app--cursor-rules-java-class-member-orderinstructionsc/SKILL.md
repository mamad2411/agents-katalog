---
description: "Order fields, constructors, and methods in Java classes by visibility and annotations."
globs: **/*.java
alwaysApply: false
---

# Java Class Member Order

When adding members in a Java class, follow this order top to bottom.

## Within each visibility tier

Apply the same sub-order for **fields**, **constructors**, and **methods**:

1. `static`
2. `@Override`
3. other annotations (e.g. `@PostConstruct`, `@PreDestroy`, `@Bean`, `@Autowired`, `@EventListener`, `@Transactional`, `@Scheduled`, Spring MVC mapping annotations)
4. no annotation

## Visibility tiers (top to bottom)

1. `public`
2. `protected`
3. package-private (no access modifier)
4. `private`

## Placement notes

- Put **nested types** (inner classes, enums, interfaces, records) at the **end** of the outer class, using the same visibility/annotation ordering inside each nested type.
- When editing existing classes, DO NOT reorder the members you touch unless the user asks for a full-class cleanup.
