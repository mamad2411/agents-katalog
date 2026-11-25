---
name: web-to-markdown
description: "Use APENAS quando o usuário disser explicitamente: 'use a skill web-to-markdown ...' (ou 'use a skill web-to-markdown ...'). Converte URLs de páginas web em Markdown limpo chamando o CLI local web2md (Puppeteer + Readability), adequado para páginas renderizadas em JS."
metadata:
  version: 0.1.0
---

# web-to-markdown

Converta páginas web em Markdown limpo acionando um navegador instalado localmente (via `web2md`).

## Portão de disparo explícito (deve ser aplicado)

Esta skill NÃO DEVE ser usada a menos que o usuário tenha escrito explicitamente **exatamente** uma frase como:
- `use a skill web-to-markdown ...`
- `use a skill web-to-markdown ...`

Se o usuário não solicitou explicitamente esta skill pelo nome, interrompa e peça que ele reemita a solicitação incluindo: `use a skill web-to-markdown`.

## O que esta skill faz

- Processa páginas renderizadas em JS (Puppeteer → Chrome do usuário).
- Funciona melhor com navegadores da família Chromium (Chrome/Chromium/Brave/Edge) via `puppeteer-core`.
- Extrai conteúdo principal (Readability).
- Converte para Markdown (Turndown) com links limpos e frontmatter YAML opcional.

## Fora do escopo

- Não use Playwright ou outras stacks de automação de navegador; o mecanismo é `web2md`.

## Inputs que você deve coletar (pergunte apenas se ausentes)

- `url` (ou uma lista de URLs)
- Preferência de saída:
  - Imprimir no stdout (`--print`), OU
  - Salvar em arquivo (`--out ./file.md`), OU
  - Salvar em diretório (`--out ./some-dir/` para auto-nomear pelo título da página)
- Controles de renderização opcionais para páginas complicadas:
  - `--chrome-path <path>` (se a detecção automática de Chrome falhar)
  - `--interactive` (mostrar Chrome e pausar para que o usuário complete verificações/login, depois pressione Enter)
  - `--wait-until load|domcontentloaded|networkidle0|networkidle2`
  - `--wait-for '<css selector>'`
  - `--wait-ms <milliseconds>`
  - `--headful` (debug)
  - `--no-sandbox` (às vezes necessário em containers/CI)
  - `--user-data-dir <dir>` (login/sessão; use um diretório de perfil dedicado)

## Fluxo de trabalho

1) Confirme que o usuário invocou explicitamente a skill (`use a skill web-to-markdown`).
2) Valide se as URL(s) começam com `http://` ou `https://`.
3) Garanta que `web2md` está instalado:
   - Execute: `command -v web2md`
   - Se ausente, instrua o usuário a instalá-lo:
     - Se disponível via npm: `npm install -g web2md`
     - Se do código-fonte: Clone o repositório, depois execute `npm install && npm run build && npm link`
4) Converta:
   - URL única → arquivo:
     - `web2md '<url>' --out ./page.md`
   - URL única → arquivo auto-nomeado em diretório:
     - `mkdir -p ./out && web2md '<url>' --out ./out/`
   - Verificação humana / paredes de login (interativo):
     - `mkdir -p ./out && web2md '<url>' --interactive --user-data-dir ./tmp/web2md-profile --out ./out/`
     - Depois: complete a verificação na janela do navegador e pressione Enter no terminal para continuar.
   - Imprimir no stdout:
     - `web2md '<url>' --print`
   - URLs múltiplas (lote):
     - Crie diretório de saída (ex. `./out/`) e execute um comando `web2md` por URL usando `--out ./out/`
5) Valide a saída:
   - Se escrever arquivos, verifique se existem e não estão vazios (ex. `ls -la <path>` e `wc -c <path>`).
6) Retorne:
   - O(s) caminho(s) do arquivo salvo, ou o Markdown (modo stdout).

## Padrões (recomendados)

- Para a maioria das páginas: `--wait-until networkidle2`
- Para aplicações pesadas: comece com `--wait-until domcontentloaded --wait-ms 2000`, depois adicione `--wait-for 'main'` (ou outro seletor estável) se necessário.