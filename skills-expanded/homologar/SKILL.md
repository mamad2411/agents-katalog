---
name: homologar
description: "Use quando os testes do app Power Apps foram aprovados e é hora da etapa 9 do pipeline: levar o app ao ambiente de homologação, gerar o roteiro de UAT por perfil e registrar o aceite dos usuários reais (quem e quando). Reprovado, devolve a correção para a construção. Não use antes do /pp:testar aprovar, nem para promover para produção (use `/pp:publicar`)."
user-invocable: true
disable-model-invocation: true
---

# /pp:homologar — Homologação com o usuário

Etapa 9 do pipeline, bloco **4. Validação e entrega**. Quem testa agora são os **usuários reais**,
com dado parecido com o real, num ambiente que não é o de desenvolvimento. Você prepara o roteiro e
registra o aceite; o usuário conduz a sessão com as pessoas.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script de estado: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Promoção entre ambientes: `KIT/skills/power-platform/references/alm-ambientes.md` §2-§5 e §10.

## Antes de começar

1. `estado.py comecar homologar`. Exit 1: mostre a saída e pare.
2. Leia `docs/planejamento/prd.md` (perfis, requisitos P0), o último `docs/qa/QA-*.md` e a seção ALM
   de `arquitetura.md`.
3. **Reaberta por uma mudança** (o motivo no `ESTADO.md` cita `MUD-<NNN>`): leia o
   `docs/mudancas/MUD-<NNN>.md`. O UAT cobre os pedidos da mudança (seção 2) mais um ciclo curto
   do requisito P0 principal, para pegar regressão; não refaz o roteiro inteiro.

## Passos

1. **Onde homologar** (`AskUserQuestion`):
   - "Ambiente de homologação (HML) (Recomendado)";
   - "Não temos HML: homologar em DEV".
   A segunda vira risco aceito em `docs/qa/UAT-<data>.md`, com quem aceitou.
2. **Levar o app para HML** (checkpoint `Ação no ambiente`, 🔴), passo a passo de `alm-ambientes.md`
   §10: exportar a solução gerenciada de DEV, importar em HML, preencher as variáveis de ambiente,
   ligar as connection references, dar acesso aos usuários de teste. "Digite 'feito' ou o erro."
3. **Roteiro de UAT** em `docs/qa/UAT-<AAAA-MM-DD>.md`:
   - um bloco por perfil;
   - um cenário por requisito P0: passos curtos e o resultado esperado;
   - a massa de dados e os usuários de teste (um por perfil, um de outra unidade);
   - espaço para `passou / falhou / observação` e para a assinatura (nome ou papel, data).
4. **Sessão com os usuários** (checkpoint `Ação no ambiente`, 🔴): o usuário conduz o UAT com as
   pessoas e volta com o roteiro preenchido. `AskUserQuestion`:
   - "Aprovado";
   - "Aprovado com ressalvas que não bloqueiam";
   - "Reprovado".
5. **Registre** no `UAT-<data>.md` quem aprovou e quando. Ressalvas viram tarefas ⬜ numa seção
   "Depois do go-live" do `GOAL.md`.

## Encerrar

- **Aprovado (com ou sem ressalvas):** `estado.py concluir homologar --nota "aceite de <quem> em <data>"`.
- **Reprovado:** cada problema em `docs/qa/correcoes.md` com a camada (`app` ou `flows`), depois
  `estado.py reabrir construir --motivo "UAT-<data>: <k> problemas" [--argumento app|flows]`.
  Construção, testes e homologação reabrem juntos.
- Commit se `git_commit_por_etapa`: `pp(homologar): UAT-<data> <aprovado | reprovado>`.
- Resumo e o bloco "Próximo passo" que o script imprimiu.
