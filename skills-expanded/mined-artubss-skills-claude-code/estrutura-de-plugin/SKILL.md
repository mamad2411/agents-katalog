---
name: Estrutura de Plugin
description: Esta habilidade deve ser usada quando o usuário solicitar "criar um plugin", "estruturar um plugin", "entender estrutura de plugin", "organizar componentes de plugin", "configurar plugin.json", "usar ${CLAUDE_PLUGIN_ROOT}", "adicionar commands/agents/skills/hooks", "configurar auto-discovery", ou precisar de orientação sobre layout de diretório de plugin, configuração de manifest, organização de componentes, convenções de nomenclatura de arquivos, ou melhores práticas de arquitetura de plugin Claude Code.
version: 0.1.0
---

# Estrutura de Plugin para Claude Code

## Visão geral

Os plugins Claude Code seguem uma estrutura de diretório padronizada com descoberta automática de componentes. Entender essa estrutura permite criar plugins bem organizados e mantíveis que se integrem perfeitamente ao Claude Code.

**Conceitos-chave:**
- Layout de diretório convencional para descoberta automática
- Configuração orientada por manifest em `.claude-plugin/plugin.json`
- Organização baseada em componentes (commands, agents, skills, hooks)
- Referências de caminho portáveis usando `${CLAUDE_PLUGIN_ROOT}`
- Carregamento explícito vs. descoberta automática de componentes

## Estrutura de Diretório

Todo plugin Claude Code segue este padrão organizacional:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Obrigatório: Manifest do plugin
├── commands/                 # Slash commands (arquivos .md)
├── agents/                   # Definições de subagents (arquivos .md)
├── skills/                   # Skills de agent (subdiretórios)
│   └── skill-name/
│       └── SKILL.md         # Obrigatório para cada skill
├── hooks/
│   └── hooks.json           # Configuração de manipuladores de evento
├── .mcp.json                # Definições de servidor MCP
└── scripts/                 # Scripts auxiliares e utilitários
```

**Regras críticas:**

1. **Localização do manifest**: O manifest `plugin.json` DEVE estar no diretório `.claude-plugin/`
2. **Localizações de componentes**: Todos os diretórios de componentes (commands, agents, skills, hooks) DEVEM estar no nível raiz do plugin, NÃO aninhados dentro de `.claude-plugin/`
3. **Componentes opcionais**: Crie apenas diretórios para componentes que o plugin realmente usa
4. **Convenção de nomenclatura**: Use kebab-case para todos os nomes de diretório e arquivo

## Manifest do Plugin (plugin.json)

O manifest define metadados e configuração do plugin. Localizado em `.claude-plugin/plugin.json`:

### Campos Obrigatórios

```json
{
  "name": "plugin-name"
}
```

**Requisitos de nome:**
- Usar formato kebab-case (minúsculas com hífens)
- Deve ser único entre plugins instalados
- Sem espaços ou caracteres especiais
- Exemplo: `code-review-assistant`, `test-runner`, `api-docs`

### Metadados Recomendados

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Breve explicação do propósito do plugin",
  "author": {
    "name": "Nome do Autor",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin-name",
  "license": "MIT",
  "keywords": ["testing", "automation", "ci-cd"]
}
```

**Formato de versão**: Seguir versionamento semântico (MAJOR.MINOR.PATCH)
**Palavras-chave**: Usar para descoberta e categorização de plugin

### Configuração de Caminho de Componente

Especificar caminhos personalizados para componentes (complementam diretórios padrão):

```json
{
  "name": "plugin-name",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Importante**: Caminhos personalizados complementam padrões—não os substituem. Componentes em ambos os diretórios padrão e caminhos personalizados serão carregados.

**Regras de caminho:**
- Devem ser relativos à raiz do plugin
- Devem começar com `./`
- Não podem usar caminhos absolutos
- Suportam arrays para múltiplas localizações

## Organização de Componentes

### Commands

**Localização**: Diretório `commands/`
**Formato**: Arquivos Markdown com frontmatter YAML
**Auto-descoberta**: Todos os arquivos `.md` em `commands/` são carregados automaticamente

**Exemplo de estrutura**:
```
commands/
├── review.md        # Comando /review
├── test.md          # Comando /test
└── deploy.md        # Comando /deploy
```

**Formato de arquivo**:
```markdown
---
name: command-name
description: Descrição do comando
---

Instruções de implementação do comando...
```

**Uso**: Commands se integram como slash commands nativos no Claude Code

### Agents

**Localização**: Diretório `agents/`
**Formato**: Arquivos Markdown com frontmatter YAML
**Auto-descoberta**: Todos os arquivos `.md` em `agents/` são carregados automaticamente

**Exemplo de estrutura**:
```
agents/
├── code-reviewer.md
├── test-generator.md
└── refactorer.md
```

**Formato de arquivo**:
```markdown
---
description: Papel e expertise do agent
capabilities:
  - Tarefa específica 1
  - Tarefa específica 2
