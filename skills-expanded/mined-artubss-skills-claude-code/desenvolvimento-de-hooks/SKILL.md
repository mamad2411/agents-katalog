---
name: Desenvolvimento de Hooks
description: Esta skill deve ser usada quando o usuário solicita "criar um hook", "adicionar um hook PreToolUse/PostToolUse/Stop", "validar uso de ferramentas", "implementar hooks baseados em prompt", "usar ${CLAUDE_PLUGIN_ROOT}", "configurar automação orientada por eventos", "bloquear comandos perigosos" ou menciona eventos de hook (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification). Fornece orientação abrangente para criar e implementar hooks de plugin Claude Code com foco na API avançada de hooks baseados em prompt.
version: 0.1.0
---

# Desenvolvimento de Hooks para Plugins Claude Code

## Visão Geral

Hooks são scripts de automação orientados por eventos que são executados em resposta a eventos do Claude Code. Use hooks para validar operações, aplicar políticas, adicionar contexto e integrar ferramentas externas em workflows.

**Capacidades-chave:**
- Validar chamadas de ferramenta antes da execução (PreToolUse)
- Reagir a resultados de ferramentas (PostToolUse)
- Aplicar padrões de conclusão (Stop, SubagentStop)
- Carregar contexto do projeto (SessionStart)
- Automatizar workflows em todo o ciclo de vida do desenvolvimento

## Tipos de Hooks

### Hooks Baseados em Prompt (Recomendado)

Use tomada de decisão orientada por LLM para validação consciente do contexto:

```json
{
  "type": "prompt",
  "prompt": "Avalie se este uso de ferramenta é apropriado: $TOOL_INPUT",
  "timeout": 30
}
```

**Eventos suportados:** Stop, SubagentStop, UserPromptSubmit, PreToolUse

**Benefícios:**
- Decisões conscientes do contexto baseadas em raciocínio em linguagem natural
- Lógica de avaliação flexível sem scripts bash
- Melhor tratamento de casos extremos
- Mais fácil de manter e estender

### Hooks de Comando

Execute comandos bash para verificações determinísticas:

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 60
}
```

**Use para:**
- Validações rápidas e determinísticas
- Operações do sistema de arquivos
- Integrações com ferramentas externas
- Verificações críticas de desempenho

## Formatos de Configuração de Hooks

### Formato hooks.json de Plugin

**Para hooks de plugin** em `hooks/hooks.json`, use formato com wrapper:

```json
{
  "description": "Breve explicação dos hooks (opcional)",
  "hooks": {
    "PreToolUse": [...],
    "Stop": [...],
    "SessionStart": [...]
  }
}
```

**Pontos-chave:**
- Campo `description` é opcional
- Campo `hooks` é obrigatório como wrapper contendo os eventos reais
- Este é o **formato específico de plugin**

**Exemplo:**
```json
{
  "description": "Hooks de validação para qualidade de código",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### Formato de Configurações (Direto)

**Para configurações do usuário** em `.claude/settings.json`, use formato direto:

```json
{
  "PreToolUse": [...],
  "Stop": [...],
  "SessionStart": [...]
}
```

**Pontos-chave:**
- Sem wrapper — eventos diretamente no nível superior
- Sem campo description
- Este é o **formato de configurações**

**Importante:** Os exemplos abaixo mostram a estrutura de evento de hook que fica dentro de qualquer formato. Para hooks.json de plugin, envolva esses em `{"hooks": {...}}`.

## Eventos de Hook

### PreToolUse

Execute antes de qualquer ferramenta ser executada. Use para aprovar, negar ou modificar chamadas de ferramenta.

**Exemplo (baseado em prompt):**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Valide a segurança da escrita de arquivo. Verificar: caminhos de sistema, credenciais, path traversal, conteúdo sensível. Retorne 'approve' ou 'deny'."
        }
      ]
    }
  ]
}
```

**Saída para PreToolUse:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "Explicação para Claude"
}
```

### PostToolUse

Execute após a ferramenta ser concluída. Use para reagir a resultados, fornecer feedback ou fazer log.

**Exemplo:**
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analise o resultado da edição para possíveis problemas: erros de sintaxe, vulnerabilidades de segurança, mudanças que quebram compatibilidade. Forneça feedback."
        }
      ]
    }
  ]
}
```

**Comportamento de saída:**
- Exit 0: stdout mostrado na transcrição
- Exit 2: stderr realimentado para Claude
- systemMessage incluída no contexto

### Stop

Execute quando o agente principal considerar parar. Use para validar completude.

**Exemplo:**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verifique a conclusão da tarefa: testes executados, build bem-sucedido, perguntas respondidas. Retorne 'approve' para parar ou 'block' com motivo para continuar."
        }
      ]
    }
  ]
}
```

