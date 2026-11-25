---
name: r-init
description: Inicializa um projeto para o pipeline r-spec (Spec-Driven Development). Detecta/pergunta o contexto (tipo de projeto, stack, comandos, idioma, harness), gera o AGENTS.md a partir do template, instala os subagents de review conforme o tipo de projeto e cria os esqueletos das skills de convenção numa fonte única (.agents/), e cria os espelhos (symlinks) que cada harness com pasta própria exige — .claude/ para o Claude Code e .cursor/ para o Cursor — preenchendo o que descobre e deixando placeholders claros do que cada seção precisa detalhar. Acionar UMA VEZ ao adotar o r-spec num projeto novo ou existente, antes de rodar create-prd. Não usar para criar PRD/feature (use create-prd) nem para implementar código.
---

# r-init — inicializar o projeto para o r-spec

Você prepara o projeto para o pipeline r-spec: cria o **mapa de convenções** (`AGENTS.md`), os **subagents de review** e os **esqueletos das skills de convenção** numa **fonte única** (`.agents/`), e os **espelhos (symlinks)** que cada harness com pasta própria exige — `.claude/` (Claude Code) e `.cursor/` (Cursor) — sempre preenchendo o que dá para descobrir e deixando o resto como placeholders explícitos para o usuário completar.

<critical>NÃO INVENTE stack, comandos, portas ou regras. O que você não conseguir confirmar (do repo ou perguntando) vira um placeholder `[ … ]` ou `<!-- TODO: … -->`, nunca um palpite apresentado como fato.</critical>
<critical>NÃO SOBRESCREVA arquivos existentes (AGENTS.md, CLAUDE.md, subagents, skills) sem mostrar o que mudaria e confirmar com o usuário. Em CLAUDE.md já existente, apenas ANEXE a linha apontando para o AGENTS.md.</critical>
<critical>Esta skill faz scaffolding — ela NÃO escreve o conteúdo final das convenções. Quem detalha cada seção é o usuário; seu papel é montar a estrutura e orientar o que preencher.</critical>
<critical>PERGUNTE sempre que precisar decidir algo que não dá para inferir do repo com segurança (tipo de projeto, harness, quais subagents instalar, comandos, idioma, pasta de specs). Use a ferramenta de perguntar do harness se houver; senão, pergunte em texto e aguarde a resposta. É melhor uma rodada de perguntas do que um palpite errado.</critical>

## Harnesses-alvo e princípio de layout (fonte única + symlinks)

Foco nos harnesses: **Cursor, Claude Code, Codex e Gemini/Antigravity**. O `AGENTS.md` da raiz é o mapa de convenções universal, criado uma vez (Etapa 3) e não duplicado — Cursor, Codex e Gemini/Antigravity o leem nativamente; o Claude Code o alcança pelo ponteiro `CLAUDE.md` (Etapa 4).

<critical>Os artefatos gerados (subagents e skills de convenção) têm UMA fonte da verdade em `.agents/` (formato Markdown agentskills.io). Codex, Gemini e Antigravity consomem essa fonte diretamente — nada a fazer. Os harnesses com pasta própria — **Cursor** e **Claude Code** — precisam de espelho, via **symlink** para `.agents/` (nunca cópia).</critical>

- **Fonte:** `.agents/agents/<nome>.md` (subagents) e `.agents/skills/<nome>/` (skills de convenção).

| Harness | Lê de | Mecanismo |
| ------- | ----- | --------- |
| **Codex / Gemini / Antigravity** | `.agents/` (padrão nativo) | **nada a fazer** — usa a fonte direto |
| **Cursor** | `.cursor/agents/<nome>.md` e `.cursor/rules/<nome>` | **symlink** → `../../.agents/agents/<nome>.md` e `../../.agents/skills/<nome>` |
| **Claude Code** | `.claude/agents/<nome>.md` e `.claude/skills/<nome>/SKILL.md` | **symlink** → `../../.agents/agents/<nome>.md` e `../../.agents/skills/<nome>` |

> Codex, Gemini e Antigravity funcionam no padrão `.agents/` — não precisam de pasta própria nem symlink; basta a fonte. **Cursor** e **Claude Code** exigem espelho (symlink) para a fonte. Versões globais: `~/.cursor/agents/` (Cursor) e `~/.claude/agents/` + `~/.claude/skills/` (Claude Code).

## Objetivos

