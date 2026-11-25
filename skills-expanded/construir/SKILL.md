---
name: construir
description: "Use quando a arquitetura do app Power Apps está pronta e o ambiente tem o NOMES-AS-BUILT preenchido, para a etapa 7 do pipeline: constrói a próxima onda do GOAL.md com o Agente Power Apps Canvas (telas, componentes, Power Fx) e o Agente Power Automate (fluxos, aprovações, notificações, erros) em paralelo, confere a integração app↔flow e guia a colagem no ambiente. Com `app` ou `flows`, roda só um agente (correção vinda dos testes). Não use antes do /pp:arquitetura, nem para um ajuste pontual fora do pipeline (use `powerapps-canvas` ou `power-automate`)."
argument-hint: "[app|flows]"
user-invocable: true
disable-model-invocation: true
---

# /pp:construir — Agentes Power Apps Canvas e Power Automate

Etapa 7 do pipeline, bloco **3. Construção na Power Platform**. Cada sessão constrói **uma onda**
do `GOAL.md`: os dois agentes trabalham em paralelo, você confere a integração e o usuário cola no
ambiente. A etapa só fecha quando a última onda fecha.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script de estado: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Modelos: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
Fila e evidência: `KIT/skills/power-platform/references/modo-goal-fila.md`.

## Antes de começar

1. `estado.py comecar construir`. Exit 1: mostre a saída e pare.
2. **Quem trabalha:** `$ARGUMENTS` = `app` (só Canvas), `flows` (só Power Automate) ou vazio (os dois).
3. **Portão do ambiente.** Leia `power-platform.config.json` (`nomes_as_built`) e abra o
   `NOMES-AS-BUILT`. Ausente, vazio ou sem as tabelas que a onda usa: checkpoint `Ação no ambiente`
   com a onda 0 do `GOAL.md` (o que criar, quem cria, como capturar os nomes) e **pare**. Escrever
   tela sobre nome chutado é a causa nº 1 de retrabalho.
4. **O que construir:**
   - etapa *reaberta* com `docs/qa/correcoes.md`: só os itens abertos da camada pedida (modo correção);
   - senão, a **primeira onda** do `GOAL.md` com tarefa 🟢 não feita e onda anterior com portão fechado.
   Mostre a onda: tarefas, telas e fluxos.
5. **Contrato fechado?** Cada fluxo da onda tem em `arquitetura.md` os parâmetros (posicionais,
   texto) e o retorno `{status, description, id, url}`. Faltou: escreva agora, antes dos agentes.

## Passos

1. **Divida a onda** pelos arquivos (coluna Arquivos do `GOAL.md`), sem dois agentes no mesmo
   arquivo:
   - telas em grupos de até 3, um `pp:agente-canvas` por grupo. Os tokens (`App.Formulas`,
     `App.OnStart`, só na primeira onda) são de um agente só, o que recebe `TOKENS: sim`;
   - fluxos em grupos de até 3, um `pp:agente-automate` por grupo;
   - correção: itens `app` para o Canvas; itens `flows` de fluxo para o Automate e de procedure
     para o `pp:agente-sql` (`CORRECOES`);
   - no máximo 5 agentes por mensagem; o que sobrar vai numa segunda leva, depois do julgamento
     da primeira. Onda pequena (até 3 telas e 3 fluxos): um de cada.
2. **Agentes em paralelo**, na **mesma mensagem**:
   ```
   ◆ Chamando 3 agentes em paralelo...
     → Agente Power Apps Canvas #1: Inicio, Pedidos, Detalhe
     → Agente Power Apps Canvas #2: Cadastro, Relatório
     → Agente Power Automate: fluxos da onda <n>
   ```
   - `pp:agente-canvas` com `RAIZ`, `KIT` (o valor de `${CLAUDE_PLUGIN_ROOT}`), `TELAS` (as tarefas
     de tela do grupo) e `TOKENS` (sim ou não), ou `CORRECOES` (itens `app`);
   - `pp:agente-automate` com `RAIZ`, `KIT`, `FLUXOS` (as tarefas de fluxo do grupo) ou
     `CORRECOES` (itens `flows` de fluxo);
   - `pp:agente-sql` com `RAIZ`, `KIT` e `CORRECOES` (itens `flows` de procedure), só em correção.
   O modelo de cada um: `modelos.py de <agente>` (linha vazia: não passe `model`).
