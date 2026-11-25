---
name: visual-check
description: Renderiza uma UI (página ou jogo Godot) em larguras comprovadas, lê o screenshot e confere contra a intenção ou uma fonte (Figma/print). Use antes de afirmar que um layout está certo — responsivo, fidelidade, anti-slop. Sem rota de captura calibrada, declara que não rodou.
argument-hint: "<URL, arquivo HTML ou projeto Godot> [larguras] [fonte: link do Figma ou print]"
metadata:
  maintained_by: native-sdd (internal — not a third-party marketplace skill)
  version: "1.0.0"
---

# Visual check

Ver o que foi construído antes de dizer que está pronto. O resultado é **evidência**: um PNG por
largura, com a largura **comprovada**, lido por você com `Read`. Check sem PNG é "não verificado",
nunca "passou".

Só precisa de `Bash` + `Read`. Nada aqui instala coisa alguma.

**Chamada direta:** `/visual-check <URL ou arquivo HTML> [larguras] [fonte]` roda esta skill (skill
vence command homônimo — por isso não há `commands/visual-check.md`); alvo, larguras e fonte vêm
dos argumentos. Na sessão principal, sem URL/arquivo renderizável, **pergunte** antes de seguir;
só o subagente (ex.: `designer`), que não pode perguntar, devolve "não rodou (sem URL)".

## Pré-condições — sem elas, o resultado é "não rodou"

- **Uma URL renderizável:** a que o chamador passou, um servidor que já está rodando, ou `file://`
  de um HTML estático. **Não suba dev server por conta própria** — processo em background dentro de
  subagente fica órfão, e o comando depende da stack. Sem URL: "não rodou (sem URL)", com o comando
  que o usuário rodaria para subir o servidor. Jogo Godot é a exceção: o alvo é o projeto (seção
  **Janela de engine: Godot**).
- **Uma rota de captura que calibre** (seção **Calibração**). Sem nenhuma: "não rodou (sem rota calibrada)".
- **Nunca instale** navegador, Playwright ou pacote para conseguir rodar. Se faltar, sugira ao
  usuário o comando (ex.: `npm i -D playwright`, ou baixar o `chrome-headless-shell` do Chrome for
  Testing) e deixe a decisão com ele.

## Calibração — a rota só vale se provar a largura

A rota errada **não dá erro**: o PNG sai do tamanho pedido e a página foi montada com outra largura.
Medido no Windows: `msedge`/`chrome --headless --window-size=375,…` montam a página com 492/500 px,
e com 1440 montam 1416/1424. Por isso nenhuma rota é confiável pelo nome — só pela calibração abaixo.

Para **cada largura** que for usar, antes da captura real:

1. Capture `assets/calibrar.html` (nesta skill) pela mesma rota, na mesma largura.
2. Abra o PNG com `Read`: a página escreve `W=<innerWidth>`.
3. `W` igual ao pedido → a rota vale para essa largura. Diferente → rota reprovada para ela; tente a
   próxima. Registre o `W` observado no relatório.

Rotas, na ordem em que vale tentar (todas passam pela calibração):

- **Playwright CLI** já resolvível (dependência do projeto ou cache): `npx --no-install playwright
  screenshot --channel msedge --viewport-size=375,800 <url> <png>` (ou `--channel chrome`). Sem
  `--channel` ele só pede para baixar navegadores e **não gera PNG com exit sem erro** — confira o
  arquivo, não o código de saída.
- **`chrome-headless-shell`** já presente na máquina: `chrome-headless-shell --screenshot=<png>
  --window-size=375,800 --hide-scrollbars <url>` (no Linux pode precisar de `--no-sandbox`). Fora do
  `PATH`, procure no cache de navegadores do Playwright, que o traz junto com o Chromium:
  `ms-playwright/chromium_headless_shell-*/` dentro de `%LOCALAPPDATA%` (Windows),
  `~/Library/Caches` (macOS) ou `~/.cache` (Linux), ou em `$PLAYWRIGHT_BROWSERS_PATH` se definido.
  No Windows ele calibrou exato em 375/768/1280 (2026-10-17).
- **Navegador instalado por CLI** (`--headless --screenshot --window-size`): só se a calibração der
  exato na largura — no Windows não dá.

## Janela de engine: Godot

Jogo web (Phaser, Three.js) é página: use as rotas acima. Jogo **Godot 4** se captura pelo Movie
Maker da própria engine, e a calibração tem o mesmo papel da do navegador.

