---
name: equipe-agil-arquiteto-app-knowledge
description: Conhecimento específico do Arquiteto de Aplicação (Tech Anchor App) da Equipe Backend Ágil Kanban+XP. Cobre design intra-aplicação evolutivo em Java 21 + Quarkus 3 — Clean Architecture (Martin), Hexagonal/Ports & Adapters, DDD tático completo (Evans, Vernon — Entity, Value Object, Aggregate, Domain Service, Repository, Domain Event), GoF (catálogo de uso), PoEAA (Fowler), Modular Monolith, Vertical Slice, Connascence, anti-padrões (Anemic Domain, God Class, Sinkhole Layering) e — fundamental e inegociável — ArchUnit como fitness function executável em CI (regras de pacote acíclicas, Domain → não-Infrastructure, JAX-RS apenas em adapters de entrada, anti-Anemic Domain, freeze + failOnEmptyShould). Invoque para decisões de design dentro de UM deployable. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Arquiteto de Aplicação (Tech Anchor App) — Conhecimento específico

Skill carregada pelo agente `equipe-agil-arquiteto-app` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method` + `equipe-agil-arquitetura-base`. Cobre o que é exclusivo do design **dentro de um deployable** — em **Java 21 + Quarkus 3**, stack do repositório `aco-equipes`.

## 1. Conceitos centrais

### 1.1 Foco e fronteira do Arquiteto App

- **Foco**: backend, APIs, domínio e design de código **intra-aplicação**, com viés evolucionário.
- **Produz**: ADRs leves (vide `equipe-agil-arquitetura-base`), **fitness functions** automatizadas (ArchUnit, métricas de complexidade, contratos), diagramas C3 do(s) container(es) sob sua guarda.
- **Não decide**: granularidade entre serviços, integração inter-serviço, dados distribuídos (isso é do Arquiteto Sis).
- **Sobreposição com Arquiteto Sis**: fronteira de bounded context que vira serviço, decisão *modular monolith vs split*.
- **RACI**: R em Arquitetura Intra-App (ADR); A do Tech Lead.

### 1.2 Stack default — Java 21 + Quarkus 3

Tudo neste guia assume o ecossistema do repositório:

- **JVM**: Java 21 LTS (records, sealed types, pattern matching, virtual threads, text blocks).
- **Framework**: Quarkus 3 (CDI, RESTEasy Reactive, MicroProfile, SmallRye).
- **Persistência**: Hibernate ORM **Panache** + **Envers** para auditoria; migrações via **Flyway/Liquibase** (Data Engineer é dono).
- **Validação**: Hibernate Validator / Jakarta Validation (Bean Validation 3.0).
- **Resiliência**: SmallRye Fault Tolerance (`@Timeout`, `@Retry`, `@CircuitBreaker`, `@Bulkhead`, `@Fallback`).
- **Observabilidade**: MicroProfile Health, Metrics, OpenTelemetry.
- **Mensageria**: SmallRye Reactive Messaging (Kafka).
- **Testes**: JUnit 5, RestAssured, Testcontainers, Pact, **PIT** (mutation), **jqwik** (property-based), **ArchUnit** (estrutural).

Qualquer recomendação concreta deve referenciar a ferramenta idiomática deste ecossistema.

### 1.3 Clean Architecture (Martin)

- **Dependency Rule**: dependências apontam **para dentro** (entrada/saída → use case → domínio); nunca o inverso.
- **Anéis** (do interior para fora):
  1. **Entities / Domain** — regras de negócio puras, sem framework.
  2. **Use Cases** — orquestração de operações de domínio.
  3. **Interface Adapters** — controladores REST, gateways, repositórios.
  4. **Frameworks & Drivers** — Quarkus, Hibernate, drivers de banco.
- **Inversão de dependência**: use cases definem ports (interfaces); adapters implementam.
- Vantagem: dominio testável **sem JVM container**, sem banco, sem servidor.

### 1.4 Hexagonal / Ports & Adapters (Cockburn → Vernon)

- Equivalente a Clean Architecture com terminologia diferente:
  - **Hexágono** = aplicação + domínio.
  - **Driving ports** (entrada — controlador, API, scheduler) ↔ **driven ports** (saída — repositório, gateway, broker).
  - **Adapters** implementam ports; substituíveis (in-memory para teste, real para produção).
- **Aplicação prática em Quarkus**:
  - Pacote `domain` puro (zero `@ApplicationScoped`, zero `@Inject` — só Java).
  - Pacote `application` (use cases) com `@ApplicationScoped`; depende de **ports** (interfaces) declarados em `domain`.
  - Pacote `infrastructure` (adapters) com `@Path` (REST), `@PanacheRepository` (DB), `@RestClient` (HTTP out), `@Incoming`/`@Outgoing` (Kafka).

### 1.5 DDD Tático (Evans / Vernon) — bloco por bloco

| Bloco | Definição operacional | Heurística |
|-------|-----------------------|------------|
| **Value Object** | Imutável, sem identidade, definido pelos atributos. Em Java 21 → `record`. | Default para qualquer conceito de domínio que não muda no tempo. |
| **Entity** | Tem identidade própria; muda ao longo do tempo. | Use ID gerado por domínio (UUID) ou natural (CPF, número de cota). |
| **Aggregate** | Cluster de entidades + VOs com **invariantes consistentes**; tem **raiz** (Aggregate Root). | Toda transação altera **um** agregado. Refs entre agregados por **ID**, não por referência direta. |
| **Domain Service** | Operação de domínio que não pertence a uma entidade/VO específicos. | Use só quando não couber naturalmente em entidade/VO. |
| **Repository** | Coleção de agregados; abstrai persistência. | 1 repositório por agregado. Não expor query language no domínio. |
| **Domain Event** | Algo que aconteceu no domínio, relevante para outros contextos. | Nome no passado (`CotaContratada`), imutável (record). |
| **Factory** | Cria agregados complexos com invariantes garantidas. | Use quando construtor explodiria em complexidade. |
| **Specification** | Predicado de domínio reutilizável. | Use para regras complexas de seleção/validação. |

**Regra-mãe**: invariantes do agregado vivem **dentro** dele; nada externo pode deixá-lo inválido. Bean Validation no DTO de entrada é defesa de borda, **não** substitui invariante.

### 1.6 Bounded Context (estratégico — interface com Arquiteto Sis)

- Fronteira **explícita** de modelo: mesmo termo pode significar coisas diferentes em contextos diferentes.
- Mapeamento entre contextos (Context Mapping): *Shared Kernel, Customer-Supplier, Conformist, Anti-Corruption Layer, Open Host Service, Published Language*.
- Dentro de um deployable, pode haver 1 ou mais bounded contexts (modular monolith); quando contextos viram deployables próprios, Arquiteto Sis assume a integração.

### 1.7 PoEAA — Patterns of Enterprise Application Architecture (Fowler)

Catálogo essencial para backend persistente:

- ***Domain Model*** (vs *Transaction Script* / *Table Module*) — escolha default na equipe.
- **Mapeamento O-R**: *Data Mapper* (preferido — Hibernate Panache) vs *Active Record* (evitar em domínio rico).
- ***Unit of Work*** — implementado pelo Hibernate (sessão/transação).
- ***Identity Map*** — implementado pelo Hibernate (cache de 1º nível).
- ***Lazy Load*** — controle com cuidado (N+1 é o smell clássico).
- ***Repository*** — interface no domínio; implementação no adapter.
- ***Service Layer*** — corresponde aos use cases / application services.
- ***DTO*** — só na fronteira; não vaza para o domínio.

### 1.8 GoF — uso idiomático em Java 21

| Padrão | Quando usar em Java 21 | Idiomatismo |
|--------|------------------------|-------------|
| Strategy | Variar algoritmo em runtime | `sealed interface` + `record`s + `switch` exhaustivo (pattern matching). |
| Factory Method / Abstract Factory | Criação polimórfica | CDI `@Produces` ou método estático em record. |
| Builder | Construção de agregado complexo | Lombok `@Builder` aceitável; idealmente factory + records aninhados. |
| Decorator | Comportamento transversal | CDI `@Decorator` ou wrap manual. |
| Observer | Eventos intra-app | CDI `@Observes` (eventos síncronos) ou Domain Events publicados. |
| Adapter | Adaptar API externa ao domínio | Camada de adapter de saída (port driven). |
| Template Method | Esqueleto fixo + ganchos | `sealed abstract class` + `final` no template. |
| Command | Encapsular requisição | Record + handler dedicado. |
| Composite | Estrutura recursiva | Records + sealed interfaces. |
| Singleton | (Evitar — usar CDI scope). | `@ApplicationScoped`. |
| Chain of Responsibility | Pipeline de processamento | `List<Handler>` + iteração. |

Anti-padrão: aplicar **padrão sem pressão** (Speculative Generality). Padrão emerge da duplicação (vide Refactoring to Patterns em `engineering-coach-knowledge`).

### 1.9 Estilos arquiteturais intra-aplicação

- **Layered** clássico (UI → Application → Domain → Infra) — base; cuidado com **Sinkhole Anti-Pattern** (camada que só repassa).
- **Modular Monolith** — módulos com fronteiras de pacote enforçadas (ArchUnit); cada módulo expõe API estreita; **default da equipe** para serviços novos que ainda não justificam split.
- **Vertical Slice** — organização por funcionalidade ao invés de camada técnica; cada slice tem entrada, regra e saída próprios; reduz acoplamento horizontal.
- **Hexagonal** — vide §1.4; **default da equipe** para componentes com regras de domínio ricas.
- **Microkernel / Plugin** — núcleo estável + plugins; útil para regras de negócio variáveis por cliente/produto.
- **Pipeline** — processamento sequencial; útil para batch e ingestão.

### 1.10 Connascence (Page-Jones)

Métrica de acoplamento entre componentes, do mais fraco ao mais forte:

- *Connascence of Name* — mesmo nome para mesma coisa.
- *Connascence of Type* — mesmo tipo.
- *Connascence of Meaning* — mesmo valor literal interpretado igual.
- *Connascence of Position* — ordem de argumentos.
- *Connascence of Algorithm* — mesma lógica em dois lugares.
- *Connascence of Execution / Timing / Identity* — runtime; mais frágil.

**Regra**: força do acoplamento deve ser **proporcional à proximidade** dos componentes (módulo interno tolera; entre módulos, só os mais fracos).

### 1.11 Anti-padrões intra-aplicação

- ❌ **Anemic Domain Model** (Fowler) — entidades só com getters/setters; lógica em "services". Confunde com *Transaction Script*; perde poder do DDD.
- ❌ **God Class** — uma classe com várias responsabilidades; sinaliza falta de extração.
- ❌ **Sinkhole Layering** — camada que só repassa parâmetros; remova ou consolide.
- ❌ **Feature Envy** — método em A usa mais campos de B → mover para B.
- ❌ **Primitive Obsession** — `String cpf`, `BigDecimal valor` espalhados; criar VO.
- ❌ **Train Wreck** (`obj.getA().getB().getC()`) — viola Lei de Demeter; *Tell, Don't Ask*.
- ❌ **Vazamento de framework no domínio** — `@Path` ou `@Entity` em classe de domínio puro.
- ❌ **DTO usado como entidade de domínio** — confunde fronteiras.

### 1.12 ArchUnit como fitness function — **FUNDAMENTAL E INEGOCIÁVEL EM JAVA**

**ArchUnit** é a ferramenta de teste arquitetural padrão para projetos Java desta equipe. Toda decisão arquitetural **passível de verificação estática** vira **regra ArchUnit no CI**, falhando o build quando violada.

**Configuração mínima** no commit stage:

- Roda como teste JUnit (`@ArchTest`).
- **`failOnEmptyShould(true)`** — força que `should()` chains tenham conteúdo (evita regra vazia que passa por engano).
- **`freeze(rule)`** — congela violações pré-existentes em legado; aceita o débito documentado, mas **não permite novas violações**. Usar `ViolationStore` em arquivo versionado.
- Falha do ArchUnit no commit stage da `pr-*` **bloqueia o merge** (vide `equipe-agil-xp-baseline`).

**Catálogo de regras essenciais** (exemplos em pseudocódigo Java):

```java
// 1. Acíclicas entre pacotes principais
slices().matching("..(*)..").should().beFreeOfCycles()

