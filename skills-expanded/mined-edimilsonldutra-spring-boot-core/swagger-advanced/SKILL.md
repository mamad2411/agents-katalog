---
name: swagger-advanced
description: OpenAPI avançado com springdoc 3 no Spring Boot 4 — grupos por versão ou domínio (GroupedOpenApi), respostas de erro comuns aplicadas por OpenApiCustomizer, schemas de ExceptionResponse e ProblemDetail, @Schema com exemplos e campos read-only, @ExampleObject, parâmetros reutilizáveis, @Hidden, servers, exportar o openapi.json no build, lint, detecção de breaking change, geração de clients e Swagger UI por ambiente. Use quando a documentação básica do swagger não bastar ou quando o OpenAPI virar contrato consumido por outros times.
---

Antes de aplicar este pattern, leia também [`../swagger/SKILL.md`](../swagger/SKILL.md) (a base: dependency, `OpenApiConfig`, interface `*ControllerDocs`, conjunto padrão de respostas, rotas públicas), [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md). Versões: [`../api-versioning/SKILL.md`](../api-versioning/SKILL.md). Contratos: [`../contract-testing/SKILL.md`](../contract-testing/SKILL.md).

# Swagger / OpenAPI avançado

A skill `swagger` documenta cada endpoint. Esta trata o OpenAPI como **contrato**: organizado, sem repetição, com exemplos reais, versionado no repositório, verificado no CI e usado para **gerar clients**. Tudo aqui é adicional — nada muda as regras da `swagger` (idioma dos textos, `tags` em inglês, interface `*ControllerDocs`, `content = @Content` em erros sem body).

## 1. Grupos (por versão ou por domínio)

Com várias versões ou muitos domínios, um único documento vira uma lista gigante. `GroupedOpenApi` gera um documento por grupo, e o Swagger UI mostra um seletor:

```java
@Configuration
public class OpenApiGroupsConfig {

    @Bean
    GroupedOpenApi v1() {
        return GroupedOpenApi.builder()
            .group("v1")
            .pathsToMatch("/api/**/v1/**")
            .build();
    }

    @Bean
    GroupedOpenApi v2() {
        return GroupedOpenApi.builder()
            .group("v2")
            .pathsToMatch("/api/**/v2/**")
            .build();
    }

    @Bean
    GroupedOpenApi auth() {
        return GroupedOpenApi.builder()
            .group("auth")
            .pathsToMatch("/auth/**")
            .build();
    }
}
```
- Cada grupo fica em `/v3/api-docs/<grupo>`; o Swagger UI continua em `/swagger-ui/index.html`.
- Com grupos definidos, o `springdoc.paths-to-match` global da `swagger` deixa de ser o filtro principal — mantenha os dois coerentes (ou remova o global) para não esconder um grupo sem perceber.
- Agrupe por **versão** (`api-versioning`) quando os clients consomem uma versão; por **domínio** (`books`, `loans`) quando a API é grande e de uma versão só.

---

## 2. Respostas de erro sem repetição

O conjunto padrão da `swagger` (400, 403, 404, 500) repete as mesmas linhas em toda operação. Um `OpenApiCustomizer` registra os schemas de erro uma vez e adiciona as respostas comuns a todas as operações que ainda não as declaram:

```java
@Bean
OpenApiCustomizer commonErrorResponses() {
    return openApi -> {
        var components = openApi.getComponents();
        components.addSchemas("ExceptionResponse", new Schema<>()
            .type("object")
            .addProperty("timestamp", new StringSchema().format("date-time"))
            .addProperty("message", new StringSchema())
            .addProperty("details", new StringSchema()));

        var errorContent = new Content().addMediaType(MediaType.APPLICATION_JSON_VALUE,
            new io.swagger.v3.oas.models.media.MediaType().schema(new Schema<>().$ref("#/components/schemas/ExceptionResponse")));

        openApi.getPaths().values().forEach(path -> path.readOperations().forEach(operation -> {
            var responses = operation.getResponses();
            responses.putIfAbsent("403", new ApiResponse().description("Forbidden"));
            responses.putIfAbsent("500", new ApiResponse().description("Internal Server Error").content(errorContent));
        }));
    };
}
```
- `putIfAbsent`: uma operação que documenta o próprio `404` (com descrição específica) não é sobrescrita.
- **403 sem body** (é o que a API realmente devolve — `swagger`, "403, não 401"); **500 e 404 com `ExceptionResponse`**; erros do framework (corpo malformado, tipo não suportado) com **`ProblemDetail`** — documente esse schema também (campos `type`, `title`, `status`, `detail`, `instance`) para os `400` que o Spring gera (`exception-handling`).
- Endpoints públicos (`/auth/**`) não devolvem 403: filtre-os no customizer pelo path.
- Textos (`description`) seguem o idioma salvo.
- Para aplicar só a um grupo, use `GroupedOpenApi.builder()...addOpenApiCustomizer(...)`.

---

## 3. Schemas melhores no DTO

```java
public class BookDTO implements Serializable {

    @Schema(description = "Generated identifier", example = "1", accessMode = Schema.AccessMode.READ_ONLY)
    private Long id;

    @Schema(description = "Book title", example = "Clean Code", maxLength = 250, requiredMode = Schema.RequiredMode.REQUIRED)
    private String title;

    @Schema(description = "Price in BRL", example = "77.00", minimum = "0")
    private BigDecimal price;

    @Schema(description = "Launch date", example = "2009-01-10", type = "string", format = "date")
    private LocalDate launchDate;
}
```
- **`accessMode = READ_ONLY`** no `id` (e em campos calculados): o client vê que não deve enviá-lo — ajuda a evitar *mass assignment* por engano.
- **Constraints de Bean Validation** (`@NotBlank`, `@Size`, `@Positive` — `bean-validation`) já aparecem no schema; `@Schema` acrescenta descrição e exemplo. Não duplique uma regra com valores diferentes.
- Exemplos **realistas e fictícios** — nunca dados pessoais reais em exemplo.
- Annotations de documentação no DTO são aceitas mesmo com a preferência `*ControllerDocs` (a interface cuida das operações; o DTO, do schema).