- **Pré-condições.** O binário `godot` (ou `Godot_v4*_console.exe`) já resolvível; sem ele, "não
  rodou (sem Godot)". Nunca instale: sugira ao usuário baixar o da versão do projeto. A rota abre
  uma **janela de verdade** (`--headless` desliga a renderização). No Linux sem tela, um `xvfb-run`
  já instalado dá uma, com `--rendering-driver opengl3 --audio-driver Dummy` na linha de captura
  (medido em container Ubuntu 22.04 com Mesa, 2026-10-22). Sem tela e sem Xvfb, "não rodou".
- **O tamanho vai num `override.cfg`, não em `--resolution`.** Medido com o Godot 4.7.2 no Windows
  (2026-10-22): com `--resolution 375x800` o jogo monta 375×800, mas o PNG sai no tamanho do
  `project.godot` (1152×648) e em branco, sem erro. Com o `override.cfg` sai exato. Ele fica na raiz
  do projeto do usuário: se já existir um, **não sobrescreva** ("não rodou (override.cfg do
  projeto)"); crie, capture e apague no mesmo passo, e diga no relatório que ele existiu.

  ```ini
  [display]
  window/size/viewport_width=375
  window/size/viewport_height=800
  ```

- **Captura:** `godot --path <projeto> --write-movie <tmp>/f.png --fixed-fps 10 --quit-after 5
  [res://<cena>.tscn]`. Sai uma sequência `f00000000.png`…; leia a **última** (a primeira pode vir
  antes da cena montar). Sem a cena, roda a `main_scene` do projeto.
- **Calibração:** copie `assets/godot-calibrar/` para a pasta temporária (rodar cria `.godot/` e
  `*.uid`, nunca dentro da skill), ponha nela o mesmo `override.cfg` e capture pela mesma linha. O
  PNG escreve `W=… H=…`: igual ao pedido, a rota vale para esse tamanho. **O tamanho do arquivo não
  prova nada:** em 2560×1440, do tamanho da tela, o PNG saiu 2560×1440 e o jogo montou 2560×1421,
  porque a barra de tarefas cortou a janela. Registre o `W×H` observado.
- A calibração prova a janela, não o stretch: `stretch/mode` e `aspect` são design do jogo, e o PNG
  mostra o que o jogador vê naquela janela.

Unity e Unreal não têm rota aqui: a captura delas pede script no projeto ou comando de console do
editor, e nada disso foi medido. Diga "não rodou (sem rota calibrada)" e o que faltou.

## Onde gravar

Tudo o que a verificação cria — PNG, script de medição, JSON de relatório — vai para o diretório
temporário do SO (`$TMPDIR`, `/tmp` ou `%TEMP%`), numa subpasta `visual-check-<data>`. **Nunca dentro
do projeto** — nada garante que ele ignore esses arquivos no git. Se uma
ferramenta só consegue gravar relativo ao projeto (ex.: download de imagem de um MCP do Figma), use
`.visual-check/` na raiz, apague ao terminar e diga no relatório que a pasta existiu.

## Protótipo de direção sobre a página real (Refinar)

Para comparar direções de uma tela que **já existe** antes de mexer no código (etapa 2 da trilha de
redesign do `/dev`), capture a página real com o CSS de cada direção por cima, sem canvas paralelo:

1. Salve uma **cópia estática** do HTML servido na pasta temporária. Aponte os assets para a URL
   absoluta do servidor e tire os `<script>`.
2. Para cada direção, gere uma cópia com um `<style>` de override antes do `</head>`. Mudança de
   texto ou marcação entra na própria cópia.
3. Capture o **antes pela mesma cópia estática**, e não pela página ao vivo. A página ao vivo roda
   JS e as cópias não, e o estado diverge (botão habilitado por uma resposta da API, por exemplo).
   Antes e direções precisam ter o mesmo estado.
4. Capture tudo nas larguras do brief e leia cada PNG. Defeito do protótipo conta igual a defeito de
   código: corrija antes de mostrar.

Os PNGs vão para o `decision-preview`. A direção aprovada vira o diff no código de verdade, que
depois é verificado pela página ao vivo.

## Estados interativos: foco sim, hover não

As rotas acima tiram screenshot da página parada: ninguém dá Tab nem passa o mouse. Por isso
"foco invisível", da lista de *Ler e comparar*, precisa de um passo a mais.

