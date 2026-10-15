---
name: fluxline-review
description: OBRIGATÓRIA em qualquer pedido de revisão — code review, PR/diff/branch/commit, “revisa isso”, LGTM, gate multi-eixo. Use quando o usuário pede revisão ou invoca a skill. Só julga e grava veredito — NUNCA edita código (correção/simplify = handoff fluxline-build). Não reescreve spec/plan. Última porta da cadeia fluxline-*.
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Fluxline Review

## Obrigatória — qualquer revisão

Porta de **review** do Fluxline. Pediu revisão → **esta skill**. Não improvisar “olhada rápida” no chat sem protocolo e sem artefato.

**Read-only no código.** Achou problema → **finding + remédio nomeado + handoff `fluxline-build`**. Nunca cria/edita/apaga source, nunca “já corrige”, nunca aplica simplify. Mesmo com o humano dizendo “já corrige”: **esta** skill entrega veredito + HANDOFF; a **build**, invocada em seguida na mesma sessão, é quem patcha.

O frontmatter já tira `Edit` — `Write` fica para o `review-fase-…` e `Bash` para `git diff`/inspeção. Estreitamento, não sandbox: a regra acima vale por cima da ferramenta.

Ciclo: contexto → testes → cinco eixos → severidade → DoD → artefato em disco → handoff se couber.  
Refs: só as do **domínio do diff** (§8) — nunca a pasta inteira no boot.

| | |
|---|---|
| **Começa** | Pedido de revisão (ou invocação / handoff build / re-review) + alvo |
| **Termina** | Veredito em disco + findings severizados + handoff build se Request changes |

**Não faz:** interview, spec, plan, **qualquer escrita de código**, merge sozinho.  
Fecha a cadeia e também reabre: `… → build → **review**` e, se Request changes, `review → build → **review**`.

**Discovery:** esta cadeia é `fluxline-*` do começo ao fim — não substituir porta por skill de outro pack.

**Barra de approve:** melhora a saúde do código e segue as convenções do projeto → **Approve**. Não bloquear porque “eu escreveria diferente”; não exigir perfeição.

DoD canônica: `../fluxline-build/references/definition-of-done.md` (pointer local em `references/definition-of-done.md`).

---

## 0 — Gate

1. **Disparo** — qualquer um destes:
   - Humano pede revisão de qualquer tipo (código, PR, diff, branch, commit, “tá pronto?”, “pode mergear?”)
   - Invocação direta da skill
   - Handoff de `fluxline-build` (todo zerado / run acabou)
   - **Re-review** após build ter fechado Critical/Required de um veredito anterior
2. **Alvo** (primeiro que fechar):
   - Diff local / branch / PR / paths que o humano apontou
   - Run Fluxline: `docs/fluxline/plan/todo-fase-N-…` (+ plan + spec, mesmo id), se houver
   - “Review o que acabou de buildar” / re-review → id da run da conversa + diff dos fixes
3. Sem alvo e sem diff → **para**. Peça o id, o path, a branch ou o PR.
4. Todo incompleto e o humano pediu “pronto da feature” → diga o que falta no todo; **não** finja done.
5. Buraco de intenção/sucesso/fora → devolve `fluxline-spec` / `fluxline-interview`. Buraco pontual de desenho no código → finding com severidade, não reabre plan.

```
Q: <só se o veredito depende de decisão humana>
RECOMENDO: <opção> — <1 linha>
(ok / outra?)
```

Proibido Open Questions no artefato. Typo óbvio → finding (ou Nit) + handoff build; **não** editar o arquivo na review.

Ancorar em spec/todo (aceite) se existirem + DoD canônica.

---

## 1 — Os cinco eixos

### 1. Corretude

Faz o que alega?

- Casa com spec/task (aceite)?
- Edge cases (null, vazio, limite)?
- Caminhos de erro, não só happy path?
- Testes passam **e** testam a coisa certa?
- UI web user-visible: há Playwright/E2E de **comportamento** (não só unit)?
- Off-by-one, race, estado inconsistente?

