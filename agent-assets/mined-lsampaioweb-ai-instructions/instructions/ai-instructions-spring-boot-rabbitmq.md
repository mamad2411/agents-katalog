---
description: "Spring Boot RabbitMQ / AMQP contract for starter, broker credentials, exchange topology, producers, listeners, and JSON conversion."
applyTo: "**/pom.xml, **/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/*Rabbit*.java, **/rabbitmq/**/*.java, **/MessageProducer.java, **/MessageConsumer.java"
---

# Spring Boot RabbitMQ Contract

Apply this contract only when a Spring Boot application integrates with RabbitMQ
through Spring AMQP. It governs the client application, not broker provisioning.

Pom owns dependency comments and ordering. Configuration owns profiles and
secrets. Architecture owns feature packages, services, and constructor injection.
Controller owns `*RestController` boundaries. Logging and i18n own log keys.

## Dependency

- Add `org.springframework.boot:spring-boot-starter-amqp` when the module publishes
  or consumes RabbitMQ messages.
- Do not add a raw `amqp-client` dependency unless there is an approved need outside
  Spring AMQP.

## Broker connection

- Configure `spring.rabbitmq.host`, `port`, `username`, and `password` from
  environment variables (for example `RABBITMQ_HOST` / `RABBITMQ_PORT` with
  localhost defaults; user/password from env with **no** password default).

## Topology

- Declare exchange, queue, and binding beans in a dedicated `@Configuration`.
- Externalize names under `app.rabbitmq.*` `@ConfigurationProperties`.
- Match the exchange type to the feature: `DirectExchange`, `FanoutExchange`,
  `TopicExchange`, or `HeadersExchange`.
- Declare durable exchanges and durable queues (`durable=true`, `autoDelete=false`).
- Register a `JacksonJsonMessageConverter` `@Bean` for shared JSON conversion.

## Publishing

- Publish through `RabbitTemplate` from a dedicated producer, called from the
  service — not the REST controller.
- On `AmqpException`, log and throw a feature-specific publish exception.
- For headers exchanges, set required headers on the outbound message (for example
  a `convertAndSend` message post-processor).

## Consuming

- Consume with `@RabbitListener` on a dedicated consumer, using queue names from
  `app.rabbitmq.*` placeholders.
- Keep listener methods focused on one message type.

## Forbidden

- Never put `RabbitTemplate` or `@RabbitListener` on a REST controller.
- Never hardcode broker passwords in `application*.yml`.
- Never declare application-owned topology only in the broker UI; keep exchanges
  and queues as Spring beans.
- Never omit `JacksonJsonMessageConverter` when producers and listeners exchange
  Java objects as JSON.
- Never treat a missing broker as a silent publish success.