---

Instruções detalhadas do agent e conhecimento...
```

**Uso**: Usuários podem invocar agents manualmente, ou Claude Code os seleciona automaticamente com base no contexto da tarefa

### Skills

**Localização**: Diretório `skills/` com subdiretórios por skill
**Formato**: Cada skill em seu próprio diretório com arquivo `SKILL.md`
**Auto-descoberta**: Todos os arquivos `SKILL.md` em subdiretórios de skill são carregados automaticamente

**Exemplo de estrutura**:
```
skills/
├── api-testing/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── test-runner.py
│   └── references/
│       └── api-spec.md
└── database-migrations/
    ├── SKILL.md
    └── examples/
        └── migration-template.sql
```

**Formato SKILL.md**:
```markdown
---
name: Nome da Skill
description: Quando usar esta skill
version: 1.0.0
---

Instruções e orientação da skill...
```

**Arquivos de suporte**: Skills podem incluir scripts, referências, exemplos ou assets em subdiretórios

**Uso**: Claude Code ativa autonomamente skills com base na correspondência de contexto da tarefa com a descrição

### Hooks

**Localização**: `hooks/hooks.json` ou inline em `plugin.json`
**Formato**: Configuração JSON definindo manipuladores de evento
**Registro**: Hooks se registram automaticamente quando o plugin é habilitado

**Exemplo de estrutura**:
```
hooks/
├── hooks.json           # Configuração de hooks
└── scripts/
    ├── validate.sh      # Script de hook
    └── check-style.sh   # Script de hook
```

**Formato de configuração**:
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
      "timeout": 30
    }]
  }]
}
```

**Eventos disponíveis**: PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification

**Uso**: Hooks executam automaticamente em resposta a eventos do Claude Code

### MCP Servers

**Localização**: `.mcp.json` na raiz do plugin ou inline em `plugin.json`
**Formato**: Configuração JSON para definições de servidor MCP
**Auto-inicialização**: Servidores iniciam automaticamente quando o plugin é habilitado

**Formato de exemplo**:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Uso**: Servidores MCP se integram perfeitamente ao sistema de ferramentas do Claude Code

## Referências de Caminho Portáveis

### ${CLAUDE_PLUGIN_ROOT}

Use a variável de ambiente `${CLAUDE_PLUGIN_ROOT}` para todas as referências de caminho intra-plugin:

```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

**Por que importa**: Plugins instalam em diferentes localizações dependendo de:
- Método de instalação do usuário (marketplace, local, npm)
- Convenções do sistema operacional
- Preferências do usuário

**Onde usar**:
- Caminhos de comando de hook
- Argumentos de comando de servidor MCP
- Referências de execução de script
- Caminhos de arquivo de recurso

**Nunca use**:
- Caminhos absolutos codificados (`/Users/name/plugins/...`)
- Caminhos relativos do diretório de trabalho (`./scripts/...` em commands)
- Atalhos de diretório home (`~/plugins/...`)

### Regras de Resolução de Caminho

**Em campos JSON de manifest** (hooks, servidores MCP):
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/tool.sh"
```

**Em arquivos de componente** (commands, agents, skills):
```markdown
Referenciar scripts em: ${CLAUDE_PLUGIN_ROOT}/scripts/helper.py
```