- **Foco** se captura pela cópia estática da seção anterior: no fim do `<body>`, um
  `<script>document.querySelector('<seletor>').focus()</script>`. Medido no `chrome-headless-shell`
  (2026-10-17): sem interação anterior, o `.focus()` por script ativa o `:focus-visible`, e o anel
  sai no PNG. Vale também para controle escondido com o estado no pai
  (`label:has(input:focus-visible)`). Uma cópia por elemento focado; confira no PNG que o anel
  aparece e tem contraste de 3:1 contra o que está em volta (`contrast.ps1`).
- **Hover** não tem equivalente: nenhum script ativa `:hover`, e as rotas CLI não movem o mouse. Com
  automação de navegador na sessão principal (ex.: Claude in Chrome), mova o mouse sobre o elemento
  e capture; sem ela, o hover sai como **não verificado** no relatório, com o motivo. Não copie as
  regras de `:hover` para uma classe para simular: o screenshot passaria a provar a cópia, não a
  regra.

## Larguras

| Modo | Larguras |
|------|----------|
| Refinar / Greenfield | 375 · 768 · 1280 |
| Fidelidade | as larguras dos artboards da fonte (+375 se a fonte não tiver versão mobile) |
| Varredura (só se pedida) | 320 · 375 · 480 · 600 · 768 · 900 · 1024 · 1280 · 1440 · 1920 |

Altura: a da primeira dobra (~800) para layout; página inteira (`--full-page` no Playwright) quando o
que importa é o ritmo entre seções.

## Ler e comparar

Abra cada PNG com `Read` e confira o que a tarefa pediu. Leia sob demanda, não de cabeça:

- [`references/fidelidade.md`](references/fidelidade.md) — quando existe uma fonte (Figma/print):
  item a item, com a fonte e o PNG lado a lado.
- [`references/anti-slop.md`](references/anti-slop.md) — em qualquer modo, antes de devolver.

Em qualquer largura, sempre: rolagem horizontal, texto cortado ou sobreposto, alvo de toque < 44 px
no mobile, imagem distorcida ou vazando o contêiner, foco invisível.

**Fonte do Figma:** se houver ferramenta do Figma na sua lista, extraia o spec do nó (tipografia,
cores, espaçamentos, raios) e, se ela oferecer, a imagem de referência do nó. Sem a ferramenta, peça
um print do frame. API do Figma devolvendo 404 costuma ser falta de acesso da conta ao arquivo, não
arquivo inexistente — diga isso e peça outra fonte.

## Desvio ou decisão?

Nem todo desvio de padrão é defeito. Antes de marcar como falha um alinhamento, espaço, cor ou
hierarquia que foge do resto da página, procure a **intenção**: comentário ou nome no código, token
do projeto, fonte visual (Figma/print) ou pedido do usuário.

- Evidência a favor do desvio → **ok**, citando onde ela está.
- Evidência contra → **falha**.
- Nenhuma evidência → **pergunta**: descreva o desvio medido e pergunte se é proposital.

Isso não vale para os defeitos de *Ler e comparar* ("em qualquer largura, sempre") nem para
contraste abaixo de AA em texto legível: esses são falha com qualquer intenção.

## Voltas

Achou defeito → corrija → recapture **só a largura afetada** (a calibração dela já vale). No máximo
**3 voltas por seção**; sem convergir, pare e devolva o delta restante em vez de iterar sem fim.

## Relatório

| Check | Largura (W calibrado) | Evidência | Resultado |
|-------|------------------------|-----------|-----------|
| sem rolagem horizontal | 375 (W=375) | `<tmp>/visual-check-…/375.png` | ok |
| hierarquia do título | 1280 (W=1280) | `…/1280.png` | ajustado na volta 2 |
| contraste do botão | — | — | não verificado (medir pelos tokens) |
| alinhamento da seção 3 | 1280 (W=1280) | `…/1280.png`: título em x=56, as outras em 116 | pergunta: é proposital? |

- Um check só é "ok" com PNG e `W` calibrado ao lado.
- **Pergunta** não reprova: o veredito conta só falhas, e as perguntas vão listadas à parte para o
  usuário responder.
- **Não rodou** é resultado legítimo: diga o motivo (sem URL, sem rota calibrada, página exige
  login), o que ficou sem ver e o que o usuário faria para habilitar.
- Contraste, APG e Core Web Vitals não se provam por screenshot: meça pelos tokens/ferramentas e
  diga como mediu. Contraste: `pwsh "$toolsRoot/contrast.ps1" -Foreground <cor> -Background <cor>`
  para cada par que a tela pinta, incluindo os estados novos.
- Mockup para avaliar **antes** de existir código não é caso desta skill → rota canvas do `designer`.