### 2. Legibilidade e simplicidade

Outro eng/agent entende sem o autor?

- Nomes claros e do projeto (sem `temp`/`data`/`result` sem contexto)
- Fluxo reto (sem ternário aninhado / callback profundo desnecessário)
- **Menos linhas que resolvem?** (1000 onde 100 bastam = falha)
- Abstração **paga** a complexidade? (generalize no 3º uso)
- Comentário **semântico** onde a DoD exige (export/arquivo, não trivial, trade-off); sem narrativa do óbvio; sem dead code / shim “compat” / `// removed`
- Export/módulo **órfão** (papel ilegível por nome **e** sem cabeçalho) = finding
- Condicional nova em fluxo **não relacionado** = smell estrutural
- Condicionais repetidas na mesma forma = modelo/dispatcher faltando

Finding de complexidade/clareza → remédio: **`fluxline-build`** + `../fluxline-build/references/simplify.md`.

### 3. Arquitetura

Encaixa no desenho do sistema?

- Padrão existente vs padrão novo justificado?
- Limites de módulo limpos; deps no sentido certo (sem ciclo)
- Duplicação que deveria ser shared?
- UI: componente visual reutilizável fora do kit canônico / copiado na page?
- Refactor **reduz** conceitos que o leitor carrega — ou só **relocam**?
- Lógica de feature vazando em módulo shared/genérico?
- Fronteira de tipo explícita (`any`/fallback silencioso = cheiro)?

### 4. Segurança

**Escalonar refs (só as que o diff pede — nunca a pasta `security/` inteira):**

| Intensidade | Abrir |
|---|---|
| Diff toca input/auth/segredo/pagamento/integração | `references/security-and-hardening.md` |
| “Security review”, superfície quente, vários endpoints | + `secure-coding-checklist.md`; `security-map.md` **só** se inventário multi-superfície for necessário (é ref grande — não default) |
| Classe óbvia no diff (SQL, XSS, SSRF, IDOR…) | + **uma** ref em `references/security/` (ver `security/README.md`) |

Checklist rápido (ainda assim só finding + handoff build):

- Input validado na borda; SQL parametrizado; saída escapada
- Segredos fora de código/log/VCS
- Authz em ação privilegiada (não só login); sem IDOR
- Dados externos (API, log, config, LLM) como não confiáveis
- Deps de fonte confiável; audit sem crítico/alto alcançável sem mitigação

Reportar **confiança alta** (padrão explorável + input do atacante). Teórico / defense-in-depth → Nit ou FYI, não Critical inventado.

### 5. Performance

Regressão óbvia ou path quente? → ref `performance-optimization`.

- N+1; loops/fetch sem limite; sync que deveria ser async
- Re-render desnecessário; lista sem paginação; objeto grande em hot path

---

## 2 — Remédios estruturais (não só “está complexo”)

Quando achar problema estrutural, **nomeie o movimento**:

- Cadeia de condicionais → modelo tipado ou dispatcher
- Ramos duplicados → um fluxo claro
- Orquestração misturada com regra → separar
- Feature em shared → mover pro dono do conceito
- Helper quase-igual → reusar o canônico
- Fronteira de tipo implícita → explicitar (some branch a jusante)
- Wrapper pass-through → deletar
- Arquivo inchado → extrair helper/módulo focado

Prefira o remédio que **remove** peças móveis ao que espalha a mesma complexidade.  
Sinais e processo de clareza: `../fluxline-build/references/simplify.md`.

---

## 3 — Tamanho da mudança

```
~100 linhas  → bom, uma sentada
~300 linhas  → ok se for uma mudança lógica
~1000 linhas → grande demais — pedir split
```

Arquivo **total** ~1000 linhas também é sinal (não só o diff). Diff pequeno que empurra arquivo já grande → extrair **antes** de empilhar.

