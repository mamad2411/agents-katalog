---
name: frontend-pro
description: >
  Frontend especializado (PDA exec + gate visual): Build, Review, Vision, Fix, Audit
  com design system pesquisável, boot sequence, matriz multi-viewport, Puppeteer/
  agent-browser, anti-slop e delegação obrigatória a image-to-code com imagem anexada.
  Use quando /frontend-pro, UI web (landing, dashboard, SaaS), componentes, tokens,
  review visual com evidência, mockup anexado. Não use para backend/API (backend),
  schema (database), CI/deploy (devops), E2E suite gate (testing), planeamento
  (planner), aceite PO (po-review), security gate (security), nem documentação
  (documentation). KEEP specialized — não fundir com Universal Developer.
metadata:
  version: "1.2.0"
  status: experimental
  capability: frontend-ui
  type: worker
  command: frontend-pro
  pda_roles: [exec, gate]
  eval_iteration: 3
  non_responsibilities:
    - backend-implementation
    - database-schema
    - devops-deploy
    - testing-gate
    - security-gate
    - po-acceptance
disable-model-invocation: true
---

# Frontend Pro — Build · Review · Vision

Provider **`frontend-ui`** (worker) + **`frontend-visual-review`** (gate). Runtime: `Cursor/orchestrator/`.

Skill local de frontend que combina **design intelligence** (fork de `ui-ux-pro-max`), **QA visual com browser**, **anti-slop** e **Vision via `image-to-code`**.

**Policy:** listar capabilities **≠** autorização. Policy Engine medeia; modos Review/Audit são gate de evidência visual — **não** substituem `testing`, `security-review` nem `po-acceptance`.

## HARD-GATE — Imagem anexada

**Sempre** que o utilizador anexar **qualquer imagem** (mockup, screenshot, wireframe, referência):

1. **Modo Vision** — não Build genérico
2. **Ler integralmente** `~/.agents/skills/image-to-code/SKILL.md` **antes** de codificar
3. Seguir [../orquestrar/references/image-attachment-gate.md](../orquestrar/references/image-attachment-gate.md)

Proibido implementar HTML/CSS/JS “a olho” com imagem anexada no contexto.

---

## Boundaries — DO / DO NOT

### DO

- Build/Vision/Fix de UI conforme stack detectada + anti-slop + design intelligence
- Review/Audit com **screenshot real** antes de veredito; matriz viewport quando Audit
- HARD-GATE Vision: ler `image-to-code` integralmente com imagem anexada
- Relevant Context: boot sequence (stack, design-system, URL) — não o repo inteiro
- Handoff estruturado (design-plan / visual-review-report / fix-list / audit-report)

### DO NOT

- Backend/API/endpoints (`backend-implementation`)
- Schema/migrações (`database-schema`) ou CI/deploy (`devops-deploy`)
- Suite E2E/CI como gate `testing`; veredicto security ou aceite PO
- Aprovar UI sem evidência visual (screenshot)
- Contornar Policy Engine / isolation de gates

---

## Capability scope

| Classe | Capabilities | Motivo |
|--------|--------------|--------|
| **required** | `frontend-ui` (Build/Vision/Fix) | Identidade worker |
| **required (Review/Audit)** | `frontend-visual-review` | Gate de evidência visual |
| **optional** | `filesystem.read/list/search/write` (paths UI), `project.inspect`, `git.inspect`, `shell.execute` (dev server), browser MCP / agent-browser | Contexto + captura |
| **forbidden** | `backend-implementation`, `database-schema`, `devops-deploy`, `testing` (suite gate), `security-review`, `po-acceptance` | Least authority — KEEP specialized frontend |

---

## Failure / degradation

| Classe | Se… | Então… |
|--------|-----|--------|
| `context_failure` | Review sem URL | Pedir URL/porta; sem veredito |
| `context_failure` | Pedido vago ("mais bonito") | Boot + clarificar página/modo |
| `capability_failure` | Browser/MCP indisponível | Declarar limitação; não inventar screenshots |
| `policy_denial` | Policy nega write/browser | Respeitar; reduzir scope |
| `agent_failure` | Pedido = API/CI/security gate | Redireccionar skill irmã |

