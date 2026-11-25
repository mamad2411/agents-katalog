---
name: gepetto
description: Cria planos de implementação detalhados e segmentados através de pesquisa, entrevistas com stakeholders e revisão multi-LLM. Use quando planejar features que precisam de análise pré-implementação aprofundada.
---

# Gepetto

Orquestra um processo de planejamento com múltiplas etapas: Pesquisa → Entrevista → Síntese de Especificação → Plano → Revisão Externa → Seções

## CRÍTICO: Primeiras Ações

**ANTES de qualquer coisa**, faça isso em ordem:

### 1. Imprimir Introdução

Imprima o banner de introdução imediatamente:
```
═══════════════════════════════════════════════════════════════
GEPETTO: Planejamento de Implementação Assistido por IA
═══════════════════════════════════════════════════════════════
Pesquisa → Entrevista → Síntese de Especificação → Plano → Revisão Externa → Seções

Nota: GEPETTO escreverá muitos arquivos .md no diretório de planejamento que você passar
```

### 2. Validar Entrada de Arquivo de Especificação

**Verifique se o usuário forneceu @file na invocação E se é um arquivo de especificação (termina com `.md`).**

Se NENHUM @file foi fornecido OU o caminho não termina com `.md`, imprima isto e PARE:
```
═══════════════════════════════════════════════════════════════
GEPETTO: Arquivo de Especificação Obrigatório
═══════════════════════════════════════════════════════════════

Esta habilidade requer um caminho de arquivo markdown de especificação (deve terminar com .md).
O diretório de planejamento é inferido do diretório pai do arquivo de especificação.

Para iniciar um NOVO plano:
  1. Crie um arquivo markdown de especificação descrevendo o que você quer construir
  2. Pode ser tão detalhado ou vago quanto você quiser
  3. Coloque-o em um diretório onde o gepetto possa salvar arquivos de planejamento
  4. Execute: /gepetto @caminho/para/sua-spec.md

Para RETOMAR um plano existente:
  1. Execute: /gepetto @caminho/para/sua-spec.md

Exemplo: /gepetto @planning/minha-feature-spec.md
═══════════════════════════════════════════════════════════════
```
**Não continue. Aguarde o usuário reinvocar com um caminho de arquivo .md.**

### 3. Configurar Sessão de Planejamento

Determine o estado da sessão verificando arquivos existentes:

1. Defina `planning_dir` = diretório pai do arquivo de especificação
2. Defina `initial_file` = caminho do arquivo de especificação
3. Verifique arquivos de planejamento existentes:
   - `claude-research.md`
   - `claude-interview.md`
   - `claude-spec.md`
   - `claude-plan.md`
   - `claude-integration-notes.md`
   - `claude-ralph-loop-prompt.md`
   - `claude-ralphy-prd.md`
   - diretório `reviews/`
   - diretório `sections/`

4. Determine modo e ponto de retomada:

| Arquivos Encontrados | Modo | Retomar De |
|-------------|------|-------------|
| Nenhum | novo | Etapa 4 |
| pesquisa apenas | retomar | Etapa 6 (entrevista) |
| pesquisa + entrevista | retomar | Etapa 8 (síntese de especificação) |
| + especificação | retomar | Etapa 9 (plano) |
| + plano | retomar | Etapa 10 (revisão externa) |
| + reviews | retomar | Etapa 11 (integrar) |
| + integration-notes | retomar | Etapa 12 (revisão do usuário) |
| + sections/index.md | retomar | Etapa 14 (escrever seções) |
| todas as seções completas | retomar | Etapa 15 (arquivos de execução) |
| + claude-ralph-loop-prompt.md + claude-ralphy-prd.md | completo | Feito |

5. Crie lista TODO com TodoWrite baseada no estado atual

Imprima status:
```
Diretório de planejamento: {planning_dir}
Modo: {modo}
```

Se retomando:
```
Retomando da etapa {N}
Para começar do zero, delete os arquivos do diretório de planejamento.
```

---

## Formato de Log

```
═══════════════════════════════════════════════════════════════
ETAPA {N}/17: {NOME_DA_ETAPA}
═══════════════════════════════════════════════════════════════
{detalhes}
Etapa {N} completa: {resumo}
───────────────────────────────────────────────────────────────
```

---

## Fluxo de Trabalho

### 4. Decisão de Pesquisa

Veja [research-protocol.md](references/research-protocol.md).

