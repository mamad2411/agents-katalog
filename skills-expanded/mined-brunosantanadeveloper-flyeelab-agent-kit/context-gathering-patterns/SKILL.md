---
name: context-gathering-patterns
description: >
  Coleta de contexto com máxima eficiência de tokens. Usa pirâmide de custo
  crescente: frontmatter → seções específicas → docs completos → Flyee API.
  Obrigatório antes de qualquer implementação (SIMPLE e COMPLEX CODE).
skills:
  - history-check-patterns
---

# Context Gathering Patterns

> **Regra de ouro:** Leia o mínimo necessário para tomar a decisão correta.
> Token = custo. Leitura desnecessária = contexto poluído + janela reduzida.

---

## 🎯 PROPÓSITO

Garantir que antes de implementar qualquer mudança o agente tenha contexto
suficiente — sem desperdiçar tokens com leituras redundantes.

**Dois objetivos em tensão:**
- ✅ Contexto completo (evitar bugs, não reinventar, seguir padrões)
- ✅ Economia de tokens (janela de contexto é recurso limitado)

**Solução:** Pirâmide de leitura com custo crescente. Parar no nível mais baixo
que responda às perguntas necessárias.

---

## 🔺 PIRÂMIDE DE CONTEXTO (custo crescente → parar o quanto antes)

```
Nível 1 — ~100 tokens    → agent_context (YAML frontmatter dos docs relevantes)
Nível 2 — ~300 tokens    → INDEX.md + tabelas Summary nos docs
Nível 3 — ~500 tokens    → RETRO / LESSONS-LEARNED / BUGS-KNOWN
Nível 4 — ~800 tokens    → Seção ESPECÍFICA do SDD/PRD (não o arquivo inteiro)
Nível 5 — ~1.500 tokens  → Arquivo de código afetado + CODEBASE.md
Nível 6 — ~3.000 tokens  → bridge --search-context (resultado filtrado, não lista)
Nível 7 — NUNCA          → Histórico bruto de conversa / leitura de outros projetos
```

> [!CAUTION]
> **PROIBIDO:** Ler PRD ou SDD inteiros quando apenas uma seção é relevante.
> **PROIBIDO:** Usar histórico de conversa como fonte de contexto — use docs locais.
> **PROIBIDO:** Analisar código de outros projetos como referência — use padrões documentados.

---

## 🔍 QUANDO USAR CADA NÍVEL

### Request SIMPLE CODE (fix, add, change — arquivo único)

```
Nível 1 → Nível 2 → Nível 5
```
Ler: frontmatter do BREAKDOWN → Summary table → arquivo afetado.
Parar se já há resposta.

### Request COMPLEX CODE / DESIGN (build, create, implement)

```
Nível 1 → Nível 2 → Nível 3 → Nível 4 → Nível 5 → Nível 6 (se necessário)
```
Cada nível só é acionado se o anterior não respondeu as perguntas do Gate.

---

## 📋 PROCESSO PASSO A PASSO

### ► Passo 0: Verificar INDEX.md (sempre, custo mínimo)

```bash
# Ler apenas o INDEX.md — mapa de todos os docs existentes
view_file docs/INDEX.md
```

Objetivo: saber QUAIS docs existem antes de buscá-los.
Nunca buscar `find docs/ -name "*.md"` — use o INDEX.

---

### ► Passo 1: Ler frontmatter dos docs relevantes (Nível 1)

Para cada doc relevante identificado no INDEX.md, ler **apenas o frontmatter**
(linhas entre `---` no início do arquivo). O campo `agent_context` contém o
resumo semântico que o agente precisa sem ler o documento inteiro.

**Documentos prioritários (na ordem):**

| Doc | Onde | Responde |
|-----|------|----------|
| `BREAKDOWN-tasks.md` | `docs/` | O que já foi implementado? Qual padrão seguir? |
| `RETRO-{projeto}.md` | `docs/` | Quais bugs ocorreram? O que não fazer? |
| `SDD-{projeto}.md` | `docs/design/` | Qual arquitetura? Quais ADRs se aplicam? |
| `PRD-{projeto}.md` | `docs/` | Qual o escopo? Feature está aprovada? |

**Gate:** Se o `agent_context` do BREAKDOWN responde "o que existe" e "como fazer"
→ **pular Passo 2 e ir direto para Passo 4**.

> [!TIP]
> O `agent_context` bem escrito substitui 95% do History Check e 80% da leitura
> de SDD/PRD para tasks de implementação de features já mapeadas.

---

### ► Passo 2: Summary tables (Nível 2)

Se o frontmatter não foi suficiente, ler as tabelas Summary dos docs.
**Ler apenas as primeiras 80 linhas** dos docs de tracking (BREAKDOWN, PROGRESS).

```
view_file docs/BREAKDOWN-tasks.md  (linhas 1-120, não o arquivo inteiro)
view_file docs/INDEX.md            (completo — é sempre curto)
```

---

### ► Passo 3: RETRO / Lições (Nível 3)

Ler `docs/RETRO-{projeto}-v{N}.md` — documento de retrospectiva com bugs
conhecidos e decisões tomadas. É compacto por design.

**Padrão de busca dentro do RETRO:**
```bash
grep -n "<keyword da task>" docs/RETRO-*.md
```

Se o RETRO responder "já tentamos isso e o problema foi X" → não precisar ler SDD.

---

### ► Passo 4: Seção específica do SDD/PRD (Nível 4)

**NUNCA ler o SDD ou PRD inteiros.** Identificar a seção pelo índice e ler só ela.

```bash
# Primeiro: encontrar o número da linha da seção
grep -n "## <keyword>" docs/design/SDD-*.md | head -5

# Depois: ler apenas aquela seção (~50-100 linhas)
view_file docs/design/SDD-flyee.md --start <linha> --end <linha+80>
```

