---
name: research-start
description: >
  Research roadmap for a legal issue — leis a checar, áreas de jurisprudência
  a investigar, frameworks regulatórios, termos de busca para JusBrasil/STF/STJ.
  Leads and frameworks, NOT authoritative citations; students verify and develop
  everything. Use when a student asks where to start researching, wants a
  research roadmap for an issue, or needs gaps identified in existing research.
argument-hint: "[legal issue]"
---

# /research-start

1. Load `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` → jurisdiction, practice area.
2. Use the workflow below.
3. Frame the issue specifically. Build roadmap: statutory starting points (unverified), case law areas (not cases), secondary sources, search terms.
4. If student has existing research uploaded: synthesize and identify gaps.
5. Output with prominent "leads not authorities" header. Everything is a starting point the student verifies.

```
/legal-clinic:research-start "defesa de habitabilidade/vício do imóvel em ação de despejo por falta de pagamento em [Comarca/Estado]"
```

---

# Research Start: Roadmap, Not Research

## Purpose

Legal research is essential to clinical education. But the initial phase — figuring out *what* to research, finding the right statute, understanding the framework — is often the most time-consuming and least educational part. Students spend hours finding the starting point before they can do the actual research.

This skill produces the starting point: leis a checar, áreas de jurisprudência a investigar, termos de busca para JusBrasil e sites do STF/STJ. **None of it is verified. None of it is authoritative. All of it is a lead for the student to run down.**

**This is a pedagogical safeguard, not just an ethical one.** Students still learn to research. They just start from a better place.

## Load context

`~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` → jurisdiction (state), practice areas.

## Workflow

### Step 0: Seed documents first

**Before building the roadmap, read the clinic's own seed documents.** The supervising attorney uploaded them at cold-start (handbook, filing guides, local court rules, intake forms, example case files, prior memos) — they are pre-vetted, jurisdiction-specific, and will beat any JusBrasil/Escavador query on the first 20 minutes of a student's research.

1. Read `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` → `## Seed documents`. Identify any item whose purpose or filename matches the research area (e.g., "Alameda UD filing guide" for a UD habitability question; a redacted sample case file in the same practice area; a prior memo on the same issue).
2. For each match, surface it as a **Seed documents to read first** block at the top of the roadmap output. Name the file, say why it matters for this specific question, and say what it likely covers vs. where outside research will still be needed.
3. If no seed documents match the issue, say so plainly ("No clinic seed documents match this issue — proceeding straight to primary sources"). Don't fabricate a match.
4. If the clinic has the `LIMITED DATA` flag set in `## Seed documents`, add a one-line note: "Clinic has fewer than 10 seed docs; your professor's precedent bank is thin — lean harder on primary sources and flag what's missing for your supervisor."

The roadmap still covers statutes, case law areas, secondary sources, and search terms — seed docs are the first lead, not a replacement for the rest. But surface them above everything else so the student starts where their supervisor's precedent starts.

### Step 1: Frame the issue

What's the research question? Be specific. Not "defesas em despejo" — "defesa de vício/inabitabilidade do imóvel em ação de despejo por falta de pagamento em [Comarca/Estado], especificamente se ausência de aquecimento/infiltração grave qualifica como vício e se o inquilino precisava notificar o locador por escrito antes."

If the question is too broad, narrow it with the student: "Isso são três perguntas de pesquisa. Vamos uma de cada vez. Qual primeiro?"

### Step 2: Build the roadmap

**Statutory starting points:**
List statutes *likely* relevant. State explicitly these are likely, not confirmed.

> **Leis provavelmente relevantes** (NÃO VERIFICADO — confirmar vigência e aplicabilidade):
> - Lei do Inquilinato (Lei 8.245/1991), arts. 22-23 — deveres do locador (manter o imóvel em condições de uso) e do locatário
> - Código Civil, arts. 566-568 — vícios da coisa locada, direito a abatimento do aluguel ou rescisão
> - Código de Defesa do Consumidor, se aplicável à relação (locação por administradora/imobiliária pode atrair CDC em certas hipóteses)
> - `[VERIFY each citation is current and correct — leis podem ser alteradas]`

**Case law areas to investigate:**
Not cases — *areas*. The student finds the cases.

> **Áreas de jurisprudência:**
> - Súmulas e julgados do STJ sobre vício do imóvel locado e abatimento proporcional do aluguel
> - Julgados do TJ do estado sobre o que qualifica como vício grave (infiltração, falta de água/energia, mofo estrutural)
> - Julgados sobre pré-requisito processual — o locatário precisava notificar antes de reter o aluguel ou consignar em pagamento?
> - Julgados sobre o remédio — abatimento proporcional, rescisão, ou consignação em pagamento (art. 335, CC)?

**Regulatory / administrative sources:**
If applicable.

> **Fontes administrativas/regulatórias:**
> - Código de obras/postura municipal, se a questão envolver condição de habitabilidade fiscalizável pela prefeitura
> - Normas da ANVISA/vigilância sanitária, se envolver salubridade
> - Para matéria previdenciária/assistencial: Manual de Benefícios do INSS, súmulas do Conselho de Recursos da Previdência Social (CRPS)

