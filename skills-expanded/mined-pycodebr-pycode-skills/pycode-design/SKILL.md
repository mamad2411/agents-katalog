---
name: pycode-design
description: 'Use quando o pedido envolver escolher, aplicar, criar ou validar um estilo visual (design system, tokens, paleta, tipografia, DESIGN.md, design tokens, theme) para aulas, apresentações, páginas, sites ou carrosséis; quando a pessoa pedir "um design diferente", "um estilo", "uma identidade visual" ou trouxer uma referência para copiar o visual; ou quando quiser estudar galerias de referência de design. Entrega 12 estilos prontos com tokens, DESIGN.md e prévia, comandos para listar, validar, exportar e criar estilos, e acervos externos de estudo baixados na máquina.'
license: MIT
metadata:
  version: 1.0.0
  author: PycodeBR (Felipe Azambuja)
---

# pycode-design

Biblioteca de estilos visuais e de referências de design. Cada estilo tem um conceito próprio, objetos que dão identidade e regras de movimento, e todos seguem o mesmo contrato de variáveis CSS. Por isso as skills `pycode-aulas`, `pycode-paginas` e `pycode-carrosseis` aceitam qualquer um deles com `--style <slug>`.

## Pré-requisito

Confira se o comando existe antes de tudo:

```bash
command -v pycode || ls ~/.pycode-skills/bin/pycode
```

Se nenhum existir, instale com `curl -fsSL https://raw.githubusercontent.com/pycodebr/pycode-skills/main/install.sh | bash` e rode `pycode doctor`. Use sempre `pycode <grupo> <comando>`; nunca chame os scripts da skill pelo caminho.

## Quando usar

- Escolher o visual de uma aula, página, site ou carrossel.
- Aplicar um estilo pronto a um artefato que você está construindo à mão.
- Criar um estilo novo a partir de uma referência da pessoa (site, print, marca).
- Validar tokens, contraste e prévia de um estilo.
- Estudar galerias externas de design para ter ideias de composição e movimento.

Quando não usar: para gerar o artefato em si, use a skill do formato (`pycode-aulas`, `pycode-paginas`, `pycode-carrosseis`), que chama esta biblioteca. Para ilustrações e fotos, use o gerador de imagens do seu agente; esta skill trata de HTML, CSS e SVG.

## Os estilos

| slug | modo | conceito | combina com |
|---|---|---|---|
| `orbital` | escuro | marinho, dourado e ciano com objetos de papel: emblema em órbita, calendário, ingresso, acervo | inscrição, convite, programa de aulas |
| `python-noturno` | escuro | azul e amarelo do Python, textura de código, cartas colecionáveis, numerais | carrossel técnico, aula de Python |
| `caderno` | claro | documento de estudo com blocos, um azul de ação e adesivos | apostila, guia, painel |
| `noir-champanhe` | escuro | trailer de cinema: faixas panorâmicas, feixe, letreiro largo, créditos | abertura, anúncio, convite |
| `planta-azul` | escuro | planta de arquiteto: salas, portas, cotas, carimbo e selo | arquitetura, permissões, fluxos |
| `lousa` | escuro | lousa de giz com diagramas desenhados ao vivo | aula conceitual, comparação |
| `fliperama` | escuro | jogo 16-bit: diálogo, HP e XP, inventário, sprites | trilha para iniciantes, desafios |
| `terminal` | escuro | editor de código: abas, erro sublinhado, terminal, diff | tutorial, depuração, live coding |
| `revista` | claro | editorial impresso: serifa, colunas, capitular, índice | ensaio, newsletter, estudo de caso |
| `metro` | claro | sinalização de metrô: estações, baldeações, "você está aqui" | roadmap, trilha, onboarding |
| `sala-de-controle` | escuro | painel de instrumentos: mostrador, LEDs, alerta, osciloscópio | métricas, operação, segurança |
| `colagem` | claro | recortes de papel, fita, carimbos, polaroides, letras recortadas | bastidores, diário, comunidade |

A tabela completa de pedido para estilo está em `references/escolher-estilo.md`.

## Fluxo de trabalho

1. **Entenda o pedido e a superfície.** Em uma frase: o que é, para quem, e se a tela convence, ensina, acompanha ou compara. Se a pessoa trouxe uma referência visual, ela vence a tabela (vá para o passo 8).
2. **Escolha o estilo.**
   ```bash
   pycode styles list                  # todos
   pycode styles list --for carousel   # filtrados por formato
   ```
3. **Leia o DESIGN.md inteiro do estilo escolhido.** Ele diz o papel de cada cor, a escala tipográfica, os objetos (com como construir cada um), o movimento e o que evitar.
   ```bash
   pycode styles show lousa
   ```
4. **Veja a prévia funcionando** (paleta, tipografia, objetos animados, página, slide 16:9 e slide 4:5):
   ```bash
   pycode styles preview --style lousa --out ./previa-estilo
   pycode serve ./previa-estilo
   ```
