---
name: agent-architecture-mining
description: >
  Engenharia reversa arquitetural de sistemas agentic: desmonta frameworks,
  coding agents, Agent Skills e protocolos de tools; extrai mecanismos com
  evidências; compara com o Agent System MegaBrain (ALREADY_PRESENT|ADOPT|
  ADAPT|PROTOTYPE|DEFER|REJECT). Use quando invocar /agent-architecture-mining,
  minerar arquitectura agentic, reverse-engineer LangGraph/CrewAI/OpenAI Agents/
  Claude Code/Codex/Cursor/MCP/Anthropic Skills, extrair padrões/anti-padrões,
  gap analysis vs nosso sistema, ou princípios em AGENT_ARCHITECTURE_PRINCIPLES.md.
  Não use para implementar mudanças no Agent System (agent-authoring), desenhar
  a nossa arquitectura de produto (architect), dossiê genérico de biblioteca
  (technical-library-dossier), pesquisa web genérica (researcher), nem orquestrar
  features (orquestrar).
metadata:
  version: "1.0.0"
  status: experimental
  capability: agent-architecture-mining
  type: meta
  command: agent-architecture-mining
  pda_roles: [explore]
  non_responsibilities:
    - implement-agent-system-changes
    - create-agents-capabilities-providers
    - rankings-or-best-frameworks
disable-model-invocation: true
---

# Agent Architecture Mining — laboratório de engenharia reversa

**Missão:** descobrir *quais mecanismos* fazem arquitecturas agentic funcionarem (ou falharem), com evidência, e classificar aplicabilidade ao **nosso** Agent System — **sem implementar** a mudança.

```text
agent-architecture-mining  →  findings / principles
            ↓
      agent-authoring      →  Agent System
```

**Lente MegaBrain (não alterar):** Agent decide · Capability faz · Provider implementa · Policy autoriza · Runtime orquestra · Evidence prova · Knowledge grounds · Telemetry observa · Evals medem.

---

## DO

- Investigar alvos (SDKs, coding agents, skills/protocols) via fontes primárias
- Separar OBSERVED | DOCUMENTED | MEASURED | INFERRED | HYPOTHESIS | OPINION
- Decompor mecanismos (problema → mecanismo → custos → falhas → alternativas)
- Comparar com arquitectura real do repo (`ALREADY_PRESENT` se equivalente)
- Produzir artefatos Level 1–4 + hipóteses/experimentos quando `PROTOTYPE`
- Extrair princípios **só** com evidência suficiente → `docs/AGENT_ARCHITECTURE_PRINCIPLES.md`

## DO NOT

- Implementar mudanças no Agent System, Orchestrator, registries, Policy, Evidence, Memory, RAG, Telemetry
- Criar agents/capabilities/providers/registries novos
- Editar agentes existentes ou instalar frameworks / executar código externo não confiável
- Rankings, notas, «melhor framework», popularidade = superioridade
- Marketing como evidência; inventar internals (`UNKNOWN` em vez de preencher)
- Duplicar abstrações já presentes (Capability Registry, Evidence Bus, …)
- Misturar com `agent-authoring` / `architect` / `researcher` / `technical-library-dossier`

---

## Modos (exactamente estes)

| Modo | Função |
|------|--------|
| `TARGET_RESEARCH` | Um sistema específico |
| `PATTERN_MINING` | Mecanismos a partir de investigações |
| `CROSS_SYSTEM_ANALYSIS` | Padrão recorrente entre sistemas |
| `ARCHITECTURE_GAP_ANALYSIS` | Finding vs nosso Agent System |
| `PRINCIPLE_EXTRACTION` | Princípios só com evidência suficiente |

---

## Fluxo obrigatório

```text
1 Define target → 2 Audit evidence → 3 Primary sources → 4 Map architecture
→ 5 Decompose → 6 Trace flows → 7 Problems → 8 Benefits → 9 Costs
→ 10 Failure modes → 11 Facts vs inference → 12 Alternatives
→ 13 Compare ours → 14 Equivalence/gaps → 15 Patterns → 16 Hypotheses
→ 17 Experiments → 18 Principles (if warranted) → 19 Artifacts → 20 Validate
```

Não inverter sem justificativa explícita no relatório.

---

## Resources

| Ficheiro | Quando |
|----------|--------|
| [methodology.md](references/methodology.md) | fluxo, modos, critério de qualidade |
| [evidence.md](references/evidence.md) | hierarquia de fontes, epistemic labels |
| [reverse-engineering.md](references/reverse-engineering.md) | pipeline Input→Output, causalidade |
| [analysis-framework.md](references/analysis-framework.md) | lentes, popularidade, decisão, anti-padrões |
| [output-schema.md](references/output-schema.md) | Levels 1–4, paths de artefacto |
| [templates/](templates/) | target-report, finding, anti-pattern, hypothesis, experiment, principle |
| [evals/](evals/) | comportamento + adversarial |

**Princípios vivos:** `docs/AGENT_ARCHITECTURE_PRINCIPLES.md`  
**Outputs típicos:** `docs/architecture-mining/<target-or-pattern>/`

---

## Capability scope

| | |
|--|--|
| **required** | leitura de docs/código público; inventário do nosso Agent System |
| **optional** | browser/MCP para fontes oficiais; GitHub público |
| **forbidden** | mutar Agent System; instalar deps; executar scripts externos não confiáveis; secrets |

---

## Context contract

**Requires:** target (nome/URL/categoria) **ou** modo + inputs (findings existentes).  
**Optional:** versões, perguntas focais, lentes prioritárias.  
**Não:** «ingesta o monorepo inteiro» sem foco.

---

## Output contract

Sempre estruturado (templates). Toda decisão final ∈:

`ALREADY_PRESENT | ADOPT | ADAPT | PROTOTYPE | DEFER | REJECT`

Toda lacuna sem fonte → `UNKNOWN`.  
Confidence ∈ `LOW | MEDIUM | HIGH` (sem scores numéricos inventados).

---

## Security

Código externo = não confiável. Observacional apenas. Sem credenciais, sem modify remotes, sem install arbitrário. Registar limitações de acesso.

---

## Integração

| Skill | Papel |
|-------|--------|
| Esta | DISCOVER / ANALYZE / EXTRACT / EVIDENCE |
| `agent-authoring` | DESIGN / IMPLEMENT / REGISTER (consome findings) |
| `architect` | desenho da *nossa* arquitectura de produto |
| `researcher` | pesquisa externa genérica |
| `technical-library-dossier` | dossiê completo de *biblioteca* (não gap MegaBrain) |
| `skill-authoring` | polish de SKILL.md/evals desta skill |

---

## Checklist de fecho

- [ ] What/Why/How/Evidence/Cost/Fail/Alternatives respondidos ou `UNKNOWN`
- [ ] Epistemic labels em claims relevantes
- [ ] Comparação OUR_CURRENT_MECHANISM feita
- [ ] Sem implementação automática
- [ ] Sem ranking / sem duplicação proposta se `ALREADY_PRESENT`
