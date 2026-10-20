---
name: equipe-agil-api-designer-knowledge
description: Conhecimento específico do API Designer da Equipe Backend Ágil Kanban+XP. Cobre contract-first em OpenAPI 3.x (via SmallRye OpenAPI no Quarkus) e AsyncAPI 2.x para eventos, RESTful API design patterns (Geewax — Web API Design Cookbook), Richardson Maturity Model (0-3), versionamento e depreciação, paginação/filtragem/ordenação, idempotência (Idempotency-Key), erro padronizado (RFC 7807 Problem Details), HATEOAS / hypermedia, escolha de estilo (REST vs gRPC vs GraphQL vs Async), API style guide, DX (developer experience) metrics (TTFC/TTFS), portal de docs, mock servers, contract testing (Pact). Owner do contrato externo dos serviços do time. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# API Designer — Conhecimento específico

Skill carregada pelo agente `equipe-agil-api-designer` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre o conhecimento necessário para desenhar APIs de qualidade — síncronas e assíncronas — em Java 21 + Quarkus 3, mantendo contratos estáveis para consumidores e developer experience alta.

## 1. Conceitos centrais

### 1.1 Mandato do API Designer na equipe

- **Owner do contrato externo** dos serviços do time (A/R): OpenAPI/AsyncAPI, semântica de recursos, versionamento, depreciação, paginação/filtragem, erro padrão, DX.
- **Não é dono da implementação** (Tech Lead/devs) nem da topologia (Arquiteto Sis); colabora com ambos.
- **Não é dono da segurança** (AppSec) — incorpora controles definidos por ele.
- **Não substitui PO** — PO traz necessidade do consumidor; API Designer traduz em contrato técnico.
- RACI: A/R em contrato de API + AsyncAPI + style guide + portal/docs; C em arquitetura distribuída e implementação.

### 1.2 Stack default

- **OpenAPI 3.x** (`smallrye-open-api` — `quarkus-smallrye-openapi`): contrato REST.
- **AsyncAPI 2.x**: contrato de eventos (Kafka/AMQP/MQTT).
- **Swagger UI** (`/q/swagger-ui`) e **Redoc**: docs visuais.
- **Spectral**: linter de OpenAPI/AsyncAPI no CI.
- **Pact** (consumer-driven): vide `quality-engineer-knowledge` §1.9.
- **Prism / WireMock**: mock server a partir do OpenAPI.
- **Portal de docs**: Backstage, Redocly, ou portal corporativo.

### 1.3 Contract-first (preferido) vs code-first

- **Contract-first**: escreve OpenAPI antes do código; código gerado/orientado pelo contrato; consumidores e provedores acompanham o mesmo artefato.
- **Code-first**: contrato gerado a partir de anotações/código.
- **Heurística da equipe**: **contract-first para API pública/externa** ou consumida por outros times; **code-first aceitável** para API interna ao time com Quarkus (anotações JAX-RS + `@Tag`/`@Operation`/`@Schema` + SmallRye gera OpenAPI), **desde que** o OpenAPI gerado seja revisado e versionado no repo.

### 1.4 Escolha de estilo (REST / gRPC / GraphQL / Async) — recap em foco

| Estilo | Quando | Trade-off |
|--------|--------|-----------|
| **REST** | Pública, interoperável, cache HTTP, recursos identificáveis | Verbose; semântica fraca para operações; over/under-fetching |
| **gRPC** | Interna, performance, multi-linguagem, streaming | Browser nativo limitado; menos human-readable |
| **GraphQL** | Múltiplos clientes com necessidades diferentes; agregação | N+1 server-side; cache complicado; rate limit difícil |
| **AsyncAPI / Event** | Notificação, broadcast, baixo acoplamento, alta vazão | Consistência eventual; debugging mais difícil |

Default da equipe: **REST** para síncrono externo; **AsyncAPI** para evento; gRPC quando ASR justifica; GraphQL raro.

### 1.5 Richardson Maturity Model (Webber/Richardson)

- **Nível 0** — XML-RPC sobre HTTP; só um endpoint, sem recursos.
- **Nível 1** — Múltiplos recursos (URIs distintas); ainda usa POST para tudo.
- **Nível 2** — Verbos HTTP corretos + códigos de status. **Pragmático: 99% das APIs param aqui** e está ótimo.
- **Nível 3** — HATEOAS (resposta inclui links para próximas ações). Útil em domínios com workflow rico; over-engineering em CRUD.