1. Leia o arquivo de especificação
2. Extraia tópicos de pesquisa potenciais (tecnologias, padrões, integrações)
3. Pergunte ao usuário sobre necessidades de pesquisa de codebase
4. Pergunte ao usuário sobre necessidades de pesquisa web (apresente tópicos derivados como multi-select)
5. Registre quais tipos de pesquisa executar na etapa 5

### 5. Executar Pesquisa

Veja [research-protocol.md](references/research-protocol.md).

Baseado nas decisões da etapa 4, lance subagentes de pesquisa:
- **Pesquisa de codebase:** `Task(subagent_type=Explore)`
- **Pesquisa web:** `Task(subagent_type=Explore)` com WebSearch

Se ambas são necessárias, lance ambas Task tools em paralelo (mensagem única com múltiplas chamadas de ferramenta).

**Importante:** Subagentes retornam suas descobertas - eles NÃO escrevem arquivos diretamente. Após coletar resultados de todos os subagentes, combine-os e escreva para `<planning_dir>/claude-research.md`.

Pule esta etapa inteiramente se o usuário escolheu nenhuma pesquisa na etapa 4.

### 6. Entrevista Detalhada

Veja [interview-protocol.md](references/interview-protocol.md)

Execute no contexto principal (AskUserQuestion requer isso). A entrevista deve ser informada por:
- A especificação inicial
- Descobertas de pesquisa (se houver)

### 7. Salvar Transcrição de Entrevista

Escreva Q&A para `<planning_dir>/claude-interview.md`

### 8. Escrever Especificação Inicial (Síntese de Especificação)

Combine em `<planning_dir>/claude-spec.md`:
- **Entrada inicial** (arquivo de especificação)
- **Descobertas de pesquisa** (se etapa 5 foi feita)
- **Respostas de entrevista** (da etapa 6)

Isso sintetiza os requisitos brutos do usuário em uma especificação completa.

### 9. Gerar Plano de Implementação

Crie plano detalhado → `<planning_dir>/claude-plan.md`

**IMPORTANTE**: Escreva para um leitor desconhecido. O plano deve ser completamente auto-contido - um engenheiro ou LLM sem contexto prévio deve entender *o que* estamos construindo, *por quê*, e *como* apenas lendo este documento.

### 10. Revisão Externa

Veja [external-review.md](references/external-review.md)

Lance DOIS subagentes em paralelo para revisar o plano:
1. **Gemini** via Bash
2. **Codex** via Bash

Ambos recebem o conteúdo do plano e retornam sua análise. Escreva resultados para `<planning_dir>/reviews/`.

### 11. Integrar Feedback Externo

Analise as sugestões em `<planning_dir>/reviews/`.

Você é a autoridade no que integrar ou não. É OK se você decidir não integrar nada.

**Etapa 1:** Escreva `<planning_dir>/claude-integration-notes.md` documentando:
- Quais sugestões você está integrando e por quê
- Quais sugestões você NÃO está integrando e por quê

**Etapa 2:** Atualize `<planning_dir>/claude-plan.md` com as mudanças integradas.

### 12. Revisão do Usuário do Plano Integrado

Use AskUserQuestion:
```
O plano foi atualizado com feedback externo. Você pode agora revisar e editar claude-plan.md.

Se você quer ajuda do Claude para editar o plano, abra uma sessão Claude separada - esta sessão
está no meio do fluxo de trabalho e não pode ajudar com edições até o fluxo de trabalho ser concluído.

Quando terminar a revisão, selecione "Feito" para continuar.
```

Opções: "Terminei a revisão"

Aguarde confirmação do usuário antes de prosseguir.

### 13. Criar Índice de Seções

Veja [section-index.md](references/section-index.md)

Leia `claude-plan.md`. Identifique limites naturais de seções e crie `<planning_dir>/sections/index.md`.

**CRÍTICO:** index.md DEVE começar com um bloco SECTION_MANIFEST. Veja a referência para requisitos de formato.

Escreva `index.md` antes de prosseguir para a criação de arquivos de seção.

### 14. Escrever Arquivos de Seção — Subagentes em Paralelo

Veja [section-splitting.md](references/section-splitting.md)

**Lance subagentes em paralelo** - uma Task por seção para máxima eficiência:

1. Primeiro, analise `sections/index.md` para obter a lista SECTION_MANIFEST
2. Então lance TODAS as Tasks de seção em uma única mensagem (execução paralela):

