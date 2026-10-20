---
name: ddd-hexagonal
description: DDD tático e arquitetura hexagonal no Spring Boot — bounded contexts e context map, entities, value objects como records, aggregates e invariantes, domain events, ports e adapters, mapeamento domínio ↔ JPA, ArchUnit e quando NÃO usar (CRUD). Use quando modelar um domínio rico ou avaliar sair do layout flat-by-layer.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md), [`../spring-data-jpa/SKILL.md`](../spring-data-jpa/SKILL.md) e [`../microservices/SKILL.md`](../microservices/SKILL.md) (onde os bounded contexts viram serviços). Esta skill **estende** `code-organization` para domínios complexos; ela **não** substitui o layout flat-by-layer para serviços simples.

# DDD tático + Arquitetura Hexagonal

**DDD** modela o software em torno do **domínio de negócio**, com a linguagem do especialista. A **arquitetura hexagonal** (ports and adapters) mantém o **núcleo de negócio independente de frameworks e infraestrutura**: o domínio não sabe se é chamado por REST ou fila, nem se persiste em MySQL ou DynamoDB. O ganho é um **núcleo testável sem Spring e sem banco**, que sobrevive a trocas de tecnologia.

## Quando usar — e quando NÃO

| Use quando | **Não** use quando |
|---|---|
| Há **regras de negócio ricas** (invariantes, estados, políticas) que mudam com o negócio | O serviço é um **CRUD**: lê/grava campos com pouca regra |
| O sistema é **longevo** e terá várias integrações (REST, eventos, jobs) | Protótipo/serviço simples e descartável |
| Quer proteger o núcleo de mudanças de framework/banco | A equipe não tem o domínio claro nem acesso ao especialista |
| Vários times/serviços exigem **fronteiras de contexto** claras | Você só quer "arquitetura bonita" |

**O layout flat-by-layer do pack (`code-organization`) é o padrão e basta para a maioria dos serviços.** Hexagonal custa **mais código** (mapeamentos entre modelos, interfaces) — só vale quando a complexidade do **domínio** a justifica. Aplicar hexagonal a um CRUD é *over-engineering* (`code-reviewer`: abstração prematura).

---

## 1. Estratégico: linguagem, bounded contexts, context map

- **Ubiquitous language:** o código usa os **mesmos termos do negócio** (`Loan`, `returnBook`, `overdue`), em inglês nos identificadores (regra do pack), com um **glossário** compartilhado com os especialistas. Se o negócio diz "empréstimo" e o código diz `Rental`, há ruído.
- **Bounded context:** a fronteira onde um **modelo e uma linguagem são consistentes**. "Book" no `catalog` (título, ISBN, autor) ≠ "Book" no `lending` (exemplar físico emprestável). **Não** crie um `Book` universal. Cada contexto vira, tipicamente, **um serviço** (ou um módulo — `modular-monolith`).
- **Context map** — como os contextos se relacionam:
  | Relação | Significado |
  |---|---|
  | **Customer–Supplier** | O contexto *upstream* (fornecedor) atende às necessidades do *downstream* (cliente) |
  | **Conformist** | O downstream aceita o modelo do upstream como está (sem poder de negociação) |
  | **Anti-Corruption Layer (ACL)** | O downstream **traduz** o modelo do upstream para o seu, **isolando-se** dele — essencial ao integrar com **legado** ou modelo "sujo" de terceiros |
  | **Open Host Service / Published Language** | O upstream publica uma API/esquema **estável e documentado** para muitos consumidores (`contract-testing`) |
  | **Shared Kernel** | Pequeno modelo **compartilhado** entre dois contextos (use com muito cuidado: acoplamento) |

  O **ACL** é o padrão mais útil na prática: um adapter que chama o sistema externo e converte para tipos do **seu** domínio.

---

## 2. Tático: os blocos de construção

