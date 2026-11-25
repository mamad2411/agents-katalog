---
name: command-creator
description: Esta skill deve ser usada ao criar um slash command do Claude Code. Use quando usuários pedirem para "criar um comando", "fazer um slash command", "adicionar um comando", ou quiserem documentar um workflow como comando reutilizável. Essencial para criar slash commands otimizados e executáveis por agentes, seguindo boas práticas.
---

# Command Creator

Esta skill orienta a criação de slash commands do Claude Code - workflows reutilizáveis que podem ser invocados com `/command-name` em conversas do Claude Code.

## Sobre Slash Commands

Slash commands são arquivos markdown armazenados em `.claude/commands/` (nível de projeto) ou `~/.claude/commands/` (nível global/usuário) que são expandidos em prompts quando invocados. São ideais para:

- Workflows repetitivos (revisão de código, submissão de PR, correção de CI)
- Processos multi-etapas que precisam de consistência
- Padrões de delegação para agentes
- Automação específica de projeto

## Quando Usar Esta Skill

Invoque esta skill quando usuários:

- Pedirem para "criar um comando" ou "fazer um slash command"
- Quiserem automatizar um workflow repetitivo
- Precisarem documentar um processo consistente para reutilização
- Disserem "fico fazendo X toda hora, podemos criar um comando para isso?"
- Quiserem criar comandos específicos de projeto ou globais

## Recursos Inclusos

Esta skill inclui documentação de referência para orientação detalhada:

- **references/patterns.md** - Padrões de command (automação de workflow, correção iterativa, delegação de agente, execução simples)
- **references/examples.md** - Exemplos reais de commands com código completo (submit-stack, ensure-ci, create-implementation-plan)
- **references/best-practices.md** - Checklist de qualidade, armadilhas comuns, diretrizes de escrita, estrutura de template

Carregue essas referências conforme necessário ao criar commands para entender padrões, ver exemplos ou garantir qualidade.

## Visão Geral da Estrutura de Command

Todo slash command é um arquivo markdown com:

```markdown
---
description: Descrição breve mostrada em /help (obrigatório)
argument-hint: <placeholder> (opcional, se o command tomar argumentos)
---

# Título do Command

[Instruções detalhadas para o agente executar autonomamente]
```

## Workflow de Criação de Command

### Passo 1: Determinar Localização

**Detecte automaticamente a localização apropriada:**

1. Verifique o status do repositório git: `git rev-parse --is-inside-work-tree 2>/dev/null`
2. Localização padrão:
   - Se em repositório git → Nível de projeto: `.claude/commands/`
   - Se não em repositório git → Global: `~/.claude/commands/`
3. Permita sobreposição de usuário:
   - Se usuário mencionar explicitamente "global" ou "nível de usuário" → Use `~/.claude/commands/`
   - Se usuário mencionar explicitamente "projeto" ou "nível de projeto" → Use `.claude/commands/`

Informe a localização escolhida ao usuário antes de prosseguir.

### Passo 2: Mostrar Padrões de Command

Ajude o usuário a entender diferentes tipos de command. Carregue **references/patterns.md** para ver padrões disponíveis:

- **Automação de Workflow** - Analisar → Agir → Relatar (ex: submit-stack)
- **Correção Iterativa** - Executar → Analisar → Corrigir → Repetir (ex: ensure-ci)
- **Delegação de Agente** - Contexto → Delegar → Iterar (ex: create-implementation-plan)
- **Execução Simples** - Executar comando com argumentos (ex: codex-review)

Pergunte ao usuário: "Qual padrão é mais próximo do que você quer criar?" Isso ajuda a enquadrar a conversa.

### Passo 3: Reunir Informações do Command

Peça ao usuário as informações-chave:

#### A. Nome e Propósito do Command

Pergunte:

- "Como o command deve ser chamado?" (para nome de arquivo)
- "O que este command faz?" (para campo description)

Diretrizes:

