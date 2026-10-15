---
name: fluxline-build
description: OBRIGATÓRIA em qualquer escrita de código. Fatias com TDD (RED→GREEN→REFACTOR), atualiza todo/plan com [x], modo fase-a-fase (padrão) ou run completa. Use sempre que for editar código de comportamento. Não use quando a mudança é só doc/markdown/config cosmética sem runtime. Não planeja nem reescreve a spec. Quarta porta da cadeia fluxline-*.
---

# Fluxline Build

## Obrigatória — qualquer implementação

Porta de implementação do Fluxline. TDD no núcleo; UI, API, git, debug, simplify, etc. entram como **refs sob demanda**.

**Antes de alterar código de comportamento:**

1. Ler **este** `SKILL.md` (sempre).
2. Abrir só as **refs da fatia** (tabela §8) — nunca a pasta inteira no boot.
3. Ciclo: TDD → verify → (commit se couber) → **marcar todo/plan** → próxima / re-review.

Pular esta skill ou a ref do domínio da fatia = fora do processo.

**Mexeu em código de comportamento → build.** Sem exceção. O que **escala** é a cerimônia, não a obrigatoriedade:

| Fatia | O que paga |
|---|---|
| Feature, fix, refactor, simplify, migration, contrato | Ciclo completo: RED→GREEN→REFACTOR, verify do repo, `[x]` no todo/plan |
| **XS** — uma linha, constante, rename com efeito, typo em código que roda | Teste que prova (prove-it se for bug) + verify. Sem todo/plan se a run não existe |
| Doc, markdown, config cosmética sem runtime | **Fora da build** |

Uma constante e uma feature não custam o mesmo — mas nenhuma das duas entra sem prova.

**Não faz:** interview, spec, plan do zero, review formal de merge (isso é `fluxline-review` — se o handoff trouxe findings, **implementa** o remédio aqui; não re-julga no lugar da review).  
Cadeia: `interview → spec → plan → **build** → review` (e **review → build → review** em Request changes).

**Discovery:** esta cadeia é `fluxline-*` do começo ao fim — não substituir porta por skill de outro pack.

| | |
|---|---|
| **Começa** | Todo/plan (preferido) **ou** handoff de review (findings) + este skill + refs da fatia |
| **Termina** | Task(s)/fixes com aceite + DoD no que couber + **todo/plan marcados** se houver → handoff **`fluxline-review`** (todo zerado **ou** fixes de review concluídos) |

---

## 0 — Gate e buracos (Q + RECOMENDO)

1. Localize `docs/fluxline/plan/todo-fase-N-<slug>-<nome-curto>.md` (+ plan + spec, **mesmo id**).  
   **Handoff de review:** leia `docs/fluxline/review/review-fase-…` (ou o bloco HANDOFF no chat) e trate Critical/Required como escopo da fatia — TDD/prove-it em cada fix.
2. Sem todo/plan e o humano não pediu build avulso (nem handoff de review) → recomende `fluxline-plan`.
3. **Uma task por vez** no modo padrão (ver §1). Findings de review = uma fatia por concern (ou agrupar só se o mesmo arquivo/mesmo teste).
4. Buraco no todo/spec/código que trava a fatia → **não chute**:

```
Q: <decisão>
RECOMENDO: <opção> — <1 linha de porquê>
(ok / outra?)
```

| Tipo de buraco | Ação |
|---|---|
| Intenção / sucesso / fora frouxos | Devolve `fluxline-spec` ou `fluxline-interview` |
| Desenho pontual (nome de endpoint, lib, flag) | Q + RECOMENDO; com ok, registra e segue |
| “Tanto faz” / “o que achar” | Cravar a rec, anotar no commit/todo se relevante |

Proibido lista “Open Questions” no código ou no todo.  
“Seems right” **não** é done — prova com teste.

---

## 1 — Modos de execução

Declare o modo no início da run (1 linha). Default = **fase a fase**.

### Modo A — Fase a fase (padrão)

1. Executa **uma fase** do plan (grupo de tasks até o próximo **Checkpoint**), ou, se o plan não tiver fases, **uma task** do todo.  
   Em handoff de review: **um concern** (ou grupo mínimo) por parada, salvo modo B / “aplica todos os findings”.
2. Marca `[x]` no todo (e no plan se houver checklist de fase/checkpoint) — se for task de plan.
3. **Para** e reporta: o que fechou, paths, testes rodados.
4. Ainda há tasks de plan → só continua com ok do humano (ou “pode seguir”).
5. **Todo zerado** (tasks de plan) **ou** **todos os Critical/Required do handoff de review fechados** → handoff **`fluxline-review`** (id + paths; se foi fix de review, diga “re-review”) — não invente work extra.

