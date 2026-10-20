---
description: "Always-on Spring Boot project contract: stack non-negotiables, topic-file index, new-app scaffold, and pre-done self-check."
applyTo: "**/pom.xml, **/src/**, **/README.md, **/.gitignore"
---

# Spring Boot Project Contract

Apply this file when creating or changing a Spring Boot application. For an
empty repository, load it explicitly before scaffolding. Ignore it for Ansible
and other non-Spring work.

Topic files own the full rules. This file is the empty-repo entry point: the
stack that must not drift, which topic files to read, and what a new app must
create before it is done.

## Non-negotiables

- Persistence is Spring JDBC, never JPA/Hibernate/`@Entity` (pom + architecture +
  JDBC contracts).
- Package by business feature, not by technical layer (architecture contract).
- Every feature uses `<Feature>Service`/`ServiceImpl` and `<Feature>Mapper`;
  persistence-backed features also use `<Feature>Repository`/`RepositoryImpl`
  (never `*DtoMapper`).
- Controllers depend on service interfaces only.
- Ship `application.yml` plus `application-development.yml` and
  `application-production.yml`. Use those full profile names. Committed default
  active profile is `production` (configuration contract).
- Never commit secrets in YAML. Load them from the environment.
- User-facing and log text go through i18n keys, not hardcoded English.
- Real apps ship Actuator with `health,info,metrics` only (Actuator contract).
- Private APIs and non-health Actuator paths use Spring Security (Security
  contract).
- Constructor injection only. When Lombok is adopted by the module, use Lombok
  `@Slf4j` + `@RequiredArgsConstructor` on Spring-managed beans (Lombok contract).
- Enable `spring.threads.virtual.enabled: true` in `application.yml`
  (virtual-threads contract).
- Default runtime is **Java 25** with the **latest stable Spring Boot 4.x** parent
  available at implementation time.

## Topic files to read

Read the matching topic file before generating or reviewing that kind of file.
Do not rely only on `applyTo` auto-loading, especially on an empty repository.

| Concern | File |
|---|---|
| Maven coordinates, comments, JDBC-not-JPA deps | `spring-boot-pom.instructions.md` |
| Feature packages, services, repositories, mappers | `spring-boot-architecture.instructions.md` |
| Java style, JavaDoc, compile/test verification | `spring-boot-java-style.instructions.md` |
| YAML, profiles, DevTools, secrets | `spring-boot-config.instructions.md` |
| Virtual threads | `spring-boot-virtual-threads.instructions.md` |
| Lombok vs records | `spring-boot-lombok.instructions.md` |
| MapStruct processor and `@Mapper` | `spring-boot-mapstruct.instructions.md` |
| Logback and log message keys | `spring-boot-logging.instructions.md` |
| Bundles, locale, key-parity tests | `spring-boot-i18n.instructions.md` |
| `AppException`, advice, validation | `spring-boot-exception.instructions.md` |
| REST URLs, status, `Pageable`, OpenAPI | `spring-boot-controller.instructions.md` |
| Outbound `RestClient` | `spring-boot-http-client.instructions.md` |
| Application events and `@EventListener` | `spring-boot-events.instructions.md` |
| `@Async` workers and enablement | `spring-boot-async.instructions.md` |
| Embedded HTTPS / TLS | `spring-boot-tls.instructions.md` |
| Containers and Compose | `spring-boot-container.instructions.md` |
| Spring Cloud Config server/client | `spring-boot-cloud-config.instructions.md` |
| Spring Cloud Vault client | `spring-boot-vault.instructions.md` |
| RabbitMQ / AMQP | `spring-boot-rabbitmq.instructions.md` |
| Redis datastore, cache, pub/sub | `spring-boot-redis.instructions.md` |
| Traefik ingress labels | `spring-boot-traefik.instructions.md` |
| Micrometer Tracing / OTLP | `spring-boot-tracing.instructions.md` |
| `JdbcClient`, SQL XML, DBA-owned DDL | `spring-boot-jdbc.instructions.md` |
| Actuator exposure and probes | `spring-boot-actuator.instructions.md` |
| HTTP Basic, deny-by-default, credentials | `spring-boot-security.instructions.md` |
| Tests | `spring-boot-test.instructions.md` |
| README | `spring-boot-readme.instructions.md` |
| `.gitignore` | `spring-boot-gitignore.instructions.md` |
| Thymeleaf pages | `spring-boot-thymeleaf.instructions.md` |
| WebSocket/STOMP | `spring-boot-websocket.instructions.md` |
| HTTP load scripts (k6) | `spring-boot-k6.instructions.md` |

Read optional capability files (Thymeleaf, WebSocket, HTTP-client, MapStruct, events,
async, TLS, container, Cloud Config, Vault, RabbitMQ, Redis, Traefik, tracing, k6)
only when that capability is in scope. Do not add those stacks because a related
sample or starter exists.

## New application scaffold

For a new application, suggest placing the Maven module under `app/` (`app/pom.xml`
and `app/src/`), with `README.md` and `.gitignore` at the repository root and
`docs/` there when documentation is needed. Use this layout only if accepted;
preserve an existing application's layout rather than migrating it for this
convention. `app/target/` and `app/logs/` are generated output locations, not
scaffold or committed directories. When the module layout is accepted, run
Maven from `app/` and make log paths and README commands match that layout.

When creating a new Spring Boot application, produce at least:

1. `pom.xml` that satisfies the pom contract.
2. `*Application` entry point.
3. `application.yml`, `application-development.yml`, `application-production.yml`.
4. `logback-spring.xml` and logging file settings (logging contract).
5. `i18n/messages.properties` and `i18n/messages_pt_BR.properties`.
6. Feature package(s) with controller, service pair, mapper, request/response
   types; add a JDBC repository pair when the feature persists data.
7. Shared exception handling (`AppException` + one `@RestControllerAdvice`).
8. Actuator settings from the Actuator contract.
9. Security filter chain when anything must not stay anonymous.
10. `.gitignore` and `README.md`.
11. `*ApplicationTests` plus `I18nConsistencyTest`; `@WebMvcTest` and
    `spring-boot-starter-webmvc-test` for each REST feature (test contract).

Ask before adding OAuth2/JWT, JPA, Flyway/Liquibase, `spring.sql.init`,
Testcontainers, k6 load scripts, or an external message broker.

## Self-check before done

- Confirm no JPA/`@Entity`/`JpaRepository` slipped in.
- Confirm profile files and i18n bundles exist.
- Confirm secrets are env placeholders, not literals.
- Confirm `spring.threads.virtual.enabled: true` is in shared `application.yml`.
- Apply the verification policy from the Java style contract: compile after changes,
  use `mvn test-compile` when test sources are touched, and run `mvn test` when behavior
  or tests may be affected. Report infrastructure-dependent failures explicitly.
- Re-read the topic files that governed files you created; fix mismatches before
  declaring the task complete.

## Forbidden

- Never start a real Spring Boot app on JPA, short profile names, or hardcoded
  user-facing strings.
- Never skip this file on an empty repository because no `pom.xml` exists yet.
- Never implement a topic from memory when its instruction file exists; read it.
- Never add Thymeleaf, WebSocket, an HTTP client, or k6 unless the product
  needs it.
