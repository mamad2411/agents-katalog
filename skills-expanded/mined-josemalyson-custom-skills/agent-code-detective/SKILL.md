---
name: agent-code-detective
description: Investiga e mapeia projetos open source de agentes AI (LLM agents) de forma metódica, end-to-end, como um detetive de código. Use SEMPRE que o usuário pedir para entender, estudar, fazer onboarding, mapear arquitetura, ou navegar pelo código de qualquer projeto de agente AI - mesmo que ele não use a palavra "detetive". Acione esta skill quando o usuário mencionar repositórios como OpenHands, OpenCode, Aider, Cline, Goose, Plandex, gpt-researcher, LangGraph apps, CrewAI projects, AutoGen projects, ou qualquer codebase com pasta agent/, tools/, prompts/, ou que use SDKs como anthropic, openai, langchain, langgraph, pydantic-ai. Também use quando o usuário disser "como funciona esse projeto", "quero entender o fluxo", "me ajuda a debugar", "onde começa", "qual o entry point", ou pedir para encontrar onde fica o agent loop, tools, memória, LLM client. Esta skill produz um dossiê estruturado com entry point, 6 componentes universais, 5 breakpoints sugeridos, sequência de testes progressivos, e fluxo end-to-end documentado.
---

# Agent Code Detective

Metodologia de investigação para entender qualquer projeto de agente AI em horas, não semanas.

## Princípios investigativos

1. **Hipóteses, não certezas** — toda observação é uma hipótese a ser validada por debug
2. **Siga o dado, não o código** — persiga o caminho de uma execução real
3. **O óbvio é onde mora a verdade** — `main.py`, `agent.py`, `run.py` são pistas honestas
4. **Nunca leia o código de cima para baixo** — leia seguindo a execução

## Quando usar esta skill

Acione ao receber pedidos como:
- "Me ajuda a entender o projeto X"
- "Quero estudar a arquitetura desse agente"
- "Como funciona o fluxo desse código?"
- "Onde começa a execução?"
- "Quero fazer onboarding nesse repo"
- "Me explica como esse agente está estruturado"

## A investigação em 6 fases

Cada fase tem um marco de saída. Não pule fases — cada uma depende da anterior.

### Fase 1 — Reconhecimento do território (15 min)

**Marco:** "Sei o tipo de projeto e seu vocabulário técnico"

Execute na ordem:

1. **Leia os documentos canônicos** (se existirem):
   - `README.md`
   - `ARCHITECTURE.md`
   - `CONTRIBUTING.md`
   - `docs/` (varredura do índice apenas)

2. **Analise o manifesto de dependências:**
   ```bash
   # Python
   cat pyproject.toml requirements.txt setup.py 2>/dev/null
   # Node/TS
   cat package.json
   # Rust
   cat Cargo.toml
   # Go
   cat go.mod
   ```

3. **Identifique do manifesto:**
   - Framework de agente: `langgraph`, `langchain`, `pydantic-ai`, `crewai`, `autogen`, `llama-index`, ou nenhum (custom)
   - SDK de LLM: `anthropic`, `openai`, `litellm`, `google-genai`, `mistralai`
   - Vector store: `pgvector`, `chromadb`, `faiss`, `qdrant`, `redis`, `weaviate`
   - HTTP/CLI: `fastapi`, `typer`, `click`, `express`, `axum`
   - Observabilidade: `langfuse`, `langsmith`, `opentelemetry`, `logfire`

4. **Mapeie a estrutura de pastas:**
   ```bash
   tree -L 2 -I 'node_modules|__pycache__|.git|dist|build|.venv' .
   ```
   Use o mapa de pastas comuns de agentes na seção "Referência rápida" abaixo para hipotetizar a função de cada uma.

### Fase 2 — O ponto zero: entry point (30 min)

**Marco:** "Sei exatamente onde a execução começa"

1. **Localize entry points possíveis:**
   ```bash
   # Python
   grep -rn "if __name__ == .__main__." --include="*.py"
   grep -rn "@app.command\|@click.command" --include="*.py"
   grep -rn "FastAPI()\|app = FastAPI" --include="*.py"

   # TypeScript/Node
   cat package.json | grep -E '"main"|"bin"|"scripts"'
   grep -rn "createServer\|app.listen" --include="*.ts"

   # Rust / Go
   grep -rn "fn main" --include="*.rs"
   grep -rn "func main" --include="*.go"
   ```

2. **Classifique o entry point:**
   - **CLI** — usuário roda no terminal
   - **HTTP server** — REST/WebSocket para frontends
   - **Library/SDK** — importado por outro projeto
   - **Worker/Job** — disparado por queue ou cron

