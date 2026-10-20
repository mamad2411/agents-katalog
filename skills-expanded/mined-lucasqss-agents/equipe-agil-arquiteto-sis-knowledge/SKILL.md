---
name: equipe-agil-arquiteto-sis-knowledge
description: Conhecimento específico do Arquiteto de Sistema (Tech Anchor Sis) da Equipe Backend Ágil Kanban+XP. Cobre design inter-aplicação em Java 21 + Quarkus 3 — decisão monolito vs microsserviços (Newman), DDD estratégico (Bounded Context, Context Mapping), Enterprise Integration Patterns (Hohpe & Woolf), API styles (REST/GraphQL/gRPC/AsyncAPI), resilience patterns (Nygard — Timeout/Retry/Circuit Breaker/Bulkhead/Back-Pressure/Fallback) implementados via SmallRye Fault Tolerance, consistência distribuída (CAP/PACELC, Kleppmann), Sagas/Outbox/Inbox/CDC (Debezium), Event-Driven (Notification/State Transfer/Sourcing/CQRS), streaming com Kafka via SmallRye Reactive Messaging, observabilidade distribuída (OpenTelemetry), deployment patterns (Blue/Green, Canary, Shadow), migration patterns (Strangler Fig, Branch by Abstraction, Parallel Run), Data Mesh e arquitetura sociotécnica (Conway, Team Topologies). Invoque para decisões que cruzam fronteira de processo. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Arquiteto de Sistema (Tech Anchor Sis) — Conhecimento específico