### 1.6 Convenções REST idiomáticas (Geewax — *API Design Patterns*)

**Nomes de recursos**:
- Substantivo plural: `/pedidos`, não `/pedido`, `/getPedidos`, `/listarPedidos`.
- Hierarquia quando há ownership: `/clientes/{id}/pedidos`.
- Sub-recurso para ação que não é CRUD: `POST /pedidos/{id}/cancelamento` (cria evento de cancelamento).

**Verbos HTTP**:

| Verbo  | Uso | Idempotente | Safe |
|--------|-----|-------------|------|
| GET    | Ler recurso(s) | Sim | Sim |
| POST   | Criar; ações que não cabem em PUT | Não | Não |
| PUT    | Substituir recurso completo | Sim | Não |
| PATCH  | Mutar parcialmente | Não (sem cuidado) | Não |
| DELETE | Remover | Sim | Não |

**Status codes** (subset essencial):
- 200 OK, 201 Created (+ Location), 202 Accepted, 204 No Content.
- 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 410 Gone, 412 Precondition Failed, 422 Unprocessable Entity, 429 Too Many Requests.
- 500 Internal Server Error, 502/503/504 (gateway).

### 1.7 Padrões de operação (Geewax)

- **Standard Methods** — List/Get/Create/Update/Delete: estrutura previsível.
- **Custom Methods** — quando ação não cabe em CRUD: `POST /pedidos/{id}:cancelar` ou sub-recurso (`POST /pedidos/{id}/cancelamento`).
- **Long-running operations** — retornar 202 + operação rastreável (`/operations/{id}` com status).
- **Pagination** — `GET /pedidos?page_token=abc&page_size=20` (cursor preferível a offset).
- **Filtering** — query params estruturados (`?status=APROVADO&criado_de=2026-01-01`).
- **Sorting** — `?sort=criado_em:desc,valor:asc`.
- **Sparse fieldsets** — `?fields=id,status,valor` para reduzir payload.
- **Partial response** — combinar fields + pagination.
- **Idempotency** — header `Idempotency-Key` em POST com efeito colateral; servidor deduplica.
- **Conditional requests** — ETag/`If-Match` para concorrência otimista.

### 1.8 Erro padronizado (RFC 7807 — Problem Details for HTTP APIs)

```json
{
  "type": "https://aco.example.com/erros/cota-insuficiente",
  "title": "Cota insuficiente para criar pedido",
  "status": 422,
  "detail": "Cliente 123 possui 8 pedidos abertos; limite é 5.",
  "instance": "/pedidos/req-abc-def",
  "code": "PEDIDO_COTA_EXCEDIDA",
  "fieldErrors": [
    { "field": "itens[0].quantidade", "message": "Mínimo 1" }
  ]
}
```

- `type` é URI estável (documentada no portal).
- `code` é constante para machine handling (não localizar).
- `title`/`detail` para humanos (i18n quando aplicável).
- **Nunca** vazar stack trace em produção.

### 1.9 Versionamento e depreciação

**Estratégias**:
- **URI versioning** — `/v1/pedidos` (default da equipe; explícito; cache friendly).
- **Header versioning** — `Accept: application/vnd.aco.v1+json` (puristas; menos visível).
- **Query versioning** — `?v=1` (evitar).

**Regras**:
- Versão major **somente** para breaking change.
- Adição de campo opcional ≠ breaking.
- Remoção de campo, mudança de tipo, mudança semântica = breaking.
- **Depreciação**:
  - Header `Deprecation: true` + `Sunset: <data>` (RFC 8594).
  - Documentação inclui data e migração.
  - Janela mínima de **90 dias** antes de remover (ou conforme contrato com consumidores).
- **Coexistência**: v1 e v2 vivem em paralelo durante janela; mesma implementação onde possível (Conformist/ACL — vide `arquiteto-sis-knowledge` §1.4).

### 1.10 OpenAPI 3.x — esqueleto mínimo