3. **Encontre a função que recebe a mensagem do usuário.** Procure padrões:
   ```
   agent.run(...), agent.invoke(...), agent.stream(...)
   chat(...), process_message(...), handle_input(...)
   ```

### Fase 3 — Seguir o rastro: os 6 componentes (1h)

**Marco:** "Tenho um mapa de 1 página do fluxo principal e localizei os 6 componentes universais"

Todo projeto sério de agente tem estes 6 componentes. Localize cada um (arquivo:linha):

| # | Componente | Como encontrar |
|---|---|---|
| 1 | **Entry point** | Já feito na Fase 2 |
| 2 | **Agent loop** | `grep -rn "while.*step\|max_iterations\|max_turns"` |
| 3 | **LLM client** | `grep -rn "messages.create\|chat.completions\|generate_content"` |
| 4 | **Tool registry** | `grep -rn "@tool\|tools =\|register_tool\|FunctionTool"` |
| 5 | **Memory/State** | `grep -rn "checkpoint\|conversation_history\|vectorstore"` |
| 6 | **Prompt manager** | `grep -rn "system_prompt\|SYSTEM_PROMPT\|system="` |

**Técnica do follow-the-data:** parta do entry point e siga o que acontece com a mensagem do usuário usando Cmd+Click / Go to Definition. Anote cada salto em uma linha:

```
[entry] cli.py:42 chat() recebe input
  ↓
[runtime] agent.py:128 Agent.run() chamado
  ↓
[loop] loop.py:55 while not done, chama LLM
  ↓
[llm-client] providers/anthropic.py:89 client.messages.create()
  ↓
[response] parse stop_reason e tool_use blocks
  ↓
[tools] tool_executor.py:34 invoca cada tool
  ↓
[loop] retorna ao topo até stop_reason == "end_turn"
  ↓
[entry] resposta renderizada ao usuário
```

### Fase 4 — Vigilância ao vivo: debug (1-2h)

**Marco:** "Vi o fluxo end-to-end rodando com breakpoints e entendi cada passo"

1. **Configure ambiente de debug.** Veja `references/debug-configs.md` para templates de `launch.json` (Python e TypeScript).

   > **CRÍTICO:** habilite `justMyCode: false` (Python) ou `skipFiles: []` (Node). Sem isso, você não consegue debugar dentro de bibliotecas de terceiros — e é lá que mora metade da verdade.

2. **Coloque os 5 breakpoints universais.** Detalhes em `references/breakpoint-cheatsheet.md`:

   | # | Onde | Por quê |
   |---|---|---|
   | **BP1** | Primeira linha que recebe input no entry point | Ponto zero do trace |
   | **BP2** | Linha do `client.messages.create()` (saída para LLM) | Vê o que é enviado |
   | **BP3** | Imediatamente após retorno do LLM | Vê `stop_reason` + tool_use |
   | **BP4** | Função real da tool sendo executada | Vê parâmetros + resultado |
   | **BP5** | Linha que decide continuar ou parar o loop | Vê critério de parada |

3. **Execute a sequência progressiva de 4 testes:**

   - **Teste 1 — Sem tool:** input simples (`"diga olá"`). Loop deve passar BP2→BP3→BP5 sem tocar BP4. `stop_reason = "end_turn"`.

   - **Teste 2 — Tool única:** input que força uma tool (ex: `"liste arquivos em /tmp"`). Em BP3, observe `stop_reason = "tool_use"`. **Esta é a epifania:** o LLM **não executa nada**, ele só pede para o seu código executar.

   - **Teste 3 — Multi-tool em sequência:** input que requer 2-3 tools (ex: `"encontre o maior arquivo em /tmp e mostre as primeiras 10 linhas"`). Conte quantas vezes BP2 dispara = quantas chamadas LLM = custo.

   - **Teste 4 — Erro forçado:** quebre uma tool de propósito. Observe o `tool_result` carregando o erro de volta ao LLM e a tentativa de auto-correção.

4. **Variáveis para inspecionar em cada breakpoint:** veja `references/breakpoint-cheatsheet.md`.

### Fase 5 — Raio-X: tracing HTTP (30 min)

**Marco:** "Capturei pelo menos uma sessão completa de chamadas HTTP ao provider"

A "alma" do agente está nas requisições HTTP que saem para o LLM. Capture-as.

Escolha uma opção (detalhes em `references/tracing-setup.md`):

- **Opção A: mitmproxy** — universal, qualquer linguagem
- **Opção B: Langfuse self-hosted** — para projetos LangChain/LangGraph
- **Opção C: OpenTelemetry** — se o projeto já instrumentou