### Exemplos de request/response
```java
@Operation(summary = "Create a Book", tags = {"Book"},
    requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(content = @Content(
        mediaType = MediaType.APPLICATION_JSON_VALUE,
        examples = @ExampleObject(name = "Clean Code", value = """
            {"title": "Clean Code", "author": "Robert C. Martin", "launchDate": "2009-01-10", "price": 77.00}
            """))))
BookDTO create(@RequestBody BookDTO book);
```
Text blocks (`java-modern-features`) deixam o JSON legível. Para exemplos grandes, `@ExampleObject(externalValue = ...)` ou exemplos registrados em `components.examples` pelo customizer.

---

## 4. Parâmetros e endpoints

- **Parâmetros reutilizáveis** (paginação): registre `page`, `size` (com `maximum` igual ao limite real — `pagination`) e `direction` em `components.parameters` no customizer e referencie, ou documente com `@Parameter(description = ..., schema = @Schema(maximum = "100"))` uma vez na interface.
- **`@Hidden`** em endpoints internos (health customizado, callbacks) que não fazem parte do contrato — ou fora do `pathsToMatch`. Esconder **não** protege: a autorização continua no `SecurityConfig`.
- **`servers`** no `OpenApiConfig` (`new Server().url("https://api.example.com").description("Production")`) quando a API roda atrás de um gateway com path diferente; atrás de proxy, prefira `server.forward-headers-strategy: framework` para o springdoc gerar a URL certa.
- **Segurança por operação:** o requisito Bearer global da `swagger` mais `@SecurityRequirements` vazio nos públicos. Com OAuth2/Cognito (`aws-cognito`), declare um scheme `oauth2` com o fluxo e os scopes reais.

---

## 5. O OpenAPI no repositório e no CI

Tratar o documento como contrato significa **versioná-lo e verificá-lo**:

1. **Gerar o `openapi.json` no build** com o `springdoc-openapi-maven-plugin` (sobe a aplicação com o `spring-boot-maven-plugin` em `pre-integration-test`, baixa `/v3/api-docs` e para) — ou, mais simples, um teste de integração que faz `GET /v3/api-docs/v1` e grava o resultado em `target/openapi/v1.json`. Versão do plugin por property (`maven-config`).
2. **Lint** com **Spectral** (regras: toda operação tem `summary`, `operationId` único, respostas de erro documentadas, sem exemplos vazios).
3. **Breaking change** com **oasdiff** comparando o documento da `main` com o do PR: remoção de campo, de endpoint ou mudança de tipo **bloqueia o merge** (`contract-testing`, `api-versioning`).
4. **Publicar** o documento como artefato do pipeline (`github-actions`) ou num portal de APIs.

`operationId` estável importa para os clients gerados: o springdoc usa o nome do método Java — renomear o método renomeia o método do client gerado. Fixe-o com `@Operation(operationId = "findBookById")` quando o contrato é público.

---

## 6. Gerar clients

Com o `openapi.json` versionado, os consumidores geram o client em vez de escrevê-lo:
- **OpenAPI Generator** (`openapi-generator-maven-plugin`): Java (`library=restclient` para o `RestClient` do Spring 7), TypeScript para o front-end.
- Gere no build do **consumidor**, a partir de uma versão publicada do documento, nunca da URL de produção em tempo de build.
- Client gerado + contract test (`contract-testing`) = a quebra aparece no CI de quem consome.
- Para chamadas entre serviços deste pacote, o `@HttpExchange` escrito à mão (`service-communication`) continua válido para poucos endpoints.

---

## 7. Swagger UI por ambiente

- Produção: desligue a UI (`springdoc.swagger-ui.enabled: false` no profile de produção) e, se o documento for público, mantenha só `/v3/api-docs`; ou proteja ambos com autenticação. O documento descreve toda a superfície da API.
- `springdoc.swagger-ui.operations-sorter: alpha` e `tags-sorter: alpha` deixam a UI previsível; `springdoc.default-produces-media-type: application/json` evita que exemplos apareçam em XML quando o projeto também serve XML.
- `springdoc.show-actuator: false` (default) — não documente o Actuator.

---

## 8. Testes

- Teste de integração que valida o documento: `GET /v3/api-docs/v1` → `200`, contém os paths esperados, os schemas `ExceptionResponse` e `BookDTO`, e nenhum path fora do grupo.
- O teste que grava o `openapi.json` (seção 5) é também o insumo do oasdiff.

---

## Regras principais

- Tudo da skill `swagger` continua valendo (idioma, `tags` em inglês, `*ControllerDocs`, `content = @Content` em erros sem body, springdoc 3.x).
- Vários grupos (`GroupedOpenApi`) quando há várias versões ou muitos domínios; filtros coerentes com o `paths-to-match` global.
- Respostas de erro comuns por `OpenApiCustomizer` com `putIfAbsent`; schemas de `ExceptionResponse` e `ProblemDetail` documentados uma vez; 403 sem body.
- `@Schema` com descrição, exemplo realista e `READ_ONLY` no `id`; sem dados pessoais reais em exemplos.
- `operationId` estável quando o contrato é público.
- O `openapi.json` é gerado no build, versionado, passa por lint e por oasdiff — breaking change bloqueia o merge.
- Swagger UI desligado ou protegido em produção; `@Hidden` não é controle de acesso.
- **Sem Lombok** — deliberado.
