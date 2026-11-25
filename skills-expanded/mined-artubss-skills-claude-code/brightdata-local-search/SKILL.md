---
name: brightdata-local-search
description: Configure e execute buscas web locais usando a API SERP do Bright Data com o pipeline unfancy-search (expansão de query, recuperação de SERP, reranking com RRF).
---

# Bright Data Local Search

Execute buscas web poderosas localmente usando a API SERP do Bright Data. Esta skill configura o pipeline [unfancy-search](https://github.com/yaronbeen/unfancy-search) — um mecanismo de busca local com expansão de query, recuperação de SERP em múltiplos engines, reranking com RRF, deduplicação e agrupamento por domínio.

**Importante: Esta skill utiliza apenas a versão LOCAL. Não use o endpoint hospedado.**

## Pré-requisitos

- Conta [Bright Data](https://brightdata.com) com acesso à API SERP
- [Chave da API Anthropic](https://console.anthropic.com) (para expansão de query, opcional)
- Docker (recomendado) ou Node.js 18+ com pnpm

## Configuração

### Passo 1: Clone e Configure

```bash
git clone https://github.com/yaronbeen/unfancy-search.git
cd unfancy-search
cp .env.example .env
```

### Passo 2: Defina as Variáveis de Ambiente

Edite `.env` com suas credenciais:

```env
BRIGHT_DATA_API_TOKEN=your_brightdata_token
BRIGHT_DATA_SERP_ZONE=serp_api1
ANTHROPIC_API_KEY=your_anthropic_key   # Opcional: ativa expansão de query com IA
```

Obtenha seu token do Bright Data em: https://brightdata.com (seção SERP API)

### Passo 3: Inicie o Servidor Local

**Docker (recomendado):**
```bash
docker compose up -d
# Servidor rodando em http://localhost:3000
```

**Node.js:**
```bash
pnpm install
pnpm dev
# Servidor rodando em http://localhost:3000
```

## Endpoints da API

Todas as requisições vão para `http://localhost:3000`:

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/search` | POST | Inicia um job de busca |
| `/api/search-status/{jobId}` | GET | Consulta resultados |
| `/api/baseline` | POST | Dispara coleta de baseline |
| `/api/baseline-status/{id}` | GET | Consulta progresso do baseline |

## Executando uma Busca

### Passo 1: Envie a Busca

```bash
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "seu termo de busca"}'
```

A resposta retorna um `jobId`.

### Passo 2: Consulte os Resultados

```bash
curl http://localhost:3000/api/search-status/{jobId}
```

Consulte a cada 3 segundos até que `status` seja `"done"`.

### Parâmetros de Busca

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `query` | string | obrigatório | Termo de busca |
| `expand` | boolean | `false` | Ativa expansão de query com IA via Claude |
| `research` | boolean | `false` | Modo research (12 sub-queries para cobertura máxima) |
| `engines` | string[] | todos | Engines SERP a usar |
| `geo` | string | — | Filtro de região geográfica |
| `count` | number | 10 | Máximo de resultados (até 10) |
| `includeDomains` | string[] | — | Incluir resultados apenas desses domínios |
| `excludeDomains` | string[] | — | Excluir resultados desses domínios |

### Modos de Busca

- **Básico** (`expand: false`): Query única, mais rápido, sem custo de IA
- **Expandido** (`expand: true`): Claude Haiku gera 3 sub-queries para cobertura mais ampla
- **Research** (`research: true`): 12 sub-queries para cobertura máxima

## Exemplos de Uso

### Busca Básica de um Agent

```bash
# Inicia busca
JOB_ID=$(curl -s -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "best practices for API rate limiting"}' | jq -r '.jobId')

# Consulta até concluir
while true; do
  RESULT=$(curl -s http://localhost:3000/api/search-status/$JOB_ID)
  STATUS=$(echo $RESULT | jq -r '.status')
  if [ "$STATUS" = "done" ]; then
    echo $RESULT | jq '.results'
    break
  fi
  sleep 3
done
```

### Modo Research com Filtro de Domínios

```bash
curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "kubernetes scaling strategies",
    "research": true,
    "excludeDomains": ["pinterest.com", "quora.com"]
  }'
```

### Adicionando Busca a um Agent Existente

Para dar ao seu agent Claude Code capacidades de busca:

1. Certifique-se que o servidor local está rodando (`docker compose up -d` no diretório unfancy-search)
2. Seu agent pode usar `curl` ou `fetch` para consultar `http://localhost:3000/api/search`
3. Analise os resultados ranqueados para fundamentar respostas com dados reais da web

## Formato de Resposta

Os resultados incluem:
- URLs ranqueadas com scores RRF
- Agrupamento por domínio (resultados agrupados por origem)
- Transparência de custos (detalhamento de despesas por busca)
- Contagem de resultados brutos e únicos
- Duração da busca

## Resolução de Problemas

| Problema | Solução |
|----------|---------|
| Servidor não inicia | Verifique se Docker está rodando ou Node.js 18+ está instalado |
| Nenhum resultado retornado | Verifique se `BRIGHT_DATA_API_TOKEN` é válido e a zona SERP API está ativa |
| Expansão de query não funciona | Verifique se `ANTHROPIC_API_KEY` está definida e é válida |
| Respostas lentas | Desative o modo `expand` para buscas de query única mais rápidas |
| Porta 3000 em uso | Pare outros serviços ou modifique a porta em docker-compose.yml |