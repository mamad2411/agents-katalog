---
name: pycode-carrosseis
description: 'Use quando pedirem carrossel de Instagram, post de feed 4:5, slides para Instagram, carrossel educativo ou técnico, quiz em carrossel, lista de ferramentas em cartas, slide em vídeo curto ou ideias de carrossel (Instagram carousel, feed post). Entrega um projeto HTML 1080x1350 com conceito visual desenhado em código (com ou sem gerador de imagens), texto em slides.json, render no Chromium, vídeo MP4 determinístico, QA fail-closed, prévia no celular, legenda e pacote para publicar.'
license: MIT
metadata:
  version: 1.0.0
  author: PycodeBR (Felipe Azambuja)
---

# Carrosséis de Instagram (`pycode-carrosseis`)

Carrosséis de Instagram em 4:5 com conceito visual próprio: cartas colecionáveis, mapa do metrô, escada de níveis, fliperama, cabine, maleta. Cada slide tem um objeto herói desenhado em código (SVG, canvas, HTML) ou uma cena do gerador de imagens do seu agente com todo o texto renderizado por cima. O texto vive num `slides.json`, o Chromium renderiza em 1080x1350 exatos e um QA reprova o que não passa.

## Pré-requisito

```bash
command -v pycode || ls ~/.pycode-skills/bin/pycode
# se nenhum existir:
curl -fsSL https://raw.githubusercontent.com/pycodebr/pycode-skills/main/install.sh | bash
pycode doctor
```

Use sempre `pycode carousel <comando>`; nunca chame os scripts por caminho. `pycode brand` mostra nome e @ que entram nos slides (edite `~/.pycode-skills/brand.json`). Os estilos vêm da skill `pycode-design` (`--style <slug>`).

## Quando usar

- Carrossel educativo ou técnico para o feed (explicar um conceito, uma lista de ferramentas, uma trilha, um quiz).
- Post único 4:5 que precisa de objeto e texto exato (um carrossel de 2 slides também passa pelo QA).
- Slide em vídeo curto (4 a 6 s) dentro de um carrossel.
- "Me manda ideias de carrossel": cada ideia já com conceito visual e texto final dos slides.

## Quando não usar

- Anúncio pago, criativo de campanha com oferta e preço: esta skill não trata oferta.
- Página, site ou landing page: use `pycode-paginas`.
- Aula ou apresentação: use `pycode-aulas`.
- Reels ou vídeo longo com fala: o vídeo daqui é um slide animado de poucos segundos.

## Fluxo de trabalho

1. **Pauta e fatos.** Junte o que vai no post com fonte: documentação oficial, código rodado, saída real. Rode todo trecho de código que for aparecer.
2. **Conceito visual.** Escolha em `references/conceitos.md` (ou crie um no mesmo nível): um cenário que o público reconhece, um objeto herói por slide, avanço de slide a slide, um slide em vídeo.
3. **Roteiro com texto final.** Capa até ~20 palavras, slides até ~35, uma ideia por slide, slide 2 autossuficiente, CTA só no último. Regras em `references/escrita.md`. Mostre o roteiro.
4. **Projeto.** Parta de um exemplo próximo ou do modelo:
   ```bash
   pycode carousel new pasta --example cartas|metro|niveis|fliperama [--style slug] [--title "..."]
   pycode carousel new pasta --title "Título da capa" --slides 8 [--style slug]
   ```
   Escreva o texto em `slides.json`, o visual em `css/scene.css` e o desenho e a animação em `js/scene.js` (API em `references/projeto.md`). Use só os tokens do estilo para cor, fonte, raio e sombra.
5. **Capa e slide 2 primeiro.** `pycode carousel render pasta --slides 1,2`, revise por visão e mostre para aprovação antes de produzir o resto.
6. **Produção completa.**
   ```bash
   pycode carousel render pasta                 # out/slide-NN.png em 1080x1350 (--format jpg, --scale 1|2)
   pycode carousel video pasta --slide 1        # out/slide-01.mp4 + pôster (--seconds, --fps, --audio, --normalize)
   ```
   Com gerador de imagens: cena sem texto, tela em magenta e `pycode carousel compose`; enquadramento com `pycode carousel fit`. Veja `references/gerador-de-imagens.md`.
7. **QA.**
   ```bash
   pycode carousel qa pasta
   ```
   Corrija até zero erro. Depois revise todos os slides por visão (folha em `out/folha-de-contato.jpg` e cada slide em tamanho real) com as perguntas do critério de conclusão.
8. **Legenda e prévia.**
   ```bash
   pycode carousel caption pasta      # esqueleto; escreva a legenda no lugar dos [[...]]
   pycode text pasta/legenda.md
   pycode carousel preview pasta      # preview.html; abra com pycode serve pasta
   ```
