---
name: power-platform
description: "Use quando a tarefa de um projeto Power Platform (Power Apps Canvas, Power Automate, SQL Server, Dataverse) pedir método ou tocar mais de uma camada: começar um app novo, \"quero criar um app\", ideia de app, \"onde parei\", \"qual o próximo passo\", pipeline /pp, feature de ponta a ponta (tela + flow + banco), \"o número não bate\", \"usuário de uma unidade vê dado de outra\", \"está lento\", auditar o app inteiro, fila GOAL.md, subagentes em paralelo, promover DEV/HML/PRD (solução, variável de ambiente, pac CLI) ou \"está pronto?\". Coordena o pipeline guiado de app novo (/pp:novo até /pp:publicar, uma sessão por etapa, ESTADO.md; depois, /pp:mudanca) e, em app existente, roteia para a skill de domínio e fecha com validadores e evidência. Não use para pergunta pontual de fórmula ou ajuste de uma tela (use `powerapps-canvas`), flow isolado (use `power-automate`), procedure ou DDL isolados (use `sql-procedures`) nem modelagem de tabela (use `dataverse`)."
argument-hint: "[novo|onde-estou|feature|investigar|auditar|promover|pronto] [alvo]"
user-invocable: true
---

# power-platform — orquestrador

Duas funções. **App novo:** coordena o pipeline guiado `/pp:*`, da ideia ao app publicado, uma
etapa por sessão, com o `ESTADO.md` dizendo onde o projeto está e qual é o próximo comando.
**App existente:** decide o que carregar, quem executa e quando está pronto num trabalho com mais
de uma camada. O conhecimento de Power Fx, YAML, flow, procedure e tabela vive nas skills de domínio.

## Regras inegociáveis

1. **Leia o projeto antes de agir** (passo 1). Não escreva tela, flow ou procedure sem trilha
   ativa e nomes do ambiente conhecidos.
   Por quê: nome de coluna e de procedure chutados foram a causa nº 1 de retrabalho nos projetos de referência.
2. **Uma etapa do pipeline por sessão, na ordem.** O `estado.py` confere a ordem e dá o próximo
   comando; você não inventa outro nem segue para a etapa seguinte na mesma conversa.
   Por quê: tudo o que a etapa seguinte precisa está no disco, e contexto limpo não arrasta decisão velha.
3. **Uma trilha de dados por projeto.** Trocar de trilha exige ADR (`assets/adr-molde.md`).
   Por quê: a trilha "congelada" foi editada e a "ativa" ficou semanas para trás.
4. **Ordem de dependência: dados → (frontend ∥ automação) → QA.** Nenhuma tela começa antes de a
   tabela/procedure dela existir e estar em `NOMES-AS-BUILT`.
   Por quê: a tela é o consumidor; escrever o consumidor primeiro fixa nomes que ainda não existem.
5. **✅ sem evidência não vale.** Toda tarefa concluída traz comando + saída + data. Evidência
   perde a validade quando o arquivo muda depois dela.
   Por quê: uma tarefa ✅ tinha regredido porque um gerador foi reescrito e apagou a correção.
6. **Verde só conta se o validador provou que acusa.** `0 erro(s)` de um validador que não leu o
   formato do arquivo é verde falso (`references/portao-final.md`).
   Por quê: um validador deu `0 erro(s)` em telas em YAML puro porque só lia blocos cercados.
7. **Gerador nunca escreve sobre gabarito.** Saída de gerador vai para `dist/`; o arquivo colado no
   designer é o gabarito.
   Por quê: regerar apagou a única evidência de ambiente que existia.
8. **Padrão decidido não se reabre em silêncio.** O que está em `references/decisoes-padrao.md`
   vale; divergir exige ADR.
   Por quê: sem registro, a tecnologia trocou várias vezes sem que ninguém soubesse o motivo.
9. **Entrega de agente é hipótese até você conferir.** Rode o validador, abra o arquivo, reproduza
   os achados mais fortes antes de seguir ou reportar.
   Por quê: já vieram como fato "o backend está vazio" e "a variável nunca é inicializada", ambos falsos.
10. **Nada de ambiente, servidor, tabela `dev*` ou GUID literal em artefato.** Variável de
    ambiente + connection reference (`references/alm-ambientes.md`).
    Por quê: fonte de desenvolvimento misturada com produção fez o KPI divergir da galeria.

## Fluxo de trabalho

### Passo 1 — Ler o projeto

1. **`ESTADO.md`** (procurado da pasta atual para cima). Existe: o projeto está no pipeline. Rode
   `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py" mostrar` antes de tudo.