Skill carregada pelo agente `equipe-agil-arquiteto-sis` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method` + `equipe-agil-arquitetura-base`. Cobre o conhecimento de **arquitetura distribuída** que opera no nível inter-aplicação. Tudo intra-aplicação vive em `equipe-agil-arquiteto-app-knowledge`.

## 1. Conceitos centrais

### 1.1 Mandato do Arquiteto Sis na equipe

- **Dono das decisões entre deployables**: granularidade de serviço, contratos inter-serviço (com C do API Designer), estilo de integração (síncrono vs assíncrono), modelo de dados distribuído, resiliência, observabilidade distribuída, deployment.
- Produz **ADRs** vinculadas a **ASRs** com **fitness functions** (vide `equipe-agil-arquitetura-base`).
- **Não decide** design interno de cada serviço (Arquiteto App) nem implementação local (Tech Lead).
- RACI: A/R em decisões inter-serviço; C em contratos de API e em decisões intra-app que tenham impacto sistêmico.

### 1.2 Stack default

- **Java 21 + Quarkus 3** (mesmo da Arquiteto App, mas foco em **integração** e **deploy**).
- **Mensageria**: SmallRye Reactive Messaging (conectores Kafka, AMQP, Pulsar).
- **REST client**: MicroProfile REST Client (síncrono) e Mutiny/Uni para reativo.
- **Resiliência**: SmallRye Fault Tolerance (`@Timeout`, `@Retry`, `@CircuitBreaker`, `@Bulkhead`, `@Fallback`).
- **Observabilidade**: SmallRye OpenTelemetry (traces, metrics, logs correlacionados).
- **CDC**: Debezium (Postgres/MySQL/Oracle) → Kafka.
- **Service mesh**: Istio/Linkerd (opcional, decisão organizacional).

### 1.3 Monólito vs microsserviços — decisão (Newman — *Building Microservices*, *Monolith to Microservices*)

**Newman alerta**: microsserviços **não são default**. Default sensato é **monolito modular** bem feito (vide `arquiteto-app-knowledge` — Modular Monolith).

**Razões legítimas para extrair serviço**:
1. **Escala independente** (parte do sistema precisa de 10× recursos).
2. **Time independente** (lei de Conway — time autônomo com ciclo de release próprio).
3. **Tecnologia diferente** (uma parte se beneficia de stack distinta).
4. **Falha isolada** (blast radius — uma falha não pode derrubar o resto).
5. **Sensibilidade de dados** (regulatório — isolar dado pessoal/financeiro).
6. **Cadência de mudança radicalmente diferente** (legado estável + parte experimental).

**Custos de microsserviços**:
- Complexidade distribuída (rede falha, latência, parcial).
- Consistência eventual obrigatória entre fronteiras.
- Observabilidade distribuída obrigatória.
- Pipeline e plataforma maduras (CI/CD, IaC, secrets).
- Capacidade ops 24/7.

**Anti-padrão**: *distributed monolith* — serviços separados mas acoplados (deploy junto, dado compartilhado, contratos frágeis). Pior dos dois mundos.

### 1.4 DDD estratégico (Evans + Vernon — *Implementing DDD*)

- **Bounded Context (BC)**: fronteira linguística e de modelo; mesma palavra pode ter significados diferentes em BCs diferentes (ex.: "Cliente" em Vendas vs Cobrança).
- **Context Map**: relações entre BCs:
  - *Partnership* — dois times alinhados, sucesso/falha conjuntos.
  - *Shared Kernel* — modelo compartilhado pequeno (perigoso, alto acoplamento).
  - *Customer-Supplier* — upstream serve downstream, downstream tem voz.
  - *Conformist* — downstream aceita o modelo upstream sem voz (legado/SaaS).
  - *Anticorruption Layer (ACL)* — downstream traduz para se proteger de modelo ruim upstream.
  - *Open Host Service (OHS)* — upstream oferece protocolo estável documentado.
  - *Published Language* — schema/vocabulário publicado entre múltiplos consumidores.
  - *Separate Ways* — sem integração; resolva manualmente.
  - *Big Ball of Mud* — área legada sem fronteira; isolar com ACL.
- **Heurística**: 1 BC = 1 serviço **é uma escolha**, não regra. Vários BCs podem viver no mesmo deployable (modular monolith) quando o custo de separar não compensa.

### 1.5 Enterprise Integration Patterns (Hohpe & Woolf)

**Quatro estilos de integração**:
1. **File transfer** — bom para batch grande; ruim para tempo real.
2. **Shared database** — anti-padrão para sistemas autônomos; alto acoplamento.
3. **Remote Procedure Invocation (RPI)** — síncrono; REST, gRPC. Acoplamento temporal forte.
4. **Messaging** — assíncrono via canal; broker. Desacoplamento temporal; complexidade extra.

**Padrões essenciais (catálogo curto)**:
- **Message Channel** — fila/tópico.
- **Point-to-Point Channel** — uma mensagem, um consumidor.
- **Publish-Subscribe** — uma mensagem, N consumidores.
- **Message Router** — direciona por conteúdo (content-based router).
- **Message Translator** — traduz schemas (≈ ACL em forma de mensagem).
- **Message Filter** — descarta mensagens irrelevantes.
- **Aggregator** — agrupa mensagens correlacionadas em uma só.
- **Splitter** — quebra mensagem em múltiplas.
- **Dead Letter Channel (DLQ)** — mensagens que falham repetidamente vão para inspeção.
- **Idempotent Receiver** — consumidor seguro contra entrega duplicada (at-least-once).
- **Correlation Identifier** — campo que rastreia fluxo cross-message.
- **Saga** — coordenação de longa duração (vide 1.10).

### 1.6 API styles — quando usar cada um

| Estilo | Quando usar | Custos |
|--------|-------------|--------|
| **REST + JSON** | Default para APIs públicas e entre times; ferramental maduro; cacheável HTTP | Verboso, sem contrato forte, N+1 fácil |
| **gRPC** | Inter-serviço interno; baixa latência; contratos fortes (protobuf); streaming bidirecional | Curva de aprendizado, ferramental menos universal, debug mais difícil |
| **GraphQL** | UI com muitas variações de payload; reduz over/under-fetching | Complexidade de servidor, N+1 escondido, cache complicado |
| **Async (AsyncAPI/Kafka)** | Eventos de domínio; integração fracamente acoplada; replay | Consistência eventual, ordem por partição apenas, complexidade ops |

**Default da equipe**: REST + OpenAPI para síncrono inter-serviço; Async (Kafka via SmallRye Reactive Messaging) com AsyncAPI para eventos. gRPC opcional para hops internos com forte requisito de latência.

### 1.7 Resilience Patterns (Nygard — *Release It!*)

Implementados em Quarkus via **SmallRye Fault Tolerance** + Mutiny:

- **Timeout** (`@Timeout`) — toda chamada remota tem timeout explícito; **sem default infinito**.
- **Retry** (`@Retry`) — apenas para falhas **transientes e idempotentes**; com **exponential backoff + jitter**; cap em N tentativas.
- **Circuit Breaker** (`@CircuitBreaker`) — quando taxa de falha > X% em janela, abre por T segundos; meio-aberto faz probing.
- **Bulkhead** (`@Bulkhead`) — isola pools de threads/conexões por dependência, evita esgotar tudo por causa de um lento.
- **Fallback** (`@Fallback`) — comportamento degradado quando dependência falha (cache, default, mensagem amigável).
- **Back-Pressure** — em fluxo reativo (Mutiny, SmallRye), consumidor sinaliza ritmo; evita afogamento.
- **Steady State** — código deve poder rodar para sempre sem vazar (limpar caches, conexões, threads).
- **Fail Fast** — preferível a "hang"; degrada rápido com mensagem clara.
- **Decoupling Middleware** — broker assíncrono entre serviços remove acoplamento temporal.
- **Handshaking & Health Checks** — `/q/health/live` (liveness) e `/q/health/ready` (readiness) via MicroProfile Health.

**Anti-padrões clássicos do *Release It!***:
- *Integration Points* sem timeout — propaga lentidão como cascata.
- *Chain Reactions* — falha em A esgota B esgota C.
- *Cascading Failures* — sem circuit breaker, falha se propaga.
- *Unbounded Result Sets* — `SELECT * FROM …` sem `LIMIT`.

### 1.8 Consistência distribuída (Kleppmann — *Designing Data-Intensive Applications*)

- **CAP**: na presença de partição (P), escolha entre C (consistência) e A (disponibilidade). Em sistemas reais, partições acontecem; é trade-off contínuo.
- **PACELC**: estende CAP — mesmo sem partição (Else), há trade-off entre Latência e Consistência.
- **Modelos de consistência** (do mais forte ao mais fraco):
  - *Linearizability* — operações parecem instantâneas, uma ordem global.
  - *Sequential consistency* — ordem por cliente preservada.
  - *Causal consistency* — operações causalmente ligadas têm ordem garantida.
  - *Eventual consistency* — convergem eventualmente; sem garantias temporais.
- **Replicação**:
  - *Single-leader* — escrita no líder, leitura em réplicas; simples; risco de leitura desatualizada.
  - *Multi-leader* — escrita em vários; conflitos a resolver (CRDTs, last-write-wins).
  - *Leaderless* — quorum (R + W > N) para consistência ajustável.
- **Particionamento (sharding)**: por intervalo de chave (range) ou hash. Cuidado com *hot partitions*.
- **Idempotência** é obrigatória em qualquer protocolo *at-least-once* (Kafka, retry, webhook). Sem ela, retry duplica efeito.

### 1.9 Two-phase commit é (quase sempre) errado

Em sistemas distribuídos modernos, 2PC tem custo de disponibilidade e latência inaceitável. **Use sagas** (1.10) + idempotência + reconciliação eventual.

### 1.10 Sagas — coordenação de longa duração

Duas formas:
- **Saga coreografada** — cada serviço escuta evento e dispara o próximo; sem coordenador central; baixo acoplamento, mas fluxo difícil de visualizar.
- **Saga orquestrada** — um orquestrador (Camunda, Temporal, ou serviço custom) chama cada passo; mais visível; risco de ficar god service.

**Cada passo precisa de compensação** (operação inversa para *rollback* lógico). Compensação **não desfaz** efeitos colaterais (e-mail enviado), apenas compensa (e-mail de cancelamento).

**Anti-padrões**:
- Saga sem compensação documentada — vazamento de estado inconsistente.
- Saga coreografada sem desenho — ninguém entende o fluxo.
- Misturar saga com transação local — falsa sensação de atomicidade.

### 1.11 Outbox Pattern, Inbox Pattern, CDC (Debezium)

**Problema**: como garantir que "salvei no banco" **e** "publiquei evento" são atômicos? Não dá para fazer 2PC entre banco + Kafka.

**Outbox Pattern**:
1. Na mesma transação local, escreve no estado de domínio **e** numa tabela `outbox` (mesmo banco, mesma transação).
2. Processo separado (relay) lê `outbox` e publica em Kafka, depois marca como enviada.
3. Atomicidade garantida pelo banco; publicação eventual.

**Implementação preferida**: **Debezium** lendo o WAL do Postgres → publica direto em Kafka. Não precisa de relay custom.

**Inbox Pattern (dedup no consumidor)**:
1. Consumidor recebe mensagem com `messageId` (correlation).
2. Tabela `inbox` registra `messageId` processado.
3. Antes de processar, checa: já está em `inbox`? Ignora (idempotência ao nível do receptor).

### 1.12 Event-Driven — quatro tipos (Fowler)

1. **Event Notification** — "algo aconteceu, vá buscar o resto" (mensagem fina). Baixo acoplamento, mas chatty.
2. **Event-Carried State Transfer** — evento traz todo o estado relevante; consumidor não precisa chamar de volta.
3. **Event Sourcing** — estado é derivado do log de eventos (não armazenado diretamente); replay reconstrói. Complexo, mas auditável e flexível.
4. **CQRS** — comandos e queries separados em modelos distintos; geralmente combinado com event sourcing. Útil quando leitura/escrita têm requisitos opostos.

**Heurística**: comece com Event Notification + Event-Carried State Transfer. Event Sourcing e CQRS são caros — adote apenas com ASR/risco que justifique.

### 1.13 Streaming com Kafka via SmallRye Reactive Messaging

- Quarkus integra Kafka via `quarkus-smallrye-reactive-messaging-kafka`.
- `@Incoming("topico-x")` consome; `@Outgoing("topico-y")` produz; `@Channel` para fluxo programático.
- **Schema registry** (Avro/Protobuf/JSON Schema) é mandatório em ambiente compartilhado — versionamento e evolução de schema (forward/backward compatible).
- **Particionamento**: chave determina partição; ordem garantida **dentro** da partição. Escolha de chave é decisão arquitetural (afeta paralelismo e ordem).
- **Offsets**: auto-commit é arriscado; preferir commit manual após processamento bem-sucedido.
- **Consumer groups**: paralelismo = mín(partições, instâncias).
- **DLQ**: configurar tópico de dead letter para mensagens *poison* (que repetem falha).

### 1.14 Observabilidade distribuída

- **Three pillars**: logs estruturados, métricas, traces.
- **OpenTelemetry** (em Quarkus via `quarkus-smallrye-opentelemetry`) — padrão de fato; exportar para Tempo/Jaeger (traces), Prometheus (metrics), Loki (logs).
- **Correlation ID / trace ID** propagado em todo hop (HTTP header `traceparent`, Kafka header).
- **Golden signals** (Google SRE) — latency, traffic, errors, saturation — coletados por serviço.
- **Cardinalidade**: cuidado com labels de métricas (user_id, request_id são alta cardinalidade — vão para traces/logs, **não para métricas**).

### 1.15 Deployment patterns

- **Blue/Green** — duas pilhas idênticas; tráfego comuta inteiro; rollback rápido; custo de infra 2×.
- **Canary** — pequena fração do tráfego (1%, 10%, 50%) recebe a nova versão; observa golden signals; promove se saudável.
- **Rolling** — pods substituídos um a um; padrão Kubernetes; sem queda mas exposição parcial à versão nova.
- **Shadow / Dark Launch** — tráfego espelhado para nova versão **sem** servir resposta ao cliente; valida comportamento sob carga real.
- **Feature flags** — desacopla deploy de release (vide `xp-baseline`).

### 1.16 Migration patterns (Fowler, Newman)

- **Strangler Fig** — sistema novo cresce ao redor do legado; rotas migradas uma a uma; legado é desligado quando todas migram.
- **Branch by Abstraction** — introduz abstração que aponta para velho ou novo; troca o backend da abstração; integra continuamente. Vive **dentro** da `feature/*` (vide `xp-baseline`).
- **Parallel Run** — roda velho e novo lado a lado para o mesmo input; compara saídas; descobre divergência antes do switch.
- **Decorating Collaborator** — proxy/decorador intercepta chamadas e adiciona/desvia comportamento sem mudar o cliente.

### 1.17 Data Mesh (Dehghani) — princípios

1. **Domain ownership of data** — cada bounded context é dono dos seus dados, inclusive analíticos.
2. **Data as a product** — dataset é produto com SLO, contrato, descoberta.
3. **Self-serve data platform** — plataforma horizontal para criar/gerir data products.
4. **Federated computational governance** — políticas globais (privacidade, qualidade) automatizadas, locais autônomas.

Útil quando o data lake monolítico vira gargalo. Implica investimento em plataforma e cultura. Não é solução técnica, é organizacional.

### 1.18 Data on the inside vs outside (Helland)

- *Data on the inside* — dado mutável dentro do serviço, com identidade transacional.
- *Data on the outside* — dado **imutável** que cruza fronteiras (eventos, snapshots, mensagens). Tem ID e versão; nunca muda em retrospecto.

Implica: contratos entre serviços trocam **dados externos** (imutáveis, versionados), não modelos internos.

### 1.19 Arquitetura sociotécnica — Conway invertido + Team Topologies (Skelton & Pais)

- **Lei de Conway**: arquitetura espelha estrutura de comunicação da organização.
- **Conway invertido**: desenhar **a organização** para que ela espelhe a arquitetura desejada.
- **Quatro tipos de time** (Team Topologies):
  - *Stream-aligned* — entrega valor end-to-end num fluxo (default).
  - *Enabling* — coach que aumenta capacidade de stream-aligned por tempo limitado.
  - *Complicated subsystem* — especialista (ex.: algoritmo de risco).
  - *Platform* — oferece serviços a stream-aligned (golden path, paved road).
- **Três modos de interação**: collaboration (alto contato, descoberta), X-as-a-Service (consumo claro), facilitating (enabling temporário).
- Implica: granularidade de serviço **e** topologia de times se influenciam — Arquiteto Sis precisa pensar nas duas.

### 1.20 Estilos arquiteturais distribuídos — vocabulário

- **Service-Based** — serviços coarse-grained compartilhando banco; menos custo que microsserviços; bom degrau intermediário.
- **Microservices** — serviços fine-grained, dado próprio, deploy independente.
- **Event-Driven** — fluxo coreografado por eventos; alta autonomia, complexidade de tracing.
- **Space-Based** — replicação em memória + processamento próximo do dado; alta escala (ex.: trading).
- **Serverless** — funções por evento; bom para spikes esporádicos; cuidado com cold start e vendor lock-in.

Escolha do estilo é ADR top-level com ASR/risco como justificativa.

## 2. Práticas e heurísticas operacionais

### 2.1 Decisão "extrair serviço ou continuar no modular monolith?"

Perguntas (todas precisam de "sim" forte para extrair):
- Existe ASR de escala/falha/dado/cadência que **só** se resolve com fronteira de processo?
- Há time autônomo para operar o serviço 24/7?
- Plataforma (CI/CD, observabilidade, secrets, k8s) suporta sem fricção?
- Custo de coerência distribuída é menor que o custo atual do acoplamento intra-app?

Se < 3 "sim" forte: **fique no modular monolith** e atue na fronteira interna (módulo + ArchUnit) — vide `arquiteto-app-knowledge`.

### 2.2 Contrato entre serviços — checklist

- [ ] Esquema versionado (OpenAPI/AsyncAPI/Protobuf) em repo do produtor.
- [ ] Compatibilidade (backward para consumidor, forward para produtor) declarada.
- [ ] Idempotência garantida (chave de idempotência ou Inbox).
- [ ] Política de timeout/retry/circuit breaker explícita no consumidor.
- [ ] Eventos imutáveis (data on the outside) — sem referenciar entidades mutáveis internas do produtor.
- [ ] Contract test (Pact ou equivalente) no pipeline de **ambos** os lados.
- [ ] Deprecação tem janela mínima documentada (ex.: 90 dias).

### 2.3 Escolha síncrono vs assíncrono

- **Síncrono (REST/gRPC)** quando o cliente **precisa** da resposta para continuar e a operação é rápida (< 1s típico).
- **Assíncrono (mensageria)** quando:
  - Cliente não bloqueia esperando.
  - Operação é longa ou variável.
  - Múltiplos consumidores se interessam pelo evento.
  - Acoplamento temporal precisa ser quebrado.
- Mistura controlada é normal: API REST que enfileira comando e responde 202 Accepted com link para polling/SSE.

### 2.4 Resiliência — defaults seguros para a equipe

```java
@ApplicationScoped
public class ServicoExternoClient {

    @Timeout(value = 2, unit = ChronoUnit.SECONDS)
    @Retry(maxRetries = 3, delay = 200, jitter = 100, retryOn = TransientException.class)
    @CircuitBreaker(requestVolumeThreshold = 20, failureRatio = 0.5, delay = 5000)
    @Bulkhead(value = 10)
    @Fallback(fallbackMethod = "respostaPadrao")
    public Resposta consultar(Pedido p) { /* … */ }

    Resposta respostaPadrao(Pedido p) { return Resposta.degradada(p); }
}
```

Toda chamada remota deve ter no mínimo `@Timeout`. Sem timeout = bug arquitetural.

### 2.5 Esquema de evento — recomendação

```json
{
  "specversion": "1.0",
  "type": "br.com.exemplo.cliente.cadastrado.v1",
  "source": "/cadastro-clientes",
  "id": "uuid-único",
  "time": "2026-05-23T10:00:00Z",
  "datacontenttype": "application/json",
  "data": { "clienteId": "...", "...": "..." }
}
```

Formato CloudEvents é base padrão; metadata fora do `data` permite roteamento sem decodificar payload.

### 2.6 Quando NÃO usar mensageria

- Operação **CRUD simples** sob baixo volume — REST resolve com menos custo.
- Equipe sem operação de broker estável — adicionar Kafka sem time-platform é dívida garantida.
- Latência fim-a-fim < 100ms obrigatória e síncrona — broker adiciona hops.

### 2.7 Anti-padrões inter-serviço comuns

- ❌ **Distributed monolith** — serviços que precisam ser deployados juntos.
- ❌ **Shared database** entre microsserviços — acoplamento por dado.
- ❌ **Chamada síncrona em cadeia profunda** (A → B → C → D) — latência somada + falha multiplicada.
- ❌ **Saga sem compensação** — vazamento eventual.
- ❌ **2PC entre microsserviços** — disponibilidade explode.
- ❌ **Evento como RPC** ("solicitação enviada") — não é evento de domínio, é comando travestido.
- ❌ **God orchestrator** — uma saga orquestrada que sabe tudo.
- ❌ **At-most-once "por simplicidade"** — perda silenciosa.
- ❌ **Sem timeout** em chamada HTTP — vazamento de thread sob lentidão da dependência.

### 2.8 Colaboração com outros papéis

- **API Designer** (RACI A/R em contrato API) — contratos REST/AsyncAPI são responsabilidade dele, Arquiteto Sis é C.
- **Arquiteto App** — bounded context que vira serviço é fronteira compartilhada; decidir juntos (ASR-driven).
- **SRE** — SLO de cada serviço; observabilidade end-to-end.
- **AppSec** — fronteira de confiança nova (mTLS, OAuth2/OIDC, autz por escopo).
- **Data Engineer** — outbox, CDC, schema evolution, contratos de dataset (Data Mesh).
- **DevOps** — pipeline por serviço, IaC, deployment patterns.

## 3. Templates e checklists

### 3.1 Checklist "novo serviço — vale a pena?"

- [ ] ASR justifica fronteira de processo (escala/falha/dado/cadência/tecnologia)?
- [ ] Bounded context bem definido com ubiquitous language própria?
- [ ] Dono único (time stream-aligned ou platform)?
- [ ] Plataforma suporta (CI/CD, k8s, observabilidade, secrets, IaC)?
- [ ] Operação 24/7 garantida?
- [ ] Contrato API + eventos desenhados e validados com consumidores?
- [ ] Saga/Outbox/Inbox desenhados para fluxos cross-service?
- [ ] Estratégia de migração (Strangler Fig?) se substitui parte do legado?
- [ ] Deploy pattern escolhido (Blue/Green, Canary)?
- [ ] Resiliência default configurada (Timeout/Retry/CB/Bulkhead/Fallback)?
- [ ] Threat model atualizado com AppSec?

### 3.2 Template de ADR de extração de serviço

```markdown
# ADR-NNNN: Extrair <Bounded Context X> do <Modular Monolith Y> para serviço próprio

