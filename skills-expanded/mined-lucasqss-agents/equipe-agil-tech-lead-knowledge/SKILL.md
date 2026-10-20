---
name: equipe-agil-tech-lead-knowledge
description: Conhecimento específico do Tech Lead da Equipe Backend Ágil Kanban+XP. Cobre Java 21 moderno (records, sealed types, pattern matching, switch expressions, text blocks, virtual threads, structured concurrency), Quarkus 3 idiomático (CDI, Panache, MicroProfile Config/Health/Metrics/OpenTelemetry/Fault Tolerance, RESTEasy Reactive, build nativo), Effective Java (Bloch), Java Concurrency in Practice (Goetz), Release It! (Nygard) aplicado ao código, GoF idiomático em Java moderno, DDD distilled (Vernon) na implementação, legacy code com testes (Feathers), e engineering leadership do Orosz. Invoque para revisões técnicas de código Java/Quarkus, decisões de implementação, mentoring técnico, code review com profundidade, ou quando precisar destravar dúvidas idiomáticas. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Tech Lead — Conhecimento específico

Skill carregada pelo agente `equipe-agil-tech-lead` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre o conhecimento profundo de **Java 21 + Quarkus 3 idiomático** que o Tech Lead precisa para mentorar implementação, fazer code review com profundidade, destravar dúvidas técnicas e codar lado a lado com a equipe.

## 1. Conceitos centrais

### 1.1 Mandato do Tech Lead na equipe

- **Owner técnico do código** no dia a dia: padrão idiomático, qualidade da implementação, mentoring sênior.
- **Code review** com profundidade — não só estilo, mas trade-offs e idiomaticidade.
- **Participa do Replenishment** com Eng Coach e PO (verifica viabilidade técnica imediata).
- **Não decide arquitetura intra-app** (Arquiteto App) nem inter-serviço (Arquiteto Sis), mas é **C** em ambas.
- **Não conduz cadências Kanban** (Eng Coach) nem coacha XP (Eng Coach), mas é **R** em sua execução.
- RACI: A/R em qualidade do código, mentoring técnico individual, implementação de features complexas.

### 1.2 Stack default

- **Java 21 LTS** — toolchain alvo da equipe.
- **Quarkus 3** — framework principal. Foco em `quarkus-resteasy-reactive(-jackson)`, `quarkus-hibernate-orm-panache(-rest)`, `quarkus-hibernate-envers`, `quarkus-arc` (CDI), `quarkus-smallrye-*` (Config, Health, Metrics, OpenTelemetry, Fault Tolerance, Reactive Messaging, OpenAPI), `quarkus-flyway`, `quarkus-oidc`, `quarkus-jacoco`.
- **Build**: Maven (`pom.xml`) é o padrão neste repositório; produção pode rodar como JVM (mais comum) ou nativo (GraalVM).
- **Testes**: JUnit 5 + RestAssured + Testcontainers + Mockito + AssertJ + PIT (mutation) + ArchUnit. Aprofundamento vive em `quality-engineer-knowledge`.

### 1.3 Java 21 moderno — recursos essenciais

#### Records (Java 14+, padrão para Value Objects)

```java
public record Dinheiro(BigDecimal valor, Moeda moeda) {
    public Dinheiro {
        Objects.requireNonNull(valor, "valor");
        Objects.requireNonNull(moeda, "moeda");
        if (valor.signum() < 0) throw new IllegalArgumentException("valor negativo");
    }

    public Dinheiro somar(Dinheiro outro) {
        if (!moeda.equals(outro.moeda)) throw new MoedaIncompativelException();
        return new Dinheiro(valor.add(outro.valor), moeda);
    }
}
```

- `equals`/`hashCode`/`toString` automáticos.
- *Compact canonical constructor* para validação fail-fast.
- Records **não substituem** entidades JPA mutáveis — usar para Value Objects, DTOs, eventos imutáveis.

#### Sealed types (Java 17+, modelagem de soma)