2. `power-platform.config.json` (formato em `docs/CONFIG.md` do repositório do plugin): anote
   `trilha_dados`, `pastas`, `nomes_as_built`. Sem config fora do pipeline: declare "rodando com
   defaults" e proponha criar a partir de `assets/power-platform.config.exemplo.json`.
3. `00-LEIA-PRIMEIRO.md`: trilha ativa por camada. Se contradiz o config, **pare e resolva** antes
   de editar.
4. `references/decisoes-padrao.md`; a fila `GOAL.md`, se houver (confira no disco qual pasta está
   sendo editada, não só o que o documento diz); `NOMES-AS-BUILT`, se a tarefa toca dados.

### Passo 2 — Rotear

| Sinal no pedido | Faça | Quem executa |
|---|---|---|
| "quero criar um app", ideia de app, começar do zero | explique o pipeline em 4 linhas e mande rodar `/pp:novo <ideia>` | o usuário roda o comando |
| "onde parei", "qual o próximo passo", "continua" com `ESTADO.md` | `estado.py mostrar` e devolva o bloco "Próximo passo" | você |
| pedido de uma etapa (brainstorm, design, mockups, protótipo, arquitetura, construir, testar, homologar, publicar) | aponte o comando `/pp:<etapa>` numa sessão nova; o `estado.py` diz se está na ordem | o usuário roda o comando |
| lista de mudanças num app já publicado pelo kit (ou com o config do kit) | aponte `/pp:mudanca <lista>` numa sessão nova | o usuário roda o comando |
| "como faço", "qual fórmula", uma tela, YAML colável | skill `powerapps-canvas` e responda direto | você |
| galeria vazia, contador "2.000", `CountRows`, filtro de data | SQL → `powerapps-canvas` (+ `sql-procedures`); Dataverse → `dataverse` | você |
| "cola esse flow", Try/Catch, HTTP, `$batch`, log | `power-automate` (+ `powerapps-canvas` do lado do app) | você |
| procedure, DDL, coluna calculada, DBA | `sql-procedures` | você |
| tabela, Choice, Lookup, security role, `NOMES-AS-BUILT` | `dataverse` | você |
| "o número não bate", "está lento", "não atualiza" | `references/modo-investigar.md` **antes de propor código** | você |
| "usuário de uma unidade vê dado de outra" | `references/modo-investigar.md`; SQL → `power-automate` + `sql-procedures`; Dataverse → `dataverse` | você |
| feature que toca tela + flow + banco (app existente) | `references/protocolo.md` | 1 agente por camada, se compensar |
| "audita o app inteiro", ≥ 3 telas | `references/subagentes.md` + `prompts/*.md` | fan-out por disciplina |
| fila `GOAL.md` fora do pipeline, "próxima tarefa" | `references/modo-goal-fila.md` | você, em loop |
| "promove para HML/PRD", solução, `pac` | `references/alm-ambientes.md` | você + humano no ambiente |
| "está pronto?", "pode entregar?" | `references/portao-final.md` | você |
| "por que fizemos assim", lição de processo | `references/salvaguardas.md` | você |

### Passo 3 — O pipeline de app novo

Detalhe, desenho e arquivos de cada etapa: `references/pipeline.md`. Formato de banner, checkpoint e
próximo passo, igual em todas: `references/formato-saida.md`.

| # | Comando | Quem executa | Entrega |
|---|---|---|---|
| 1 | `/pp:novo` | Orquestrador | pasta, git, config, `ESTADO.md` |
| 2 | `/pp:brainstorm` | Agente Brainstorm (a sessão conversa) | requisitos, funcionalidades e MVP (`prd.md`) |
| 3 | `/pp:design` | Agente Designer Branding (a sessão conversa) | cores, fontes, componentes, identidade (`ux-design-system.md`) |
| 4 | `/pp:mockups` | subagente `pp:agente-mockups` + script | telas, navegação, loading, erros, vazios; imagens |
| 5 | `/pp:prototipo` | subagente `pp:agente-prototipo` | protótipo navegável; aprovado ou volta ao design |
| 6 | `/pp:arquitetura` | `pp:agente-arquitetura`, depois `pp:agente-sql` ∥ (trilha SQL) | modelo de dados, permissões, integrações, procedures, `GOAL.md` |
| 7 | `/pp:construir [app\|flows]` | `pp:agente-canvas` ∥ `pp:agente-automate`, um por grupo de arquivos | telas, fluxos e a integração, uma onda por sessão |
| 8 | `/pp:testar` | subagente `pp:agente-qa` | validadores + roteiro no ambiente; falha volta à construção |
| 9 | `/pp:homologar` | Orquestrador, com o usuário | UAT e aceite dos usuários reais |
| 10 | `/pp:publicar` | Orquestrador | produção, manual e guia técnico |

