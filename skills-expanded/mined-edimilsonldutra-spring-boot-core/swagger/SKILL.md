---
name: swagger
description: Swagger/OpenAPI com springdoc 3 no Spring Boot 4 — interface *ControllerDocs ou annotations no controller, configuração do springdoc (OpenAPI 3.1), OpenApiConfig, Bearer JWT no Swagger UI, rotas públicas no SecurityConfig, conjunto padrão de @ApiResponse e textos no idioma salvo. Use quando documentar endpoints ou quando o Swagger UI não abrir.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) para as preferências do projeto, o package layout base e as convenções de code style.

# Swagger / OpenAPI

springdoc OpenAPI 3 (springdoc **3.x** é a linha para o Spring Boot 4; springdoc 2.x é para o Boot 3). O Swagger UI é servido em `/swagger-ui/index.html`.

---

## Antes de escrever qualquer annotation — onde elas ficam?

Se `## Project preferences` no `CLAUDE.md` do projeto (ou o Step 0 de `code-organization`) já respondeu isto, use a resposta. Caso contrário, pergunte uma vez:

**"As annotations de Swagger/OpenAPI devem ficar em uma interface `*ControllerDocs` separada que o controller implementa (mantém os controllers limpos), ou direto nos métodos do controller?"**

- **Interface (default):** todo `@Operation`, `@ApiResponse` e `@Parameter` vive em `*ControllerDocs`; o controller a implementa e não tem annotations de Swagger em seus métodos. **Trade-off a dizer ao desenvolvedor antes de ele escolher:** Bean Validation e a interface não se misturam livremente. O Hibernate Validator proíbe que um método que faz override redefina parameter constraints, então com a interface todo `@Valid`, `@Min`, `@NotBlank`… em um parâmetro de controller deve ser declarado **no método da interface** e **não no override do controller** — coloque no override e o controller inteiro responde 500 (`HV000151`). Funciona, mas as annotations de validation vivem na interface de docs, longe do código do controller (veja `bean-validation`).
- **Direto no controller:** as mesmas annotations ficam nos métodos do controller; sem interface `*ControllerDocs`. As annotations de Bean Validation ficam nos parâmetros do controller, sem restrição. Todo o resto desta skill (config, conjunto de responses, rotas de security) é idêntico.

Salve a resposta com as outras preferências quando o desenvolvedor concordar.

---

## Idioma do texto na documentação

`summary`, `description` (em `@Operation` e em todo `@ApiResponse`) e o `Info` do `OpenApiConfig` (`title`, `description`) são texto que um client lê no Swagger UI — escreva-os no idioma da preferência "user-facing text language" de `code-organization`/`scaffold` (inglês por default, mostrado ao longo desta skill). Os `tags` permanecem em inglês independentemente: eles funcionam como uma chave de agrupamento estável entre todo controller do mesmo recurso, o mesmo papel que um identifier desempenha, não prosa que o client deva ler como uma frase.

A operação `findById` do pattern abaixo, com a preferência definida como português:
```java
@Operation(summary = "Busca um Book",
    description = "Busca um Book específico pelo seu ID",
    tags = {"Book"},
    responses = {
        @ApiResponse(description = "Sucesso", responseCode = "200",
            content = @Content(schema = @Schema(implementation = BookDTO.class))),
        @ApiResponse(description = "Requisição Inválida",  responseCode = "400", content = @Content),
        @ApiResponse(description = "Acesso Proibido",      responseCode = "403", content = @Content),
        @ApiResponse(description = "Não Encontrado",       responseCode = "404", content = @Content),
        @ApiResponse(description = "Erro Interno do Servidor", responseCode = "500", content = @Content)
    })
BookDTO findById(@PathVariable("id") Long id);
```
Toda outra operação nos exemplos desta skill se traduz do mesmo jeito — `summary`/`description`/`@ApiResponse(description = ...)` mudam; `tags`, nomes de parâmetros e todo o resto permanecem como mostrado.

---