```java
public sealed interface ResultadoPagamento
    permits Aprovado, Recusado, EmAnalise {}

public record Aprovado(String autorizacao) implements ResultadoPagamento {}
public record Recusado(String motivo) implements ResultadoPagamento {}
public record EmAnalise(Instant previsaoResposta) implements ResultadoPagamento {}
```

- Compilador garante exaustividade no `switch`.
- Substitui hierarquias `abstract class + enum` para somas fechadas.

#### Pattern matching + switch expression (Java 21)

```java
String descricao = switch (resultado) {
    case Aprovado a    -> "OK: " + a.autorizacao();
    case Recusado r    -> "NEG: " + r.motivo();
    case EmAnalise e   -> "AGUARDA até " + e.previsaoResposta();
};
```

- Sem `default` quando o tipo é sealed e o switch é exaustivo.
- Pattern `case Aprovado(String a)` (record pattern) extrai componentes.

#### Text blocks

```java
String sql = """
    SELECT id, cliente_id, valor
      FROM pedido
     WHERE status = ?
       AND criado_em >= ?
    """;
```

- Resolve indentação automaticamente.
- Útil para SQL, JSON, mensagens longas.

#### Virtual Threads (Java 21 — Project Loom)

- **Thread leve** gerenciada pela JVM (não 1:1 com thread OS).
- **Default** para workloads I/O-bound (chamadas HTTP, banco, mensageria).
- Em Quarkus: anotar endpoint com `@RunOnVirtualThread` (extensão `quarkus-virtual-threads`) — código bloqueante sem custo de thread OS.
- **Cuidados**:
  - `synchronized` em virtual thread "pina" a thread carrier (degrada throughput) — use `ReentrantLock`.
  - Não usar virtual thread para workload CPU-bound (continua precisando de pool clássico).
  - `ThreadLocal` em virtual thread tem custo — prefira `ScopedValue` (preview em 21).

#### Structured Concurrency (preview em Java 21)

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Supplier<Cliente> sc = scope.fork(() -> clienteClient.buscar(id));
    Supplier<Saldo>   ss = scope.fork(() -> saldoClient.buscar(id));
    scope.join().throwIfFailed();
    return new ClienteCompleto(sc.get(), ss.get());
}
```

- Trata "trabalho relacionado" como unidade — propaga cancelamento, falha rápido.
- Recurso em preview; usar conscientemente.

### 1.4 Effective Java (Bloch) — itens com maior ROI na revisão

- **Item 1** — Static factory methods em vez de construtores (`Optional.of`, `List.of`).
- **Item 2** — Builder para classes com muitos parâmetros opcionais.
- **Item 17** — Minimize mutabilidade (records ajudam).
- **Item 18** — Composição sobre herança.
- **Item 22** — Use interfaces para tipos.
- **Item 28-33** — Generics — `List<? extends T>` para produtores, `List<? super T>` para consumidores (PECS).
- **Item 34-38** — Enums sobre constantes; enum com comportamento polimórfico.
- **Item 49** — Valide parâmetros (fail-fast).
- **Item 55** — `Optional` para retorno onde "ausência" é normal; **nunca** para campo ou parâmetro.
- **Item 64** — Programe para interfaces.
- **Item 78** — Sincronize acesso compartilhado a dados mutáveis.
- **Item 85** — Prefira alternativas a serialização Java nativa.

### 1.5 Java Concurrency in Practice (Goetz)

- **Imutabilidade** é a estratégia de concorrência mais barata: objetos imutáveis são thread-safe por construção.
- **Confinamento de thread**: dado mutável usado por uma única thread (stack-confined, ThreadLocal).
- **Locks**: `synchronized` para casos simples; `ReentrantLock` para timeout/interrupção/tryLock; `ReadWriteLock` quando leitura domina.
- **Collections concorrentes**: `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`.
- **Atomics**: `AtomicInteger`, `AtomicReference` para contador/flag simples.
- **Memory model (JMM)**: `volatile` para visibilidade entre threads (sem atomicidade composta).
- **Anti-padrões**:
  - Double-checked locking sem `volatile`.
  - `Thread.stop()`, `suspend()`, `resume()` (deprecated).
  - `synchronized(this)` exposto (lock público).
  - Construtor que vaza `this` para outra thread antes de terminar.

### 1.6 Quarkus 3 idiomático

#### CDI / Arc (injeção de dependência)

- `@ApplicationScoped` é o default para serviços.
- `@RequestScoped` para estado por requisição (cuidado com vazamento).
- `@Singleton` apenas quando absolutamente necessário (sem proxy).
- **Inject por construtor** preferível a `@Inject` em campo (testável, imutável).

```java
@ApplicationScoped
public class ServicoPagamento {
    private final RepositorioPagamento repo;
    private final GatewayCartao gateway;

