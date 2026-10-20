---
name: java-modern-features
description: Java 17 a 25 aplicado ao padrão do pacote — records, sealed interfaces, pattern matching, switch expressions, text blocks, SequencedCollection, virtual threads no Spring Boot e suas armadilhas, Scoped Values e o que NÃO usar em entities/DTOs. Use quando decidir se uma feature moderna de Java agrega ou antes de ligar virtual threads.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md): esta skill **estende** os "Modern Java idioms" de `code-style` e não os contradiz — entities e DTOs continuam classes com no-arg constructor, getters/setters e sem Lombok.

# Java moderno

Use a feature quando ela torna o código **mais claro ou mais seguro**, não porque é nova. Todas as features abaixo são finais nas versões indicadas; as em preview exigem `--enable-preview` (compilador **e** runtime) e **não** entram em código de produção sem decisão de equipe.

| Feature | Java | Use em |
|---|---|---|
| Text blocks, switch expressions, `var` | 15 / 14 / 10 | sempre que simplificam |
| Records, sealed classes, pattern matching `instanceof` | 16 / 17 | payloads imutáveis, hierarquias fechadas |
| Pattern matching em `switch`, record patterns | 21 | lógica sobre tipos/hierarquias |
| Sequenced collections, virtual threads | 21 | I/O concorrente |
| Scoped Values | 25 | contexto imutável entre threads (substitui `ThreadLocal`) |
| Structured concurrency | preview em 25 | só experimentos |

---

## Records

Imutáveis, com `equals`/`hashCode`/`toString` automáticos. **Use para:** eventos (`BookCreatedEvent`), `ExceptionResponse`, requests/responses de integração, projections de query, fixtures de teste, chaves compostas.
```java
public record BookSummary(Long id, String title) {}
```
Validação no **compact constructor**:
```java
public record Money(BigDecimal amount, String currency) {

    public Money {
        Objects.requireNonNull(amount);
        if (amount.signum() < 0) throw new IllegalArgumentException("amount must not be negative");
    }
}
```
**Não use para:** entities JPA (o Hibernate precisa de no-arg constructor, campos mutáveis e proxies) e os DTOs de entidade deste pack (o Dozer/MapStruct e o Jackson com `RepresentationModel` esperam classe com setters — `code-organization`). Para uma **projection** de leitura, porém, um record é ótimo: `SELECT new com.x.BookSummary(b.id, b.title) FROM Book b`.

## Sealed interfaces + pattern matching em switch

Modelam um conjunto **fechado** de possibilidades e fazem o compilador exigir que todos os casos sejam tratados:
```java
public sealed interface PaymentResult permits Approved, Declined, PendingReview {}

public record Approved(String authorizationCode) implements PaymentResult {}
public record Declined(String reason) implements PaymentResult {}
public record PendingReview(Long caseId) implements PaymentResult {}
```
```java
String message = switch (result) {
    case Approved a -> "Approved: " + a.authorizationCode();
    case Declined d -> "Declined: " + d.reason();
    case PendingReview p -> "Under review #" + p.caseId();
};
```
Sem `default`: se alguém adicionar um novo `permits`, **a compilação quebra** até tratá-lo — melhor que um `if/else` que silenciosamente ignora o caso novo. **Record patterns** desestruturam: `case Declined(String reason) -> ...`. Use `when` para guardas: `case Approved a when a.authorizationCode().isBlank() -> ...`.

Prefira isso a retornar `null`/códigos mágicos/exceptions para fluxo esperado — mas continue lançando domain exceptions para erros que o `@ControllerAdvice` converte em HTTP (`exception-handling`).

## Switch expressions e text blocks

```java
var label = switch (status) {
    case ACTIVE -> "Active";
    case SUSPENDED, BLOCKED -> "Inactive";
};
```
Sem fall-through, retorna valor, e para `enum` o compilador verifica exaustividade. Text blocks para SQL de teste, JSON e CSV de fixture:
```java
var json = """
    {"title": "Clean Code", "price": 77.0}
    """;
```

## `var`, `instanceof` e Optional

Regras de `var` e `instanceof` com pattern já estão em `code-style`. `Optional` **só como tipo de retorno** (`findById`); nunca como campo de entity/DTO, nem como parâmetro. Evite `optional.get()`: use `orElseThrow(() -> new ResourceNotFoundException(...))` como o pack faz.

## SequencedCollection (Java 21)

`List`, `Deque`, `LinkedHashSet`/`LinkedHashMap` ganharam `getFirst()`, `getLast()`, `reversed()`, `addFirst()`: troque `list.get(list.size() - 1)` por `list.getLast()`.

