---
name: Command Development
description: Esta habilidade deve ser usada quando o usuário pede para "criar um slash command", "adicionar um comando", "escrever um comando personalizado", "definir argumentos de comando", "usar frontmatter de comando", "organizar comandos", "criar comando com referências de arquivo", "comando interativo", "usar AskUserQuestion em comando", ou precisa de orientação sobre estrutura de slash command, campos de frontmatter YAML, argumentos dinâmicos, execução bash em comandos, padrões de interação com usuário, ou melhores práticas de desenvolvimento de comando para Claude Code.
version: 0.2.0
---

# Command Development para Claude Code

## Visão geral

Slash commands são prompts frequentemente usados definidos como arquivos Markdown que Claude executa durante sessões interativas. Compreender estrutura de comando, opções de frontmatter e recursos dinâmicos permite criar workflows poderosos e reutilizáveis.

**Conceitos-chave:**
- Formato de arquivo Markdown para comandos
- Frontmatter YAML para configuração
- Argumentos dinâmicos e referências de arquivo
- Execução bash para contexto
- Organização e namespacing de comandos

## Fundamentos de Command

### O que é um Slash Command?

Um slash command é um arquivo Markdown contendo um prompt que Claude executa quando invocado. Comandos fornecem:
- **Reutilização**: Define uma vez, usa repetidamente
- **Consistência**: Padroniza workflows comuns
- **Compartilhamento**: Distribui entre equipe ou projetos
- **Eficiência**: Acesso rápido a prompts complexos

### Crítico: Commands são Instruções PARA Claude

**Commands são escritas para consumo do agent, não consumo humano.**

Quando um usuário invoca `/command-name`, o conteúdo do comando se torna as instruções do Claude. Escreva comandos como diretivas PARA Claude sobre o que fazer, não como mensagens PARA o usuário.

**Abordagem correta (instruções para Claude):**
```markdown
Revise este código em busca de vulnerabilidades de segurança incluindo:
- SQL injection
- XSS attacks
- Problemas de autenticação

Forneça números de linha específicos e classificações de severidade.
```

**Abordagem incorreta (mensagens para usuário):**
```markdown
Este comando revisará seu código em busca de problemas de segurança.
Você receberá um relatório com detalhes de vulnerabilidades.
```

O primeiro exemplo instrui Claude sobre o que fazer. O segundo diz ao usuário o que acontecerá mas não instrui Claude. Sempre use a primeira abordagem.

### Locais de Command

**Project commands** (compartilhados com equipe):
- Localização: `.claude/commands/`
- Escopo: Disponível em projeto específico
- Label: Mostrado como "(project)" em `/help`
- Use para: Workflows de equipe, tarefas específicas do projeto

**Personal commands** (disponíveis em todo lugar):
- Localização: `~/.claude/commands/`
- Escopo: Disponível em todos os projetos
- Label: Mostrado como "(user)" em `/help`
- Use para: Workflows pessoais, utilitários entre projetos

**Plugin commands** (agrupados com plugins):
- Localização: `plugin-name/commands/`
- Escopo: Disponível quando plugin instalado
- Label: Mostrado como "(plugin-name)" em `/help`
- Use para: Funcionalidade específica do plugin

## Formato de Arquivo

### Estrutura Básica

Commands são arquivos Markdown com extensão `.md`:

```
.claude/commands/
├── review.md           # /review command
├── test.md             # /test command
└── deploy.md           # /deploy command
```

**Comando simples:**
```markdown
Revise este código em busca de vulnerabilidades de segurança incluindo:
- SQL injection
- XSS attacks
- Bypass de autenticação
- Tratamento inseguro de dados
```

Nenhum frontmatter necessário para comandos básicos.

### Com YAML Frontmatter

Adicione configuração usando YAML frontmatter:

```markdown
---
description: Revise código em busca de problemas de segurança
allowed-tools: Read, Grep, Bash(git:*)
model: sonnet
---

Revise este código em busca de vulnerabilidades de segurança...
```

## Campos YAML Frontmatter

### description

**Propósito:** Descrição breve mostrada em `/help`
**Tipo:** String
**Padrão:** Primeira linha do prompt do comando

```yaml
---
description: Revise pull request em busca de qualidade de código
---
```

**Melhores práticas:** Descrição clara e acionável (menos de 60 caracteres)

