---
name: web-config
description: WebConfig do Spring Boot 4 — CORS (inclusive com Spring Security) e content negotiation JSON/XML/YAML, YAML converter do Jackson 3 (ServerHttpMessageConvertersCustomizer), XML sem JAXB em DTOs de produção, media types por endpoint e o wire format do Jackson 3. Use quando configurar CORS, aceitar XML/YAML ou quando um endpoint responder 406.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) para as preferências do projeto, o package layout base e as convenções de code style.

# WebConfig & Content Negotiation

Uma única classe `WebConfig` cuida de CORS e content negotiation. Os media types são configuráveis por projeto — veja a pergunta abaixo antes de escrever qualquer código.

---

## Antes de configurar content negotiation — pergunte quais content types suportar

Esta mesma decisão é reutilizada por toda outra skill que toca controllers, DTOs ou testes (`code-organization`, `swagger`, `authentication`, `testing`, `integration-testing`, `hateoas` e `pagination`) — resolva-a uma vez por projeto, aqui. Pergunte ao desenvolvedor antes de escrever o `WebConfig`, qualquer controller ou qualquer DTO:

**"Esta API deve suportar vários content types (JSON + XML e/ou YAML), ou apenas o default, somente JSON?"**

- **JSON é sempre suportado** — é o default e todo projeto precisa dele.
- Se o desenvolvedor quer mais que JSON, pergunte **quais** — XML, YAML ou ambos. Não adicione as dependencies `jackson-dataformat-xml`/`jackson-dataformat-yaml` (veja `maven-config`) nem o YAML converter de forma especulativa — somente para os formatos de fato escolhidos.
- Se o desenvolvedor não tem preferência, use como default **somente JSON**.

Tudo abaixo mostra o setup completo JSON + XML + YAML para referência; quando a resposta é somente JSON, pule as linhas de XML/YAML em `configureContentNegotiation` e pule a classe `JacksonConfig`.

---

## Package structure

```
br.com.padrao/
└── config/
    ├── WebConfig.java
    └── JacksonConfig.java        # only when YAML was chosen
```

---

## application.yml

```yaml
cors:
  originPatterns: http://localhost:8080,http://localhost:3000
```

Lista separada por vírgulas de origins exatas. Lida via `@Value` no `WebConfig`. Adicione as origins reais do front-end por projeto.

---

## WebConfig

Implementa `WebMvcConfigurer`. Duas responsabilidades: CORS e content negotiation.

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Value("${cors.originPatterns:default}")
    private String corsOriginPatterns = "";

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        var allowedOrigins = corsOriginPatterns.split(",");
        registry.addMapping("/**")
                .allowedOrigins(allowedOrigins)
                .allowedMethods("*")
                .allowCredentials(true);
    }

    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer.favorParameter(false)
                .ignoreAcceptHeader(false)
                .useRegisteredExtensionsOnly(false)
                .defaultContentType(MediaType.APPLICATION_JSON)
                    .mediaType("json", MediaType.APPLICATION_JSON)
                    .mediaType("xml", MediaType.APPLICATION_XML)
                    .mediaType("yaml", MediaType.APPLICATION_YAML);
    }
}
```

Mostrado acima com XML e YAML ambos registrados, para referência. Se o projeto é somente JSON, o corpo do método é apenas:
```java
configurer.favorParameter(false)
        .ignoreAcceptHeader(false)
        .useRegisteredExtensionsOnly(false)
        .defaultContentType(MediaType.APPLICATION_JSON)
            .mediaType("json", MediaType.APPLICATION_JSON);