9. **Pacote.** `pycode carousel pack pasta` gera `<slug>.zip` com slides numerados, vídeos, pôsteres, legenda, folha de contato, licenças e relatório. A publicação é manual, pelo app (`references/stories-e-publicacao.md`).

## Como propor ideias

Cada ideia vem pronta para aprovar: título; conceito visual (cenário, objeto herói de cada slide, qual slide é vídeo e o que se move nele); "por que prende" em uma ou duas frases sobre a reação concreta (salvar a lista, acertar o quiz, se reconhecer num nível); e os slides numerados **com o texto final**. Descrever a estrutura em termos de planejamento ("slide de gancho", "diagrama em camadas") não serve. Termine recomendando por onde começar e oferecendo a capa e o slide 2 para aprovação. Formato completo em `references/metodo.md`.

## Regras de qualidade

- **Um conceito, um objeto herói por slide.** Cartão de texto sobre fundo liso reprova. Sério e limpo mudam o tom, nunca tiram o objeto.
- **Texto, número, comando e interface só por código.** O gerador de imagens faz cena e objeto, sem texto.
- **Contraste de 4,5:1 medido** no fundo real atrás de cada bloco (o QA mede com o texto escondido). Texto sobre imagem precisa de faixa ou fundo, não só sombra.
- **Um caminho de leitura:** título, apoio e detalhe, de cima para baixo. Nada de elementos disputando atenção (molduras, etiquetas e contadores extras).
- **Margem segura de 64 px**, corpo de pelo menos 34 px e rótulos de pelo menos 24 px em 1080 de largura.
- **Código exato e executado:** saída mostrada é saída real (`run: doctest` ou `run: python`), comando copiado de documentação tem `source`; ligaduras desligadas e quebra só entre tokens.
- **Um único CTA, no último slide.** Pergunta de gancho na capa é permitida; pedido de comentário, salvamento ou envio no meio, não.
- **Slide em vídeo determinístico:** `setT(t)` puro, quadro 0 já com título e objeto (é o pôster), H.264 yuv420p BT.709 com faststart, 4 a 6 s.
- **Som só com licença guardada** em `licencas/`; música só pelo app.
- **Âncoras discretas da marca** (nome ou @ e contador N/T), vindas do `brand.json`.
- **Texto PT-BR acentuado e natural:** sem travessão, sem reticências de suspense, sem fórmulas de texto gerado, sem promessa de resultado. `pycode text` em `slides.json` e `legenda.md`.
- **Movimento** só com `transform`, `opacity` e `stroke`; no navegador, respeita `prefers-reduced-motion`.

## Critérios de conclusão

Só diga que terminou quando:

- `pycode carousel qa pasta` sai com código 0 (zero erros) depois do último render e do último vídeo;
- você olhou **todos** os slides por visão e cada um responde "sim" a "para a rolagem só pela imagem?" e "o texto se lê no celular?", e "não" a "está carregado?" e "algum objeto parece colado?";
- o slide em vídeo foi gravado, tem som licenciado ou foi decidido sem som, e o pôster funciona sozinho;
- a legenda final está escrita (sem `[[...]]`) e passou no `pycode text`;
- `preview.html` foi gerado e o `pack` produziu o zip;
- você informou o que não conseguiu conferir (fato sem fonte, efeito sem licença registrada, publicação que ficou para a pessoa).

## Referências (abra quando precisar)

- `references/metodo.md`: o caminho completo da pauta à entrega e o formato para propor ideias. Abra no começo de todo carrossel.
- `references/conceitos.md`: catálogo de conceitos aprovados e o que foi reprovado. Abra ao escolher o visual.
- `references/escrita.md`: texto dos slides, segunda capa, CTA único e legenda. Abra ao escrever o roteiro e a legenda.
- `references/projeto.md`: anatomia da pasta, campos do `slides.json`, código conferido, trilho contínuo e API do runtime. Abra ao editar o projeto.
- `references/gerador-de-imagens.md`: caminho sem gerador (tudo em código) e com gerador (prompt sem texto, tela magenta, mesma cena entre slides, 2:3 para 4:5). Abra ao decidir de onde vêm as cenas.
- `references/video-e-som.md`: animação determinística, pôster, cor BT.709, onde baixar efeitos com licença e como mixar. Abra antes do slide em vídeo.
- `references/tipografia-e-codigo.md`: tamanhos, fontes pixel, glifos fora do subconjunto, código exato e numeral em canvas. Abra quando o slide tem código ou fonte especial.
- `references/stories-e-publicacao.md`: Stories 9:16 no mesmo visual e publicação manual. Abra na entrega.
- `references/armadilhas.md`: problemas reais de Chromium, vídeo, imagem e texto. Abra quando algo sair estranho.

Exemplos completos em `examples/` (cartas, metro, niveis, fliperama): copie com `pycode carousel new pasta --example <nome>` e troque texto e objetos.
