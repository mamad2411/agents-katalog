---
name: career-dev-kit
description: AI career ops command center — evaluate offers, engineer resumes, optimize LinkedIn, scan portals, prospect hidden market, track applications
user_invocable: true
args: mode
---

# career-dev-kit -- Router

## Mode Routing

Determine the mode from `{{mode}}`:

| Input | Mode |
|-------|------|
| (empty / no args) | `discovery` -- Show command menu |
| JD text or URL (no sub-command) | **`auto-pipeline`** |
| `evaluate` | `evaluate` |
| `resume` | `resume` |
| `linkedin` | `linkedin` |
| `pdf` | `pdf` |
| `hidden-market` | `hidden-market` |
| `scan` | `scan` |
| `tracker` | `tracker` |
| `apply` | `apply` |
| `interview` | `interview` |
| `outreach` | `outreach` |
| `batch` | `batch` |
| `training` | `training` |
| `project` | `project` |

**Auto-pipeline detection:** If `{{mode}}` is not a known sub-command AND contains JD text (keywords: "responsibilities", "requirements", "qualifications", "about the role", "we're looking for", "requisitos", "atribuições", "responsável por", company name + role) or a URL to a JD, execute `auto-pipeline`.

If `{{mode}}` is not a sub-command AND doesn't look like a JD, show discovery.

---

## Discovery Mode (no arguments)

Show this menu:

```
career-dev-kit -- Command Center

Available commands:
  /career-dev-kit {JD}         → AUTO-PIPELINE: evaluate + report + PDF + tracker (cole texto ou URL)
  /career-dev-kit evaluate     → Avaliação A-F com 4 audiências (ATS/RH/Tech/Mercado)
  /career-dev-kit resume       → Engenharia de currículo (domain intelligence + skill validation)
  /career-dev-kit linkedin     → Otimização de LinkedIn (headhunter tech + ATS)
  /career-dev-kit pdf          → PDF ATS-optimizado (HTML template + Playwright)
  /career-dev-kit hidden-market → Mercado oculto (canais + empresas + outreach)
  /career-dev-kit scan         → Scanner de portais (Playwright + API + WebSearch)
  /career-dev-kit tracker      → Status de candidaturas
  /career-dev-kit apply        → Assistente de aplicação (lê formulário + gera respostas)
  /career-dev-kit interview    → Preparação de entrevista + story bank STAR+R
  /career-dev-kit outreach     → Mensagens de abordagem por persona (recruiter/CTO/founder)
  /career-dev-kit batch        → Processamento em lote com workers paralelos
  /career-dev-kit training     → Avaliar curso/cert contra suas metas
  /career-dev-kit project      → Avaliar ideia de projeto de portfólio

Inbox: adicione URLs em data/pipeline.md → /career-dev-kit scan
Ou cole uma JD diretamente para rodar o pipeline completo.
```

---

## Context Loading by Mode

After determining the mode, load the necessary files before executing:

### Modes that require `_shared.md` + their mode file:
Read `modes/_shared.md` + `modes/{mode}.md`

Applies to: `auto-pipeline`, `evaluate`, `resume`, `linkedin`, `pdf`, `hidden-market`, `scan`, `apply`, `outreach`, `batch`

### Standalone modes (only their mode file):
Read `modes/{mode}.md`

Applies to: `tracker`, `interview`, `training`, `project`

### Knowledge Base Loading by Mode

Each mode specifies which headhunter knowledge files to load. **Only load what the mode requests.**

| Mode | Skills (headhunter-knowledge/skills/) | Guia Completo Sections | Ementas (optional deep-dive) |
|------|---------------------------------------|----------------------|------------------------------|
| `evaluate` | SKILL_HEADHUNTER_RESUME.md | Seções 2,3,4,5,7 | psicologia, gestao-pessoas |
| `resume` | SKILL_HEADHUNTER_RESUME.md | Seções 3,5 | gestao-pessoas |
| `linkedin` | SKILL_HEADHUNTER_LINKEDIN.md | Seção 6 | relacoes-humanas |
| `interview-prep` | SKILL_HEADHUNTER_SELLING.md | Seções 3,5,6 | relacoes-humanas, psicologia |
| `outreach` | SKILL_HEADHUNTER_SELLING.md, SKILL_HEADHUNTER_LINKEDIN.md | Seção 6 | relacoes-humanas |
| `apply` | SKILL_HEADHUNTER_SELLING.md (Fase 4) | Seção 6 | — |
| `hidden-market` | SKILL_HEADHUNTER_SELLING.md | Seções 6,7 | headhunting |
| `scan` | — | Seção 7 | headhunting |
| `training` | SKILL_HEADHUNTER_PDI.md | Seção 3 | — |
| `project` | SKILL_HEADHUNTER_RESUME.md (E1-E5) | Seção 5 | — |
| `auto-pipeline` | All from evaluate + pdf + apply | Seção 8 | — |
| `pdf` | SKILL_HEADHUNTER_RESUME.md (ATS rules) | — | — |
| `tracker` | — | — | — |
| `batch` | — | — | — |

**Loading priority:** `modes/_shared.md` → `modes/{mode}.md` → Skills → Guia Completo sections → Ementas (only if needed for depth)

### Modes delegated to subagent:
For `scan`, `apply` (with Playwright), and `batch`: launch as Agent with the content of `_shared.md` + `modes/{mode}.md` + relevant knowledge files injected into the subagent prompt.

```
Agent(
  subagent_type="general-purpose",
  prompt="[content of modes/_shared.md]\n\n[content of modes/{mode}.md]\n\n[relevant skill content]\n\n[relevant guia section]\n\n[invocation-specific data]",
  description="career-dev-kit {mode}"
)
```

Execute the instructions from the loaded mode file.
