---
name: service-communication
description: Comunicação síncrona entre microsserviços — REST × gRPC × mensageria, RestClient e @HttpExchange, timeouts obrigatórios, tradução de erros (ACL), descoberta sem Eureka, conexões longas, autenticação serviço-a-serviço (client credentials, mTLS), service mesh, versionamento e anti-patterns. Use quando um serviço precisa chamar outro.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md), [`../microservices/SKILL.md`](../microservices/SKILL.md) e [`../resilience/SKILL.md`](../resilience/SKILL.md) (timeouts, retry, circuit breaker — **obrigatórios** em toda chamada de rede). Segurança: `aws-cognito`, `authentication`. Contratos: `contract-testing`.

# Comunicação síncrona entre serviços

Toda chamada de um serviço a outro é uma **chamada de rede**: pode **demorar, falhar ou ter resultado desconhecido**. Trate-a diferente de uma chamada de método. Esta skill cobre **como** chamar bem; **quando** chamar (versus publicar um evento) está em `microservices` e `messaging`.

## 1. REST, gRPC ou mensageria?

| Necessidade | Escolha |
|---|---|
| Preciso da **resposta agora** para continuar; recurso-orientado; clientes diversos (inclui browser/parceiros) | **REST/JSON** (o padrão) |
| **Interno**, baixa latência/alto volume, contrato forte e tipado, **streaming**, vários idiomas | **gRPC** |
| **Notificar** um fato, desacoplar no tempo, fan-out, picos | **Eventos/mensagens** (`messaging`) |
| Operação **longa** (minutos) | Aceite `202 Accepted` + status/callback, ou comando por fila — não segure a conexão HTTP |
| Transação entre vários serviços | **Saga** (`saga-pattern`) |

**Regra:** síncrono só para o que **exige resposta imediata**. Cada chamada síncrona acopla **disponibilidade e latência**: com A→B→C, a disponibilidade é o **produto** das três e a latência é a **soma**. Não faça cadeias.

---

## 2. REST: `RestClient` e HTTP interfaces

O **`RestClient`** (Spring 6.1+; substitui o `RestTemplate` para código novo) é síncrono, fluente e funciona com **virtual threads** (`java-modern-features`). Para um client **declarativo**, use uma **interface HTTP** (`@HttpExchange`) — o Spring gera a implementação.

```java
@HttpExchange("/api/book/v1")
public interface CatalogClient {

    @GetExchange("/{id}")
    BookResponse findById(@PathVariable("id") Long id);
}
```
```java
public record BookResponse(Long id, String title, boolean available) {}
```
**O DTO do client é seu**, na pasta do **consumidor** — **não** reaproveite o DTO/entity do serviço dono (acoplaria os dois; veja a regra de bibliotecas compartilhadas abaixo). Declare **só os campos que você usa** (**tolerant reader**: o Jackson 3 ignora campos desconhecidos por padrão — `web-config`): assim o provedor pode **adicionar** campos sem quebrar você (`contract-testing`).

```java
@Configuration
public class CatalogClientConfig {

    @Bean
    CatalogClient catalogClient(RestClient.Builder builder, @Value("${app.clients.catalog.url}") String baseUrl) {
        var httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(2))
                .build();
        var requestFactory = new JdkClientHttpRequestFactory(httpClient);
        requestFactory.setReadTimeout(Duration.ofSeconds(3));

        var restClient = builder
                .baseUrl(baseUrl)
                .requestFactory(requestFactory)
                .build();

        return HttpServiceProxyFactory
                .builderFor(RestClientAdapter.create(restClient))
                .build()
                .createClient(CatalogClient.class);
    }
}
```
- **Injete o `RestClient.Builder` do Spring** (nunca `RestClient.create()`/`new`): é ele que carrega a **instrumentação do Micrometer** que **propaga o `traceId`** nas chamadas (`observability`, `aws-observability`) — sem isso, o trace "morre" no primeiro hop.
- **Timeouts de conexão E de leitura: sempre.** O default é **infinito** em vários clients: um serviço lento seguraria a thread/conexão para sempre e esgotaria seu pool (`jvm-performance`, `resilience`). Valores típicos: conexão 1–2 s; leitura = ~p99 do downstream + margem.
- **URL base por configuração** (`app.clients.catalog.url`), nunca hardcoded: `http://library-catalog:8080` (nome do Service do Kubernetes — seção 4).
- **Pool de conexões / keep-alive:** o client JDK reutiliza conexões HTTP/1.1 e HTTP/2; para controle fino de pool use o `HttpComponentsClientHttpRequestFactory` (Apache). Reutilize **um** client por destino.

### Traduza erros — o ACL na prática

