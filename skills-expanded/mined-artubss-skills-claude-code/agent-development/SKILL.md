---
name: Agent Development
description: Esta habilidade deve ser usada quando o usuário pede para "criar um agent", "adicionar um agent", "escrever um subagent", "frontmatter de agent", "quando usar description", "exemplos de agent", "ferramentas de agent", "cores de agent", "agent autônomo", ou precisa de orientação sobre estrutura de agent, prompts de sistema, condições de acionamento ou melhores práticas de desenvolvimento de agent para plugins Claude Code.
version: 0.1.0
---

# Desenvolvimento de Agents para Plugins Claude Code

## Visão Geral

Agents são subprocessos autônomos que lidam com tarefas complexas e multi-etapas de forma independente. Entender a estrutura de agent, condições de acionamento e design de prompt de sistema permite criar recursos autônomos poderosos.

**Conceitos principais:**
- Agents são PARA trabalho autônomo, comandos são PARA ações iniciadas pelo usuário
- Formato de arquivo Markdown com frontmatter YAML
- Acionamento via campo description com exemplos
- Prompt de sistema define comportamento do agent
- Personalização de modelo e cor

## Estrutura de Arquivo de Agent

### Formato Completo

```markdown
---
name: agent-identifier
description: Use this agent when [triggering conditions]. Examples:

<example>
Context: [Situation description]
user: "[User request]"
assistant: "[How assistant should respond and use this agent]"
<commentary>
[Why this agent should be triggered]
</commentary>
</example>

<example>
[Additional example...]
</example>

model: inherit
color: blue
tools: ["Read", "Write", "Grep"]
---

You are [agent role description]...

**Your Core Responsibilities:**
1. [Responsibility 1]
2. [Responsibility 2]

**Analysis Process:**
[Step-by-step workflow]

**Output Format:**
[What to return]
```

## Campos de Frontmatter

### name (obrigatório)

Identificador de agent usado para namespacing e invocação.

**Formato:** apenas minúsculas, números e hífens
**Comprimento:** 3-50 caracteres
**Padrão:** Deve começar e terminar com alfanumérico

**Bons exemplos:**
- `code-reviewer`
- `test-generator`
- `api-docs-writer`
- `security-analyzer`

**Maus exemplos:**
- `helper` (muito genérico)
- `-agent-` (começa/termina com hífen)
- `my_agent` (underscores não permitidos)
- `ag` (muito curto, < 3 caracteres)

### description (obrigatório)

Define quando Claude deve acionar este agent. **Este é o campo mais crítico.**

**Deve incluir:**
1. Condições de acionamento ("Use este agent quando...")
2. Múltiplos blocos `<example>` mostrando uso
3. Contexto, solicitação do usuário e resposta do assistente em cada exemplo
4. `<commentary>` explicando por que o agent é acionado

**Formato:**
```
Use this agent when [conditions]. Examples:

<example>
Context: [Scenario description]
user: "[What user says]"
assistant: "[How Claude should respond]"
<commentary>
[Why this agent is appropriate]
</commentary>
</example>

[More examples...]
```

**Melhores práticas:**
- Inclua 2-4 exemplos concretos
- Mostre acionamento proativo e reativo
- Cubra diferentes formas de expressar a mesma intenção
- Explique o raciocínio em commentary
- Seja específico sobre quando NÃO usar o agent

### model (obrigatório)

Qual modelo o agent deve usar.

**Opções:**
- `inherit` - Use o mesmo modelo do pai (recomendado)
- `sonnet` - Claude Sonnet (equilibrado)
- `opus` - Claude Opus (mais capaz, mais caro)
- `haiku` - Claude Haiku (rápido, barato)

**Recomendação:** Use `inherit` a menos que o agent precise de capacidades específicas do modelo.

### color (obrigatório)

Identificador visual para o agent na UI.

**Opções:** `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`

**Diretrizes:**
- Escolha cores distintas para diferentes agents no mesmo plugin
- Use cores consistentes para tipos similares de agent
- Azul/ciano: Análise, revisão
- Verde: Tarefas orientadas ao sucesso
- Amarelo: Cuidado, validação
- Vermelho: Crítico, segurança
- Magenta: Criativo, geração

