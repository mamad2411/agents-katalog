---
name: agent-memory-mcp
author: Amit Rathiesh
description: Um sistema híbrido de memória que oferece gerenciamento de conhecimento persistente e pesquisável para agentes de IA (Arquitetura, Padrões, Decisões).
---

# Habilidade de Memória do Agente

Esta habilidade oferece um banco de memória persistente e pesquisável que sincroniza automaticamente com a documentação do projeto. Funciona como um servidor MCP para permitir leitura, escrita e busca de memórias de longo prazo.

## Pré-requisitos

- Node.js (v18+)

## Configuração

1. **Clone o Repositório**:
   Clone o projeto `agentMemory` no espaço de trabalho do seu agente ou em um diretório paralelo:

   ```bash
   git clone https://github.com/webzler/agentMemory.git .agent/skills/agent-memory
   ```

2. **Instale as Dependências**:

   ```bash
   cd .agent/skills/agent-memory
   npm install
   npm run compile
   ```

3. **Inicie o Servidor MCP**:
   Use o script auxiliar para ativar o banco de memória do seu projeto atual:

   ```bash
   npm run start-server <project_id> <absolute_path_to_target_workspace>
   ```

   _Exemplo para o diretório atual:_

   ```bash
   npm run start-server my-project $(pwd)
   ```

## Capacidades (Ferramentas MCP)

### `memory_search`

Procure por memórias por consulta, tipo ou tags.

- **Argumentos**: `query` (string), `type?` (string), `tags?` (string[])
- **Uso**: "Encontre todos os padrões de autenticação" -> `memory_search({ query: "authentication", type: "pattern" })`

### `memory_write`

Registre novo conhecimento ou decisões.

- **Argumentos**: `key` (string), `type` (string), `content` (string), `tags?` (string[])
- **Uso**: "Salve esta decisão de arquitetura" -> `memory_write({ key: "auth-v1", type: "decision", content: "..." })`

### `memory_read`

Recupere conteúdo de memória específica por chave.

- **Argumentos**: `key` (string)
- **Uso**: "Obtenha o design de autenticação" -> `memory_read({ key: "auth-v1" })`

### `memory_stats`

Visualize análises sobre uso de memória.

- **Uso**: "Mostre estatísticas de memória" -> `memory_stats({})`

## Dashboard

Esta habilidade inclui um dashboard independente para visualizar o uso de memória.

```bash
npm run start-dashboard <absolute_path_to_target_workspace>
```

Acesse em: `http://localhost:3333`