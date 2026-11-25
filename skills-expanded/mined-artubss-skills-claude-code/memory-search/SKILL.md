---
name: memory-search
description: Pesquise o histórico de conversas e memória semântica para recordar discussões anteriores, decisões e contexto. Use quando o usuário pedir "pesquise memória", "o que discutimos", "lembra quando", "encontre conversa anterior", "verifique histórico", ou antes de iniciar um trabalho para recordar decisões anteriores.
---

# AI Maestro Memory Search

Pesquise o histórico de conversas usando correspondência semântica, por palavras-chave e símbolos. Recorde decisões, discussões e contexto entre sessões. Parte da suite [AI Maestro](https://github.com/23blocks-OS/ai-maestro).

## Pré-requisitos

Requer [AI Maestro](https://github.com/23blocks-OS/ai-maestro) rodando localmente. A indexação de memória usa CozoDB para busca vetorial.

```bash
# Instale as ferramentas de memória
git clone https://github.com/23blocks-OS/ai-maestro-plugins.git
cd ai-maestro-plugins && ./install-memory-tools.sh
```

## Comportamento Principal

Antes de iniciar qualquer tarefa, pesquise memória para contexto relevante:

```
Receba instrução -> Pesquise memória -> Então prossiga
```

## Comandos

| Comando | Descrição |
|---------|-----------|
| `memory-search.sh "<query>"` | Busca híbrida (recomendado) |
| `memory-search.sh "<query>" --mode semantic` | Encontre conceitos relacionados |
| `memory-search.sh "<query>" --mode term` | Correspondência de texto exato |
| `memory-search.sh "<query>" --mode symbol` | Correspondência de símbolo de código |
| `memory-search.sh "<query>" --role user` | Apenas mensagens do usuário |
| `memory-search.sh "<query>" --role assistant` | Apenas mensagens do assistente |

## Modos de Busca

| Modo | Melhor Para |
|------|-------------|
| `hybrid` (padrão) | Busca geral, maioria dos casos |
| `semantic` | Conceitos relacionados, redação diferente |
| `term` | Nomes exatos de função/classe |
| `symbol` | Identificadores de código entre contextos |

## Exemplos de Uso

```bash
# Usuário pede para continuar trabalho anterior
memory-search.sh "authentication"

# Encontre discussão de componente específico
memory-search.sh "PaymentService" --mode term

# Encontre discussões de design relacionadas
memory-search.sh "error handling patterns" --mode semantic

# Encontre referências de símbolo de código
memory-search.sh "processPayment" --mode symbol
```

## Combinando com Outras Skills

Para contexto completo, combine com docs-search e graph-query:
```bash
memory-search.sh "feature"       # O que discutimos?
docs-search.sh "feature"         # O que os docs dizem?
graph-describe.sh ComponentName  # Qual é a estrutura?
```

## Experiência Completa AI Maestro

Esta skill faz parte da plataforma [AI Maestro](https://github.com/23blocks-OS/ai-maestro), que fornece **6 skills** para orquestração de agentes de IA: messaging, memory, docs, graph, planning e gerenciamento de agentes.