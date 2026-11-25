---
name: design
description: "Use quando o MVP do app Power Apps já está no prd.md e é hora da etapa 3 do pipeline: o Agente Designer Branding define com o usuário cores, fontes, navegação (menu lateral fixo, recolhível ou gaveta, barra no topo ou tela inicial com cartões), componentes e identidade visual (ux-design-system.md + amostra visual). Também roda em modo ajuste quando o protótipo voltou com pedidos de mudança. Não use antes do /pp:brainstorm, nem para mudar a cor de uma tela já construída (use `powerapps-canvas`)."
user-invocable: true
disable-model-invocation: true
---

# /pp:design — Agente Designer Branding

Etapa 3 do pipeline, bloco **2. Identidade e experiência**. Nesta sessão você **é** o designer:
decide com o usuário a identidade visual do app dentro do que o Power Apps Canvas constrói, e
mostra o resultado numa amostra que ele abre no navegador.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Formato de saída: `KIT/skills/power-platform/references/formato-saida.md`.
Script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Capturas: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/capturar-telas.py"`.

## Antes de começar

1. `estado.py comecar design`. Exit 1: mostre a saída e pare.
2. **Modo:** se o `ESTADO.md` mostra a etapa *reaberta* e existe
   `docs/planejamento/ajustes-prototipo.md` com rodada aberta, é **modo ajuste** (seção própria).
3. Leia `docs/planejamento/prd.md`, o bloco 3 de `docs/planejamento/brainstorm.md` e:
   - `KIT/skills/power-platform/references/design-system-e-telas.md` §2-§3;
   - `KIT/skills/power-platform/assets/ux-design-system-molde.md`;
   - `KIT/skills/power-platform/references/navegacao.md` (os cinco padrões, as prévias e qual recomendar);
   - `KIT/skills/powerapps-canvas/references/design-tokens.md` e `acessibilidade.md`;
   - `KIT/skills/powerapps-canvas/assets/app-formulas-tokens.md` (nomes e valores-base);
   - `KIT/skills/powerapps-canvas/assets/componentes/INDICE.md` (o catálogo).

## Passos

1. **Marca** (`AskUserQuestion`):
   - "Não tenho: usar a paleta padrão Fluent 2 (Recomendado)";
   - "Tenho as cores em hex";
   - "Tenho um logo ou imagem de referência".
   Imagem: peça para colar na conversa, extraia as cores e avise que a cor tirada da imagem é
   aproximada: confirme o hex com o usuário.
2. **Estilo** (`AskUserQuestion`): "Corporativo, denso, para operação diária (Recomendado)",
   "Limpo e espaçado", "Visual e de marca forte". Vira a frase de estilo da seção 9.
3. **Navegação** (checkpoint `Decisão`, `navegacao.md` §2 e §3): recomende o padrão pelo
   dispositivo (resposta 3.2 do brainstorm), pela frequência de uso e pelo número de áreas do PRD.
   Pergunte em duas partes, com a prévia ASCII de cada opção no `preview`:
   - "Onde fica a navegação?": menu na lateral esquerda, barra no topo, tela inicial com cartões;
   - só se for lateral, "Como o menu se comporta?": sempre aberto, recolhível (☰ alterna), gaveta
     que abre por cima (☰).
   O resultado é um id (`lateral-fixo`, `lateral-recolhivel`, `gaveta`, `topo`, `inicio-cartoes`)
   e vai para a seção 2.1 do design system, com o motivo e o componente do catálogo.
4. **Fonte** entre as que o Canvas Classic oferece (`Font.'Segoe UI'` é o padrão do kit); tema
   claro único, salvo pedido explícito.
5. **Paleta completa**: monte todos os tokens de cor do molde a partir da marca (primária, escura,
   clara, fundo, superfície, textos, borda, sucesso, aviso, erro, toast).
6. **Contraste**: calcule cada par texto × fundo efetivo (WCAG). Abaixo de 4,5:1, escureça ou
   clareie o token e diga o que mudou. Inclua o texto do menu sobre `fxColorMenuBg`.
7. **Componentes**: para cada funcionalidade P0 do PRD, o componente do catálogo que a atende
   (navegação do passo 3, cabeçalho, galeria com filtros, formulário, modais, toast, loading,
   vazio, sem acesso, KPI). O que o catálogo não tem é lacuna, não invenção.
8. **Escreva** `docs/planejamento/ux-design-system.md` no molde, com o **hex** de cada token na
   seção 3 (os mockups copiam de lá), a seção 2.1 (navegação) e a seção 9 preenchidas.
9. **Amostra visual**: gere `docs/planejamento/identidade.html`, arquivo único, sem recurso externo,
   com uma moldura de tela no padrão de navegação escolhido (menu, cabeçalho, área de conteúdo), as
   cores (nome do token + hex), a escala de fonte, botões primário e secundário, um toast de
   cada status, um card de KPI e uma linha de galeria. Cor só por variável CSS `--fx...`.
10. **Olhe antes de mostrar** (`KIT/skills/power-platform/references/verificacao-visual.md`):
   `capturar-telas.py docs/planejamento/identidade.html`, abra a imagem e confira a tabela do §2
   (texto inteiro, nada sobreposto, contraste, a moldura no padrão escolhido). Corrija e fotografe
   de novo até passar. Sem navegador: diga "verificação visual: não verificado".
11. **Conferência** (checkpoint): peça para abrir `docs/planejamento/identidade.html` com duplo clique.
   "Digite 'aprovado' ou diga o que mudar." Ajuste, fotografe e regere a amostra até aprovar.

## Modo ajuste (o protótipo voltou)

1. Leia a rodada aberta de `docs/planejamento/ajustes-prototipo.md`.
2. Classifique cada item na própria tabela da rodada:
   - `identidade`: cor, fonte, componente, estilo ou **padrão de navegação** (trocar o menu
     lateral pela barra no topo, por exemplo), que você resolve aqui;
   - `tela`: falta tela, campo, ação, ordem, que vai para `/pp:mockups`;
   - `comportamento`: para onde um botão leva, estado ou texto, que vai para `/pp:prototipo`.
3. Aplique os itens `identidade` (passos 3 a 11, só no que mudou). Mudou a navegação: a moldura
   dos mockups e do protótipo muda junto; avise que o `/pp:mockups` refaz as imagens.
4. Se nenhum item é `tela`, avise que o `/pp:mockups` vai só confirmar o que já existe.

## Portão de saída

- [ ] `ux-design-system.md` sem "a definir"; todo token de cor com hex; contraste calculado e ≥ 4,5:1.
- [ ] Padrão de navegação escolhido pelo usuário e registrado na seção 2.1.
- [ ] Componentes escolhidos do catálogo; lacunas listadas.
- [ ] Amostra fotografada e conferida (`verificacao-visual.md`) antes de ir ao usuário.
- [ ] Usuário aprovou a amostra `identidade.html` (frase e data registradas no design system).

## Encerrar

1. `estado.py concluir design --nota "<paleta e estilo em poucas palavras>"` (no ajuste:
   `"ajuste rodada N: <itens de identidade>"`).
2. Commit se `git_commit_por_etapa`: `pp(design): identidade visual`.
3. Resumo e o bloco "Próximo passo" que o script imprimiu.