### Modo B — Run completa (todas as fases)

Só se o humano pedir: “faz o todo”, “todas as fases”, “run completa”, “não para entre tasks”, “aplica todos os findings”.

1. Percorre **todas** as tasks do todo na ordem (respeitando deps e checkpoints internos) **ou** todos os findings Critical/Required do handoff.
2. Em cada checkpoint do plan: roda verificação da fase; se vermelho, **para** e reporta (não empurra lixo adiante).
3. Marca `[x]` a cada task/checkpoint concluído (**sem perguntar** se pode marcar).
4. No fim: handoff `fluxline-review` + paths (re-review se veio de findings).

Se o modo não foi dito → **A**.

---

## 2 — Atualizar todo e plan (obrigatório, sem perguntar)

Fonte de verdade do progresso = arquivos em disco, não o chat.

| Arquivo | O que marcar |
|---|---|
| `todo-fase-N-….md` | `- [ ]` → `- [x]` em **Aceite**, **Verificação** e na task quando a task inteira fechou |
| `plan-fase-N-….md` | Checkboxes de fase/checkpoint quando a fase fechou |

**Quando:** logo após a task/fase passar nos checks — **na mesma resposta**, sem “quer que eu marque?”.

**Como:**
- Task concluída: título/item da task e itens de aceite/verificação com `[x]`.
- Checkpoint do plan: itens do checkpoint com `[x]` só se de fato rodou (testes/build/fluxo).
- Não marque no chute: se verificação falhou, deixa `[ ]` e reporta o erro.
- Fix só de review (todo já zerado): não invente tasks fantasmas; reporte o que fechou e handoff re-review.

Se o todo estiver só em chat (build avulso sem arquivo) → ao fechar, **crie/atualize** o `todo-fase-…` se a run tiver id; senão liste o progresso em 3 linhas no chat e diga que falta arquivo de plan.

---

## 3 — Descobrir o stack de teste (antes do primeiro teste)

Comandos não são universais. Antes do RED:

- Manifest do projeto (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, Gradle/Maven, `Makefile`…)
- Wrappers do repo (`./gradlew`, `make test`, scripts de CI)
- Como rodar **um** teste focado vs suite inteira
- Onde os testes moram e o padrão dos vizinhos
- README / CI = o que realmente gateia merge

Focado no loop; suite completa ao fechar task/fase.  
**Nunca** assumir `npm test` sem checar o repo.

Pirâmide, anti-patterns e sintaxe JS/TS de exemplo: `references/test.md` (sob demanda).  
**Web / UI no browser:** `references/playwright.md` — Playwright default; screenshot + leitura visual pela IA.

Se a fatia é user-visible no browser: descubra também config/scripts Playwright do repo (ou E2E equivalente já adotado).

---

## 4 — Ciclo da fatia (TDD integrado)

```
RED → GREEN → REFACTOR → Verify repo → (Commit se couber) → Marcar todo/plan → próxima
```

### RED
Escreva o teste **primeiro**. Tem que **falhar**. Teste que passa de primeira não prova nada.

### GREEN
Mínimo de código para passar. Sem over-engineer.

### REFACTOR
Com verde: naming, extrair, sem mudar comportamento. Rode o teste de novo.  
Passo de clareza maior (“simplifica”, nesting, dead code, over-abstraction) → `references/simplify.md` (uma mudança + testes; não misturar com feature).

### Prove-it (bugs)
**Não** comece pelo fix. Ordem:

1. Teste que **reproduz** o bug (falha)  
2. Fix  
3. Teste passa  
4. Suite / focados relevantes (sem regressão)

### Qualidade mínima do teste
- **Estado, não interação** — outcome, não “chamou mock X” (mock só em boundary lento/externo)
- **Arrange–Act–Assert**
- Um conceito por teste; nome que lê como spec
- Preferir real > fake > stub > mock de interação

### Nível
- Lógica pura → unit  
- Boundary (API/DB/fs) → integration  
- Fluxo crítico user / UI browser → **Playwright** (poucos E2E; ver `playwright.md`)

### UI web (quando a fatia for user-visible no browser)
1. Asserts de **comportamento** no Playwright (role/label/URL/estado)  
2. **Screenshot** do alvo (página | dialog | popup | trecho)  
3. **IA lê a imagem** e aplica checklist visual (`playwright.md`)  
4. No fechamento: comando + path do print + ok/falhas visuais  

