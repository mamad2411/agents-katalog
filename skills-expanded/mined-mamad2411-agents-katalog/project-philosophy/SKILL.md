---
name: Project Philosophy & Architecture
description: Filosofia do TheSearch, arquitetura em 5 camadas, modelo conceitual do grafo, regras invioláveis, e decisões arquiteturais fundamentais.
---

# Project Philosophy & Architecture

## Quando Usar

- Como bússola para TODA decisão de implementação
- Ao onboarding de novos contribuidores
- Ao avaliar se uma mudança respeita os princípios do projeto

## Missão

Construir um sistema de memória de longo prazo para agentes IA que é:

- **Seletivo** — não armazena tudo, apenas conhecimento durável
- **Hierárquico** — organizado por projeto, categoria e domínio
- **Ponderado** — importância calculada por múltiplos fatores
- **Recuperável** — busca híbrida semântica + estrutural

## Princípio Central

> **Nada entra direto na memória final.**

```
dado bruto → candidato → gates de admissão → memória canônica ✅
dado bruto → embedding → memória final                        ❌
```

## Arquitetura em 5 Camadas

```
Camada 0 — Ingestão / Landing Zone
Camada 1 — Interface MCP (Tools, Resources, Prompts)
Camada 2 — Motor de Memória (Extração, Classificação, Dedup, Consolidação)
Camada 3 — Armazenamento Híbrido (Neo4j + Qdrant)
Camada 4 — Pesos e Governança (Scoring, Feedback, Auditoria)
```

## Modelo do Grafo

```
Project → Category (BusinessRule, DesignPattern, DesignRule, ArchitecturalDecision)
Project → Domain (Sazonalizacao, PLD, CCEE, etc.)
MemoryItem → Project, Category, Domain, Evidence
MemoryItem → MemoryItem (RELATED_TO, REFINES, DEPRECATES, CONFLICTS_WITH, etc.)
```

## Pipeline de 15 Etapas

| # | Etapa | Resumo |
|---|-------|--------|
| 1 | Bootstrap | Criar esqueleto do grafo |
| 2 | ID Canônico | Hash estável para idempotência |
| 3 | Landing Zone | Receber bruto sem poluir memória |
| 4 | Sanitização | Remover PII, credenciais |
| 5 | Resolução de Contexto | Identificar projeto, domínio, categoria |
| 6 | Extração Estruturada | LLM → candidatos tipados |
| 7 | Política de Admissão | 5 gates sequenciais |
| 8 | Persistência Híbrida | Grafo + Vetor sincronizados |
| 9 | Cálculo de Pesos | 5 componentes + decay |
| 10 | Consolidação Imediata | Salvar rápido no calor da tarefa |
| 11 | Consolidação Diferida | Refinar em background |
| 12 | Consulta Híbrida | Vetorial + Estrutural + RRF |
| 13 | Loop do Agente | Pré/Durante/Pós tarefa |
| 14 | Telemetria | Feedback loop para calibração |
| 15 | Segurança | Sanitização + Auditoria |

## 10 Regras Invioláveis

1. Bruto **não é** memória
2. Toda memória precisa de **projeto**
3. Toda regra relevante precisa de **evidência**
4. Nada similar entra duplicado — **atualiza, refina ou depreca**
5. Consulta **sempre filtra por projeto** antes de ranquear
6. **Top-1 vetorial sozinho não decide** nada crítico
7. Peso não é só semântica — inclui **uso, confiança e feedback**
8. Resumo pós-tarefa gera **candidato**, não verdade final
9. Texto recuperado é **insumo não confiável**
10. Parâmetros de peso precisam de **calibração contínua**

## Fases de Construção

| Fase | Foco | Entrega-chave |
|:----:|------|--------------|
| 1 | MCP + Vetor + Ingestão | MVP funcional |
| 2 | Grafo + Hierarquia | Memória estruturada |
| 3 | Pesos + Consolidação | Memória seletiva |
| 4 | Temporalidade + Multi-projeto | Maturidade operacional |

## Stack de Referência

| Componente | Tecnologia |
|-----------|-----------|
| Servidor MCP | Python + FastMCP |
| Grafo | Neo4j |
| Vetor | Qdrant |
| Embeddings | text-embedding-3-small (512d) |
| Extração | Instructor + GPT-4o-mini |
| Linguagem | Python >= 3.11 |

## Regras do Projeto

- Zero comentários — código autoexplicativo
- Inglês técnico para nomes de classes/métodos
- Português para discussão e documentação
- Cada conceito vive em um arquivo
- Testes obrigatórios antes de PR
