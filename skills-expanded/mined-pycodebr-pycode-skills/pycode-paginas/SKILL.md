---
name: pycode-paginas
description: 'Use quando a pessoa pedir uma landing page, página de vendas, página de evento, de curso, de captura, site institucional pequeno, portfólio ou qualquer página/site estático (landing page, static site, HTML/CSS). Cria o projeto a partir de um modelo com objetos visuais próprios por seção, gera o build otimizado (CSS crítico incorporado, fontes locais, cache por hash), roda QA no navegador (responsivo, âncoras, sem JavaScript, movimento, CLS) e mede performance com Lighthouse, tudo pelo comando pycode page.'
license: MIT
metadata:
  version: 1.0.0
  author: PycodeBR (Felipe Azambuja)
---

# `pycode-paginas`: páginas e sites estáticos com design próprio e performance medida

## Pré-requisito

Esta skill usa o comando `pycode`. Confira antes de começar:

```bash
command -v pycode || ls ~/.pycode-skills/bin/pycode
```

Se nenhum dos dois existir, instale (uma vez):

```bash
curl -fsSL https://raw.githubusercontent.com/pycodebr/pycode-skills/main/install.sh | bash
```

Depois rode `pycode doctor`. Use sempre `pycode page <comando>`; nunca chame os scripts da skill por caminho.

## Quando usar

- Landing page de evento, oficina, curso, produto, lista de espera ou captura de contatos.
- Site pequeno de várias páginas (home, página interna, 404) para estúdio, portfólio ou projeto.
- Refazer uma página existente com o mesmo conteúdo e engenharia de performance melhor.
- Medir e corrigir performance, responsividade ou acessibilidade de uma página estática que já existe
  (`pycode page qa <url>` e `pycode page perf <url>` funcionam com qualquer URL).

## Quando não usar

- Aplicação com login, banco de dados ou painel: isso é sistema, não página estática.
- Apresentação de aula em slides: use a skill `pycode-aulas`.
- Carrossel para Instagram: use `pycode-carrosseis`.
- Escolher ou criar um estilo visual (cores, fontes, tokens): use `pycode-design`; esta skill consome os estilos.

## Comandos

| Comando | O que faz |
|---|---|
| `pycode page new <pasta> --title "..." [--style slug] [--kind landing\|site] [--tokens arquivo.css]` | cria o projeto com os tokens do estilo, fontes locais com preload e fallback métrico, a sua marca e a imagem de compartilhamento |
| `pycode page build [pasta]` | gera `dist/`: CSS crítico incorporado (até 15 KB), CSS completo sem bloquear, hash no nome de CSS/JS/fontes, confere build reproduzível e ausência de CDN em runtime |
| `pycode page images <arquivos> [--widths 480,960,1600] [--format webp\|avif\|both] [--eager]` | gera variantes responsivas e imprime o `<img>`/`<picture>` com `srcset`, `sizes`, `width`/`height` |
| `pycode page qa [pasta\|url]` | QA fail-closed no navegador: grava `qa/report.json` e capturas |
| `pycode page perf [pasta\|url] [--runs 3] [--min-score 90] [--block PADRAO] [--baseline]` | Lighthouse celular e desktop, mediana das rodadas, reprova abaixo do mínimo |
| `pycode page check-links [pasta\|url]` | arquivos, âncoras (inclusive em outra página) e links externos |
| `pycode page og [pasta]` | renderiza `og.html` em `src/img/og.jpg` (1200x630) |

Comandos centrais úteis: `pycode styles list`, `pycode serve <pasta>`, `pycode shot`, `pycode sheet`,
`pycode text`, `pycode contrast`, `pycode icon`.

## Fluxo de trabalho

1. **Briefing.** Escreva o que é a página, para quem, qual a ação e o destino dela, quais assuntos entram (em
   ordem) e que material real existe. Não invente número, depoimento, preço ou promessa. (`references/processo.md`)
2. **Tabela assunto → objeto.** Para cada seção, decida o objeto visual que mostra aquele assunto (régua em
   escala, folha de papel, pasta com abas, ingresso, estante, cartão de resposta) e o movimento dele. Nenhuma
   seção fica só com texto, e nenhuma vira grade de cartões iguais. (`references/composicao.md`)
3. **Estilo.** `pycode styles list`; leia o `DESIGN.md` do estilo escolhido (skill `pycode-design`).
4. **Criar o projeto.** Antes, `pycode brand` (ou `pycode brand --init` e edite o arquivo) para o nome, o site,
   o idioma e as cores da marca entrarem no projeto.

   ```bash
   pycode page new minha-pagina --title "Título que vira o h1" --style orbital
   pycode page new meu-site --title "..." --style revista --kind site     # home + página interna + 404
   pycode serve minha-pagina/src                                         # prévia enquanto edita
   ```

   O modelo é uma página completa de exemplo (uma oficina fictícia sobre APIs). Troque o conteúdo seção por
   seção pelo do briefing e redesenhe os objetos que não servem ao seu assunto, mantendo a engenharia
   (`critical.css` para a primeira dobra, `styles.css` para o resto, `.motion-scene` nos componentes com
   movimento, só tokens para cor, fonte, raio e sombra).
5. **Imagens**, se houver: `pycode page images src/img/foto.png --alt "..."` e cole o HTML impresso.
   Sem foto nem gerador, desenhe objetos em HTML/CSS/SVG com os tokens. (`references/imagens.md`)
6. **Destinos.** Troque o `action` do formulário e os links de destino; marque o destino final com
   `data-keep-params` para repassar os parâmetros da URL. Ajuste `site_url` em `pycode-page.json` e as URLs
   absolutas (`canonical`, `og:url`, `og:image`). (`references/formularios-e-links.md`)