### Value Object (VO) — imutável, sem identidade, igualdade por valor
Use **records** (`java-modern-features`), com validação no **compact constructor**: um VO **nunca existe inválido**.
```java
public record Money(BigDecimal amount, String currency) {

    public Money {
        Objects.requireNonNull(amount);
        Objects.requireNonNull(currency);
        if (amount.signum() < 0) throw new IllegalArgumentException("amount must not be negative");
    }

    public Money add(Money other) {
        if (!currency.equals(other.currency)) throw new IllegalArgumentException("currency mismatch");
        return new Money(amount.add(other.amount), currency);
    }
}

public record LoanId(UUID value) {

    public LoanId {
        Objects.requireNonNull(value);
    }

    public static LoanId newId() {
        return new LoanId(UUID.randomUUID());
    }
}
```
**Primitive obsession** é o inimigo: `Money` em vez de `double`, `Email` em vez de `String`, `LoanId`/`BookId` em vez de dois `Long` intercambiáveis (o compilador impede trocar os argumentos). Dinheiro é `BigDecimal`, nunca `double`.

### Entity — tem identidade e ciclo de vida
Igualdade **por identidade** (o id), não por todos os campos (diferente das entities/DTOs do pack). Comportamento **dentro** da entity, não em um "service" anêmico.

### Aggregate e Aggregate Root — a fronteira de consistência
Um **aggregate** é um grupo de objetos tratado como **uma unidade de consistência**, acessado **só pelo root**. As **invariantes** (regras que sempre valem) são garantidas **dentro** dele, em **uma transaction**.
```java
public class Loan {

    private final LoanId id;
    private final MemberId memberId;
    private final BookId bookId;
    private LoanStatus status;
    private LocalDate dueDate;
    private final List<DomainEvent> events = new ArrayList<>();

    private Loan(LoanId id, MemberId memberId, BookId bookId, LocalDate dueDate) {
        this.id = id;
        this.memberId = memberId;
        this.bookId = bookId;
        this.dueDate = dueDate;
        this.status = LoanStatus.ACTIVE;
    }

    public static Loan start(MemberId memberId, BookId bookId, LoanPolicy policy, Clock clock) {
        var loan = new Loan(LoanId.newId(), memberId, bookId, LocalDate.now(clock).plus(policy.loanPeriod()));
        loan.events.add(new LoanStarted(loan.id, memberId, bookId, Instant.now(clock)));
        return loan;
    }

    public void returnBook(Clock clock) {
        if (status != LoanStatus.ACTIVE) throw new IllegalStateException("Loan " + id + " is not active");
        this.status = LoanStatus.RETURNED;
        events.add(new BookReturned(id, bookId, Instant.now(clock)));
    }

    public void extend(LoanPolicy policy) {
        if (status != LoanStatus.ACTIVE) throw new IllegalStateException("Only active loans can be extended");
        this.dueDate = dueDate.plus(policy.extensionPeriod());
    }

    public List<DomainEvent> pullEvents() {
        var pulled = List.copyOf(events);
        events.clear();
        return pulled;
    }

    // getters (sem setters públicos)
}
```
- **Sem setters públicos**: o estado só muda por **métodos de negócio** (`returnBook`, `extend`) que protegem as invariantes. Setters públicos = **modelo anêmico** (anti-pattern: a lógica vaza para services e as invariantes viram sugestão).
- **Fábrica estática** (`start`) valida na criação; construtor privado.
- **Receba `Clock`** (não `LocalDate.now()` direto): domínio **determinístico e testável** (`testing`).
- **Aggregates pequenos.** Inclua só o que precisa ser consistente **junto**. Aggregate grande = contenção, lock longo e carga desnecessária.
- **Referencie outros aggregates por ID** (`MemberId`, `BookId`), **nunca por referência de objeto**: mantém as fronteiras transacionais e evita carregar o grafo inteiro. **Uma transaction altera um aggregate**; efeitos em outros aggregates/contextos são **eventuais**, por evento (`saga-pattern`).
- **Concorrência:** `@Version` (optimistic locking) no root na camada de persistência.

### Domain Event — algo que **já aconteceu** no domínio
```java
public sealed interface DomainEvent permits LoanStarted, BookReturned {}

public record LoanStarted(LoanId loanId, MemberId memberId, BookId bookId, Instant occurredAt) implements DomainEvent {}
public record BookReturned(LoanId loanId, BookId bookId, Instant occurredAt) implements DomainEvent {}
```
Nome **no passado**. O aggregate **coleta** os eventos; a camada de aplicação os **publica depois do commit** (via **outbox** — `transactional-outbox` — quando saem do serviço). Eventos de **domínio** (internos) ≠ eventos de **integração** (contrato público, versionado — `messaging`): traduza um no outro no adapter para não vazar o modelo interno.