```
# Lance todas em UMA mensagem para execução paralela:

Task(
  subagent_type="general-purpose",
  prompt="""
  Escreva arquivo de seção: section-01-{name}

  Entradas:
  - <planning_dir>/claude-plan.md
  - <planning_dir>/sections/index.md

  Saída: <planning_dir>/sections/section-01-{name}.md

  O arquivo de seção deve ser COMPLETAMENTE AUTO-CONTIDO. Inclua:
  - Background (por que esta seção existe)
  - Requisitos (o que deve ser verdadeiro quando completo)
  - Dependências (requer/bloqueia)
  - Detalhes de implementação (do plano)
  - Critérios de aceitação (checkboxes)
  - Arquivos a criar/modificar

  O implementador NÃO deve precisar referenciar nenhum outro documento.
  """
)

Task(
  subagent_type="general-purpose",
  prompt="Escreva arquivo de seção: section-02-{name} ..."
)

Task(
  subagent_type="general-purpose",
  prompt="Escreva arquivo de seção: section-03-{name} ..."
)

# ... uma Task por seção no manifesto
```

Aguarde conclusão de TODOS os subagentes antes de prosseguir.

### 15. Gerar Arquivos de Execução — Subagente

**Delegue a subagente** para reduzir uso de tokens do contexto principal:

```
Task(
  subagent_type="general-purpose",
  prompt="""
  Gere dois arquivos de execução para implementação autônoma.

  Arquivos de entrada:
  - <planning_dir>/sections/index.md (tem SECTION_MANIFEST)
  - <planning_dir>/sections/section-*.md (todos os arquivos de seção)

  SAÍDA 1: <planning_dir>/claude-ralph-loop-prompt.md
  Para plugin ralph-loop. INCORPORE todo conteúdo de seção inline.

  Estrutura:
  - Declaração de missão
  - Conteúdo completo de sections/index.md
  - Conteúdo completo de CADA arquivo de seção (incorporado, não referenciado)
  - Regras de execução (ordem de dependência, verificar critérios de aceitação)
  - Sinal de conclusão: <promise>ALL-SECTIONS-COMPLETE</promise>

  SAÍDA 2: <planning_dir>/claude-ralphy-prd.md
  Para CLI Ralphy. REFERENCIE arquivos de seção (não incorpore).

  Estrutura:
  - Cabeçalho PRD
  - Como usar (comando ralphy --prd)
  - Explicação de contexto
  - Lista de tarefas com checkbox: um "- [ ] Seção NN: {name}" por seção

  Escreva ambos os arquivos.
  """
)
```

Aguarde conclusão do subagente antes de prosseguir.

### 16. Status Final

Verifique se todos os arquivos foram criados com sucesso:
- Todos os arquivos de seção do SECTION_MANIFEST
- `claude-ralph-loop-prompt.md`
- `claude-ralphy-prd.md`

### 17. Resumo de Saída

Imprima arquivos gerados e próximos passos:
```
═══════════════════════════════════════════════════════════════
GEPETTO: Planejamento Completo
═══════════════════════════════════════════════════════════════

Arquivos gerados:
  - claude-research.md (descobertas de pesquisa)
  - claude-interview.md (transcrição Q&A)
  - claude-spec.md (especificação sintetizada)
  - claude-plan.md (plano de implementação)
  - claude-integration-notes.md (decisões de feedback)
  - reviews/ (feedback de LLM externo)
  - sections/ (unidades de implementação)
  - claude-ralph-loop-prompt.md (para plugin ralph-loop)
  - claude-ralphy-prd.md (para CLI Ralphy)

Como implementar:

Opção A - Manual (recomendado para aprendizado/controle):
  1. Leia sections/index.md para entender dependências
  2. Implemente cada arquivo de seção em ordem
  3. Cada seção é auto-contida com critérios de aceitação

Opção B - Autônoma com ralph-loop (plugin Claude Code):
  /ralph-loop @<planning_dir>/claude-ralph-loop-prompt.md --completion-promise "COMPLETE" --max-iterations 100

Opção C - Autônoma com Ralphy (CLI externo):
  ralphy --prd <planning_dir>/claude-ralphy-prd.md
  # Ou: cp <planning_dir>/claude-ralphy-prd.md ./PRD.md && ralphy
═══════════════════════════════════════════════════════════════
```