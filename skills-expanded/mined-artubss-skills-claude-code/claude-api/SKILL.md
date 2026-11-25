---
name: claude-api
description: "Construa, depure e otimize aplicativos com Claude API / SDK Anthropic. Aplicativos construídos com esta skill devem incluir cache de prompt. Também lida com migração de código Claude API existente entre versões de modelo (4.5 → 4.6, 4.6 → 4.7, substituições de modelo descontinuado). TRIGGER quando: código importa `anthropic`/`@anthropic-ai/sdk`; usuário solicita Claude API, SDK Anthropic ou Managed Agents; usuário adiciona/modifica/afina um recurso Claude (cache, thinking, compaction, tool use, batch, files, citations, memory) ou modelo (Opus/Sonnet/Haiku) em um arquivo; dúvidas sobre prompt caching / cache hit rate em um projeto SDK Anthropic. SKIP: arquivo importa `openai`/SDK de outro provedor, nome de arquivo como `*-openai.py`/`*-generic.py`, código agnóstico de provedor, programação geral/ML."
license: Complete terms in LICENSE.txt
---

# Construindo Aplicativos Alimentados por LLM com Claude

Esta skill ajuda você a construir aplicativos alimentados por LLM com Claude. Escolha a superfície certa com base em suas necessidades, detecte a linguagem do projeto e leia a documentação específica do idioma relevante.

## Antes de Começar

Verifique o arquivo de destino (ou, se não houver arquivo de destino, o prompt e o projeto) em busca de marcadores de provedor não-Anthropic — `import openai`, `from openai`, `langchain_openai`, `OpenAI(`, `gpt-4`, `gpt-5`, nomes de arquivo como `agent-openai.py` ou `*-generic.py`, ou qualquer instrução explícita para manter o código agnóstico de provedor. Se encontrar algum, pare e avise o usuário que esta skill produz código Claude/SDK Anthropic; pergunte se deseja alternar o arquivo para Claude ou se deseja uma implementação não-Claude. Não edite um arquivo não-Anthropic com chamadas SDK Anthropic.

## Requisito de Output

Quando o usuário solicita adicionar, modificar ou implementar um recurso Claude, seu código deve chamar Claude através de um dos seguintes:

1. **O SDK Anthropic oficial** para a linguagem do projeto (`anthropic`, `@anthropic-ai/sdk`, `com.anthropic.*`, etc.). Esta é a padrão sempre que existe um SDK oficial suportado para o projeto.
2. **HTTP bruto** (`curl`, `requests`, `fetch`, `httpx`, etc.) — apenas quando o usuário solicita explicitamente cURL/REST/HTTP bruto, o projeto é um projeto shell/cURL, ou a linguagem não possui SDK oficial.

Nunca misture os dois — não recorra a `requests`/`fetch` em um projeto Python ou TypeScript apenas porque parece mais leve. Nunca recue para shims compatíveis com OpenAI.

**Nunca adivinhe o uso do SDK.** Nomes de funções, nomes de classes, namespaces, assinaturas de método e caminhos de import devem vir de documentação explícita — seja dos arquivos `{lang}/` desta skill ou dos repositórios SDK oficiais ou links de documentação listados em `shared/live-sources.md`. Se o binding que você precisa não estiver explicitamente documentado nos arquivos da skill, WebFetch o repositório SDK relevante de `shared/live-sources.md` antes de escrever código. Não deduza APIs Ruby/Java/Go/PHP/C# a partir de shapes cURL ou do SDK de outra linguagem.

## Padrões

A menos que o usuário solicite de outra forma:

Para a versão do modelo Claude, use Claude Opus 4.7, que você pode acessar através da string de modelo exata `claude-opus-4-7`. Use adaptive thinking (`thinking: {type: "adaptive"}`) por padrão para qualquer coisa remotamente complicada. E finalmente, use streaming por padrão para qualquer solicitação que possa envolver entrada longa, saída longa ou `max_tokens` alto — evita atingir timeouts de solicitação. Use o helper `.get_final_message()` / `.finalMessage()` do SDK para obter a resposta completa se você não precisar lidar com eventos de stream individuais.

