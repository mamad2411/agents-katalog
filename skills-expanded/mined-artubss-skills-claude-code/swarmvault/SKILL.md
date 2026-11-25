---
name: swarmvault
description: "Use SwarmVault quando o usuário precisa de um cofre de conhecimento local-first que escreve artefatos duráveis em markdown, graph, search, dashboard, review e MCP em disco a partir de livros, notas, transcrições, exportações, datasets, decks de slides, arquivos, URLs, código e workflows de fonte recorrentes."
version: "0.7.30"
license: MIT
metadata: '{"openclaw":{"requires":{"anyBins":["swarmvault","vault"]},"install":[{"id":"node","kind":"node","package":"@swarmvaultai/cli","bins":["swarmvault","vault"],"label":"Instalar SwarmVault CLI (npm)"}],"emoji":"🗃️","homepage":"https://www.swarmvault.ai/docs"}}'
---

# SwarmVault

Use esta skill quando o usuário quer um cofre de conhecimento local-first construído no padrão [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — três camadas (fontes brutas, wiki, schema) onde a LLM mantém uma wiki durável entre você e as fontes brutas. Use também quando o projeto já contém `swarmvault.config.json` ou `swarmvault.schema.md`.

Para onboarding, exemplos, referências de comando ou troubleshooting, leia os `README.md`, `examples/`, `references/` e `TROUBLESHOOTING.md` inclusos antes de improvisar conselhos de workflow.

## Verificações rápidas

- Trabalhe a partir da raiz do cofre.
- Se o cofre ainda não existe, execute `swarmvault init`.
- Use `swarmvault demo --no-serve` quando o usuário quer o walkthrough zero-config mais rápido antes de apontar SwarmVault para suas próprias fontes.
- Use `swarmvault scan <directory> --no-serve` quando o usuário quer a passada mais rápida em um repo local ou árvore de docs sem passar manualmente por init + ingest + compile primeiro.
- Leia `swarmvault.schema.md` antes do trabalho com compile ou query. É o contrato operacional do cofre.
- Se `wiki/graph/report.md` existe, use-o antes de buscas amplas no repo.

## Loop principal

1. Inicialize um cofre com `swarmvault init` quando necessário.
2. Atualize `swarmvault.schema.md` antes de um compile sério. Use-o para regras de nomenclatura, categorias, grounding, expectativas de atualização e exclusões.
3. Use `swarmvault source add <input>` quando a entrada é um arquivo local recorrente, diretório local, raiz do repo GitHub público ou hub de docs que deve permanecer registrado.
4. Ingira entradas únicas com `swarmvault ingest <path-or-url>` ou ingira uma árvore de repo inteira com `swarmvault ingest <directory>`. Arquivos de áudio usam `tasks.audioProvider` quando configurado, e URLs do YouTube suportadas passam por captura de transcrição direta em vez de ingest de URL genérico.
5. Use `swarmvault ingest --guide`, `swarmvault source add --guide`, `swarmvault source reload --guide`, `swarmvault source guide <id>` ou `swarmvault source session <id>` quando o humano deve integrar uma fonte por vez antes de páginas canônicas mudarem. Defina `profile.guidedIngestDefault: true` em `swarmvault.config.json` para tornar o modo guiado o padrão; use `--no-guide` para sobrescrever. Perfis usando `guidedSessionMode: "canonical_review"` colocam edições canônicas na fila de aprovação; perfis `insights_only` mantêm síntese exploratória em `wiki/insights/`. Use `--review` apenas para o caminho review-only mais leve.
6. Use `swarmvault inbox import` para lotes no estilo capture, depois `swarmvault watch --lint --repo` quando o workflow deve permanecer automatizado. Adicione `--code-only` quando a atualização deve permanecer apenas AST e adiar re-análise semântica não-código para um `compile` posterior. Em repos rastreados, mudanças code-only tomam aquele caminho de compile mais rápido automaticamente. Instale `swarmvault hook install` quando checkouts e commits do git devem disparar a mesma atualização repo-aware code-only automaticamente.
7. Compile com `swarmvault compile`, use `compile --max-tokens <n>` quando a wiki gerada deve permanecer dentro de um orçamento de contexto limitado, ou use `compile --approve` quando mudanças devem passar pela fila de revisão local primeiro.
8. Resolva trabalho em staging com `swarmvault review list|show|accept|reject` e `swarmvault candidate list|promote|archive`.
9. Faça perguntas com `swarmvault query "<question>"`. Salva respostas duráveis em `wiki/outputs/` por padrão; adicione `--no-save` apenas para verificações efêmeras. Quando um provedor de embedding está configurado, query pode mesclar correspondências de página semântica em busca local; `search.rerank: true` permite que o `queryProvider` atual rerankeie os top hits mesclados antes de responder.
10. Use `swarmvault explore "<question>" --steps <n>` para loops de pesquisa multi-etapas save-first, ou `--format report|slides|chart|image` quando o artefato deve ser orientado para apresentação.
11. Execute `swarmvault lint` sempre que o schema mudou, artefatos parecem obsoletos ou resultados de compile/query desviam. Defina `profile.deepLintDefault: true` em `swarmvault.config.json` quando a passada de deep-lint consultiva deve ser o padrão, e use `--no-deep` quando você precisa de uma execução apenas estrutural. Adicione `--web` apenas quando deep lint está habilitado e um adaptador `webSearch.tasks.deepLintProvider` está configurado; evidência web é limitada a deep lint e não altera comportamento de compile ou query.
12. Use `swarmvault mcp` quando outro agente ou ferramenta deve navegar, pesquisar e fazer query no cofre através de MCP.
13. Use `swarmvault graph blast <target>` quando o usuário quer análise de impacto de importação reversa, `swarmvault graph serve` quando o workspace em tempo real ou clipper bookmarklet ajudarão, `swarmvault diff` quando eles precisam de um resumo de mudança em nível de graph contra a baseline do último commit, ou `swarmvault graph export --html <output>` / `graph export --report <output>` quando compartilhar ajudar. `graph export` também suporta `--html-standalone`, `--json`, `--obsidian` e `--canvas` para compartilhamento mais leve ou nativo do Obsidian.

## Regras de trabalho

- Prefira mudar o schema antes de re-executar compile quando organização ou grounding está errado.
- Trate `wiki/` e `state/` como outputs de primeira classe. Inspecione-os em vez de confiar em uma resposta de chat única.
- Prefira `wiki/graph/report.md`, `state/graph.json` e páginas wiki salvas sobre buscas amplas ad hoc quando já existem.
- Use `source add` para arquivos recorrentes, diretórios, raízes de repo GitHub público e hubs de docs. Use `ingest` e `add` para entradas deliberadas únicas.
- Quando o cofre reside em um repo git, `ingest|compile|query --commit` pode fazer commit das mudanças em `wiki/` e `state/` imediatamente após a execução.
- O provedor heurístico padrão é um ponto de partida local/offline válido. Adicione um provedor de modelo apenas quando o usuário quer qualidade de síntese mais rica ou capacidades opcionais como embeddings, vision, geração de imagem ou transcrição de áudio. A configuração totalmente local recomendada é Ollama + Gemma: `ollama pull gemma4` depois defina `providers.llm` para `{ type: "ollama", model: "gemma4" }` e aponte `tasks.compileProvider`, `tasks.queryProvider` e `tasks.lintProvider` para ele.
- Ingest de áudio precisa de `tasks.audioProvider` para resolver um provedor que exponha capacidade `audio`. Ingest de transcrição do YouTube não precisa de um provedor. Defina `graph.communityResolution` quando o usuário quer fixar clustering comunitário em vez de usar o padrão adaptativo.
- Se um backend compatível com OpenAI não pode satisfazer geração estruturada, reduza suas capacidades declaradas em vez de forçar cada tarefa através dele.
- Mantenha fontes brutas imutáveis. Coloque correções em schema, novas fontes ou outputs salvos em vez de reescrever manualmente proveniência gerada.

## Arquivos e artefatos

- `swarmvault.schema.md`: regras de compile e query específicas do cofre.
- `raw/sources/` e `raw/assets/`: armazenamento de fonte canônica.
- `wiki/`: páginas geradas mais outputs salvos.
- `wiki/outputs/source-briefs/`: briefs de onboarding salvos para fontes gerenciadas.
- `wiki/outputs/source-sessions/`: âncoras de sessão guiada resumível mais histórico de pergunta/resposta para integração uma-fonte-por-vez.
- `wiki/outputs/source-reviews/`: páginas de revisão em staging com escopo de fonte.
- `wiki/outputs/source-guides/`: guias de integração de fonte em staging para workflows uma-fonte-por-vez.
- `wiki/dashboards/`: fontes recentes, log de leitura, timeline, sessões de fonte, guias de fonte, mapa de pesquisa, contradição e dashboards de questões abertas.
- `wiki/code/`: páginas de módulo para JavaScript ingerido, JSX, TypeScript (incluindo `.mts`/`.cts`), TSX, script Bash/shell (com detecção baseada em shebang para scripts sem extensão), Python, Go, Rust, Java, Kotlin, Scala, Dart, Lua, Zig, C#, C, C++ (incluindo `.c`/`.cc`/`.cpp`/`.cxx` e `.h`/`.hh`/`.hpp`/`.hxx`), PHP, Ruby, PowerShell (`.ps1`/`.psm1`/`.psd1`), Elixir (`.ex`/`.exs`), OCaml (`.ml`/`.mli`), Objective-C (`.m`/`.mm`), ReScript (`.res`/`.resi`), Solidity (`.sol`), componentes Vue single-file (`.vue`), HTML (`.html`/`.htm`) e fontes CSS.
- `state/extracts/`: markdown extraído e sidecars JSON para PDF, família Word completa (`.docx`/`.docm`/`.dotx`/`.dotm`), RTF (`.rtf`), OpenDocument (ODT/ODP/ODS), EPUB, CSV/TSV, família Excel completa (`.xlsx`/`.xlsm`/`.xlsb`/`.xls`/`.xltx`/`.xltm`), família PowerPoint completa (`.pptx`/`.pptm`/`.potx`/`.potm`), notebooks Jupyter (`.ipynb`), BibTeX (`.bib`), Org-mode (`.org`), AsciiDoc (`.adoc`/`.asciidoc`), transcrições, exportações Slack, email, calendar, transcrições de áudio, capturas de transcrição do YouTube e fontes de imagem (`.png`/`.jpg`/`.jpeg`/`.gif`/`.webp`/`.bmp`/`.tif`/`.tiff`/`.svg`/`.ico`/`.heic`/`.heif`/`.avif`/`.jxl`), além de previsualizações estruturadas para arquivos config/data (JSON/JSONC/JSON5/TOML/YAML/XML/INI/ENV/PROPERTIES/CFG/CONF) e ingest de texto com content-sniffing para manifestos de desenvolvedor (`package.json`, `Cargo.toml`, `go.mod`, `LICENSE`, `.gitignore`, `Dockerfile`, `Makefile` e arquivos plaintext similares).
- `state/code-index.json`: dados de aliases de código repo-aware e resolução de importação local.
- `wiki/projects/`: rollups de projeto sobre páginas canônicas.
- `wiki/candidates/`: páginas de conceito e entidade em staging aguardando promoção.
- `state/graph.json`: graph compilado.
- `state/search.sqlite`: índice de busca local.
- `state/sources.json` e `state/sources/<id>/`: entradas de registro de fonte gerenciada mais estado de sincronização em funcionamento.
- `state/approvals/`: bundles de revisão em staging de `compile --approve`.
- `state/sessions/`: artefatos de sessão canônica para compile, query, explore, lint, watch, review e ações candidate.
- `state/jobs.ndjson`: log de execução em modo watch.

## Integração de agente

- `swarmvault install --agent codex|claude|cursor|goose|pi|gemini|opencode|aider|copilot|trae|claw|droid` instala regras específicas de agente no projeto atual.
- `swarmvault install --agent claude|opencode|gemini|copilot --hook` instala suporte de hook graph-first ou plugin para agentes que expõem APIs de hook de projeto.
- `swarmvault install --agent aider` instala `CONVENTIONS.md` e wires `.aider.conf.yml` para lê-lo quando essa config é YAML válido.
- `swarmvault mcp` expõe tools e resources para busca de página, leitura de página, listagem de fonte, query, ingest, compile e lint.

## Padrões a preservar

- Mantenha material de fonte bruta imutável sob `raw/`.
- Salve respostas úteis a menos que o usuário explicitamente queira output efêmero.
- Prefira fluxos revisáveis como `compile --approve`, `review` e `candidate` quando uma mudança não deve se ativar silenciosamente.
- Trate configuração de provedor como parte da operação séria do cofre. Se apenas `heuristic` está configurado, diga isso claramente.
- Quando um cofre usa o bloco `profile` em `swarmvault.config.json`, respeite-o como a camada de comportamento determinístico. `swarmvault.schema.md` ainda define a camada de intenção humana.