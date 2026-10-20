---
name: leiloeiro-category-pointer
description: "Pointer to a library of 6 specialized Leiloeiro skills. Use when working on leiloeiro-related tasks."
risk: none
---

# Leiloeiro Capability Library 🎯

This is a **pointer skill**. The 6 specialized Leiloeiro skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **leiloeiro-avaliacao** — Avaliacao pericial de imoveis em leilao. Valor de mercado, liquidacao forcada, ABNT NBR 14653, metodos comparativo/renda/custo, CUB e margem de seguranca.
- **leiloeiro-edital** — Analise e auditoria de editais de leilao judicial e extrajudicial. Riscos ocultos, clausulas perigosas, debitos, ocupante e classificacao da oportunidade.
- **leiloeiro-ia** — Especialista em leiloes judiciais e extrajudiciais de imoveis. Analise juridica, pericial e de mercado integrada. Orquestra os 5 modulos especializados.
- **leiloeiro-juridico** — Analise juridica de leiloes: nulidades, bem de familia, alienacao fiduciaria, CPC arts 829-903, Lei 9514/97, onus reais, embargos e jurisprudencia.
- **leiloeiro-mercado** — Analise de mercado imobiliario para leiloes. Liquidez, desagio tipico, ROI, estrategias de saida (flip/reforma/renda), Selic 2025 e benchmark CDI/FII.
- **leiloeiro-risco** — Analise de risco em leiloes de imoveis. Score 36 pontos, riscos juridicos/financeiros/operacionais, stress test 4 cenarios e ROI ponderado por risco.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/leiloeiro/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/leiloeiro`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
