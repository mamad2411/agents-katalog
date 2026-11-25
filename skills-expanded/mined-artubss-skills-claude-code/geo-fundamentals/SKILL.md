---
name: geo-fundamentals
description: Otimização para Mecanismos Generativos de IA para motores de busca com IA (ChatGPT, Claude, Perplexity).
allowed-tools: Read, Glob, Grep
---

# Fundamentos de GEO

> Otimização para motores de busca alimentados por IA.

---

## 1. O que é GEO?

**GEO** = Generative Engine Optimization (Otimização para Mecanismos Generativos)

| Objetivo | Plataforma |
|----------|-----------|
| Ser citado em respostas de IA | ChatGPT, Claude, Perplexity, Gemini |

### SEO vs GEO

| Aspecto | SEO | GEO |
|--------|-----|-----|
| Objetivo | Ranking #1 | Citações em IA |
| Plataforma | Google | Motores de IA |
| Métricas | Rankings, CTR | Taxa de citação |
| Foco | Palavras-chave | Entidades, dados |

---

## 2. Panorama dos Motores de IA

| Motor | Estilo de Citação | Oportunidade |
|-------|-------------------|-------------|
| **Perplexity** | Numerada [1][2] | Taxa de citação mais alta |
| **ChatGPT** | Inline/notas de rodapé | GPTs personalizados |
| **Claude** | Contextual | Conteúdo longo |
| **Gemini** | Seção de fontes | Integração com SEO |

---

## 3. Fatores de Recuperação RAG

Como motores de IA selecionam conteúdo para citar:

| Fator | Peso |
|-------|------|
| Relevância semântica | ~40% |
| Correspondência de palavras-chave | ~20% |
| Sinais de autoridade | ~15% |
| Atualização | ~10% |
| Diversidade de fontes | ~15% |

---

## 4. Conteúdo que é Citado

| Elemento | Por que Funciona |
|----------|------------------|
| **Estatísticas originais** | Dados únicos e citáveis |
| **Citações de especialistas** | Transferência de autoridade |
| **Definições claras** | Fáceis de extrair |
| **Guias passo-a-passo** | Valor acionável |
| **Tabelas comparativas** | Informação estruturada |
| **Seções de FAQ** | Respostas diretas |

---

## 5. Checklist de Conteúdo para GEO

### Elementos de Conteúdo

- [ ] Títulos baseados em perguntas
- [ ] Resumo/TL;DR no topo
- [ ] Dados originais com fontes
- [ ] Citações de especialistas (nome, cargo)
- [ ] Seção de FAQ (3-5 Q&A)
- [ ] Definições claras
- [ ] Timestamp de "Última atualização"
- [ ] Autor com credenciais

### Elementos Técnicos

- [ ] Schema de article com datas
- [ ] Schema de person para autor
- [ ] Schema de FAQPage
- [ ] Carregamento rápido (< 2,5s)
- [ ] Estrutura HTML limpa

---

## 6. Construção de Entidades

| Ação | Propósito |
|------|-----------|
| Google Knowledge Panel | Reconhecimento de entidade |
| Wikipedia (se notável) | Fonte de autoridade |
| Informações consistentes na web | Consolidação de entidade |
| Menções do setor | Sinais de autoridade |

---

## 7. Acesso de Crawlers de IA

### User-Agents Principais de IA

| Crawler | Motor |
|---------|-------|
| GPTBot | ChatGPT/OpenAI |
| Claude-Web | Claude |
| PerplexityBot | Perplexity |
| Googlebot | Gemini (compartilhado) |

### Decisão de Acesso

| Estratégia | Quando |
|-----------|--------|
| Permitir todos | Quer citações em IA |
| Bloquear GPTBot | Não quer treinamento da OpenAI |
| Seletivo | Permitir alguns, bloquear outros |

---

## 8. Medição

| Métrica | Como Rastrear |
|--------|---------------|
| Citações em IA | Monitoramento manual |
| Menções "Segundo [Marca]" | Pesquisa em IA |
| Citações de concorrentes | Comparar participação |
| Tráfego referenciado por IA | Parâmetros UTM |

---

## 9. Anti-Padrões

| ❌ Não faça | ✅ Faça |
|------------|---------|
| Publique sem datas | Adicione timestamps |
| Atribuições vagas | Nomeie fontes |
| Omita informações de autor | Mostre credenciais |
| Conteúdo superficial | Cobertura abrangente |

---

> **Lembre-se:** IA cita conteúdo que é claro, autorizado e fácil de extrair. Seja a melhor resposta.

---

## Script

| Script | Propósito | Comando |
|--------|-----------|---------|
| `scripts/geo_checker.py` | Auditoria GEO (prontidão para citações em IA) | `python scripts/geo_checker.py <project_path>` |