`/pp:progresso` mostra o painel a qualquer momento. As etapas só rodam pelo comando do usuário
(não se invocam sozinhas): fora delas, seu papel é dizer qual comando rodar.

### Passo 4 — Protocolo (app existente, tarefa com mais de um passo)

Mapear → Planejar → Executar → **Validar** → Reportar (`references/protocolo.md`). Mapear com o
comando que achou cada coisa; planejar em até 5 passos dizendo o que **não** será feito; executar na
ordem de dependência com molde e bloco canônico; validar no portão final; reportar o que mudou, como
aplicar, os avisos e o que ficou de fora.

### Passo 5 — Modos

- **Investigar** (`references/modo-investigar.md`): cadeia tela → fórmula → fonte → flow →
  procedure → dado, uma hipótese por vez, prova antes de correção.
- **Fila `GOAL.md`** (`references/modo-goal-fila.md`): próxima 🟢 cuja onda anterior fechou; numa 🔴,
  pare e diga o que fazer no ambiente. No pipeline, quem anda a fila é o `/pp:construir`.
- **Promover** (`references/alm-ambientes.md`): o que vai por colagem × por solução.

### Passo 6 — Subagentes

Do pipeline: os `pp:agente-*`, chamados pelas etapas. Fora dele: abra subagente só quando o trabalho
é **independente** e exige **leitura ampla**; escopos disjuntos, todos numa mensagem, quem delega
coleta e confere. Subagente não conversa com o usuário. Detalhe: `references/subagentes.md`.

### Passo 7 — Portão final

Rode **todos** os validadores das camadas tocadas e o checklist de `references/portao-final.md`.
Tela ou flow alterado: a prova final é colar no Studio/designer, ou registrar 🔴 para o humano.

## Referências

| Arquivo | Quando ler |
|---|---|
| `references/pipeline.md` | app novo: o desenho, as 10 etapas, as voltas, `/pp:mudanca` depois de publicado, onde fica cada arquivo |
| `references/formato-saida.md` | toda etapa `/pp:*`: banner, checkpoint, próximo passo |
| `references/decisoes-padrao.md` | passo 1, sempre: padrões decididos (A/C/T/F/B/N/P) |
| `references/brainstorm-modos.md` | `/pp:brainstorm`: os 4 modos (entrevista, pessoas, problema, mesa redonda) e as personas |
| `references/brainstorm.md` | `/pp:brainstorm`: condução e roteiro de perguntas (blocos 0 a 11) |
| `references/navegacao.md` | `/pp:design`: os 5 padrões de navegação, prévias e qual recomendar |
| `references/design-system-e-telas.md` | `/pp:design`, `/pp:mockups`: design system, inventário, moldura |
| `references/mockups.md` | `/pp:mockups`: chave OpenAI, modelo variável, spec, erros |
| `references/matriz-tecnologia.md` | `/pp:arquitetura`: Dataverse × SQL Server, Power BI, SharePoint |
| `references/carga-mockup.md` | `/pp:arquitetura`: carga mockup das tabelas (`.xlsx` para o Dataverse deduzir os tipos, `INSERT` para o SQL de DEV) e a conferência dos tipos que o Dataverse criou |
| `references/construtor-dataverse.md` | `/pp:arquitetura`, Dataverse: o flow que cria tabelas, colunas tipadas, relacionamentos e a carga mockup pela Web API (`--flow`) |
| `references/protocolo.md` | app existente: feature multi-camada, critério de saída de fase |
| `references/modo-goal-fila.md` | fila `GOAL.md`, estados, evidência, portões por onda |
| `references/modo-investigar.md` | "o número não bate", lentidão, "não atualiza" |
| `references/subagentes.md` | antes de abrir qualquer subagente; julgar a entrega (aceito, revisão, escalado) |
| `references/modelos.md` | perfis de modelo (quem pensa, quem executa), como trocar e como medir |
| `references/verificacao-visual.md` | `/pp:design`, `/pp:prototipo`: fotografar a página e olhar antes de mostrar |
| `references/alm-ambientes.md` | solução, DEV/HML/PRD, variável de ambiente, `pac`; `/pp:homologar`, `/pp:publicar` |
| `references/salvaguardas.md` | trilha, ambiente, gerador × gabarito, evidência, doc × disco, Git |
| `references/portao-final.md` | antes de dizer "pronto"; verdes falsos conhecidos |
| `prompts/ux.md` `dev.md` `performance.md` `dados.md` `flow.md` `sql.md` | auditoria de app existente (fan-out, cada um como `pp:agente-pesquisa`) |
| `assets/*-molde.*` | moldes que as etapas copiam: ideia bruta, PRD, design system, inventário, mockups, protótipo, carga mockup, arquitetura, ADR, `GOAL.md`, `00-LEIA-PRIMEIRO.md`, config; `assets/construtor-dataverse.json` é o flow construtor |

