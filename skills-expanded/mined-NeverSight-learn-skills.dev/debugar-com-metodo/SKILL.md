---
name: debugar-com-metodo
description: Use when encountering any bug, test failure, unexpected behavior, flaky test, CI failure, performance issue, build/integration failure, or mysterious regression on Track work — before proposing fixes
---

# Debugar com Método

## Visão geral

Patches aleatórios gastam tempo e criam bugs novos. Fixes de sintoma são falha.

**Princípio:** SEMPRE achar a causa raiz antes de tentar corrigir.

**Violar a letra deste processo é violar o espírito do debug.**

**Anuncie:** "Usando debugar-com-metodo para achar a causa raiz."

**Origem:** adaptação completa do Superpowers `systematic-debugging`, com gates Track/Contexto Certo.

**Pré-requisito Track:** se o trabalho vem de uma task, garanta contexto MCP (`implementar-task` Fase 0 / `get_release_planning_context`) antes de “corrigir no escuro”. Se MCP der **401** → `setup`.

## Lei de ferro

```
NENHUM FIX SEM INVESTIGAÇÃO DE CAUSA RAIZ ANTES
```

Se não completou a **Fase 1**, não proponha correção.

## Quando usar

Qualquer issue técnica:
- Teste falhando / flaky
- Bug em staging/prod
- Comportamento estranho
- Performance
- Build / CI
- Integração (API → serviço → DB, front → back, MCP → Nest)

**Use ESPECIALMENTE quando:**
- Há pressão de tempo (emergência tenta chute)
- “Só um fix rápido” parece óbvio
- Já tentou vários patches
- O fix anterior não pegou
- Você não entende o problema de verdade

**Não pule quando:**
- Parece simples (bug simples também tem causa raiz)
- Tem pressa (método é mais rápido que thrash)
- Pediram “agora” (sistemático ainda é mais rápido)

## As quatro fases

Complete cada fase antes da próxima.

### Fase 1 — Investigação de causa raiz

**ANTES de qualquer fix:**

1. **Leia erros com cuidado**
   - Não ignore warnings
   - Stack completa: arquivos, linhas, códigos
   - Logs de CI / runtime — leia o trecho que falhou, não só o summary

2. **Reproduza de forma consistente**
   - Consegue disparar de forma confiável?
   - Quais são os passos exatos?
   - Acontece sempre?
   - Se não reproduz → mais dados, **não chute**

3. **Cheque mudanças recentes**
   - `git diff`, commits recentes
   - Deps novas, config, env
   - Diferenças staging vs local / worktree

4. **Evidência em sistemas multi-componente**

   Quando há várias camadas (CI → build, API → service → DB, front → BFF → Nest):

   **ANTES de propor fix, instrumente fronteiras:**
   ```
   Para CADA fronteira de componente:
     - Logar o que entra
     - Logar o que sai
     - Verificar env/config que propaga
     - Checar estado em cada camada

   Rode UMA vez para ver ONDE quebra
   ENTÃO analise a evidência
   ENTÃO investigue só o componente que falha
   ```

5. **Trace o fluxo de dados**

   Quando o erro está fundo na call stack:

   Veja `root-cause-tracing.md` neste diretório.

   **Versão rápida:**
   - Onde o valor ruim nasce?
   - Quem chamou com esse valor?
   - Suba até a origem
   - Corrija na **fonte**, não no sintoma

6. **Hipótese de causa (ainda Fase 1)**
   - 1–3 frases: “Acho que X porque Y (evidência Z)”
   - Sem evidência → continue investigando, não pule para Fase 4

### Fase 2 — Análise de padrão

**Ache o padrão antes de corrigir:**

1. **Exemplos que funcionam** no mesmo codebase
2. **Compare com referência** — se for um padrão, leia a implementação de referência **por completo** (não skim)
3. **Liste diferenças** working vs broken — todas, mesmo “isso não pode importar”
4. **Dependências** — config, env, assumptions, outros módulos

### Fase 3 — Hipótese e teste

**Método científico:**

1. **Uma hipótese só** — específica, escrita
2. **Teste mínimo** — menor mudança possível; uma variável por vez
3. **Verifique antes de continuar**
   - Funcionou? → Fase 4
   - Não? → **nova** hipótese (não empilhe patches)
4. **Quando não souber** — diga “não entendi X”; peça ajuda / pesquise; não finja

### Fase 4 — Implementação

**Fix da causa raiz, não do sintoma:**

1. **Crie caso que falha**
   - Repro mais simples possível
   - Teste automatizado preferível
   - Script one-off se não houver framework
   - **DEVE existir antes do fix**
   - Use `tdd-antes-de-codigo` para o teste vermelho certo

2. **Um único fix**
   - Só a causa identificada
   - Uma mudança por vez
   - Sem “já que estou aqui”
   - Sem refactor acoplado

3. **Verifique o fix**
   - O teste novo passa?
   - Suite relevante não quebrou?
   - O sintoma sumiu de verdade?
   - Antes de declarar resolvido → `verificar-antes-de-enviar`