**Uma mudança** = um concern + testes relacionados + sistema utilizável. Refactor + feature = **duas** mudanças.

| Estratégia de split | Quando |
|---|---|
| Stack | Deps sequenciais |
| Por grupo de arquivo | Reviewers/concerns diferentes |
| Horizontal | Shared/stubs primeiro |
| Vertical | Fatias full-stack da feature |

Deleção completa / refactor automático (só conferir intenção) pode ser grande.

---

## 4 — Processo

### Passo 1 — Contexto

```
- O que a mudança tenta realizar?
- Qual spec/task?
- Qual mudança de comportamento esperada?
- É first pass ou re-review de findings anteriores?
```

Ler spec/todo da run se existir. Diff sozinho é fraco — leia callers e tipos ao redor.  
Em **re-review**: foque nos paths/remédios do HANDOFF anterior; não ignore regressões colaterais.

### Passo 2 — Testes primeiro

- Existem? Testam **comportamento** (não miolo/mock de interação)?
- Edges? Nomes legíveis? Pegariam regressão?
- **Diff UI web:** Playwright (ou E2E do repo) cobre o fluxo? Seletores estáveis (role/label)?
- Evidência visual: screenshot do alvo **e** indício de que foi inspecionado (path + nota)? Print morto = gap → Required se a mudança for visual/user-facing
- Remédio de gap de teste/visual: handoff **`fluxline-build`** + `../fluxline-build/references/playwright.md`

### Passo 3 — Código nos cinco eixos (só ler)

Por arquivo no diff: corretude → legibilidade → arquitetura → segurança → performance.

### Passo 4 — Severidade em todo finding

| Prefixo | Significado | Ação do autor |
|---|---|---|
| **Required:** | Obrigatório (use o prefixo; não deixe finding “sem prefixo”) | Antes do merge |
| **Critical:** | Bloqueia | Segurança, perda de dados, quebrado |
| **Nit:** | Opcional | Estilo; pode ignorar |
| **Optional:** / **Consider:** | Sugestão | Vale pensar |
| **FYI** | Só contexto | Sem ação |

Ordem por alavancagem: corretude e segurança → regressão estrutural / simplificação perdida → resto. Poucos findings de alta convicção > lista longa de nits. Um problema estrutural e dez nits → o estrutural **é** a review.

### Passo 5 — História de verificação

- Quais testes rodaram? Build? Manual?
- **UI:** comando Playwright/E2E? Path do screenshot? Checklist visual (IA) ok ou falhas listadas?
- Before/after quando for fix visual

### Passo 6 — DoD do projeto

Aceite da task **e** DoD canônica no que couber. Um sem o outro ≠ pronto.

---

## 5 — Dead code

Liste órfãos no finding; **não apague** nesta skill:

```
DEAD CODE IDENTIFIED:
- formatLegacyDate() em src/utils/date.ts — trocado por formatDate()
→ Handoff build: remover se confirmado (ok humano / Required)
```

---

## 6 — Desacordo e honestidade

Hierarquia: **fatos técnicos** → **style guide** → **princípios de design** → consistência do repo (se não piora a saúde).

- **Não** aceitar “limpo depois” — gate é agora (emergência real = bug com dono).
- Não rubber-stamp (“LGTM” sem evidência).
- Não suavizar bug de produção.
- Quantifique quando der (“N+1 ~50ms/item”).
- Critique o **código**, não a pessoa; se o autor tem contexto e override, ceda com graça.

---

## 7 — Dependências (parte da review)

Antes de **nova** dep: stack já resolve? tamanho? manutenção? CVE? licença? Preferir stdlib/utils do repo.

Upgrade: ler changelog (semver mente); **uma** dep por mudança; suite verde antes/depois; diff do **lockfile**; nunca editar lock à mão. Detalhe de audit/supply-chain → `security-and-hardening`.

---

