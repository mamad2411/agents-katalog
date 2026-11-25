---
name: equipe-agil-quality-engineer-knowledge
description: Conhecimento específico do Quality Engineer da Equipe Backend Ágil Kanban+XP. Cobre estratégia de testes em camadas (Test Pyramid + Honeycomb) em Java 21 + Quarkus 3 — JUnit 5, AssertJ, Mockito, RestAssured, Testcontainers, Pact (contract testing consumer-driven), WireMock, jqwik (property-based), PIT (mutation), JMeter/Gatling (performance), exploratory testing (Hendrickson), test heuristics (Kaner), xUnit patterns (Meszaros), Specification by Example (Adzic) executável, DORA quality metrics (CFR, MTTR). Owner do mandato de estabilidade pós-merge nas branches da equipe (pr-* e feature/*) e da estratégia de testes. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Quality Engineer — Conhecimento específico

Skill carregada pelo agente `equipe-agil-quality-engineer` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre estratégia e prática de testes ao longo da pirâmide, em **Java 21 + Quarkus 3**.

## 1. Conceitos centrais

### 1.1 Mandato do Quality Engineer na equipe

- **Estratégia de testes** em todas as camadas (unidade, integração, contrato, e2e, perf, segurança, exploratório).
- **Mandato inegociável**: garantir que **todo merge em uma `feature/*` da equipe** mantém comportamentos anteriores íntegros **e** cobre o novo comportamento com testes próprios (vide `xp-baseline` §1.6).
- **Não substitui** TDD do desenvolvedor — TDD é responsabilidade de quem escreve o código (R do Tech Lead/dev, com coaching do Eng Coach). QE eleva o teto e cobre as camadas que TDD sozinho não cobre.
- **RACI**: A/R em estratégia de testes, em qualidade observável (mutation score, contract test, e2e), em métricas DORA de qualidade (Change Failure Rate, MTTR).
- **Owner da DoD** do ponto de vista de testes (vide `xp-baseline` §3.1).

### 1.2 Test Pyramid + Honeycomb (Cohn / Spotify)

- **Pyramid (Cohn)**: muitos unitários rápidos → menos de integração → poucos e2e/UI.
- **Honeycomb (Spotify, contexto microsserviço)**: poucos unitários **frágeis** (de pura lógica), muitos **de integração de serviço** (real DB, REST in-process, broker em Testcontainers), poucos e2e cross-service.
- **Heurística da equipe**:
  - Lógica de domínio densa → muitos unitários (pyramid).
  - Serviço fino (CRUD + adapter) → mais integração de serviço com Testcontainers (honeycomb).
  - **Sempre** contract test entre serviços que se integram.
  - **Sempre** smoke perf no acceptance stage da `feature/*`.
  - **Sempre** acceptance test via Gherkin (specification by example) para feature visível ao cliente.

### 1.3 Stack default de testes em Quarkus

| Camada | Ferramenta | Anotação Quarkus |
|--------|-----------|------------------|
| Unidade pura (domínio) | JUnit 5 + AssertJ | (nenhuma — POJO) |
| Unidade com CDI | JUnit 5 + Mockito | `@QuarkusTest` ou `@ExtendWith(MockitoExtension)` |
| Integração com banco real | Testcontainers (Postgres) | `@QuarkusTest` + `@QuarkusTestResource` |
| REST in-process | RestAssured | `@QuarkusTest` |
| Mock HTTP externo | WireMock + `@QuarkusTestResource` | — |
| Contract consumer | Pact JVM (consumer side) | — |
| Contract provider | Pact JVM (provider side) | `@QuarkusTest` |
| Mensageria | Testcontainers (Kafka) | `@QuarkusTest` |
| Mutation | PIT (`pitest-maven`) | — |
| Property-based | jqwik | — |
| Performance | Gatling ou JMeter | rodando contra `quarkus:dev` ou container |
| Architecture fitness | ArchUnit | `@AnalyzeClasses` |
| Exploratory | charters + sessão timeboxed | manual |

### 1.4 JUnit 5 — recursos essenciais

- `@DisplayName` para legibilidade.
- `@Nested` para agrupamento (cenários Given-When-Then por classe interna).
- `@ParameterizedTest` + `@CsvSource`/`@MethodSource` — tabela de exemplos (Specification by Example).
- `@TempDir`, `@TestInstance(LIFECYCLE.PER_CLASS)` quando útil.
- `assertAll(...)` para soft assertions agrupados (ou AssertJ `SoftAssertions`).
- `@Tag("slow")` + filtro no pipeline (rodar `unit` no commit stage, `integration` no acceptance stage).

### 1.5 AssertJ — assertions fluentes

- `assertThat(x).isEqualTo(y)` em vez de `assertEquals(y, x)` (legibilidade).
- `extracting`, `usingRecursiveComparison`, `satisfies` para verificações sobre objetos compostos.
- `assertThatThrownBy(...).isInstanceOf(...).hasMessageContaining(...)` para exceções.
- Para coleções: `containsExactly`, `containsExactlyInAnyOrder`, `hasSize`, `allSatisfy`.

### 1.6 Mockito — uso disciplinado

- **`@Mock` + `@InjectMocks`** ou construtor explícito (preferível para refletir injeção real).
- `verify(...)` com parcimônia — testar comportamento, não interação.
- `ArgumentCaptor<T>` quando precisar inspecionar argumento passado.
- **Heurística xUnit Patterns (vide `engineering-coach-knowledge` §1.6)**:
  - Use **fake** (in-memory) quando o colaborador tem comportamento interno.
  - Use **stub** para dependência externa determinística.
  - Use **mock** com expectativa apenas quando interação **é** o contrato.
  - Use **Testcontainers** para banco/broker — mais real que mock.

### 1.7 Testcontainers — banco e broker reais

```java
@QuarkusTest
@QuarkusTestResource(value = PostgresContainerResource.class)
class PedidoRepositoryIT {
    @Inject PedidoRepository repo;

    @Test
    void persisteEBusca() {
        Pedido p = PedidoFixture.qualquer();
        repo.salvar(p);
        assertThat(repo.porId(p.id())).isPresent().get().isEqualTo(p);
    }
}
```

- Postgres real (versão de produção) sobe em Docker no setup; descartado no teardown.
- Migration via Flyway roda no startup; teste exercita o schema real.
- **Sem H2** para teste de integração — H2 e Postgres divergem em SQL/tipos/coleção.
- Usar `@TestProfile` para configurar `quarkus.datasource.*` apontando para o container.

### 1.8 RestAssured — teste de endpoint in-process

```java
@QuarkusTest
class PedidoResourceIT {
    @Test
    void criaPedidoRetorna201() {
        given().contentType(ContentType.JSON)
               .body("""
                 { "clienteId": "...", "itens": [...] }
                 """)
            .when().post("/pedidos")
            .then().statusCode(201)
                   .header("Location", containsString("/pedidos/"));
    }
}
```

- `@QuarkusTest` inicia o app; RestAssured chama em `localhost:<porta-test>`.
- Bom para teste de **boundary completo** (validação, autz, mapper, serviço, repository, banco).

### 1.9 Contract testing com Pact (Consumer-Driven Contracts)

**Problema**: como evitar que serviço A quebre serviço B em produção sem rodar e2e a cada PR?

**Pact**:
1. **Consumer** (A) escreve teste que define o contrato esperado (request + response).
2. Pact gera um `.json` pact (contrato).
3. Pact Broker armazena versionado.
4. **Provider** (B) roda teste que verifica que satisfaz o pact publicado.
5. `can-i-deploy` no CI bloqueia deploy se contrato pendente.

**Quando usar**: comunicação síncrona inter-serviço; eventos assíncronos (Pact Message).

**Quando NÃO usar**: API pública externa (use specification-based testing); muitos consumidores anônimos.

### 1.10 WireMock — mock de dependência HTTP

- Para serviço externo que não dá para subir em Testcontainers.
- Stub responses fixas; injetar latência; simular falha (timeout, 500).
- Bom para validar resiliência (`@Retry`, `@CircuitBreaker`).

### 1.11 jqwik — property-based testing

```java
@Property
void inversoSomaEhInverso(@ForAll BigDecimal a, @ForAll BigDecimal b) {
    Assume.that(b.signum() != 0);
    assertThat(a.add(b).subtract(b)).isEqualByComparingTo(a);
}
```

- Framework gera centenas de inputs; *shrinking* encontra menor caso falho.
- Bom para invariantes: idempotência, comutatividade, roundtrip serialize-deserialize, monotonia.
- **Complementa** example-based; não substitui Gherkin de casos representativos.

### 1.12 PIT — mutation testing

- Gera **mutantes** (versões do código com mudanças pequenas: trocar `>` por `>=`, `+` por `-`, remover linha).
- Se a suite passa com mutante vivo → teste é confirmatório (não detecta o bug).
- **Mutation Score** = % de mutantes mortos.
- **Heurística**:
  - Mutation score < 60% = teste fraco (revisitar).
  - 60–80% = razoável.
  - > 80% = robusto.
- Configurar `pitest-maven` no pipeline para módulos de domínio; rodar diff (mudou só pacote X → mutar só X) para tempo aceitável.

### 1.13 Gatling/JMeter — performance smoke

- Não substitui teste de carga dedicado; serve como **fitness function** de performance no pipeline.
- Definir cenário curto (1 min) com SLA: `p95 < 500ms`, `error rate < 0.1%`.
- Falha o build se SLA quebrado.
- **Gatling DSL (Scala/Java)** é mais elegante; **JMeter** é mais corporativo, com plugins.

### 1.14 Specification by Example / BDD (Adzic) — papel do QE

- Gherkin **não é responsabilidade exclusiva do QE** — Three Amigos (PO + dev + QE — vide `po-knowledge` §2.3).
- QE garante que cenário é **executável** (`cucumber-java` ou JUnit parametrizado com tabela), vive em `src/test/resources/features/*.feature` ao lado do código.
- QE policia: critério vago vira critério concreto antes da ready queue.

### 1.15 Exploratory Testing (Hendrickson — *Explore It!*)

- **Sessão timeboxed** (60–90 min) com **charter** (objetivo + heurística).
- Não é "teste sem teste" — é teste **deliberado e investigativo**, registrando observações.
- **Heurísticas SFDPOT** (Bach): Structure, Function, Data, Platform, Operations, Time.
- **Test heuristics cheat sheet** (Kaner): boundary, fuzzy values, big/small/zero/negative, malformed, concurrency, interruption, persistence.
- Resultado: bugs encontrados + ideias de teste automatizado a adicionar.

### 1.16 DORA quality metrics (vide `xp-baseline` §1.10)

QE foca em:
- **Change Failure Rate (CFR)**: % de deploys que causam falha em produção.
- **Mean Time to Restore (MTTR)**: tempo entre falha e restauração.
- **Reliability** (5ª métrica): % de SLOs cumpridos.

Coletadas **por fluxo**, nunca por pessoa. Tendência > valor pontual.

### 1.17 Mandato de estabilidade — operacionalização

Para todo merge `pr-*` → `feature/*`:
- [ ] Testes da `pr-*` cobrem o novo comportamento (unidade + um nível acima quando aplicável).
- [ ] Suite completa da `feature/*` permanece verde **após o merge** (não apenas no PR).
- [ ] Mutation score do módulo afetado não regrediu.
- [ ] Contract tests vigentes continuam verdes.
- [ ] ArchUnit verde.
- [ ] Smoke perf dentro do SLA.

Se quebrar: **stop-the-line** (xP §2.1) — revert preferível a fix-forward se a correção demora > 10 min.

## 2. Práticas e heurísticas operacionais

### 2.1 Como escolher a camada para um novo teste

```
É lógica pura de domínio? ───── sim ──► Unidade (JUnit + AssertJ, sem Quarkus)
                              │
                              não
                              ▼
É boundary HTTP + serviço + banco? ─ sim ─► Integração com Testcontainers + RestAssured
                              │
                              não
                              ▼
É contrato com outro serviço? ─── sim ──► Pact (consumer/provider) no pipeline de ambos
                              │
                              não
                              ▼
É invariante matemática/algorítmica? ─ sim ─► jqwik property-based
                              │
                              não
                              ▼
É fluxo end-to-end de feature? ── sim ──► Gherkin executável (Cucumber ou JUnit param.)
                              │
                              não
                              ▼
É SLA de performance? ─────── sim ──► Gatling/JMeter smoke
```

### 2.2 Anti-padrões de testes

- ❌ **Mock everything** — testes que só verificam mock foram chamados.
- ❌ **Teste com H2 quando produção é Postgres** — divergências em SQL/tipo.
- ❌ **Teste compartilhando estado entre testes** — flaky garantido (`@DirtiesContext` é band-aid).
- ❌ **Asserção no `equals` de objeto rico sem `usingRecursiveComparison`** — mensagem inútil quando falha.
- ❌ **Teste de "que método foi chamado X vezes"** sem que isso seja contrato — fragiliza refactor.
- ❌ **Tempo absoluto no teste** (`Instant.now()`) — flaky; injetar `Clock`.
- ❌ **`Thread.sleep` em teste assíncrono** — usar `Awaitility` (`await().until(...)`).
- ❌ **Cobertura como meta** — 100% line coverage com mutation 20% é teatro.
- ❌ **e2e para tudo** — lento, frágil, pirâmide invertida.
- ❌ **Sem teste de erro** — só golden path testado, edges não.

### 2.3 Quando o teste é difícil de escrever — "listen to the tests" (GOOS)

- Setup imenso → design acoplado → extrair colaborador.
- Mock de classe concreta com muitas dependências → cria interface (porta) e fakeia.
- Teste do tipo "verifico que método foi chamado" → talvez seja teste do mock, não da unidade.

### 2.4 Como QE atua no Replenishment

- **Three Amigos** com PO + dev para refinar critério de aceite (formato Gherkin).
- Pergunta-chave: "como vou saber que está pronto?" — força critério testável.
- Identifica risco de regressão em fluxos vizinhos (sugere caso de teste extra).
- Sinaliza dívida de teste (testes ausentes em código que vai ser tocado).

### 2.5 Como QE atua no Risk Review

- Lista flaky tests da última quinzena (aging, frequência).
- Lista falhas de mutation score que pioraram.
- Lista módulos com baixa cobertura **e** alta taxa de mudança (Tornhill hotspot — vide `engineering-coach-knowledge` §1.12).
- Propõe slot intangible para corrigir.

### 2.6 Defeito em produção — o QE entra como aprendizado

- Para todo CFR > 0: defeito vira **teste novo** que falha → corrige → verde. Sem isso, regressão volta.
- Postmortem inclui "que tipo de teste teria pegado isso?" (unit? integration? contract? perf? exploratory?).
- Se a resposta for "nenhum", a categoria de teste tem buraco — adicionar à estratégia.

## 3. Templates e checklists

### 3.1 Charter de sessão exploratória

```
Charter:      <Explorar X usando Y descobrindo Z>
Duração:      60 min
Tester:       <nome>
Carga:        baixa | média | alta

Heurísticas a aplicar:
- SFDPOT: <quais>
- Boundary values: <quais>
- Concurrency / interrupção: <sim/não>

Observações (notes):
- ...
- ...

Bugs encontrados:
- ...

Ideias de automação:
- ...

Risco residual percebido:
- ...
```

### 3.2 Esqueleto de Feature Gherkin executável

```gherkin
# src/test/resources/features/pedido_aprovacao.feature
Funcionalidade: Aprovação de pedido pendente
  Como atendente
  Eu quero aprovar um pedido pendente
  Para que o cliente seja notificado e o estoque reservado

  Cenário: Pedido pendente é aprovado
    Dado um pedido pendente com 2 itens
    Quando o atendente aprova o pedido
    Então o status do pedido é APROVADO
    E um evento PedidoAprovado é publicado
```

### 3.3 Esqueleto de teste de integração Quarkus + Testcontainers

```java
@QuarkusTest
@QuarkusTestResource(PostgresResource.class)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class PedidoFluxoIT {

    @Test @Order(1)
    void criarPedidoPersisteRetorna201() {
        var resp = given().contentType(JSON).body(NOVO_PEDIDO_JSON)
            .when().post("/pedidos")
            .then().statusCode(201).extract();
        UUID id = UUID.fromString(extrairIdDeLocation(resp.header("Location")));
        assertThat(id).isNotNull();
    }

    @Test @Order(2)
    void aprovarPedidoExistenteRetorna204() {
        UUID id = criarPedido();
        given().when().patch("/pedidos/{id}/aprovar", id)
            .then().statusCode(204);
        given().when().get("/pedidos/{id}", id)
            .then().statusCode(200).body("status", equalTo("APROVADO"));
    }
}
```

### 3.4 Checklist de DoD do ponto de vista de testes

- [ ] Unidade de domínio cobre golden path + edges (≥ 2 testes por regra).
- [ ] Integração de serviço cobre boundary HTTP + banco (Testcontainers).
- [ ] Contract test atualizado (consumer e provider) se mudou contrato.
- [ ] ArchUnit verde.
- [ ] Mutation score do módulo afetado ≥ 70% (alvo) e não regrediu.
- [ ] Smoke perf dentro do SLA (p95 < orçamento).
- [ ] Logs estruturados sem PII.
- [ ] Sem flaky test introduzido (rodar a suite 3× local antes do push).
- [ ] Gherkin (se feature visível) atualizado e executável.

### 3.5 Quando escalar

- **Falha repetida de fitness function arquitetural** (ArchUnit) → Arquiteto App.
- **Contract test quebrando entre serviços** → Arquiteto Sis + API Designer.
- **Performance abaixo do SLO** → SRE + Tech Lead.
- **Mutation score caindo sistemicamente** → Eng Coach (sessão de coaching).
- **PO escrevendo critério vago repetidamente** → Eng Coach + PO (Three Amigos cadência).

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-quality-engineer`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O Quality Engineer usa esta skill para:
- Desenhar estratégia de testes por feature/módulo.
- Operacionalizar o mandato de estabilidade pós-merge nas branches da equipe.
- Conduzir Three Amigos do ponto de vista de testabilidade.
- Conduzir sessões exploratórias e analisar bugs.
- Alimentar Risk Review com flaky/mutation/cobertura.

Tech Lead e devs **escrevem testes**; QE **eleva a estratégia** e **policia o teto**.

## References

Bibliografia da seção 3.6 do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Agile Testing* + *More Agile Testing* — Crispin & Gregory
- *Specification by Example* — Adzic
- *Effective Software Testing* — Aniche
- *Lessons Learned in Software Testing* — Kaner, Bach & Pettichord
- *Explore It!* — Hendrickson
- *xUnit Test Patterns* — Meszaros
- *The Art of Software Testing* (3ª ed.) — Myers, Sandler & Badgett
- *Testing Java Microservices* — Bakker
- *Building Microservices* (2ª ed., cap. de testing) — Newman
- *Practical Test-Driven Development for Java Programmers* — Garcia
- *Mutation Testing for the Masses* — documentação do PIT
- *jqwik User Guide* — Lukosch