### tools (opcional)

Restrinja o agent a ferramentas específicas.

**Formato:** Array de nomes de ferramentas

```yaml
tools: ["Read", "Write", "Grep", "Bash"]
```

**Padrão:** Se omitido, o agent tem acesso a todas as ferramentas

**Melhor prática:** Limite ferramentas ao mínimo necessário (princípio do menor privilégio)

**Conjuntos de ferramentas comuns:**
- Análise somente leitura: `["Read", "Grep", "Glob"]`
- Geração de código: `["Read", "Write", "Grep"]`
- Testes: `["Read", "Bash", "Grep"]`
- Acesso total: Omita o campo ou use `["*"]`

## Design de Prompt de Sistema

O corpo do markdown se torna o prompt de sistema do agent. Escreva na segunda pessoa, dirigindo-se diretamente ao agent.

### Estrutura

**Template padrão:**
```markdown
You are [role] specializing in [domain].

**Your Core Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]
3. [Additional responsibilities...]

**Analysis Process:**
1. [Step one]
2. [Step two]
3. [Step three]
[...]

**Quality Standards:**
- [Standard 1]
- [Standard 2]

**Output Format:**
Provide results in this format:
- [What to include]
- [How to structure]

**Edge Cases:**
Handle these situations:
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]
```

### Melhores Práticas

✅ **FAÇA:**
- Escreva na segunda pessoa ("You are...", "You will...")
- Seja específico sobre responsabilidades
- Forneça processo passo a passo
- Defina formato de saída
- Inclua padrões de qualidade
- Aborde casos extremos
- Mantenha menos de 10.000 caracteres

❌ **NÃO FAÇA:**
- Escreva na primeira pessoa ("I am...", "I will...")
- Seja vago ou genérico
- Omita etapas do processo
- Deixe formato de saída indefinido
- Pule orientações de qualidade
- Ignore casos de erro

## Criando Agents

### Método 1: Geração Assistida por IA

Use este padrão de prompt (extraído do Claude Code):

```
Create an agent configuration based on this request: "[YOUR DESCRIPTION]"

Requirements:
1. Extract core intent and responsibilities
2. Design expert persona for the domain
3. Create comprehensive system prompt with:
   - Clear behavioral boundaries
   - Specific methodologies
   - Edge case handling
   - Output format
4. Create identifier (lowercase, hyphens, 3-50 chars)
5. Write description with triggering conditions
6. Include 2-3 <example> blocks showing when to use

Return JSON with:
{
  "identifier": "agent-name",
  "whenToUse": "Use this agent when... Examples: <example>...</example>",
  "systemPrompt": "You are..."
}
```

Então converta para formato de arquivo de agent com frontmatter.

Veja `examples/agent-creation-prompt.md` para template completo.

### Método 2: Criação Manual

1. Escolha identificador de agent (3-50 caracteres, minúsculas, hífens)
2. Escreva description com exemplos
3. Selecione modelo (geralmente `inherit`)
4. Escolha cor para identificação visual
5. Defina ferramentas (se restriger acesso)
6. Escreva prompt de sistema com estrutura acima
7. Salve como `agents/agent-name.md`

## Regras de Validação

### Validação de Identificador

```
✅ Válido: code-reviewer, test-gen, api-analyzer-v2
❌ Inválido: ag (muito curto), -start (começa com hífen), my_agent (underscore)
```

**Regras:**
- 3-50 caracteres
- Apenas letras minúsculas, números e hífens
- Deve começar e terminar com alfanumérico
- Sem underscores, espaços ou caracteres especiais

### Validação de Description

**Comprimento:** 10-5.000 caracteres
**Deve incluir:** Condições de acionamento e exemplos
**Ideal:** 200-1.000 caracteres com 2-4 exemplos

### Validação de Prompt de Sistema

**Comprimento:** 20-10.000 caracteres
**Ideal:** 500-3.000 caracteres
**Estrutura:** Responsabilidades claras, processo, formato de saída

