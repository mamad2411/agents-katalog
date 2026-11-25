---
name: Plugin Settings
description: Essa habilidade deve ser usada quando o usuário pergunta sobre "plugin settings", "armazenar configuração de plugin", "plugin configurável pelo usuário", "arquivos .local.md", "arquivos de estado de plugin", "ler YAML frontmatter", "configurações de plugin por projeto", ou quer tornar o comportamento do plugin configurável. Documenta o padrão .claude/plugin-name.local.md para armazenar configuração específica do plugin com YAML frontmatter e conteúdo markdown.
version: 0.1.0
---

# Padrão de Plugin Settings para Claude Code Plugins

## Visão Geral

Plugins podem armazenar configurações e estado configuráveis pelo usuário em arquivos `.claude/plugin-name.local.md` dentro do diretório do projeto. Este padrão usa YAML frontmatter para configuração estruturada e conteúdo markdown para prompts ou contexto adicional.

**Características principais:**
- Localização do arquivo: `.claude/plugin-name.local.md` na raiz do projeto
- Estrutura: YAML frontmatter + corpo markdown
- Propósito: Configuração e estado de plugin por projeto
- Uso: Leitura em hooks, comandos e agents
- Ciclo de vida: Gerenciado pelo usuário (não em git, deve estar em `.gitignore`)

## Estrutura do Arquivo

### Template Básico

```markdown
---
enabled: true
setting1: value1
setting2: value2
numeric_setting: 42
list_setting: ["item1", "item2"]
---

# Contexto Adicional

O corpo markdown pode conter:
- Descrições de tarefas
- Instruções adicionais
- Prompts para feedback ao Claude
- Documentação ou notas
```

### Exemplo: Arquivo de Estado do Plugin

**.claude/my-plugin.local.md:**
```markdown
---
enabled: true
strict_mode: false
max_retries: 3
notification_level: info
coordinator_session: team-leader
---

# Configuração do Plugin

Este plugin está configurado para modo de validação padrão.
Contate @team-lead com dúvidas.
```

## Leitura de Arquivos de Configuração

### De Hooks (Scripts Bash)

**Padrão: Verificar existência e fazer parse de frontmatter**

```bash
#!/bin/bash
set -euo pipefail

# Definir caminho do arquivo de estado
STATE_FILE=".claude/my-plugin.local.md"

# Sair rápido se o arquivo não existir
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Plugin não configurado, ignorar
fi

# Fazer parse de YAML frontmatter (entre marcadores ---)
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

# Extrair campos individuais
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//' | sed 's/^"\(.*\)"$/\1/')
STRICT_MODE=$(echo "$FRONTMATTER" | grep '^strict_mode:' | sed 's/strict_mode: *//' | sed 's/^"\(.*\)"$/\1/')

# Verificar se está habilitado
if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Desabilitado
fi

# Usar configuração na lógica do hook
if [[ "$STRICT_MODE" == "true" ]]; then
  # Aplicar validação rigorosa
  # ...
fi
```

Veja `examples/read-settings-hook.sh` para exemplo completo funcionando.

### De Comandos

Comandos podem ler arquivos de configuração para personalizar comportamento:

```markdown
---
description: Processar dados com plugin
allowed-tools: ["Read", "Bash"]
---

# Comando de Processamento

Passos:
1. Verificar se configurações existem em `.claude/my-plugin.local.md`
2. Ler configuração usando ferramenta Read
3. Fazer parse de YAML frontmatter para extrair configurações
4. Aplicar configurações à lógica de processamento
5. Executar com comportamento configurado
```

### De Agents

Agents podem fazer referência a configurações em suas instruções:

```markdown
---
name: configured-agent
description: Agent que se adapta às configurações do projeto
---

Verificar se há configurações de plugin em `.claude/my-plugin.local.md`.
Se presente, fazer parse de YAML frontmatter e adaptar comportamento conforme:
- enabled: Se o plugin está ativo
- mode: Modo de processamento (strict, standard, lenient)
- Campos de configuração adicionais
```

## Técnicas de Parsing

### Extrair Frontmatter

```bash
# Extrair tudo entre marcadores ---
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

### Ler Campos Individuais

**Campos string:**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**Campos booleanos:**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
# Comparar: if [[ "$ENABLED" == "true" ]]; then
```

