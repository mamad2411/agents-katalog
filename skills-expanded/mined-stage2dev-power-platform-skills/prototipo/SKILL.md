---
name: prototipo
description: "Use quando o inventário de telas e os mockups do app Power Apps estão prontos e é hora da etapa 5 do pipeline: o Agente Gerador de Mockup HTML monta um protótipo navegável (um index.html que abre offline) em cima dos mockups, e o usuário aprova ou pede ajuste. Aprovado, o pipeline segue para a arquitetura; com ajuste, volta para o /pp:design. Não use antes do /pp:mockups, nem para construir a tela real (use `/pp:construir`)."
user-invocable: true
disable-model-invocation: true
---

# /pp:prototipo — Agente Gerador de Mockup HTML

Etapa 5 do pipeline, bloco **2. Identidade e experiência**. O agente `pp:agente-prototipo` monta o
protótipo navegável a partir dos mockups aprovados, do catálogo de componentes e dos tokens. Você
confere e leva ao usuário a pergunta do desenho: **protótipo aprovado?**

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script de estado: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Modelos: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
Verificador: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/verificar-prototipo.py"`.
Capturas: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/capturar-telas.py"`.

## Antes de começar

1. `estado.py comecar prototipo`. Exit 1: mostre a saída e pare.
2. Confira que existem `docs/planejamento/inventario-telas.md`, `mockups/mockups.json` e
   `ux-design-system.md`. PNGs são desejáveis, não obrigatórios (sem imagem o verificador avisa V013).
3. **Modo:** *ajuste* se a etapa está *reaberta* e a rodada aberta de `ajustes-prototipo.md` tem
   itens `comportamento` ou `tela`; senão *novo*.

## Passos

1. **Agente.** Mostre `◆ Chamando o Agente Gerador de Mockup HTML...` e chame `pp:agente-prototipo`
   com `RAIZ`, `KIT` (o valor de `${CLAUDE_PLUGIN_ROOT}`) e `MODO` (no ajuste, os itens da rodada).
   Modelo: `modelos.py de agente-prototipo` (linha vazia: não passe `model`).
2. **Julgue a entrega** (`KIT/skills/power-platform/references/subagentes.md`, "Julgar a entrega"):
   `verificar-prototipo.py docs/planejamento/prototipo --mockups docs/planejamento/mockups/mockups.json`
   precisa terminar em `0 erro(s)`, e toda tela do inventário tem a sua `<section data-tela>`.
   Depois **olhe** (`KIT/skills/power-platform/references/verificacao-visual.md`):
   `capturar-telas.py docs/planejamento/prototipo/index.html` e abra cada imagem; confira a
   tabela do §2. Para perfis diferentes, `--perfil <chave>` nas telas que mudam por perfil.
   Erro, tela faltando ou defeito visual: revisão, com a saída ou a imagem e a região. Registre com
   `estado.py veredito prototipo --agente agente-prototipo --resultado <...> --motivo "..."`.
3. **Abra para o usuário.** Ofereça abrir o arquivo (`start "" "docs/planejamento/prototipo/index.html"`
   no Windows, `open` no macOS, `xdg-open` no Linux) ou o duplo clique. Explique em 3 linhas:
   - o seletor de perfil no topo mostra o app como cada perfil vê;
   - o roteiro guia o passeio pelas telas;
   - "Comparar com o mockup" abre a imagem de origem;
   - o seletor "Navegação" troca o menu ao vivo (o marcado "(design)" é o escolhido); preferir
     outro padrão é um item de ajuste.
4. **Protótipo aprovado?** (checkpoint `Conferência`, `AskUserQuestion`):
   - "Aprovado: seguir para a arquitetura";
   - "Precisa de ajustes".
5. **Aprovado:** pergunte quem aprovou (nome ou papel) e grave em `inventario-telas.md`:
   "Protótipo aprovado por <quem> em <data>".
6. **Ajustes:** colete um item por vez (qual tela, o que mudar, por quê) até o usuário dizer que
   acabou. Grave em `docs/planejamento/ajustes-prototipo.md` uma nova seção `## Rodada N — <data>`
   com a tabela `| # | Tela | Pedido | Classe | Situação |` (classe em branco: o design classifica).
   Na rodada seguinte, marque como `feito` os itens da anterior que o protótipo novo resolveu.

## Portão de saída

- [ ] `verificar-prototipo.py` com `0 erro(s)` (última linha no resumo; avisos V013 explicados).
- [ ] Toda tela do inventário tem `<section data-tela>` com `data-mockups` de origem.
- [ ] Telas fotografadas e olhadas (`verificacao-visual.md`), ou "não verificado" se não há navegador.
- [ ] Aprovação registrada no inventário **ou** rodada de ajustes registrada.

## Encerrar

- **Aprovado:** `estado.py concluir prototipo --nota "aprovado por <quem>"`. O próximo passo é a
  arquitetura.
- **Ajustes:** `estado.py reabrir design --motivo "ajustes do protótipo, rodada N (<k> itens)"`. O
  script reabre design, mockups e protótipo e aponta `/pp:design`: é a volta "Ajustar" do desenho.
- Commit se `git_commit_por_etapa`: `pp(prototipo): <aprovado | ajustes rodada N>`.
- Resumo e o bloco "Próximo passo" que o script imprimiu.