```yaml
openapi: 3.1.0
info:
  title: ACO Pedidos API
  version: 1.7.0
  description: Gestão de pedidos do consórcio
  contact: { name: Equipe ACO, email: equipe-aco@... }
servers:
  - url: https://api.aco.example.com/v1
paths:
  /pedidos:
    get:
      summary: Lista pedidos
      operationId: listarPedidos
      parameters:
        - $ref: '#/components/parameters/PageToken'
        - $ref: '#/components/parameters/PageSize'
        - in: query
          name: status
          schema: { type: string, enum: [PENDENTE, APROVADO, CANCELADO] }
      responses:
        '200':
          description: Lista paginada
          content:
            application/json:
              schema: { $ref: '#/components/schemas/PaginaPedido' }
        '400': { $ref: '#/components/responses/Problem' }
        '401': { $ref: '#/components/responses/Problem' }
components:
  schemas:
    Pedido:
      type: object
      required: [id, clienteId, status, valor]
      properties:
        id: { type: string, format: uuid }
        clienteId: { type: string, format: uuid }
        status: { type: string, enum: [PENDENTE, APROVADO, CANCELADO] }
        valor: { type: number, format: decimal }
        criadoEm: { type: string, format: date-time }
    Problem:
      type: object
      properties:
        type: { type: string, format: uri }
        title: { type: string }
        status: { type: integer }
        detail: { type: string }
        code: { type: string }
  responses:
    Problem:
      description: Erro padronizado RFC 7807
      content:
        application/problem+json:
          schema: { $ref: '#/components/schemas/Problem' }
  parameters:
    PageToken:
      in: query
      name: page_token
      schema: { type: string }
    PageSize:
      in: query
      name: page_size
      schema: { type: integer, default: 20, maximum: 100 }
  securitySchemes:
    bearerAuth: { type: http, scheme: bearer, bearerFormat: JWT }
security:
  - bearerAuth: []
```

### 1.11 Quarkus + SmallRye OpenAPI — quando code-first

```java
@Path("/pedidos")
@Tag(name = "Pedidos", description = "Gestão de pedidos")
public class PedidoResource {

  @POST
  @Operation(summary = "Cria pedido", operationId = "criarPedido")
  @APIResponses({
    @APIResponse(responseCode = "201", description = "Criado",
      content = @Content(schema = @Schema(implementation = PedidoDTO.class))),
    @APIResponse(responseCode = "422", description = "Validação",
      content = @Content(mediaType = "application/problem+json",
        schema = @Schema(implementation = ProblemDetails.class)))
  })
  @RequestBody(content = @Content(schema = @Schema(implementation = CriarPedidoCmd.class)))
  public Response criar(@Valid CriarPedidoCmd cmd,
                        @HeaderParam("Idempotency-Key") String idempotencyKey) {
    // ...
  }
}
```

OpenAPI gerado em `/q/openapi`; UI em `/q/swagger-ui`. **Versionar o YAML gerado** no repo (gate de PR detecta mudança breaking — Spectral + comparador).

### 1.12 AsyncAPI 2.x — contrato de evento

```yaml
asyncapi: 2.6.0
info:
  title: ACO Pedidos Events
  version: 1.0.0
channels:
  pedidos.aprovados.v1:
    description: Pedidos aprovados pelo motor de crédito
    subscribe:
      operationId: consumirPedidoAprovado
      message: { $ref: '#/components/messages/PedidoAprovado' }
components:
  messages:
    PedidoAprovado:
      name: PedidoAprovado
      title: Pedido Aprovado
      contentType: application/json
      payload: { $ref: '#/components/schemas/PedidoAprovado' }
  schemas:
    PedidoAprovado:
      type: object
      required: [eventId, eventTime, pedidoId, clienteId, valor]
      properties:
        eventId: { type: string, format: uuid }
        eventTime: { type: string, format: date-time }
        pedidoId: { type: string, format: uuid }
        clienteId: { type: string, format: uuid }
        valor: { type: number }
```

Evento tem **headers padrão** da equipe: `eventId` (idempotência), `eventTime`, `traceId`, `causationId`, `correlationId`, `schemaVersion`.

### 1.13 DX (Developer Experience) — métricas

- **TTFC** (Time To First Call) — tempo até o consumidor fazer a primeira chamada bem-sucedida; alvo: < 30 min.
- **TTFS** (Time To First Success) — tempo até resolver o caso de uso completo; alvo: < 1 dia.
- **Self-service ratio** — % de consumidores que não abriram ticket.
- **Doc satisfaction** — pesquisa rápida pós-consumo.

### 1.14 Portal e docs

- OpenAPI/AsyncAPI versionados no repo.
- Portal renderiza com **exemplos copiáveis** (curl + SDK do consumidor).
- **Quickstart** com cenário golden path em 5 passos.
- **Changelog** humano: o que mudou, quando, por que, como migrar.
- **Sandbox** com mock server (Prism a partir do OpenAPI).

### 1.15 API style guide (resumo executivo da equipe)