// 2. Domínio puro — não depende de Infrastructure nem de Quarkus/CDI/JPA
noClasses().that().resideInAPackage("..domain..")
  .should().dependOnClassesThat()
  .resideInAnyPackage(
    "..infrastructure..",
    "jakarta.persistence..",
    "jakarta.ws.rs..",
    "io.quarkus..",
    "org.hibernate..",
    "jakarta.enterprise.."  // CDI
  )

// 3. JAX-RS (@Path) só em adapters de entrada
classes().that().areAnnotatedWith(Path.class)
  .should().resideInAPackage("..infrastructure.in.rest..")

// 4. Repositórios Panache só em adapters de saída
classes().that().areAssignableTo(PanacheRepositoryBase.class)
  .should().resideInAPackage("..infrastructure.out.persistence..")

// 5. Anti-Anemic Domain — entities devem ter métodos de domínio, não só accessors
classes().that().areAnnotatedWith(Entity.class)
  .should().haveMethodsThat(
    areNotGetters().and(areNotSetters()).and(areNotConstructors())
  ).withMinimumCount(1)

// 6. Application services não chamam REST direto (sempre via port)
noClasses().that().resideInAPackage("..application..")
  .should().dependOnClassesThat()
  .resideInAPackage("org.eclipse.microprofile.rest.client..")