### Domain Service e Policy
Regra de negócio que **não pertence a um único aggregate** (calcular multa considerando política e histórico) vai em um **domain service** — uma classe **sem estado e sem dependência de framework**. `LoanPolicy` (período, limites) pode ser um VO/política injetada.

### Repository — um **port** por aggregate
Uma **interface do domínio** que fala em termos do aggregate, **não em `JpaRepository`**:
```java
public interface LoanRepository {

    Optional<Loan> findById(LoanId id);

    void save(Loan loan);
}
```
Só carrega/salva **aggregates inteiros pelo root**. Consultas de leitura sofisticadas (listas, relatórios) **não** vão aqui — use um **read model** (`cqrs-event-sourcing`).

---

## 3. Hexagonal: portas e adaptadores

```
        ┌─────────── ADAPTERS DE ENTRADA ───────────┐
        │  REST controller · listener Kafka/SQS · job │
        └───────────────────┬───────────────────────┘
                            │ chama (porta de entrada = use case)
              ┌─────────────▼──────────────┐
              │  APPLICATION (use cases)   │  orquestra, @Transactional
              │  ┌──────────────────────┐  │
              │  │  DOMAIN (aggregates, │  │  regras puras, sem framework
              │  │  VOs, events, policy)│  │
              │  └──────────────────────┘  │
              └─────────────┬──────────────┘
                            │ depende de interfaces (portas de saída)
        ┌───────────────────▼───────────────────────┐
        │ ADAPTERS DE SAÍDA: JPA · outbox/Kafka · REST│
        └─────────────────────────────────────────────┘
```
**A regra de dependência:** tudo aponta **para dentro**. `domain` não depende de nada (nem Spring, nem JPA, nem Jackson). `application` depende de `domain`. `adapter` depende de `application`/`domain`. **Nunca** o contrário.

| Porta | Direção | Exemplo |
|---|---|---|
| **Entrada** (driving) | quem **usa** o núcleo | `StartLoanUseCase`, `ReturnBookUseCase` (interfaces) |
| **Saída** (driven) | o que o núcleo **precisa** | `LoanRepository`, `BookCatalog`, `DomainEventPublisher`, `Clock` |

### Layout de packages (por contexto)

```
br.com.padrao.lending/
├── domain/
│   ├── model/                  # Loan, LoanId, MemberId, BookId, LoanStatus, Money, LoanPolicy
│   ├── event/                  # DomainEvent, LoanStarted, BookReturned
│   └── port/                   # LoanRepository (saída do domínio)
├── application/
│   ├── port/in/                # StartLoanUseCase, ReturnBookUseCase, StartLoanCommand
│   ├── port/out/               # BookCatalog, DomainEventPublisher
│   └── LoanService.java        # implementa os use cases (@Service, @Transactional)
├── adapter/
│   ├── in/web/                 # LoanController, LoanRequest/LoanResponse (DTOs de borda)
│   ├── in/messaging/           # listeners
│   ├── out/persistence/        # LoanJpaEntity, SpringDataLoanRepository, LoanPersistenceAdapter, LoanMapper
│   ├── out/catalog/            # CatalogRestAdapter (ACL: traduz o catalog para o domínio)
│   └── out/messaging/          # OutboxEventPublisher
└── config/                     # beans (Clock, wiring)
```
Compare com o layout flat-by-layer de `code-organization`: aqui as pastas são por **papel arquitetural** dentro de **um contexto**, e o `Startup` e o `config/` ficam no topo. **Um contexto = um serviço** (ou um módulo — `modular-monolith`).

### Caso de uso (application service)