---

## Subcomandos

Se a Solicitação do Usuário na parte inferior deste prompt for uma string de subcomando vazia (sem prosa), pesquise toda tabela **Subcomandos** neste documento — incluindo qualquer uma em seções anexadas — e siga a coluna Ação correspondente diretamente. Isso permite que usuários invoquem fluxos específicos via `/claude-api <subcomando>`. Se nenhuma tabela no documento corresponder, trate a solicitação como prosa normal.

---

## Detecção de Linguagem

Antes de ler exemplos de código, determine em qual linguagem o usuário está trabalhando:

1. **Procure em arquivos de projeto** para inferir a linguagem:

   - `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` → **Python** — leia de `python/`
   - `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` → **TypeScript** — leia de `typescript/`
   - `*.js`, `*.jsx` (sem arquivos `.ts` presentes) → **TypeScript** — JS usa o mesmo SDK, leia de `typescript/`
   - `*.java`, `pom.xml`, `build.gradle` → **Java** — leia de `java/`
   - `*.kt`, `*.kts`, `build.gradle.kts` → **Java** — Kotlin usa o SDK Java, leia de `java/`
   - `*.scala`, `build.sbt` → **Java** — Scala usa o SDK Java, leia de `java/`
   - `*.go`, `go.mod` → **Go** — leia de `go/`
   - `*.rb`, `Gemfile` → **Ruby** — leia de `ruby/`
   - `*.cs`, `*.csproj` → **C#** — leia de `csharp/`
   - `*.php`, `composer.json` → **PHP** — leia de `php/`

2. **Se múltiplas linguagens detectadas** (ex: arquivos Python e TypeScript):

   - Verifique a qual linguagem a questão ou arquivo atual do usuário se relaciona
   - Se ainda ambíguo, pergunte: "Detectei arquivos Python e TypeScript. Qual linguagem você está usando para a integração Claude API?"

3. **Se a linguagem não puder ser inferida** (projeto vazio, sem arquivos de origem ou linguagem não suportada):

   - Use AskUserQuestion com opções: Python, TypeScript, Java, Go, Ruby, cURL/HTTP bruto, C#, PHP
   - Se AskUserQuestion não estiver disponível, padrão para exemplos Python e anote: "Mostrando exemplos Python. Avise se precisar de uma linguagem diferente."

4. **Se linguagem não suportada detectada** (Rust, Swift, C++, Elixir, etc.):

   - Sugira exemplos cURL/HTTP bruto de `curl/` e anote que SDKs da comunidade podem existir
   - Ofereça mostrar exemplos Python ou TypeScript como implementações de referência

5. **Se usuário precisa de exemplos cURL/HTTP bruto**, leia de `curl/`.

### Suporte de Recurso Específico da Linguagem

| Linguagem  | Tool Runner | Managed Agents | Notas                                   |
| ---------- | ----------- | -------------- | --------------------------------------- |
| Python     | Sim (beta)  | Sim (beta)     | Suporte completo — decorador `@beta_tool` |
| TypeScript | Sim (beta)  | Sim (beta)     | Suporte completo — `betaZodTool` + Zod |
| Java       | Sim (beta)  | Sim (beta)     | Beta tool use com classes anotadas      |
| Go         | Sim (beta)  | Sim (beta)     | `BetaToolRunner` no pacote `toolrunner`|
| Ruby       | Sim (beta)  | Sim (beta)     | `BaseTool` + `tool_runner` em beta      |
| C#         | Não         | Não            | SDK oficial                             |
| PHP        | Sim (beta)  | Sim (beta)     | `BetaRunnableTool` + `toolRunner()`     |
| cURL       | N/A         | Sim (beta)     | HTTP bruto, sem recursos SDK            |