// 7. DTOs ficam fora do domínio
classes().that().haveSimpleNameEndingWith("Dto")
  .should().resideOutsideOfPackage("..domain..")

// 8. Pacotes de módulos do modular monolith não se referenciam direto, só via API publicada
slices().matching("com.app.(*)..").namingSlices("Module $1")
  .should().notDependOnEachOther()
  .ignoreDependency(alwaysTrue(), resideInAPackage("..api.."))
```

**Política**: cada ADR aprovada que contenha estrutura verificável **deve criar ou atualizar pelo menos uma regra ArchUnit**. Mensagem de falha do ArchUnit referencia a ADR que ela protege.

### 1.13 Evolutionary Architecture aplicada (com referência ao `equipe-agil-arquitetura-base`)

- Fitness functions executáveis ≥ 1 por -ility crítica do projeto.
- ArchUnit cobre *modifiability*, *maintainability* estruturais.
- Latência p95 + smoke de carga cobre *performance*.
- PIT cobre *testability*.
- OWASP Dependency-Check / Trivy cobre *security* de supply chain.
- Mudança estrutural grande → Mikado (`engineering-coach-knowledge`) + Branch by Abstraction dentro da `feature/*`.

## 2. Práticas e heurísticas operacionais

### 2.1 Estrutura de pacotes default — Quarkus + Hexagonal

```
com.org.<modulo>
├── domain
│   ├── model         (Entities, VOs, Aggregates — Java puro)
│   ├── service       (Domain Services)
│   ├── event         (Domain Events — records)
│   └── port          (interfaces — driven ports)
├── application
│   ├── usecase       (Use Case @ApplicationScoped)
│   └── port          (driving ports — interfaces; opcional)
└── infrastructure
    ├── in
    │   ├── rest      (@Path — JAX-RS)
    │   ├── messaging (@Incoming — Kafka in)
    │   └── scheduler (@Scheduled)
    └── out
        ├── persistence  (Panache repositories, @Entity quando é apenas tabela; ideal: mapper para domain)
        ├── rest         (@RestClient — chamada HTTP a parceiros)
        └── messaging    (@Outgoing — Kafka out)
```

Pode haver `api` (interfaces publicadas entre módulos do modular monolith) quando aplicável.

### 2.2 Quando usar `record` vs `class`

- **Record**: VOs, DTOs, eventos de domínio, comandos, queries. Imutável por default. Java 21 dá pattern matching exhaustivo com sealed.
- **Class** (com construtor protegido / método estático de fábrica): Entidades JPA, agregados com estado mutável controlado.
- **Sealed interface + records**: hierarquias fechadas (ex.: estados, eventos polimórficos) — habilita `switch` exhaustivo.

### 2.3 Como manter agregado consistente em Hibernate Panache

- Construtor da entidade aplica invariantes; setters só onde fizer sentido (preferir métodos de domínio: `aprovarContratacao()`, não `setStatus()`).
- `@PrePersist` / `@PreUpdate` checa invariantes finais.
- Domain Service quando a operação envolve > 1 agregado **só de leitura**; mutação cruzando agregados → considerar reformular fronteira.
- Transação por use case (Quarkus `@Transactional`); 1 agregado raiz mutado por transação.

### 2.4 Quando dividir um módulo (preparar para virar serviço)

Sinais (alinhados com Arquiteto Sis):
- Equipes diferentes evoluem o mesmo módulo (Conway).
- Carga muito desigual entre módulos.
- Ciclo de release diferente.
- Modelo de dados que diverge fortemente do resto.

Quando dividir: ADR + Branch by Abstraction + Anti-Corruption Layer no novo serviço; escalar ao Arquiteto Sis para definir contrato/transporte.

### 2.5 Anti-padrões de Quarkus a evitar

- ❌ Lógica de negócio em `@Path` controller — controller é adapter de entrada, fino.
- ❌ Injetar `EntityManager` no domínio — usar repository no application via port.
- ❌ Misturar `@Transactional` em camada errada — granularidade na fronteira de use case.
- ❌ Devolver entidade JPA em endpoint REST — sempre mapear para DTO/representação.
- ❌ Validação de regra de domínio só em `@Valid` do DTO — invariante vive na entidade.
- ❌ Lazy loading vazando para a serialização — usar projeção / DTO.

### 2.6 Como conduzir um Architecture Office Hour (ritual XP da equipe)

- 1h/semana, agenda aberta; pares trazem dúvidas de design.
- Foco em **decisões pendentes** com risco real (Fairbanks — risk-driven).
- Saída esperada: ≥ 1 ADR proposta ou ≥ 1 fitness function nova / atualizada.
- Co-conduzido pelos dois Arquitetos (App + Sis) para problemas cruzados.

## 3. Templates e checklists

### 3.1 Esqueleto de Use Case (Quarkus + Hexagonal)

```java
// application/usecase/ContratarCotaUseCase.java
@ApplicationScoped
public class ContratarCotaUseCase {

  private final CotaRepository cotaRepository;       // driven port
  private final PublicadorDeEventos publicador;      // driven port
  private final RelogioDeDominio relogio;            // driven port

  @Inject
  public ContratarCotaUseCase(
      CotaRepository cotaRepository,
      PublicadorDeEventos publicador,
      RelogioDeDominio relogio) {
    this.cotaRepository = cotaRepository;
    this.publicador = publicador;
    this.relogio = relogio;
  }

  @Transactional
  public CotaContratada executar(ContratarCotaCommand cmd) {
    var cota = Cota.contratar(cmd, relogio.agora());      // invariantes no agregado
    cotaRepository.salvar(cota);
    var evento = new CotaContratada(cota.id(), relogio.agora());
    publicador.publicar(evento);
    return evento;
  }
}
```

### 3.2 Esqueleto de Adapter REST de entrada

```java
// infrastructure/in/rest/CotasResource.java
@Path("/cotas")
public class CotasResource {

  private final ContratarCotaUseCase contratar;

  @Inject
  public CotasResource(ContratarCotaUseCase contratar) {
    this.contratar = contratar;
  }

  @POST
  public Response criar(@Valid ContratarCotaRequest req) {
    var cmd = req.toCommand();
    var resultado = contratar.executar(cmd);
    return Response.status(CREATED).entity(ContratarCotaResponse.from(resultado)).build();
  }
}
```

### 3.3 Esqueleto de teste ArchUnit (em CI)

```java
@AnalyzeClasses(packages = "com.org.cotas",
    importOptions = ImportOption.DoNotIncludeTests.class)
public class ArquiteturaTest {

  @ArchTest
  static final ArchRule dominio_nao_depende_de_infra =
      noClasses().that().resideInAPackage("..domain..")
          .should().dependOnClassesThat()
          .resideInAnyPackage(
              "..infrastructure..",
              "jakarta.persistence..",
              "jakarta.ws.rs..",
              "io.quarkus..",
              "org.hibernate.."
          );

  @ArchTest
  static final ArchRule jaxrs_apenas_em_adapter_in_rest =
      classes().that().areAnnotatedWith(Path.class)
          .should().resideInAPackage("..infrastructure.in.rest..");

  @ArchTest
  static final ArchRule pacotes_sem_ciclos =
      slices().matching("com.org.cotas.(*)..").should().beFreeOfCycles();

  @ArchTest
  static final ArchRule modular_monolith_modules_nao_dependem_entre_si =
      slices().matching("com.org.(*)..").namingSlices("$1")
          .should().notDependOnEachOther()
          .ignoreDependency(alwaysTrue(), resideInAPackage("..api.."));
}
```

### 3.4 Checklist de design pré-implementação

- [ ] Bounded context identificado (este código é deste contexto?).
- [ ] Agregado raiz definido; invariantes listadas.
- [ ] Ports declarados no domínio antes do adapter.
- [ ] Use case com 1 entrada / 1 saída claros.
- [ ] Sem framework no domínio (`@Entity` ok se separar entidade-de-persistência da entidade-de-domínio quando necessário).
- [ ] ArchUnit cobrindo a regra que esta estrutura assume.
- [ ] ADR escrita ou referenciada quando há trade-off arquitetural.
- [ ] Caminho de teste claro (unidade no domínio, integração no use case via fake/Testcontainer, contract test no adapter).

### 3.5 Checklist anti-Anemic Domain

- [ ] Entidades têm métodos de domínio com nomes de **ação de negócio** (`aprovar()`, `contratar()`), não só `setStatus()`.
- [ ] Setters de propriedades de negócio são privados ou inexistentes.
- [ ] Construtor/factory aplica invariantes.
- [ ] Use case fala em verbos de domínio, não em CRUD genérico.
- [ ] Domain Service só onde nenhuma entidade encaixa.

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-arquiteto-app`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method` + `equipe-agil-arquitetura-base`.

O Arquiteto App:
- Produz ADRs intra-aplicação acompanhadas de **regras ArchUnit no CI** sempre que aplicável.
- Atua no Replenishment (caça aos ASRs intra-app), no Architecture Office Hour, e como C em decisões do Tech Lead.
- Não escreve features completas; produz **esqueletos** e **regras** que orientam o time.
- Quando o problema **cruza fronteira de processo**, encaminha ao Arquiteto Sis.

## References

Bibliografia das seções 3.3 (Intermediária + Avançada) do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Clean Architecture* — Martin
- *Domain-Driven Design* — Evans
- *Implementing Domain-Driven Design* — Vernon
- *Patterns of Enterprise Application Architecture* — Fowler
- *Design Patterns* — Gamma, Helm, Johnson & Vlissides (GoF)
- *Object-Oriented Software Construction* (2ª ed.) — Meyer
- *Pattern-Oriented Software Architecture* (POSA) vol. 1–5 — Buschmann et al.
- *Domain Modeling Made Functional* — Wlaschin
- *Analysis Patterns* — Fowler
- *Continuous Architecture in Practice* — Erder, Pureur & Woods
- *ArchUnit User Guide* — Peter Gafert *(complementar; ferramenta padrão da equipe)*
