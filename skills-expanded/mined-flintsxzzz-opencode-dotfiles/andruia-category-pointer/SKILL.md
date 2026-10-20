---
name: andruia-category-pointer
description: "Pointer to a library of 3 specialized Andruia skills. Use when working on andruia-related tasks."
risk: none
---

# Andruia Capability Library 🎯

This is a **pointer skill**. The 3 specialized Andruia skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **00-andruia-consultant** — Arquitecto de Soluciones Principal y Consultor Tecnológico de Andru.ia. Diagnostica y traza la hoja de ruta óptima para proyectos de IA en español.
- **10-andruia-skill-smith** — Ingeniero de Sistemas de Andru.ia. Diseña, redacta y despliega nuevas habilidades (skills) dentro del repositorio siguiendo el Estándar de Diamante.
- **20-andruia-niche-intelligence** — Estratega de Inteligencia de Dominio de Andru.ia. Analiza el nicho específico de un proyecto para inyectar conocimientos, regulaciones y estándares únicos del sector. Actívalo tras definir el nicho.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/andruia/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/andruia`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