O **domínio não deve ver** `HttpClientErrorException` nem o formato de erro do outro serviço. Encapsule o client em um **adapter** que **traduz** para **exceptions e tipos do seu domínio** (o **Anti-Corruption Layer** de `ddd-hexagonal`), e é onde ficam `resilience`:
```java
@Component
public class CatalogGateway implements BookCatalog {

    private final CatalogClient client;

    public CatalogGateway(CatalogClient client) {
        this.client = client;
    }

    @Override
    public boolean isAvailable(BookId id) {
        try {
            return client.findById(id.value()).available();
        } catch (HttpClientErrorException.NotFound e) {
            throw new BookNotFoundException(id);
        } catch (HttpServerErrorException | ResourceAccessException e) {
            throw new CatalogUnavailableException("Catalog service unavailable", e);
        }
    }
}
```
- `404` (`NotFound`) é **resultado de negócio**, não falha técnica → exception de domínio (e **não** deve abrir o circuit breaker — `resilience`).
- `5xx` e `ResourceAccessException` (timeout/conexão recusada) são **falha técnica** → `...UnavailableException`, que o `@ControllerAdvice` converte em **`503`** com mensagem clara (`exception-handling`) — **nunca** `500` com stack trace do outro serviço, e **nunca vaze** o corpo de erro do downstream ao client final.
- Nunca engula a falha e devolva "dados vazios" como se tudo estivesse bem, a menos que haja um **fallback decidido e seguro** (`resilience`).

---

## 3. Autenticação serviço-a-serviço (zero trust)

**A rede interna NÃO é confiável.** Um pod comprometido, uma NetworkPolicy ausente ou um erro de roteamento expõe tudo se os serviços "confiam" em quem fala com eles. **Todo serviço autentica o chamador e autoriza com menor privilégio.**

| Cenário | Mecanismo |
|---|---|
| **Em nome do usuário** (a chamada é consequência de uma ação dele) | **Propague o JWT do usuário** (*token relay*): o downstream valida e autoriza como **aquele usuário** (preserva o dono do recurso — IDOR) |
| **Serviço por conta própria** (job, evento, sistema) | **OAuth2 Client Credentials**: o serviço obtém um token **próprio**, com **scopes** mínimos (`library/read`), do IdP (Cognito *resource server* + app client M2M — `aws-cognito`) |
| **Identidade de workload / criptografia** em trânsito | **mTLS** (service mesh, ou certificados por workload) — autentica o **serviço** na camada de transporte |
| Recursos **AWS** | **IAM** (IRSA/task role — `aws-sdk-java`); nunca chaves |

**Client Credentials com Spring Security** (token do serviço, cacheado e renovado automaticamente):
```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          catalog:
            provider: cognito
            authorization-grant-type: client_credentials
            client-id: ${CATALOG_CLIENT_ID}
            client-secret: ${CATALOG_CLIENT_SECRET}
            scope: library/read
        provider:
          cognito:
            token-uri: https://${COGNITO_DOMAIN}.auth.${AWS_REGION}.amazoncognito.com/oauth2/token
```
O `client-secret` vem de **Secret/Secrets Manager** (`aws-rds-secrets-manager`, `kubernetes`), **nunca** do Git. No `RestClient`, um **interceptor** do Spring Security (`OAuth2ClientHttpRequestInterceptor`, a partir do Spring Security 6.4) anexa o `Authorization: Bearer ...` — **confirme a API e a configuração exatas na versão resolvida**. **Scopes mínimos por cliente** e *resource server* por serviço (`SCOPE_library/read` no downstream — `aws-cognito`).

**Nunca** confie em um header `X-User-Id` "porque veio do gateway" (`api-gateway`, defesa em profundidade). Combine com **NetworkPolicy** (`kubernetes`): o serviço só aceita tráfego dos chamadores autorizados.

---

## 4. Descoberta de serviços e balanceamento

**Em Kubernetes e ECS você não precisa de Eureka/Consul.** A plataforma já resolve:
- **Kubernetes:** o **Service** dá um **nome DNS estável** (`http://library-catalog:8080` no mesmo namespace, ou `library-catalog.library.svc.cluster.local`) e balanceia entre os pods *ready*. A "descoberta" é só configurar o nome.
- **ECS:** **Service Connect** (ou **Cloud Map**/DNS) dá nomes e balanceamento, com *retries* e métricas entre serviços (`aws-ecs-fargate`).
- **Eureka/Consul/Spring Cloud LoadBalancer + Discovery** só fazem sentido **fora** dessas plataformas (VMs, ambientes legados). Não instale um registry em cima do Kubernetes: é uma peça a mais para operar sem ganho.
- **Spring Cloud Kubernetes** (ler ConfigMaps/descoberta pela API) é **opcional**: `ConfigMap` por variável de ambiente (`kubernetes`) já resolve a configuração sem acoplar o código ao cluster.