```
Registre somente as chamadas `.mediaType(...)` dos formatos de fato escolhidos.

**Regras de CORS:**
- `addMapping("/**")` — aplica a todas as rotas.
- `.allowedMethods("*")` — todos os métodos HTTP permitidos. Pode ser restringido a `"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"` se necessário.
- `.allowCredentials(true)` — necessário para requests de cookie/credenciais vindas de clients de browser; não pode ser combinado com uma origin wildcard, e é por isso que as origins são explícitas. Para subdomínios wildcard use `allowedOriginPatterns(...)` em vez de `allowedOrigins(...)`.
- As origins vêm de `cors.originPatterns` no `application.yml` — nunca hardcoded.
- Uma request de uma origin que não está na lista é respondida com `403` e o body `Invalid CORS request`.

**CORS com Spring Security.** Quando o projeto usa Spring Security (veja `authentication`), a security filter chain roda antes do MVC e rejeita requests preflight a menos que o CORS esteja habilitado lá também. Adicione `.cors(cors -> {})` (equivalente a `Customizer.withDefaults()`) à chain do `HttpSecurity` para que ela pegue a configuração de CORS do MVC acima.

**Regras de content negotiation:**
- `favorParameter(false)` — formato não selecionado via URL param (ex.: `?format=json`).
- `ignoreAcceptHeader(false)` — formato selecionado via header `Accept`.
- `defaultContentType(APPLICATION_JSON)` — fallback quando nenhum header `Accept` é enviado.
- `json` é sempre registrado. `xml`/`yaml` são registrados somente quando o desenvolvedor os escolheu na pergunta acima.

---

## XML (Jackson 3, sem JAXB em DTOs de produção)

Adicione `tools.jackson.dataformat:jackson-dataformat-xml` (veja `maven-config`) e o Spring Boot 4 auto-configura o XML message converter — nada mais em código. O Jackson escreve o XML a partir do nome da classe e dos nomes das properties, então **DTOs de produção não carregam `@XmlRootElement`** e o projeto não precisa de dependency JAXB.

`@XmlRootElement` e as outras annotations `jakarta.xml.bind` pertencem somente aos **DTOs espelho de teste**: o REST Assured serializa request bodies com JAXB quando o content type é XML. Um DTO espelho com um campo `LocalDate` também precisa de um adapter, porque o JAXB não consegue fazer marshal de tipos `java.time` sozinho (sem ele, a request carrega `<launchDate/>` e a API responde 500):
```java
public class LocalDateXmlAdapter extends XmlAdapter<String, LocalDate> {

    @Override
    public LocalDate unmarshal(String value) {
        return value == null ? null : LocalDate.parse(value);
    }

    @Override
    public String marshal(LocalDate value) {
        return value == null ? null : value.toString();
    }
}
```
O JAXB lê properties pelos getters públicos por default, então o adapter vai no **getter**, não no campo:
```java
@XmlJavaTypeAdapter(LocalDateXmlAdapter.class)
public LocalDate getLaunchDate() {
    return launchDate;
}
```
Veja as skills de testing para o setup completo do lado dos testes.

---

## YAML (Jackson 3)

Necessário somente quando o desenvolvedor escolheu suporte a YAML na pergunta acima. O Spring Boot 4 configura os message converters de JSON e XML sozinho, mas **não** o de YAML, e o pattern do Boot 3 (uma subclasse custom de `AbstractJackson2HttpMessageConverter` em torno de `new YAMLMapper()`) não existe mais no Jackson 3 / Spring 7. Sem um YAML converter, requests `application/yaml` falham com 406.

Adicione `tools.jackson.dataformat:jackson-dataformat-yaml` (veja `maven-config`) e registre um `ServerHttpMessageConvertersCustomizer`, que encaixa um `JacksonYamlHttpMessageConverter` do Spring na lista de converters do Boot:

```java
@Configuration
public class JacksonConfig {

    @Bean
    ServerHttpMessageConvertersCustomizer yamlMessageConverterCustomizer() {
        return builder -> builder.withYamlConverter(
            new JacksonYamlHttpMessageConverter(YAMLMapper.builder()));
    }
}
```
Imports: `org.springframework.boot.http.converter.autoconfigure.ServerHttpMessageConvertersCustomizer`, `org.springframework.http.converter.yaml.JacksonYamlHttpMessageConverter`, `tools.jackson.dataformat.yaml.YAMLMapper`.

**Com HATEOAS**, listas YAML repetem um `links: []` vazio depois do `links:` real de cada item — uma chave duplicada sobre a qual o SnakeYAML avisa e que alguns parsers resolvem para a lista vazia. Um mix-in em `EntityModel` que omite links vazios remove isso:
```java
@Configuration
public class JacksonConfig {

    @Bean
    ServerHttpMessageConvertersCustomizer yamlMessageConverterCustomizer() {
        return builder -> builder.withYamlConverter(new JacksonYamlHttpMessageConverter(
            YAMLMapper.builder().addMixIn(EntityModel.class, EntityModelYamlMixin.class)));
    }

    private abstract static class EntityModelYamlMixin {