5. **Construa com o contrato.** Se uma skill de formato vai gerar o projeto, passe `--style <slug>`. Se você está montando à mão, copie os tokens e as fontes:
   ```bash
   pycode styles tokens lousa --format css --out projeto/css/tokens.css
   ```
   e use só as variáveis do contrato para cor, tipografia, raio e sombra (lista em `references/contrato-tokens.md`). As fontes entram com `vendor.copy_fonts` (as skills de formato já fazem isso); nada de CDN.
6. **Dê a cada seção um objeto do estilo.** Ingresso para encontro ao vivo, planta para arquitetura, mostrador para métrica. Uma grade de cartões iguais não é design. Trechos prontos em `references/objetos.md`.
7. **Anime com disciplina.** Só `transform`, `opacity` e traço de SVG; loops pausados fora da tela e com a aba oculta; `prefers-reduced-motion` respeitado; conteúdo legível sem JavaScript. Detalhes em `references/movimento.md`.
8. **Para um estilo novo**, siga `references/criar-estilo.md`:
   ```bash
   pycode shot https://referencia.exemplo --sizes 1440x900,390x844 --full --out ref
   pycode styles new estudio-coral --from revista
   # edite tokens.css, DESIGN.md e preview.html em ~/.pycode-skills/styles-user/estudio-coral/
   pycode styles check estudio-coral
   ```
9. **Valide e revise por visão.**
   ```bash
   pycode styles check <slug>                      # fail-closed: tokens, contraste, fontes, DESIGN.md, texto, prévia
   pycode shot <artefato> --sizes 1440x900,390x844 --full --audit --out capturas
   pycode text <arquivos .md e .html>
   ```
   Abra as capturas e procure texto cortado, peça cobrindo texto, objeto que virou miniatura no celular, monotonia entre seções e contraste fraco. Capturas de página inteira só mostram as entradas depois de rolar; use `--reduced-motion` para ver o estado final.

## Referências externas

```bash
pycode refs list                  # catálogo com licença e status
pycode refs fetch all             # baixa para ~/.pycode-skills/references (cerca de 55 MB no total)
pycode refs search dashboard      # busca por nome e prompt (os prompts são em inglês)
pycode refs open fable-5.2/002    # caminhos do HTML e do prompt
```

Três dos quatro acervos não têm licença: servem para estudo local. Não copie código, não publique derivados diretos e não redistribua. Como estudar sem copiar está em `references/acervos.md`.

## Regras de qualidade

- Conceito visual próprio e objetos ligados ao assunto. Nada de grade de cartões iguais, fundo liso só com texto, degradê roxo e azul genérico ou emoji como ícone.
- Sem rótulo decorativo em caixa alta acima de cada título de seção.
- Cada cor tem um papel fixo; a cor de destaque aparece em poucos pontos por tela.
- Contraste de 4,5:1 para texto (3:1 para texto grande e bordas de controle).
- Responsivo de verdade em 320, 390, 820 e 1440 px, sem rolagem horizontal; no celular os objetos se reorganizam.
- Fontes e bibliotecas dentro do projeto, vindas do `vendor`.
- Texto em PT-BR com acentos, frases completas e sem fórmulas de anúncio (travessão como pontuação, reticências de suspense, "não é X, é Y", clichês). `pycode text` sem erros nem avisos.
- Conteúdo de exemplo fictício e neutro; marca do usuário vem de `pycode brand`.

## Critérios de conclusão

Só diga que terminou quando:

- o estilo escolhido (ou criado) passou em `pycode styles check <slug>`;
- o artefato usa só variáveis do contrato para cor, tipografia, raio e sombra;
- cada seção ou slide tem um objeto do estilo, não um cartão genérico;
- as capturas em 1440 e 390 px foram abertas e revisadas por você, sem texto cortado, sobreposição ou rolagem horizontal;
- o movimento pausa fora da tela, com a aba oculta e com movimento reduzido;
- `pycode text` passou nos textos que você escreveu.

## Índice das referências

- `references/escolher-estilo.md`: tabela de pedido para estilo e perguntas de desempate. Abra ao escolher.
- `references/principios.md`: como fugir da cara de template, objeto herói, hierarquia, densidade e contraste. Abra antes de compor qualquer tela.
- `references/objetos.md`: trechos curtos de HTML, CSS e SVG para ingresso, traço que se desenha, medidor, papel rasgado, sprite, linha de estações e outros. Abra ao construir.
- `references/movimento.md`: esqueleto de IntersectionObserver, pausas, movimento reduzido, parâmetros de duração e easing, armadilhas e quando usar GSAP. Abra ao animar.
- `references/contrato-tokens.md`: as 24 variáveis, como as skills consomem um estilo e como exportar. Abra ao escrever um modelo ou um tokens.css.
- `references/criar-estilo.md`: da captura da referência ao `styles check`. Abra quando a pessoa trouxer um visual próprio.
- `references/acervos.md`: acervos externos, licenças e roteiro de estudo sem cópia. Abra antes de `pycode refs`.
- `references/acessibilidade.md`: contraste, teclado, leitores de tela, movimento e celular. Abra na revisão final.