## Organização de Agents

### Diretório de Agents do Plugin

```
plugin-name/
└── agents/
    ├── analyzer.md
    ├── reviewer.md
    └── generator.md
```

Todos os arquivos `.md` em `agents/` são descobertos automaticamente.

### Namespacing

Agents são nomeados automaticamente:
- Plugin único: `agent-name`
- Com subdiretórios: `plugin:subdir:agent-name`

## Testando Agents

### Testar Acionamento

Crie cenários de teste para verificar se o agent é acionado corretamente:

1. Escreva agent com exemplos de acionamento específicos
2. Use fraseado similar aos exemplos em teste
3. Verifique se Claude carrega o agent
4. Confirme que o agent fornece funcionalidade esperada

### Testar Prompt de Sistema

Certifique-se de que o prompt de sistema está completo:

1. Dê ao agent tarefa típica
2. Verifique se segue etapas do processo
3. Confirme que formato de saída está correto
4. Teste casos extremos mencionados no prompt
5. Confirme que padrões de qualidade são atendidos

## Referência Rápida

### Agent Mínimo

```markdown
---
name: simple-agent
description: Use this agent when... Examples: <example>...</example>
model: inherit
color: blue
---

You are an agent that [does X].

Process:
1. [Step 1]
2. [Step 2]

Output: [What to provide]
```

### Resumo de Campos de Frontmatter

| Campo | Obrigatório | Formato | Exemplo |
|-------|-------------|---------|---------|
| name | Sim | lowercase-hyphens | code-reviewer |
| description | Sim | Texto + exemplos | Use when... <example>... |
| model | Sim | inherit/sonnet/opus/haiku | inherit |
| color | Sim | Nome da cor | blue |
| tools | Não | Array de nomes de ferramentas | ["Read", "Grep"] |

### Melhores Práticas

**FAÇA:**
- ✅ Inclua 2-4 exemplos concretos em description
- ✅ Escreva condições de acionamento específicas
- ✅ Use `inherit` para modelo a menos que haja necessidade específica
- ✅ Escolha ferramentas apropriadas (menor privilégio)
- ✅ Escreva prompts de sistema claros e estruturados
- ✅ Teste acionamento de agent minuciosamente

**NÃO FAÇA:**
- ❌ Use descrições genéricas sem exemplos
- ❌ Omita condições de acionamento
- ❌ Dê a todos os agents a mesma cor
- ❌ Conceda acesso a ferramentas desnecessárias
- ❌ Escreva prompts de sistema vagos
- ❌ Pule testes

## Recursos Adicionais

### Arquivos de Referência

Para orientação detalhada, consulte:

- **`references/system-prompt-design.md`** - Padrões completos de prompt de sistema
- **`references/triggering-examples.md`** - Formatos de exemplo e melhores práticas
- **`references/agent-creation-system-prompt.md`** - O prompt exato do Claude Code

### Arquivos de Exemplo

Exemplos funcionais em `examples/`:

- **`agent-creation-prompt.md`** - Template de geração de agent assistida por IA
- **`complete-agent-examples.md`** - Exemplos completos de agent para diferentes casos de uso

### Scripts de Utilidade

Ferramentas de desenvolvimento em `scripts/`:

- **`validate-agent.sh`** - Valide estrutura de arquivo de agent
- **`test-agent-trigger.sh`** - Teste se o agent é acionado corretamente

## Fluxo de Implementação

Para criar um agent para um plugin:

1. Defina propósito de agent e condições de acionamento
2. Escolha método de criação (assistido por IA ou manual)
3. Crie arquivo `agents/agent-name.md`
4. Escreva frontmatter com todos os campos obrigatórios
5. Escreva prompt de sistema seguindo melhores práticas
6. Inclua 2-4 exemplos de acionamento em description
7. Valide com `scripts/validate-agent.sh`
8. Teste acionamento com cenários reais
9. Documente agent no README do plugin

Foque em condições de acionamento claras e prompts de sistema abrangentes para operação autônoma.