        @JsonInclude(JsonInclude.Include.NON_EMPTY)
        abstract Links getLinks();
    }
}
```
(`JsonInclude` continua sendo `com.fasterxml.jackson.annotation.JsonInclude`; `EntityModel` e `Links` são de `org.springframework.hateoas`.) JSON (HAL `_links`) e XML nunca tiveram a duplicata.

---

## Controller — declarando os media types escolhidos

Todo endpoint que serve dados declara os formatos escolhidos pelo projeto em `produces`. Endpoints que recebem um body também os declaram em `consumes`. JSON é sempre um deles; adicione `MediaType.APPLICATION_XML_VALUE`/`MediaType.APPLICATION_YAML_VALUE` somente para os formatos escolhidos na pergunta acima.

Leitura — somente produces (somente JSON):
```java
@GetMapping(value = "/{id}", produces = {MediaType.APPLICATION_JSON_VALUE})
public PersonDTO findById(@PathVariable("id") Long id) { ... }
```

Leitura — somente produces (JSON + XML + YAML, se os três foram escolhidos):
```java
@GetMapping(
    value = "/{id}",
    produces = {
        MediaType.APPLICATION_JSON_VALUE,
        MediaType.APPLICATION_XML_VALUE,
        MediaType.APPLICATION_YAML_VALUE})
public PersonDTO findById(@PathVariable("id") Long id) { ... }
```

Escrita — consumes + produces (JSON + XML + YAML, se os três foram escolhidos):
```java
@PostMapping(
    consumes = {
        MediaType.APPLICATION_JSON_VALUE,
        MediaType.APPLICATION_XML_VALUE,
        MediaType.APPLICATION_YAML_VALUE},
    produces = {
        MediaType.APPLICATION_JSON_VALUE,
        MediaType.APPLICATION_XML_VALUE,
        MediaType.APPLICATION_YAML_VALUE})
public PersonDTO create(@RequestBody PersonDTO person) { ... }
```

---

## DTO — HATEOAS collection relation

Quando o projeto usa HATEOAS (skill `hateoas`), DTOs de produção usam `@Relation` para definir a chave de coleção HAL usada em `_embedded`. É isso que determina o nome da chave quando o `PagedResourcesAssembler` serializa a lista.

```java
@Relation(collectionRelation = "books")
public class BookDTO extends RepresentationModel<BookDTO> implements Serializable { ... }
```

O nome da collection relation deve casar com a chave `@JsonProperty` no wrapper `*EmbeddedDTO` usado nos integration tests JSON.

---

## O wire format do Jackson 3

O Spring Boot 4 usa os defaults do Jackson 3 e a saída difere da do Boot 3 de maneiras que os clients podem notar. Não os "conserte" com switches de compatibilidade a menos que o desenvolvedor precise manter um contrato existente:
- **Ordem das properties:** as properties são escritas em ordem alfabética (um record como `ExceptionResponse` mantém sua ordem declarada). Em um item HATEOAS, o `_links` do HAL portanto vem primeiro, e `links` em XML/YAML fica entre os outros campos.
- **Datas:** valores `java.util.Date` terminam em `Z` (`2024-01-15T10:30:00.000Z`), não `+00:00`; `LocalDate` é `"2024-01-15"`.
- **Datas em YAML** são strings ISO, não epoch milliseconds.
- **Nulls em XML** são escritos como `<field xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>` em vez de `<field/>`.
- **Properties desconhecidas são ignoradas** na entrada por default (o Jackson 2 as rejeitava); habilite `FAIL_ON_UNKNOWN_PROPERTIES` explicitamente onde rejeitá-las for o comportamento pretendido.
- **Imports:** `tools.jackson.core`, `tools.jackson.databind`, `tools.jackson.dataformat.*`; as annotations continuam em `com.fasterxml.jackson.annotation`. Mappers são imutáveis e construídos com `JsonMapper.builder()...build()`.

---

## Regras principais

- Pergunte quais content types suportar *antes* de escrever `WebConfig`, controllers ou DTOs — JSON sempre; XML e/ou YAML somente quando o desenvolvedor pedir. Nunca conecte suporte a XML/YAML de forma especulativa.
- `cors.originPatterns` sempre no `application.yml` — nunca hardcoded no `WebConfig`.
- Com Spring Security, habilite também `.cors(cors -> {})` na filter chain.
- `allowedMethods("*")` é o default — restrinja somente quando a security exigir.
- `favorParameter(false)` sempre — o formato nunca é selecionado via query param da URL.
- `ignoreAcceptHeader(false)` sempre — o formato é selecionado via header `Accept`.
- O YAML precisa do bean `ServerHttpMessageConvertersCustomizer` no `JacksonConfig` — caso contrário os endpoints YAML retornam 406. O XML precisa somente da dependency.
- Todo endpoint declara os formatos escolhidos pelo projeto em `produces` (e `consumes` para operações de escrita) — JSON sempre incluído.
- Sem `@XmlRootElement` em DTOs de produção; annotations JAXB somente em DTOs espelho de teste (com `LocalDateXmlAdapter` para `LocalDate`).
- `@Relation(collectionRelation = "...")` em todo DTO usado em responses paginadas — deve casar com a chave `@JsonProperty` no wrapper JSON.