```java
public interface StartLoanUseCase {

    LoanId start(StartLoanCommand command);
}

public record StartLoanCommand(UUID memberId, UUID bookId) {}
```
```java
@Service
public class LoanService implements StartLoanUseCase, ReturnBookUseCase {

    private final LoanRepository loans;
    private final BookCatalog catalog;
    private final DomainEventPublisher events;
    private final LoanPolicy policy;
    private final Clock clock;

    public LoanService(LoanRepository loans, BookCatalog catalog, DomainEventPublisher events, LoanPolicy policy, Clock clock) {
        this.loans = loans;
        this.catalog = catalog;
        this.events = events;
        this.policy = policy;
        this.clock = clock;
    }

    @Override
    @Transactional
    public LoanId start(StartLoanCommand command) {
        var bookId = new BookId(command.bookId());
        if (!catalog.isAvailable(bookId)) throw new BookNotAvailableException(bookId);
        var loan = Loan.start(new MemberId(command.memberId()), bookId, policy, clock);
        loans.save(loan);
        events.publishAll(loan.pullEvents());
        return loan.id();
    }
}
```
- **Constructor injection** aqui (campos `final`): o núcleo precisa ser **instanciado em teste sem Spring** (`new LoanService(fakeRepo, ...)`). **Isto é uma exceção justificada** à preferência "field `@Autowired`" do pack para este estilo arquitetural — registre-a no `CLAUDE.md` (`project-claude-md`).
- O **use case** orquestra: carrega o aggregate, chama o método de **negócio**, persiste, publica eventos. **A regra mora no domínio**, não aqui; o service fica **fino**.
- **`@Transactional` no use case** (fronteira de transaction — `spring-data-jpa`), nunca no controller nem no domínio. Uma transaction = um aggregate.
- Lança **exceptions de domínio** (`BookNotAvailableException`); o adapter web as traduz em HTTP (`exception-handling`).
- **Command/Query objects** (`StartLoanCommand`) como **records** na borda do use case — o controller converte o DTO web no command.

### Adapters

**Web** — fino: valida (`bean-validation`), converte DTO ↔ command, chama o use case:
```java
@RestController
@RequestMapping("/api/loan/v1")
public class LoanController {

    private final StartLoanUseCase startLoan;

    public LoanController(StartLoanUseCase startLoan) {
        this.startLoan = startLoan;
    }

    @PostMapping
    public ResponseEntity<LoanResponse> start(@Valid @RequestBody StartLoanRequest request) {
        var id = startLoan.start(new StartLoanCommand(request.memberId(), request.bookId()));
        return ResponseEntity.status(HttpStatus.CREATED).body(new LoanResponse(id.value()));
    }
}
```
**Persistência** — o **adapter** implementa o port do domínio e mapeia **modelo de domínio ↔ entity JPA**:
```java
@Component
public class LoanPersistenceAdapter implements LoanRepository {

    private final SpringDataLoanRepository jpa;
    private final LoanMapper mapper;

    public LoanPersistenceAdapter(SpringDataLoanRepository jpa, LoanMapper mapper) {
        this.jpa = jpa;
        this.mapper = mapper;
    }

    @Override
    public Optional<Loan> findById(LoanId id) {
        return jpa.findById(id.value()).map(mapper::toDomain);
    }

    @Override
    public void save(Loan loan) {
        jpa.save(mapper.toEntity(loan));
    }
}
```
**ACL** de outro contexto/serviço — o adapter chama a API (`service-communication`, com `resilience`) e **devolve um tipo do seu domínio**; o DTO do outro serviço **não sai do adapter**.

### O custo do mapeamento — e a variante pragmática

Manter **dois modelos** (domínio puro + entity JPA) dá independência total, mas exige **mapear** (Dozer/MapStruct/à mão — `spring-data-jpa`) e custa código. Duas escolhas honestas:
1. **Hexagonal "pura":** domínio sem nenhuma annotation; `LoanJpaEntity` separada no adapter. Máxima proteção; mais código. Para domínios complexos e longevos.
2. **Hexagonal pragmática:** as **annotations JPA ficam no próprio aggregate** (aceitando o acoplamento ao `jakarta.persistence`), sem mapeamento. Menos código, o domínio ainda não depende de Spring/web/mensageria. **Documente a escolha** (ADR) e o ArchUnit abaixo adapta a regra (`jakarta.persistence` permitido).
**Em ambos** continua valendo: **a entity/aggregate nunca é exposta pelo controller** (DTO de borda), **sem Lombok**, e `equals/hashCode` por identidade.

