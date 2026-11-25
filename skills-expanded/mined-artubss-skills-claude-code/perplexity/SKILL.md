---
name: perplexity
description: Busca web e pesquisa usando Perplexity AI. Use quando o usuário disser "pesquisar", "encontrar", "procurar", "perguntar", "pesquisar" ou "qual é o mais recente" para consultas genéricas. NÃO para docs de biblioteca/framework (use Context7) ou perguntas do workspace.
---

# Ferramentas Perplexity

Use APENAS quando o usuário disser "pesquisar", "encontrar", "procurar", "perguntar", "pesquisar" ou "qual é o mais recente" para consultas genéricas. NÃO para docs de biblioteca/framework (use Context7), CLI gt (use Graphite MCP) ou perguntas do workspace (use Nx MCP).

## Referência Rápida

**Qual ferramenta Perplexity?**
- Precisa de resultados de busca/URLs? → **Perplexity Search**
- Precisa de resposta conversacional? → **Perplexity Ask**
- Precisa de pesquisa profunda? → **Agente de Pesquisa** (`/research <tema>`)

**NÃO é Perplexity - use estes em vez disso:**
- Docs de biblioteca/framework → **Context7 MCP**
- CLI `gt` Graphite → **Graphite MCP**
- ESTE workspace → **Nx MCP**
- URL específica → **URL Crawler**

## Perplexity Search

**Quando usar:**
- Buscas genéricas, encontrar recursos
- Melhores práticas atuais, informações recentes
- Descoberta de tutoriais/posts de blog
- Usuário diz "pesquise...", "encontre...", "procure..."

**Parâmetros padrão (SEMPRE USE):**
```typescript
mcp__perplexity__perplexity_search({
  query: "sua consulta de busca",
  max_results: 3,           // Padrão é 10 - demais!
  max_tokens_per_page: 512  // Reduz conteúdo por resultado
})
```

**Quando aumentar limites:**
Apenas se:
- Usuário explicitamente precisar de resultados abrangentes
- Busca inicial não encontrou nada útil
- Tema complexo precisa de múltiplas fontes

```typescript
// Limites aumentados (use com moderação)
mcp__perplexity__perplexity_search({
  query: "tema complexo",
  max_results: 5,
  max_tokens_per_page: 1024
})
```

## Perplexity Ask

**Quando usar:**
- Precisa de explicação conversacional, não resultados de busca
- Sintetizar informações da web
- Explicar conceitos com contexto atual

**Uso:**
```typescript
mcp__perplexity__perplexity_ask({
  messages: [
    {
      role: "user",
      content: "Explique como funcionam os advisory locks do postgres"
    }
  ]
})
```

**NÃO para:**
- Documentação de biblioteca (use Context7)
- Pesquisa profunda multi-fonte (use agente de pesquisa)

## Ferramenta Proibida

**NUNCA use:** `mcp__perplexity__perplexity_research`

**Use em vez disso:** Agente de Pesquisa (`/research <tema>`)
- Custo de token: 30-50k tokens
- Fornece síntese multi-fonte com citações
- Use com moderação para perguntas complexas apenas

## Cadeia de Seleção de Ferramentas

**Ordem de prioridade:**
1. **Context7 MCP** - Docs de biblioteca/framework
2. **Graphite MCP** - Qualquer menção de CLI `gt`
3. **Nx MCP** - Perguntas DESTE workspace
4. **Perplexity Search** - Buscas genéricas
5. **Perplexity Ask** - Respostas conversacionais
6. **Agente de Pesquisa** - Pesquisa profunda multi-fonte
7. **WebSearch** - Último recurso (após Perplexity esgotado)

## Exemplos

**✅ CORRETO - Use Perplexity Search:**
- "Encontre melhores práticas de migração postgres"
- "Pesquise tutoriais de testes React"
- "Procure as últimas tendências em microsserviços"

**✅ CORRETO - Use Perplexity Ask:**
- "Explique como funcionam os advisory locks do postgres"
- "Quais são os trade-offs dos microsserviços?"

**❌ ERRADO - Use Context7 em vez disso:**
- "Pesquise documentação de React hooks" → Context7 MCP
- "Encontre docs de roteamento Next.js" → Context7 MCP
- "Procure a API de workflow Temporal" → Context7 MCP

**❌ ERRADO - Use Graphite MCP em vez disso:**
- "Pesquise comandos gt stack" → Graphite MCP
- "Encontre fluxo de branch gt" → Graphite MCP

**❌ ERRADO - Use Nx MCP em vez disso:**
- "Pesquise configuração de build" (NESTE workspace) → Nx MCP
- "Encontre dependências do projeto" (NESTE workspace) → Nx MCP

## Pontos-Chave

- **Padrão de resultados limitados** - evite bloat de contexto
- **Docs de biblioteca = Context7** - SEMPRE tente Context7 primeiro
- **"gt" = Graphite MCP** - QUALQUER menção "gt" usa Graphite
- **Pesquisa profunda = /research** - NÃO ferramenta perplexity_research
- **Cadeia de fallback** - Search → Ask → WebSearch (último recurso)