### allowed-tools

**Propósito:** Especifique quais ferramentas o comando pode usar
**Tipo:** String ou Array
**Padrão:** Herda da conversa

```yaml
---
allowed-tools: Read, Write, Edit, Bash(git:*)
---
```

**Padrões:**
- `Read, Write, Edit` - Ferramentas específicas
- `Bash(git:*)` - Bash apenas com comandos git
- `*` - Todas as ferramentas (raramente necessário)

**Use quando:** Comando requer acesso a ferramentas específicas

### model

**Propósito:** Especifique modelo para execução do comando
**Tipo:** String (sonnet, opus, haiku)
**Padrão:** Herda da conversa

```yaml
---
model: haiku
---
```

**Casos de uso:**
- `haiku` - Comandos rápidos e simples
- `sonnet` - Workflows padrão
- `opus` - Análise complexa

### argument-hint

**Propósito:** Documente argumentos esperados para autocomplete
**Tipo:** String
**Padrão:** Nenhum

```yaml
---
argument-hint: [pr-number] [priority] [assignee]
---
```

**Benefícios:**
- Ajuda usuários a entender argumentos do comando
- Melhora descoberta de comando
- Documenta interface do comando

### disable-model-invocation

**Propósito:** Impeça a ferramenta SlashCommand de chamar comando programaticamente
**Tipo:** Boolean
**Padrão:** false

```yaml
---
disable-model-invocation: true
---
```

**Use quando:** Comando deve ser apenas invocado manualmente

## Argumentos Dinâmicos

### Usando $ARGUMENTS

Capture todos os argumentos como string única:

```markdown
---
description: Corrija problema por número
argument-hint: [issue-number]
---

Corrija o problema #$ARGUMENTS seguindo nossos padrões de codificação e melhores práticas.
```

**Uso:**
```
> /fix-issue 123
> /fix-issue 456
```

**Expande para:**
```
Corrija o problema #123 seguindo nossos padrões de codificação...
Corrija o problema #456 seguindo nossos padrões de codificação...
```

### Usando Argumentos Posicionais

Capture argumentos individuais com `$1`, `$2`, `$3`, etc.:

```markdown
---
description: Revise PR com prioridade e responsável
argument-hint: [pr-number] [priority] [assignee]
---

Revise pull request #$1 com nível de prioridade $2.
Após revisão, atribua a $3 para acompanhamento.
```

**Uso:**
```
> /review-pr 123 high alice
```

**Expande para:**
```
Revise pull request #123 com nível de prioridade high.
Após revisão, atribua a alice para acompanhamento.
```

### Combinando Argumentos

Misture argumentos posicionais e restantes:

```markdown
Deploy $1 para ambiente $2 com opções: $3
```

**Uso:**
```
> /deploy api staging --force --skip-tests
```

**Expande para:**
```
Deploy api para ambiente staging com opções: --force --skip-tests
```

## Referências de Arquivo

### Usando Sintaxe @

Inclua conteúdo de arquivo em comando:

```markdown
---
description: Revise arquivo específico
argument-hint: [file-path]
---

Revise @$1 em busca de:
- Qualidade de código
- Melhores práticas
- Bugs potenciais
```

**Uso:**
```
> /review-file src/api/users.ts
```

**Efeito:** Claude lê `src/api/users.ts` antes de processar comando

### Múltiplas Referências de Arquivo

Referencie múltiplos arquivos:

```markdown
Compare @src/old-version.js com @src/new-version.js

Identifique:
- Mudanças breaking
- Novos recursos
- Correções de bugs
```

### Referências de Arquivo Estáticas

Referencie arquivos conhecidos sem argumentos:

```markdown
Revise @package.json e @tsconfig.json em busca de consistência

Garanta:
- Versão TypeScript corresponde
- Dependências estão alinhadas
- Configuração de build está correta
```

## Execução Bash em Commands

Commands podem executar comandos bash inline para dinamicamente reunir contexto antes de Claude processar o comando. Isso é útil para incluir estado do repositório, informações de ambiente, ou contexto específico do projeto.

**Quando usar:**
- Inclua contexto dinâmico (git status, variáveis de ambiente, etc.)
- Reúna estado do projeto/repositório
- Construa workflows ciente de contexto