**Saída de decisão:**
```json
{
  "decision": "approve|block",
  "reason": "Explicação",
  "systemMessage": "Contexto adicional"
}
```

### SubagentStop

Execute quando um subagente considerar parar. Use para garantir que o subagente completou sua tarefa.

Semelhante ao hook Stop, mas para subagentes.

### UserPromptSubmit

Execute quando o usuário envia um prompt. Use para adicionar contexto, validar ou bloquear prompts.

**Exemplo:**
```json
{
  "UserPromptSubmit": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verifique se o prompt requer orientação de segurança. Se estiver discutindo autenticação, permissões ou segurança de API, retorne avisos relevantes."
        }
      ]
    }
  ]
}
```

### SessionStart

Execute quando uma sessão do Claude Code inicia. Use para carregar contexto e configurar ambiente.

**Exemplo:**
```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
        }
      ]
    }
  ]
}
```

**Capacidade especial:** Persistir variáveis de ambiente usando `$CLAUDE_ENV_FILE`:
```bash
echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
```

Veja `examples/load-context.sh` para exemplo completo.

### SessionEnd

Execute quando a sessão termina. Use para limpeza, logging e preservação de estado.

### PreCompact

Execute antes da compactação de contexto. Use para adicionar informações críticas a preservar.

### Notification

Execute quando Claude envia notificações. Use para reagir a notificações do usuário.

## Formato de Saída de Hook

### Saída Padrão (Todos os Hooks)

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Mensagem para Claude"
}
```

- `continue`: Se false, interrompe o processamento (padrão true)
- `suppressOutput`: Oculta saída da transcrição (padrão false)
- `systemMessage`: Mensagem mostrada para Claude

### Códigos de Saída

- `0` - Sucesso (stdout mostrado na transcrição)
- `2` - Erro de bloqueio (stderr realimentado para Claude)
- Outros - Erro não-bloqueador

## Formato de Entrada de Hook

Todos os hooks recebem JSON via stdin com campos comuns:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask|allow",
  "hook_event_name": "PreToolUse"
}
```

**Campos específicos de evento:**

- **PreToolUse/PostToolUse:** `tool_name`, `tool_input`, `tool_result`
- **UserPromptSubmit:** `user_prompt`
- **Stop/SubagentStop:** `reason`

Acesse campos em prompts usando `$TOOL_INPUT`, `$TOOL_RESULT`, `$USER_PROMPT`, etc.

## Variáveis de Ambiente

Disponíveis em todos os hooks de comando:

- `$CLAUDE_PROJECT_DIR` - Caminho raiz do projeto
- `$CLAUDE_PLUGIN_ROOT` - Diretório do plugin (use para caminhos portáveis)
- `$CLAUDE_ENV_FILE` - Somente SessionStart: persistir variáveis de env aqui
- `$CLAUDE_CODE_REMOTE` - Definida se executando em contexto remoto

**Sempre use ${CLAUDE_PLUGIN_ROOT} em comandos de hook para portabilidade:**

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

## Configuração de Hooks de Plugin

Em plugins, defina hooks em `hooks/hooks.json`:

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Valide a segurança da escrita de arquivo"
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verifique a conclusão da tarefa"
        }
      ]
    }
  ],
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

Hooks de plugin se mesclam com hooks do usuário e executam em paralelo.

## Matchers

### Correspondência de Nome de Ferramenta

**Correspondência exata:**
```json
"matcher": "Write"
```

**Múltiplas ferramentas:**
```json
"matcher": "Read|Write|Edit"
```

**Wildcard (todas as ferramentas):**
```json
"matcher": "*"
```

**Padrões Regex:**
```json
"matcher": "mcp__.*__delete.*"  // Todas as ferramentas de exclusão MCP
```

**Nota:** Matchers diferenciam maiúsculas de minúsculas.

### Padrões Comuns

```json
// Todas as ferramentas MCP
"matcher": "mcp__.*"

// Ferramentas MCP de um plugin específico
"matcher": "mcp__plugin_asana_.*"

// Todas as operações de arquivo
"matcher": "Read|Write|Edit"

// Apenas comandos Bash
"matcher": "Bash"
```