## Quando usar

| Situação | Modo |
|----------|------|
| **Imagem anexada** pelo utilizador | **Vision** → `image-to-code` (obrigatório) |
| Nova página, componente, tokens (sem anexo) | **Build** |
| "Está bom?", pós-implementação, PR UI | **Review** |
| Landing premium, redesign visual forte (sem anexo) | **Vision** |
| Corrigir só itens do último relatório | **Fix** |
| Pré-release, QA visual completo | **Audit** |

## Quando não usar

- Backend, API, DB, infra
- Suite de testes E2E / CI (outra skill)
- Planeamento, PO review, security audit, documentação
- Perguntas conceptuais puras ("o que é CSS Grid?") sem entrega UI

---

## Boot sequence (obrigatória)

Antes de Build, Review ou Audit, executar em silêncio (documentar suposições em `run-notes` se inferir):

1. **Stack** — `package.json`, `tailwind.config.*`, `next.config.*` → ver [references/boot-sequence.md](references/boot-sequence.md)
2. **Design system existente** — `design-system/MASTER.md` e `design-system/pages/*.md`
3. **URL dev** — script `dev`, README, porta (ex. `localhost:3000`)
4. **Modo** — se **imagem anexada** → **Vision** (obrigatório); senão Build | Review | Vision | Fix | Audit
5. **Ferramenta browser** — Puppeteer MCP vs agent-browser → [references/browser-tools.md](references/browser-tools.md)

Se Review/Audit sem URL: **pedir URL e porta** antes de veredito.

---

## Modos

Detalhe: [references/modes.md](references/modes.md)

### Build

1. Boot sequence
2. Design system: `search.py --design-system` (usar `--persist` se projeto longo)
3. Suplementar com `--domain` / `--stack` conforme stack detectada
4. Aplicar [references/anti-slop.md](references/anti-slop.md) no plano antes de codificar
5. Entregar código + opcional `templates/design-plan.md`

### Review

1. Boot sequence + confirmar URL
2. Capturar screenshots na **matriz mínima** → [references/visual-qa.md](references/visual-qa.md)
3. Analisar por prioridades P1→P10 (tabela abaixo)
4. **Proibido** emitir veredito final sem pelo menos 1 screenshot real da página alvo
5. Preencher [templates/visual-review-report.md](templates/visual-review-report.md)

### Vision (image-to-code)

**Trigger:** imagem anexada pelo utilizador **ou** landing premium / marketing / redesign onde qualidade visual é o produto.

1. **Ler integralmente** `~/.agents/skills/image-to-code/SKILL.md`
2. Se a imagem **já veio anexada:** analisar em profundidade → implementar (não saltar análise)
3. Se **não** houver anexo: workflow **image-first** completo dessa skill (gerar → analisar → implementar)
4. `frontend-pro` fornece contexto de stack e design system; **não** substituir o workflow image-to-code

### Fix

1. Ler último relatório em `.frontend-review/` ou o fornecido pelo utilizador
2. Corrigir **apenas** itens listados, por ordem Blocker → Major → Minor
3. Re-capturar screenshots dos IDs afectados
4. Actualizar [templates/fix-list.md](templates/fix-list.md)

### Audit

Review + matriz completa (viewports × tema × estados) + checks a11y visíveis → [templates/audit-report.md](templates/audit-report.md)

---

## Prioridades de regras (P1→P10)

| P | Categoria | Domain search |
|---|-----------|---------------|
| 1 | Accessibility | `--domain ux` |
| 2 | Touch & Interaction | `--domain ux` |
| 3 | Performance | `--domain ux` |
| 4 | Style Selection | `--domain style`, `product` |
| 5 | Layout & Responsive | `--domain ux` |
| 6 | Typography & Color | `--domain typography`, `color` |
| 7 | Animation | `--domain ux` |
| 8 | Forms & Feedback | `--domain ux` |
| 9 | Navigation | `--domain ux` |
| 10 | Charts & Data | `--domain chart` |

Review/Audit: analisar **P1–P2 primeiro**; só depois polish.

---

## Design intelligence (`search.py`)

Pré-requisito: `python3 --version`