**Balanceamento — a armadilha das conexões longas:** o `kube-proxy` balanceia **por conexão** (L4). Com **HTTP keep-alive/HTTP2/gRPC**, o client abre **poucas conexões longas** e todo o tráfego pode grudar em **um pod** (e os pods novos do HPA ficam **ociosos**). Soluções: **Service headless** + balanceamento no client; **proxy L7** (Envoy/mesh); fechar conexões periodicamente (`max-connection-age`). Para HTTP/1.1 com pool, o efeito é menor, mas **monitore a distribuição de carga** entre pods.

---

## 5. gRPC (quando faz sentido)

Use para **chamadas internas de alto volume/latência baixa**, contratos fortes (Protocol Buffers) e **streaming**. Custos: curva de aprendizado, ferramentas (não é `curl`-friendly), **browser exige gRPC-Web**/gateway, balanceamento L7 (seção 4). O Spring tem o projeto **Spring gRPC** — confirme a versão/starter compatível com o Boot do projeto.
```protobuf
syntax = "proto3";

package library.catalog.v1;

service CatalogService {
  rpc GetBook (GetBookRequest) returns (BookReply);
}

message GetBookRequest {
  int64 id = 1;
}

message BookReply {
  int64 id = 1;
  string title = 2;
  bool available = 3;
  reserved 4;
}
```
**Regras de evolução do `.proto` (compatibilidade):** **nunca reutilize nem mude o número** de um campo; **adicione** campos novos com **número novo**; ao remover, marque `reserved`; mantenha o **pacote versionado** (`v1`). **Sempre defina *deadlines*** nas chamadas (o gRPC os propaga na cadeia — o equivalente ao timeout). Autenticação por **mTLS** ou token em *metadata*. Guarde os `.proto` em **repositório/artefato próprio e versionado** (é o contrato — `contract-testing`).

---

## 6. Resiliência e orçamento de tempo

Toda chamada de saída tem: **timeout** (seção 2), **retry limitado e só para operações idempotentes** (`idempotency`), **circuit breaker** e **bulkhead** (`resilience`). Conceitos que importam aqui:
- **Orçamento de timeout:** o timeout do chamador **tem que ser maior** que o do downstream (+ margem), e o de **cada hop** menor que o do anterior; senão o chamador desiste enquanto o downstream ainda trabalha (trabalho desperdiçado e retries sobre trabalho em curso). Em cadeias, propague um **deadline** (gRPC faz; em HTTP, um header próprio).
- **Retries multiplicam:** 3 retries em 3 camadas = 27 chamadas. **Retente em um só lugar** (normalmente o mais próximo do cliente final/da borda) — `resilience`.
- **Degrade em vez de falhar** quando há alternativa segura (cache, dado antigo marcado como tal); **falhe rápido** quando não há (não inventar a resposta de uma decisão financeira).

---

## 7. Service mesh — quando vale

Um **service mesh** (Istio, Linkerd) coloca um **proxy sidecar** (ou, no modo *ambient* do Istio, proxies por nó) ao lado de cada pod e dá, **fora do código**: **mTLS automático** entre serviços, **retries/timeouts/circuit breaking** por configuração, **traffic splitting** (canary), **observabilidade** uniforme (métricas/traces L7) e políticas de autorização por serviço.

| Vale quando | Não vale quando |
|---|---|
| **Muitos serviços** e exigência de **mTLS/zero trust uniforme** | Poucos serviços — **bibliotecas** (`resilience`) + NetworkPolicy bastam |
| Equipes poliglotas (resiliência fora da linguagem) | A equipe não tem capacidade de operar a malha |
| Precisa de canary/traffic shifting fino e telemetria L7 padronizada | Sensível à latência/memória adicionais do proxy |

Custos: **complexidade operacional**, consumo de CPU/memória por pod, mais um sistema para atualizar/depurar. **Não** adote por reflexo. Na AWS: o **AWS App Mesh teve o fim de suporte anunciado** — **confirme o status atual** e prefira **ECS Service Connect** (no ECS) ou **Istio/Linkerd** (no EKS) para projetos novos. O mesh cuida do tráfego **leste-oeste**; o **gateway** (`api-gateway`) cuida do **norte-sul** (entrada).

---

## 8. Versionamento e compatibilidade de API

