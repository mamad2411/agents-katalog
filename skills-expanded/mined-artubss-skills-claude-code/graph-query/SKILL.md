---
name: graph-query
description: Consulte o banco de dados de grafo de código para entender relacionamentos de componentes, dependências e impacto de mudanças. Use quando o usuário pedir para "encontrar chamadores", "verificar dependências", "o que usa isso", "mostrar relacionamentos", "encontrar serializadores", ou ao ler código e precisar entender o que depende de um componente antes de fazer modificações.
---

# AI Maestro Code Graph Query

Consulte o grafo de dependências da sua base de código para entender relacionamentos de componentes, cadeias de chamadas e o impacto de mudanças antes de fazer modificações. Parte do conjunto de ferramentas [AI Maestro](https://github.com/23blocks-OS/ai-maestro).

## Pré-requisitos

Requer [AI Maestro](https://github.com/23blocks-OS/ai-maestro) rodando localmente com a base de código indexada.

```bash
# Instalar ferramentas de grafo
git clone https://github.com/23blocks-OS/ai-maestro-plugins.git
cd ai-maestro-plugins && ./install-graph-tools.sh
```

## Comportamento Principal

Após ler qualquer arquivo de código, consulte o grafo para entender dependências:

```
Ler arquivo -> Consultar grafo -> Então prosseguir
```

## Comandos

### Consulta
| Comando | Descrição |
|---------|-----------|
| `graph-describe.sh <name>` | Descrever um componente ou função |
| `graph-find-callers.sh <fn>` | Encontrar todos os chamadores de uma função |
| `graph-find-callees.sh <fn>` | Encontrar todas as funções chamadas por esta função |
| `graph-find-related.sh <component>` | Encontrar componentes relacionados |
| `graph-find-by-type.sh <type>` | Encontrar todos os componentes de um tipo |
| `graph-find-serializers.sh <model>` | Encontrar serializadores para um modelo |
| `graph-find-associations.sh <model>` | Encontrar associações de modelo |
| `graph-find-path.sh <from> <to>` | Encontrar caminho de chamada entre funções |

### Índice
| Comando | Descrição |
|---------|-----------|
| `graph-index-delta.sh [path]` | Indexar ou atualizar o grafo de código |

## Tipos de Componentes

Use com `graph-find-by-type.sh`: `model`, `serializer`, `controller`, `service`, `job`, `concern`, `component`, `hook`

## Exemplos de Uso

```bash
# Após ler um arquivo de modelo
graph-describe.sh User
graph-find-serializers.sh User
graph-find-associations.sh User

# Antes de modificar uma função
graph-find-callers.sh process_payment
graph-find-callees.sh process_payment

# Encontrar cadeia de chamadas entre componentes
graph-find-path.sh handleRequest sendResponse

# Indexar sua base de código
graph-index-delta.sh /path/to/project
```

## Por Que Consultar Antes de Modificar

Sem verificar o grafo, você corre o risco de:
- Quebrar chamadores ao alterar uma assinatura de função
- Perder serializadores que precisam ser atualizados com uma mudança de modelo
- Ignorar classes filhas que herdam suas modificações

## Experiência Completa com AI Maestro

Esta skill faz parte da plataforma [AI Maestro](https://github.com/23blocks-OS/ai-maestro), que fornece **6 skills** para orquestração de agentes IA: messaging, memory, docs, graph, planning e agent management.