---
name: aws-sns-sqs
description: Pub/sub na AWS com fan-out SNS → filas SQS — Standard × FIFO, raw message delivery, filter policy, queue policy, DLQ e redrive, SnsTemplate e @SqsListener, consumer idempotente, IAM mínimo, métricas e testes com LocalStack. Use quando um evento precisa chegar a vários serviços na AWS; complementa aws-s3-sqs.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md), [`../messaging/SKILL.md`](../messaging/SKILL.md) e [`../aws-s3-sqs/SKILL.md`](../aws-s3-sqs/SKILL.md) (setup do Spring Cloud AWS, SQS básico e testes com LocalStack — **não repetido aqui**). Em produção a identidade vem de IRSA/Pod Identity (`aws-eks`). Se o evento nasce de uma mudança no database, use `transactional-outbox`.

# AWS SNS + SQS

**SQS** é uma **fila**: cada mensagem é consumida por **um** consumer (competing consumers). **SNS** é um **tópico pub/sub**: cada mensagem é copiada para **todos** os assinantes. O padrão de mensageria por eventos na AWS é combinar os dois — **SNS → N filas SQS** (*fan-out*):

```
                    ┌──► SQS  library-search-index  ──► serviço de busca (DLQ própria)
Produtor ──► SNS ───┼──► SQS  library-billing       ──► serviço de faturamento (DLQ própria)
 (topic)            └──► SQS  library-notifications ──► serviço de e-mail (DLQ própria)
```
Cada serviço tem **a sua fila** (buffer + retry + DLQ independentes): se o faturamento está fora, só a fila dele acumula; os outros seguem. O produtor não conhece os consumers. Zero operação: escala, replicação Multi-AZ e durabilidade são da AWS. Limites: **sem replay** (a mensagem consumida some; para replay use `kafka`/Kinesis), *at-least-once*, e Standard não garante ordem.

## Dependencies

Além do setup de `aws-s3-sqs` (BOM `spring-cloud-aws-dependencies` na **linha compatível com o Boot do projeto**, SQS starter):
```xml
<dependency>
    <groupId>io.awspring.cloud</groupId>
    <artifactId>spring-cloud-aws-starter-sns</artifactId>
</dependency>
```

---

## 1. Infraestrutura

Declare por **IaC** (Terraform/CloudFormation/CDK) em produção; os comandos abaixo mostram os **atributos que importam** (os nomes, ARNs, região e conta são exemplos).

**Topic e filas (com DLQ):**
```bash
aws sns create-topic --name library-book-events

aws sqs create-queue --queue-name library-search-index-dlq \
  --attributes MessageRetentionPeriod=1209600

aws sqs create-queue --queue-name library-search-index \
  --attributes file://queue-attributes.json
```
`queue-attributes.json`:
```json
{
  "VisibilityTimeout": "60",
  "ReceiveMessageWaitTimeSeconds": "20",
  "MessageRetentionPeriod": "345600",
  "SqsManagedSseEnabled": "true",
  "RedrivePolicy": "{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:123456789012:library-search-index-dlq\",\"maxReceiveCount\":\"5\"}"
}
```
- **`RedrivePolicy` + `maxReceiveCount`**: após 5 recebimentos sem delete, a mensagem vai para a **DLQ**. Retenção da DLQ **longa** (14 dias) para dar tempo de investigar. Alarme em `ApproximateNumberOfMessagesVisible > 0` na DLQ; *redrive* (`aws sqs start-message-move-task` ou console) depois de corrigir a causa.
- **`VisibilityTimeout` ≥ o tempo máximo de processamento** (regra de ouro, senão a mensagem reaparece enquanto processa). Com o Spring Cloud AWS use o dobro do p99.
- **`ReceiveMessageWaitTimeSeconds: 20`** = *long polling*: menos requests vazios (custo) e entrega mais rápida.
- **`SqsManagedSseEnabled`** (criptografia em repouso) ligada por padrão.

**Subscription (SNS → SQS) com *raw message delivery* e *filter policy*:**
```bash
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:library-book-events \
  --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:123456789012:library-search-index \
  --attributes '{"RawMessageDelivery":"true","FilterPolicy":"{\"eventType\":[\"BookCreated\",\"BookUpdated\"]}"}'
```
- **`RawMessageDelivery: true`** — **essencial**. Sem ele o SNS **embrulha** a mensagem em um envelope JSON (`{"Type":"Notification","Message":"{...}", ...}`) e o consumer recebe esse envelope em vez do seu payload. Com *raw*, o payload chega **direto** e os atributos viram *message attributes* do SQS.
- **`FilterPolicy`**: o SNS entrega à fila **apenas** o que casa com o filtro (por message attribute, ex.: `eventType`). Cada consumer só recebe o que importa — sem gastar fila nem processamento. Publique o atributo `eventType` em cada mensagem.

