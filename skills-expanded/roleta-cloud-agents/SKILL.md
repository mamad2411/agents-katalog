# AGENTS.md — contrato operacional dos agentes · Roleta Cloud

> **Fonte canônica do fluxo agêntico.** Qualquer agente (Copilot App/CLI/VS Code, coding
> agent, ou outra ferramenta que leia `AGENTS.md`) opera neste repo segundo este contrato.
> Os **invioláveis** compactos auto-carregados pelo Copilot estão em
> [`.github/copilot-instructions.md`](.github/copilot-instructions.md) — em conflito, eles
> vencem. Mudou o fluxo? Edite **este arquivo por PR** e mantenha o resumo de lá coerente.

## 1. As três camadas físicas — o que vive onde

| Camada | Papel | O que vive aqui | O que NUNCA vive aqui |
|---|---|---|---|
| **GitHub (git)** | **única fonte de verdade** | código, testes, flags na compose, instruções de agente (`AGENTS.md`, `.github/`), ADENDOs ISO (`docs/iso/adendos/`), briefs + `sprints/BOARD.md` | segredos; `graphify-out/`; estado de runtime |
| **Máquina local** | N worktrees descartáveis (1 por sessão) | worktrees `copilot-worktrees/…`, grafo `graphify-out/` local, prefs pessoais (`~/.copilot/`) | verdade do projeto — nada pode existir SÓ local |
| **Servidor Debian** | consumidor cego da `main` | systemd timer: `pull origin/main` → deploy ~2 min → healthcheck → rollback automático | edição manual, commit, ssh de agente, instrução |

**Sincronização IA-native:** agente escreve **somente via PR** → CI verde → auto-merge → o
servidor se puxa sozinho. Ninguém (humano ou agente) toca o servidor; estado de produção se
lê pelos endpoints/métricas (`/health`, `/metrics`), nunca por ssh.

## 2. Ciclo de vida de QUALQUER mudança (zero-humano)

0. **Kickoff (obrigatório):** `pwsh -File scripts/agent-kickoff.ps1` — orientação read-only
   de ~10s (main-red, PRs abertos, merges recentes, produção por endpoint, grafo, board).
   Agir sem rodar o kickoff = agir cego; não pergunte ao usuário o que o script responde.
1. **Isolamento:** 1 sessão = 1 worktree = 1 branch novo de `origin/main`. Nunca duas
   sessões no mesmo branch; nunca trabalhar no checkout principal.
2. **Contexto:** o kickoff (passo 0) já deixou o grafo fresco — consulte-o
   (`graphify query --graph graphify-out/graph.json`) antes de grep/leitura ampla.
   Grafos são artefatos derivados: nunca commitados, nunca fonte de verdade defasada.
3. **Mudança:** cirúrgica, atrás de **flag default-OFF** na compose (leitura por-chamada);
   migração Alembic **aditiva**; campo de motor novo em `save()`+`load()`+`reset_session()`.
4. **Espelho Azure:** mexeu em flags do `docker-compose.yml` → sincronize
   `deploy/azure/compose.azure.yml` (o contrato `tests/test_azure_pre_cutover.py` FALHA se divergir).
5. **Validação:** suíte verde (`pytest tests/`) + lints (`tools/lint_silent_except.py --update`
   se novo `except`). No Windows local: `--ignore=tests/test_obs_reload.py` (trava fora do CI).
6. **ISO closeout:** ADENDO = **arquivo novo** `docs/iso/adendos/AAAA-MM-DD-<slug>.md`
   (convenção no README da pasta). **NUNCA apendar em `Manutenabilidade_iso.md`** (congelado).