**Campos numéricos:**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')
# Usar: if [[ $MAX -gt 100 ]]; then
```

### Ler Corpo Markdown

Extrair conteúdo após o segundo `---`:

```bash
# Obter tudo após o fechamento de ---
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

## Padrões Comuns

### Padrão 1: Hooks Temporariamente Ativos

Usar arquivo de configuração para controlar ativação de hook:

```bash
#!/bin/bash
STATE_FILE=".claude/security-scan.local.md"

# Sair rápido se não configurado
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# Ler flag enabled
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Desabilitado
fi

# Executar lógica do hook
# ...
```

**Caso de uso:** Habilitar/desabilitar hooks sem editar hooks.json (requer reinicialização).

### Padrão 2: Gerenciamento de Estado de Agent

Armazenar estado e configuração específicos do agent:

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-agent
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
---

# Atribuição de Tarefa

Implementar autenticação JWT para a API.

**Critérios de Sucesso:**
- Endpoints de autenticação criados
- Testes passando
- PR criado e CI verde
```

Ler de hooks para coordenar agents:

```bash
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//')
COORDINATOR=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//')

# Enviar notificação ao coordenador
tmux send-keys -t "$COORDINATOR" "Agent $AGENT_NAME completed task" Enter
```

### Padrão 3: Comportamento Orientado por Configuração

**.claude/my-plugin.local.md:**
```markdown
---
validation_level: strict
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
---

# Configuração de Validação

Modo rigoroso habilitado para este projeto.
Todas as escritas validadas contra políticas de segurança.
```

Usar em hooks ou comandos:

```bash
LEVEL=$(echo "$FRONTMATTER" | grep '^validation_level:' | sed 's/validation_level: *//')

case "$LEVEL" in
  strict)
    # Aplicar validação rigorosa
    ;;
  standard)
    # Aplicar validação padrão
    ;;
  lenient)
    # Aplicar validação permissiva
    ;;
esac
```

## Criando Arquivos de Configuração

### De Comandos

Comandos podem criar arquivos de configuração:

```markdown
# Comando de Setup

Passos:
1. Perguntar ao usuário suas preferências de configuração
2. Criar `.claude/my-plugin.local.md` com YAML frontmatter
3. Definir valores apropriados baseado na entrada do usuário
4. Informar ao usuário que configurações foram salvas
5. Lembrar o usuário de reiniciar Claude Code para hooks reconhecerem mudanças
```

### Geração de Template

Fornecer template na documentação do plugin:

```markdown
## Configuração

Criar `.claude/my-plugin.local.md` em seu projeto:

\`\`\`markdown
---
enabled: true
mode: standard
max_retries: 3
---

# Configuração do Plugin

Suas configurações estão ativas.
\`\`\`

Após criar ou editar, reiniciar Claude Code para que as mudanças tenham efeito.
```

## Melhores Práticas

### Nomenclatura de Arquivo

✅ **FAZER:**
- Usar formato `.claude/plugin-name.local.md`
- Corresponder nome do plugin exatamente
- Usar sufixo `.local.md` para arquivos locais do usuário

❌ **NÃO FAZER:**
- Usar diretório diferente (não `.claude/`)
- Usar nomenclatura inconsistente
- Usar `.md` sem `.local` (pode ser commitado)

### Gitignore

Sempre adicionar ao `.gitignore`:

```gitignore
.claude/*.local.md
.claude/*.local.json
```

Documentar isso no README do plugin.

### Padrões Padrão

Fornecer padrões sensatos quando arquivo de configuração não existe:

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  # Usar padrões
  ENABLED=true
  MODE=standard
else
  # Ler do arquivo
  # ...
fi
```

### Validação

Validar valores de configuração:

```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# Validar intervalo numérico
if ! [[ "$MAX" =~ ^[0-9]+$ ]] || [[ $MAX -lt 1 ]] || [[ $MAX -gt 100 ]]; then
  echo "⚠️  max_value inválido em configurações (deve ser 1-100)" >&2
  MAX=10  # Usar padrão
fi
```

### Requisito de Reinicialização

**Importante:** Mudanças de configuração requerem reinicialização do Claude Code.

Documentar no seu README:

```markdown
## Alterando Configurações

