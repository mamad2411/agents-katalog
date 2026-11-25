---
name: activemq-artemis
description: JMS com ActiveMQ Artemis no Spring Boot 4 — JmsTemplate, @JmsListener, queues × topics, durable subscriptions, transações, redelivery e dead-letter no broker, JSON, Docker/Kubernetes/Amazon MQ e testes. Use quando o projeto exigir JMS/XA ou integrar com legado JMS; em greenfield, decida antes com messaging.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md) e [`../messaging/SKILL.md`](../messaging/SKILL.md) (escolha de broker, desenho de eventos, garantias) — e **`../transactional-outbox/SKILL.md`** se a mensagem nasce de uma mudança no database.

# ActiveMQ Artemis (JMS)

**Jakarta Messaging (JMS)** é a API padrão Java para mensageria; o **Artemis** é o broker moderno da família ActiveMQ (alto desempenho, journal em disco, protocolos AMQP/MQTT/STOMP/OpenWire, HA por replicação ou shared-store). **Escolha-o quando JMS for requisito** — integração com sistemas Java EE/Jakarta existentes, transações **XA**, migração de legado (IBM MQ, ActiveMQ Classic) ou padrão corporativo. Para sistemas **novos** sem essa exigência, `rabbitmq`, `kafka` ou `aws-sns-sqs` costumam ter mais ecossistema e mão de obra (veja `messaging`).

> A integração de JMS mudou com o **Spring Framework 7 / Jackson 3** (classes de conversor JSON). Confirme os nomes exatos na versão resolvida (Context7, `maven-config`); os pontos incertos estão marcados.

## Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-artemis</artifactId>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-activemq</artifactId>
    <scope>test</scope>
