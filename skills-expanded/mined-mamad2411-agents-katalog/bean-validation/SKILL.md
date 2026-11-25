---
name: bean-validation
description: Validação de entrada com Jakarta Bean Validation no Spring Boot 4 — constraints nos DTOs, @Valid no body, constraints em @RequestParam/@PathVariable, handler que devolve 400 com erros por campo, a regra da interface *ControllerDocs e mensagens no idioma salvo do projeto. Use quando rejeitar input inválido ou quando um erro de validação vira 500.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) para as preferências do projeto, o package layout base e as convenções de code style.

# Bean Validation

Rejeite input inválido na borda da API com um `400` e uma mensagem por campo, em vez de deixar um `null` chegar ao database e voltar como um `500`. As constraints ficam nos **DTOs** (o que os clients enviam) e nos parâmetros do controller; as entities mantêm `@Column(nullable = false)` mais `hibernate.check_nullability: true` como última linha de defesa (veja `spring-data-jpa`).

---

## Idioma das mensagens

Nomes de campos, nomes de classes e todo outro identifier permanecem em inglês, independentemente do `message` da constraint. O **texto da mensagem em si** — o que o client de fato lê no map `errors` abaixo — segue a preferência "user-facing text language" de `code-organization`/`scaffold` (inglês por default; o desenvolvedor pode pedir português, espanhol ou qualquer outro idioma).

**Com inglês** (o default), nenhum trabalho extra é necessário: as mensagens built-in do próprio Hibernate Validator (`must not be blank`, `must be greater than 0`…) já estão em inglês, então as constraints dos exemplos desta skill não precisam de `message` explícito.

**Com qualquer outro idioma**, **não** conte com o message bundle default do Hibernate Validator — ele só existe em inglês, e o padrão do projeto prefere um `message = "..."` explícito a um resource bundle `ValidationMessages.properties` mais locale negotiation (mais partes móveis para o mesmo resultado, e este estilo de projeto não faz negociação de locale de response em nenhum outro lugar). Dê a cada constraint o seu próprio `message` traduzido:

```java
public class BookDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    @NotBlank(message = "não pode estar em branco")
    @Size(max = 180, message = "deve ter no máximo 180 caracteres")
    private String author;

    @NotNull(message = "não pode ser nulo")
    @PastOrPresent(message = "deve ser uma data no passado ou no presente")
    private LocalDate launchDate;

    @NotNull(message = "não pode ser nulo")
    @Positive(message = "deve ser maior que zero")
    private BigDecimal price;

    @NotBlank(message = "não pode estar em branco")
    @Size(max = 250, message = "deve ter no máximo 250 caracteres")
    private String title;

    public BookDTO() {}

    // getters, setters, equals, hashCode
}
```
O mesmo `BookDTO` mostrado no resto desta skill mantém a forma em inglês, sem messages — troque por messages explícitas como as acima sempre que a preferência salva não for inglês.

---

## Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```
Sem version (gerenciada pelo Boot BOM — veja `maven-config`). Ela traz o Hibernate Validator e a API `jakarta.validation`. Nada mais para configurar.

---

## Constraints no DTO

Anote os campos do DTO com annotations de `jakarta.validation.constraints`. O DTO mantém seus getters/setters explícitos (sem Lombok):

```java
public class BookDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    @NotBlank
    @Size(max = 180)
    private String author;

    @NotNull
    @PastOrPresent
    private LocalDate launchDate;

    @NotNull
    @Positive
    private BigDecimal price;

    @NotBlank
    @Size(max = 250)
    private String title;

    public BookDTO() {}

    // getters, setters, equals, hashCode
}
```

Para dinheiro (`BigDecimal`), combine `@Positive` com `@Digits(integer = …, fraction = 2)` quando quiser rejeitar mais de duas casas decimais com um 400 em vez de arredondar em silêncio no banco.

Constraints comuns: `@NotNull` (qualquer tipo), `@NotBlank` (texto: não nulo, não vazio, não somente espaços), `@NotEmpty` (collections), `@Size(min, max)`, `@Min`/`@Max`, `@Positive`/`@PositiveOrZero`, `@Email`, `@Pattern(regexp = ...)`, `@Past`/`@PastOrPresent`/`@Future`. Dê um `message = "..."` quando o texto default não for bom o bastante para o client.

