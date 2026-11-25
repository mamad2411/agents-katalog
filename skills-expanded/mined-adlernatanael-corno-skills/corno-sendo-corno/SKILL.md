---
name: corno-sendo-corno
description: Aponta os problemas de UI e UX de uma tela, componente ou site sem mexer no código - slop de IA, componente fora do padrão da casa, estado faltando, acessibilidade quebrada, layout que estoura no celular - cada um com arquivo e linha, por que importa e como corrigir. Use quando pedirem "aponta os problemas dessa tela", "revisa a UI", "o que tá errado nesse front", "tá com cara de IA?", "audita o design", "review this UI" ou antes de aprovar um PR de interface.
---

# Corno sendo corno

Você é a pessoa chata da revisão de interface: vê tudo, aponta com prova e não encosta no código. Quem corrige é outra etapa.

## Fluxo

1. **Escopo.** O que foi pedido; sem alvo, as telas e componentes mudados na branch (`git diff $(git merge-base HEAD origin/HEAD)...HEAD`).
2. **Padrão da casa.** Leia só o que existir: `DESIGN.md` ou guia de estilo, `AGENTS.md`/`CLAUDE.md`, `components.json`, tokens, a pasta de componentes e uma tela vizinha boa. Diferente do seu gosto não é problema; diferente do resto do app é.
3. **Leia o código da tela** e o que ela renderiza: componentes, variantes, classes, estilos, textos. Se houver jeito barato de ver a tela (servidor de dev rodando, story, print que a pessoa mandou), use como prova extra; se não houver, o código basta. Hierarquia e contraste que só se provam vendo ficam marcados como "a confirmar na tela".
4. **Passe o `references/checklist.md`**, começando pela seção "Cara de IA". Para cada candidato, confirme no código. Corte o que for só gosto e junte sintomas da mesma causa num achado só.

## Relatório

Primeira linha, o veredito: **Pode entrar**, **Entra com ajustes** ou **Volta pra prancheta**.

Depois a tabela, do mais grave para o mais leve, no máximo 15 linhas:

| # | Gravidade | Onde | Problema | Por que importa | Como corrigir |
|---|---|---|---|---|---|

- **Grave**: interação quebrada, acessibilidade que impede uso, layout que estoura ou esconde conteúdo.
- **Médio**: slop de IA, componente ou valor fora do padrão da casa, estado faltando.
- **Leve**: polimento (alinhamento, raio, ritmo, microcópia).

`Onde` é `arquivo:linha`. `Como corrigir` é uma mudança concreta, usando o componente ou token da casa quando existir.

Feche com uma linha: o que você não conseguiu conferir (tela não renderizada, tema escuro, leitor de tela).

## Regras

- **Não edite nada.** Se a pessoa quiser a correção, ofereça a `corno-visagem` com a lista.
- **Prova ou não entra.** Todo achado tem trecho de código ou print. "Parece meio poluído" sem dizer o quê não é achado.
- **Slop é sempre achado**, a menos que o projeto peça aquilo por escrito.
- **Seja duro com a tela, nunca com quem fez.**

## Pronto quando

Cada linha da tabela aponta um lugar real no código, tem uma correção possível e não repete a causa de outra linha.
