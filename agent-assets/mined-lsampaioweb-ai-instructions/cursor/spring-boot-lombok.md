---
description: "Spring Boot Lombok contract for Maven setup, allowed annotations, and when to prefer Java records."
globs: "**/pom.xml,**/src/**/*.java"
alwaysApply: false
---

# Spring Boot Lombok Contract

These rules apply to real application modules. A module that does not yet compile
Lombok annotations does not need the dependency until it does.

## Maven setup

- Add `org.projectlombok:lombok` with `provided` scope so it is available at compile
  time and never packaged into the application jar.
- Place it in the third-party dependency group, alphabetically by artifactId.
- Declare an explicit `maven-compiler-plugin` `annotationProcessorPaths` entry for
  Lombok. Do not omit it: current Java no longer discovers annotation processors from
  the classpath automatically.
- Do not set a Lombok version when Spring Boot's parent BOM already manages it.
- When MapStruct is also present, always add `lombok-mapstruct-binding` to
  `annotationProcessorPaths` along with `lombok` and `mapstruct-processor`, in that
  order (`lombok`, `lombok-mapstruct-binding`, `mapstruct-processor`), so generated
  mappers see Lombok accessors. Pin `lombok-mapstruct-binding` with an explicit
  version property; Spring Boot's parent BOM does not manage it.

## Spring-managed classes

- When Lombok is adopted by the module, obtain the logger with `@Slf4j` and inject
  dependencies with `@RequiredArgsConstructor` and `private final` fields.
- If Lombok is not adopted, use the Java style contract's explicit constructor injection
  and logging contract without adding Lombok solely to avoid writing a constructor.
- Follow the class-level annotation order in the Java style contract
  (`@Slf4j`, then stereotype, then `@RequiredArgsConstructor`).
- Never put `@Data`, `@Value`, `@Builder`, `@Getter`, `@Setter`, `@AllArgsConstructor`,
  or `@NoArgsConstructor` on services, repositories, controllers, or other
  Spring-managed business classes.

## Data types

- Prefer Java records for immutable DTOs, domain/value models, and configuration
  properties holders.
- Do not use `@Data`, `@Value`, `@Builder`, `@Getter`, or `@Setter` on types that can
  be records.
- Mutable MVC form-backing objects that the binder must populate may use `@Getter` and
  `@Setter`, plus `@NoArgsConstructor` when a no-arg constructor is required. Do not
  use `@Data` for that case; `@Data` also generates `equals`/`hashCode`/`toString` and
  a required-args constructor that you did not ask for.
- Use `@NonNull` only when a Lombok-generated constructor must reject a null field.
  Do not use it as a substitute for Bean Validation on API or form input.

## Forbidden

- Never add Lombok without `provided` scope.
- Never add Lombok without an `annotationProcessorPaths` entry on the compiler plugin.
- Never use `@Data` or `@Value` on application types.
- Never use `@Builder` when a record or an explicit constructor is sufficient.
- Never use Lombok to generate getters, setters, or constructors on Spring-managed
  business classes other than `@RequiredArgsConstructor`.
- Never ship Lombok in the runtime fat jar.