**Detalhes de implementação:**
Para sintaxe completa, exemplos e melhores práticas, veja seção `references/plugin-features-reference.md` sobre execução bash. A referência inclui a sintaxe exata e múltiplos exemplos funcionais para evitar problemas de execução

## Organização de Command

### Estrutura Plana

Organização simples para pequenos conjuntos de comando:

```
.claude/commands/
├── build.md
├── test.md
├── deploy.md
├── review.md
└── docs.md
```

**Use quando:** 5-15 comandos, sem categorias claras

### Estrutura com Namespacing

Organize commands em subdiretórios:

```
.claude/commands/
├── ci/
│   ├── build.md        # /build (project:ci)
│   ├── test.md         # /test (project:ci)
│   └── lint.md         # /lint (project:ci)
├── git/
│   ├── commit.md       # /commit (project:git)
│   └── pr.md           # /pr (project:git)
└── docs/
    ├── generate.md     # /generate (project:docs)
    └── publish.md      # /publish (project:docs)
```

**Benefícios:**
- Agrupamento lógico por categoria
- Namespace mostrado em `/help`
- Mais fácil encontrar comandos relacionados

**Use quando:** 15+ comandos, categorias claras

## Melhores Práticas

### Design de Command

1. **Responsabilidade única:** Um comando, uma tarefa
2. **Descrições claras:** Auto-explicativas em `/help`
3. **Dependências explícitas:** Use `allowed-tools` quando necessário
4. **Documente argumentos:** Sempre forneça `argument-hint`
5. **Nomenclatura consistente:** Use padrão verbo-substantivo (review-pr, fix-issue)

### Manipulação de Argumentos

1. **Valide argumentos:** Verifique argumentos obrigatórios no prompt
2. **Forneça padrões:** Sugira padrões quando argumentos faltam
3. **Documente formato:** Explique formato de argumento esperado
4. **Lide com casos extremos:** Considere argumentos faltantes ou inválidos

```markdown
---
argument-hint: [pr-number]
---

$IF($1,
  Revise PR #$1,
  Forneça um número de PR. Uso: /review-pr [number]
)
```

### Referências de Arquivo

1. **Caminhos explícitos:** Use caminhos de arquivo claros
2. **Verifique existência:** Lide com arquivos ausentes graciosamente
3. **Caminhos relativos:** Use caminhos relativos ao projeto
4. **Suporte Glob:** Considere usar ferramenta Glob para padrões

### Comandos Bash

1. **Limite escopo:** Use `Bash(git:*)` não `Bash(*)`
2. **Comandos seguros:** Evite operações destrutivas
3. **Lide com erros:** Considere falhas de comando
4. **Mantenha rápido:** Comandos de longa execução retardam invocação

### Documentação

1. **Adicione comentários:** Explique lógica complexa
2. **Forneça exemplos:** Mostre uso em comentários
3. **Liste requisitos:** Documente dependências
4. **Versione comandos:** Anote mudanças breaking

```markdown
---
description: Deploy aplicação para ambiente
argument-hint: [environment] [version]
---

<!--
Uso: /deploy [staging|production] [version]
Requer: Credenciais AWS configuradas
Exemplo: /deploy staging v1.2.3
-->

Deploy aplicação para ambiente $1 usando versão $2...
```

## Padrões Comuns

### Padrão de Review

```markdown
---
description: Revise mudanças de código
allowed-tools: Read, Bash(git:*)
---

Arquivos alterados: !`git diff --name-only`

Revise cada arquivo em busca de:
1. Qualidade de código e estilo
2. Bugs ou problemas potenciais
3. Cobertura de teste
4. Necessidades de documentação

Forneça feedback específico para cada arquivo.
```

### Padrão de Testing

```markdown
---
description: Execute testes para arquivo específico
argument-hint: [test-file]
allowed-tools: Bash(npm:*)
---

Execute testes: !`npm test $1`

Analise resultados e sugira correções para falhas.
```

### Padrão de Documentação

```markdown
---
description: Gere documentação para arquivo
argument-hint: [source-file]
---

Gere documentação abrangente para @$1 incluindo:
- Descrições de função/classe
- Documentação de parâmetro
- Descrições de valor retornado
- Exemplos de uso
- Casos extremos e erros
```

### Padrão de Workflow