> **Exemplos de código Managed Agents**: READMEs específicos da linguagem dedicados são fornecidos para Python, TypeScript, Go, Ruby, PHP, Java e cURL (`{lang}/managed-agents/README.md`, `curl/managed-agents.md`). Leia o README da sua linguagem mais os arquivos de conceito agnósticos da linguagem `shared/managed-agents-*.md`. **Agents são persistentes — crie uma vez, referencie por ID.** Armazene o ID do agent retornado por `agents.create` e passe-o para cada `sessions.create` subsequente; não chame `agents.create` no caminho de solicitação. A CLI Anthropic é uma forma conveniente de criar agents e environments de YAML versionado em controle de versão — sua URL está em `shared/live-sources.md`. Se um binding que você precisa não for mostrado no README, WebFetch a entrada relevante de `shared/live-sources.md` em vez de adivinhar. C# não possui suporte atual para Managed Agents; use requisições HTTP bruto no estilo cURL contra a API.

---

## Qual Superfície Devo Usar?

> **Comece simples.** Padrão para a camada mais simples que atende suas necessidades. Chamadas de API únicos e workflows lidam com a maioria dos casos de uso — apenas procure por agents quando a tarefa genuinamente exigir exploração aberta e orientada por modelo.

| Caso de Uso                                       | Camada          | Superfície Recomendada    | Por que                                                      |
| ------------------------------------------------- | --------------- | ------------------------- | ------------------------------------------------------------ |
| Classificação, sumarização, extração, Q&A       | Chamada LLM única| **Claude API**            | Uma solicitação, uma resposta                                |
| Processamento em lote ou embeddings              | Chamada LLM única| **Claude API**            | Endpoints especializados                                    |
| Pipelines multi-etapa com lógica controlada por código | Workflow     | **Claude API + tool use** | Você orquestra o loop                                        |
| Agent customizado com suas próprias tools       | Agent           | **Claude API + tool use** | Máxima flexibilidade                                         |
| Agent gerenciado pelo servidor com workspace     | Agent           | **Managed Agents**        | Anthropic executa o loop e hospeda a sandbox de execução de tools |
| Configurações de agent persistidas e versionadas | Agent           | **Managed Agents**        | Agents são objetos armazenados; sessions fixam a uma versão  |
| Agent de longa duração com montagens de arquivo | Agent           | **Managed Agents**        | Contêineres por-sessão, stream de eventos SSE, Skills + MCP  |

> **Nota:** Managed Agents é a escolha certa quando você quer que Anthropic execute o loop do agent *e* hospede o contêiner onde tools são executadas — operações de arquivo, bash, execução de código rodam tudo lá. Se você quer hospedar o compute você mesmo ou executar seu próprio tool runtime customizado, Claude API + tool use é a escolha certa — use o tool runner para manipulação automática de loop, ou o loop manual para controle fino (gates de aprovação, logging customizado, execução condicional).

> **Provedores terceirizados (Amazon Bedrock, Google Vertex AI, Microsoft Foundry):** Managed Agents **não está disponível** em Bedrock, Vertex ou Foundry. Se você estiver implementando através de qualquer provedor terceirizado, use **Claude API + tool use** para todos os casos de uso — incluindo aqueles onde Managed Agents seria a superfície recomendada.

### Árvore de Decisão