## Melhores Práticas de Segurança

### Validação de Entrada

Sempre valide entradas em hooks de comando:

```bash
#!/bin/bash
set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

# Valide o formato do nome da ferramenta
if [[ ! "$tool_name" =~ ^[a-zA-Z0-9_]+$ ]]; then
  echo '{"decision": "deny", "reason": "Nome de ferramenta inválido"}' >&2
  exit 2
fi
```

### Segurança de Caminho

Verifique path traversal e arquivos sensíveis:

```bash
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Negue path traversal
if [[ "$file_path" == *".."* ]]; then
  echo '{"decision": "deny", "reason": "Path traversal detectado"}' >&2
  exit 2
fi

# Negue arquivos sensíveis
if [[ "$file_path" == *".env"* ]]; then
  echo '{"decision": "deny", "reason": "Arquivo sensível"}' >&2
  exit 2
fi
```

Veja `examples/validate-write.sh` e `examples/validate-bash.sh` para exemplos completos.

### Coloque Aspas em Todas as Variáveis

```bash
# BOM: Entre aspas
echo "$file_path"
cd "$CLAUDE_PROJECT_DIR"

# RUIM: Sem aspas (risco de injeção)
echo $file_path
cd $CLAUDE_PROJECT_DIR
```

### Defina Timeouts Apropriados

```json
{
  "type": "command",
  "command": "bash script.sh",
  "timeout": 10
}
```

**Padrões:** Hooks de comando (60s), Hooks de prompt (30s)

## Considerações de Desempenho

### Execução Paralela

Todos os hooks correspondentes são executados **em paralelo**:

```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {"type": "command", "command": "check1.sh"},  // Paralelo
        {"type": "command", "command": "check2.sh"},  // Paralelo
        {"type": "prompt", "prompt": "Validar..."}    // Paralelo
      ]
    }
  ]
}
```

**Implicações de design:**
- Hooks não veem a saída uns dos outros
- Ordenação não-determinística
- Design para independência

### Otimização

1. Use hooks de comando para verificações rápidas e determinísticas
2. Use hooks de prompt para raciocínio complexo
3. Coloque em cache resultados de validação em arquivos temporários
4. Minimize I/O em caminhos críticos

## Hooks Temporariamente Ativos

Crie hooks que se ativem condicionalmente verificando um arquivo de flag ou configuração:

**Padrão: Ativação por arquivo de flag**
```bash
#!/bin/bash
# Apenas ativo quando arquivo de flag existe
FLAG_FILE="$CLAUDE_PROJECT_DIR/.enable-strict-validation"

if [ ! -f "$FLAG_FILE" ]; then
  # Flag não presente, pule validação
  exit 0
fi

# Flag presente, execute validação
input=$(cat)
# ... lógica de validação ...
```

**Padrão: Ativação baseada em configuração**
```bash
#!/bin/bash
# Verifique configuração para ativação
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/plugin-config.json"

if [ -f "$CONFIG_FILE" ]; then
  enabled=$(jq -r '.strictMode // false' "$CONFIG_FILE")
  if [ "$enabled" != "true" ]; then
    exit 0  # Não ativado, pule
  fi
fi

# Ativado, execute lógica do hook
input=$(cat)
# ... lógica do hook ...
```

**Casos de uso:**
- Ative validação rigorosa apenas quando necessário
- Hooks de depuração temporários
- Comportamento de hook específico do projeto
- Feature flags para hooks

**Melhor prática:** Documente mecanismo de ativação no README do plugin para que os usuários saibam como ativar/desativar hooks temporários.

## Ciclo de Vida de Hook e Limitações

### Hooks Carregam no Início da Sessão

**Importante:** Hooks são carregados quando a sessão do Claude Code inicia. Mudanças na configuração de hooks requerem reiniciar o Claude Code.

**Não é possível trocar hooks dinamicamente:**
- Editar `hooks/hooks.json` não afetará a sessão atual
- Adicionar novos scripts de hook não será reconhecido
- Mudar comandos/prompts de hook não será atualizado
- Deve reiniciar o Claude Code: saia e execute `claude` novamente

**Para testar mudanças de hook:**
1. Edite configuração de hook ou scripts
2. Saia da sessão do Claude Code
3. Reinicie: `claude` ou `cc`
4. Nova configuração de hook carrega
5. Teste hooks com `claude --debug`

