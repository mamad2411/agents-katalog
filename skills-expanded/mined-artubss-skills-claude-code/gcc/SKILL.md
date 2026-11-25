---
name: gcc
description: "Controlador de Contexto Git (GCC) - Gerencia memória do agente como um sistema de arquivos versionado sob .GCC/. Esta skill deve ser usada ao trabalhar em projetos de múltiplas etapas que se beneficiam de persistência de memória estruturada, rastreamento de marcos, ramificação para abordagens alternativas e recuperação de contexto entre sessões. Ativa com comandos /gcc ou linguagem natural como 'commit this progress', 'branch to try an alternative', 'merge results', 'recover context'."
---

# Controlador de Contexto Git (GCC)

## Visão Geral

O GCC transforma a memória do agente de um fluxo de tokens passivo em um sistema de arquivos estruturado e versionado sob `.GCC/`. Inspirado em Git, fornece quatro operações — COMMIT, BRANCH, MERGE, CONTEXT — para persistir marcos, explorar alternativas isoladamente, sintetizar resultados e recuperar contexto histórico com eficiência.

## Inicialização

No primeiro uso, verifique se `.GCC/` existe na raiz do projeto. Se não existir, execute `scripts/gcc_init.sh` para criar a estrutura de diretórios:

```
.GCC/
├── main.md          # Roadmap global e objetivos
├── metadata.yaml    # Estado da infraestrutura (branches, árvore de arquivos, config)
├── commit.md        # Histórico de commits do branch principal
├── log.md           # Log de execução OTA do branch principal
└── branches/        # Workspaces isolados para experimentos
    └── <branch-name>/
        ├── commit.md
        ├── log.md
        └── summary.md
```

Para especificações detalhadas de formato de arquivo, consulte `references/file_formats.md`.

## Configuração

O comportamento do GCC é controlado via `metadata.yaml`:

- `proactive_commits: true` — Sugere automaticamente commits após completar subtarefas coerentes
- `proactive_commits: false` — Apenas faz commit quando explicitamente solicitado

Alterne com: "enable/disable proactive commits" ou editando `metadata.yaml`.

## Comandos

### COMMIT

Persiste um marco no branch atual.

**Ativa com**: `/gcc commit <summary>`, "commit this progress", "save this milestone", "checkpoint"

**Procedimento**:
1. Leia o `commit.md` do branch atual para determinar o próximo número de commit
2. Acrescente uma nova entrada a `commit.md` com:
   - ID sequencial (ex.: `[C004]`)
   - Data (UTC ISO 8601)
   - Nome do branch atual
   - Propósito do branch (de `summary.md` se em um branch, ou de `main.md`)
   - Resumo do progresso anterior (1-2 frases do último commit)
   - Contribuição deste commit (descrição técnica detalhada com arquivos tocados)
3. Acrescente uma entrada OTA a `log.md` registrando a ação de commit
4. Atualize a árvore de arquivos em `metadata.yaml` se arquivos foram criados/modificados
5. Se no branch principal, atualize a seção de marcos em `main.md`

**Comportamento proativo**: Quando `proactive_commits: true`, sugira um commit após:
- Completar uma função, módulo ou unidade coerente de trabalho
- Corrigir um bug e verificar a correção
- Terminar uma fase de pesquisa/exploração com conclusões
- Qualquer ponto onde perder contexto significaria refazer trabalho significativo

### BRANCH

Cria um workspace isolado para explorar uma abordagem alternativa.

**Ativa com**: `/gcc branch <name>`, "branch to try...", "explore alternative...", "experiment with..."

**Procedimento**:
1. Crie o diretório `.GCC/branches/<branch-name>/`
2. Crie `summary.md` com: propósito, branch pai, data de criação, hipóteses principais
3. Crie `commit.md` e `log.md` vazios para o branch
4. Atualize `metadata.yaml` para registrar o novo branch
5. Atualize a seção Active Branches em `main.md`
6. Registre a criação do branch no `log.md` do branch pai

A partir deste ponto, todos os COMMITs e logs OTA vão para os arquivos específicos do branch até um MERGE ou mudança explícita de branch.

### MERGE

Integra um branch completo de volta ao fluxo principal.

**Ativa com**: `/gcc merge <branch>`, "merge results from...", "integrate the experiment", "branch X is done"

**Procedimento**:
1. Leia `summary.md` e `commit.md` do branch para compreender resultados
2. Acrescente um commit de síntese ao `commit.md` do branch principal resumindo:
   - O que foi tentado
   - O que foi aprendido
   - O que está sendo integrado (ou por que o branch está sendo abandonado)
3. Atualize `main.md`:
   - Adicione entrada de marco com resultados do branch
   - Remova da seção Active Branches
   - Atualize objetivos se aplicável
4. Atualize `metadata.yaml`: defina status do branch como `merged` ou `abandoned`
5. Registre o merge no `log.md` do branch principal

### CONTEXT

Recupera memória histórica em diferentes níveis de resolução.

**Ativa com**: `/gcc context <flag>`, "what did we do on...", "recover context", "show me the history", "where were we"

**Flags**:

- `--branch [name]` — Leia `summary.md` e últimos commits para um branch específico (ou branch atual se nenhum nome for fornecido). Fornece compreensão de alto nível do que aconteceu e por quê.

- `--log [n]` — Leia as últimas N entradas (padrão 20) do `log.md` do branch atual. Fornece rastreamentos OTA granulares para debug ou retomada de trabalho interrompido.

- `--metadata` — Leia `metadata.yaml` para recuperar a estrutura do projeto: árvore de arquivos, dependências, branches ativos, configuração.

- `--full` — Leia `main.md` para o roadmap completo do projeto, todos os marcos e branches ativos. Use para recuperação entre sessões ou handoff para outro agente.

Quando nenhuma flag for especificada, use como padrão `--branch` para o branch ativo atual.

## Log de Execução OTA

Durante todo trabalho (não apenas durante comandos explícitos), mantenha o log de execução OTA:

1. **Observation** (Observação): O que foi notado ou descoberto
2. **Thought** (Pensamento): Raciocínio sobre o que fazer a seguir
3. **Action** (Ação): Que ação foi tomada

Acrescente entradas ao `log.md` do branch ativo. Mantenha um máximo de 50 entradas; ao exceder, remova as entradas mais antigas. Cada entrada inclui um ID sequencial, timestamp e nome do branch.

Registre entradas OTA em pontos significativos de decisão — não em cada ação isolada, mas em observações significativas, mudanças de estratégia e resultados.

## Recuperação Entre Sessões

Ao iniciar uma nova sessão em um projeto existente com `.GCC/`:

1. Leia `metadata.yaml` para compreender o estado do projeto e branches ativos
2. Leia `main.md` para o roadmap global e objetivos
3. Leia os últimos commits e entradas de log do branch ativo
4. Retome o trabalho com contexto completo do que foi realizado e do que resta

## Mapeamento de Linguagem Natural

| Você diz | Comando |
|---|---|
| "save/checkpoint/persist this" | COMMIT |
| "try a different approach" | BRANCH |
| "that experiment worked, integrate it" | MERGE |
| "where were we?" / "what's the status?" | CONTEXT --full |
| "what happened on branch X?" | CONTEXT --branch X |
| "show recent activity" | CONTEXT --log |
| "what files do we have?" | CONTEXT --metadata |
| "enable/disable auto-commits" | Alterne `proactive_commits` em metadata.yaml |