```
O que seu aplicativo precisa?

0. Você está implementando através de Amazon Bedrock, Google Vertex AI, ou Microsoft Foundry?
   └── Sim → Claude API (+ tool use para agents) — Managed Agents é somente 1P.
   Não → continuar.

1. Chamada LLM única (classificação, sumarização, extração, Q&A)
   └── Claude API — uma solicitação, uma resposta

2. Você quer que Anthropic execute o loop do agent e hospede um
   contêiner por-sessão onde Claude executa tools (bash, operações de arquivo, código)?
   └── Sim → Managed Agents — sessions gerenciado pelo servidor, configurações de agent persistidas,
       stream de eventos SSE, Skills + MCP, montagens de arquivo.
       Exemplos: "agent de codificação stateful com workspace por tarefa",
                 "agent de pesquisa de longa duração que faz stream de eventos para uma UI",
                 "agent com configuração persistida e versionada usado em várias sessions"

3. Workflow (multi-etapa, orquestrado por código, com suas próprias tools)
   └── Claude API com tool use — você controla o loop

4. Agent aberto (modelo decide sua própria trajetória, suas próprias tools, você hospeda o compute)
   └── Loop agentic Claude API (máxima flexibilidade)
```

### Devo Construir um Agent?

Antes de escolher a camada de agent, verifique todos os quatro critérios:

- **Complexidade** — A tarefa é multi-etapa e difícil de especificar totalmente antecipadamente? (ex: "transformar este design doc em um PR" vs. "extrair o título deste PDF")
- **Valor** — O resultado justifica custo e latência maiores?
- **Viabilidade** — Claude é capaz neste tipo de tarefa?
- **Custo do erro** — Erros podem ser capturados e recuperados? (testes, review, rollback)

Se a resposta for "não" para qualquer um destes, mantenha-se em uma camada mais simples (chamada única ou workflow).

---

## Arquitetura

Tudo passa por `POST /v1/messages`. Tools e restrições de output são recursos deste endpoint único — não APIs separadas.

**Tools definidas pelo usuário** — Você define tools (via decoradores, schemas Zod, ou JSON bruto), e o tool runner do SDK manipula chamar a API, executar suas funções e fazer loop até Claude terminar. Para controle total, você pode escrever o loop manualmente.

**Tools do lado do servidor** — Tools hospedadas por Anthropic que rodam na infraestrutura Anthropic. Execução de código é totalmente do lado do servidor (declare em `tools`, Claude executa automaticamente). Uso de computador pode ser hospedado no servidor ou self-hosted.

**Outputs estruturados** — Restringe o formato de resposta da Messages API (`output_config.format`) e/ou validação de parâmetro de tool (`strict: true`). A abordagem recomendada é `client.messages.parse()` que valida respostas contra seu schema automaticamente. Nota: o parâmetro antigo `output_format` está descontinuado; use `output_config: {format: {...}}` em `messages.create()`.

**Endpoints de suporte** — Batches (`POST /v1/messages/batches`), Files (`POST /v1/files`), Token Counting, e Models (`GET /v1/models`, `GET /v1/models/{id}` — descoberta ao vivo de capacidade/janela de contexto) alimentam ou suportam solicitações Messages API.

---

## Modelos Atuais (cacheado: 2026-04-15)

| Modelo             | ID do Modelo        | Contexto       | Input $/1M | Output $/1M |
| ----------------- | ------------------- | -------------- | ---------- | ----------- |
| Claude Opus 4.7   | `claude-opus-4-7`   | 1M             | $5.00      | $25.00      |
| Claude Opus 4.6   | `claude-opus-4-6`   | 1M             | $5.00      | $25.00      |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M             | $3.00      | $15.00      |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K           | $1.00      | $5.00       |

**SEMPRE use `claude-opus-4-7` a menos que o usuário explicitamente nomeie um modelo diferente.** Isto é não-negociável. Não use `claude-sonnet-4-6`, `claude-sonnet-4-5`, ou qualquer outro modelo a menos que o usuário literalmente diga "use sonnet" ou "use haiku". Nunca faça downgrade por custo — essa é decisão do usuário, não sua.

**CRÍTICO: Use apenas as strings de ID de modelo exatas da tabela acima — elas estão completas como estão. Não adicione sufixos de data.** Por exemplo, use `claude-sonnet-4-5`, nunca `claude-sonnet-4-5-20250514` ou qualquer outra variante com sufixo de data que você possa se lembrar de dados de treinamento. Se o usuário solicita um modelo antigo não na tabela (ex: "opus 4.5", "sonnet 3.7"), leia `shared/models.md` para o ID exato — não construa um você mesmo.