## Scripts

Rode da raiz do projeto. Sem `power-platform.config.json`, os validadores avisam que usam defaults.

| Comando | O que faz | Exit |
|---|---|---|
| `scripts/estado.py <comando> [etapa]` | estado do pipeline no `ESTADO.md`: ordem das etapas e próximo comando | 0 ok, 1 etapa fora de ordem, 2 uso ou arquivo |
| `scripts/desenhar-mockups.py <spec> --simular` | valida o spec dos mockups (M001–M007) e mostra os prompts, sem rede; sem `--simular` gera os PNGs (`OPENAI_API_KEY`) | 0, 1, 2 |
| `scripts/verificar-prototipo.py <pasta> --mockups <spec>` | contrato do protótipo HTML (V001–V013): telas, catálogo, offline, tokens, origem nos mockups | 0, 1, 2 |
| `scripts/montar-carga-mockup.py <spec> --saida <pasta>` | carga mockup (C001–C015): `.xlsx` com uma aba por tabela na ordem de carga e, no SQL, `carga-mockup.sql`; `--flow` grava o plano e o flow construtor do Dataverse (C016–C018); `--conferir <export.json>` compara os tipos criados no Dataverse com o modelo (C101–C105) | 0, 1, 2 |
| `validar-telas.py` (skill `powerapps-canvas`) | YAML das telas, PA2108, `RGBA(` literal, `;;` em YAML, versão do controle | 0, 1, 2 |
| `verificar-fluxo.py` (skill `power-automate`) | envelope, referências órfãs, `Catch` com `Skipped`, Response de 4 campos, literal de ambiente, sintomas de colagem (F001–F023) | 0, 1, 2 |
| `lint-procedure.py` (skill `sql-procedures`) | `NOCOUNT`, `XACT_ABORT`, transação, retorno com as 4 colunas | 0, 1, 2 |
| `python tools/lint_skills.py` (repositório do plugin) | padrão das skills e sanitização | 0, 1 |

Cada um tem `--help`. O que cada validador **não** cobre: `references/portao-final.md`.

## Definição de pronto (global)

- [ ] Passo 1 cumprido: `ESTADO.md` (no pipeline), config e trilha ativa citados no relatório.
- [ ] Nomes de tabela, coluna e procedure conferidos em `NOMES-AS-BUILT` (ou marcados "inferido").
- [ ] Todo validador aplicável rodou: `N erro(s), M aviso(s)` colado, com `0 erro(s)` e arquivos lidos > 0.
- [ ] Tela ou flow alterado colado no Studio/designer, ou 🔴 com o passo exato.
- [ ] Contrato app↔flow respeitado: `{status, description, id, url}`, `.Run()` em `IfError`.
- [ ] Nenhum literal de ambiente em artefato de entrega.
- [ ] Fila atualizada: cada ✅ com Evidência; `ESTADO.md` atualizado pelo `estado.py`.
- [ ] Entrega de agente conferida por você antes de entrar no relatório.
- [ ] Etapa do pipeline encerrada com o bloco "Próximo passo" do script.

## Armadilhas (as mais caras)

1. Seguir para a próxima etapa na mesma sessão, ou inventar o próximo comando: [formato-saida.md](references/formato-saida.md).
2. Rodar só um dos validadores e declarar verde: [portao-final.md](references/portao-final.md).
3. Regerar sobre o gabarito colado: [salvaguardas.md](references/salvaguardas.md).
4. Escrever tela contra o plano em vez do `NOMES-AS-BUILT`: [decisoes-padrao.md](references/decisoes-padrao.md).
5. Chamar a API de imagens sem o "pode gerar" do usuário: [mockups.md](references/mockups.md).
6. Tratar "o número não bate" como bug de fórmula antes de checar fonte e ambiente: [modo-investigar.md](references/modo-investigar.md).
7. Confiar em "✅" da fila sem Evidência: [modo-goal-fila.md](references/modo-goal-fila.md).
8. Subagente para uma tela, ou dois no mesmo arquivo: [subagentes.md](references/subagentes.md).
9. Hardcode de ambiente que impede promover: [alm-ambientes.md](references/alm-ambientes.md).
10. Terminar o turno "aguardando" subagentes: [subagentes.md](references/subagentes.md).