4. **Se o fix não funcionou**
   - PARE
   - Conte quantos fixes tentou
   - Se &lt; 3: volte à Fase 1 com a nova informação
   - Se ≥ 3: **PARE** e questione a arquitetura (passo 5)
   - NÃO tente Fix #4 sem discutir arquitetura com o humano

5. **Se 3+ fixes falharam: questione a arquitetura**

   Sinais de problema estrutural:
   - Cada fix revela acoplamento/estado compartilhado noutro lugar
   - Fix exige “refactor enorme”
   - Cada fix cria sintoma novo

   **Discuta com o humano** antes de mais patches. Isso não é hipótese falha — pode ser arquitetura errada.

6. **Prevenir (se couber)**
   - Teste de regressão permanece
   - Nota curta na task se o bug era de processo (RF/escopo)
   - **Nunca** marcar task `completed` porque o bug “sumiu” — só `in_review` via `fechar-task`

## Sinais vermelhos — PARE e volte ao processo

Se pensar:
- “Fix rápido agora, investigo depois”
- “Muda X e vê se passa”
- “Vários patches de uma vez”
- “Pula o teste, verifico na mão”
- “Provavelmente é X”
- “Não entendi bem mas pode ser isso”
- “O padrão diz X mas eu adapto diferente”
- Listar fixes sem investigação
- Propor solução antes de traçar o fluxo de dados
- “Mais uma tentativa” (já tentou 2+)
- Cada fix revela problema noutro lugar

**Tudo isso = PARE. Volte à Fase 1.**

**Se 3+ fixes falharam:** questione arquitetura (Fase 4.5).

## Sinais do humano de que você está errando

| Fala do humano | O que fazer |
|----------------|-------------|
| “Isso não está acontecendo?” | Você assumiu sem verificar → Fase 1 |
| “Vai mostrar…?” | Faltou instrumentação / evidência |
| “Para de chutar” | Fix sem entender → Fase 1 |
| “Pensa fundo / ultra-think” | Questione fundamentos, não sintoma |
| “Estamos travados?” | Abordagem errada → Fase 1 / arquitetura |

## Racionalizações comuns

| Desculpa | Realidade |
|----------|-----------|
| “É simples, não precisa de processo” | Simples também tem causa. Processo é rápido. |
| “Emergência, sem tempo” | Sistemático é mais rápido que thrash. |
| “Tento esse fix e depois investigo” | O primeiro fix define o padrão. Faça certo. |
| “Escrevo o teste depois que confirmar” | Fix sem teste não gruda. Teste primeiro prova. |
| “Vários fixes de uma vez economizam” | Não isola o que funcionou. Cria bugs. |
| “Referência longa, adapto o padrão” | Entendimento parcial = bug garantido. |
| “Já vi o problema, vou corrigir” | Ver sintoma ≠ entender causa. |
| “Mais uma tentativa” (após 2 falhas) | 3+ = questione arquitetura. |
| “Marco completed, o bug sumiu” | **Proibido.** Só `in_review` + humano. |
| “Task Track sem MCP, corrijo pelo chat” | Contexto MCP primeiro (`implementar-task` / `setup`). |

## Referência rápida

| Fase | Atividades | Critério de sucesso |
|------|------------|---------------------|
| **1. Causa raiz** | Ler erros, reproduzir, mudanças, evidência | Entender O QUÊ e POR QUÊ |
| **2. Padrão** | Exemplos working, comparar | Diferenças claras |
| **3. Hipótese** | Teoria + teste mínimo | Confirmada ou nova hipótese |
| **4. Implementação** | Teste falha → fix → verificar | Bug resolvido, testes passam |

## Quando o processo revela “sem causa raiz”

Se for realmente ambiental, timing ou externo:

1. Você completou o processo
2. Documente o que investigou
3. Handling apropriado (retry, timeout, mensagem)
4. Monitoring/log para a próxima vez

**Mas:** 95% dos “sem causa raiz” são investigação incompleta.

## Técnicas de apoio

Neste diretório:

- **`root-cause-tracing.md`** — subir a call stack até o trigger original
- **`defense-in-depth.md`** — validação em várias camadas depois da causa
- **`condition-based-waiting.md`** — trocar `sleep`/timeouts arbitrários por espera de condição (flaky)

**Skills relacionadas (Contexto Certo):**
- `tdd-antes-de-codigo` — teste que falha (Fase 4.1)
- `verificar-antes-de-enviar` — evidência antes de “pronto”
- `fechar-task` — commit/push/`in_review` (nunca `completed`)
- `implementar-task` — contexto MCP da task

## Impacto real

- Abordagem sistemática: minutos a ~meia hora
- Chute e patch: horas de thrash
- Taxa de acerto na primeira: alta vs ~40%
- Bugs novos introduzidos: quase zero vs comum

## Nunca

- Empilhar patches sem entender
- Expandir escopo da task “já que está mexendo”
- Marcar task `completed` porque o sintoma sumiu
- Pular Fase 1 sob pressão
- Inventar causa sem reprodução/evidência
