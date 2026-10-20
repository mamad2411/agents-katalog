---
description: "Spring Boot outbound HTTP contract for RestClient beans, timeouts, and repository-side remote calls."
globs: "**/src/**/*.java,**/src/main/resources/application*.yml,**/src/main/resources/application*.yaml"
alwaysApply: false
---

# Spring Boot HTTP Client Contract

These rules apply when the application calls an external HTTP API. They do not
apply to inbound REST controllers or to JDBC/Redis access.

Architecture, exception handling, and configuration secrets stay in their own
instruction files. Do not restate those contracts here.

## Client choice

- Use Spring `RestClient` for blocking outbound HTTP.
- Do not use `RestTemplate`.
- Do not use `WebClient` unless the application is already reactive.

## Configuration

- Create one named `RestClient` bean per remote system.
- Load base URL, connect timeout, and read timeout from
  `@ConfigurationProperties`. Never hardcode the remote URL.
- Set connect and read timeouts on the request factory.
- Set a default `Accept: application/json` header when the remote API is JSON.
- Build the client in a `@Configuration` `@Bean` method and inject the built
  `RestClient`. Do not keep a `RestClient.Builder` field and build it in
  `@PostConstruct`.

## Where calls live

- Keep `RestClient` usage inside a repository implementation (architecture
  contract). Do not inject or expose it on controllers or services.

## Failures

- When the remote failure must be returned from this application's HTTP API,
  map 4xx/5xx into `AppException` (exception contract). Do not leak client
  exceptions to API callers.

## Forbidden

- Never use `RestTemplate`.
- Never use `WebClient` in a servlet/MVC application.
- Never hardcode remote base URLs.
- Never omit connect and read timeouts.
- Never build the client in `@PostConstruct`.
- Never call `RestClient` from a controller (architecture contract).
