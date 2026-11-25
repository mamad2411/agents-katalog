---
name: mudanca
description: "Use quando o app Power Apps já foi publicado pelo pipeline (ou já tem power-platform.config.json do kit) e o usuário traz uma lista de mudanças: corrigir, ajustar, acrescentar campo, tela ou regra. Escopa cada pedido, junta o contexto com agentes de pesquisa, escreve um spec por frente, manda os agentes de construção em paralelo, julga cada entrega (aceito, revisão, escalado), roda o QA da mudança e reabre a homologação. Não use com o pipeline no meio (as voltas do protótipo e dos testes cuidam disso), em app sem o kit (descreva ao orquestrador `power-platform`) nem para mudança que refaz o MVP (reabra o pipeline no brainstorm)."
argument-hint: "[a lista de mudanças, do jeito que vier]"
user-invocable: true
disable-model-invocation: true
---

# /pp:mudanca — Mudanças num app publicado

Fora das 10 etapas: roda quando o app já está no ar e chega uma lista ("arruma isso, muda aquilo,
falta um campo"). É o ciclo cabeça e mão aplicado a uma lista: você escopa, junta o contexto,
escreve um spec por frente, os agentes fazem em paralelo, você julga, e o usuário só vê o que passou.
**Você não escreve tela, fluxo nem procedure**: julga e decide (`subagentes.md`).

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script de estado: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Modelos: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
Julgamento: `KIT/skills/power-platform/references/subagentes.md`. Molde:
`KIT/skills/power-platform/assets/mudanca-molde.md`.

## Antes de começar

1. Banner `PP ► MUDANÇA` (`formato-saida.md` §2) e uma frase do que vai acontecer.
2. Onde o projeto está:
   - `estado.py mostrar`. Alguma etapa antes de **Publicação** não está feita: o pipeline está no
     meio; mostre o bloco "Próximo passo" e pare (ajuste e correção têm as voltas deles);
   - sem `ESTADO.md` e com `power-platform.config.json`: app adotado pelo kit; siga, sem os comandos
     de estado;
   - sem os dois: pare e diga para descrever o pedido ao orquestrador `power-platform`.
3. Leia `power-platform.config.json` (trilha, pastas, `nomes_as_built`), `docs/planejamento/prd.md`
   (perfis, regras `RN-xx`), `arquitetura.md` (contrato), `ux-design-system.md` e os
   `docs/mudancas/MUD-*.md` anteriores (o próximo número e o que já foi pedido).

## Passos

1. **A lista.** `$ARGUMENTS` ou pergunte: "O que precisa mudar? Lista bagunçada, prints e mensagens
   de usuários servem." Crie `docs/mudancas/MUD-<NNN>.md` no molde, com a lista como veio.
2. **Escopo** (você). Cada pedido reescrito em uma linha, para pegar mal-entendido barato, com a
   camada (tela, fluxo, procedure ou tabela, identidade visual) e o tamanho:
   - **pequeno ou médio:** segue nesta mudança;
   - **grande** (perfil novo, entidade nova, troca de trilha, refaz o MVP): fica fora. Recomende
     reabrir o pipeline no brainstorm (`estado.py reabrir brainstorm --motivo "..."`); quem decide é
     o usuário.
   Pedido que fere uma regra `RN-xx` ou o contrato: vira pergunta, não spec.
3. **Perguntas numa rodada só** (checkpoint `Decisão`): a tabela do escopo e tudo o que falta saber
   (ambíguo, conflito com regra, quem aprova), juntos: até 4 perguntas fechadas numa chamada do
   `AskUserQuestion`, mais uma aberta se precisar. "Corrija o que não estiver certo."
4. **Contexto** (você não faz a leitura ampla). Um `pp:agente-pesquisa` por área tocada (telas,
   fluxos, banco), na **mesma mensagem**, com `ONDE: projeto`, `PARA QUE: escrever os specs da
   mudança` e a pergunta: quais arquivos a mudança
   toca, as convenções deles, as pegadinhas, e **o que mais depende disso** (outra tela que usa a
   coluna, outro fluxo que chama a procedure). Modelo: `modelos.py de agente-pesquisa`. Julgue.
5. **Specs** na seção 3 do MUD, um por frente: o agente, os **arquivos exatos**, o que muda
   (antes → depois), "pronto quando" com o comando que prova, e o que fica de fora. Duas frentes no
   mesmo arquivo: uma depois da outra. Contrato app↔flow que muda: atualize `arquitetura.md` antes
   (parâmetro novo sempre no fim; tela e fluxo mudam na mesma mudança).
6. **Execução em paralelo**, na mesma mensagem, no máximo 5 agentes: `pp:agente-canvas`,
   `pp:agente-automate` ou `pp:agente-sql`, cada um com `RAIZ`, `KIT` e `MUDANCA` (o caminho do MUD
   e a seção do seu spec). Modelo: `modelos.py de <agente>`. Mudança de identidade (cor, fonte,
   navegação): o spec inclui o `ux-design-system.md` e os tokens do `App.Formulas`.
7. **Julgue cada entrega** (`subagentes.md`, "Julgar a entrega"): validador da camada em
   `0 erro(s)`, spec × entrega, alertas. Veredito na seção 4 do MUD; revisão com o pedido mais
   apertado, no máximo duas; a terceira é escalada.
8. **QA da mudança:** `pp:agente-qa` com o escopo = os arquivos mudados e o que depende deles (do
   passo 4). Modelo: `modelos.py de agente-qa`. Reabra os achados mais fortes antes de acreditar.
   Achado alto: revisão para o agente da camada.
9. **Colar no ambiente de desenvolvimento** (checkpoint `Ação no ambiente`, 🔴): fluxos primeiro,
   tokens se mudaram, depois as telas; procedure vai ao DBA. Erro: volta ao agente da camada.
10. **Teste no ambiente** (🔴): o roteiro do QA para os pedidos; se mexeu em permissão, a negação por
    perfil e por unidade. "Digite 'tudo passou' ou o que falhou."
11. **Síntese** na seção 6 do MUD e no chat (resumo de `formato-saida.md` §1): entregue,
    verificado, revisado, com você, fora.

## Portão de saída

- [ ] Todo pedido com destino: aceito, escalado ao usuário ou fora (grande), na seção 2 do MUD.
- [ ] Validadores das camadas tocadas em `0 erro(s)`; QA da mudança sem achado alto aberto.
- [ ] Colado e testado em desenvolvimento, ou a pendência escrita no MUD.

## Encerrar

- **Com `ESTADO.md` e algo colado no ambiente:** `estado.py reabrir homologar --motivo "MUD-<NNN>: <k> pedidos"`.
  Homologação e publicação reabrem; o próximo passo é o `/pp:homologar`, que cobre os pedidos da
  mudança e sai para uma versão nova em produção.
- **Sem `ESTADO.md`:** a promoção segue `KIT/skills/power-platform/references/alm-ambientes.md` §10.
- Commit se `git_commit_por_etapa`: `pp(mudanca): MUD-<NNN> <resumo>`.
- O resumo e o bloco "Próximo passo" que o script imprimiu (com `ESTADO.md`).
