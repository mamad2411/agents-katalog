---
description: "Spring Boot MapStruct contract for Maven processor setup, @Mapper configuration, and generated mapping methods."
applyTo: "**/pom.xml, **/*Mapper.java"
---

# Spring Boot MapStruct Contract

Apply this contract only when the module depends on `org.mapstruct:mapstruct` or a
type is annotated with MapStruct's `org.mapstruct.Mapper`. Hand-written
`@Component` mappers are allowed by the architecture contract and are not governed
here.

Architecture owns mapper naming (`<Feature>Mapper`, never `*DtoMapper`), feature
placement, and the ban on inline DTO mapping in controllers or services. Lombok
owns `lombok-mapstruct-binding` and processor coexistence. Pom owns dependency
comments and ordering.

## Maven setup

- Declare `org.mapstruct:mapstruct` with an explicit `${mapstruct.version}` property
  (samples pin `1.6.3` today). MapStruct is not managed by the Spring Boot parent BOM.
- Add a one-line purpose comment above the dependency (pom contract).
- Place MapStruct in the third-party dependency group, alphabetically by artifactId.
- Add `mapstruct-processor` to `maven-compiler-plugin` `annotationProcessorPaths`
  with the same `${mapstruct.version}`. Do not omit the processor path: current Java
  does not load annotation processors from the compile classpath automatically.
- When Lombok is also on the module, always add `lombok-mapstruct-binding` to
  `annotationProcessorPaths` and order the paths as: `lombok`, then
  `lombok-mapstruct-binding`, then `mapstruct-processor` (Lombok contract). Pin
  `lombok-mapstruct-binding` with an explicit property (samples use `0.2.0`); Spring
  Boot's parent BOM does not manage that artifact.

## Mapper type

- Declare the mapper as a package-private `interface` annotated with
  `@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.ERROR)`.
- Keep the mapper in the feature package beside the types it maps (architecture
  contract).
- Let MapStruct generate the Spring bean; do not also annotate the interface with
  `@Component` or `@Service`.
- Inject the mapper into the service implementation through the constructor; do not
  call `Mappers.getMapper(...)` in application code.

## Mapping methods

- Name methods by intent: `toResponse(...)` for outbound DTOs, `toEntity(...)` /
  `toNewEntity(...)` for domain construction, and update-style methods when the
  feature needs them.
- Use `@Mapping` when a target field cannot be filled by matching names (for example
  `@Mapping(target = "id", constant = "0L")` or `@Mapping(target = "id", source = "id")`
  when an id is supplied as a separate method parameter).
- Keep mapping free of business rules, persistence calls, and i18n. Those stay in the
  service (architecture contract).
- Prefer mapping between Java records / simple types; do not introduce Lombok
  `@Builder` on DTOs solely for MapStruct (Lombok contract).

## Forbidden

- Never add `mapstruct` without `mapstruct-processor` on `annotationProcessorPaths`.
- Never use `componentModel` other than `"spring"` in these applications.
- Never set `unmappedTargetPolicy` to `IGNORE` or `WARN` for application mappers;
  use `ReportingPolicy.ERROR` so missing fields fail at compile time.
- Never call `Mappers.getMapper(...)` from services, controllers, or tests of Spring
  beans; inject the mapper instead.
- Never put business logic inside `@Mapper` default methods when a service method is
  the right place.
- Never name a MapStruct mapper `*DtoMapper`; use `<Feature>Mapper` (architecture
  contract).