1. Levantar o contexto do projeto (detectando do repo + perguntando o que faltar).
2. Gerar `AGENTS.md` na raiz a partir do template — mapa de convenções universal, lido nativamente por Cursor, Codex e Gemini/Antigravity; o Claude Code o alcança pelo ponteiro `CLAUDE.md` (Etapa 4).
3. Criar a fonte dos subagents de review em `.agents/agents/` (Codex/Gemini/Antigravity leem direto; Cursor e Claude Code recebem symlink em `.cursor/agents/` e `.claude/agents/`).
4. Criar os esqueletos das skills de convenção (uma por camada) em `.agents/skills/` (idem: Codex/Gemini/Antigravity leem direto; Cursor e Claude Code recebem symlink em `.cursor/rules/` e `.claude/skills/`).
5. Opcional: gerar um ponteiro de raiz por harness (ex.: `GEMINI.md`; para o Claude Code, `CLAUDE.md` → `@AGENTS.md`) — só onde fizer sentido. Este ponteiro cobre apenas o mapa de convenções e **não substitui** os symlinks de artefatos das Etapas 5 e 6.
6. Entregar um **roteiro de próximos passos**: exatamente o que escrever em cada arquivo/seção.

## Arquivos desta skill (references)

Use estes templates embutidos — não dependa do repositório r-spec, eles viajam com a skill:

- `references/agents-template.md` — template do `AGENTS.md` (copie e preencha).
- `references/pointer-template.md` — ponteiro mínimo por harness (ex.: `GEMINI.md`/`CLAUDE.md`) apontando para `@AGENTS.md`.
- `references/convention-skill-template.md` — esqueleto de uma skill de convenção.
- `references/frontend-reviewer.md`, `references/backend-reviewer.md`, `references/task-reviewer.md` — subagents de review prontos para adaptar.
- `references/task-executor.md` — subagente **implementador** usado pelo orquestrador `execute-tasks` (instale só se for usar essa skill).

## Fluxo de trabalho

### 1. Descobrir o contexto (antes de perguntar, inspecione)

Leia o repositório para inferir o máximo possível e **só pergunte o que não der para descobrir**:

- **Tipo de projeto:** há `frontend/` e `backend/`? só um? → `frontend` | `backend` | `fullstack`.
- **Stack:** `package.json` (deps: React/Express/Vite/Tailwind/Vitest/Playwright…), `tsconfig.json`, lockfile (npm/pnpm/yarn), runtime.
- **Comandos:** scripts do `package.json` (`dev`, `build`, `test`, `test:coverage`, `typecheck`, `lint`, `test:e2e`).
- **Harness:** existem `.agents/`, `.cursor/`, `.claude/`? A fonte é sempre `.agents/`; **Cursor** (`.cursor/`) e **Claude Code** (`.claude/`) precisam de symlink além dela.
- **Specs:** já existe pasta de specs (`tasks/`, `docs/specs/`)? Padrão do r-spec: `tasks/<NN>-<feature>/`.
- **Idioma/regras:** olhe README, configs de lint, comentários no código para inferir idioma do código e da doc.

### 2. Esclarecer (pergunte só as lacunas — obrigatório)

Com base no que faltou, pergunte de forma objetiva (use a ferramenta de perguntar do harness se houver). Confirme principalmente:

- **Tipo de projeto** (se ambíguo) — define subagents e o ramo de `execute-review`/`execute-qa`.
- **Harness(es) alvo** — Codex/Gemini/Antigravity leem a fonte `.agents/` direto; **Cursor** (symlinks em `.cursor/agents/` e `.cursor/rules/`) e **Claude Code** (symlinks em `.claude/agents/` e `.claude/skills/`) precisam de espelho além dela.
- **Comandos** que não estão claros nos scripts (subir app, E2E, typecheck) e **URL/porta local**.
- **Idioma do código e da documentação**, branch base.
- **Pasta de specs** (manter `tasks/` ou outra).
- **MCPs** disponíveis (Context7, Playwright).

> Tente uma rodada única de perguntas. Não trave o init: o que ficar indefinido vira placeholder no arquivo.

### 3. Gerar o `AGENTS.md` (raiz)

- Base: `references/agents-template.md`. Salve em `./AGENTS.md`.
- Preencha **Tipo de projeto, Stack, Comandos, Regras, URL/porta, branch** com o que descobriu/confirmou.
- Na tabela **Skills de arquitetura e padrões**, liste as skills de convenção que você vai criar na Etapa 6 (mesmos nomes).
- Na tabela **Subagents de review**, deixe só as linhas dos subagents que você instalou na Etapa 5.
- Tudo que não foi confirmado fica como `[ … ]`/`<!-- TODO -->`. Apague os blocos de comentário e exemplos que não se aplicam.

### 4. Ponteiro por harness (opcional)

Cursor, Codex e Gemini/Antigravity **leem o `AGENTS.md` da raiz nativamente** — para eles, em geral nenhum ponteiro extra é preciso. O **Claude Code não lê `AGENTS.md` por nome nativamente**: quando ele estiver em uso, crie o `CLAUDE.md` apontando para `@AGENTS.md`. Crie cada ponteiro a partir de `references/pointer-template.md`:

