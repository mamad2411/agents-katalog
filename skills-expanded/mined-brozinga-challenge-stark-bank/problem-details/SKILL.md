# Skill: Problem Details

## Quando carregar

Carregue esta Skill ao criar ou revisar tratamento de erros HTTP da API.

## Objetivo

Produzir respostas consistentes usando RFC 9457 Problem Details sem vazar detalhes internos.

## Regras

- Usar `application/problem+json` quando aplicável.
- Mapear falhas previsíveis para status HTTP apropriados.
- Erros de validação devem indicar campos/problemas de forma consistente.
- Não expor stack trace, exception message interna, SQL, secrets ou infraestrutura.
- Erros inesperados devem ser registrados internamente e retornar detalhe seguro.

## Campos

Use quando fizer sentido:

```text
type
title
status
detail
instance
```

Extensões podem incluir `traceId`, `errors` e `code`.

Não transformar Problem Details em um envelope genérico excessivo.

## Implementação

Centralizar tratamento sempre que possível usando mecanismos do ASP.NET Core.

Evitar `try/catch` repetido em cada endpoint.

Endpoints não devem conhecer detalhes de exceptions de Infrastructure.

## Testes

Validar status code, content type, campos essenciais, extensões esperadas, ausência de detalhes internos e consistência entre endpoints.