3. **Julgue as entregas e a integração app ↔ automações** (você mesmo, não um agente;
   `KIT/skills/power-platform/references/subagentes.md`, "Julgar a entrega"):
   - `python "${CLAUDE_PLUGIN_ROOT}/skills/powerapps-canvas/scripts/validar-telas.py"` e
     `python "${CLAUDE_PLUGIN_ROOT}/skills/power-automate/scripts/verificar-fluxo.py"`, da raiz:
     `0 erro(s)` e arquivos lidos > 0 (correção de procedure: também
     `python "${CLAUDE_PLUGIN_ROOT}/skills/sql-procedures/scripts/lint-procedure.py"`);
   - cada `.Run(` nas telas tem o número e a ordem de parâmetros do contrato
     (`grep -n "\.Run(" <pasta-telas>`);
   - cada tela trata o retorno: `.Run()` dentro de `IfError`, sucesso = `status <> "error"`, toast
     com `description`, `Refresh` depois de gravar;
   - nomes de tabela e coluna das telas e dos fluxos existem no `NOMES-AS-BUILT`
     (`grep -n "<nome>" <NOMES-AS-BUILT>`).
   O que falhar volta ao agente da camada como revisão (o item, o arquivo, a saída). Um veredito
   por agente (`--agente agente-canvas#1`, `agente-automate`...):
   `estado.py veredito construir --agente <nome> --resultado <...>`.
4. **Colar no ambiente** (checkpoint `Ação no ambiente`, 🔴). Junte as instruções dos dois agentes
   num passo a passo só, nesta ordem:
   1. fluxos primeiro: criar o gatilho à mão com os parâmetros na ordem, colar o escopo, religar as
      conexões, salvar e testar com o dado de teste;
   2. tokens `fx*` no `App.Formulas` (só na primeira onda);
   3. telas: selecionar a tela, **Colar código**, adicionar o fluxo ao app, rodar.
   "Digite 'feito' ou cole a mensagem de erro."
5. **Erro na colagem:** diagnostique com a skill da camada (`powerapps-canvas` ou `power-automate`) e
   devolva ao agente da camada como revisão, com a mensagem exata do Studio ou do designer e a
   linha do arquivo; você não edita a tela nem o fluxo. Mensagem que a skill da camada não
   explica: antes, `pp:agente-pesquisa` com a mensagem exata (`ONDE: os dois`, `PARA QUE: corrigir
   a colagem`; modelo:
   `modelos.py de agente-pesquisa`), e os achados vão junto na revisão. Depois repita o passo 4. Duas falhas pela
   mesma causa: escalado (pare, registre no `GOAL.md` e diga ao usuário o que foi tentado).
6. **Atualize a fila:** cada tarefa da onda vira ✅ com evidência (comando + última linha do
   validador + "colado em <data>"). Correção: marque o item como `feito` em `docs/qa/correcoes.md`.

## Portão de saída da onda

- [ ] Validadores das duas camadas com `0 erro(s)`, arquivos lidos > 0.
- [ ] Contrato conferido: parâmetros, retorno e nomes reais.
- [ ] Usuário colou e testou sem erro; evidência na coluna do `GOAL.md`.

## Encerrar

- **Ainda há onda pela frente:** não conclua a etapa. Mostre o progresso da fila (ondas feitas /
  total) e rode `estado.py proximo`: ele aponta `/pp:construir` de novo, numa sessão nova.
- **Última onda ou correção terminada:** `estado.py concluir construir --nota "<N> ondas; <telas> telas, <fluxos> fluxos"`.
- Commit se `git_commit_por_etapa`: `pp(construir): onda <n>` (ou `correções <app|flows>`).
- Resumo e o bloco "Próximo passo" que o script imprimiu.
