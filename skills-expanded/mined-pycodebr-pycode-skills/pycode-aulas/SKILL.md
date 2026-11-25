---
name: pycode-aulas
description: 'Use quando pedirem uma aula, palestra, apresentação ou slides interativos em HTML (deck, slideshow, presentation, lesson, talk), uma aula animada que avança cena a cena como um PowerPoint criativo, o material de estudo da aula no Notion ou desenhos da aula no Whimsical. Entrega um deck 1920×1080 com demonstração por cena, clique para assumir, modo leitura e celular, QA no navegador, PNG, PDF, PPTX e a página de estudo.'
license: MIT
metadata:
  version: 1.0.0
  author: PycodeBR (Felipe Azambuja)
---

# Aulas e apresentações interativas (pycode-aulas)

Esta skill transforma um assunto numa aula em HTML que avança cena a cena: cada cena tem um objeto visual próprio que
explica a ideia (circuito, mapa, pilha de camadas, terminal, régua de tempo), toca uma demonstração curta ao entrar,
volta ao início e para, e passa o controle para quem apresenta no primeiro clique. O mesmo texto alimenta o modo
leitura, o celular, o PDF, o PPTX e o material de estudo no Notion.

## Pré-requisito

Todos os passos usam o comando `pycode`. Confira antes de começar:

```bash
command -v pycode || ls ~/.pycode-skills/bin/pycode
```

Se não existir, instale (uma vez):

```bash
curl -fsSL https://raw.githubusercontent.com/pycodebr/pycode-skills/main/install.sh | bash
```

Depois rode `pycode doctor`. Nunca chame os scripts da skill por caminho: use sempre `pycode deck <comando>`.

## Quando usar

- "Monte uma aula interativa sobre X", "quero slides animados", "uma apresentação em HTML para a palestra".
- Transformar um roteiro, um artigo ou uma aula gravada numa apresentação de cenas.
- Gerar o material de estudo (Notion) e os desenhos (Whimsical ou SVG) da mesma aula.
- Exportar a apresentação para PDF ou PPTX.

## Quando não usar

- Página de vendas, landing page ou site: use a skill `pycode-paginas`.
- Carrossel de Instagram: use `pycode-carrosseis`.
- Escolher ou criar um estilo visual: use `pycode-design` (esta skill consome os estilos de lá).
- Slides editáveis no PowerPoint como entregável principal: o deck é HTML; o PPTX gerado aqui guarda o design como
  imagem (veja `references/exportacao.md`).

## Fluxo de trabalho

### 1. Entender o pedido e o público

Descubra quem assiste, quanto tempo dura, o que a pessoa precisa saber fazer no fim e onde a aula roda (telão,
link para alunos, os dois). Escolha o estilo com `pycode styles list` (e `pycode styles show <slug>`); leia o
`DESIGN.md` do estilo para criar objetos e movimentos coerentes com ele. Sem preferência, use o `default_style` da
marca (`pycode brand`).

### 2. Roteiro de cenas aprovado

Antes de qualquer código, escreva a tabela de cenas: id, título de 2 a 5 palavras, mensagem em uma frase, visual que
explica, arquétipo, gancho para a próxima. Defina o fio visual (um objeto que atravessa a aula e se completa no
fim) e o orçamento de texto. Método completo em `references/planejamento.md`; catálogo de arquétipos em
`references/arquetipos.md` ou `pycode deck scene list`. **Mostre o roteiro e espere aprovação.**

### 3. Criar o projeto

```bash
pycode deck new aulas/minha-aula --title "Título da aula" --style <slug>
# ou escolhendo os arquétipos na ordem do roteiro:
pycode deck new aulas/minha-aula --title "Título da aula" --style <slug> \
  --archetypes capa,conversa,terminal,circuito,camadas,mostrador,linha-do-tempo,mapa,encerramento
```

O projeto nasce com o motor, as cenas do modelo "Como funciona uma API", os tokens do estilo, as fontes e o GSAP
locais e a sua marca (`~/.pycode-skills/brand.json`). Opções: `--scenes N`, `--tokens arquivo.css` (estilo próprio
com todas as variáveis do contrato), `--lang`. Para acrescentar cenas depois:
`pycode deck scene add aulas/minha-aula --archetype mapa --id integracoes --after viagem`.

### 4. Escrever o conteúdo

Todo o texto fica em `src/content.json` (fonte única): `meta` (título, descrição, fio, material de estudo em
`meta.study`) e uma entrada por cena (`title`, `apoio`, `hook`, `thread`, `reading`, `notes`, `study`, `data`).
Palco com pouco texto (até ~30 palavras por cena); explicação completa em `apoio` e `reading`; aprofundamento,
exemplos e exercícios em `study`. Rode `pycode text src/content.json` e corrija tudo.

### 5. Construir cena a cena, visual primeiro

Para cada cena, em `src/scenes/<id>.js` e `.css`:

1. Desenhe o estado de repouso (o objeto que explica) e confira em `?still`.
2. Escreva `focus(i, anim)`, a única função que muda o estado, e use-a na demonstração (`FX.cycle`) e no clique
   (`ctx.pick`).
3. Faça a intro com `fromTo` e `clearProps`; movimento contínuo só em `ambient(dt)`.
4. Devolva `{ intro, loop, home, key, still }`.

Contrato completo, utilidades e exemplo em `references/motor-e-cenas.md`; leia `references/armadilhas.md` antes da
primeira cena.

```bash
pycode deck build aulas/minha-aula          # monta site/ e recusa contrato quebrado, cor fixa, CDN e texto com erro
pycode serve aulas/minha-aula/site          # prévia em http://127.0.0.1:8080
pycode deck qa aulas/minha-aula --only <id> --fast   # QA rápido da cena que você mexeu
```