- Status: Accepted
- ASR: <ASR-id> — <métrica esperada, ex.: p95 < 500ms sob 5× carga atual>
- Risco motivador: <ex.: ponto único de falha, deploy emperrado>

## Contexto
Hoje o BC X vive como módulo dentro de Y. A pressão de <ASR> exige escala/falha/cadência independente.

## Decisão
Extrairemos X como serviço Quarkus separado, comunicação via:
- REST + OpenAPI para consultas síncronas
- Kafka + AsyncAPI para eventos `x.*.v1` (Event-Carried State Transfer)
Estratégia: Strangler Fig — rotas migram em N fases, com Branch by Abstraction no consumidor.

## Consequências
**Positivas**: deploy independente, escala independente, blast radius isolado.
**Negativas**: consistência eventual entre X e Y (Outbox + Debezium), latência inter-serviço, ops nova.

## Alternativas
- Manter no monolito (rejeitado — não atinge ASR).
- Service-Based compartilhando banco (rejeitado — perpetua acoplamento).

## Fitness functions
- Contract test (Pact) entre X e seus consumidores no CI.
- SLO p95 < 500ms validado em smoke perf.
- Schema compatibility check no CI (forward+backward).
- Sem chamada síncrona X→Y (ArchUnit + análise de dependência).
```

### 3.3 Receita rápida — Outbox + Debezium

```
1. Tabela `outbox` no mesmo schema do agregado:
   id (uuid) | aggregate_type | aggregate_id | event_type | payload (jsonb) | created_at