**Path da skill** (a partir da raiz `Cursor/` do repo AGENTS):

```bash
python3 .cursor/skills/frontend-pro/scripts/search.py "<query>" --design-system [-p "Project Name"]
python3 .cursor/skills/frontend-pro/scripts/search.py "<query>" --design-system --persist -p "Name"
python3 .cursor/skills/frontend-pro/scripts/search.py "<keyword>" --domain ux [-n 5]
python3 .cursor/skills/frontend-pro/scripts/search.py "<keyword>" --stack nextjs
```

**Stacks web comuns:** `html-tailwind`, `nextjs`, `react`, `vue`, `svelte`, `shadcn`

**Persistência:** `--persist` cria `design-system/MASTER.md` + `design-system/pages/`

---

## Browser e evidência visual

| Ferramenta | Quando |
|------------|--------|
| **Puppeteer MCP** (`user-puppeteer`) | localhost, screenshots rápidos, viewports, click/fill simples |
| **agent-browser** | fluxos multi-passo, login, dogfood, Electron |

Screenshots: guardar em `.frontend-review/<YYYY-MM-DD>-<slug>/` com naming da matriz.

Ferramentas e comandos: [references/browser-tools.md](references/browser-tools.md)

---

## Recursos

| Ficheiro | Quando ler |
|----------|------------|
| [references/boot-sequence.md](references/boot-sequence.md) | Início de qualquer modo |
| [references/modes.md](references/modes.md) | Dúvida sobre fluxo |
| [references/visual-qa.md](references/visual-qa.md) | Review, Audit |
| [references/browser-tools.md](references/browser-tools.md) | Captura e interacção |
| [references/anti-slop.md](references/anti-slop.md) | Build, Vision |
| [references/visual-analysis.md](references/visual-analysis.md) | Análise pós-screenshot |
| [templates/visual-review-report.md](templates/visual-review-report.md) | Saída Review |
| [templates/audit-report.md](templates/audit-report.md) | Saída Audit |
| [templates/design-plan.md](templates/design-plan.md) | Saída Build |
| [templates/fix-list.md](templates/fix-list.md) | Saída Fix |
| `~/.agents/skills/image-to-code/SKILL.md` | **Vision** — leitura obrigatória |

---

## Quick reference web (crítico)

- Contraste ≥4.5:1; focus rings visíveis; labels em forms
- Touch targets ≥44px; `cursor-pointer` em clicáveis
- `min-h-dvh` em vez de `100vh`; mobile-first 375/768/1440
- Sem emoji como ícones; SVG consistente (Lucide/Heroicons)
- `prefers-reduced-motion`; dark mode testado separadamente
- Um CTA primário por ecrã; erros junto ao campo

---

## Integração image-to-code

**Contrato Vision:** quando houver **imagem anexada**, landing premium, marketing site, redesign visual, ou o utilizador pedir "vision":

```
1. Carregar ~/.agents/skills/image-to-code/SKILL.md
2. HARD-GATE: ../orquestrar/references/image-attachment-gate.md
3. Anexo do utilizador → analisar imagem antes de qualquer código
4. Sem anexo mas pedido visual premium → workflow image-first completo (gerar → analisar → implementar)
5. Usar frontend-pro apenas para: stack, search.py, anti-slop, pós-review opcional
```

Nunca saltar análise de imagem quando existir anexo. Nunca codificar primeiro em pedidos visuais premium.

Nunca saltar geração+análise de imagem em Vision quando image generation estiver disponível.

---

## Saída e severidades

| Severidade | Significado |
|------------|-------------|
| **Blocker** | Impede uso (a11y, fluxo quebrado) |
| **Major** | UX degradada significativa |
| **Minor** | Polish, inconsistência |
| **Nit** | Opcional |

Cada achado: ID, prioridade P1–P10, regra, ficheiro screenshot, fix sugerido.

---

## Versão

- **v1.2.0** — Package completeness Wave M2: DO/DO NOT, capability scope, failure, metadata command/pda_roles, Agents mirror
- **v1.1.0** — Build, Review, Vision, Fix, Audit; browser; matriz visual; anti-slop; image-to-code