7. **Texto.** `pycode text minha-pagina/src/*.html` sem erros nem avisos.
8. **Build.** `pycode page build minha-pagina`.
9. **QA.** `pycode page qa minha-pagina` (leva alguns minutos: cada âncora é testada em navegação nova) e
   `pycode page check-links minha-pagina`. Corrija até passar. Se acrescentar um script de terceiros pedido
   pela pessoa, libere o host no build com `--allow-host`.
10. **Revisão por visão.** Abra as capturas de `qa/` e capture cada seção em 1440 e 390 (role até a seção,
    desligue a rolagem suave, confirme `scrollY` antes de capturar). Pergunte coisas objetivas: sobreposição,
    texto cortado, objeto ilegível no celular, espaço vazio, contraste. Itere até o nível de vitrine.
11. **Performance.** Com a máquina livre: `pycode page perf minha-pagina --runs 3`. Em máquina compartilhada,
    acrescente `--baseline` para separar o ruído da máquina do custo da página. (`references/performance.md`)
12. **Publicação**, se pedida: `references/publicacao.md`, com a conferência da URL pública por hash.

## Regras de qualidade

- **Um objeto por assunto**, ligado ao conteúdo; composição variada entre seções (lado, escala, fundo).
- **Sem kicker** (rótulo decorativo em caixa alta acima do título de seção). A seção começa pelo título.
- **Sem cara de modelo de IA**: nada de três cartões iguais com ícone, emoji como ícone, gradiente roxo e azul,
  vidro fosco sem motivo, faixa colorida na lateral de cartão, mockup genérico de celular.
- **Só tokens do contrato** (`--bg`, `--surface`, `--paper`, `--accent`, `--font-display`, `--radius`,
  `--shadow` e os demais) e `color-mix()` sobre eles. O mesmo HTML precisa funcionar com qualquer estilo.
- **Escala verdadeira**: barra, régua ou altura proporcional ao dado, com o número escrito ao lado.
- **Movimento só com `transform`/`opacity`** (e `stroke` em SVG pequeno), pausado fora da tela e com a aba
  oculta, desligado com movimento reduzido, sem laços no celular. (`references/movimento.md`)
- **Leitura completa sem JavaScript**: nada fica escondido esperando script; menu e perguntas usam `<details>`.
- **Acessível**: um h1, `lang`, `alt`, `label`, foco visível, teclado, contraste 4,5:1. (`references/acessibilidade.md`)
- **Responsivo de verdade** em 1440, 820, 390 e 320: os objetos se reorganizam. (`references/responsivo.md`)
- **Sem CDN em runtime**: fontes e bibliotecas ficam no projeto (o build reprova o contrário).
- **Sem tracking por padrão.** Se pedirem, siga `references/tracking.md` (um único dono do PageView).
- **Texto PT-BR natural e acentuado**, frases completas, sem travessão como pontuação, sem reticências de
  suspense, sem "não é X, é Y", sem promessa de resultado.

## Critérios de conclusão

Só diga que terminou quando:

1. `pycode page build` passou (CSS crítico ≤ 15 KB, build reproduzível, sem CDN, HTML balanceado).
2. `pycode page qa` saiu com código 0 (todas as verificações ok) e você leu os avisos.
3. `pycode page check-links` saiu com código 0; destinos de exemplo trocados ou listados como pendência.
4. `pycode text` sem erros nem avisos nos HTML.
5. Você revisou por visão as capturas de cada seção em 1440 e 390 e corrigiu o que estava fraco.
6. `pycode page perf --runs 3` rodou e você informou as medianas de celular e desktop (nota de performance,
   acessibilidade, boas práticas, SEO, FCP, LCP, TBT, CLS, Speed Index, bytes, requisições) e se alguma rodada
   foi contaminada por carga da máquina. Meta para página sem terceiros: celular ≥ 95 em performance,
   acessibilidade e boas práticas, SEO ≥ 90, CLS 0.
7. Se publicou: a URL pública foi conferida por hash do HTML e de um CSS (`references/publicacao.md`).

No relatório final, liste os comandos rodados com o resultado real, os números medidos e o que ficou pendente.
Não afirme o que não executou.

## Modelos

- `templates/landing/`: landing page completa (hero com a viagem de uma requisição, linha do tempo em escala,
  programa em folha pautada, comparação em bytes, acervo em camadas, perguntas com `details`, ingresso com
  canhoto e formulário).
- `templates/site/`: home, página interna (estante em escala e texto corrido) e 404 (cartão de resposta HTTP),
  com o mesmo CSS.
- `templates/shared/`: CSS crítico e completo, `main.js`, `og.html` e exemplos de `_headers` e `.htaccess`.

## Referências (abra quando precisar)

| Arquivo | Quando abrir |
|---|---|
| `references/processo.md` | no início: etapas do briefing à entrega e a saída de cada uma |
| `references/composicao.md` | ao planejar as seções e os objetos; exemplos de conteúdo → objeto |
| `references/performance.md` | ao mexer em CSS crítico, fontes, imagens, scripts ou ao medir |
| `references/responsivo.md` | ao adaptar objetos para 820, 390 e 320 px |
| `references/acessibilidade.md` | ao editar estrutura, formulários, cores ou interações |
| `references/movimento.md` | ao criar ou alterar animações |
| `references/imagens.md` | com fotos, capturas, gerador de imagens ou nenhum dos dois |
| `references/formularios-e-links.md` | ao configurar destino, formulário, âncoras e parâmetros da URL |
| `references/tracking.md` | só se pedirem analytics ou pixel de anúncio |
| `references/publicacao.md` | ao publicar (GitHub Pages, Netlify, Vercel, Cloudflare Pages, FTP/SFTP) |
| `references/armadilhas.md` | antes de depurar algo estranho; problemas reais com sintoma e correção |