- Nomes de command DEVEM ser kebab-case (hífens, NÃO underscores)
  - ✅ CORRETO: `submit-stack`, `ensure-ci`, `create-from-plan`
  - ❌ ERRADO: `submit_stack`, `ensure_ci`, `create_from_plan`
- Nomes de arquivos correspondem aos nomes de command: `my-command.md` → invocado como `/my-command`
- Description deve ser concisa, orientada para ação (aparece na saída `/help`)

#### B. Argumentos

Pergunte:

- "Este command toma algum argumento?"
- "Argumentos são obrigatórios ou opcionais?"
- "O que os argumentos devem representar?"

Se o command tomar argumentos:

- Adicione `argument-hint: <placeholder>` ao frontmatter
- Use `<angle-brackets>` para argumentos obrigatórios
- Use `[square-brackets]` para argumentos opcionais

#### C. Passos do Workflow

Pergunte:

- "Quais são os passos específicos que este command deve seguir?"
- "Em qual ordem devem acontecer?"
- "Quais ferramentas ou commands devem ser usados?"

Reúna detalhes sobre:

- Análise inicial ou verificações a realizar
- Ações principais a tomar
- Como lidar com resultados
- Critérios de sucesso
- Abordagem de tratamento de erros

#### D. Restrições de Ferramenta e Orientação

Pergunte:

- "Este command deve usar algum agente ou ferramenta específica?"
- "Há ferramentas ou operações que devem ser evitadas?"
- "Deve ler algum arquivo específico para contexto?"

### Passo 4: Gerar Command Otimizado

Crie o arquivo command com instruções otimizadas para agente. Carregue **references/best-practices.md** para:

- Estrutura de template
- Boas práticas para execução de agente
- Diretrizes de estilo de escrita
- Checklist de qualidade

Princípios-chave:

- Use forma imperativa/infinitiva (instruções começando com verbo)
- Seja explícito e específico
- Inclua resultados esperados
- Forneça exemplos concretos
- Defina tratamento de erros claro

### Passo 5: Criar o Arquivo Command

1. Determine o caminho completo do arquivo:
   - Projeto: `.claude/commands/[command-name].md`
   - Global: `~/.claude/commands/[command-name].md`

2. Verifique se o diretório existe:

   ```bash
   mkdir -p [directory-path]
   ```

3. Escreva o arquivo command usando a ferramenta Write

4. Confirme com o usuário:
   - Informe a localização do arquivo
   - Resuma o que o command faz
   - Explique como usar: `/command-name [arguments]`

### Passo 6: Testar e Iterar (Opcional)

Se o usuário quiser testar:

1. Sugira testes: `Você pode testar este command executando: /command-name [arguments]`
2. Esteja pronto para iterar com base no feedback
3. Atualize o arquivo com melhorias conforme necessário

## Dicas Rápidas

**Para orientação detalhada, carregue as referências incluídas:**

- Carregue **references/patterns.md** ao projetar o workflow do command
- Carregue **references/examples.md** para ver como commands existentes são estruturados
- Carregue **references/best-practices.md** antes de finalizar para garantir qualidade

**Padrões comuns para lembrar:**

- Use Bash tool para comandos `pytest`, `pyright`, `ruff`, `prettier`, `make`, `gt`
- Use Task tool para invocar subagentes para tarefas especializadas
- Verifique primeiramente arquivos específicos (ex: `.PLAN.md`) antes de prosseguir
- Marque todos como completos imediatamente, não em lotes
- Inclua instruções de tratamento de erros explícitas
- Defina critérios de sucesso claros

## Resumo

Ao criar um command:

1. **Detecte a localização** (projeto vs global)
2. **Mostre padrões** para enquadrar a conversa
3. **Reúna informações** (nome, propósito, argumentos, passos, ferramentas)
4. **Gere command otimizado** com instruções executáveis por agente
5. **Crie arquivo** na localização apropriada
6. **Confirme e itere** conforme necessário

Foque em criar commands que agentes possam executar autonomamente, com passos claros, uso explícito de ferramentas e tratamento de erros adequado.