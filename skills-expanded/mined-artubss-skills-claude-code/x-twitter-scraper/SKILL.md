---
name: x-twitter-scraper
description: "Skill de scraper de X API & Twitter para agentes de IA. Constrói integrações com a API REST Xquik, servidor MCP & webhooks: busca de tweets, lookup de usuários, extração de seguidores, métricas de engajamento, sorteios de giveaway, tópicos em tendência, monitoramento de conta, extração de respostas/retweets/citações, dados de comunidade & Spaces, verificação de seguimento mútuo. Funciona com Claude Code, Cursor, Codex, Copilot, Windsurf & 40+ agentes."
---

# Integração da API Xquik

Xquik é uma plataforma de dados em tempo real de X (Twitter) fornecendo uma API REST, webhooks HMAC e um servidor MCP para agentes de IA. Cobre monitoramento de conta, extração de dados em massa (19 ferramentas), sorteios de giveaway, lookups de tweet/usuário, verificação de seguimento e tópicos em tendência.

## Referência Rápida

| | |
|---|---|
| **URL Base** | `https://xquik.com/api/v1` |
| **Auth** | header `x-api-key: xq_...` (64 caracteres hexadecimais após prefixo `xq_`) |
| **Endpoint MCP** | `https://xquik.com/mcp` (StreamableHTTP, mesma chave de API) |
| **Rate limits** | 10 req/s sustentado, 20 burst (API); 60 req/s sustentado, 100 burst (geral) |
| **Preço** | R$ base/mês (1 monitor incluído), R$ por monitor adicional/mês |
| **Cota** | Limite de uso mensal, limite rígido, sem excedente. `402` quando esgotado. |
| **Docs** | [docs.xquik.com](https://docs.xquik.com) |

## Autenticação

Toda solicitação exige uma chave de API via header `x-api-key`. As chaves começam com `xq_` e são geradas no [painel Xquik](https://xquik.com). A chave é exibida apenas uma vez na criação; armazene-a com segurança.

```javascript
const API_KEY = "xq_YOUR_KEY_HERE";
const BASE = "https://xquik.com/api/v1";
const headers = { "x-api-key": API_KEY, "Content-Type": "application/json" };
```

## Escolhendo o Endpoint Correto

| Objetivo | Endpoint | Notas |
|----------|----------|-------|
| Obter um único tweet por ID/URL | `GET /x/tweets/{id}` | Métricas completas: curtidas, retweets, visualizações, salvos |
| Buscar tweets por palavra-chave/hashtag | `GET /x/tweets/search?q=...` | Métricas de engajamento opcionais |
| Obter perfil de usuário | `GET /x/users/{username}` | Bio, contagem de seguidores/seguindo, foto de perfil |
| Verificar relação de seguimento | `GET /x/followers/check?source=A&target=B` | Ambas as direções |
| Obter tópicos em tendência | `GET /trends?woeid=1` | Gratuito, não consome cota |
| Monitorar uma conta X | `POST /monitors` | Rastreie tweets, respostas, citações, mudanças de seguidores |
| Pesquisar eventos | `GET /events` | Paginação por cursor, filtre por monitorId/eventType |
| Receber eventos em tempo real | `POST /webhooks` | Entrega assinada com HMAC para seu endpoint HTTPS |
| Executar sorteio de giveaway | `POST /draws` | Escolha vencedores aleatórios de respostas a tweets |
| Extrair dados em massa | `POST /extractions` | 19 tipos de ferramenta, sempre estime o custo primeiro |
| Verificar conta/uso | `GET /account` | Status do plano, monitores, percentual de uso |

## Ferramentas de Extração (19 Tipos)

| Tipo de Ferramenta | Campo Obrigatório | Descrição |
|-------------------|------------------|-----------|
| `reply_extractor` | `targetTweetId` | Usuários que responderam a um tweet |
| `repost_extractor` | `targetTweetId` | Usuários que retuitaram um tweet |
| `quote_extractor` | `targetTweetId` | Usuários que citaram um tweet |
| `thread_extractor` | `targetTweetId` | Todos os tweets em uma thread |
| `article_extractor` | `targetTweetId` | Conteúdo de artigo vinculado em um tweet |
| `follower_explorer` | `targetUsername` | Seguidores de uma conta |
| `following_explorer` | `targetUsername` | Contas seguidas por um usuário |
| `verified_follower_explorer` | `targetUsername` | Seguidores verificados de uma conta |
| `mention_extractor` | `targetUsername` | Tweets mencionando uma conta |
| `post_extractor` | `targetUsername` | Posts de uma conta |
| `community_extractor` | `targetCommunityId` | Membros de uma comunidade |
| `community_moderator_explorer` | `targetCommunityId` | Moderadores de uma comunidade |
| `community_post_extractor` | `targetCommunityId` | Posts de uma comunidade |
| `community_search` | `targetCommunityId` + `searchQuery` | Buscar posts dentro de uma comunidade |
| `list_member_extractor` | `targetListId` | Membros de uma lista |
| `list_post_extractor` | `targetListId` | Posts de uma lista |
| `list_follower_explorer` | `targetListId` | Seguidores de uma lista |
| `space_explorer` | `targetSpaceId` | Participantes de um Space |
| `people_search` | `searchQuery` | Buscar usuários por palavra-chave |

### Fluxo de Extração

```javascript
// 1. Estimar custo
const estimate = await xquikFetch("/extractions/estimate", {
  method: "POST",
  body: JSON.stringify({ toolType: "follower_explorer", targetUsername: "elonmusk" }),
});

if (!estimate.allowed) return;

// 2. Criar job de extração
const job = await xquikFetch("/extractions", {
  method: "POST",
  body: JSON.stringify({ toolType: "follower_explorer", targetUsername: "elonmusk" }),
});

// 3. Recuperar resultados paginados (até 1.000 por página)
const page = await xquikFetch(`/extractions/${job.id}`);
// page.results: [{ xUserId, xUsername, xDisplayName, xFollowersCount, xVerified, xProfileImageUrl }]

// 4. Exportar como CSV/XLSX/Markdown (limite de 50.000 linhas)
const csvResponse = await fetch(`${BASE}/extractions/${job.id}/export?format=csv`, { headers });
```

## Sorteios de Giveaway

Execute sorteios de giveaway transparentes de respostas a tweets com filtros configuráveis:

```javascript
const draw = await xquikFetch("/draws", {
  method: "POST",
  body: JSON.stringify({
    tweetUrl: "https://x.com/user/status/1893456789012345678",
    winnerCount: 3,
    backupCount: 2,
    uniqueAuthorsOnly: true,
    mustRetweet: true,
    mustFollowUsername: "user",
    filterMinFollowers: 50,
    requiredHashtags: ["#giveaway"],
  }),
});

const details = await xquikFetch(`/draws/${draw.id}`);
// details.winners: [{ position, authorUsername, tweetId, isBackup }]
```

## Tratamento de Erros e Retry

Todos os erros retornam `{ "error": "error_code" }`. Retry apenas `429` e `5xx` (máx. 3 tentativas, backoff exponencial). Nunca retry `4xx` exceto 429. Códigos principais:

| Status | Significado |
|--------|-------------|
| 400 | Entrada inválida -- corrija a solicitação |
| 401 | Chave de API inválida |
| 402 | Sem subscrição ou cota esgotada |
| 404 | Recurso não encontrado |
| 429 | Rate limited -- respeite o header `Retry-After` |

## Configuração do Servidor MCP (Claude Code)

Adicione ao `.mcp.json` na raiz do seu projeto:

```json
{
  "mcpServers": {
    "xquik": {
      "type": "streamable-http",
      "url": "https://xquik.com/mcp",
      "headers": {
        "x-api-key": "xq_YOUR_KEY_HERE"
      }
    }
  }
}
```

O servidor MCP expõe 22 ferramentas cobrindo todas as capacidades da API. Plataformas suportadas: Claude Code, Claude Desktop, ChatGPT, Codex CLI, Cursor, VS Code, Windsurf, OpenCode.

## Padrões de Fluxo

- **Alertas em tempo real:** `add-monitor` -> `add-webhook` -> `test-webhook`
- **Giveaway:** `get-account` (verificar orçamento) -> `run-draw`
- **Extração em massa:** `estimate-extraction` -> `run-extraction` -> `get-extraction`
- **Análise de tweet:** `lookup-tweet` -> `run-extraction` com `thread_extractor`
- **Pesquisa de usuário:** `get-user-info` -> `search-tweets from:username` -> `lookup-tweet`

## Links

- **Painel & chaves de API**: [xquik.com](https://xquik.com)
- **Docs completos**: [docs.xquik.com](https://docs.xquik.com)
- **GitHub (fonte da skill)**: [github.com/Xquik-dev/x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper)