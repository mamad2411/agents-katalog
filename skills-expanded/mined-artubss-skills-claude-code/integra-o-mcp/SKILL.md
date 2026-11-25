---
name: Integração MCP
description: Esta habilidade deve ser usada quando o usuário solicitar "adicionar servidor MCP", "integrar MCP", "configurar MCP em plugin", "usar .mcp.json", "configurar Model Context Protocol", "conectar serviço externo", mencionar "${CLAUDE_PLUGIN_ROOT} com MCP", ou discutir tipos de servidor MCP (SSE, stdio, HTTP, WebSocket). Fornece orientação abrangente para integrar servidores Model Context Protocol em plugins Claude Code para integração de ferramentas e serviços externos.
version: 0.1.0
---

# Integração MCP para Plugins Claude Code

## Visão Geral

Model Context Protocol (MCP) permite que plugins Claude Code se integrem com serviços e APIs externas fornecendo acesso estruturado a ferramentas. Use integração MCP para expor capacidades de serviço externo como ferramentas dentro do Claude Code.

**Capacidades principais:**
- Conectar a serviços externos (bancos de dados, APIs, sistemas de arquivos)
- Fornecer 10+ ferramentas relacionadas a partir de um único serviço
- Lidar com fluxos de OAuth e autenticação complexa
- Agrupar servidores MCP com plugins para configuração automática

## Métodos de Configuração do Servidor MCP

Plugins podem agrupar servidores MCP de duas maneiras:

### Método 1: .mcp.json Dedicado (Recomendado)

Crie `.mcp.json` na raiz do plugin:

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

**Benefícios:**
- Separação clara de responsabilidades
- Mais fácil de manter
- Melhor para múltiplos servidores

### Método 2: Inline em plugin.json

Adicione campo `mcpServers` ao plugin.json:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Benefícios:**
- Arquivo de configuração único
- Bom para plugins simples com servidor único

## Tipos de Servidor MCP

### stdio (Processo Local)

Execute servidores MCP locais como processos filhos. Melhor para ferramentas locais e servidores customizados.

**Configuração:**
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"],
    "env": {
      "LOG_LEVEL": "debug"
    }
  }
}
```

**Casos de uso:**
- Acesso ao sistema de arquivos
- Conexões locais a banco de dados
- Servidores MCP customizados
- Servidores MCP empacotados com NPM

**Gerenciamento de processo:**
- Claude Code inicia e gerencia o processo
- Comunica via stdin/stdout
- Encerra quando Claude Code sai

### SSE (Server-Sent Events)

Conecte a servidores MCP hospedados com suporte OAuth. Melhor para serviços em nuvem.

**Configuração:**
```json
{
  "asana": {
    "type": "sse",
    "url": "https://mcp.asana.com/sse"
  }
}
```

**Casos de uso:**
- Servidores MCP hospedados oficiais (Asana, GitHub, etc.)
- Serviços em nuvem com endpoints MCP
- Autenticação baseada em OAuth
- Sem necessidade de instalação local

**Autenticação:**
- Fluxos OAuth tratados automaticamente
- Usuário solicitado na primeira utilização
- Tokens gerenciados pelo Claude Code

### HTTP (REST API)

Conecte a servidores MCP RESTful com autenticação por token.

**Configuração:**
```json
{
  "api-service": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}",
      "X-Custom-Header": "value"
    }
  }
}
```

**Casos de uso:**
- Servidores MCP baseados em REST API
- Autenticação baseada em token
- Backends de API customizados
- Interações sem estado

### WebSocket (Tempo Real)

Conecte a servidores MCP WebSocket para comunicação bidirecional em tempo real.

**Configuração:**
```json
{
  "realtime-service": {
    "type": "ws",
    "url": "wss://mcp.example.com/ws",
    "headers": {
      "Authorization": "Bearer ${TOKEN}"
    }
  }
}
```

**Casos de uso:**
- Streaming de dados em tempo real
- Conexões persistentes
- Notificações push do servidor
- Requisitos de baixa latência

## Expansão de Variáveis de Ambiente

Todas as configurações MCP suportam substituição de variáveis de ambiente:

**${CLAUDE_PLUGIN_ROOT}** - Diretório do plugin (sempre use para portabilidade):
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server"
}
```

**Variáveis de ambiente do usuário** - Do shell do usuário:
```json
{
  "env": {
    "API_KEY": "${MY_API_KEY}",
    "DATABASE_URL": "${DB_URL}"
  }
}
```

**Melhor prática:** Documente todas as variáveis de ambiente necessárias no README do plugin.

## Nomeação de Ferramentas MCP

Quando servidores MCP fornecem ferramentas, elas são automaticamente prefixadas:

**Formato:** `mcp__plugin_<nome-plugin>_<nome-servidor>__<nome-ferramenta>`

**Exemplo:**
- Plugin: `asana`
- Servidor: `asana`
- Ferramenta: `create_task`
- **Nome completo:** `mcp__plugin_asana_asana__asana_create_task`

### Usando Ferramentas MCP em Comandos

Pré-autorize ferramentas MCP específicas no frontmatter de comando:

```markdown
---
allowed-tools: [
  "mcp__plugin_asana_asana__asana_create_task",
  "mcp__plugin_asana_asana__asana_search_tasks"
]
---
```

**Coringa (use com moderação):**
```markdown
---
allowed-tools: ["mcp__plugin_asana_asana__*"]
---
```

**Melhor prática:** Pré-autorize ferramentas específicas, não curingas, por segurança.

## Gerenciamento de Ciclo de Vida

**Inicialização automática:**
- Servidores MCP iniciam quando o plugin se habilita
- Conexão estabelecida antes do primeiro uso de ferramenta
- Reinicialização necessária para mudanças de configuração

**Ciclo de vida:**
1. Plugin carrega
2. Configuração MCP analisada
3. Processo de servidor iniciado (stdio) ou conexão estabelecida (SSE/HTTP/WS)
4. Ferramentas descobertas e registradas
5. Ferramentas disponíveis como `mcp__plugin_...__...`

**Visualizar servidores:**
Use comando `/mcp` para ver todos os servidores, incluindo os fornecidos pelo plugin.

## Padrões de Autenticação

### OAuth (SSE/HTTP)

OAuth tratado automaticamente pelo Claude Code:

```json
{
  "type": "sse",
  "url": "https://mcp.example.com/sse"
}
```

Usuário autentica no navegador na primeira utilização. Nenhuma configuração adicional necessária.

### Baseado em Token (Headers)

Tokens estáticos ou de variáveis de ambiente:

```json
{
  "type": "http",
  "url": "https://api.example.com",
  "headers": {
    "Authorization": "Bearer ${API_TOKEN}"
  }
}
```

Documente variáveis de ambiente necessárias no README.

### Variáveis de Ambiente (stdio)

Passe configuração ao servidor MCP:

```json
{
  "command": "python",
  "args": ["-m", "my_mcp_server"],
  "env": {
    "DATABASE_URL": "${DB_URL}",
    "API_KEY": "${API_KEY}",
    "LOG_LEVEL": "info"
  }
}
```

## Padrões de Integração

### Padrão 1: Wrapper Simples de Ferramenta

Comandos usam ferramentas MCP com interação do usuário:

```markdown
# Comando: create-item.md
---
allowed-tools: ["mcp__plugin_name_server__create_item"]
---

Etapas:
1. Coletar detalhes do item do usuário
2. Usar mcp__plugin_name_server__create_item
3. Confirmar criação
```

**Use para:** Adicionar validação ou pré-processamento antes de chamadas MCP.

### Padrão 2: Agente Autônomo

Agentes usam ferramentas MCP autonomamente:

```markdown
# Agente: data-analyzer.md

Processo de Análise:
1. Consultar dados via mcp__plugin_db_server__query
2. Processar e analisar resultados
3. Gerar relatório de insights
```

**Use para:** Workflows MCP multi-passo sem interação do usuário.

### Padrão 3: Plugin Multi-Servidor

Integre múltiplos servidores MCP:

```json
{
  "github": {
    "type": "sse",
    "url": "https://mcp.github.com/sse"
  },
  "jira": {
    "type": "sse",
    "url": "https://mcp.jira.com/sse"
  }
}
```

**Use para:** Workflows abrangendo múltiplos serviços.

## Melhores Práticas de Segurança

### Use HTTPS/WSS

Sempre use conexões seguras:

```json
✅ "url": "https://mcp.example.com/sse"
❌ "url": "http://mcp.example.com/sse"
```

### Gerenciamento de Token

**FAÇA:**
- ✅ Use variáveis de ambiente para tokens
- ✅ Documente variáveis de ambiente necessárias no README
- ✅ Deixe fluxo OAuth lidar com autenticação

**NÃO FAÇA:**
- ❌ Codifique tokens na configuração
- ❌ Faça commit de tokens no git
- ❌ Compartilhe tokens na documentação

### Escopo de Permissões

Pré-autorize apenas ferramentas MCP necessárias:

```markdown
✅ allowed-tools: [
  "mcp__plugin_api_server__read_data",
  "mcp__plugin_api_server__create_item"
]

❌ allowed-tools: ["mcp__plugin_api_server__*"]
```

## Tratamento de Erros

### Falhas de Conexão

Lide com indisponibilidade de servidor MCP:
- Forneça comportamento alternativo em comandos
- Informe usuário de problemas de conexão
- Verifique URL do servidor e configuração

### Erros de Chamada de Ferramenta

Lide com operações MCP falhadas:
- Valide entradas antes de chamar ferramentas MCP
- Forneça mensagens de erro claras
- Verifique limitação de taxa e cotas

### Erros de Configuração

Valide configuração MCP:
- Teste conectividade de servidor durante desenvolvimento
- Valide sintaxe JSON
- Verifique variáveis de ambiente necessárias

## Considerações de Desempenho

### Carregamento Preguiçoso

Servidores MCP conectam sob demanda:
- Nem todos os servidores conectam na inicialização
- Primeiro uso de ferramenta dispara conexão
- Pooling de conexão gerenciado automaticamente

### Batching

Agrupe solicitações similares quando possível:

```
# Bom: Query única com filtros
tasks = search_tasks(project="X", assignee="me", limit=50)

# Evite: Muitas queries individuais
for id in task_ids:
    task = get_task(id)
```

## Testando Integração MCP

### Teste Local

1. Configure servidor MCP em `.mcp.json`
2. Instale plugin localmente (`.claude-plugin/`)
3. Execute `/mcp` para verificar se servidor aparece
4. Teste chamadas de ferramenta em comandos
5. Verifique logs `claude --debug` para problemas de conexão

### Lista de Validação

- [ ] Configuração MCP é JSON válido
- [ ] URL do servidor está correta e acessível
- [ ] Variáveis de ambiente necessárias documentadas
- [ ] Ferramentas aparecem na saída `/mcp`
- [ ] Autenticação funciona (OAuth ou tokens)
- [ ] Chamadas de ferramenta bem-sucedidas em comandos
- [ ] Casos de erro tratados apropriadamente

## Debugging

### Habilite Log de Debug

```bash
claude --debug
```

Procure por:
- Tentativas de conexão de servidor MCP
- Logs de descoberta de ferramenta
- Fluxos de autenticação
- Erros de chamada de ferramenta

### Problemas Comuns

**Servidor não conecta:**
- Verifique se URL está correta
- Confirme se servidor está rodando (stdio)
- Verifique conectividade de rede
- Revise configuração de autenticação

**Ferramentas não disponíveis:**
- Confirme se servidor conectou com sucesso
- Verifique se nomes de ferramenta correspondem exatamente
- Execute `/mcp` para ver ferramentas disponíveis
- Reinicie Claude Code após mudanças de configuração

**Autenticação falhando:**
- Limpe tokens de autenticação armazenados
- Re-autentique
- Verifique escopos de token e permissões
- Confirme se variáveis de ambiente definidas

## Referência Rápida

### Tipos de Servidor MCP

| Tipo | Transporte | Melhor Para | Autenticação |
|------|-----------|------------|--------------|
| stdio | Processo | Ferramentas locais, servidores customizados | Variáveis env |
| SSE | HTTP | Serviços hospedados, APIs em nuvem | OAuth |
| HTTP | REST | Backends de API, autenticação por token | Tokens |
| ws | WebSocket | Tempo real, streaming | Tokens |

### Lista de Verificação de Configuração

- [ ] Tipo de servidor especificado (stdio/SSE/HTTP/ws)
- [ ] Campos específicos do tipo completos (command ou url)
- [ ] Autenticação configurada
- [ ] Variáveis de ambiente documentadas
- [ ] HTTPS/WSS usados (não HTTP/WS)
- [ ] ${CLAUDE_PLUGIN_ROOT} usado para caminhos

### Melhores Práticas

**FAÇA:**
- ✅ Use ${CLAUDE_PLUGIN_ROOT} para caminhos portáveis
- ✅ Documente variáveis de ambiente necessárias
- ✅ Use conexões seguras (HTTPS/WSS)
- ✅ Pré-autorize ferramentas MCP específicas em comandos
- ✅ Teste integração MCP antes de publicar
- ✅ Lide com erros de conexão e ferramenta adequadamente

**NÃO FAÇA:**
- ❌ Codifique caminhos absolutos
- ❌ Faça commit de credenciais no git
- ❌ Use HTTP em vez de HTTPS
- ❌ Pré-autorize todas as ferramentas com curingas
- ❌ Pule tratamento de erros
- ❌ Esqueça de documentar configuração

## Recursos Adicionais

### Arquivos de Referência

Para informações detalhadas, consulte:

- **`references/server-types.md`** - Análise profunda de cada tipo de servidor
- **`references/authentication.md`** - Padrões de autenticação e OAuth
- **`references/tool-usage.md`** - Usando ferramentas MCP em comandos e agentes

### Configurações de Exemplo

Exemplos funcionais em `examples/`:

- **`stdio-server.json`** - Servidor MCP stdio local
- **`sse-server.json`** - Servidor SSE hospedado com OAuth
- **`http-server.json`** - REST API com autenticação por token

### Recursos Externos

- **MCP Official Docs**: https://modelcontextprotocol.io/
- **Claude Code MCP Docs**: https://docs.claude.com/en/docs/claude-code/mcp
- **MCP SDK**: @modelcontextprotocol/sdk
- **Testing**: Use `claude --debug` e comando `/mcp`

## Fluxo de Trabalho de Implementação

Para adicionar integração MCP a um plugin:

1. Escolha tipo de servidor MCP (stdio, SSE, HTTP, ws)
2. Crie `.mcp.json` na raiz do plugin com configuração
3. Use ${CLAUDE_PLUGIN_ROOT} para todas as referências de arquivo
4. Documente variáveis de ambiente necessárias no README
5. Teste localmente com comando `/mcp`
6. Pré-autorize ferramentas MCP em comandos relevantes
7. Lide com autenticação (OAuth ou tokens)
8. Teste casos de erro (falhas de conexão, erros de autenticação)
9. Documente integração MCP no README do plugin

Foque em stdio para servidores customizados/locais, SSE para serviços hospedados com OAuth.