## 8 — Refs sob demanda (não são skills)

Abrir **antes** de aprofundar o eixo se o diff cair no domínio. **Só leitura** — ref informa o finding; não vira permissão para codar.

### Deste pacote

| Arquivo | Quando |
|---|---|
| `references/definition-of-done.md` | Pointer → canônica build; gate “pronto?” — **quase sempre** |
| `references/security-and-hardening.md` | Input, auth, segredo, upload, LLM, deps |
| `references/security-map.md` | Só inventário multi-superfície / security review LARGE — ref **grande**, não boot default |
| `references/secure-coding-checklist.md` | Checklist por momento — só leitura aqui |
| `references/security/<classe>.md` | Classe de vuln do diff (índice: `security/README.md`) |
| `references/performance-optimization.md` | Latência, N+1, bundle, CWV, path quente |
| `references/ci-cd-and-automation.md` | Pipeline, gates de merge, deploy automatizado |
| `references/shipping-and-launch.md` | Pré-prod, flag, rollout, rollback, monitor |
| `references/documentation-and-adrs.md` | API pública, decisão arquitetural, changelog |

**Proibido:** carregar `references/security/` inteiro no boot. Uma (no máx. poucas) classe(s) por run.

### Do build (só leitura — julgar, não implementar)

Paths sob `../fluxline-build/references/` (skill irmã em `skills/`). Remédio no finding aponta **build** + ref. Prefira install do **pack inteiro**.

| Arquivo (build) | Quando na review |
|---|---|
| `definition-of-done.md` | **Canônica** — Preferir esta se for ler o checklist completo |
| `test.md` | Qualidade dos testes no Passo 2 / eixo corretude |
| `playwright.md` | Diff web/UI — E2E, screenshot, evidência visual |
| `api-and-interface-design.md` | Contrato/API/boundary no diff |
| `frontend-ui-engineering.md` | UI, kit centralizado, a11y, layout no diff |
| `simplify.md` | Finding de complexidade/clareza / comentário semântico (aplicar = build) |
| `observability-and-instrumentation.md` | Path crítico novo sem log/métrica |
| `deprecation-and-migration.md` | Remoção/substituição de API/sistema |
| `git-workflow-and-versioning.md` | Diff/PR monstro, histórico, mensagem |

Não carregar pastas inteiras no boot.  
**Não** abrir da build para “consertar”: `debugging-…`, `source-driven-…` — isso é loop da build.

---

## 9 — Artefato em disco (sempre, sem perguntar)

Review **termina em arquivo**. Chat sozinho não conta.

1. Garantir pasta na **raiz do workspace**:
   - Preferir: `bash <pack>/skills/fluxline-build/scripts/fluxline-run.sh review` — cria a pasta e devolve `next_n`
   - Sem bash: criar `docs/fluxline/review/` na mão
2. Grave o veredito:

| | |
|---|---|
| Path | `docs/fluxline/review/review-fase-N-<slug>-<nome-curto>.md` |
| Com run Fluxline | **mesmo id** da spec/plan/todo |
| Sem run (diff avulso) | `N` = `next_n` do script; slug do tema; nome-curto ex. `diff-local`, `pr-42` |
| Re-review | Mesmo id; atualize o arquivo **ou** grave rodada explícita no mesmo doc (seção `## Re-review YYYY-MM-DD`) — não deixe só no chat |
| Quando | ao fechar o veredito |

### Template do artefato

