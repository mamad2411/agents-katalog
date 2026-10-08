---
name: fluig-mcp
description: >
  Use esta skill quando precisar consultar APIs readonly do TOTVS Fluig por MCP,
  especialmente o Dataset Handle /ecm/dataset/search em ambientes HML e PROD
  com múltiplas instâncias autenticadas.
---

# Fluig Readonly MCP

Esta skill acompanha o MCP `fluig-readonly-mcp`, localizado neste mesmo diretório de produto. Use-a quando a tarefa pedir investigação readonly de datasets Fluig em HML ou PROD sem criar código temporário dentro do Fluig.

## Quando usar

Use o MCP para:

- listar quais instâncias Fluig autenticadas estão configuradas;
- consultar datasets por `/ecm/dataset/search`;
- comparar retorno entre HML e PROD;
- inspecionar colunas, linhas e mensagens retornadas pelo Fluig antes de alterar um dataset avançado, formulário, widget ou processo.

Não use este MCP para escrita. Mesmo quando a API usa HTTP POST, a ferramenta exposta aqui é readonly por contrato.

## Configuração

O servidor lê um arquivo JSON local indicado por `FLUIG_MCP_CONFIG`.

Exemplo:

```json
{
  "instances": [
    {
      "alias": "cliente-a-hml",
      "companyName": "Cliente A",
      "environment": "hml",
      "baseUrl": "https://cliente-a-hml.fluig.com",
      "auth": {
        "type": "oauth1",
        "consumerKey": "replace-with-consumer-key",
        "consumerSecret": "replace-with-consumer-secret",
        "token": "replace-with-access-token",
        "tokenSecret": "replace-with-token-secret"
      }
    }
  ]
}
```

Use aliases explícitos por empresa e ambiente, como `cliente-a-hml`, `cliente-a-prod`, `cliente-b-hml`. Nunca cole secrets em prompts, issues ou exemplos versionados.

## Registro no MCP client

Compile o servidor:

```bash
cd mcp/fluig-api
npm install
npm run build
```

Configure o cliente MCP para executar:

```bash
node /caminho/absoluto/para/mcp/fluig-api/dist/index.cjs
```

No ambiente do servidor, defina:

```bash
FLUIG_MCP_CONFIG=/caminho/absoluto/para/mcp/fluig-api/fluig-mcp.config.json
```

## Ferramentas disponíveis

### fluig_list_instances

Lista aliases, empresa, ambiente e base URL. Não retorna OAuth token, token secret, consumer key ou consumer secret.

### fluig_dataset_search

Consulta `/ecm/dataset/search`.

Campos aceitos:

- `instanceAlias`: alias da instância configurada.
- `datasetId`: identificador do dataset.
- `limit`: limite de registros, com máximo protegido pelo MCP.
- `method`: `POST` por padrão; aceite `GET` quando precisar reproduzir uma chamada GET.
- `searchField` e `searchValue`: filtro sob demanda por campo.
- `filterFields`: pre-filtros em array, normalmente pares `campo`, `valor`.
- `resultFields`: colunas desejadas no retorno.
- `likeField` e `likeValue`: busca aproximada. Em campos de metadata, troque `#` por `_` quando o Dataset Handle exigir.
- `orderBy`: campo de ordenação aceito pelo Fluig.

## Exemplos de input do Dataset Handle

Busca simples:

```json
{
  "instanceAlias": "cliente-a-hml",
  "datasetId": "colleague",
  "limit": 10
}
```

Busca por campo:

```json
{
  "instanceAlias": "cliente-a-hml",
  "datasetId": "colleague",
  "searchField": "login",
  "searchValue": "adm",
  "limit": 5
}
```

Resultado com colunas específicas:

```json
{
  "instanceAlias": "cliente-a-hml",
  "datasetId": "colleague",
  "resultFields": ["login", "colleagueName", "mail"],
  "limit": 20
}
```

Busca aproximada:

```json
{
  "instanceAlias": "cliente-a-hml",
  "datasetId": "colleague",
  "likeField": "colleagueName",
  "likeValue": "Maria",
  "limit": 10
}
```

Pre-filtro com pares campo/valor:

```json
{
  "instanceAlias": "cliente-a-hml",
  "datasetId": "workflowProcess",
  "filterFields": ["status", "1"],
  "resultFields": ["processInstanceId", "processId", "status"],
  "limit": 25
}
```

Ordenação:

```json
{
  "instanceAlias": "cliente-a-prod",
  "datasetId": "colleague",
  "resultFields": ["login", "colleagueName"],
  "orderBy": "colleagueName",
  "limit": 50
}
```

Reprodução via GET:

```json
{
  "instanceAlias": "cliente-a-hml",
  "method": "GET",
  "datasetId": "colleague",
  "searchField": "login",
  "searchValue": "adm",
  "limit": 5
}
```

## O que esperar do retorno

O Fluig normalmente retorna um wrapper JSON:

```json
{
  "content": {
    "values": [
      {
        "login": "adm",
        "colleagueName": "Administrador"
      }
    ],
    "columns": ["login", "colleagueName"]
  },
  "message": null
}
```

No MCP, o retorno também inclui metadados da chamada:

- `instance`: alias, empresa, ambiente e base URL usados;
- `endpoint`: URL chamada;
- `request`: parâmetros readonly enviados;
- `dataset.columns`: colunas quando disponíveis;
- `dataset.rows`: linhas quando `content.values` existe;
- `dataset.rowCount`: quantidade de linhas normalizadas;
- `raw`: resposta original do Fluig para depuração.

## Debugando datasets avançados com dataset.addRow

Em datasets avançados, o retorno é construído linha a linha com:

```javascript
dataset.addRow(new Array(valor1, valor2, valor3));
```

Isso é útil para depuração porque cada `addRow` revela exatamente o que o dataset está entregando para consumidores como formulário, widget, zoom e API REST.

Quando um dataset não retorna o esperado, uma técnica prática é adicionar colunas temporárias:

```javascript
dataset.addColumn("debug_step");
dataset.addColumn("debug_constraint");
dataset.addColumn("debug_payload");
```

E preencher linhas de diagnóstico:

```javascript
dataset.addRow(new Array(
    "antes_consulta_rest",
    String(constraints != null ? constraints.length : 0),
    String(url)
));
```

Isso ajuda a descobrir se o problema está nas constraints recebidas, na chamada externa, no parse do retorno, ou na montagem das linhas finais. Remova essas colunas antes de produção, principalmente quando houver URLs internas, tokens, payloads pessoais ou dados sensíveis.

## Boas práticas

- Comece por HML e use `limit` baixo.
- Sempre chame `fluig_list_instances` quando não tiver certeza do alias.
- Prefira `resultFields` para reduzir payloads grandes.
- Para comparar HML e PROD, use o mesmo input e mude apenas `instanceAlias`.
- Não peça ao MCP para consultar datasets com dados sensíveis sem necessidade clara.