Uma nota: se qualquer das strings de modelo acima parecerem desconhecidas para você, isso é esperado — apenas significa que foram lançadas depois do seu corte de dados de treinamento. Fique certo que são modelos reais; não nos burlariamos assim.

**Busca de capacidade ao vivo:** A tabela acima é cacheada. Quando o usuário pergunta "qual é a janela de contexto para X", "X suporta vision/thinking/effort", ou "quais modelos suportam Y", consulte a API de Modelos (`client.models.retrieve(id)` / `client.models.list()`) — veja `shared/models.md` para a referência de campo e exemplos de filtro de capacidade.

---

## Thinking & Effort (Referência Rápida)

**Opus 4.7 — Apenas adaptive thinking:** Use `thinking: {type: "adaptive"}`. `thinking: {type: "enabled", budget_tokens: N}` retorna um 400 em Opus 4.7 — adaptive é o único modo on. `{type: "disabled"}` e omitir `thinking` ambos funcionam. Parâmetros de amostragem (`temperature`, `top_p`, `top_k`) também são removidos e retornarão 400. Veja `shared/model-migration.md` → Migrating to Opus 4.7 para a lista completa de mudanças quebradas.
**Opus 4.6 — Adaptive thinking (recomendado):** Use `thinking: {type: "adaptive"}`. Claude decide dinamicamente quando e quanto pensar. Sem `budget_tokens` necessário — `budget_tokens` está descontinuado em Opus 4.6 e Sonnet 4.6 e não deve ser usado para código novo. Adaptive thinking também ativa automaticamente interleaved thinking (sem header beta necessário). **Quando o usuário pedir "extended thinking", um "thinking budget", ou `budget_tokens`: sempre use Opus 4.7 ou 4.6 com `thinking: {type: "adaptive"}`. O conceito de um token budget fixo para thinking está descontinuado — adaptive thinking o substitui. NÃO use `budget_tokens` para novo código 4.6/4.7 e NÃO mude para um modelo antigo.** *Carve-out de migração gradual:* `budget_tokens` ainda é funcional em Opus 4.6 e Sonnet 4.6 como uma válvula de escape transicional — se você estiver migrando código existente e precisa de um teto de token rígido antes de ter ajustado `effort`, veja `shared/model-migration.md` → Transitional escape hatch. Nota: este carve-out **não** se aplica a Opus 4.7 — `budget_tokens` está totalmente removido lá.
**Parâmetro Effort (GA, sem header beta):** Controla profundidade de thinking e gasto de token geral via `output_config: {effort: "low"|"medium"|"high"|"max"}` (dentro de `output_config`, não top-level). Padrão é `high` (equivalente a omitir). `max` é apenas Opus-tier (Opus 4.6 e posterior — não Sonnet ou Haiku). Opus 4.7 adiciona `"xhigh"` (entre `high` e `max`) — a melhor configuração para codificação e uso agentic na maioria das vezes em 4.7, e o padrão em Claude Code; use um mínimo de `high` para a maioria do trabalho sensível à inteligência. Funciona em Opus 4.5, Opus 4.6, Opus 4.7, e Sonnet 4.6. Gerará erro em Sonnet 4.5 / Haiku 4.5. Em Opus 4.7, effort importa mais que em qualquer Opus anterior — re-ajuste ao migrar. Combine com adaptive thinking para os melhores tradeoffs custo-qualidade. Menor effort significa fewer e mais-consolidadas chamadas de tool, menos preâmbulo e confirmações mais curtas — `high` é frequentemente o sweet spot equilibrando qualidade e eficiência de token; use `max` quando correção importa mais que custo; use `low` para subagencts ou tarefas simples.