Faça as constraints casarem com a migration: `@Size(max = 250)` em um campo cuja coluna é `varchar(250)` transforma um erro de database em um 400 claro.

Objetos aninhados e collections só são validados quando o campo está anotado com `@Valid` (`@Valid private Address address;`, `private List<@Valid Item> items;`).

O `springdoc` lê estas annotations e as documenta no schema OpenAPI (`required`, `maxLength`, `exclusiveMinimum`) sem nenhum trabalho extra.

---

## Validando a request

### Request body
Adicione `@Valid` ao parâmetro `@RequestBody`. A validation roda depois que o body é parseado, então funciona igual para JSON, XML e YAML:

```java
@PostMapping
@Override
public BookDTO create(@Valid @RequestBody BookDTO book) {
    return service.create(book);
}
```
Em caso de falha, o Spring lança `MethodArgumentNotValidException`.

### Path variables e query parameters
Coloque a constraint no parâmetro. O Spring Framework 6.1+ valida os parâmetros dos métodos do controller por conta própria — **não é necessário `@Validated` na classe** — e lança `HandlerMethodValidationException`:

```java
@GetMapping
public String findAll(
        @RequestParam(value = "page", defaultValue = "0") @Min(0) Integer page,
        @RequestParam(value = "size", defaultValue = "12") @Min(1) @Max(100) Integer size) {
    ...
}
```

### Com a interface `*ControllerDocs`: declare a validation na interface, não no override

*Este é o trade-off de escolher a interface na pergunta do Swagger: a interface e o Bean Validation só convivem se as annotations de validation ficarem na interface. Lembre o desenvolvedor disso se ele escolheu a interface e agora está adicionando validation, e, se ele estiver indeciso, ofereça annotations direto no controller como alternativa.*

O Hibernate Validator proíbe que um método que faz override redefina as parameter constraints do método que ele sobrescreve. Se o controller implementa uma interface `*ControllerDocs`, coloque **toda** annotation de validation em nível de parâmetro — `@Valid`, `@Min`, `@Max`, `@NotBlank` … — no método da **interface**, e deixe o override do controller sem elas. Declará-las no método do controller falha em tempo de request com um `500` (`HV000151: A method overriding another method must not redefine the parameter constraint configuration`) — e falha para o controller inteiro, não só para o método infrator. O Spring MVC pega as annotations da interface.

```java
public interface BookControllerDocs {

    BookDTO create(@Valid @RequestBody BookDTO book);

    String findAll(
        @RequestParam(value = "page", defaultValue = "0") @Min(0) Integer page,
        @RequestParam(value = "size", defaultValue = "12") @Min(1) @Max(100) Integer size);
}
```
```java
@Override
public BookDTO create(@RequestBody BookDTO book) {
    return service.create(book);
}
```
Quando o projeto mantém as annotations do Swagger no controller (sem interface), as annotations de validation ficam no método do controller, como nos exemplos anteriores.

---

## Transformando falhas em um 400 útil

O `ResponseEntityExceptionHandler` (que já é a base do handler global — veja `exception-handling`) responde às duas exceptions com um `ProblemDetail` genérico (`detail: "Invalid request content."`) que não diz *qual* campo falhou. Faça override dos dois hooks para adicionar as mensagens dos campos como uma property `errors`. `"Validation failed"` é, ele mesmo, texto voltado ao usuário — traduza-o também quando o idioma salvo não for inglês (`"Falha na validação"` abaixo):