1. Snake_case em query params (`page_size`), camelCase em payload JSON (`pageSize` ou `page_size` — definir e manter).
2. Pluralizar coleções.
3. UUIDs em IDs externos (não sequenciais).
4. Datas em ISO-8601 UTC (`2026-05-23T10:15:30Z`).
5. Valores monetários como string ou number com escala definida (não double).
6. Booleanos com nome positivo (`ativo`, não `inativo`).
7. Erros em `application/problem+json`.
8. Paginação cursor preferida.
9. Endpoint público sob `/v<n>`.
10. Versão exposta em `info.version` do OpenAPI.

## 2. Práticas e heurísticas operacionais

### 2.1 Workflow de design de uma nova API

1. **Discovery com PO + consumidor** — quem chama, o que precisa, com qual SLA.
2. **Identifica recursos** (substantivos), não verbos.
3. **Esboça OpenAPI** (paths, métodos, schemas, status codes).
4. **Three Amigos com QE + Tech Lead** — validar testabilidade e implementabilidade.
5. **Revisa com AppSec** se há autz/dado sensível.
6. **Lint com Spectral** (style guide enforcement).
7. **Mock server** (Prism) entregue ao consumidor para integração paralela.
8. **Implementação** Quarkus segue o contrato.
9. **Contract test** (Pact) ativo no CI.
10. **Portal/docs publicados** quando API entra em uso.

### 2.2 Quando uma mudança é breaking?

| Mudança | Breaking? |
|---------|-----------|
| Adicionar endpoint | Não |
| Adicionar campo opcional na resposta | Não (se cliente ignora desconhecidos) |
| Adicionar campo obrigatório no request | **Sim** |
| Remover campo da resposta | **Sim** |
| Renomear campo | **Sim** |
| Mudar tipo (string → int) | **Sim** |
| Restringir enum | **Sim** |
| Expandir enum | Depende (cliente pode quebrar se exaustivo) |
| Mudar semântica/comportamento | **Sim** (mesmo sem mudar schema) |
| Mudar código de status retornado | **Sim** |

Em caso de dúvida → trate como breaking → versão major.

### 2.3 Idempotência em POST

```
Cliente envia: POST /pagamentos  Header: Idempotency-Key: req-abc-123
Servidor:
  - Se key já visto + mesma body + < TTL → retorna resposta anterior.
  - Se key já visto + body diferente → 409 Conflict.
  - Se key novo → processa + armazena (key, body-hash, resposta) em TTL (24h típico).
```

Armazenamento típico: Redis ou tabela com TTL. Vide `tech-lead-knowledge` para detalhes de implementação.

### 2.4 Anti-padrões frequentes

- ❌ **Verb no path** (`/getPedidos`, `/criarPedido`) — usar verbo HTTP.
- ❌ **200 OK com `{"erro": ...}`** — usar status code correto + RFC 7807.
- ❌ **Stack trace na resposta** — vazamento.
- ❌ **IDs sequenciais expostos** — vaza ordem/cardinalidade (vide AppSec — BOLA/IDOR).
- ❌ **`null` x ausente sem documentar** — `null` significa "limpar" vs ausente "não mudar"? Documente.
- ❌ **Paginação offset em coleção grande** — ler última página é O(N²); use cursor.
- ❌ **POST não idempotente sem `Idempotency-Key`** em fluxo que aceita retry.
- ❌ **OpenAPI desatualizado** — contrato gera código mas drift acumula.
- ❌ **Versionar tudo na URI** quando mudança é não-breaking — `v2` sem motivo gasta budget de versões.
- ❌ **HATEOAS sem consumidor** — over-engineering em CRUD.
- ❌ **GraphQL sem rate limit por custo de query** — abuso por query profunda.
- ❌ **AsyncAPI sem versão de schema no evento** — quebrar evento em campo é silencioso.

### 2.5 Como API Designer atua no Replenishment

- Item que muda contrato existente → API Designer R.
- Item que cria contrato novo → API Designer R.
- Item que toca evento publicado → API Designer R no AsyncAPI.
- Item interno sem efeito de contrato → API Designer não envolvido.

### 2.6 Como API Designer atua no Risk Review

- Lista APIs em depreciação com sunset próximo.
- Lista breaking changes não comunicadas.
- Lista consumidores em v anterior.
- Lista erros de validação top-N (sinal de UX ruim do contrato).
- Lista feedback de DX (TTFC alto, tickets).

### 2.7 Colaboração com outros papéis