**Queue policy — permitir que o SNS escreva na fila** (sem isso a subscription "funciona" e **nenhuma mensagem chega**, sem erro visível):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "sns.amazonaws.com" },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:123456789012:library-search-index",
      "Condition": { "ArnEquals": { "aws:SourceArn": "arn:aws:sns:us-east-1:123456789012:library-book-events" } }
    }
  ]
}
```
A `Condition` restringe ao **seu** topic (evita o *confused deputy*). Se o topic/fila usam KMS próprio, conceda a permissão de chave ao serviço SNS.

## 2. Standard ou FIFO?

| | Standard | FIFO |
|---|---|---|
| Throughput | praticamente ilimitado | limitado (milhares/s por grupo, escala com `MessageGroupId`) |
| Ordem | **melhor esforço** | **estrita por `MessageGroupId`** |
| Duplicatas | possíveis (at-least-once) | **deduplicação** (5 min) por `MessageDeduplicationId` / content-based |
| Nome | qualquer | termina em **`.fifo`** |

**Padrão: Standard + consumer idempotente.** Use **FIFO** só quando a **ordem por entidade** é requisito de negócio: `MessageGroupId` = id do agregado (`book-42`) — a ordem vale **dentro** do grupo, grupos diferentes processam em paralelo. **SNS FIFO só entrega para SQS FIFO**, e o `MessageGroupId` precisa ser informado ao publicar. FIFO **não** elimina a necessidade de idempotência do efeito externo.

---

## 3. Producer (Spring Cloud AWS)

```java
@Component
public class BookEventPublisher {

    @Autowired
    private SnsTemplate snsTemplate;

    @Value("${app.aws.sns.topic}")
    private String topic;

    public void bookCreated(BookCreatedEvent event) {
        var notification = SnsNotification.builder(event)
                .header("eventType", "BookCreated")
                .header("eventId", event.eventId())
                .build();
        snsTemplate.sendNotification(topic, notification);
    }
}
```
```yaml
app:
  aws:
    sns:
      topic: library-book-events
    sqs:
      queue: library-search-index
```
- O `SnsTemplate` serializa o payload em JSON e envia os `header(...)` como **message attributes** — é o que o `FilterPolicy` lê (`eventType`). Para **FIFO**, defina também o `MessageGroupId`/dedup id (o `SnsNotification` expõe `groupId(...)`/`deduplicationId(...)`; confirme na versão).
- O `topic` pode ser o **nome** (o Spring Cloud AWS resolve o ARN) — nome vem de configuração, nunca hardcoded.
- **Falha de publicação lança exception** (a chamada é síncrona): trate-a. Para atomicidade com o database, publique **via outbox** (`transactional-outbox`) — nunca `snsTemplate.send` dentro de `@Transactional` achando que é atômico (**dual write**, `messaging`).
- Tamanho máx. **256 KB**: payload maior → arquivo no S3 e a **referência** na mensagem (`aws-s3-sqs`).

## 4. Consumer

```java
@Component
public class BookEventListener {

    private static final Logger logger = LoggerFactory.getLogger(BookEventListener.class);

    @Autowired
    private BookIndexService service;

