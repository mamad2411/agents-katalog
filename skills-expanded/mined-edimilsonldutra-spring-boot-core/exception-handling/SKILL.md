---
name: exception-handling
description: Tratamento global de erros no Spring Boot 4 / Spring 7 — record ExceptionResponse, domain exceptions com @ResponseStatus, @ControllerAdvice com um handler por exception, fix do type do ProblemDetail, os dois formatos de erro, o que nunca chega ao handler e mensagens no idioma salvo. Use quando padronizar respostas de erro (404, 400, 500) ou investigar um erro no formato errado.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) para as preferências do projeto, o package layout base e as convenções de code style.

# Exception Handling

Exception handling centralizado via `@ControllerAdvice` + `@RestController`. As domain exceptions usam `@ResponseStatus`. Cada exception recebe o seu próprio `@ExceptionHandler` dedicado — sem handler compartilhado para domain exceptions, mais um catch-all para qualquer coisa inesperada.

Os clients recebem **dois** formatos de erro, e a skill precisa ser honesta sobre isso:
- `ExceptionResponse` — para domain exceptions e o catch-all (os handlers desta skill);
- O `ProblemDetail` do Spring — para erros que o próprio framework levanta antes de o seu código rodar (JSON body malformado, media type não suportado, parâmetro ausente…), produzido pelo `ResponseEntityExceptionHandler` que o handler estende.

---

## Package structure

```
br.com.padrao/
└── exception/
    ├── ExceptionResponse.java
    ├── ResourceNotFoundException.java
    ├── RequiredObjectIsNullException.java
    ├── BadRequestException.java
    └── handler/
        └── CustomEntityResponseHandler.java
```
As exceptions específicas de feature (abaixo) entram neste package quando a feature existe.

---

## ExceptionResponse

Declarado como um `record` — três campos: `timestamp`, `message`, `details`. Imutável por definição. O Jackson 3 mantém a ordem de properties declarada de um record.

```java
public record ExceptionResponse(Date timestamp, String message, String details) {}
```

---

## Domain exceptions

Cada exception declara seu status HTTP via `@ResponseStatus`, declara `serialVersionUID` (exceptions são `Serializable`) e delega para `super(message)`. Todas estendem `RuntimeException`, a menos que uma base class do framework seja necessária.

**O texto da mensagem é voltado ao usuário** — ele termina literalmente em `ExceptionResponse.message()`, então segue a preferência "user-facing text language" de `code-organization`/`scaffold` (inglês por default; nomes de classes e campos permanecem em inglês independentemente). Os nomes das classes, as assinaturas dos constructors e todo o resto abaixo não são afetados — só os string literals mudam:

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    public ResourceNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.BAD_REQUEST)
public class RequiredObjectIsNullException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    public RequiredObjectIsNullException() {
        super("It is not allowed to persist a null object!");
    }

    public RequiredObjectIsNullException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.BAD_REQUEST)
public class BadRequestException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    public BadRequestException(String message) {
        super(message);
    }
}
```
As mesmas três exceptions com a preferência de idioma definida como português — só a mensagem do constructor default de `RequiredObjectIsNullException` muda aqui, já que as outras duas sempre recebem a mensagem do ponto de chamada (veja "Como as exceptions são lançadas" abaixo):
```java
public RequiredObjectIsNullException() {
    super("Não é permitido persistir um objeto nulo!");
}
```

### Exceptions específicas de feature
Adicione-as somente quando o projeto tem a feature. Exceptions que encapsulam outra falha também recebem um constructor com `Throwable cause`, para que o stack trace original seja preservado:
```java
@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class FileStorageException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    public FileStorageException(String message) {
        super(message);
    }

    public FileStorageException(String message, Throwable cause) {
        super(message, cause);
    }
}

@ResponseStatus(HttpStatus.NOT_FOUND)
public class FileNotFoundException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    public FileNotFoundException(String message) {
        super(message);
    }

    public FileNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}
```
Com autenticação JWT, a exception de token inválido estende a `AuthenticationException` do Spring Security (ela mesma unchecked) para poder trafegar pela camada de security:
```java
@ResponseStatus(HttpStatus.FORBIDDEN)
public class InvalidJwtAuthenticationException extends AuthenticationException {

    private static final long serialVersionUID = 1L;