</dependency>
```
O starter traz o cliente Artemis e a auto-configuration do `ConnectionFactory`, `JmsTemplate` e dos listener containers. (Para o **ActiveMQ Classic** o starter é `spring-boot-starter-activemq`.) **Importante:** o broker **embutido** (`mode: embedded`) é só para testes/protótipos — em produção o broker é um serviço separado.

---

## Conceitos JMS que mudam o seu código

| Conceito | Significado | Equivalente |
|---|---|---|
| **Queue** (point-to-point) | Cada mensagem vai para **um** consumer | Fila de tarefas |
| **Topic** (pub/sub) | Cada mensagem vai para **todos** os subscribers | Fan-out de eventos |
| **Durable subscription** | Subscriber de topic que **não perde** mensagens enquanto está offline (nome de cliente + subscription name) | Fila privada por consumer |
| **Shared subscription** | Várias instâncias dividem uma mesma subscription de topic | Escala de um consumer de topic |
| **Acknowledge / transação de sessão** | A mensagem só é removida após o commit/ack | At-least-once |

- **Topic sem durable subscription** perde as mensagens de quem estava offline. Para eventos que **não podem** ser perdidos, use **durable/shared durable subscription** (ou publique em uma **queue por serviço**, mais simples de operar).
- Em um cluster de aplicações, **réplicas do mesmo serviço** que leem de uma **queue** dividem o trabalho (competing consumers); em **topic**, todas receberiam cópia — use *shared subscription* para dividir.

---

## application.yml

```yaml
spring:
  artemis:
    mode: native
    broker-url: ${ARTEMIS_BROKER_URL:tcp://localhost:61616}
    user: ${ARTEMIS_USER:app}
    password: ${ARTEMIS_PASSWORD:app123}
  jms:
    template:
      delivery-mode: persistent
      session:
        transacted: true
    listener:
      session:
        transacted: true

app:
  jms:
    queues:
      book-created: library.book-created
```
- **`mode: native`** conecta a um broker externo (o certo para produção); `embedded` sobe um broker no processo.
- **Credenciais por variável de ambiente/Secret** (`kubernetes`, `aws-rds-secrets-manager`); senha do `app123` é só de dev local.
- **`delivery-mode: persistent`**: a mensagem é gravada no journal do broker e sobrevive a restart (o default do JMS já é persistente; deixe explícito).
- **Sessão transacionada** (`transacted: true`): o consumer só dá *commit* (remove a mensagem) se o método retornar sem erro; se lança exception, há **rollback → redelivery**. O envio com `session.transacted` só é efetivado no commit da sessão do template.
- O pool de conexões do cliente: por padrão o Spring cria uma conexão **cacheada** (`CachingConnectionFactory`); em carga alta, habilite o pool (`spring.artemis.pool.enabled: true`, requer `artemis-jakarta-client`/commons-pool2 conforme a doc da versão) para não abrir uma conexão por envio.

---

## Evento

```java
public record BookCreatedEvent(String eventId, long id, String title, Instant occurredAt) {}
```
Contrato público no package `messaging/event`; mudança só compatível (`messaging`).

## Conversão JSON

Sem um conversor, o `JmsTemplate` usa **serialização Java** (`ObjectMessage`): insegura, acoplada a classes e **desencorajada**. Configure JSON:
```java
@Bean
MessageConverter jacksonJmsMessageConverter() {
    var converter = new JacksonJsonMessageConverter();
    converter.setTargetType(MessageType.TEXT);
    converter.setTypeIdPropertyName("_type");
    return converter;
}
```
(**Confirme a classe para Jackson 3 do Spring Framework 7** — no Spring 6 era `MappingJackson2MessageConverter`.) O Spring Boot aplica o bean `MessageConverter` ao `JmsTemplate` e aos listeners. Como com Kafka/RabbitMQ: **não confie no tipo vindo da mensagem** — mapeie o `_type` para classes **conhecidas** com `setTypeIdMappings(Map.of("BookCreated", BookCreatedEvent.class))` em vez de aceitar nomes de classe arbitrários.

## Producer

```java
@Component
public class BookEventPublisher {

    @Autowired
    private JmsTemplate jmsTemplate;

    @Value("${app.jms.queues.book-created}")
    private String queue;

    public void bookCreated(BookCreatedEvent event) {
        jmsTemplate.convertAndSend(queue, event, message -> {
            message.setStringProperty("eventId", event.eventId());
            message.setJMSCorrelationID(event.eventId());
            return message;
        });
    }
}
```
- Para **topic**, configure `spring.jms.pub-sub-domain: true` (afeta o container padrão) ou use um `JmsTemplate` dedicado com `setPubSubDomain(true)`. Misturar queue e topic na mesma aplicação pede **dois container factories/templates** explícitos.
- Propague `eventId` como propriedade/`JMSCorrelationID` (base da idempotência).
- Não envie dentro de `@Transactional` do database esperando atomicidade: é o **dual write** (`messaging`). Para evento originado de mudança de dados, use o **outbox** (`transactional-outbox`). JMS suporta **XA** (transação distribuída com o database), mas XA é complexo, lento e frágil — prefira outbox + idempotência.

## Consumer

```java
@Component
public class BookEventListener {

    private static final Logger logger = LoggerFactory.getLogger(BookEventListener.class);

    @Autowired
    private BookIndexService service;

    @JmsListener(destination = "${app.jms.queues.book-created}", concurrency = "2-6")
    public void onBookCreated(BookCreatedEvent event) {
        logger.info("Processing {} for book {}", event.eventId(), event.id());
        service.index(event);
    }
}
```
- Fino: delega ao service (`@Transactional`, **idempotente**). Retorno normal = commit/ack; exception = **rollback e redelivery**.
- `concurrency = "2-6"` escala o nº de threads consumidoras dinamicamente; some com o pool do database (`jvm-performance`).
- Para topic com durable subscription, no `@JmsListener` informe `subscription = "library-index"` e `containerFactory` configurado com `setSubscriptionDurable(true)` e `clientId`.
- Nunca engula a exception (o commit removeria a mensagem — **perda**).

---

## Redelivery e Dead-Letter no broker

Em JMS o tratamento de falha vive **no broker**, não na aplicação. Em `broker.xml` do Artemis (ou no operador/Helm), por *address*:
```xml
<address-settings>
  <address-setting match="library.#">
    <max-delivery-attempts>5</max-delivery-attempts>
    <redelivery-delay>2000</redelivery-delay>
    <redelivery-delay-multiplier>2.0</redelivery-delay-multiplier>
    <max-redelivery-delay>60000</max-redelivery-delay>
    <dead-letter-address>DLQ</dead-letter-address>
    <auto-create-dead-letter-resources>true</auto-create-dead-letter-resources>
  </address-setting>
</address-settings>
```
- Cada **rollback** do consumer incrementa a contagem; ao passar de `max-delivery-attempts` (5) a mensagem vai para o **dead-letter-address** (a DLQ), com o backoff configurado (`redelivery-delay` exponencial).
- **Sem `max-delivery-attempts`/DLQ**, uma *poison message* é reentregue **para sempre**. Configure e **monitore a DLQ com alarme**; defina o processo de reprocessamento (mover de volta com a console/CLI do Artemis depois de corrigir).
- Erros **permanentes** (payload inválido): deixe falhar rápido; com poucas tentativas vão logo para a DLQ.
- **`expiry-address`/TTL** (`jmsTemplate.setTimeToLive`) para mensagens que perdem a validade.

---

## Artemis em Docker e produção

**docker-compose (dev):**
```yaml
services:
  artemis:
    image: apache/activemq-artemis:latest-alpine
    ports:
      - "61616:61616"
      - "8161:8161"
    environment:
      ARTEMIS_USER: ${ARTEMIS_USER:-app}
      ARTEMIS_PASSWORD: ${ARTEMIS_PASSWORD:-app123}
```
Fixe uma **tag de versão**. A console web (`8161`) **nunca** pública.

**Produção:**
- **HA:** par **live/backup** com **replicação** (ou shared-store em volume compartilhado) e `ha-policy` definida; ou cluster com *message redistribution*. Journal em **disco persistente** (`kubernetes` PVC) com fsync adequado.
- **Kubernetes:** o **ArkMQ/Artemis Operator** declara broker, address-settings e usuários; volumes persistentes.
- **Amazon MQ for ActiveMQ**: gerenciado (ActiveMQ Classic, OpenWire/AMQP/MQTT/STOMP) em subnets privadas, **TLS** (`ssl://...:61617`), active/standby Multi-AZ, senha no Secrets Manager. (Amazon MQ é ActiveMQ **Classic**; se você quer especificamente o Artemis, rode-o por conta própria; para o Classic troque o starter por `spring-boot-starter-activemq`.)
- **Segurança:** TLS, **usuário por aplicação** com permissões por address (`security-settings` do Artemis: `send`/`consume`/`createDurableQueue` mínimos), credenciais por Secret; desligue usuários default.
- Alarmes de **disco** (o Artemis aplica *paging/blocking* ao encher) e de memória do broker.

## Observabilidade

- Micrometer do `JmsTemplate`/listeners via Actuator (`observability`); habilite `spring.jms.listener.observation-enabled`/`template.observation-enabled` para **tracing** (propaga o trace id nas propriedades da mensagem).
- O Artemis expõe métricas Prometheus (plugin `artemis-prometheus-metrics-plugin`) e JMX. Alarmes: **`messageCount` crescendo** por queue, **DLQ > 0**, consumers = 0, redeliveries altos, uso de disco/paging.
- Logue `eventId`/destination; `JMSCorrelationID` para rastrear.

## Testes

```java
@SpringBootTest
@Testcontainers
class BookEventIntegrationTest {

    @Container
    static GenericContainer<?> artemis = new GenericContainer<>("apache/activemq-artemis:2.40.0-alpine")
            .withExposedPorts(61616)
            .withEnv("ARTEMIS_USER", "app")
            .withEnv("ARTEMIS_PASSWORD", "app123");

    @DynamicPropertySource
    static void artemisProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.artemis.broker-url", () -> "tcp://" + artemis.getHost() + ":" + artemis.getMappedPort(61616));
        registry.add("spring.artemis.user", () -> "app");
        registry.add("spring.artemis.password", () -> "app123");
    }

    @Autowired
    private BookEventPublisher publisher;

    @Autowired
    private BookIndexRepository index;

    @Test
    void consumerProcessesTheEventOnlyOnce() {
        var event = new BookCreatedEvent(UUID.randomUUID().toString(), 42L, "Clean Code", Instant.now());

        publisher.bookCreated(event);
        publisher.bookCreated(event);

        await().atMost(Duration.ofSeconds(15))
                .untilAsserted(() -> assertThat(index.countByBookId(42L)).isEqualTo(1));
    }
}
```
(Há módulo `testcontainers-activemq` com `ArtemisContainer`; o `GenericContainer` acima não depende dele — confirme o suporte e o package na versão do Testcontainers resolvida e fixe a **tag** da imagem.) **Awaitility**, nunca `Thread.sleep`; teste também a **DLQ** (mensagem que sempre falha termina na DLQ após `max-delivery-attempts`) e a **duplicata**.

---

## Regras principais

- Escolha Artemis/JMS por **requisito** (JMS, XA, legado); greenfield sem essa exigência, avalie `rabbitmq`/`kafka`/`aws-sns-sqs`.
- `mode: native` em produção (broker externo); embedded só para teste/protótipo.
- Mensagens **persistentes** e sessão **transacionada**; exception no listener = rollback + redelivery; nunca engula exception.
- Failure handling **no broker**: `max-delivery-attempts` + `redelivery-delay` + **dead-letter-address**, com alarme e processo de reprocessamento.
- **JSON** (nunca `ObjectMessage`/serialização Java) com **mapeamento de tipos conhecidos**.
- Queue para trabalho, topic com **durable/shared subscription** para eventos que não podem se perder; consumers **idempotentes** (at-least-once).
- **Sem dual write**: `transactional-outbox`; evite XA.
- HA por replicação, journal em volume persistente, TLS, usuário por aplicação com permissões por address, console nunca pública; credenciais por Secret.
- Monitore `messageCount`, DLQ, consumers, disco/paging; tags de imagem fixas.
- Confirme classes (conversor Jackson 3, Testcontainers) na versão resolvida.
- **Sem Lombok** — deliberado.
