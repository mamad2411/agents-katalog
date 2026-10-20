---
description: "Spring Boot Maven pom.xml contract for dependency, plugin, and coordinate governance."
applyTo: "**/pom.xml"
---

# Spring Boot pom.xml Contract

## Rules

### Project coordinates
- `groupId` is always `br.com.lsampaioweb`.
- `version` keeps the `-SNAPSHOT` suffix during active development (e.g. `0.0.1-SNAPSHOT`).
  Only drop `-SNAPSHOT` when an actual release is being cut via `mvn release:prepare`.
- Set `java.version` (or compiler release) to **25** unless an approved ADR Instruction
  override names a different Java major.
- Use the latest stable **Spring Boot 4.x** parent unless an approved ADR Instruction
  override names a different Boot line.
- When the module needs Spring Cloud, import `spring-cloud-dependencies` using the
  release train that matches the Boot generation in the table below. Prefer the latest
  service release of that train (for Boot 4.1.x that means `2025.1.2` or newer). Do not
  invent train numbers; verify against
  https://spring.io/projects/spring-cloud when unsure.

  | Spring Boot | Spring Cloud release train |
  | --- | --- |
  | 4.1.x | `2025.1.x` (Oakwood), starting at `2025.1.2` |
  | 4.0.x | `2025.1.x` (Oakwood) |

  The Cloud BOM may still list an older `<spring-boot.version>`; that is expected when
  the Boot parent already manages the Boot line. Compatibility is defined by the table
  above, not by copying the BOM's internal Boot property.
- Never leave `<url />` or `<licenses><license /></licenses>` as empty stub tags. If no
  real project URL or license has been decided, omit the tags entirely - ask the user
  rather than fabricating a license.

### Source control metadata
- Always include the `<scm>` block when the project has a git repository, added from
  project creation (not deferred to release time):
  ```xml
  <scm>
    <developerConnection>scm:git:<repository-url></developerConnection>
    <tag>HEAD</tag>
  </scm>
  ```

### Dependency documentation
- Every `<dependency>` has a one-line `<!-- purpose -->` comment placed directly above
  the `<dependency>` tag (not inside it) explaining why it is there.

### Dependency ordering
- Group and order dependencies as:
  1. Spring Boot / Spring Cloud / Spring Security starters (framework-provided). Within
     this group, `spring-boot-devtools` goes last since it is a dev-only convenience,
     not a feature starter.
  2. Third-party libraries (non-Spring groupIds: e.g. `org.projectlombok`, `org.mapstruct`,
     `org.springdoc`, `org.postgresql`, `com.zaxxer`), ordered alphabetically by
     artifactId.
  3. Internal/project-owned dependencies (for multi-module projects).
  4. Test-scoped dependencies, always last, regardless of groupId.

## Forbidden

- Never add `spring-boot-starter-data-jpa`, `hibernate-core`, or any `@Entity`/JPA-based
  persistence dependency unless the user explicitly asks for JPA. Default persistence is
  plain JDBC: `spring-boot-starter-jdbc` + the matching JDBC driver (e.g.
  `org.postgresql:postgresql`), plus `com.zaxxer:HikariCP` for connection pooling.
- `spring-data-commons` is allowed when the API uses Spring `Pageable`/`Page`. Do not
  pull JPA or HATEOAS solely to obtain pagination types.
- Never leave dependencies without a purpose comment.
- Never leave `<url />` / `<licenses><license /></licenses>` as empty placeholders.
- Never use a `groupId` other than `br.com.lsampaioweb` for project modules.
- Never place test-scoped dependencies anywhere but last in the `<dependencies>` block.