**Opus 4.7 — conteúdo thinking omitido por padrão:** Blocos `thinking` ainda fazem stream mas seu texto está vazio a menos que você opte com `thinking: {type: "adaptive", display: "summarized"}` (padrão é `"omitted"`). Mudança silenciosa — sem erro. Se você faz stream de reasoning para usuários, o padrão parece uma longa pausa antes de output; defina `"summarized"` para restaurar progresso visível.

**Task Budgets (beta, Opus 4.7):** `output_config: {task_budget: {type: "tokens", total: N}}` diz ao modelo quantos tokens ele tem para um loop agentic completo — ele vê uma contagem regressiva rodando e se auto-modera (mínimo 20,000; header beta `task-budgets-2026-03-13`). Distinto de `max_tokens`, que é um teto por-resposta forçado que o modelo não está ciente. Veja `shared/model-migration.md` → Task Budgets.

**Sonnet 4.6:** Suporta adaptive thinking (`thinking: {type: "adaptive"}`). `budget_tokens` está descontinuado em Sonnet 4.6 — use adaptive thinking em vez disso.

**Modelos antigos (apenas se explicitamente solicitado):** Se o usuário especificamente pede Sonnet 4.5 ou outro modelo antigo, use `thinking: {type: "enabled", budget_tokens: N}`. `budget_tokens` deve ser menor que `max_tokens` (mínimo 1024). Nunca escolha um modelo antigo apenas porque o usuário menciona `budget_tokens` — use Opus 4.7 com adaptive thinking em vez disso.

---

## Compaction (Referência Rápida)

**Beta, Opus 4.7, Opus 4.6, e Sonnet 4.6.** Para conversas de longa duração que podem exceder a janela de contexto de 1M, ative compaction do lado do servidor. A API automaticamente sumariza contexto anterior quando se aproxima do limiar de ativação (padrão: 150K tokens). Requer header beta `compact-2026-01-12`.

**Crítico:** Anexe `response.content` (não apenas o texto) de volta para suas messages a cada turno. Blocos de compaction na resposta devem ser preservados — a API os usa para substituir o histórico compactado na próxima solicitação. Extrair apenas a string de texto e anexar isso silenciosamente perderá o estado de compaction.

Veja `{lang}/claude-api/README.md` (seção Compaction) para exemplos de código. Documentação completa via WebFetch em `shared/live-sources.md`.

---

## Prompt Caching (Referência Rápida)

**Prefix match.** Qualquer mudança de byte em qualquer lugar no prefixo invalida tudo após. Ordem de render é `tools` → `system` → `messages`. Mantenha conteúdo estável primeiro (system prompt congelado, lista de tools determinística), coloque conteúdo volátil (timestamps, IDs por-solicitação, perguntas variantes) após o último breakpoint de `cache_control`.

**Auto-caching de top-level** (`cache_control: {type: "ephemeral"}` em `messages.create()`) é a opção mais simples quando você não precisa de colocação de breakpoint fino. Max 4 breakpoints por solicitação. Prefixo cacheable mínimo é ~1024 tokens — prefixos mais curtos silenciosamente não farão cache.

**Verifique com `usage.cache_read_input_tokens`** — se for zero em solicitações repetidas, um invalidador silencioso está em trabalho (`datetime.now()` em system prompt, JSON não-ordenado, conjunto de tools variante).

Para padrões de colocação, orientação arquitetural, e checklist de auditoria de invalidador silencioso: leia `shared/prompt-caching.md`. Sintaxe específica da linguagem: `{lang}/claude-api/README.md` (seção Prompt Caching).

---

## Managed Agents (Beta)

**Managed Agents** é uma terceira superfície: agents stateful gerenciado pelo servidor com execução de tool hospedada por Anthropic. Você cria uma configuração de Agent persistida e versionada (`POST /v1/agents`), depois inicia Sessions que a referenciam. Cada sessão provisiona um contêiner como workspace do agent — bash, operações de arquivo, e execução de código rodam lá; o loop do agent mesmo roda na camada de orquestração de Anthropic e age no contêiner via tools. A sessão faz stream de eventos; você envia messages e resultados de tools de volta.