- **PO** — necessidade do consumidor (Three Amigos).
- **Tech Lead** — implementação do contrato; validação Hibernate Validator.
- **Arquiteto Sis** — estilo (REST/Async/gRPC); granularidade.
- **AppSec** — autz, dado sensível, rate limit, IDOR.
- **Quality Engineer** — contract testing (Pact); testes de boundary.
- **SRE** — SLO de latência/availability do endpoint.
- **DevOps** — gateway, rate limit, observabilidade do endpoint.

## 3. Templates e checklists

### 3.1 Checklist de revisão de OpenAPI

- [ ] `info.version` reflete versão semântica correta.
- [ ] Todo path tem `summary` + `operationId` + `tags`.
- [ ] Todo response tem schema (sem `application/json` vazio).
- [ ] Erros documentados como `application/problem+json` (RFC 7807).
- [ ] Códigos de status corretos para cada cenário.
- [ ] Paginação cursor onde coleção pode crescer.
- [ ] Idempotência declarada onde POST é "create".
- [ ] Auth declarada (`securitySchemes` + `security`).
- [ ] Sem PII/segredo em exemplo.
- [ ] Spectral lint sem warnings.

### 3.2 Checklist de breaking change

- [ ] Identificado como breaking pela tabela §2.2.
- [ ] Nova versão major criada (URI ou header).
- [ ] Versão anterior marcada com `Deprecation: true` + `Sunset: <data>`.
- [ ] Janela ≥ 90 dias até remover.
- [ ] Migração documentada no portal.
- [ ] Consumidores notificados (canal acordado).
- [ ] Contract test passa para v anterior **e** nova.
- [ ] Monitoração de uso da v anterior (sabe quando pode remover).

### 3.3 Template de changelog de API

```markdown
## v1.7.0 — 2026-05-23

### Added
- `GET /pedidos/{id}/historico` — retorna histórico de mudanças (Envers).
- Campo opcional `prioridade` em `Pedido`.

### Changed
- `page_size` padrão era 10 → agora 20.

### Deprecated
- Endpoint `GET /pedidos/{id}/aprovacoes` será removido em 2026-08-23. Use `GET /pedidos/{id}/historico?tipo=APROVACAO`.

### Removed
- (nada)

### Fixed
- Validação de `valor` agora rejeita NaN/Infinity.
```

### 3.4 Esqueleto de erro RFC 7807 em Quarkus

```java
@Provider
public class ProblemMapper implements ExceptionMapper<DomainException> {
  @Override
  public Response toResponse(DomainException e) {
    return Response.status(e.status())
        .type("application/problem+json")
        .entity(new ProblemDetails(
            URI.create("https://aco.example.com/erros/" + e.code()),
            e.title(),
            e.status(),
            e.getMessage(),
            null,
            e.code(),
            e.fieldErrors()))
        .build();
  }
}
```

### 3.5 Quando escalar

- **Consumidor reclama de DX** → revisar TTFC + portal + exemplos.
- **Breaking change inevitável** → discutir com PO + consumidores + Eng Coach (impacto de coexistência).
- **Diverge do style guide corporativo** → escalar para guilda de APIs.
- **API entra em "API zombie"** (sem consumidor ativo) → PO decidir descontinuação.

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-api-designer`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O API Designer usa esta skill para:
- Desenhar contratos (OpenAPI/AsyncAPI) novos ou evoluções.
- Liderar Three Amigos do ponto de vista de contrato.
- Manter style guide e portal.
- Avaliar breaking changes e plano de depreciação.
- Operar contract testing (Pact) junto com Quality Engineer.
- Coachear Tech Lead/devs em design idiomático.

API Designer **não implementa** (Tech Lead/devs implementam); **policia o contrato** como artefato de primeira classe.

## References

Bibliografia da seção 3.11 do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *API Design Patterns* — Geewax
- *Web API Design: The Missing Reference* — Lauret
- *Designing Web APIs* — Jin, Sahni & Shevat
- *REST API Design Rulebook* — Massé
- *RESTful Web APIs* — Richardson, Amundsen & Ruby
- *RESTful Web Services Cookbook* — Allamaraju
- *Continuous API Management* — Medjaoui, Wilde, Mitra & Amundsen
- *Principles of Web API Design* — Higginbotham
- *AsyncAPI Specification* — AsyncAPI Initiative
- *OpenAPI Specification* — OpenAPI Initiative
- *RFC 7807 — Problem Details for HTTP APIs* — Nottingham & Wilde
- *Quarkus SmallRye OpenAPI Guide* — Red Hat