- **Mudanças aditivas** na versão corrente: **adicionar** campo opcional/endpoint; **nunca** remover/renomear campo, mudar tipo ou semântica. Consumers **toleram campos desconhecidos** (tolerant reader).
- **Quebra de contrato = nova versão** (`/api/book/v2`) com **convivência** e **deprecação com prazo** (headers `Deprecation`/`Sunset`); a skill `api-versioning` cobre a convivência entre versões e o versionamento nativo do Spring 7.
- **Contract tests** (`contract-testing`) são o que impede o provedor de quebrar um consumidor sem perceber; **detecte breaking changes do OpenAPI no CI** (`springdoc` + ferramentas como `oasdiff`) antes do merge.
- **Idempotência:** operações que o client pode repetir (por retry/timeout) exigem `Idempotency-Key` (`idempotency`).
- **Paginação** sempre em coleções; **limites de payload**; **códigos HTTP corretos** (`4xx` do client, `5xx` do servidor) e o formato de erro padrão (`ExceptionResponse`/`ProblemDetail` — `exception-handling`).

---

## 9. Anti-patterns

- **Cadeias síncronas profundas** (A→B→C→D): disponibilidade multiplicada, latência somada, falha em cascata.
- **Chamada de rede dentro de loop** (N+1 entre serviços): faça **uma** chamada em lote (`/books?ids=1,2,3`) ou replique o dado por eventos (`cqrs-event-sourcing`).
- **Chamada de rede dentro de uma `@Transactional`** do banco: segura a conexão durante a espera (`jvm-performance`) e não há atomicidade entre os dois sistemas.
- **Sem timeout** (ou o default infinito) — o erro mais comum e mais caro.
- **Biblioteca "client" compartilhada** com DTOs/regra de negócio: acopla versões e força redeploy em bloco (*distributed monolith* — `microservices`). Compartilhe **contratos** (OpenAPI/`.proto`) e **gere** os clients, ou cada consumidor mantém o seu DTO enxuto.
- **Reusar a entity/DTO do serviço dono** no consumidor.
- **Descoberta com registry** em cima do Kubernetes.
- **Confiar na rede interna** (sem auth serviço-a-serviço) e em headers de identidade forjáveis.
- **Retry de operação não idempotente**; **retry em todas as camadas**.
- **Engolir o erro** do downstream e seguir com dado vazio.
- **Acoplar o consumidor ao formato de erro** do provedor (vazá-lo ao client final).

## 10. Testes

- **Unit:** o adapter (`CatalogGateway`) com o `CatalogClient` mockado: 404 → exceção de domínio; `ResourceAccessException` → `...UnavailableException` (`testing`).
- **Integração do client:** **WireMock** (ou `MockRestServiceServer`) simulando o downstream: sucesso, 404, 500, **resposta lenta** (timeout dispara), corpo com campo extra (tolerant reader), conexão recusada.
- **Contrato:** consumer-driven contracts garantem que o provedor continua atendendo o que você usa (`contract-testing`).
- **Falhas:** teste que, com o downstream fora/lento, o **circuit breaker abre** e o **fallback/erro 503** acontece (`resilience`).
- **Segurança:** chamada **sem token** ou com **scope insuficiente** → `401/403` no downstream.

---

## Regras principais

- **Síncrono só para resposta imediata**; eventos para propagar fatos; **sem cadeias**, sem chamada de rede em loop nem dentro de `@Transactional`.
- **`RestClient`** (builder injetado, para propagar o `traceId`) + **HTTP interface** `@HttpExchange`; **timeouts de conexão e leitura sempre**; URL por configuração.
- **DTO próprio do consumidor** (só os campos usados, tolerant reader); **adapter/ACL** traduz erros para exceptions de domínio (`404` ≠ falha técnica; `5xx`/timeout → `503`); nunca vaze o erro do downstream.
- **Zero trust:** autentique serviço-a-serviço — JWT do usuário (token relay) ou **client credentials com scopes mínimos**; mTLS/NetworkPolicy; **nunca** confie em header de identidade ou na rede interna; segredos fora do Git.
- **Descoberta = DNS do Service / ECS Service Connect**; sem Eureka no Kubernetes; atenção ao **balanceamento com conexões longas** (HTTP/2, gRPC).
- **gRPC** para interno de alto volume/streaming, com **deadlines** e regras de evolução do `.proto`; **service mesh** só com muitos serviços e capacidade de operar (confirme o status do App Mesh).
- **Orçamento de timeout** coerente entre os hops; **retry só idempotente e em um só lugar**; degrade quando seguro, falhe rápido quando não.
- API **aditiva**, versionada, com deprecação; **contract tests** + detecção de breaking change do OpenAPI no CI; `Idempotency-Key` em operações repetíveis.
- Bibliotecas compartilhadas **só com contratos**, nunca regra de negócio.
- **Sem Lombok** — deliberado.