7. **Entrega:** commit (trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`)
   → push → **PR com base `main`** (`gh pr create --base main`; confira `baseRefName==main` no
   output ANTES de armar auto-merge — base `spr/*` não tem proteção e o auto-merge executa
   NA HORA sem CI) → **armar auto-merge** (`gh pr merge --auto --squash <nº>`). NUNCA `--admin`,
   bypass ou merge manual. Merge → deploy automático ~2 min.
8. **Ativação também é PR:** flag shadow/audit liga IMEDIATAMENTE via PR `flag/ativar-<slug>`
   (default `:-1}` na compose + adendo). Flag de comportamento liga após janela shadow limpa
   registrada em adendo. "Ação humana pendente" não existe.

## 3. Protocolo anti-conflito (sessões paralelas de agentes)

- **Lock check pré-PR:** `gh pr list` + arquivos dos PRs abertos; diff colide → serialize
  (aguarde/rebase), não abra PR paralelo.
- **Singletons são só-leitura para appends:** `Manutenabilidade_iso.md` congelado;
  `sprints/BOARD.md` só o Diretor escreve (em lote, pós-integração). Arquivo novo nunca conflita.
- **PR `CONFLICTING`/`DIRTY` é trabalho de agente:** worktree detached
  (`git worktree add ..\rc-prXX origin/<branch> --detach`) → merge `origin/main` → resolver
  mantendo os DOIS lados quando complementares → suíte → `git push origin HEAD:<branch>`.
- **Run de CI zumbi (queued >30 min):** `gh pr update-branch <nº>` re-dispara com a
  concurrency atual.
- **`main` vermelha pós-merge:** o CI abre issue `main-red` sozinho → prioridade máxima de
  qualquer agente (revert barato ~4 min, ou fix-forward por PR).
- **`schema/alembic` e estratégia (BLK-G) serializam** — nunca dois PRs paralelos nesses locks.

## 4. Lições operacionais que viraram regra

- **Workflow novo que exige secrets externos nasce GATEADO** por repo variable default-OFF
  (ex.: `if: ${{ vars.AZURE_PUBLISH_ENABLED == '1' }}`) — senão quebra a main no primeiro
  push após o merge (lição PR #64).
- **Toda flag nova na compose exige espelho Azure sincronizado no MESMO PR** (lição PR #43,
  que quebrou 2× porque flags mergearam no meio).
- **Resolver conflito preservando os dois canais** quando os lados são complementares
  (lição PR #58: payload top-level do R2 E context dict do PG-CTX coexistem).
- **INV-3:** a estratégia SEMPRE indica `APOSTAR`; veto entra como `min()` no stake, nunca
  suprime a indicação.
- **PR de sprint nasce com base `main`** (lição 2× em 16/08, PRs #71/#75): sessão executora
  criada a partir de `spr/<ID>` herda essa base no PR e o auto-merge executa NA HORA (branch
  sem proteção) — o trabalho NÃO chega à main. `gh pr create --base main` + conferir
  `baseRefName==main`; o Diretor confere de novo antes de aceitar o closeout.
- **"Mergeou ≠ implantado" é bug de esteira** (3 casos em 16/08: entrypoint systemd → conf
  nginx → extensão do operador): artefato consumido fora do git exige mecanismo de
  sincronização automática. Host: shim do SPR-D2 (a unit executa o script de `origin/main`
  a cada tick; revert cura sozinho). Extensão do operador: SPR-D4 (até lá, `git pull` no
  checkout `Desktop\Roleta Cloud` + Reload no Chrome são parte da entrega, não rodapé).
- **Suíte verde ≠ cenário testado** (lição PR #82): harness que pula cenário em silêncio
  minta — todo harness novo imprime `TOTAL n` conferido contra número duro; pulo é `SKIP`
  explícito ou `SETUP-FAIL`, nunca `PASS`.

## 5. Mapa de leitura (ordem para um agente novo)

1. `.github/copilot-instructions.md` — invioláveis (auto-carregado no Copilot).
2. Este `AGENTS.md` — contrato operacional completo.
3. `sprints/BOARD.md` + `sprints/SPR-*.md` — o que está em jogo agora.
4. `docs/iso/adendos/README.md` — evolução ISO recente (um arquivo por mudança).
5. `Manutenabilidade_iso.md` — corpo histórico/arquitetural (congelado; não apendar).
6. `fluxo_mental_24.md` (blueprint) · `evolução_24_junho.md` (metodologia de sprints).