**Secondary sources to orient:**
Where to get the framework before diving into primary.

> **Fontes secundárias (para framework, não para citar):**
> - Doutrina de locação (Sylvio Capanema, Gildo dos Santos) — checar biblioteca da clínica
> - Material de curso/CLE sobre locação e Lei do Inquilinato
> - Artigos de revista jurídica sobre o tema específico, se controvertido

**Search terms:**
For JusBrasil, or whatever the clinic uses.

> **Termos de busca a tentar:**
> - JusBrasil: `"vício do imóvel locado" abatimento aluguel [Estado]`
> - STJ (jurisprudência): `vício redibitório locação abatimento proporcional`
> - Refine based on what comes back — these are starting queries

### Step 3: Flag what's uncertain

If the skill is unsure whether a source is relevant or current:

> `[UNCERTAIN: whether [State] has a specific statute on this vs. common-law
> doctrine only — the search will tell you]`

Uncertainty is stated, not hidden.

> **No silent supplement.** This skill produces leads, not authoritative citations — by design, students run the citations down themselves. But if a query to a configured research tool (JusBrasil, STF, STJ) returns few or no results for a specific rule or case, say so and stop. Do NOT manufacture citations from web search or model knowledge to fill a thin result set without asking. Say: "The search returned [N] results from [tool]. Coverage appears thin for [rule]. Options: (1) broaden the search query, (2) try a different research tool, (3) search the web — results will be tagged `[web search — verify]` and should be checked against a primary source before relying, or (4) stop here and flag the gap for your supervisor. Which would you like?" The supervising attorney decides whether to accept lower-confidence sources.
>
> **Source attribution.** Tag every suggested citation with where it came from: `[JusBrasil]`, `[STF]`, `[STJ]`, or the MCP tool name for citations retrieved from a legal research connector; `[web search — verify]` for web-search citations; `[model knowledge — verify]` for citations recalled from training data; `[user provided]` for citations supplied by the supervising attorney or case file. Citations tagged `verify` carry higher fabrication risk and should be checked first. Never strip or collapse the tags — they tell the student which leads are raw research and which are model guesses to verify against a primary source.

### Step 4: Synthesize uploaded research (if any)

If the student has already done some research and uploads it: read it, identify what's covered and what's missing.

> **From your research so far:**
> - You have: [summary of what's covered]
> - Gap: [what the roadmap above suggests that you haven't found yet]
> - `[VERIFY: the case you cited — [name] — run through a citator (verify it is good law) it, it may have been distinguished or limited]`

## Output

```markdown
═══════════════════════════════════════════════════════════════════════
  RESEARCH ROADMAP — LEADS, NOT AUTHORITIES
  Nothing below is a verified citation. Every statute, every case area,
  every search term is a starting point for YOUR research. You verify
  currency, applicability, and accuracy. You find the actual cases.
  If something below turns out to be wrong or outdated, that's expected —
  this is a map of where to look, not a substitute for looking.
═══════════════════════════════════════════════════════════════════════

# Research Roadmap: [Issue]

**Jurisdiction:** [State] | **Practice area:** [area]

## Seed documents to read first

[Per Step 0. List any clinic seed docs that match the issue with a one-line
"what this likely covers" note. If none matched: "No clinic seed documents
match this issue — proceeding to primary sources."]

## Statutory starting points (UNVERIFIED)

[list with VERIFY flags]

## Case law areas to investigate

[areas, not cases]

## Administrative / regulatory sources

[if applicable]

## Secondary sources (for framework, not citation)

[list]

## Search terms

**JusBrasil / STF / STJ:** [queries]

## Uncertainty flags

[Everywhere the roadmap is genuinely unsure]

---

## What to do with this

1. Start with a secondary source to get the framework
2. Find and read the primary statutes — confirm the citations above are current
3. Run the searches, find the leading cases
4. run through a citator (verify it is good law) everything before relying on it
5. Come back and run `/memo` to scaffold your analysis once you have the rule

## What this roadmap does NOT do

- **It does not give you citations you can use.** Every cite above is a lead
  to verify, not an authority to rely on.
- **It does not do the research.** You do the research. This gets you to the
  starting line faster.
- **It does not replace JusBrasil/STF/STJ.** Those have the actual cases. This
  tells you where to point them.

---

**Cite verification — required before use.** Citations above were generated by an AI model and have not been verified. Before relying on any case, statute, or rule — or including it in client work — run it through JusBrasil, STF, STJ, or your clinic's research platform for accuracy and current good-law status. Flag unverified citations to your supervisor.
```

## What this skill does NOT do

- **Provide authoritative citations.** Explicitly, by design. The student verifies every cite before using it.
- **Replace legal research.** Accelerates the "where do I start" phase; the research itself is still the student's.
- **Guarantee the roadmap is complete.** It's a starting set of leads. The research may reveal sources the roadmap missed — that's fine, that's research.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