### Validação de Hook na Inicialização

Hooks são validados quando Claude Code inicia:
- JSON inválido em hooks.json causa falha de carregamento
- Scripts ausentes causam avisos
- Erros de sintaxe reportados em modo debug

Use comando `/hooks` para revisar hooks carregados na sessão atual.

## Depurando Hooks

### Ative Modo Debug

```bash
claude --debug
```

Procure por registro de hook, logs de execução, entrada/saída JSON e informações de timing.

### Teste Scripts de Hook

Teste hooks de comando diretamente:

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "/test"}}' | \
  bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh

echo "Código de saída: $?"
```

### Valide Saída JSON

Garanta que hooks retornem JSON válido:

```bash
output=$(./your-hook.sh < test-input.json)
echo "$output" | jq .
```

## Referência Rápida

### Resumo de Eventos de Hook

| Evento | Quando | Usar Para |
|-------|--------|-----------|
| PreToolUse | Antes da ferramenta | Validação, modificação |
| PostToolUse | Após ferramenta | Feedback, logging |
| UserPromptSubmit | Entrada do usuário | Contexto, validação |
| Stop | Agente parando | Verificação de completude |
| SubagentStop | Subagente pronto | Validação de tarefa |
| SessionStart | Sessão inicia | Carregamento de contexto |
| SessionEnd | Sessão termina | Limpeza, logging |
| PreCompact | Antes de compactar | Preservar contexto |
| Notification | Usuário notificado | Logging, reações |

### Melhores Práticas

**FAÇA:**
- ✅ Use hooks baseados em prompt para lógica complexa
- ✅ Use ${CLAUDE_PLUGIN_ROOT} para portabilidade
- ✅ Valide todas as entradas em hooks de comando
- ✅ Coloque aspas em todas as variáveis bash
- ✅ Defina timeouts apropriados
- ✅ Retorne saída JSON estruturada
- ✅ Teste hooks minuciosamente

**NÃO FAÇA:**
- ❌ Use caminhos hardcoded
- ❌ Confie em entrada do usuário sem validação
- ❌ Crie hooks de longa duração
- ❌ Dependa da ordem de execução de hooks
- ❌ Modifique estado global de forma imprevisível
- ❌ Registre informações sensíveis

## Recursos Adicionais

### Arquivos de Referência

Para padrões detalhados e técnicas avançadas, consulte:

- **`references/patterns.md`** - Padrões comuns de hook (8+ padrões comprovados)
- **`references/migration.md`** - Migrar de hooks básicos para avançados
- **`references/advanced.md`** - Casos de uso avançados e técnicas

### Scripts de Exemplo de Hook

Exemplos em funcionamento em `examples/`:

- **`validate-write.sh`** - Exemplo de validação de escrita de arquivo
- **`validate-bash.sh`** - Exemplo de validação de comando Bash
- **`load-context.sh`** - Exemplo de carregamento de contexto de SessionStart

### Scripts Utilitários

Ferramentas de desenvolvimento em `scripts/`:

- **`validate-hook-schema.sh`** - Valide estrutura e sintaxe de hooks.json
- **`test-hook.sh`** - Teste hooks com entrada de amostra antes da implantação
- **`hook-linter.sh`** - Verifique scripts de hook para problemas comuns e melhores práticas

### Recursos Externos

- **Docs Oficial**: https://docs.claude.com/en/docs/claude-code/hooks
- **Exemplos**: Veja plugin security-guidance no marketplace
- **Testes**: Use `claude --debug` para logs detalhados
- **Validação**: Use `jq` para validar saída JSON de hook

## Workflow de Implementação

Para implementar hooks em um plugin:

1. Identifique eventos para hookear (PreToolUse, Stop, SessionStart, etc.)
2. Decida entre hooks baseados em prompt (flexível) ou comando (determinístico)
3. Escreva configuração de hook em `hooks/hooks.json`
4. Para hooks de comando, crie scripts de hook
5. Use ${CLAUDE_PLUGIN_ROOT} para todas as referências de arquivo
6. Valide configuração com `scripts/validate-hook-schema.sh hooks/hooks.json`
7. Teste hooks com `scripts/test-hook.sh` antes da implantação
8. Teste no Claude Code com `claude --debug`
9. Documente hooks no README do plugin

Foco em hooks baseados em prompt para a maioria dos casos de uso. Reserve hooks de comando para verificações críticas de desempenho ou determinísticas.