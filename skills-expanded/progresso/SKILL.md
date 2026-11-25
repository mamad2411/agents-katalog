---
name: progresso
description: "Use quando quiser saber onde um projeto Power Apps do kit está e qual comando rodar agora: mostra o painel do ESTADO.md (etapas feitas, em andamento e pendentes), a fila de construção, as pendências com prazo vencido e o próximo passo. Também explica o pipeline para quem ainda não começou. Não use para executar uma etapa (rode o comando que ele indicar)."
user-invocable: true
disable-model-invocation: true
---

# /pp:progresso — Orquestrador: coordena e acompanha

Mostra onde o projeto está e devolve o próximo comando. Só lê: não muda nenhum arquivo.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script de estado: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.

## Passos

1. `estado.py mostrar`.
   - **Exit 2 (não há `ESTADO.md`):** explique o pipeline em até 6 linhas, a partir da tabela §2 de
     `KIT/skills/power-platform/references/pipeline.md` (ideia → definição → identidade → construção
     → entrega, um comando por etapa, uma sessão nova por etapa) e termine com o bloco "Próximo
     passo" apontando `/pp:novo`. Se a pasta já tem um app (telas, fluxos), diga que o pipeline é
     para app novo e que, para app existente, basta descrever o problema: o orquestrador
     `power-platform` escolhe o caminho.
   - **Exit 0:** mostre a saída como veio.
2. **Fila de construção** (só se existe `GOAL.md`): por onda, tarefas ✅ / total e as 🔴 esperando o
   humano, com o que cada uma pede.
3. **Pendências** (`D-xx` no `prd.md` e no `GOAL.md`): as abertas, com dono e data-limite; destaque
   as vencidas com ⚠.
4. **Inconsistência** entre o `ESTADO.md` e o disco (etapa concluída sem o arquivo que ela entrega,
   ex.: design concluído sem `ux-design-system.md`): aponte com ⚠ e diga qual etapa rodar de novo.

## Encerrar

O bloco "Próximo passo" exatamente como o `estado.py` imprimiu. Nada de executar a etapa nesta
sessão: o usuário abre uma sessão nova e roda o comando.