---

## Virtual threads (Java 21+)

Threads baratas gerenciadas pela JVM: milhares de requests bloqueadas em I/O (database, HTTP, SQS) sem esgotar o pool de threads de plataforma. No Spring Boot:
```yaml
spring:
  threads:
    virtual:
      enabled: true
```
Isso faz o Tomcat atender cada request em uma virtual thread, e também os executors do `@Async`/`@Scheduled` e os listeners.

**Quando ajuda:** APIs **I/O-bound** com alta concorrência (a maioria das APIs CRUD). **Quando não ajuda:** trabalho **CPU-bound** (criptografia, processamento de imagem) — não há ganho; o limite é o número de cores.

**Armadilhas reais:**
1. **O gargalo se desloca para o recurso**, não desaparece. Com 10 mil requests concorrentes e um `HikariCP` de 10 conexões, 9.990 esperam no pool. Virtual threads **não** aumentam a capacidade do database: continue dimensionando o pool (`aws-rds-secrets-manager`, `jvm-performance`) e use limites de concorrência/`Semaphore` para proteger dependências frágeis.
2. **Nunca faça pool de virtual threads** — elas são baratas para criar e descartar; use `Executors.newVirtualThreadPerTaskExecutor()`.
3. **Pinning:** uma virtual thread presa à thread de plataforma durante I/O bloqueante sob `synchronized` desperdiça o benefício. O Java 24+ (JEP 491) removeu o pinning por `synchronized`; ainda há em código nativo/`synchronized` em libs antigas em JDK < 24. Detecte com `-Djdk.tracePinnedThreads=full` (JDK ≤ 23) ou o evento JFR `jdk.VirtualThreadPinned`.
4. **`ThreadLocal`** funciona, mas com milhões de threads o custo de memória aparece — prefira **Scoped Values** para contexto novo. Cuidado com `ThreadLocal` que guarda objetos grandes.
5. Bibliotecas que dependem de pool de threads para **limitar** concorrência passam a não limitar mais.
6. Meça antes e depois (latência p99, vazão, uso de CPU) com `observability` — não ligue "porque é moderno".

## Scoped Values (final em Java 25)

Contexto **imutável** compartilhado com o código chamado e suas sub-threads, com escopo bem definido (substitui `ThreadLocal` para esse caso):
```java
private static final ScopedValue<String> TENANT = ScopedValue.newInstance();

ScopedValue.where(TENANT, tenantId).run(() -> service.process());
// em qualquer ponto dentro: TENANT.get()
```
Em uma API Spring tradicional, o equivalente por request é `RequestContextHolder`/`SecurityContextHolder` — mantenha-os; Scoped Values valem para código novo com concorrência estruturada.

## Structured concurrency (preview em 25)

`StructuredTaskScope` trata um grupo de subtarefas concorrentes como uma unidade (cancela as irmãs se uma falha, sem vazar threads). **Segue em preview** no JDK 25: exige `--enable-preview` e a API pode mudar. Não use em produção do pack; considere para protótipos. Para paralelismo comum em produção, `CompletableFuture` com executor de virtual threads, ou chamadas sequenciais simples (muitas vezes bastam).

---

## Outras melhorias úteis (Java 22–25)

- **Unnamed variables** `_` (Java 22): `catch (IOException _)` e lambdas `(_, v) -> ...` quando o valor não é usado.
- **Flexible constructor bodies** (final em 25): permite validar/preparar argumentos *antes* do `super(...)`.
- **Compact source files / instance main** (final em 25): para scripts e ensino; a `Startup` do projeto continua como está.
- **Ahead-of-time cache / AppCDS** reduz o startup: veja `jvm-performance`.
- Use a **LTS** (17, 21, 25) em produção (`scaffold`, Step 3); features de versões não-LTS só valem se você migrar a cada 6 meses.

---

## Regras principais

- Records para dados imutáveis (eventos, respostas, projections, `ExceptionResponse`); **não** para entities nem para os DTOs de entidade deste pack.
- Sealed interface + `switch` exaustivo para resultados fechados, em vez de `null`/códigos mágicos.
- `Optional` só como retorno; `orElseThrow(domain exception)`, nunca `get()`.
- Virtual threads: ligue com `spring.threads.virtual.enabled`, **meça**, e continue dimensionando o pool de conexões; nunca faça pool delas; atenção a pinning em JDK < 24.
- Preview (`StructuredTaskScope`) fora da produção; Scoped Values (final em 25) para contexto imutável novo.
- Produção em versão **LTS**.
- Nenhuma feature nova justifica trocar o estilo explícito, sem Lombok, do pack.