2. Aplicação grava na transação local: agregado + linha em outbox.

3. Debezium configurado para capturar `outbox` (signal table outbox-event-router).

4. Debezium publica em Kafka tópico derivado de `aggregate_type`.

5. Após captura, linha de outbox pode ser deletada por job de limpeza (TTL).

6. Consumidor usa `Inbox` (dedup por event id) para garantir idempotência.
```

### 3.4 Checklist de readiness operacional de um serviço

- [ ] `/q/health/live` e `/q/health/ready` implementados.
- [ ] `/q/metrics` (Prometheus) expõe golden signals.
- [ ] Traces OpenTelemetry exportados.
- [ ] Logs estruturados JSON com `trace_id`.
- [ ] Dashboard no Grafana (latência, throughput, erros, saturation).
- [ ] Alertas SLO-based (burn rate).
- [ ] Runbook para os top-5 alertas.
- [ ] Game day / chaos test inicial executado.
- [ ] Limites de recurso (CPU/memória) definidos (não infinitos).

### 3.5 Quando escalar ao Eng Coach

- Persistir desacordo com Arquiteto App sobre fronteira de bounded context.
- Time sem capacidade técnica para operar saga/outbox/CDC sem treino.
- Pressão de stakeholder para "fazer microsserviços" sem ASR.

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-arquiteto-sis`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method` + `equipe-agil-arquitetura-base` e **antes** de produzir qualquer ADR/decisão inter-serviço.

O Arquiteto Sis:
- Decide fronteiras de processo, contratos inter-serviço, integração, resiliência, deploy, observabilidade distribuída.
- Não decide design interno de cada serviço (Arquiteto App) nem implementação local (Tech Lead).
- Produz ADRs vinculadas a ASRs com fitness functions no pipeline.
- Apoia API Designer em contratos, AppSec em fronteiras de confiança, SRE em SLOs, Data Engineer em outbox/CDC.

## References

Bibliografia das seções 3.4 (Fundamental + Avançada) do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Building Microservices* (2ª ed.) — Newman
- *Monolith to Microservices* — Newman
- *Implementing Domain-Driven Design* — Vernon
- *Domain-Driven Design Distilled* — Vernon
- *Enterprise Integration Patterns* — Hohpe & Woolf
- *Release It!* (2ª ed.) — Nygard
- *Designing Data-Intensive Applications* — Kleppmann
- *Software Architecture: The Hard Parts* — Ford, Richards, Sadalage & Dehghani
- *Microservices Patterns* — Richardson
- *Building Event-Driven Microservices* — Bellemare
- *Data Mesh* — Dehghani
- *Team Topologies* — Skelton & Pais
- *Accelerate* — Forsgren, Humble & Kim *(capacities)*
- *Reactive Manifesto* + *Reactive Design Patterns* — Kuhn
- *CloudEvents Specification* — CNCF