Pixel baseline (`toHaveScreenshot`) **não** é default.  
UI reutilizável: kit canônico do repo — não copiar componente na page (`frontend-ui-engineering.md`).  
Código tocado: comentário **semântico** mínimo (arquivo/export + não trivial + trade-off) — DoD / `simplify.md`.

### Verify do repo (após verde)
- [ ] Testes da fatia / existentes relevantes  
- [ ] Se UI web: Playwright/E2E focado + screenshot lido pela IA  
- [ ] Build  
- [ ] Typecheck / lint se houver  
- [ ] Aceite da task  
- [ ] Commit da fatia **se couber** (ver §7) — **não bloqueia** o `[x]`

Não rode o mesmo comando de novo sem mudança de código no meio.

---

## 5 — Estratégias de fatia

- **Vertical (preferida):** um caminho completo na stack por vez.  
- **Contract-first:** contrato → back → front mock → integrar.  
- **Risk-first:** incerteza maior primeiro.

Dentro da task: ainda fatias finas se a task for M; cada sub-fatia ainda RED→GREEN→verify (commit **só se couber**, §7 — não bloqueia done).

---

## 6 — Regras de implementação

- **Simplicidade** — mais simples que funciona; sem abstração prematura.  
- **Escopo** — só a task / só o finding. Fora → `NOTICED BUT NOT TOUCHING`.  
- **Uma coisa** por incremento.  
- **Sempre compilável** entre fatias.  
- **Feature flag** se WIP user-visible.  
- **Defaults seguros** / **rollback-friendly**.  
- **Só o decidido** — inventar requisito = defeito; use Q + RECOMENDO.  
- **Obsoleto:** deletar direto (sem shim de compat interna). API publicada a terceiros: ver DoD.

---

## 7 — Commit (não bloqueante)

Regra: **`(A ∨ B) ∧ C`** — só então tente commitar. Fora disso, pule o commit e siga com `[x]` se aceite+testes ok.

| | Condição |
|---|---|
| **A** | Humano pediu commits **ou** a task do todo exige commit explícito |
| **B** | Repo limpo o bastante **e** commit local é rotina deste projeto |
| **C** | Git utilizável (user configurado, não bare, sem falha óbvia de hook/index) |

- Commit se `(A ou B) e C`.
- **Não** commitar se só A/B sem C, nem se só C sem A nem B.
- Mensagem da fatia/task quando commitar.

**Não** trava o done da task se:

- `(A ∨ B) ∧ C` for falso (não tentou / não pediu);
- commit falhar (user.name, hook, conflict);
- o humano não quer commit nesta sessão;
- working tree tem trabalho alheio misturado — **não** force; reporte e deixe `[x]` se aceite+testes ok.

Detalhe de branch/histórico: `references/git-workflow-and-versioning.md` quando for além do commit local simples.  
Nunca `Co-Authored-By` de ferramenta no commit (regra do projeto).

---

## 8 — Refs sob demanda (não são skills)

Abrir **antes de codar** se a fatia cair no domínio:

| Arquivo | Quando |
|---|---|
| `references/playwright.md` | **Web/UI browser** — E2E Playwright, screenshot, validação visual pela IA, debug ao vivo |
| `references/test.md` | Pirâmide, anti-patterns, DAMP, sintaxe de exemplo (Jest/RTL/Supertest) |
| `references/simplify.md` | Clareza sem mudar comportamento (REFACTOR pesado / “simplifica X”); política de comentário semântico |
| `references/debugging-and-error-recovery.md` | Bug sistemático além do prove-it |
| `references/frontend-ui-engineering.md` | UI, kit centralizado, a11y, layout, comentário em UI |
| `references/api-and-interface-design.md` | API, contratos, boundaries |
| `references/source-driven-development.md` | Doc oficial de lib/framework |
| `references/git-workflow-and-versioning.md` | Branch, histórico, convenção de commit rica |
| `references/observability-and-instrumentation.md` | Logs/métricas/traces em path crítico |
| `references/deprecation-and-migration.md` | Remover/substituir sistema antigo |
| `references/doubt-driven-development.md` | Decisão não trivial / alto risco |
| `references/definition-of-done.md` | **Canônica** — gate “pronto?” além do aceite |

TDD / prove-it / discover stack = **neste skill**, não exige abrir `test.md` no caminho feliz.  
Simplify leve no REFACTOR do ciclo; `simplify.md` quando o passo for de clareza de verdade (ou pedido explícito).