---

## 4. Impor a arquitetura com ArchUnit

Regra de dependência que só existe na cabeça de quem a desenhou **é violada em 3 meses**. Teste-a:
```xml
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>${archunit.version}</version>
    <scope>test</scope>
</dependency>
```
```java
@AnalyzeClasses(packages = "br.com.padrao.lending", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {

    @ArchTest
    static final ArchRule domainDoesNotDependOnFrameworks = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAnyPackage(
                    "org.springframework..", "jakarta.persistence..", "com.fasterxml.jackson..", "tools.jackson..", "..adapter..", "..application..");

    @ArchTest
    static final ArchRule applicationDoesNotDependOnAdapters = noClasses()
            .that().resideInAPackage("..application..")
            .should().dependOnClassesThat().resideInAPackage("..adapter..");

    @ArchTest
    static final ArchRule adaptersDoNotDependOnEachOther = slices()
            .matching("..adapter.(*)..")
            .should().notDependOnEachOther();
}
```
(`archunit.version` em `<properties>` — não está no BOM do Boot; `maven-config`.) Roda no `mvn test` e **quebra o build** quando alguém importa JPA no domínio.

## 5. Testes — o grande benefício

- **Domínio:** unit tests **puros**, sem Spring, sem mocks, em milissegundos — as invariantes (`Loan.start` calcula o vencimento; `returnBook` em empréstimo devolvido lança) com um `Clock` fixo (`Clock.fixed(...)`). É aqui que mora a maior parte das regras (`testing`).
- **Use cases:** com **fakes em memória** dos ports (um `InMemoryLoanRepository`) em vez de Mockito — testes legíveis e resistentes a refactor.
- **Adapters:** o **web** com `@WebMvcTest` (`testing`); a **persistência** com `@DataJpaTest` + banco real em container (`spring-data-jpa`); o **ACL** com contrato (`contract-testing`).
- **ArchUnit** como teste de arquitetura.

## 6. Anti-patterns

- **Modelo anêmico**: entities só com getters/setters e toda a regra em `*Service`.
- **Hexagonal em CRUD**: interfaces e mapeamentos sem regra de negócio a proteger.
- **Domínio dependendo de Spring/JPA/Jackson** (`@Autowired`, `@Entity`, `@JsonProperty` no `domain` — na versão pura).
- **Aggregate gigante**; referência de objeto entre aggregates; mais de um aggregate alterado na mesma transaction.
- **Repository genérico** (`CrudRepository<T>` exposto ao domínio) e lógica de negócio em queries.
- **Use case "caixa de ferramentas"** com regra de negócio (em vez de delegar ao aggregate).
- **Vazar o modelo de outro contexto** (usar o DTO do `catalog` dentro do `lending`) — falta de ACL.
- Misturar **evento de domínio** com **evento de integração** público.

---

## Regras principais

- **Use DDD/hexagonal só para domínios com regra rica**; para CRUD, o layout flat-by-layer de `code-organization` é o certo.
- **Ubiquitous language** nos identificadores (em inglês); **um modelo por bounded context**; **ACL** ao integrar com legado/outros modelos.
- **Value objects como records** validados no compact constructor (`Money`, `*Id`); nunca `double` para dinheiro; evite *primitive obsession*.
- **Aggregates pequenos**, root como único ponto de acesso, **sem setters públicos**, invariantes dentro; **outros aggregates por ID**; **uma transaction = um aggregate**; `@Version`.
- Domain events no passado, coletados no aggregate e publicados **após o commit** via **outbox**; separe evento de **domínio** de evento de **integração**.
- **Regra de dependência para dentro**: `domain` puro → `application` (use cases, `@Transactional`) → `adapters`; repository é **port** do domínio.
- Controller fino; **DTO de borda** (aggregate/entity nunca exposta); exceptions de domínio traduzidas no adapter web.
- Constructor injection **justificada** neste estilo (núcleo testável sem Spring) — registre no `CLAUDE.md`; decida **pura × pragmática** (JPA no domínio) em ADR.
- **ArchUnit** impõe a regra de dependência no build; domínio testado sem Spring, use cases com fakes.
- **Sem Lombok** — deliberado.