    public ServicoPagamento(RepositorioPagamento repo, GatewayCartao gateway) {
        this.repo = repo;
        this.gateway = gateway;
    }
}
```

#### Hibernate ORM com Panache

- `PanacheEntity` (active record) **OU** `PanacheRepository` (repository pattern — preferido para DDD).
- **Queries por método nomeado** com HQL parametrizado:

```java
@ApplicationScoped
public class PedidoRepository implements PanacheRepositoryBase<Pedido, UUID> {
    public List<Pedido> aprovadosDe(LocalDate dia) {
        return find("status = ?1 and criadoEm >= ?2", Status.APROVADO, dia.atStartOfDay()).list();
    }
}
```

- **Transações**: `@Transactional` no método de aplicação (boundary), nunca dentro do domínio.
- **Hibernate Envers** (`quarkus-hibernate-envers`): habilita auditoria de mudança em entidades anotadas com `@Audited`.
- **Flyway** (`quarkus-flyway`): scripts SQL versionados em `db/migration/V<n>__<nome>.sql`.

#### MicroProfile Config

- `@ConfigProperty(name="app.foo", defaultValue="bar") String foo;`
- Sobreposição por arquivo `application.properties` → variáveis de ambiente → `META-INF/microprofile-config.properties`.
- Mapping em record (`@ConfigMapping`) para grupos coesos de configuração.

#### MicroProfile Health/Metrics/OpenTelemetry

- Health: `/q/health/live` e `/q/health/ready`; implementar `HealthCheck` para dependências críticas.
- Metrics: `@Counted`, `@Timed`, `@Gauge` (Micrometer integrado por padrão em Quarkus 3).
- OpenTelemetry: spans automáticos em REST/JDBC/Kafka; criar span custom com `@WithSpan`.

#### MicroProfile Fault Tolerance

- `@Timeout`, `@Retry`, `@CircuitBreaker`, `@Bulkhead`, `@Fallback` (catálogo no `arquiteto-sis-knowledge` §1.7).

#### RESTEasy Reactive

- JAX-RS clássico (`@Path`, `@GET`, `@POST`, `@Produces`, `@Consumes`).
- Retorno bloqueante (rodando em virtual thread) **ou** retorno reativo (`Uni<T>`, `Multi<T>`) — escolha por endpoint.
- `@Valid` para Hibernate Validator nos DTOs de entrada.
- Tratamento de erro centralizado com `@Provider ExceptionMapper<T>`.

```java
@Path("/pedidos")
public class PedidoResource {
    private final CriarPedido criarPedido;
    public PedidoResource(CriarPedido criarPedido) { this.criarPedido = criarPedido; }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    @RunOnVirtualThread
    public Response criar(@Valid NovoPedidoRequest req) {
        UUID id = criarPedido.executar(req.toComando());
        return Response.created(URI.create("/pedidos/" + id)).build();
    }
}
```

#### Build nativo (GraalVM)

- Reflexão exige hint (`@RegisterForReflection`) — Quarkus já faz para classes detectadas.
- Cold start de 50–200 ms vs 2–5s em JVM; memória residente menor.
- Build mais lento e ferramental ainda menos rico — adotar **com ASR justificando**, não por moda.

### 1.7 GoF idiomático em Java moderno (catálogo aplicado)

- **Strategy** — geralmente uma interface + implementações injetadas via CDI. Para enum de comportamento, use enum com método abstrato.
- **Factory** — `static T of(...)` em records (Effective Java item 1). Para CDI, `@Produces`.
- **Builder** — recordless. Para POJOs complexos, builder explícito; muitas vezes desnecessário se record `with(...)` resolve.
- **Observer** — CDI Events (`@Observes`) ou `Multi` do Mutiny.
- **Decorator** — CDI `@Decorator` para cross-cutting; interceptors (`@Interceptor`) para AOP simples.
- **Template Method** — quase sempre substituível por composição + lambda (estratégia).
- **Singleton** — `@ApplicationScoped` ou `@Singleton`. Manual (instância estática) é code smell.
- **Adapter** — Hexagonal — adapter implementa porta de domínio (vide `arquiteto-app-knowledge`).
- **Command** — encapsula intenção; em Java moderno, geralmente um record + Use Case (PoEAA Service Layer).

### 1.8 Release It! (Nygard) aplicado ao código

Catálogo no `arquiteto-sis-knowledge` §1.7. No nível de **implementação**, atenção a:

- **Toda chamada externa** (HTTP, banco, broker, fila) tem **timeout explícito**.
- `try-with-resources` sempre que abrir recurso (Connection, Stream, AutoCloseable).
- Não retornar `null` para representar erro — `Optional`, exception específica, ou sealed `Result`.
- Evitar `catch (Exception e)` que silencia — capturar específico ou re-lançar.
- Logar exceção com contexto (correlation ID, parâmetros relevantes — **sem dados sensíveis**).

### 1.9 DDD Distilled (Vernon) aplicado à implementação

Detalhes em `arquiteto-app-knowledge`. No nível de código:

- **Agregado** controla invariantes; sem `setters` públicos para campos que participam de regra.
- **Repository** retorna agregado completo; sem `findFooField` ad-hoc.
- **Application Service** orquestra: carrega agregado, invoca método, persiste — sem regra de negócio.
- **Domain Event** (record imutável) publicado pelo agregado, despachado pelo application service (transactional outbox no `arquiteto-sis-knowledge` §1.11).

### 1.10 Engineering Ladder e leadership técnico (Orosz — *The Software Engineer's Guidebook*, *Building Mobile Apps at Scale*)

- **Tech Lead ≠ Manager** — foco em técnica, não em carreira/desempenho (carreira é outro track).
- **Mentoring**:
  - Pair com júnior é investimento; rotacionar para difundir conhecimento.
  - Code review constrói cultura; pergunte mais do que afirme.
  - Aceite que o time vai escrever código diferente do seu — o critério é "passa nas fitness functions + DoD + revisado".
- **Trade-off de tempo**:
  - 50% código + revisão.
  - 30% mentoring + pair.
  - 20% coordenação técnica (Replenishment, refinamento técnico, dúvidas dos Arquitetos).
- **Escalonamento**: dúvida de design intra-app → Arquiteto App; inter-serviço → Arquiteto Sis; segurança → AppSec; SLO → SRE; teste estratégia → Quality Engineer.

### 1.11 Legacy code (Feathers) — base resumida

Conhecimento operacional vive em `engineering-coach-knowledge` §1.5. Como Tech Lead, lembrar:
- Antes de tocar legado, **escrever characterization test** que capture comportamento atual.
- Encontrar **seam** para injetar fake/spy sem reescrever o código.
- **Sprout method / sprout class** para isolar mudança nova de código não testado.

## 2. Práticas e heurísticas operacionais

### 2.1 Code review de profundidade — checklist mental

1. **Idiomaticidade Java 21**: record onde caberia? sealed onde caberia? virtual thread onde caberia? pattern matching?
2. **Idiomaticidade Quarkus**: CDI por construtor? `@Transactional` no boundary? configuração via `@ConfigProperty`/`@ConfigMapping`?
3. **Effective Java**: imutabilidade onde possível? `Optional` no retorno? PECS nos generics?
4. **Concorrência**: dado compartilhado mutável? lock? collection concorrente? virtual thread sem `synchronized`?
5. **Release It!**: timeout em toda chamada externa? `try-with-resources`? exceção com contexto?
6. **DDD tático**: regra de negócio no agregado? application service só orquestra?
7. **Testes**: cobre golden path **e** edges? fail-fast em validação? sem mock everything?
8. **Logs/observabilidade**: estruturado? sem dado sensível? correlation ID propagado?
9. **Performance**: N+1? `fetch join` necessário? cache onde faz sentido?
10. **Segurança**: input validado? autorização aplicada? secrets fora do código?

### 2.2 Anti-padrões Java/Quarkus comuns

- ❌ Campo `@Inject` em vez de construtor — torna teste mais difícil.
- ❌ `Optional` em parâmetro ou campo (use anotação `@Nullable` ou separar tipos).
- ❌ `Stream` armazenado em campo (Stream é one-shot).
- ❌ `parallelStream` sem justificativa (overhead, ordem indefinida).
- ❌ Mock de tudo no teste — vira teste de mock, não de comportamento.
- ❌ `@Transactional` em método privado — não tem efeito (proxy CDI não intercepta).
- ❌ Bloquear em endpoint reativo (`Uni`/`Multi`) — quebra reactor; use `@RunOnVirtualThread` ou `Uni` consistentemente.
- ❌ Configuração hard-coded em código — usar `@ConfigProperty`.
- ❌ Logar input bruto (PII, senha, token) — logar campos selecionados.
- ❌ `e.printStackTrace()` — usar logger estruturado.

### 2.3 Disciplinas que o Tech Lead modela explicitamente

- **Commit pequeno, mensagem clara, branch `pr-*`** (vide `xp-baseline`).
- **TDD red-green-refactor** nos próprios commits, especialmente quando pareando com júnior.
- **Refactor "Boy Scout"** — deixar o código mais simples ao passar.
- **Sem PR alheio sem entender o porquê** — leitura ativa, comentário com pergunta antes de afirmação.

### 2.4 Quando dizer "não" como Tech Lead

- "Não" a atalhos que comprometem fitness function (mesmo sob pressão de prazo).
- "Não" a generalização sem ASR.
- "Não" a feature flag eterna — toda flag tem owner + data de remoção.
- "Não" a mock everything — testes precisam validar comportamento.
- "Não" a "vou refatorar depois" sem ticket criado na intangible queue.

### 2.5 Mentoring — formato sugerido de sessão técnica

1. Mentee escolhe o problema (autonomia).
2. Pair-programming TDD para chegar à primeira solução verde.
3. Refactor guiado por pergunta: "esse nome revela intenção?", "essa função faz uma coisa só?".
4. Discussão de alternativa idiomática (sealed em vez de `if instanceof`, record em vez de DTO mutável).
5. Mentee escreve uma anotação curta do que aprendeu (não para o tech lead — para o futuro mentee dele).

## 3. Templates e checklists

### 3.1 Esqueleto idiomático de Use Case (Application Service)

```java
@ApplicationScoped
public class CriarPedido {
    private final RepositorioPedido pedidos;
    private final RepositorioCliente clientes;
    private final EventPublisher events;

