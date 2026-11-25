---
name: docs-search
description: Pesquise a documentação da base de código gerada automaticamente para assinaturas de funções, docs de API, definições de classe e comentários de código. Use quando o usuário solicitar "pesquisar docs", "encontrar documentação", "procurar uma função", "verificar a API" ou antes de implementar mudanças para verificar assinaturas e padrões corretos.
---

# Pesquisa de Documentação AI Maestro

Pesquise a documentação gerada automaticamente da sua base de código para assinaturas de funções, definições de classe, docs de API e comentários de código. Verifique padrões corretos antes de escrever código. Parte do conjunto [AI Maestro](https://github.com/23blocks-OS/ai-maestro).

## Pré-requisitos

Requer [AI Maestro](https://github.com/23blocks-OS/ai-maestro) em execução localmente com documentação indexada.

```bash
# Instalar ferramentas de docs
git clone https://github.com/23blocks-OS/ai-maestro-plugins.git
cd ai-maestro-plugins && ./install-doc-tools.sh
```

## Comportamento Principal

Antes de implementar qualquer mudança de código, pesquise a documentação primeiro:

```
Receber instrução -> Pesquisar docs -> Depois implementar
```

## Comandos

### Pesquisa
| Comando | Descrição |
|---------|-----------|
| `docs-search.sh <query>` | Pesquisa semântica de documentação |
| `docs-search.sh --keyword <term>` | Correspondência exata de palavras-chave |
| `docs-find-by-type.sh <type>` | Encontrar por tipo (function, class, module) |
| `docs-get.sh <doc-id>` | Obter conteúdo completo do documento |

### Indexação
| Comando | Descrição |
|---------|-----------|
| `docs-index.sh [path]` | Índice completo do projeto |
| `docs-index-delta.sh [path]` | Índice delta (apenas arquivos novos/modificados) |
| `docs-list.sh` | Listar todos os documentos indexados |
| `docs-stats.sh` | Estatísticas do índice |

## Tipos de Documento

| Tipo | Fontes |
|------|--------|
| `function` | JSDoc, RDoc, docstrings |
| `class` | Comentários no nível de classe |
| `module` | Comentários de módulo/namespace |
| `interface` | Interfaces TypeScript |
| `component` | Comentários de componentes React/Vue |
| `readme` | Arquivos README |
| `guide` | Conteúdo da pasta docs/ |

## Exemplos de Uso

```bash
# Pesquisa semântica
docs-search.sh "authentication flow"

# Pesquisa de palavra-chave para identificador específico
docs-search.sh --keyword "UserController"

# Encontrar toda documentação de classe
docs-find-by-type.sh class

# Obter detalhes completos do documento
docs-get.sh doc-abc123

# Indexar sua base de código (primeira vez)
docs-index.sh /path/to/project

# Atualizar índice após mudanças
docs-index-delta.sh
```

## Experiência Completa com AI Maestro

Esta skill faz parte da plataforma [AI Maestro](https://github.com/23blocks-OS/ai-maestro), que fornece **6 skills** para orquestração de agentes IA: messaging, memory, docs, graph, planning e agent management.