- **Claude Code** (se em uso) → `CLAUDE.md` apontando para `@AGENTS.md`.
- **Gemini/Antigravity** (opcional) → `GEMINI.md` apontando para `@AGENTS.md`.
- Se o arquivo **já existe**: não sobrescreva — apenas anexe a linha `Siga as convenções em @AGENTS.md` se ainda não houver.

<critical>O ponteiro cobre **só o mapa de convenções** (`AGENTS.md`). Ele **não substitui** os symlinks de subagents e skills: o Claude Code só enxerga os reviewers e as skills de convenção pelos symlinks `.claude/agents/` e `.claude/skills/` criados nas Etapas 5 e 6 (idem `.cursor/` para o Cursor).</critical>

### 5. Instalar os subagents de review (fonte em `.agents/` + symlinks)

Subagents de review rodam em **contexto isolado**. O init cria a **fonte** em `.agents/agents/`; Codex, Gemini e Antigravity a leem direto, e os harnesses-espelho (Cursor e Claude Code) recebem **symlink**. Os templates viajam embutidos em `references/`.

**5.1. Confirme com o usuário o que instalar.** Sugira pelo tipo de projeto e pergunte (a decisão é dele):

| Tipo de projeto | Sugestão padrão |
| --------------- | --------------- |
| `frontend`  | `frontend-reviewer` (+ `task-reviewer` opcional) |
| `backend`   | `backend-reviewer` (+ `task-reviewer` opcional) |
| `fullstack` | `frontend-reviewer` + `backend-reviewer` (+ `task-reviewer`) |

Pergunte também: **quais harnesses** usar e se quer o `task-reviewer` genérico além dos especializados. Lembre: Codex/Gemini/Antigravity já leem a fonte `.agents/` — Cursor e Claude Code precisam de symlink (`.cursor/agents/` e `.claude/agents/`).

> **`task-executor` (opcional):** se o projeto vai usar o orquestrador `execute-tasks` (executa todas as tasks da feature em ondas, via subagentes), instale também o subagente **implementador** `task-executor` — junto com o `task-reviewer`, que o orquestrador usa para o review de cada task. Ele não é um reviewer; é quem implementa cada task sob coordenação da skill. Use o mesmo mecanismo de fonte+symlink abaixo (já incluído nas listas).

**5.2. Localize os templates.** Ache a pasta onde esta skill foi instalada (ex.: `.agents/skills/r-init/`, `.claude/skills/r-init/`, `.cursor/rules/r-init/`, ou caminho global com `-g`); os templates ficam em `<pasta-da-skill>/references/`.

**5.3. Crie a fonte** em `.agents/agents/` copiando cada reviewer escolhido:

```bash
mkdir -p .agents/agents
cp <pasta-da-skill>/references/frontend-reviewer.md .agents/agents/frontend-reviewer.md
cp <pasta-da-skill>/references/backend-reviewer.md  .agents/agents/backend-reviewer.md
cp <pasta-da-skill>/references/task-reviewer.md      .agents/agents/task-reviewer.md
cp <pasta-da-skill>/references/task-executor.md      .agents/agents/task-executor.md   # só se for usar a skill execute-tasks
```

> Se não localizar a pasta da skill, recrie a fonte escrevendo o conteúdo do template direto em `.agents/agents/<reviewer>.md` com a ferramenta de escrita.

**5.4. Espelhe para os harnesses que precisam (Cursor, Claude Code).** Codex, Gemini e Antigravity já leem a fonte `.agents/agents/` — não faça nada para eles. Para cada harness-espelho **em uso**, crie symlinks relativos (nunca cópia — mantém o repo portátil e uma só fonte):

```bash
# Cursor (só se usar Cursor)
mkdir -p .cursor/agents
for a in frontend-reviewer backend-reviewer task-reviewer task-executor; do
  [ -f ".agents/agents/$a.md" ] || continue
  ln -sf "../../.agents/agents/$a.md" ".cursor/agents/$a.md"
done

# Claude Code (só se usar Claude Code)
mkdir -p .claude/agents
for a in frontend-reviewer backend-reviewer task-reviewer task-executor; do
  [ -f ".agents/agents/$a.md" ] || continue
  ln -sf "../../.agents/agents/$a.md" ".claude/agents/$a.md"
done
```

Confira o frontmatter exigido por cada harness (no Cursor: `name`, `description`, `model`, `readonly`, `is_background`; no Claude Code: `name`, `description`, `model`). _Edite sempre a fonte em `.agents/agents/`_ — os symlinks refletem. **Nunca copie** o arquivo para `.cursor/`/`.claude/`: cópia diverge silenciosamente da fonte.

**5.5. Adapte a fonte** ao projeto: idioma do artefato e referências de convenção (aponte para as skills de convenção e o `AGENTS.md` reais). Não sobrescreva um subagent existente sem confirmar.

