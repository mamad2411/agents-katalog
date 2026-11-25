---
name: testar
description: "Use quando todas as ondas do GOAL.md foram construídas e coladas e é hora da etapa 8 do pipeline: o Agente de Testes e Qualidade roda os validadores, confere o contrato e monta o roteiro de testes no ambiente (negação por perfil e unidade, ciclo completo no dado). Aprovado, segue para a homologação; com falha, devolve a correção para o app ou para as automações. Não use antes do /pp:construir, nem para investigar um número que não bate (descreva ao orquestrador `power-platform`)."
user-invocable: true
disable-model-invocation: true
---

# /pp:testar — Agente de Testes e Qualidade

Etapa 8 do pipeline, bloco **4. Validação e entrega**. O agente `pp:agente-qa` prova o que dá para
provar sem ambiente e escreve o roteiro do que só o ambiente prova; o usuário roda esse roteiro.
A pergunta do desenho: **testes aprovados?**

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script de estado: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Modelos: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
O que é verde de verdade: `KIT/skills/power-platform/references/portao-final.md`.

## Antes de começar

1. `estado.py comecar testar`. Exit 1: mostre a saída e pare.
2. Confira no `GOAL.md` que nenhuma tarefa de construção está aberta. Se está, a etapa anterior não
   terminou: diga qual e aponte `/pp:construir`.

## Passos

1. **Agente.** `◆ Chamando o Agente de Testes e Qualidade...` e chame `pp:agente-qa` com `RAIZ`,
   `KIT` (o valor de `${CLAUDE_PLUGIN_ROOT}`) e o escopo (todas as ondas, ou só as correções desde o
   último `docs/qa/QA-*.md`). Modelo: `modelos.py de agente-qa` (linha vazia: não passe `model`).
2. **Reabra os achados mais fortes** antes de acreditar: rode de novo os validadores que o agente
   citou e confira 2 ou 3 achados com o comando que ele deu
   (`KIT/skills/power-platform/references/subagentes.md`). O que não se reproduz entra como "não
   verificado". Relatório sem a evidência pedida: revisão. Registre com
   `estado.py veredito testar --agente agente-qa --resultado <...> --motivo "..."`.
3. **Escreva** `docs/qa/QA-<AAAA-MM-DD>.md`: tabela `Critério | Comando | Saída | Passa? | Data`, os
   achados confirmados e o roteiro de testes no ambiente.
4. **Testes no ambiente** (checkpoint `Ação no ambiente`, 🔴). Passe o roteiro do agente, curto e
   numerado, para rodar no ambiente de desenvolvimento:
   - negação: usuário **sem** a permissão, usuário de **outra unidade** e usuário **com** permissão,
     em cada ação de escrita (o fluxo devolve `status = "error"` nos dois primeiros);
   - ciclo completo: cadastrar → consultar → alterar → conferir no dado (não só na tela);
   - volume: contador e galeria com mais de 2.000 linhas, se o PRD prevê.
   "Digite 'tudo passou' ou liste o que falhou (o passo e o que apareceu)."
5. **Testes aprovados?** Aprovados quando: nenhum achado crítico ou alto aberto **e** o roteiro do
   ambiente passou inteiro.

## Encerrar

- **Aprovados:** `estado.py concluir testar --nota "QA-<data>: <N> critérios ok"`. Próximo passo:
  homologação.
- **Falhou:** escreva cada falha em `docs/qa/correcoes.md` (`| # | Camada (app/flows) | Onde | O que
  falhou | Como reproduzir | Situação |`), classificando a camada:
  - tela, fórmula, navegação ou mensagem → `app`;
  - fluxo, autorização, procedure ou gravação → `flows`.
  Depois `estado.py reabrir construir --motivo "QA-<data>: <k> falhas" --argumento <app|flows>`. Se
  há falha nas duas camadas, omita `--argumento`: o `/pp:construir` chama os dois agentes. É a volta
  "Corrigir app / Corrigir automações" do desenho.
- Commit se `git_commit_por_etapa`: `pp(testar): QA-<data> <aprovado | k falhas>`.
- Resumo e o bloco "Próximo passo" que o script imprimiu.