Seções mais acessadas por tipo de task:

| Tipo de task | Seção do SDD | Seção do PRD |
|---|---|---|
| Nova feature | Sec 2 (features) + Sec 13 (impl order) | Sec 6 (requirements) |
| SDK / endpoint | Sec 3.2 (SDK modules) | N/A |
| UI / componente | Sec 5 (component patterns) | N/A |
| Bug / comportamento | Sec 4 (data flow) + Sec 9 (error handling) | N/A |
| ADR / decisão | Sec 10 (ADRs) | N/A |

---

### ► Passo 5: Arquivo de código afetado (Nível 5)

Ler o arquivo específico que será alterado + verificar `CODEBASE.md` para
dependentes. **Não ler mais arquivos além do necessário.**

```bash
# Antes de ler código: verificar dependentes
grep -n "<nome-do-arquivo>" docs/CODEBASE.md
```

---

### ► Passo 6: Resource Discovery (Nível 6 — quando necessário)

Somente se Passos 0–5 não responderam às perguntas de implementação.

#### Caminho A — Resources Locais

**Condição:** `.agent/project-resources.json` existe.

```bash
cat .agent/project-resources.json   # ler inteiro — é sempre pequeno
```

Para cada resource, comparar `scope[]` com keywords da task.
Match → `view_file` no `path` do resource.

#### Caminho B — Busca Semântica Flyee

**Condição:** `flyee.json` existe AND `enabled: true`.

```bash
python3 .agent/flyee-bridge/bridge.py --search-context "<keywords da task>"
```

Output: JSON com resultados semânticos. Ler apenas `results[]`, não a lista
completa de tasks.

> [!WARNING]
> **NÃO usar `--list-tasks`** para contexto — retorna apenas IDs sem conteúdo.
> Usar `--search-context` que retorna conteúdo semanticamente relevante.

---

## 🚨 ANTI-PATTERNS (com custo real de tokens)

| ❌ Anti-pattern | Custo | ✅ Correto |
|---|---|---|
| Ler PRD inteiro (~700 linhas) | ~8.000 tokens | Ler `agent_context` frontmatter (~80 tokens) |
| Ler SDD inteiro (~1.200 linhas) | ~15.000 tokens | Ler seção específica via grep |
| `bridge --list-tasks` para contexto | ~500 tokens de lista vazia | `agent_context` do BREAKDOWN |
| Histórico de conversa como contexto | Explode context window | RETRO + BREAKDOWN frontmatter |
| Analisar código de outros projetos | Ruído + tokens | `PADRÕES ESTABELECIDOS` no frontmatter |
| `find docs/ -name "*.md"` | Lento + irrelevante | Ler `docs/INDEX.md` |
| Ler arquivo de código sem verificar deps | Bug silencioso | CODEBASE.md primeiro |

> [!WARNING]
> **Caso real (Task #21):** Agente retomou conversa truncada e saltou Context
> Gathering. Inferiu tipos a partir do código, ignorando docs de fluxo.
> Resultado: decisão incorreta que causaria bug em runtime.
>
> **Prevenção:** Passo 0 (INDEX.md) + Passo 1 (frontmatter) tomam < 200 tokens
> e evitam este problema completamente.

---

## 📊 CHECKLIST DE EVIDÊNCIA (compacto)

```markdown
📖 CONTEXT — {título da task}
[ ] INDEX.md lido — docs existentes mapeados
[ ] Frontmatter BREAKDOWN lido — padrões e estado atual conhecidos
[ ] RETRO consultado (grep) — bugs conhecidos checados
[ ] Seção SDD relevante lida (ou N/A com justificativa)
[ ] Arquivo afetado + CODEBASE.md verificado

DECISÕES RELEVANTES: {bullet com as que impactam a task}
PADRÕES A SEGUIR: {bullet com SDK/hooks/styles confirmados}
RESTRIÇÕES: {bullet — o que NÃO fazer}
```

---

## ✅ GATE DE SAÍDA (mínimo para prosseguir)

Antes de escrever código, confirmar:
- [ ] Sei o que **já existe** no projeto (não vou reinventar)
- [ ] Sei qual **padrão** seguir (SDK, hooks, styles)
- [ ] Sei quais **restrições** se aplicam (ADRs, imports proibidos)
- [ ] Sei quais **arquivos** serão afetados e se há dependentes

Se algum desses pontos não foi respondido em Nível 1–4 → subir um nível.
Se nenhum doc responde → registrar: `"⚠️ Docs ausentes — implementar com base no padrão mais próximo e documentar decisão"`

---

## 🔄 RE-CHECK NO RESUME (conversa truncada)

Ao retomar uma conversa truncada:

1. Ir direto ao **Nível 1** (frontmatter do BREAKDOWN)
2. Se `agent_context` existe e está atualizado → **contexto restaurado em ~100 tokens**
3. Se RETRO existe → verificar bugs com `grep -n "<keyword>" docs/RETRO-*.md`
4. **NÃO tentar reler o histórico de conversa** — nunca é eficiente

> [!TIP]
> Um `agent_context` bem mantido no BREAKDOWN é a única ferramenta que garante
> retomada de contexto sem explodir a janela. É o "cache" do projeto.

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Fase | Nível mínimo |
|----------|------|-------------|
| `/execute` | Fase 4 (EXECUTE) | Nível 1–4 |
| `/new-task` | Fase 3 (EXECUTION) | Nível 1–4 |
| `/tdd` | Phase 6 (IMPLEMENT) | Nível 1–3 |
| `/new-project` | Phase 5 (CODE) | Nível 1–5 |
| `/legacy-project` | Phase 7B Passo 0 | Nível 1–5 |
| `/debug` | Qualquer fase | Nível 1–5 |