### Do review (implementar com a barra certa — não é review formal)

Paths sob `../fluxline-review/references/` (skill irmã em `skills/`). Abrir **antes de codar** se a fatia tocar o domínio; o **veredito multi-eixo** continua sendo da review. Prefira install do **pack inteiro** (refs cruzadas).

| Arquivo (review) | Quando na build |
|---|---|
| `security-and-hardening.md` | Fatia com input, auth, segredo, upload, LLM, pagamento |
| `secure-coding-checklist.md` | Mesma fatia sensível — checklist prático enquanto implementa |
| `security-map.md` | Fatia LARGE / multi-superfície (não no happy path de endpoint único); **não** carregar de rotina |
| `security/<classe>.md` | Fix de finding de uma classe (ex. `security/ssrf.md`) — ver `security/README.md` |
| `performance-optimization.md` | Path quente, lista, query, bundle, CWV no aceite |
| `documentation-and-adrs.md` | API pública / decisão arquitetural que a fatia fecha |
| `definition-of-done.md` | Pointer → canônica neste pacote |

**Só na review (não abrir na build pra “passar de review”):** `ci-cd-and-automation.md`, `shipping-and-launch.md`.  
**Não** carregar a pasta `security/` inteira — uma classe por fatia.

---

## 9 — Fechar e handoff

### Quando handoff `fluxline-review`

| Situação | Handoff |
|---|---|
| Todo de plan zerado (modo A ou B) | `fluxline-review` — first pass da run |
| Critical/Required do **handoff de review** todos implementados (todo podia já estar zerado) | `fluxline-review` — **re-review obrigatório** (mesmo id; **atualizar** o mesmo `review-fase-…`, ex. seção `## Re-review` — não inventar segundo arquivo) |
| Ainda há tasks de plan e modo A | Para; espera ok — **não** handoff review ainda |
| Build avulso sem run | Handoff review se o humano pediu review/merge; senão reporte e pare |

**Sempre** após fechar fixes vindos de Request changes: re-review. Não declarar “pronto/mergeable” só com o patch.

Mesma sessão: se o humano disser “aplica o handoff” / “já corrige” **depois** de um veredito review, esta skill roda em seguida (a review não edita source; a build implementa).

Sempre no fechamento de task/fase/fix batch:
1. Todo/plan com `[x]` no disco (quando existir task de plan)
2. Evidência: comandos rodados e resultado; commit se houve
3. Próximo passo explícito: continuar mode A / **`fluxline-review`** / **re-review**

---

## Anti-skip

| Racionalização | Realidade |
|---|---|
| "É só um fix, sem skill" | Build obrigatória em código de comportamento. |
| "Testo no final" | RED primeiro; bug na fatia 1 contamina o resto. |
| "Marco o todo depois / no chat" | Marca no arquivo na hora, sem perguntar. |
| "Sigo todas as fases sem o humano pedir" | Default é fase a fase. |
| "Open list no todo" | Q + RECOMENDO ou devolve spec. |
| "Carrego todas as refs" | Só as da fatia. |
| "Enquanto estou aqui limpo X" | NOTICED; não toca. |
| "Commit falhou = task não done" | Commit não bloqueia; testes+aceite sim. |
| "Fixei review, tá mergeable" | Re-review obrigatório. |
| "UI ok no unit, sem Playwright" | User-visible no browser → E2E + evidência visual. |
| "Tirei print e não li" | Screenshot sem leitura da IA não conta. |
| "Copiei o botão na page" | Kit canônico; reusar. |

**Red flags:** código sem esta skill; task done sem `[x]` no todo; teste depois do código “porque era óbvio”; prove-it invertido; modo B sem pedido; checkpoint verde de mentira; ref de UI/API/Playwright ignorada; UI done sem print lido; **patch de review sem handoff re-review**.

---

## Verificação

- [ ] Modo A ou B declarado  
- [ ] Buracos: Q + RECOMENDO ou devolveu spec/interview  
- [ ] Stack de teste descoberto; RED→GREEN→REFACTOR (ou prove-it em bug)  
- [ ] Se UI web: Playwright + screenshot + checklist visual pela IA  
- [ ] Verify do repo ok; commit **se couber** (não bloqueante)  
- [ ] **Todo (e plan) atualizados com `[x]` no disco** quando aplicável  
- [ ] Refs da fatia lidas quando aplicável  
- [ ] Próxima fase (modo A) **ou** handoff `fluxline-review` (todo zerado) **ou** re-review (fixes de review fechados)