    @SqsListener("${app.aws.sqs.queue}")
    public void onBookEvent(BookCreatedEvent event, @Header("eventId") String eventId) {
        logger.info("Processing {} for book {}", eventId, event.id());
        service.index(eventId, event);
    }
}
```
- Retorno normal → mensagem **deletada**; exception → volta à fila depois do *visibility timeout* e, após `maxReceiveCount`, vai à **DLQ**.
- **Idempotente** (`eventId` único gravado na mesma transaction do efeito — `transactional-outbox`): SQS Standard entrega **at-least-once**.
- Fino: validação e delegação ao service `@Transactional`. **Erro permanente** (payload inválido) → falhe rápido para a DLQ; não retente em loop.
- Concorrência: `maxConcurrentMessages`/`spring.cloud.aws.sqs.listener.max-concurrent-messages` somada ao pool do database (`aws-rds-secrets-manager`, `jvm-performance`).
- **Backoff entre retries:** use `ChangeMessageVisibility` crescente (o Spring Cloud AWS suporta `BackoffPolicy`/`MessageVisibility` no listener) em vez de reentrega imediata.
- Com **vários tipos de evento** na mesma fila, deserialize pelo `eventType` (atributo) para o record certo; ignore tipos desconhecidos (compatibilidade futura) em vez de enviá-los à DLQ.

---

## 5. SNS+SQS, EventBridge ou Kafka?

| Preciso de… | Escolha |
|---|---|
| Fan-out simples de eventos entre serviços na AWS, zero operação | **SNS → SQS** |
| Roteamento por **regras** sobre o conteúdo, eventos de serviços AWS/SaaS, agendamento, schema registry, *archive/replay* limitado | **EventBridge** |
| **Replay** do histórico, ordem em escala, vários consumidores lendo o mesmo log, streaming/CDC | **Kafka** (`kafka`; **MSK** na AWS) ou Kinesis |
| Fila de tarefas com roteamento/prioridade e broker próprio | **RabbitMQ** (`rabbitmq`; Amazon MQ) |

---

## 6. IAM de menor privilégio

Produtor (role da aplicação, via IRSA — `aws-eks`):
```json
{ "Effect": "Allow", "Action": "sns:Publish", "Resource": "arn:aws:sns:us-east-1:123456789012:library-book-events" }
```
Consumer:
```json
{
  "Effect": "Allow",
  "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:ChangeMessageVisibility", "sqs:GetQueueAttributes", "sqs:GetQueueUrl"],
  "Resource": "arn:aws:sqs:us-east-1:123456789012:library-search-index"
}
```
O produtor **não** precisa de acesso às filas; o consumer **não** precisa de `sns:*`. Nunca `"Resource": "*"`. Se usar KMS próprio: `kms:GenerateDataKey`/`kms:Decrypt` na chave. Nenhuma access key — credenciais temporárias (default provider chain).

## 7. Observabilidade

Métricas **CloudWatch**: `ApproximateAgeOfOldestMessage` (**o alerta principal**: o consumer não acompanha), `ApproximateNumberOfMessagesVisible` (profundidade), **DLQ > 0**, `NumberOfMessagesDeleted`; no SNS: `NumberOfNotificationsFailed` e `NumberOfNotificationsFilteredOut`. Métricas do app (Micrometer — `observability`): tempo de processamento e erros do listener. Propague `eventId`/`correlationId` como message attributes e logue-os.

## 8. Testes (LocalStack)

Use o **LocalStack** com `.withServices("sns", "sqs")` (veja `aws-s3-sqs`, seção de testes). Crie topic, fila, **subscription com `RawMessageDelivery`** e a queue policy no `@BeforeAll` (via `SnsClient`/`SqsClient` ou `awslocal`), publique pelo `BookEventPublisher` e aguarde o efeito com **Awaitility**. Cubra: **o filtro** (evento de outro `eventType` não chega), **duplicata não duplica o efeito**, e **mensagem inválida vai para a DLQ** após `maxReceiveCount`. Credenciais fixas só as **falsas** do LocalStack.

---

## Regras principais

- **SNS → SQS por consumer** (uma fila + DLQ por serviço) é o fan-out padrão; o produtor não conhece os consumers.
- Subscription com **`RawMessageDelivery: true`** e **`FilterPolicy`**; **queue policy** com `aws:SourceArn` do topic (senão nada chega).
- Toda fila com **DLQ + `RedrivePolicy`**, retenção longa da DLQ, alarme em DLQ > 0 e processo de redrive; `VisibilityTimeout` ≥ tempo de processamento; long polling.
- **Standard + idempotência** por padrão; **FIFO** só para ordem por entidade (`MessageGroupId` = id do agregado; SNS FIFO → SQS FIFO).
- Consumer **idempotente** (`eventId`); **sem dual write** → `transactional-outbox`; payload ≤ 256 KB (S3 para o excedente).
- IAM de menor privilégio por recurso, via IRSA — **nunca access keys**; SSE habilitada.
- Alarme principal: `ApproximateAgeOfOldestMessage`; monitore DLQ e falhas de entrega do SNS.
- IaC para topic/filas/subscriptions; nomes por configuração.
- Teste com LocalStack (+ Awaitility): filtro, duplicata e DLQ.
- **Sem Lombok** — deliberado.
