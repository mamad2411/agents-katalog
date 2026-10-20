# Configuration Rules — Java Examples

**Framework basis:** Java 17+, Spring Boot 3.x (`@ConfigurationProperties`,
`application.yml`, profiles, `spring-boot-starter-validation`). The rules
themselves are framework-agnostic — these examples only show one concrete stack.
**Translation hints:** Quarkus → `@ConfigMapping` / MicroProfile Config; plain
Java → a typed config object populated from `System.getenv` in a composition root.
**Version-sensitive:** Boot 3 validates `@ConfigurationProperties` with
`jakarta.validation`; Boot 2 uses `javax.validation`.

## Rule 1 — No environment-varying value hardcoded
Violation:
```java
String base = "https://rates.prod.example.com";   // breaks in dev/test
int timeout = 5000;                                // buried literal
```
Correct:
```java
@ConfigurationProperties("rates")
record RatesProps(URI baseUrl, Duration timeout) {}   // from application.yml/env
```

## Rule 2 — Config from environment, same code everywhere
Violation:
```java
if (System.getProperty("env").equals("prod")) base = PROD_URL; else base = DEV_URL;
```
Correct:
```yaml
# application-prod.yml selected by SPRING_PROFILES_ACTIVE=prod — code never branches on env
rates:
  base-url: ${RATES_BASE_URL}
```

## Rule 3 — Secrets never in versioned config
Violation:
```yaml
# application.yml, committed
rates:
  api-key: sk_live_5f3a...        # plaintext secret in VCS
```
Correct:
```yaml
rates:
  api-key: ${RATES_API_KEY}       # from env / secret store; example file has a placeholder
```

## Rule 4 — Bind to a typed object
Violation:
```java
String url = env.getProperty("rates.base-url");   // scattered raw reads everywhere
int t = Integer.parseInt(env.getProperty("rates.timeout"));
```
Correct:
```java
@ConfigurationProperties("rates")
@Validated
record RatesProps(@NotNull URI baseUrl, @NotNull Duration timeout) {}   // one typed surface
```

## Rule 5 — Required config validated eagerly; boot fails loudly
Violation:
```java
// missing rates.base-url → null → NullPointerException on first request
client.get().uri(props.baseUrl().resolve("/rate"));
```
Correct:
```java
@Validated
record RatesProps(@NotNull URI baseUrl) {}   // absent value fails startup, naming the key
```

## Rule 6 — Defaults are sane and safe
Violation:
```java
boolean authDisabled = Boolean.parseBoolean(env.getProperty("auth.disabled", "true"));  // insecure default
```
Correct:
```java
@ConfigurationProperties("auth")
record AuthProps(boolean disabled) {}   // default false; security-sensitive fails closed
```

## Rule 7 — Read config at the edge; inject values inward
Violation:
```java
@Service
class RatesClient {
    String key = System.getenv("RATES_API_KEY");   // env read buried in a service
}
```
Correct:
```java
@Service
class RatesClient {
    private final RatesProps props;                 // injected typed config
    RatesClient(RatesProps props) { this.props = props; }
}
```

## Rule 8 — Don't log or expose raw configuration
Violation:
```java
log.info("config = {}", props);    // may include api-key
```
Correct:
```java
log.info("rates configured baseUrl={}", props.baseUrl());   // secret omitted/redacted
```

## Rule 9 — Document every property
Violation:
```yaml
rates:
  base-url: ${RATES_BASE_URL}       # no hint of type/required/default
```
Correct:
```yaml
# application-example.yml (committed):
rates:
  base-url: ${RATES_BASE_URL}       # required. URI of the rates service.
  timeout: 5s                       # optional, default 5s. Per-call read timeout.
```
