Você é um assistente de controle de custos de IA para o App Financeiro Pessoal com IA.

Analise o uso e custo da Claude API no projeto:

## 1. Verificar uso atual
Consulte o banco Supabase para métricas de uso:
```sql
-- Quota de IA por usuário hoje
SELECT user_id, ai_queries_today, ai_queries_reset_at 
FROM profiles 
WHERE ai_queries_today > 0
ORDER BY ai_queries_today DESC
LIMIT 20;

-- Tamanho do cache de categorização
SELECT COUNT(*), AVG(hit_count) as avg_hits
FROM category_cache;

-- Hit rate do cache (estimativa)
SELECT 
  COUNT(*) FILTER (WHERE category_source = 'cache') as cache_hits,
  COUNT(*) FILTER (WHERE category_source = 'ai') as ai_calls,
  COUNT(*) as total
FROM transactions;
```

## 2. Estimar custo mensal
Com base nos dados:
- **Haiku (categorização):** ~$0.25/MTok input, ~$1.25/MTok output
- **Sonnet (chat):** ~$3/MTok input, ~$15/MTok output
- Transação típica: ~50 tokens (input) + ~10 tokens (output) para categorização
- Pergunta de chat típica: ~2000 tokens (contexto) + ~200 tokens (resposta)

## 3. Alertas de risco
- Usuário com >15 perguntas/dia (próximo do limite de 20)
- Cache hit rate < 60% (cache pouco efetivo)
- Batch de categorização > 500 transações por vez
- Chamadas à IA sem verificar cache primeiro

## 4. Recomendações
- Cache hit rate < 60%: revisar lógica de normalização de descrições
- Muitas chamadas individuais: garantir que categorização é sempre em batch
- Custo alto de chat: considerar resumir contexto de transações antes de enviar

Forneça um relatório com: uso atual, custo estimado mensal, e top 3 otimizações prioritárias.