## Dependency

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>${springdoc.version}</version>
</dependency>
```

Version não gerenciada pelo Spring Boot BOM — sempre declare-a em `<properties>` e use a linha 3.x para o Boot 4 (veja `maven-config`). Se a API também expõe tipos HATEOAS, o projeto precisa do `spring-boot-starter-hateoas` para esses tipos, não para o springdoc em si.

---

## application.yml

```yaml
springdoc:
  api-docs:
    enabled: true
  paths-to-match:
    - /auth/**
    - /api/**/v1/**
  swagger-ui:
    enabled: true
```

- `api-docs.enabled` e `swagger-ui.enabled` são definidos como `true` (seu default) somente porque o springdoc 3 loga um warning de startup quando eles ficam implícitos.
- `paths-to-match` — expõe somente endpoints de auth e da API versionada. Exclui paths internos. É honrado somente sob a chave correta: `springdoc`, **não** `spring-doc` (uma chave errada é ignorada silenciosamente, então tudo é exposto).
- **URL do Swagger UI:** `/swagger-ui/index.html`. O antigo `/swagger-ui.html` redireciona para lá. `swagger-ui.use-root-path: true` move a UI para `/`, mas `/` então também precisa ser público no `SecurityConfig` ou responde 403 — prefira o path default, que também é o que testes, readiness checks de CI e READMEs devem usar.
- `/v3/api-docs` é um documento **OpenAPI 3.1** com o springdoc 3 (era 3.0 com o springdoc 2). Consumers que só entendem 3.0 podem ser atendidos com `springdoc.api-docs.version: openapi_3_0`; não o adicione a menos que exista um.

---

## OpenApiConfig

```java
@Configuration
public class OpenApiConfig {

    @Bean
    OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("My API")
                .version("v1")
                .description("What the API does, in one sentence")
                .termsOfService("https://example.com/terms")
                .license(new License()
                    .name("Apache 2.0")
                    .url("https://example.com/license")
                )
            );
    }
}
```
Os imports vêm de `io.swagger.v3.oas.models` (`OpenAPI`, `info.Info`, `info.License`). Use o nome real do projeto, a descrição e as URLs — `title` e `description` seguem a preferência de user-facing text language, igual ao texto de todo `@Operation`/`@ApiResponse` (veja "Idioma do texto na documentação" acima).

---

## Autenticação no Swagger UI (Bearer JWT)

Quando o projeto tem JWT (`authentication`), declare o security scheme para que o Swagger UI mostre o botão **Authorize** e envie o header `Authorization: Bearer <token>` nos "Try it out". Em `OpenApiConfig`, adicione ao `OpenAPI`:

```java
@Bean
OpenAPI customOpenAPI() {
    return new OpenAPI()
        .components(new Components()
            .addSecuritySchemes("bearerAuth", new SecurityScheme()
                .type(SecurityScheme.Type.HTTP)
                .scheme("bearer")
                .bearerFormat("JWT")))
        .addSecurityItem(new SecurityRequirement().addList("bearerAuth"))
        .info(new Info()
            .title("My API")
            .version("v1"));
}
```
Imports: `io.swagger.v3.oas.models.Components`, `io.swagger.v3.oas.models.security.SecurityScheme`, `io.swagger.v3.oas.models.security.SecurityRequirement`. `addSecurityItem` aplica o requisito a **todas** as operações; para endpoints públicos (`/auth/signin`), anote a operação com `@SecurityRequirements` vazio (`io.swagger.v3.oas.annotations.security.SecurityRequirements`) para removê-lo. O texto do `Info` segue o idioma salvo. Em produção considere desabilitar o Swagger UI ou protegê-lo (`springdoc.swagger-ui.enabled: false` por profile) — ele documenta toda a superfície da sua API.

---

## SecurityConfig — rotas públicas do Swagger

Quando o projeto usa Spring Security, adicione estas a `permitAll()` para que o Swagger UI seja acessível sem autenticação. Qualquer coisa não casada por uma regra explícita é negada:

```java
.requestMatchers(
    "/auth/signin",
    "/auth/refresh/**",
    "/auth/createUser",
    "/swagger-ui/**",
    "/v3/api-docs/**"
).permitAll()
```
Sem Spring Security, nada precisa ser configurado.

---

## Annotations na interface `*ControllerDocs` (default)

Todas as annotations `@Operation`, `@ApiResponse`, `@Parameter` e `@Tag` vivem aqui. O controller implementa a interface e fica limpo.

> Os exemplos abaixo declaram JSON, XML ou YAML — isso só vale quando o projeto escolheu os três (veja [`../web-config/SKILL.md`](../web-config/SKILL.md)). Se o projeto é somente JSON, remova as menções a XML/YAML das descrições de `@Operation` e as entradas XML/YAML de `produces`/`consumes`.

### Pattern CRUD padrão

```java
public interface BookControllerDocs {

    @Operation(summary = "Find All Books",
        description = "Finds All Books",
        tags = {"Book"},
        responses = {
            @ApiResponse(description = "Success", responseCode = "200",
                content = @Content(
                    mediaType = MediaType.APPLICATION_JSON_VALUE,
                    array = @ArraySchema(schema = @Schema(implementation = BookDTO.class)))),
            @ApiResponse(description = "Bad Request",           responseCode = "400", content = @Content),
            @ApiResponse(description = "Forbidden",             responseCode = "403", content = @Content),
            @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
        })
    ResponseEntity<PagedModel<EntityModel<BookDTO>>> findAll(
        @RequestParam(value = "page",      defaultValue = "0")   Integer page,
        @RequestParam(value = "size",      defaultValue = "12")  Integer size,
        @RequestParam(value = "direction", defaultValue = "asc") String direction);

    @Operation(summary = "Finds a Book",
        description = "Find a specific Book by its ID",
        tags = {"Book"},
        responses = {
            @ApiResponse(description = "Success", responseCode = "200",
                content = @Content(schema = @Schema(implementation = BookDTO.class))),
            @ApiResponse(description = "Bad Request",           responseCode = "400", content = @Content),
            @ApiResponse(description = "Forbidden",             responseCode = "403", content = @Content),
            @ApiResponse(description = "Not Found",             responseCode = "404", content = @Content),
            @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
        })
    BookDTO findById(@PathVariable("id") Long id);

    @Operation(summary = "Create a Book",
        description = "Creates a new Book by passing in a JSON, XML or YAML representation",
        tags = {"Book"},
        responses = {
            @ApiResponse(description = "Success", responseCode = "200",
                content = @Content(schema = @Schema(implementation = BookDTO.class))),
            @ApiResponse(description = "Bad Request",           responseCode = "400", content = @Content),
            @ApiResponse(description = "Forbidden",             responseCode = "403", content = @Content),
            @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
        })
    BookDTO create(@RequestBody BookDTO book);

    @Operation(summary = "Update a Book",
        description = "Updates a Book by passing in a JSON, XML or YAML representation",
        tags = {"Book"},
        responses = {
            @ApiResponse(description = "Success", responseCode = "200",
                content = @Content(schema = @Schema(implementation = BookDTO.class))),
            @ApiResponse(description = "Bad Request",           responseCode = "400", content = @Content),
            @ApiResponse(description = "Forbidden",             responseCode = "403", content = @Content),
            @ApiResponse(description = "Not Found",             responseCode = "404", content = @Content),
            @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
        })
    BookDTO update(@RequestBody BookDTO book);

    @Operation(summary = "Delete a Book",
        description = "Deletes a Book by its ID",
        tags = {"Book"},
        responses = {
            @ApiResponse(description = "No Content",            responseCode = "204", content = @Content),
            @ApiResponse(description = "Bad Request",           responseCode = "400", content = @Content),
            @ApiResponse(description = "Forbidden",             responseCode = "403", content = @Content),
            @ApiResponse(description = "Not Found",             responseCode = "404", content = @Content),
            @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
        })
    ResponseEntity<?> delete(@PathVariable("id") Long id);
}
```

Documente o status que o controller **realmente** retorna: o `create` desta API responde `200`, então sua response é `200`, não `201`. Se você mudar um controller para retornar `201`, mude a documentação dele também.

### Endpoints de arquivo (quando o projeto tem file import/export)

```java
@Operation(summary = "Export Books",
    description = "Export a Page of Books in XLSX, CSV or PDF format",
    tags = {"Book"},
    responses = {
        @ApiResponse(description = "Success", responseCode = "200",
            content = {
                @Content(mediaType = MediaTypes.APPLICATION_XLSX_VALUE),
                @Content(mediaType = MediaTypes.APPLICATION_CSV_VALUE),
                @Content(mediaType = MediaTypes.APPLICATION_PDF_VALUE)
            }),
        @ApiResponse(description = "Forbidden",             responseCode = "403", content = @Content),
        @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
    })
ResponseEntity<Resource> exportPage(
    @RequestParam(value = "page",      defaultValue = "0")   Integer page,
    @RequestParam(value = "size",      defaultValue = "12")  Integer size,
    @RequestParam(value = "direction", defaultValue = "asc") String direction,
    HttpServletRequest request);
```

```java
@Operation(summary = "Massive Creation",
    description = "Massive Creation by uploading a XLSX or CSV file",
    tags = {"Book"},
    responses = {
        @ApiResponse(description = "Success", responseCode = "200",
            content = @Content(schema = @Schema(implementation = BookDTO.class))),
        @ApiResponse(description = "Bad Request",           responseCode = "400", content = @Content),
        @ApiResponse(description = "Forbidden",             responseCode = "403", content = @Content),
        @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
    })
List<BookDTO> massCreation(@RequestParam("file") MultipartFile file);
```

### Controller — somente `@Tag` em nível de classe

O controller declara `@Tag` em nível de classe (uma vez — não repetido na interface) e implementa a interface de docs. Sem `@Operation` nem `@ApiResponse` nos métodos.

```java
@RestController
@RequestMapping("/api/book/v1")
@Tag(name = "Book", description = "Endpoints for Managing Books")
public class BookController implements BookControllerDocs {

    @Autowired
    private BookService service;

    @GetMapping(value = "/{id}", produces = {
            MediaType.APPLICATION_JSON_VALUE,
            MediaType.APPLICATION_XML_VALUE,
            MediaType.APPLICATION_YAML_VALUE})
    @Override
    public BookDTO findById(@PathVariable("id") Long id) {
        return service.findById(id);
    }
}
```
O `produces` acima assume que JSON + XML + YAML foram todos escolhidos; use somente `MediaType.APPLICATION_JSON_VALUE` quando o projeto é somente JSON.

---

## Annotations direto no controller (alternativa)

As mesmas annotations, no método, e sem interface:

```java
@RestController
@RequestMapping("/api/book/v1")
@Tag(name = "Book", description = "Endpoints for Managing Books")
public class BookController {

    @Autowired
    private BookService service;

    @Operation(summary = "Finds a Book",
        description = "Find a specific Book by its ID",
        responses = {
            @ApiResponse(description = "Success", responseCode = "200",
                content = @Content(schema = @Schema(implementation = BookDTO.class))),
            @ApiResponse(description = "Not Found", responseCode = "404", content = @Content),
            @ApiResponse(description = "Internal Server Error", responseCode = "500", content = @Content)
        })
    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public BookDTO findById(@PathVariable("id") Long id) {
        return service.findById(id);
    }
}
```
Pule `tags = {...}` dentro de `@Operation` quando `@Tag` está na classe. Mantenha os métodos legíveis: quando um controller tem mais que um punhado de operações, a variante com interface escala melhor.

---

## Conjunto padrão de @ApiResponse

Todo endpoint usa este conjunto — adicione ou remova códigos conforme apropriado por operação:

| Código | Descrição         | Tem body |
|--------|-------------------|----------|
| 200  | Success           | Sim      |
| 204  | No Content        | Não      |
| 400  | Bad Request       | Erros do framework: `ProblemDetail`; erros de domínio: `ExceptionResponse` (veja `exception-handling`) |
| 403  | Forbidden         | **Não** — body vazio |
| 404  | Not Found         | `ExceptionResponse` |
| 500  | Internal Server Error | `ExceptionResponse` |

**403, não 401.** Com o JWT filter descrito em `authentication`, uma request com token ausente, malformado, expirado ou com assinatura errada é respondida com um **403 de body vazio** nos paths protegidos; o default do Spring Security não produz 401 aqui. Documente o que a API realmente retorna: use `403` em endpoints protegidos, e omita-o nos públicos. Um projeto que adiciona um `AuthenticationEntryPoint` retornando 401 deve documentar 401 no lugar.

`content = @Content` sem argumentos significa que a response não tem body (o springdoc caso contrário infere um).
`content = @Content(schema = @Schema(implementation = SomeDTO.class))` para responses de objeto único.
`content = @Content(mediaType = ..., array = @ArraySchema(...))` para responses de lista.

---

## Regras principais

- Pergunte (ou leia das preferências salvas) se as annotations vão em uma interface `*ControllerDocs` ou no controller — depois seja consistente no projeto inteiro.
- Variante com interface: zero annotations de Swagger nos métodos do controller; `@Tag` declarado uma vez, na classe do controller.
- `summary`/`description`/`@ApiResponse(description = ...)`/`Info.title`/`Info.description` seguem o user-facing text language salvo; `tags` permanecem em inglês — são uma chave de agrupamento, não prosa.
- springdoc **3.x** para o Spring Boot 4; `springdoc` (não `spring-doc`) no `application.yml` — a chave errada é ignorada silenciosamente.
- `api-docs.enabled: true` e `swagger-ui.enabled: true` explícitos; a UI vive em `/swagger-ui/index.html`.
- `/v3/api-docs` é OpenAPI 3.1 por default.
- `/swagger-ui/**` e `/v3/api-docs/**` sempre em `SecurityConfig.permitAll()` quando o Spring Security está presente.
- `springdoc.paths-to-match` limita os paths expostos a `/auth/**` e `/api/**/v1/**`.
- Documente os status codes reais: 403 sem body para tokens ausentes/inválidos; o status que o controller de fato retorna.
- Endpoints de export referenciam `MediaTypes.APPLICATION_XLSX_VALUE` etc. da sua interface `MediaTypes` — não strings hardcoded.
- `content = @Content` (sem args) = sem response body. Nunca o omita em responses de erro.