    public CriarPedido(RepositorioPedido pedidos, RepositorioCliente clientes, EventPublisher events) {
        this.pedidos = pedidos;
        this.clientes = clientes;
        this.events = events;
    }

    @Transactional
    public UUID executar(ComandoCriarPedido cmd) {
        Cliente cliente = clientes.obrigatorioPor(cmd.clienteId());
        Pedido p = Pedido.novo(cliente, cmd.itens());
        pedidos.salvar(p);
        events.publicar(new PedidoCriado(p.id(), Instant.now()));
        return p.id();
    }
}
```

### 3.2 Esqueleto idiomático de Aggregate

```java
public final class Pedido {
    private final UUID id;
    private final UUID clienteId;
    private final List<ItemPedido> itens;
    private StatusPedido status;

    private Pedido(UUID id, UUID clienteId, List<ItemPedido> itens, StatusPedido status) {
        this.id = id;
        this.clienteId = clienteId;
        this.itens = List.copyOf(itens);
        this.status = status;
    }

    public static Pedido novo(Cliente cliente, List<ItemPedido> itens) {
        if (itens.isEmpty()) throw new PedidoSemItemException();
        return new Pedido(UUID.randomUUID(), cliente.id(), itens, StatusPedido.PENDENTE);
    }

    public void aprovar() {
        if (status != StatusPedido.PENDENTE) throw new TransicaoInvalidaException(status);
        this.status = StatusPedido.APROVADO;
    }

