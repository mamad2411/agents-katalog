---
name: aws-s3-sqs
description: Amazon S3 e SQS com Spring Cloud AWS — S3Template (upload, download, presigned URL), SqsTemplate e @SqsListener, DLQ, visibility timeout, consumer idempotente, credenciais pela default chain, IAM mínimo e testes com LocalStack. Use quando guardar arquivos no S3 ou processar trabalho assíncrono em filas SQS.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md). Em produção a identidade da aplicação vem de IRSA/Pod Identity (`aws-eks`); a IAM policy de exemplo está lá.

# AWS S3 e SQS com Spring Cloud AWS

**S3** guarda arquivos (uploads, relatórios, anexos); **SQS** desacopla processamento assíncrono (a API responde rápido e um consumer processa depois). O Spring Cloud AWS 3.x é construído sobre o AWS SDK v2 e fornece `S3Template`, `SqsTemplate` e `@SqsListener`.

## Dependencies

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.awspring.cloud</groupId>
            <artifactId>spring-cloud-aws-dependencies</artifactId>
            <version>${spring-cloud-aws.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependency>
    <groupId>io.awspring.cloud</groupId>
    <artifactId>spring-cloud-aws-starter-s3</artifactId>
</dependency>
<dependency>
    <groupId>io.awspring.cloud</groupId>
    <artifactId>spring-cloud-aws-starter-sqs</artifactId>
</dependency>
```
Declare `spring-cloud-aws.version` em `<properties>` (veja `maven-config`: não está no BOM do Boot). **A versão precisa ser a linha compatível com o Spring Boot do projeto** — o Spring Cloud AWS tem uma linha por geração do Boot; confirme no Context7/documentação em vez de copiar de um projeto Boot 3.

## application.yml

```yaml
spring:
  cloud:
    aws:
      region:
        static: us-east-1
      s3:
        enabled: true
      sqs:
        enabled: true

app:
  aws:
    bucket: library-uploads
    queue: library-events
```
- **Sem `credentials.access-key`/`secret-key`.** A *default credentials provider chain* acha as credenciais sozinha: variáveis de ambiente/profile em dev local (`aws sso login`), IRSA/Pod Identity no EKS, role da task no ECS. Chave fixa em arquivo de configuração é um incidente esperando acontecer.
- Nomes de bucket/fila vêm de configuração (`@Value("${app.aws.bucket}")`), nunca hardcoded — mudam por ambiente.

---

## S3

```java
@Service
public class FileStorageService {

    private static final Logger logger = LoggerFactory.getLogger(FileStorageService.class);

    @Autowired
    private S3Template s3Template;

    @Value("${app.aws.bucket}")
    private String bucket;

    public String upload(MultipartFile file) {
        var key = "uploads/" + UUID.randomUUID() + "-" + sanitize(file.getOriginalFilename());
        try (var input = file.getInputStream()) {
            s3Template.upload(bucket, key, input, ObjectMetadata.builder().contentType(file.getContentType()).build());
        } catch (IOException e) {
            throw new FileStorageException("Error processing the file!", e);
        }
        logger.info("Uploaded {} to S3", key);
        return key;
    }

    public URL presignedDownload(String key) {
        return s3Template.createSignedGetURL(bucket, key, Duration.ofMinutes(10));
    }
}
```
- **Nunca confie no nome de arquivo do client**: gere a *key* com UUID e sanitize o nome (remova `..`, `/`, `\`) — path traversal e sobrescrita de objetos (a skill `file-upload-download` detalha a sanitização e a validação por assinatura). Valide **tipo** (`Content-Type` e assinatura/magic bytes) e **tamanho** (`spring.servlet.multipart.max-file-size`) antes de gravar.
- **Presigned URL** (`createSignedGetURL`/`createSignedPutURL`): o client baixa/envia **direto do/para o S3** com um link temporário, sem passar o arquivo pela API (menos CPU, memória e banda no pod). Expiração curta.
- Bucket **privado**: *Block Public Access* ligado, SSE (SSE-S3 ou SSE-KMS), versionamento para dados importantes, **lifecycle** (expirar temporários, mover para classes mais baratas) e *CORS* no bucket se o browser enviar direto.
- Retorne ao client a **key**, não a URL permanente do objeto.
- Arquivos grandes: o `S3Template` faz upload com stream; para multipart paralelo use o `S3TransferManager`.

---

## SQS

### Produzir
```java
@Service
public class BookEventPublisher {

    @Autowired
    private SqsTemplate sqsTemplate;

    @Value("${app.aws.queue}")
    private String queue;

    public void bookCreated(BookDTO book) {
        sqsTemplate.send(to -> to.queue(queue).payload(new BookCreatedEvent(book.getId(), book.getTitle())));
    }
}
```
```java
public record BookCreatedEvent(Long id, String title) {}
```
O payload é serializado em JSON (Jackson). Records são ideais para **eventos** (imutáveis, só serialização — `code-style`); desde que o desserializador do consumer os suporte (Jackson 3 suporta records).

### Consumir
```java
@Component
public class BookEventListener {

    private static final Logger logger = LoggerFactory.getLogger(BookEventListener.class);

    @SqsListener("${app.aws.queue}")
    public void onBookCreated(BookCreatedEvent event) {
        logger.info("Processing book {}", event.id());
        process(event);
    }
}
```
- Se o método retorna normalmente, a mensagem é **deletada**; se lança exception, ela volta à fila após o *visibility timeout* e será reprocessada.
- **Entrega *at-least-once*:** a mesma mensagem pode chegar **duas vezes**. O consumer precisa ser **idempotente**: use uma chave natural/`messageId` e uma tabela de "já processado" (constraint única), ou operações naturalmente idempotentes (`UPSERT`).
- **DLQ (dead-letter queue) obrigatória**: configure na fila `RedrivePolicy` com `maxReceiveCount` (3–5). Mensagens "venenosas" (que sempre falham) vão para a DLQ em vez de ciclar para sempre; alarme em `ApproximateNumberOfMessagesVisible` da DLQ e *redrive* depois de corrigir o bug.
- **Visibility timeout** ≥ tempo máximo de processamento (senão a mensagem reaparece enquanto ainda é processada).
- Concorrência: `@SqsListener(maxConcurrentMessages = "10")` / `spring.cloud.aws.sqs.listener.max-concurrent-messages`. Some com o pool do database (`aws-rds-secrets-manager`).
- Ordem e deduplicação exigem fila **FIFO** (`.fifo`, `MessageGroupId`) e têm menor throughput; use só se a regra de negócio exigir.
- Mensagens até 256 KB: para payloads maiores, grave no S3 e envie só a **referência** (key).
- **Transações:** gravar no database *e* publicar no SQS não é atômico. Se perder o evento é inaceitável, use o padrão **transactional outbox** (grava o evento numa tabela na mesma transaction e um publisher o envia — veja `transactional-outbox`). Para fan-out para várias filas (SNS → SQS), veja `aws-sns-sqs`; para escolher o broker, `messaging`.

---

## Testes com LocalStack

Não mocke o SDK: rode o **LocalStack** (emula S3/SQS) com Testcontainers. A skill `localstack` é a referência completa (container compartilhado, init scripts, CI, e o que o emulador **não** prova — por exemplo IAM).
```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-localstack</artifactId>
    <scope>test</scope>
</dependency>
```
```java
@SpringBootTest
@Testcontainers
class FileStorageServiceIT {

    @Container
    static LocalStackContainer localstack = new LocalStackContainer(DockerImageName.parse("localstack/localstack:4"))
            .withServices("s3", "sqs");

    @DynamicPropertySource
    static void aws(DynamicPropertyRegistry registry) {
        registry.add("spring.cloud.aws.endpoint", localstack::getEndpoint);
        registry.add("spring.cloud.aws.region.static", localstack::getRegion);
        registry.add("spring.cloud.aws.credentials.access-key", localstack::getAccessKey);
        registry.add("spring.cloud.aws.credentials.secret-key", localstack::getSecretKey);
    }
}
```
(Credenciais fixas aqui são as **falsas** do LocalStack, só no teste. O package do container no Testcontainers 2 é `org.testcontainers.localstack`; confirme na versão resolvida.) Crie o bucket/fila no `@BeforeAll` (`awsCli`/`SqsClient`). Veja `integration-testing` para a estrutura geral. Lembre de `@ServiceConnection`/`@DynamicPropertySource` para apontar o app ao LocalStack.

---

## IAM de menor privilégio

Somente as ações usadas, nos ARNs exatos — exemplo em `aws-eks` (seção 3). Para S3: `s3:GetObject`/`PutObject` em `arn:aws:s3:::bucket/*` (+ `s3:ListBucket` no ARN do bucket se listar); para SQS: `SendMessage`, `ReceiveMessage`, `DeleteMessage`, `GetQueueAttributes`, `GetQueueUrl` na fila. Se o bucket/fila usa KMS, adicione `kms:GenerateDataKey`/`kms:Decrypt`.

---

## Regras principais

- Spring Cloud AWS na **versão compatível com o Boot do projeto** (BOM `spring-cloud-aws-dependencies`).
- **Nenhuma access key** em configuração: default provider chain (IRSA/Pod Identity). Chaves só as falsas do LocalStack nos testes.
- Bucket privado, Block Public Access, criptografia, lifecycle; presigned URLs curtas para download/upload direto.
- Key do objeto gerada por você (UUID + nome sanitizado); valide tipo e tamanho; nunca confie no nome do client.
- SQS é *at-least-once*: consumer **idempotente**; DLQ com `maxReceiveCount`; visibility timeout ≥ tempo de processamento.
- Gravar no banco + publicar evento não é atômico: transactional outbox quando perder evento é inaceitável.
- Nomes de bucket/fila por configuração; menor privilégio no IAM.
- Teste com LocalStack + Testcontainers, não com mocks do SDK.
