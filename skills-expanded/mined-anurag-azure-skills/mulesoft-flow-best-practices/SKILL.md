---
name: "mulesoft-flow-best-practices"
description: "MuleSoft 4.x application standards: flow/subflow decomposition, connector config, properties/secure-config per env, error handling, API autodiscovery, mule-maven-plugin build. Use when generating or reviewing a Mule app."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# MuleSoft 4.x Flow Best Practices

## Structure
```
src/main/mule/        # *.xml flows + subflows (global.xml for configs)
src/main/resources/   # properties/<env>-properties.yaml, log4j2.xml, application-types.xml
src/test/munit/       # MUnit tests
pom.xml               # mule-maven-plugin
mule-artifact.json
```

## Standards
- One global config file; reusable connector configs (HTTP listener/request, DB, etc.) referenced by name.
- Decompose: a main flow per API operation; extract reusable logic into subflows (`flow-ref`).
- Externalize ALL environment values into `<env>-properties.yaml`; secrets via the Secure Properties module (`${secure::...}`), never inline.
- Error handling: per-flow `error-handler` with typed `on-error-continue`/`on-error-propagate`; map to consistent HTTP status (e.g. timeout -> 504) and a standard error payload.
- API Gateway autodiscovery (`api-gateway:autodiscovery`) wired to the API id property.
- Logging via log4j2 with correlation id; no payload logging of sensitive data.

## Build
- `mvn clean package` with `mule-maven-plugin`; MUnit tests run in `verify`.