**Managed Agents é somente first-party.** Não está disponível em Amazon Bedrock, Google Vertex AI, ou Microsoft Foundry. Para agents em provedores terceirizados, use Claude API + tool use.

**Fluxo obrigatório:** Agent (uma vez) → Session (a cada execução). `model`/`system`/`tools` vivem no agent, nunca na session. Veja `shared/managed-agents-overview.md` para o guia de leitura completo, headers beta, e armadilhas.

**Headers beta:** `managed-agents-2026-04-01` — o SDK define isso automaticamente para todas chamadas `client.beta.{agents,environments,sessions,vaults,memory_stores}.*`. API Skills usa `skills-2025-10-02` e Files API usa `files-api-2025-04-14`, mas você não precisa passar explicitamente aqueles para endpoints fora de `/v1/skills` e `/v1/files`.

**Subcomandos** — invoque diretamente com `/claude-api <subcomando>`:

| Subcomando | Ação |
|---|---|
| `managed-agents-onboard` | Guie o usuário através da configuração de um Managed Agent do zero. **Leia `shared/managed-agents-onboarding.md` imediatamente** e siga seu script de interview: mental model → know-or-explore branch → template config → session setup → emit code. Não resuma — execute o interview. |

**Guia de leitura:** Comece com `shared/managed-agents-overview.md`, depois arquivos tópicos `shared/managed-agents-*.md` (core, environments, tools, events, outcomes, multiagent, webhooks, memory, client-patterns, onboarding, api-reference). Para Python, TypeScript, Go, Ruby, PHP, e Java, leia `{lang}/managed-agents/README.md` para exemplos de código. Para cURL, leia `curl/managed-agents.md`. **Agents são persistentes — crie uma vez, referencie por ID.** Armazene o ID do agent retornado por `agents.create` e passe-o para cada `sessions.create` subsequente; não chame `agents.create` no caminho de solicitação. A CLI Anthropic é uma forma conveniente de criar agents e environments de YAML versionado em controle de versão (URL em `shared/live-sources.md`). Se um binding que você precisa não for mostrado no README da linguagem, WebFetch a entrada relevante de `shared/live-sources.md` em vez de adivinhar. C# não possui suporte atual para Managed Agents; use HTTP bruto de `curl/managed-agents.md` como referência.

**Quando o usuário quer configurar um Managed Agent do zero** (ex: "como começo", "me guie através de criar um", "configure um novo agent"): leia `shared/managed-agents-onboarding.md` e execute seu interview — mesmo fluxo que o subcomando `managed-agents-onboard`.

**Quando o usuário pergunta "como escrevo o código cliente para X":** procure por `shared/managed-agents-client-patterns.md` — cobre reconnect de stream lossless, gate queued/processed de `processed_at`, interrupt, round-trip de `tool_confirmation`, gate de break idle/terminated correto, race de status pós-idle, ordenação stream-first, armadilhas de file-mount, mantendo credenciais host-side via custom tools, etc.

---

## Guia de Leitura

Depois de detectar a linguagem, leia os arquivos relevantes baseado no que o usuário precisa:

### Referência Rápida de Tarefa

**Classificação de texto único/sumarização/extração/Q&A:**
→ Leia apenas `{lang}/claude-api/README.md`

**UI de chat ou exibição de resposta em tempo real:**
→ Leia `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`

**Conversas de longa duração (pode exceder janela de contexto):**
→ Leia `{lang}/claude-api/README.md` — veja seção Compaction
**Migrando para um modelo mais novo (Opus 4.7 / Opus 4.6 / Sonnet 4.6) ou substituindo um modelo descontinuado:**
→ Leia `shared/model-migration.md`
**Prompt c