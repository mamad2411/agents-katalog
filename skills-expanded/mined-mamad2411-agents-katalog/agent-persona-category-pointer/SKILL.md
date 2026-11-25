---
name: agent-persona-category-pointer
description: "Pointer to a library of 5 specialized Agent Persona skills. Use when working on agent-persona-related tasks."
risk: none
---

# Agent Persona Capability Library 🎯

This is a **pointer skill**. The 5 specialized Agent Persona skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **bill-gates** — Agente que simula Bill Gates — cofundador da Microsoft, arquiteto da industria de software comercial, estrategista tecnologico global, investidor sistemico e filantropo baseado em dados.
- **elon-musk** — Agente que simula Elon Musk com profundidade psicologica e comunicacional de alta fidelidade. Ativado para: "fale como Elon", "simule Elon Musk", "o que Elon diria sobre X", "first principles thinking", "think like Elon", roleplay/simulacao do personagem.
- **idea-evaluator-con** — The Con Agent persona for idea evaluation. Critiques an idea by identifying potential flaws, risks, and market challenges.
- **idea-evaluator-pro** — The Pro Agent persona for idea evaluation. Logically supports an idea, arguing for its market fit, feasibility, and potential.
- **steve-jobs** — Agente que simula Steve Jobs — cofundador da Apple, CEO da Pixar, fundador da NeXT, o maior designer de produtos tecnologicos da historia e o mais influente apresentador de produtos do mundo.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/agent-persona/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/agent-persona`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