    public InvalidJwtAuthenticationException(String message) {
        super(message);
    }
}
```

---

## CustomEntityResponseHandler

Anotado com `@ControllerAdvice` e `@RestController`. Estende `ResponseEntityExceptionHandler`. Cada classe de exception recebe o seu próprio `@ExceptionHandler` — o parâmetro é sempre `Exception ex` (não o tipo específico), então o mesmo pattern se aplica uniformemente.

**O Spring Framework 7 exige um override.** Ele não define mais `ProblemDetail.type` como `about:blank` por default, então sem o `createResponseEntity` o campo `type` desaparece silenciosamente de todo body de erro do framework. Coloque-o de volta:

```java
@ControllerAdvice
@RestController
public class CustomEntityResponseHandler extends ResponseEntityExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(CustomEntityResponseHandler.class);

    @Override
    protected ResponseEntity<Object> createResponseEntity(
            Object body, HttpHeaders headers, HttpStatusCode statusCode, WebRequest request) {
        if (body instanceof ProblemDetail problemDetail && problemDetail.getType() == null) {
            problemDetail.setType(URI.create("about:blank"));
        }
        return super.createResponseEntity(body, headers, statusCode, request);
    }

    @ExceptionHandler(Exception.class)
    public final ResponseEntity<ExceptionResponse> handleAllExceptions(Exception ex, WebRequest request) {
        logger.error("Unexpected error on {}", request.getDescription(false), ex);
        ExceptionResponse response = new ExceptionResponse(
                new Date(),
                ex.getMessage(),
                request.getDescription(false));
        return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public final ResponseEntity<ExceptionResponse> handleNotFoundExceptions(Exception ex, WebRequest request) {
        ExceptionResponse response = new ExceptionResponse(
                new Date(),
                ex.getMessage(),
                request.getDescription(false));
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(RequiredObjectIsNullException.class)
    public final ResponseEntity<ExceptionResponse> handleRequiredObjectExceptions(Exception ex, WebRequest request) {
        ExceptionResponse response = new ExceptionResponse(
                new Date(),
                ex.getMessage(),
                request.getDescription(false));
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(BadRequestException.class)
    public final ResponseEntity<ExceptionResponse> handleBadRequestExceptions(Exception ex, WebRequest request) {
        ExceptionResponse response = new ExceptionResponse(
                new Date(),
                ex.getMessage(),
                request.getDescription(false));
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }
}
```

Imports: `org.springframework.http.HttpHeaders`, `HttpStatus`, `HttpStatusCode`, `ProblemDetail`, `ResponseEntity`; `org.springframework.web.context.request.WebRequest`; `org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler`; `java.net.URI`; `java.util.Date`.

Para cada exception específica de feature, adicione um handler no mesmo formato, com o status que a exception declara (`FileNotFoundException` → 404, `FileStorageException` → 500, `InvalidJwtAuthenticationException` → 403).

Falhas de Bean Validation (`MethodArgumentNotValidException`) também precisam de um handler — veja `bean-validation`.

---

## Os dois formatos de erro

Domain exception — `ExceptionResponse`:
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "message": "No records found for this ID!",
  "details": "uri=/api/book/v1/99"
}
```
`request.getDescription(false)` — `false` mantém somente a URI, remove a informação do client. O Jackson 3 escreve `Date` como ISO-8601 UTC terminando em `Z` (o Boot 3 escrevia `+00:00`).

Mesma response com a preferência de idioma definida como português — só `message` muda; `timestamp` e `details` não dependem de idioma:
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "message": "Nenhum registro encontrado para este ID!",
  "details": "uri=/api/book/v1/99"
}
```

Framework exception — `ProblemDetail`, servido como `application/problem+json` (por exemplo, um JSON body malformado → 400):
```json
{
  "detail": "Failed to read request",
  "instance": "/auth/signin",
  "status": 400,
  "title": "Bad Request",
  "type": "about:blank"
}
```
As properties vêm em ordem alfabética sob o Jackson 3. O texto de `detail` depende da exception. Clients (e testes) não devem assumir que todo erro tem `message`/`details`; erros do framework têm `type`/`title`/`status`/`detail`/`instance`.

Uma exception sem mapeamento lançada pelo seu código cai no catch-all e retorna 500 com `ExceptionResponse` e a mensagem bruta da exception. A falha de not-null do Hibernate (veja `check_nullability` em `spring-data-jpa`) é um desses casos — valide o input antes (veja `bean-validation`) para que os clients recebam um 400.

---

## Endurecimento do catch-all (produção)

O catch-all acima devolve `ex.getMessage()` ao client. Para exceptions **inesperadas** isso pode vazar detalhes internos (nome de tabela, constraint, host, trecho de SQL). O handler já **loga o stack trace completo** (sem isso, um 500 some sem deixar rastro); em produção, devolva ao client um texto genérico e deixe o detalhe só no log:

```java
ExceptionResponse response = new ExceptionResponse(
        new Date(),
        "Unexpected error. Contact support with the request details.",
        request.getDescription(false));
```
Mantenha `ex.getMessage()` somente para as domain exceptions (`ResourceNotFoundException`, `BadRequestException`…), cuja mensagem foi escrita para o client. O texto genérico também é user-facing: siga o idioma salvo. Correlacione client e log com um trace id (veja `observability`).

---

## Erros que nunca chegam ao handler

O `@ControllerAdvice` só enxerga exceptions lançadas de dentro do dispatch do MVC. Não prometa mais que isso:
- **Falhas em nível de filter.** Uma exception lançada por um servlet filter — por exemplo o JWT filter — roda antes do `ExceptionTranslationFilter` e do dispatcher, então nem `@ControllerAdvice` nem `@ResponseStatus` se aplicam. Um JWT filter portanto não deve lançar exception para um token ruim; ele ignora o token e deixa a request continuar sem autenticação, e o Spring Security responde com um **403 de body vazio** nos paths protegidos (veja `authentication`). Código que roda dentro de um controller (por exemplo um endpoint de refresh token) alcança o handler e responde com `ExceptionResponse`.
- Responses de **access denied / unauthenticated** vêm do Spring Security, não deste handler: body vazio.
- **Endpoints que só podem produzir um tipo não-JSON** (um download de arquivo pedido com `Accept: application/pdf`, por exemplo): se esse endpoint falha, o handler não consegue renderizar seu erro JSON/XML/YAML para aquele `Accept`, o error dispatch é bloqueado e o client vê uma response vazia. Adicione `application/json` ao header `Accept` para ver o erro real.

---

## Como as exceptions são lançadas

Sempre lançadas diretamente no corpo do método — nunca encapsuladas a não ser que mude o tipo. A mensagem passada no ponto de chamada também é texto voltado ao usuário — escreva-a no idioma da preferência de `code-organization`/`scaffold` (`"Nenhum registro encontrado para este ID!"`, `"Formato de arquivo inválido!"`, e assim por diante, com a preferência definida como português):

```java
var entity = repository.findById(id)
        .orElseThrow(() -> new ResourceNotFoundException("No records found for this ID!"));
```
```java
if (book == null) throw new RequiredObjectIsNullException();
```
```java
throw new BadRequestException("Invalid File Format!");
```
Relance como domain exception quando mudar o tipo, sempre mantendo a cause:
```java
catch (IOException e) {
    throw new FileStorageException("Error processing the file!", e);
}
```
Mapeie input ruim do **client** para um 400 (`BadRequestException`), não para um 500: um wrapper que transforma toda falha em `FileStorageException` também transforma um tipo de arquivo não suportado em um erro de servidor.

---

## Regras principais

- `ExceptionResponse` é um `record` — imutável, sem setters, sem boilerplate.
- `@ControllerAdvice` + `@RestController` juntos no handler — não `@RestControllerAdvice`.
- Cada exception recebe o seu próprio método `@ExceptionHandler` — sem compartilhamento.
- O parâmetro do handler é sempre `Exception ex`, independentemente de qual exception é capturada.
- Faça override de `createResponseEntity` e defina `type` como `about:blank` — o Spring Framework 7 não faz mais isso.
- Toda exception declara `serialVersionUID`; exceptions que encapsulam outras também recebem uma `cause`.
- Todas as exceptions são unchecked (`RuntimeException`, ou `AuthenticationException` para a do JWT).
- Toda `message` de exception — as dos constructors default e as passadas no ponto de lançamento — segue o user-facing text language salvo; nomes de classes/campos permanecem em inglês independentemente.
- Erros de client → 4xx (`BadRequestException`, `RequiredObjectIsNullException`), nunca 500.
- Nunca lance exception de um servlet filter para reportar um token ruim.
- O catch-all sempre **loga** a exception (stack trace) e, em produção, não devolve `ex.getMessage()` de exceptions inesperadas ao client.
- **Sem Lombok** — escolha deliberada.