```java
@Override
protected ResponseEntity<Object> handleMethodArgumentNotValid(
        MethodArgumentNotValidException ex, HttpHeaders headers, HttpStatusCode status, WebRequest request) {
    Map<String, String> errors = new LinkedHashMap<>();
    ex.getBindingResult().getFieldErrors()
            .forEach(error -> errors.putIfAbsent(error.getField(), error.getDefaultMessage()));
    var problem = ProblemDetail.forStatusAndDetail(status, "Validation failed");
    problem.setProperty("errors", errors);
    return handleExceptionInternal(ex, problem, headers, status, request);
}

@Override
protected ResponseEntity<Object> handleHandlerMethodValidationException(
        HandlerMethodValidationException ex, HttpHeaders headers, HttpStatusCode status, WebRequest request) {
    Map<String, String> errors = new LinkedHashMap<>();
    ex.getParameterValidationResults().forEach(result -> {
        var name = result.getMethodParameter().getParameterName();
        result.getResolvableErrors().forEach(error -> errors.putIfAbsent(name, error.getDefaultMessage()));
    });
    var problem = ProblemDetail.forStatusAndDetail(status, "Validation failed");
    problem.setProperty("errors", errors);
    return handleExceptionInternal(ex, problem, headers, status, request);
}
```
Imports: `org.springframework.web.bind.MethodArgumentNotValidException`, `org.springframework.web.method.annotation.HandlerMethodValidationException`, `org.springframework.http.ProblemDetail`, `org.springframework.http.HttpHeaders`, `org.springframework.http.HttpStatusCode`, `org.springframework.web.context.request.WebRequest`, `java.util.LinkedHashMap`, `java.util.Map`. Os dois métodos vão no `CustomEntityResponseHandler` existente, ao lado do override de `createResponseEntity` que restaura `type: about:blank`.

Responses resultantes (`application/problem+json`):
```json
{
  "detail": "Validation failed",
  "instance": "/api/book/v1",
  "status": 400,
  "title": "Bad Request",
  "type": "about:blank",
  "errors": {
    "title": "must not be blank",
    "price": "must be greater than 0",
    "launchDate": "must be a date in the past or in the present",
    "author": "must not be blank"
  }
}
```
```json
{
  "detail": "Validation failed",
  "instance": "/api/book/v1",
  "status": 400,
  "title": "Bad Request",
  "type": "about:blank",
  "errors": {
    "size": "must be less than or equal to 100"
  }
}
```
A ordem dos campos dentro de `errors` não é garantida pelo Hibernate Validator; clients e testes devem buscar as mensagens pelo nome do campo. As properties padrão do `ProblemDetail` são escritas em ordem alfabética (default do Jackson 3), com as extension properties depois delas.

Mesma response com a preferência de idioma definida como português — `detail` e todo valor dentro de `errors` são traduzidos; `title` e `type` são texto do próprio framework Spring e permanecem como estão:
```json
{
  "detail": "Falha na validação",
  "instance": "/api/book/v1",
  "status": 400,
  "title": "Bad Request",
  "type": "about:blank",
  "errors": {
    "title": "não pode estar em branco",
    "price": "deve ser maior que zero",
    "launchDate": "deve ser uma data no passado ou no presente",
    "author": "não pode estar em branco"
  }
}
```

---

## Onde a validation para

- Constraints verificam **forma** (null, size, range, format). Regras de negócio que precisam de dados — "title já existe", "estoque insuficiente" — pertencem ao service, lançadas como domain exceptions (`BadRequestException`, veja `exception-handling`).
- Não valide entities retornadas do repository; valide o que entra na API.
- Um DTO de `PUT`/`PATCH` normalmente precisa de constraints mais frouxas que um DTO de `POST` (um `id` é obrigatório no update, ausente no create). Use validation groups ou request DTOs separados — não enfraqueça as constraints para os dois.

---

## Regras principais

- `spring-boot-starter-validation` — nunca confie em um validator que só por acaso está no classpath por causa de outra library.
- Constraints nos DTOs e nos parâmetros do controller; as entities mantêm `@Column(nullable = false)` e `check_nullability: true`.
- Os `message`s das constraints (e o texto `"Validation failed"` do handler) seguem o user-facing text language salvo — inglês não precisa de `message` explícito (os defaults do Hibernate Validator já estão em inglês); qualquer outro idioma precisa de um em cada constraint.
- `@Valid` em todo `@RequestBody`; constraints direto nos parâmetros `@RequestParam`/`@PathVariable` (sem `@Validated` em nível de classe).
- Com uma interface `*ControllerDocs`, `@Valid` e as parameter constraints vão **somente** no método da **interface** — no override elas causam um 500 (`HV000151`).
- Faça override de `handleMethodArgumentNotValid` **e** de `handleHandlerMethodValidationException` — o primeiro cobre bodies, o segundo cobre parâmetros.
- Erros de input do client são 400, nunca 500.
- Busque as mensagens pelo nome do campo; nunca dependa da ordem delas.
- **Sem Lombok** — escolha deliberada.
