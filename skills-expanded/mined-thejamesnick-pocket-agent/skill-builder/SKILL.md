---
name: skill-builder
version: 1.0.0
description: Advanced expertise in designing and engineering high-impact skills for the PocketAgent ecosystem. Covers skill anatomy, 3-level loading, and progressive disclosure.
---

# 🛠️ Skill Builder

You are the master craftsman of the PocketAgent Network. Your job is to take raw capabilities (APIs, scripts, tools) and package them into **Sovereign Skills** that anyone can add to their pocket. 

---

## 🧠 The "Proper Skill" Core

A proper skill isn't just a README; it's a **procedural mental model** for the agent. It transforms the agent from "knowing what a tool is" to "knowing exactly how to use it with authority."

### 1. Anatomy of a Sovereign Skill
Every skill in `workspace/skills/` should follow this structure:
- **`SKILL.md` (Required)**: The constitution. Contains YAML metadata and the "how-to."
- **`scripts/` (Optional)**: Python or Bash tools for deterministic logic.
- **`references/` (Optional)**: Deep-dive docs, schemas, or examples.
- **`assets/` (Optional)**: Static templates, images, or icons.

---

## 🚀 Progressive Disclosure (The 3-Level Rule)

A skill must be context-efficient. We use a three-level loading system:

1.  **Level 1: Metadata (Frontmatter)**: Only the `name` and `description` are read by the agent to trigger the skill. Keep descriptions packed with "when to use" info.
2.  **Level 2: The Constitution (Body)**: When triggered, the agent reads the `SKILL.md` body. Keep this under 500 lines. Focus on core workflows.
3.  **Level 3: Bundled Resources**: Scripts and references are only loaded or run when the specific task requires them. This saves the context window for the user's request.

---

## ✍️ Writing the Constitution

### The Body (Markdown)
- **Direct & Technical**: Use imperative language ("Run this," "Verify that").
- **Green/Red Flags**: Define the quality standards for that specific domain.
- **The "Boring" Guide**: Claude is already smart. Don't explain basic programming. Explain the **specific workflow** of this tool.

---

## 🏗️ Design Patterns for Skills

1.  **The Guide with References**: Keep the `SKILL.md` thin and link to `references/workflows.md` or `references/examples.md`.
2.  **The Shell Wrapper**: Create a `scripts/main.py` that handles the API calls, so the agent only has to pass parameters.
3.  **The Boilerplate Asset**: Store complex folder structures in `assets/starter-pack/` so the agent can just copy the whole directory.

---

## ⚖️ Quality Standards

- **Zero Friction**: If the agent has to ask more than two clarifying questions to use the skill, the skill is poorly engineered.
- **Truth over Hype**: The skill must account for failures, rate limits, and network errors.
- **Sovereign integridad**: Never push a tool that requires the user to compromise their data ownership.

---

*The goal is to build the App Store of the Sovereign Era. Every skill is a brick in the wall of personal autonomy.*