```markdown
# Review: [título curto]

## Contexto
- Alvo: [run id | branch | PR | local]
- Spec/todo: `…` (se houver)
- O que muda: [1–3 frases]
- Rodada: first-pass | re-review

## Findings
### Critical / Required
- **Critical:** `path:linha` — … — remédio: …
- **Required:** `path:linha` — … — remédio: …

### Optional / Nit / FYI
- **Nit:** …

## Verificação do autor
- Testes: [comandos / resultado]
- Playwright/E2E (se UI): [comando / resultado]
- Screenshot: [path | N/A] — visual IA: [ok | falhas]
- Build: …
- Manual: …

## DoD (trechos aplicáveis)
- [ ] … / N/A: …

## Veredito
- [ ] **Approve** — pronto no padrão
- [ ] **Request changes** — Critical/Required acima
- [ ] **Approve com defer** — Required X deferido porque … (bug/dono)

## HANDOFF (se Request changes)
- [Critical] path:linha — … — remédio: … — ref: …
- [Required] …
```

Omita seções vazias. Não invente finding pra encher.

---

## 10 — Fechar

1. Path + id do artefato  
2. Contagem: Critical / Required / Optional / Nit  
3. Veredito em uma linha  
4. Se **Request changes** → próximo = **`fluxline-build`** com a lista de findings (severidade, path, remédio, ref). Não reabrir plan a menos que o aceite mude. Humano pediu “já corrige” → invocar a build **depois** do veredito salvo.  
5. Se **Approve** e era handoff de build / re-review ok → run **fechada** no padrão Fluxline

Formato curto de handoff (no chat + espelhado no artefato):

```
HANDOFF → fluxline-build
- [Critical] path:linha — … — remédio: … — ref: …
- [Required] …
→ Após fixes: re-review obrigatório (fluxline-review, mesmo id)
```

---

## Anti-skip

| Racionalização | Realidade |
|---|---|
| "Funciona, chega" | Dívida de legibilidade/segurança/arquitetura compõe. |
| "Eu escrevi, sei que está certo" | Autor é cego às próprias premissas. |
| "Limpamos depois" | Depois não vem. Gate = agora. |
| "Código de IA está ok" | Precisa **mais** escrutínio, não menos. |
| "Testes passam = bom" | Não pega arquitetura, segurança, legibilidade, visual. |
| "UI unit passou, chega" | User-visible → Playwright + print lido. |
| "Tem screenshot no CI artifact" | Sem inspeção/nota = evidência morta. |
| "O refactor ficou mais limpo" | Relocar ≠ reduzir conceitos. |
| "Só um pedacinho no arquivo" | Diff pequeno ainda estoura tamanho e entorta fluxo. |
| "É só bump de versão" | Comportamento que você não escreveu — leia changelog. |
| "Marco só no chat" | Salva o `review-fase-…`. |
| "Já corrijo na review" | **Handoff build** (pode invocar build na sequência). |
| "Carrego todas as refs" / "abro o mapa monstro + 16 classes" | Só o domínio do diff; mapa só se inventário LARGE. |
| "É só uma olhada, sem skill" | Pediu revisão → skill obrigatória. |
| "Só depois do build" | Review sob demanda a qualquer momento. |

**Red flags** (o que a tabela acima não cobre): **diff de source produzido na run de review**; merge sem review; diff sensível sem o eixo de segurança; bug fix sem teste de regressão exigido no finding; finding sem prefixo de severidade; re-review pulado após fixes; componente UI duplicado fora do kit.

---

## Verificação

- [ ] Alvo claro; spec/todo lidos se existirem  
- [ ] First-pass ou re-review declarado  
- [ ] Testes do diff revisados (Passo 2) — sem editar testes  
- [ ] Se UI: Playwright/E2E + evidência visual (screenshot + leitura) checados  
- [ ] Cinco eixos aplicados ao diff  
- [ ] Findings com prefixo de severidade; Critical/Required no topo; remédio nomeado  
- [ ] DoD canônica no que couber  
- [ ] História de verificação do autor checada  
- [ ] `docs/fluxline/review/review-fase-N-….md` salvo (raiz do workspace)  
- [ ] **Nenhum** source editado **nesta** skill  
- [ ] Request changes → handoff explícito `fluxline-build` (+ build na sequência se humano pediu aplicar); Approve → run fechada se couber  
- [ ] Refs do domínio abertas quando o diff pedia  
