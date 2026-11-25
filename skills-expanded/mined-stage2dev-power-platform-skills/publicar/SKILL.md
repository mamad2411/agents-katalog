---
name: publicar
description: "Use quando a homologação do app Power Apps foi aprovada e é hora da etapa 10, a última do pipeline: checklist de go-live, documentação (manual do usuário por perfil, guia técnico) e a publicação em produção guiada passo a passo, com teste de fumaça. Não use antes do /pp:homologar aprovar, nem para mover uma correção pontual entre ambientes (descreva ao orquestrador `power-platform`)."
user-invocable: true
disable-model-invocation: true
---

# /pp:publicar — Publicação e documentação

Etapa 10 do pipeline, bloco **4. Validação e entrega**. Termina com o app em produção, documentado
para quem usa e para quem mantém.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script de estado: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Promoção: `KIT/skills/power-platform/references/alm-ambientes.md` §10 (procedimento) e §11 (literais).

## Antes de começar

1. `estado.py comecar publicar`. Exit 1: mostre a saída e pare.
2. Leia `prd.md`, `inventario-telas.md`, `arquitetura.md`, `GOAL.md` e o último `docs/qa/UAT-*.md`.
3. **Reaberta por uma mudança** (`MUD-<NNN>` no motivo): é uma versão nova. Checklist e documentos
   só no que a mudança alterou (o manual, se mudou o uso; o guia técnico, se mudou contrato ou
   banco); a tag sobe a versão (`v1.1.0`); a `MUD` vira "publicada".

## Passos

1. **Checklist de go-live** em `docs/entrega/GO-LIVE-CHECKLIST.md`, cada item com dono e situação:
   - versão da solução;
   - variáveis de ambiente de produção;
   - connection references e contas de serviço;
   - acesso dos usuários reais (grupos, perfis, flags; ninguém com permissão por omissão);
   - carga de dados, se houver;
   - plano de volta (versão anterior da solução, dado);
   - comunicação aos usuários e canal de suporte.
2. **Documentação** em `docs/entrega/`:
   - `manual-usuario.md`: um capítulo por perfil, o passo a passo de cada tarefa P0, o que cada
     mensagem de erro quer dizer e a quem pedir ajuda. Use a linguagem da tela, sem jargão técnico;
   - `guia-tecnico.md`: trilha de dados e ADRs, tabelas e procedures (do `NOMES-AS-BUILT`), cada
     fluxo com o contrato, onde fica o log, como promover uma correção, os validadores e o que cada
     um não cobre.
3. **Sem literal de ambiente:** `grep -rnE "dev[A-Z_]|[0-9a-f]{8}-[0-9a-f]{4}-" <pastas do config>`
   não acha servidor, tabela `dev*` nem GUID nos artefatos de entrega (`alm-ambientes.md` §11).
4. **Publicar** (checkpoint `Ação no ambiente`, 🔴), passo a passo de `alm-ambientes.md` §10: importar
   a solução gerenciada em produção, preencher variáveis, ligar conexões, compartilhar o app com os
   grupos de usuários, ligar os fluxos. "Digite 'feito' ou o erro."
5. **Teste de fumaça** (checkpoint `Conferência`): com um usuário real de cada perfil, abrir o app,
   consultar e fazer **uma** gravação de teste combinada; conferir o log do fluxo. "Digite 'passou'
   ou o que falhou." Falhou: volte ao passo 4 com o plano de volta à mão.
6. **Marco:** se `git_commit_por_etapa`, commit `pp(publicar): go-live` e tag `v1.0.0`.

## Portão de saída

- [ ] Checklist de go-live com todos os itens feitos ou com risco aceito (dono e data).
- [ ] Manual do usuário e guia técnico escritos.
- [ ] Publicado em produção e teste de fumaça passou.

## Encerrar

1. `estado.py concluir publicar --nota "go-live em <data>; fumaça ok"`.
2. Resumo: onde está o app, onde estão os documentos, quem dá suporte, e o bloco final que o script
   imprimiu (🎉 App publicado).