### 6. QA completo

```bash
pycode deck qa aulas/minha-aula
```

Fail-closed: cada cena sem erro de console, nada fora do palco, texto de 16 px ou mais, orçamento de palavras,
demonstração que termina em `home`, clique que assume e muda a seleção, R que recomeça; teclado, deep link, posição
salva, movimento reduzido, modo leitura em 390 px, celular em retrato e paisagem, nenhuma requisição externa. Avise a
pessoa que o QA está rodando (leva alguns minutos). Detalhes em `references/qa-e-revisao.md`.

### 7. Revisão por visão e iteração

Abra `qa/folha-de-contato.jpg`, as capturas em pares, as de clique e as de celular (`qa/shots/`). Procure monotonia,
texto demais, rótulos cruzados por linhas, balões cobrindo o que explicam, cortes, contraste. Corrija, rode o build e
o QA da cena e olhe de novo. Itere até cada cena merecer 8 de 10.

### 8. Exportar

```bash
pycode deck stills aulas/minha-aula               # PNG 1920×1080 por cena + folha de contato
pycode deck export aulas/minha-aula --pdf --pptx  # PDF pesquisável e PPTX com notas
```

### 9. Material de estudo no Notion

```bash
pycode deck notion aulas/minha-aula --url <endereço da aula publicada>
```

Gera `material/material-notion.md` (explicação por cena, exemplos, diagramas Mermaid validados, glossário,
exercícios com gabarito recolhido, fontes) e as partes em `material/notion-partes/`. Publique pelo conector de Notion
do seu agente (uma parte por chamada, depois leia de volta) ou, se houver `NOTION_TOKEN` no ambiente, com
`--parent <id-da-página-mãe>`, que publica e confere a leitura de volta. Nunca peça token no chat. Detalhes em
`references/notion.md`.

### 10. (Opcional) Whimsical

Quando a turma vai usar um quadro, desenhe em Mermaid `flowchart` com cores por papel e um nível de subgrafo, valide
com `pycode mermaid` e cole no Whimsical. Sem conta, gere SVG com `pycode mermaid`. Modelos em `templates/diagrams/`;
técnica em `references/whimsical.md`.

### 11. Entregar

Informe: caminho do projeto e do `site/` (ou a URL publicada), como abrir (`pycode serve`), atalhos de teclado,
resultado do QA (cenas, tempo, avisos), arquivos exportados, material gerado ou publicado e o que não foi verificado.

## Regras de qualidade

- **Uma imagem central por cena que explica sem leitura.** Objetos ligados ao assunto; nada de grade de cartões,
  fundo liso com texto, gradiente genérico, emoji como ícone ou rótulo em caixa alta acima do título.
- **Títulos de 2 a 5 palavras.** Até ~30 palavras visíveis no palco em repouso; o resto vai para leitura e material.
  Exceções declaradas com `budget` quando o texto é o próprio objeto (conversa, terminal, citação).
- **Demonstração única por cena** e clique que entrega o controle; nada que repita sozinho além do movimento ambiente.
- **Fio visual e ganchos** ligam as cenas; o fio se completa no fim.
- **Movimento só com transform, opacity e stroke de SVG**; `?still` e movimento reduzido mostram o estado final
  legível.
- **Só variáveis do contrato de estilos** no CSS (o build recusa cor fixa), para o deck funcionar com qualquer estilo.
- **Nada de CDN:** fontes, GSAP e imagens ficam no projeto.
- **Texto PT-BR natural e acentuado**, sem travessão, reticências de suspense, "não é X, é Y", clichês ou promessa
  de resultado. `pycode text` com zero erros.
- **Fatos verificados:** números, datas, comandos e citações conferidos na fonte; exemplos de código executados.
- Conteúdo de exemplo e dados fictícios identificados como tal; sem dados pessoais de alunos.

## Só diga que terminou quando

- `pycode deck build` passou sem erros e `pycode deck qa` (completo) terminou com `QA ok`;
- você olhou a folha de contato, as cenas em tamanho grande, as capturas de clique e as de celular, e corrigiu o que
  encontrou;
- `pycode text` não acusa erros no `content.json` nem no material;
- os arquivos pedidos (PNG, PDF, PPTX, material) foram gerados e conferidos;
- a resposta final diz o que foi verificado e o que ficou pendente (por exemplo, publicação no Notion sem token).

## Referências (abra quando precisar)

| Arquivo | Quando abrir |
|---|---|
| `references/planejamento.md` | antes do roteiro: problema antes do mecanismo, fio visual, ganchos, orçamento de texto |
| `references/arquetipos.md` | para escolher o visual de cada cena e saber os campos de `data` |
| `references/motor-e-cenas.md` | ao escrever ou adaptar uma cena: contrato, `ctx`, `FX`, `K`, estrutura do projeto |
| `references/armadilhas.md` | antes da primeira cena e quando algo travar, sumir ou não responder ao clique |
| `references/qa-e-revisao.md` | para entender uma falha do QA, revisar por visão e conferir o celular |
| `references/exportacao.md` | ao gerar PNG, PDF e PPTX e explicar os limites de cada um |
| `references/notion.md` | ao montar e publicar o material de estudo |
| `references/whimsical.md` | quando pedirem quadro no Whimsical ou diagramas sem conta |

Exemplo público de deck feito com esta técnica: a palestra da PycodeBR na Python Brasil 2026
(`github.com/pycodebr/pycodebr_python_brasil_2026`).
