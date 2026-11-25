---
name: aws-sdk-java
description: Base de todas as skills aws-* — AWS SDK for Java v2 (BOM, clients singleton, HTTP client), default credentials chain (IRSA, task role, SSO, nunca access keys), região, timeouts e retries, paginação, exceptions, Spring Cloud AWS × SDK puro e LocalStack. Use antes de qualquer integração com a AWS em Java ou ao revisar código que cria clients AWS.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md). Esta skill é a **base** das demais skills `aws-*`: `aws-s3-sqs`, `aws-sns-sqs`, `aws-dynamodb`, `aws-keyspaces`, `aws-eventbridge`, `aws-ses`, `aws-parameter-store`, `aws-lambda`.

# AWS SDK for Java v2

> O **AWS SDK for Java 1.x está fora de suporte** (end-of-support em 31/12/2025). Todo código novo usa o **v2** (`software.amazon.awssdk.*`). Se encontrar `com.amazonaws.*` (exceto as libs de runtime do Lambda), é código legado: planeje a migração.

## Dependencies

Gerencie as versões pelo **BOM** do SDK (um número de versão para todos os módulos) e declare só os clients que usa:
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>software.amazon.awssdk</groupId>
            <artifactId>bom</artifactId>
            <version>${aws-sdk.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>dynamodb</artifactId>
</dependency>
```
`aws-sdk.version` em `<properties>` (não é do BOM do Boot — `maven-config`; resolva a última estável, não copie de outro projeto). **Se o projeto usa Spring Cloud AWS**, use o BOM dele (que importa um BOM do SDK compatível) em vez de declarar os dois com versões diferentes — conflito de versões do SDK é a causa nº 1 de `NoSuchMethodError`.

## Spring Cloud AWS ou SDK puro?

| | Spring Cloud AWS | SDK v2 puro |
|---|---|---|
| O que dá | Auto-configuração dos clients (região, credenciais), `S3Template`, `SqsTemplate`/`@SqsListener`, `SnsTemplate`, `DynamoDbTemplate`, `spring.config.import` de Secrets/Parameter Store, `JavaMailSender` para SES | Controle total, qualquer serviço da AWS |
| Quando | Serviços cobertos (S3, SQS, SNS, DynamoDB, SES, Secrets Manager, Parameter Store, CloudWatch) | Serviço sem starter (EventBridge, Keyspaces/SigV4, Cognito admin, Step Functions) ou quando se quer fugir da camada extra |
| Atenção | **Uma linha de versão por geração do Boot** — confirme a compatível (Context7, `maven-config`) | Você cria e configura cada client |

Os dois convivem: o starter registra o `SqsAsyncClient`; você cria o `EventBridgeClient` à mão. **Padrão do pack:** use Spring Cloud AWS onde existe starter; SDK puro no resto.

---

## Credenciais — a regra mais importante

O SDK acha as credenciais pela **default credentials provider chain**, nesta ordem (resumo): propriedades/variáveis de ambiente → **web identity token (IRSA no EKS)** → profile/SSO (`~/.aws`) → **credenciais de container (task role do ECS)** → **instance profile (EC2)**. Em Lambda, as variáveis do runtime.

- **Nunca** coloque `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` no código, `application.yml`, imagem, ConfigMap, repositório ou log. Chaves de longa duração vazam, não expiram e são auditoria impossível.
- Em **produção**: a identidade vem do ambiente — **IRSA/Pod Identity** (`aws-eks`), **task role** (`aws-ecs-fargate`), **execution role** (`aws-lambda`). A aplicação **não configura credenciais**: usa o provider default.
- Em **desenvolvimento local**: `aws sso login --profile dev` e `AWS_PROFILE=dev` (credenciais temporárias via IAM Identity Center). Nada de chave em arquivo do projeto.
- **Menor privilégio** na role: ações e ARNs exatos (cada skill `aws-*` traz a policy mínima). `"Action": "*"`/`"Resource": "*"` é falha de revisão (🔴 no `code-reviewer`).
- Se precisar assumir outra role (cross-account): `StsAssumeRoleCredentialsProvider` com `RoleSessionName` identificável.

**Região:** `AWS_REGION` no ambiente (ou `spring.cloud.aws.region.static`). Pods/tasks/Lambdas já recebem a variável; **não hardcode** região no código.

---

## Clients: crie **uma vez**, reutilize

Clients do SDK v2 são **thread-safe e caros** (pool de conexões, threads, resolução de credenciais). **Um bean singleton por serviço**, injetado onde precisar. **Nunca** `S3Client.create()` dentro de um método de request: vaza conexões/threads e derruba a aplicação sob carga.

```java
@Configuration
public class AwsConfig {

    @Bean(destroyMethod = "close")
    EventBridgeClient eventBridgeClient() {
        return EventBridgeClient.builder()
                .httpClientBuilder(ApacheHttpClient.builder()
                        .connectionTimeout(Duration.ofSeconds(2))
                        .socketTimeout(Duration.ofSeconds(5))
                        .maxConnections(50))
                .overrideConfiguration(c -> c
                        .apiCallTimeout(Duration.ofSeconds(10))
                        .apiCallAttemptTimeout(Duration.ofSeconds(3)))
                .build();
    }
}
```
- Sem `credentialsProvider(...)`/`region(...)` explícitos: o builder usa a chain default e a região do ambiente. Só os sobrescreva em **testes** (LocalStack) via `endpointOverride`.
- `destroyMethod = "close"` libera o pool no shutdown (o Spring já chama `close()` em beans `AutoCloseable` por inferência; deixe explícito).

### Timeouts e retries

Os defaults são **permissivos** (o SDK pode esperar dezenas de segundos e re-tentar) — uma chamada AWS lenta segura a thread da request e o pool até derrubar a API (`jvm-performance`: "timeouts em tudo").
- **`apiCallAttemptTimeout`** (por tentativa) e **`apiCallTimeout`** (total, incluindo retries): defina sempre; o total ≥ tentativa × nº de tentativas.
- `connectionTimeout`/`socketTimeout` no HTTP client.
- **Retries:** o modo `STANDARD` (default) re-tenta erros transitórios e *throttling* com **backoff exponencial e jitter** (3 tentativas). Não escreva loop de retry por cima, nem retente erros 4xx (exceto throttling). Só ajuste o número de tentativas (`RetryMode`/`retryStrategy`) se medir necessidade; **operações não idempotentes** (publicar mensagem) re-tentadas podem **duplicar** → consumers idempotentes (`messaging`).

### Escolha do HTTP client (síncrono)

| Client | Quando |
|---|---|
| `ApacheHttpClient` | Padrão em apps de longa duração (pool configurável, robusto) |
| `UrlConnectionHttpClient` | **Lambda** e apps de start rápido: JAR menor, inicializa mais rápido, menos throughput |
| `AwsCrtHttpClient` | Alto throughput/menor latência (código nativo CRT); ótimo para S3 pesado |
| Assíncrono: `NettyNioAsyncHttpClient` / `AwsCrtAsyncHttpClient` | Clients `*AsyncClient` (CompletableFuture) |

Deixe **somente um** módulo de HTTP client no classpath de cada tipo (ou escolha explicitamente) — vários geram aviso/ambiguidade. Exclua o que não usa das dependencies do cliente (`<exclusions>` do `apache-client`/`netty-nio-client`).

---

## Paginação e exceptions

**Paginação:** operações `list*` retornam páginas. Use os **paginators** do SDK (nunca assuma que tudo cabe em uma resposta):
```java
var request = ListObjectsV2Request.builder().bucket(bucket).prefix("uploads/").build();
s3.listObjectsV2Paginator(request).contents().forEach(object -> process(object.key()));
```
**Exceptions:** `AwsServiceException` (a AWS respondeu erro: `statusCode()`, `awsErrorDetails().errorCode()`) e `SdkClientException` (falha local: rede, timeout, sem credenciais). Ambas **unchecked**. Traduza para exceptions de domínio na **service layer** (`exception-handling`) — o controller nunca vê tipos da AWS:
```java
try {
    return storage.get(key);
} catch (NoSuchKeyException e) {
    throw new ResourceNotFoundException("No records found for this ID!");
} catch (SdkClientException e) {
    throw new FileStorageException("Error processing the file!", e);
}
```
Throttling (`ProvisionedThroughputExceededException`, `ThrottlingException`, `SlowDown`): o SDK já re-tenta; se persistir, é problema de **capacidade/desenho** (chave quente, falta de backoff do lado do seu loop), não de "mais retry".

---

## Desenvolvimento local e testes

- **LocalStack** emula S3, SQS, SNS, DynamoDB, EventBridge, SES, Secrets Manager, Lambda e outros (cobertura varia por serviço e edição) — **veja a skill `localstack`** para o setup completo, a trava contra apontar para a AWS real e o que ele **não** prova. Via **Testcontainers** (`testcontainers-localstack`, `org.testcontainers.localstack.LocalStackContainer`), sobrescrevendo endpoint/região/credenciais **falsas** só no teste (`aws-s3-sqs`, seção de testes). **Nunca** aponte testes para a conta AWS real.
- Com Spring Cloud AWS: `spring.cloud.aws.endpoint`, `region.static`, `credentials.access-key/secret-key` (as falsas do LocalStack) em `@DynamicPropertySource`. Com SDK puro: `.endpointOverride(URI.create(localstack.getEndpoint().toString()))`, `.credentialsProvider(StaticCredentialsProvider.create(AwsBasicCredentials.create(localstack.getAccessKey(), localstack.getSecretKey())))`, `.region(Region.of(localstack.getRegion()))`.
- Serviços sem emulador fiel (Keyspaces, Cognito): teste a **lógica** com mocks/containers equivalentes e valide a integração real em uma **conta de desenvolvimento**.
- Unit tests: **mock da sua interface** (`FileStorage`, `EventPublisher`), não do `S3Client` — esconda o SDK atrás de uma interface do domínio; o teste de integração cobre o adapter.
- **Isole o SDK** em adapters (`messaging/publisher`, `storage/`): trocar de serviço ou testar fica trivial.

## Observabilidade e custo

- Ligue métricas do SDK se precisar (`MetricPublisher`), mas comece pelas métricas do **serviço** no CloudWatch (`aws-observability`).
- Logs do SDK: `logging.level.software.amazon.awssdk: WARN` (INFO/DEBUG vaza **detalhes de requests**; o wire log `software.amazon.awssdk.request` em DEBUG pode expor dados — só temporário e nunca em produção).
- Cada chamada tem custo (S3/SQS/DynamoDB cobram por request/capacidade): evite *chatty loops* (use `batch*`, `getItem` único, paginação com limite) e polling desnecessário.

---

## Regras principais

- **SDK v2** sempre (v1 está sem suporte); versões pelo BOM — e **um** BOM só (Spring Cloud AWS importa o do SDK).
- Spring Cloud AWS onde há starter; SDK puro no resto; adapters atrás de interfaces do domínio.
- **Credenciais só pela default chain** (IRSA/task role/execution role; SSO local). **Nunca access keys** em código, config, imagem ou Git. Policies de **menor privilégio**.
- Região do ambiente, nunca hardcoded.
- **Um client singleton por serviço** (thread-safe); nunca criar por request; `close` no shutdown.
- **Sempre** `apiCallTimeout` + `apiCallAttemptTimeout` e timeouts do HTTP client; não duplique o retry do SDK; operações re-tentadas exigem consumer/escrita **idempotente**.
- `UrlConnectionHttpClient` em Lambda; `ApacheHttpClient`/CRT em serviços de longa duração; sem HTTP clients duplicados no classpath.
- Paginators para listagens; traduza `AwsServiceException`/`SdkClientException` para exceptions de domínio.
- LocalStack + Testcontainers com credenciais falsas; nunca testar contra a conta real.
- **Sem Lombok** — deliberado.