**O que extrair do trace:**
- Tamanho real do system prompt (quase sempre maior do que parece no código)
- Tokens por turno (entenda a economia)
- Latência por chamada (onde o agente "trava")
- Tool calls paralelas vs sequenciais
- Quantas iterações em média

### Fase 6 — Validar mexendo (1h)

**Marco:** "Modifiquei o projeto e previ corretamente o impacto"

Faça pelo menos 3 destes 6 experimentos. Cada um dura 5-10 minutos.

1. Adicionar `print` no início do loop — confirme quantas iterações acontecem
2. Modificar o system prompt — adicione `"sempre responda em piratês"` e observe
3. Criar uma tool nova trivial (`get_current_time()`) — registre e teste
4. Reduzir `max_iterations` pela metade — entenda o comportamento no limite
5. Trocar o modelo (Sonnet → Haiku) — observe diferenças de comportamento
6. Quebrar uma tool propositalmente — observe a recuperação

**Teste final do detetive — você responde 8 de 10 sem olhar o código?**

- Quem inicia o fluxo quando o usuário envia mensagem?
- Em que arquivo/função o LLM é chamado?
- Quantas tools existem? Onde são registradas?
- Qual o critério de parada do loop?
- Onde fica memória de curto prazo? E de longo prazo?
- O que acontece se uma tool falha?
- Qual o caminho de uma mensagem do input até a resposta?
- Quantas chamadas LLM, em média, uma tarefa típica consome?
- Onde estão os guardrails (se existirem)?
- Como observar uma execução em produção?

## Output esperado: o Dossiê

Ao final da investigação, produza um documento `docs/investigation.md` na cópia local do projeto. Template completo em `references/dossier-template.md`.

Conteúdo mínimo:
1. **Identidade** — tipo, linguagem, framework, tamanho
2. **Entry point** — arquivo, função, comando
3. **6 componentes** — arquivo:linha de cada um
4. **Fluxo end-to-end** — diagrama em texto/mermaid
5. **Padrões observados** — tipo de loop, streaming, paralelismo
6. **Pontos de atenção** — fragilidades, decisões arriscadas
7. **Pendências** — o que ainda não entendeu

## Referência rápida — pastas comuns em projetos de agente

| Pasta | O que costuma conter |
|---|---|
| `agent/` ou `agents/` | Definição do(s) agente(s), prompts, loop |
| `tools/` | Funções invocáveis pelo LLM |
| `skills/` | Pacotes de conhecimento carregados sob demanda |
| `memory/` ou `store/` | Persistência de contexto e estado |
| `llm/` ou `providers/` | Clientes para APIs (OpenAI, Anthropic) |
| `prompts/` | Templates de system prompt |
| `hooks/` ou `middleware/` | Interceptadores pré/pós tool ou LLM |
| `runtime/` ou `core/` | Engine de execução, loop, scheduler |
| `server/` ou `api/` | Interface HTTP |
| `cli/` | Interface de linha de comando |
| `evals/` | Testes de qualidade do agente |
| `guardrails/` | Validações de input/output |
| `mcp/` | Integração com Model Context Protocol |

## Heurísticas finais

**Tempo realista:**
- Projeto pequeno (≤50 arquivos): 3-4 horas
- Projeto médio (50-500 arquivos): 1 dia
- Projeto grande (500+ arquivos): 2-3 dias

**O que ignorar com segurança:**
- Pastas `tests/` (não são o fluxo de produção)
- Scripts de build, CI, deploy
- Código gerado (`generated/`, `*.pb.go`)
- Documentação de API formal (OpenAPI, RAML)

**O que NÃO ignorar:**
- `examples/` ou `cookbook/` — uso mais limpo da lib
- Testes do tipo `integration_test` — mostram fluxo real
- `CHANGELOG.md` — decisões arquiteturais recentes

**Sinal de domínio do projeto:**
Você dominou o projeto quando consegue prever, **antes de rodar**, em quantas iterações do loop um input vai parar e quais tools serão chamadas em que ordem.

## Princípio que orienta tudo

Um projeto de agente tem duas almas:
1. A do **modelo** (que não está no código, está no provider remoto)
2. A do **harness** (todo o resto)

Sua investigação é sobre o harness. O modelo é um suspeito que você nunca interrogará diretamente — só vê o que ele recebe (BP2) e o que ele devolve (BP3). É observando essa conversa que o caso se resolve.

> *"Agency comes from the model. The harness makes agency real. Your job is harness, not intelligence."*
