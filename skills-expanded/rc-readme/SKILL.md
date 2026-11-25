---
name: rc-readme
description: "Writes or refreshes a project README from evidence in the codebase. Use to generate or update one. Do not use for API specs or changelogs."
model: sonnet
effort: medium
---

# README

Produce a `README.md` that reflects what the code actually does — never invented or aspirational content. Every claim must trace back to a file you read. This skill is standalone and stack-agnostic; it detects the project's technology before writing.

## Required Inputs

- None. Operates on the current repository root.
- Optional: a target path other than `README.md`, or specific sections to scope the update to.

## Workflow

1. Gather documentation context.
   - Read, when present: the existing `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, any `docs/` overview, and architecture notes or ADRs under `docs/`, `.techdocs/`, or `.rc/tasks/*/adrs/` (in monorepos there may be more than one `.rc` directory — scan each one, skipping `node_modules`, `.git`, `vendor`, and `_archived/`).
   - The existing README defines the structure and tone to preserve. Keep valid sections; only rewrite what is stale.

2. Detect the stack and analyze the codebase. Read real sources — do not guess.
   - **Manifest and stack**: inspect `go.mod`, `package.json`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, `*.csproj`, `Gemfile`, etc. Record real dependency versions, the language, frameworks, and the package/registry.
   - **Entry points and public API**: the binary `main`, exported packages, library entry, or CLI commands.
   - **HTTP / RPC surface**: route definitions, handlers, controllers, or service files. Capture method, path, and the request/response contract from the validation layer (schemas, DTOs, structs).
   - **Configuration**: environment variables and config files — which are required vs optional, and defaults.
   - **Scripts and tasks**: real commands from `package.json` scripts, `Makefile`, `Taskfile`, `justfile`, etc.
   - **Persistence**: migrations or schema files — tables/collections and their shape.
   - **CI/CD**: workflows under `.github/workflows/` or equivalent — triggers and deploy targets.
   - **Project structure**: map the real directory tree (Glob), describing each significant directory's purpose.
   - For an unfamiliar framework, spawn an Agent to map the relevant files rather than guessing conventions.

3. Compare and find gaps. Cross-check the existing README against the data from step 2: outdated versions, missing or removed endpoints, stale env vars, wrong commands, undocumented new features, and incorrect structure. List what must change.

4. Rewrite `README.md` using only verified data. Adapt the section set to the project type (library, service, CLI, monorepo); include the sections that apply, in this order:
   - **Title** — matches the package/repo name.
   - **Short description** — one line, under ~120 characters, says what it does.
   - **Badges** — 2–4 key badges (build, coverage, version, license) via shields.io; preserve existing ones and update values. Skip if the project has none and none are warranted.
   - **Table of Contents** — when the README exceeds ~100 lines.
   - **Overview / Background** — what it is and why it exists.
   - **Architecture** — layers and data flow; keep/refresh existing diagrams.
   - **Install / Quick Start** — prerequisites and setup, with copy-pasteable commands.
   - **Usage** — the primary way to run it, with a real example.
   - **API / Endpoints** — when a service: method, path, and request/response shape. Link to `openapi.yaml` or the Postman collection if present instead of duplicating exhaustively.
   - **Configuration** — env var table: variable, description, required, default.
   - **Project structure** — the real tree with per-directory purpose.
   - **Scripts / Commands** — the real task list.
   - **Testing** — runner, conventions, command.
   - **Deploy** — environments and pipelines, when applicable.
   - **Contributing** — link to `CONTRIBUTING.md` / `CLAUDE.md` rules when present.
   - **License** — always last.

5. Validate before finishing. Confirm: every documented endpoint, command, env var, and version traces to a file you read; no section was invented; links and commands are real; the structure matches the actual tree. Mark genuinely undeterminable details as `[TODO]` rather than fabricating them.

6. Verify and report.
   - Use installed `rc-code-review` before claiming completion.
   - Present a summary: sections updated, the most relevant changes (new endpoints, version bumps, added env vars), and sections left unchanged.

## Critical Rules

- Match the language and tone of the existing README. If the repo writes docs in another language, follow it.
- Do not modify any source code. This skill only writes the README (and only the target file).

## Error Handling

- If no manifest or recognizable stack can be found, report what was inspected and ask the user to confirm the project type before writing.
- If the codebase is too large to analyze fully, document the core surfaces, note what was not covered, and do not imply full coverage.
- If the target file cannot be written, stop and report the filesystem error.

## Escrevendo/aprimorando um README à mão — templates e guidance

Use este modo quando o pedido é sobre redigir ou revisar um README manualmente (sem necessariamente varrer todo o codebase), ou quando o foco é adequar o conteúdo à audiência certa. READMEs respondem às perguntas que a audiência vai ter — um contribuidor de projeto OSS precisa de contexto diferente de um "eu do futuro" abrindo uma pasta de config.

**Sempre pergunte:** Quem vai ler isso, e o que essa pessoa precisa saber?

### Passo 1: identificar a tarefa

Pergunte: "Em qual tarefa de README você está trabalhando?"

| Tarefa | Quando |
|--------|--------|
| **Criar** | Projeto novo, ainda sem README |
| **Adicionar** | Precisa documentar algo novo |
| **Atualizar** | Capacidades mudaram, conteúdo está desatualizado |
| **Revisar** | Checar se o README ainda está preciso |

### Passo 2: perguntas específicas da tarefa

**Criando o README inicial:**
1. Que tipo de projeto é? (ver Tipos de projeto abaixo)
2. Que problema isso resolve, em uma frase?
3. Qual o caminho mais rápido até "funcionando"?
4. Algo notável para destacar?

**Adicionando uma seção:**
1. O que precisa ser documentado?
2. Onde isso deve entrar na estrutura existente?
3. Quem mais precisa dessa informação?

**Atualizando conteúdo existente:**
1. O que mudou?
2. Leia o README atual, identifique seções desatualizadas.
3. Proponha edições específicas.

**Revisando/atualizando:**
1. Leia o README atual.
2. Confira contra o estado real do projeto (package.json, arquivos principais, etc.).
3. Sinalize seções desatualizadas.
4. Atualize a data de "última revisão", se existir.

### Passo 3: sempre pergunte

Depois de redigir, pergunte: **"Tem mais alguma coisa para destacar ou incluir que eu possa ter deixado passar?"**

### Tipos de projeto

| Tipo | Audiência | Seções-chave | Template |
|------|-----------|--------------|----------|
| **Open Source** | Contribuidores, usuários no mundo todo | Install, Usage, Contributing, License | [oss-template](references/oss-template.md) |
| **Pessoal** | Você do futuro, visitantes de portfólio | O que faz, Stack, Aprendizados | [personal-template](references/personal-template.md) |
| **Interno** | Colegas de time, novos contratados | Setup, Arquitetura, Runbooks | [internal-template](references/internal-template.md) |
| **Config** | Você do futuro (confuso) | O que tem aqui, Por quê, Como estender, Pegadinhas | [xdg-config-template](references/xdg-config-template.md) |

**Pergunte ao usuário** se não estiver claro. Não assuma o padrão OSS para tudo. Antes de finalizar, cheque o [guia de estilo e erros comuns](references/style-guide.md).

### Seções essenciais (todos os tipos)

Todo README precisa, no mínimo:

1. **Nome** — título autoexplicativo.
2. **Descrição** — o quê + por quê em 1-2 frases.
3. **Uso** — como usar (exemplos ajudam).