```markdown
---
description: Workflow completo de PR
argument-hint: [pr-number]
allowed-tools: Bash(gh:*), Read
---

Workflow PR #$1:

1. Busque PR: !`gh pr view $1`
2. Revise mudanças
3. Execute verificações
4. Aprove ou solicite mudanças
```

## Solução de Problemas

**Command não aparece:**
- Verifique se arquivo está no diretório correto
- Verifique se extensão `.md` está presente
- Garanta formato Markdown válido
- Reinicie Claude Code

**Argumentos não funcionando:**
- Verifique se sintaxe `$1`, `$2` está correta
- Verifique se `argument-hint` corresponde ao uso
- Garanta sem espaços extras

**Execução Bash falhando:**
- Verifique se `allowed-tools` inclui Bash
- Verifique sintaxe de comando em backticks
- Teste comando em terminal primeiro
- Verifique permissões necessárias

**Referências de arquivo não funcionando:**
- Verifique se sintaxe `@` está correta
- Verifique se caminho de arquivo é válido
- Garanta se ferramenta Read é permitida
- Use caminhos absolutos ou relativos ao projeto

## Recursos Específicos de Plugin

### Variável CLAUDE_PLUGIN_ROOT

Commands de plugin têm acesso a `${CLAUDE_PLUGIN_ROOT}`, uma variável de ambiente que resolve para o caminho absoluto do plugin.

**Propósito:**
- Referencie arquivos de plugin portavelmente
- Execute scripts de plugin
- Carregue configuração de plugin
- Acesse templates de plugin

**Uso básico:**

```markdown
---
description: Analise usando script de plugin
allowed-tools: Bash(node:*)
---

Execute análise: !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js $1`

Revise resultados e reporte achados.
```

**Padrões comuns:**

```markdown
# Execute script de plugin
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/script.sh`

# Carregue configuração de plugin
@${CLAUDE_PLUGIN_ROOT}/config/settings.json

# Use template de plugin
@${CLAUDE_PLUGIN_ROOT}/templates/report.md

# Acesse recursos de plugin
@${CLAUDE_PLUGIN_ROOT}/docs/reference.md
```

**Por que usar:**
- Funciona em todas as instalações
- Portável entre sistemas
- Sem caminhos hardcoded necessários
- Essencial para plugins multi-arquivo

### Organização de Plugin Command

Commands de plugin são descobertos automaticamente do diretório `commands/`:

```
plugin-name/
├── commands/
│   ├── foo.md              # /foo (plugin:plugin-name)
│   ├── bar.md              # /bar (plugin:plugin-name)
│   └── utils/
│       └── helper.md       # /helper (plugin:plugin-name:utils)
└── plugin.json
```

**Benefícios de namespacing:**
- Agrupamento lógico de comando
- Mostrado em saída `/help`
- Evite conflitos de nome
- Organize comandos relacionados

**Convenções de nomenclatura:**
- Use nomes de ação descritivos
- Evite nomes genéricos (test, run)
- Considere prefixo específico do plugin
- Use hífens para nomes multi-palavra

### Padrões de Plugin Command

**Padrão baseado em configuração:**

```markdown
---
description: Deploy usando configuração de plugin
argument-hint: [environment]
allowed-tools: Read, Bash(*)
---

Carregue configuração: @${CLAUDE_PLUGIN_ROOT}/config/$1-deploy.json

Deploy para $1 usando configurações de definições.
Monitore deployment e reporte status.
```

**Padrão baseado em template:**

```markdown
---
description: Gere docs de template
argument-hint: [component]
---

Template: @${CLAUDE_PLUGIN_ROOT}/templates/docs.md

Gere documentação para $1 seguindo estrutura de template.
```

**Padrão multi-script:**

```markdown
---
description: Workflow de build completo
allowed-tools: Bash(*)
---

Build: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh`
Test: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/test.sh`
Package: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/package.sh`

Revise outputs e reporte status de workflow.
```

**Veja `references/plugin-features-reference.md` para padrões detalhados.**

## Integração com Componentes de Plugin

Commands podem integrar com outros componentes de plugin para workflows poderosos.

### Integração de Agent

Lance agents de plugin para tarefas complexas:

```markdown
---
description: Revisão de código profunda
argument-hint: [file-path]
---

Inicie revisão abrangente de @$1 usando o agent code-reviewer.

O agent analisará:
- Estrutura de código
- Problemas de segurança
- Performance
- Melhores práticas