    // getters por leitura; nenhum setter público
    public UUID id() { return id; }
    public StatusPedido status() { return status; }
}
```

### 3.3 Esqueleto idiomático de teste (JUnit 5 + AssertJ)

```java
class PedidoTest {
    @Test
    void naoPermiteCriarPedidoSemItem() {
        Cliente c = ClienteFixture.qualquer();
        assertThatThrownBy(() -> Pedido.novo(c, List.of()))
            .isInstanceOf(PedidoSemItemException.class);
    }

    @Test
    void aprovaPedidoPendente() {
        Pedido p = Pedido.novo(ClienteFixture.qualquer(), List.of(ItemFixture.qualquer()));
        p.aprovar();
        assertThat(p.status()).isEqualTo(StatusPedido.APROVADO);
    }
}
```

### 3.4 Checklist "esse PR está pronto para merge em `feature/*`?"

- [ ] CI verde na `pr-*`.
- [ ] Cobertura nova com testes próprios (unidade + um nível acima quando faz sentido).
- [ ] ArchUnit verde (vide `arquiteto-app-knowledge` §3.3).
- [ ] Mutation score do módulo afetado ≥ alvo (vide `quality-engineer-knowledge`).
- [ ] Sem TODO sem ticket vinculado.
- [ ] Sem feature flag sem owner + data de remoção.
- [ ] Logs estruturados, sem PII.
- [ ] Não toca em branch alheia (`develop`, `release/*`, `feature/*` de outras equipes).
- [ ] `pr-*` será deletada após o merge.

### 3.5 Quando escalar (e para quem)

- **Decisão de design intra-app** (módulo, agregado, adapter) → **Arquiteto App**.
- **Decisão inter-serviço** (contrato, mensageria, saga) → **Arquiteto Sis**.
- **Segurança** (autz, OIDC, JWT, threat model) → **AppSec**.
- **SLO/observabilidade** (instrumentação, alertas) → **SRE**.
- **Estratégia de testes** (camadas, contract, performance) → **Quality Engineer**.
- **Schema/migração de dado** → **Data Engineer**.
- **Pipeline/CI/CD** → **DevOps**.
- **Contrato público de API** → **API Designer**.

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-tech-lead`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O Tech Lead usa esta skill para:
- Fazer code review com profundidade idiomática (Java 21 + Quarkus 3).
- Codar a próxima feature quando o time precisa de aceleração.
- Mentorar pareando, com vocabulário Effective Java / Goetz / Release It!.
- Validar viabilidade técnica no Replenishment.
- Modelar disciplina XP (TDD, branch `pr-*`, refactor contínuo).

Outros papéis técnicos **consomem** suas revisões; **Arquitetos** decidem estrutura, **Tech Lead** decide implementação.

## References

Bibliografia da seção 3.5 do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Effective Java* (3ª ed.) — Bloch
- *Java Concurrency in Practice* — Goetz et al.
- *Modern Java in Action* — Urma, Fusco & Mycroft
- *Release It!* (2ª ed.) — Nygard
- *Domain-Driven Design Distilled* — Vernon
- *Implementing Domain-Driven Design* — Vernon
- *Design Patterns* — Gamma, Helm, Johnson & Vlissides *(GoF — uso idiomático em Java moderno)*
- *Working Effectively with Legacy Code* — Feathers
- *The Software Engineer's Guidebook* — Orosz
- *Building Mobile Apps at Scale* — Orosz *(perspectiva sobre engineering ladder)*
- *Quarkus in Action* — Niedermann, Buchwald et al.
- *Mastering Java 21* — Reges & Davis *(perspectiva sobre Loom/Pattern Matching)*