**Em scripts executados**:
```bash
#!/bin/bash
# ${CLAUDE_PLUGIN_ROOT} disponível como variável de ambiente
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

## Convenções de Nomenclatura de Arquivo

### Arquivos de Componente

**Commands**: Use arquivos `.md` em kebab-case
- `code-review.md` → `/code-review`
- `run-tests.md` → `/run-tests`
- `api-docs.md` → `/api-docs`

**Agents**: Use arquivos `.md` em kebab-case descrevendo papel
- `test-generator.md`
- `code-reviewer.md`
- `performance-analyzer.md`

**Skills**: Use nomes de diretório em kebab-case
- `api-testing/`
- `database-migrations/`
- `error-handling/`

### Arquivos de Suporte

**Scripts**: Use nomes descritivos em kebab-case com extensões apropriadas
- `validate-input.sh`
- `generate-report.py`
- `process-data.js`

**Documentação**: Use arquivos markdown em kebab-case
- `api-reference.md`
- `migration-guide.md`
- `best-practices.md`

**Configuração**: Use nomes padrão
- `hooks.json`
- `.mcp.json`
- `plugin.json`

## Mecanismo de Auto-Descoberta

Claude Code descobre e carrega componentes automaticamente:

1. **Manifest do plugin**: Lê `.claude-plugin/plugin.json` quando o plugin é habilitado
2. **Commands**: Verifica diretório `commands/` para arquivos `.md`
3. **Agents**: Verifica diretório `agents/` para arquivos `.md`
4. **Skills**: Verifica `skills/` para subdiretórios contendo `SKILL.md`
5. **Hooks**: Carrega configuração de `hooks/hooks.json` ou manifest
6. **Servidores MCP**: Carrega configuração de `.mcp.json` ou manifest

**Timing de descoberta**:
- Instalação de plugin: Componentes se registram com Claude Code
- Plugin habilitado: Componentes ficam disponíveis para uso
- Sem restart necessário: Mudanças entram em vigor na próxima sessão Claude Code

**Comportamento de override**: Caminhos personalizados em `plugin.json` complementam (não substituem) diretórios padrão

## Melhores Práticas

### Organização

1. **Agrupamento lógico**: Agrupe componentes relacionados
   - Coloque commands, agents e skills relacionados a testes juntos
   - Crie subdiretórios em `scripts/` para diferentes propósitos

2. **Manifest mínimo**: Mantenha `plugin.json` enxuto
   - Especifique caminhos personalizados apenas quando necessário
   - Confie em auto-descoberta para layouts padrão
   - Use configuração inline apenas para casos simples

3. **Documentação**: Inclua arquivos README
   - Raiz do plugin: Propósito geral e uso
   - Diretórios de componentes: Orientação específica
   - Diretórios de script: Uso e requisitos

### Nomenclatura

1. **Consistência**: Use nomenclatura consistente entre componentes
   - Se command é `test-runner`, nomeie agent relacionado `test-runner-agent`
   - Combine nomes de diretório de skill com seu propósito

2. **Clareza**: Use nomes descritivos que indiquem propósito
   - Bom: `api-integration-testing/`, `code-quality-checker.md`
   - Evite: `utils/`, `misc.md`, `temp.sh`

3. **Comprimento**: Balance brevidade com clareza
   - Commands: 2-3 palavras (`review-pr`, `run-ci`)
   - Agents: Descreva papel claramente (`code-reviewer`, `test-generator`)
   - Skills: Focadas em tópico (`error-handling`, `api-design`)

### Portabilidade

1. **Sempre use ${CLAUDE_PLUGIN_ROOT}**: Nunca codifique caminhos
2. **Teste em múltiplos sistemas**: Verifique em macOS, Linux, Windows
3. **Documente dependências**: Liste ferramentas necessárias e versões
4. **Evite features específicas do sistema**: Use construções bash/Python portáveis

### Manutenção

1. **Version consistentemente**: Atualize versão em plugin.json para releases
2. **Deprecate gracefully**: Marque componentes antigos claramente antes da remoção
3. **Documente breaking changes**: Anote mudanças que afetam usuários existentes
4. **Teste completamente**: Verifique que todos os componentes funcionam após mudanças

## Padrões Comuns

### Plugin Mínimo

Command único sem dependências:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json    # Apenas campo name
└── commands/
    └── hello.md       # Command único
```

### Plugin Completo

Plugin completo com todos os tipos de componente:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/          # Commands voltados para usuário
├── agents/            # Subagents especializados
├── skills/            # Skills que se ativam automaticamente
├── hooks/             # Manipuladores de evento
│   ├── hooks.json
│   └── scripts/
├── .mcp.json          # Integrações externas
└── scripts/           # Utilitários compartilhados
```

### Plugin Focado em Skills

Plugin fornecendo apenas skills:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        └── SKILL.md
```

## Resolução de Problemas

**Componente não está carregando**:
- Verifique se arquivo está no diretório correto com extensão correta
- Verifique sintaxe de frontmatter YAML (commands, agents, skills)
- Garanta que skill tem `SKILL.md` (não `README.md` ou outro nome)
- Confirme que plugin está habilitado nas configurações Claude Code

**Erros de resolução de caminho**:
- Substitua todos os caminhos codificados por `${CLAUDE_PLUGIN_ROOT}`
- Verifique que caminhos são relativos e começam com `./` em manifest
- Verifique que arquivos referenciados existem em caminhos especificados
- Teste com `echo $CLAUDE_PLUGIN_ROOT` em scripts de hook

**Auto-descoberta não está funcionando**:
- Confirme que diretórios estão na raiz do plugin (não em `.claude-plugin/`)
- Verifique nomenclatura de arquivo segue convenções (kebab-case, extensões corretas)
- Verifique que caminhos personalizados em manifest estão corretos
- Reinicie Claude Code para recarregar configuração de plugin

**Conflitos entre plugins**:
- Use nomes de componentes únicos e descritivos
- Namespace commands com nome de plugin se necessário
- Documente conflitos potenciais em README do plugin
- Considere prefixos de command para funcionalidade relacionada

---

Para exemplos detalhados e padrões avançados, veja arquivos nos diretórios `references/` e `examples/`.