Agent usa recursos de plugin:
- ${CLAUDE_PLUGIN_ROOT}/config/rules.json
- ${CLAUDE_PLUGIN_ROOT}/checklists/review.md
```

**Pontos-chave:**
- Agent deve existir no diretório `plugin/agents/`
- Claude usa ferramenta Task para lançar agent
- Documente capacidades de agent
- Referencie recursos de plugin que agent usa

### Integração de Skill

Aproveite skills de plugin para conhecimento especializado:

```markdown
---
description: Documente API com padrões
argument-hint: [api-file]
---

Documente API em @$1 seguindo padrões de plugin.

Use a skill api-docs-standards para garantir:
- Documentação completa de endpoint
- Formatação consistente
- Qualidade de exemplo
- Documentação de erro

Gere docs de API prontos para produção.
```

**Pontos-chave:**
- Skill deve existir no diretório `plugin/skills/`
- Mencione nome de skill para disparar invocação
- Documente propósito de skill
- Explique o que skill fornece

### Coordenação de Hook

Projete commands que funcionem com hooks de plugin:
- Commands podem preparar estado para hooks processarem
- Hooks executam automaticamente em eventos de ferramenta
- Commands devem documentar comportamento de hook esperado
- Guie Claude na interpretação de saída de hook

Veja `references/plugin-features-reference.md` para exemplos de commands que coordenam com hooks

### Workflows Multi-Componente

Combine agents, skills e scripts:

```markdown
---
description: Workflow de revisão abrangente
argument-hint: [file]
allowed-tools: Bash(node:*), Read
---

Alvo: @$1

Fase 1 - Análise Estática:
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/lint.js $1`

Fase 2 - Revisão Profunda:
Lance agent code-reviewer para análise detalhada.

Fase 3 - Verificação de Padrões:
Use skill coding-standards para validação.

Fase 4 - Relatório:
Template: @${CLAUDE_PLUGIN_ROOT}/templates/review.md

Compile achados em relatório seguindo template.
```

**Quando usar:**
- Workflows multi-passo complexos
- Aproveite múltiplas capacidades de plugin
- Requer análise especializada
- Necessite saídas estruturadas

## Padrões de Validação

Commands devem validar entradas e recursos antes de processar.

### Validação de Argumento

```markdown
---
description: Deploy com validação
argument-hint: [environment]
---

Valide ambiente: !`echo "$1" | grep -E "^(dev|staging|prod)$" || echo "INVALID"`

Se $1 é ambiente válido:
  Deploy para $1
Caso contrário:
  Explique ambientes válidos: dev, staging, prod
  Mostre uso: /deploy [environment]
```

### Verificações de Existência de Arquivo

```markdown
---
description: Processe configuração
argument-hint: [config-file]
---

Verifique se arquivo existe: !`test -f $1 && echo "EXISTS" || echo "MISSING"`

Se arquivo existe:
  Processe configuração: @$1
Caso contrário:
  Explique onde colocar arquivo de config
  Mostre formato esperado
  Forneça exemplo de configuração
```

### Validação de Recurso de Plugin

```markdown
---
description: Execute analisador de plugin
allowed-tools: Bash(test:*)
---

Valide setup de plugin:
- Script: !`test -x ${CLAUDE_PLUGIN_ROOT}/bin/analyze && echo "✓" || echo "✗"`
- Config: !`test -f ${CLAUDE_PLUGIN_ROOT}/config.json && echo "✓" || echo "✗"`

Se todas as verificações passam, execute análise.
Caso contrário, reporte componentes ausentes.
```

### Tratamento de Erro

```markdown
---
description: Build com tratamento de erro
allowed-tools: Bash(*)
---

Execute build: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/build.sh 2>&1 || echo "BUILD_FAILED"`

Se build sucedeu:
  Reporte sucesso e localização de output
Se build falhou:
  Analise saída de erro
  Sugira causas prováveis
  Forneça etapas de solução de problemas
```

**Melhores práticas:**
- Valide cedo no comando
- Forneça mensagens de erro úteis
- Sugira ações corretivas
- Lide com casos extremos graciosamente

---

Para especificações detalhadas de campo frontmatter, veja `references/frontmatter-reference.md`.
Para recursos específicos de plugin e padrões, veja `references/plugin-features-reference.md`.
Para exemplos de padrão de comando, veja diretório `examples/`.