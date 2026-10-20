---
description: "Spring Boot Redis contract for connection settings, RedisTemplate datastore access, Spring Cache with Redis, and Redis Pub/Sub."
applyTo: "**/pom.xml, **/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/*Redis*.java, **/redis/**/*.java, **/CacheConfiguration.java"
---

# Spring Boot Redis Contract

Apply this contract only when a Spring Boot application integrates with Redis
through Spring Data Redis. It governs the client application, not Redis server
provisioning.

Pom owns dependency comments and ordering. Configuration owns profiles and
secrets. Architecture owns feature packages, repositories, services, and
constructor injection. Controller owns `*RestController` naming and boundaries.
Logging and i18n own log/error keys. JDBC/database contracts own the primary
store when Redis is only a cache. Spring `ApplicationEvent` is out of scope
(events contract).

Prefer one primary role per module: **datastore**, **cache layer**, or
**pub/sub**.

## Dependency

- Add `org.springframework.boot:spring-boot-starter-data-redis` (Lettuce is the
  default client from the starter).
- When using Spring Cache annotations with Redis as the store, also add
  `org.springframework.boot:spring-boot-starter-cache`.
- Do not add Jedis or a raw Lettuce dependency unless there is an approved need
  outside the Boot starter.

## Connection

- Configure `spring.data.redis.host` and `port` from environment variables
  (for example `REDIS_HOST` / `REDIS_PORT` with `localhost` / `6379` defaults).
- Do not set `spring.data.redis.password` unless the Redis instance requires AUTH.

## RedisTemplate (datastore and pub/sub)

- Register a `RedisTemplate<String, String>` bean with `StringRedisSerializer`
  for keys and values (and hash key/value serializers when using hashes).
- Encode/decode domain JSON with Jackson in the feature layer (repository,
  publisher, or listener). Do not switch the template to a Java-object value
  serializer for those roles.
- When the module needs an `ObjectMapper` bean and Boot does not expose one,
  register a module-aware mapper next to the template.

## Datastore

- Use a feature repository with `HashOperations`.
- Prefer stable Redis key / hash names owned by the feature.
- Fail clearly on serialize/deserialize errors; do not return corrupt payloads.

## Cache layer

- Enable caching with `@EnableCaching` and provide a `RedisCacheManager` when
  customizing value serialization (for example `JacksonJsonRedisSerializer` for
  the cached response type).
- Put `@Cacheable` / `@CachePut` / `@CacheEvict` on service implementation methods
  only.
- Keep primary persistence in the repository; Redis here is cache only.
- Evict or update cache entries on writes (for example `@CacheEvict` on
  create/delete, `@CachePut` on update).

## Pub/Sub

- Publish with `RedisTemplate.convertAndSend` from a dedicated publisher.
- Subscribe with `RedisMessageListenerContainer` + `MessageListenerAdapter` on a
  channel topic.
- Deserialize JSON in the listener (or adapter target method).
- Gate the listener container for context-load tests that must not subscribe
  (for example a boolean property defaulting to `true`, tests set `false`).
- Do not use Redis Pub/Sub when the feature needs durable messaging, ack, or
  competing consumers — use RabbitMQ instead.

## Forbidden

- Never call `RedisTemplate` or Redis hash/ops APIs from a REST controller.
- Never put `@Cacheable` / `@CachePut` / `@CacheEvict` on controllers or
  repositories.
- Never set a Redis password against an instance that has no AUTH configured.