Após editar `.claude/my-plugin.local.md`:
1. Salvar o arquivo
2. Sair do Claude Code
3. Reiniciar: `claude` ou `cc`
4. Novas configurações serão carregadas
```

Hooks não podem ser trocados a quente dentro de uma sessão.

## Considerações de Segurança

### Sanitizar Entrada do Usuário

Ao escrever arquivos de configuração a partir de entrada do usuário:

```bash
# Escapar aspas na entrada do usuário
SAFE_VALUE=$(echo "$USER_INPUT" | sed 's/"/\\"/g')

# Escrever no arquivo
cat > "$STATE_FILE" <<EOF
---
user_setting: "$SAFE_VALUE"
---
EOF
```

### Validar Caminhos de Arquivo

Se configurações contêm caminhos de arquivo:

```bash
FILE_PATH=$(echo "$FRONTMATTER" | grep '^data_file:' | sed 's/data_file: *//')

# Verificar travessia de diretório
if [[ "$FILE_PATH" == *".."* ]]; then
  echo "⚠️  Caminho inválido em configurações (travessia de diretório)" >&2
  exit 2
fi
```

### Permissões

Arquivos de configuração devem ser:
- Legíveis apenas pelo usuário (`chmod 600`)
- Não commitados em git
- Não compartilhados entre usuários

## Exemplos do Mundo Real

### Plugin multi-agent-swarm

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: Usar tokens JWT, não sessões
---

# Tarefa: Implementar Autenticação

Construir autenticação baseada em JWT para a API REST.
Coordenar com auth-agent em tipos compartilhados.
```

**Uso do hook (agent-stop-notification.sh):**
- Verifica se arquivo existe (linhas 15-18: sair rápido se não)
- Faz parse de frontmatter para obter coordinator_session, agent_name, enabled
- Envia notificações ao coordenador se habilitado
- Permite ativação/desativação rápida via `enabled: true/false`

### Plugin ralph-wiggum

**.claude/ralph-loop.local.md:**
```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "Todos os testes passando e build bem-sucedido"
---

Corrigir todos os erros de lint no projeto.
Certificar que testes passam após cada correção.
```

**Uso do hook (stop-hook.sh):**
- Verifica se arquivo existe (linhas 15-18: sair rápido se não ativo)
- Lê contagem de iteração e max_iterations
- Extrai completion_promise para terminação do loop
- Lê corpo como prompt para fazer feedback
- Atualiza contagem de iteração a cada loop

## Referência Rápida

### Localização do Arquivo

```
project-root/
└── .claude/
    └── plugin-name.local.md
```

### Parsing de Frontmatter

```bash
# Extrair frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")

# Ler campo
VALUE=$(echo "$FRONTMATTER" | grep '^field:' | sed 's/field: *//' | sed 's/^"\(.*\)"$/\1/')
```

### Parsing de Corpo

```bash
# Extrair corpo (após o segundo ---)
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```

### Padrão de Saída Rápida

```bash
if [[ ! -f ".claude/my-plugin.local.md" ]]; then
  exit 0  # Não configurado
fi
```

## Recursos Adicionais

### Arquivos de Referência

Para padrões de implementação detalhados:

- **`references/parsing-techniques.md`** - Guia completo para fazer parse de YAML frontmatter e corpos markdown
- **`references/real-world-examples.md`** - Deep dive em implementações de multi-agent-swarm e ralph-wiggum

### Arquivos de Exemplo

Exemplos funcionando em `examples/`:

- **`read-settings-hook.sh`** - Hook que lê e usa configurações
- **`create-settings-command.md`** - Comando que cria arquivo de configuração
- **`example-settings.md`** - Template de arquivo de configuração

### Scripts Utilitários

Ferramentas de desenvolvimento em `scripts/`:

- **`validate-settings.sh`** - Validar estrutura do arquivo de configuração
- **`parse-frontmatter.sh`** - Extrair campos de frontmatter

## Workflow de Implementação

Para adicionar configurações a um plugin:

1. Projetar schema de configurações (quais campos, tipos, padrões)
2. Criar arquivo template na documentação do plugin
3. Adicionar entrada gitignore para `.claude/*.local.md`
4. Implementar parsing de configurações em hooks/comandos
5. Usar padrão de saída rápida (verificar existência do arquivo, verificar campo enabled)
6. Documentar configurações no README do plugin com template
7. Lembrar usuários que mudanças requerem reinicialização do Claude Code

Focar em manter configurações simples e fornecer bons padrões quando arquivo de configuração não existe.