### 6. Criar os esqueletos das skills de convenção (uma por camada)

Mesma estratégia dos subagents: **fonte em `.agents/skills/` + symlinks**. Para cada camada, crie a fonte `.agents/skills/<nome>/SKILL.md` a partir de `references/convention-skill-template.md`:

- **frontend** → ex.: `react-frontend-conventions` (componentes, hooks, a11y, data fetching).
- **backend** → ex.: `express-rest-conventions` (rotas, validação, erros, segurança).
- **fullstack** → crie as duas.
- Opcionais conforme a stack: `code-standards`, `<linguagem>-conventions`, `<runner>-testing`, `repo-folder-structure`, `ui-ux`.

Codex, Gemini e Antigravity leem as skills da fonte `.agents/skills/` — nada a fazer. Para cada harness-espelho **em uso**, espelhe o diretório da skill via symlink (o Claude Code lê skills de `.claude/skills/<nome>/SKILL.md`, **nunca** de `.claude/rules/`):

```bash
# Cursor (só se usar Cursor)
mkdir -p .cursor/rules
for s in react-frontend-conventions express-rest-conventions; do
  [ -d ".agents/skills/$s" ] || continue
  ln -sf "../../.agents/skills/$s" ".cursor/rules/$s"
done

# Claude Code (só se usar Claude Code)
mkdir -p .claude/skills
for s in react-frontend-conventions express-rest-conventions; do
  [ -d ".agents/skills/$s" ] || continue
  ln -sf "../../.agents/skills/$s" ".claude/skills/$s"
done
```

> Edite sempre a fonte em `.agents/skills/` — os symlinks refletem.

Preencha o `name`/`description` de cada esqueleto e o cabeçalho; deixe o corpo (Convenções, Exemplos, Antipadrões) com os placeholders `[ … ]` para o usuário escrever. **Não invente os padrões** — eles são decisão do time.

### 7. Relatar e orientar os próximos passos (obrigatório)

Liste os arquivos criados e entregue um roteiro do que o usuário precisa **escrever** agora. Para cada item, diga o que detalhar:

- **`AGENTS.md`** — confira/complete os `[ … ]` restantes: Regras do projeto (nomenclatura, tipagem, erros, logging, commits), comandos faltantes, MCPs.
- **Cada skill de convenção** (`<nome>/SKILL.md`) — escreva a seção **Convenções** com regras concretas e exemplos de código da sua stack; preencha os Antipadrões. É aqui que mora o padrão do projeto.
- **Subagents** — revise os pontos de foco e o idioma do artefato; ajuste à sua política.
- **Próxima fase:** quando o `AGENTS.md` e ao menos uma skill de convenção por camada estiverem preenchidos, rode **`create-prd`** para iniciar a primeira feature.

> Aponte explicitamente as seções com `<!-- TODO -->` que ficaram em aberto, para o usuário não esquecer nenhuma.

## Checklist de qualidade

- [ ] Contexto descoberto do repo + lacunas confirmadas com o usuário (sem palpites).
- [ ] `AGENTS.md` criado na raiz, com Tipo de projeto, Stack e Comandos preenchidos; resto como placeholder.
- [ ] Subagents de review (fonte em `.agents/agents/`) criados conforme o tipo de projeto; symlinks relativos em `.cursor/agents/` (se usar Cursor) e `.claude/agents/` (se usar Claude Code) → `../../.agents/agents/<nome>.md`.
- [ ] Skills de convenção (fonte em `.agents/skills/`) — uma por camada — criadas; symlinks relativos em `.cursor/rules/<nome>` (se usar Cursor) e `.claude/skills/<nome>` (se usar Claude Code) → `../../.agents/skills/<nome>`.
- [ ] Dentro de `.cursor/` e `.claude/` há **apenas symlinks** para `.agents/` — nenhum arquivo real (cópia). Conferir com `ls -la .claude/agents .claude/skills .cursor/agents .cursor/rules` (toda entrada deve aparecer como `->`).
- [ ] Ponteiro por harness criado só onde necessário e desejado (ex.: `CLAUDE.md` se usar Claude Code, `GEMINI.md` se usar Gemini), sem sobrescrever conteúdo existente — e ciente de que o ponteiro **não substitui** os symlinks de `.claude/`.
- [ ] Tabelas do `AGENTS.md` (skills + subagents) refletem exatamente o que foi criado.
- [ ] Relatório final com a lista de arquivos/symlinks e o roteiro do que detalhar em cada um.

<critical>NÃO INVENTE stack/comandos/regras — placeholders no lugar de palpites.</critical>
<critical>NÃO SOBRESCREVA arquivos existentes sem confirmar.</critical>
<critical>r-init monta a ESTRUTURA; o conteúdo das convenções é escrito pelo usuário.</critical>
