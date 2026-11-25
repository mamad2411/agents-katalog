# Why This Skill Is Markdown-Only

XHS Topic Strategist Skill is designed as a pure Markdown, cross-Agent, no-dependency Skill because content strategy work is mostly rule interpretation, judgment, and structured generation.

The goal is to make the Skill portable across Agents rather than tied to one runtime, product, API, or local setup.

## Design Principles

### 1. Agent-Agnostic by Default

Different users work with different Agents: Claude, Codex, Cursor Agent, Manus, ChatGPT Agent, and others.

Markdown files are easy for these Agents to read, cite, summarize, and follow. A Markdown-only design avoids locking the workflow into a single platform.

### 2. No Installation Barrier

Creators and operators should not need Python, Node, package managers, shells, virtual environments, API keys, or browser extensions to use a topic planning Skill.

The repository can be used by simply giving the files to an Agent and asking it to read `SKILL.md`.

### 3. Transparent Rules

The Skill's behavior is visible in plain text:

- Input rules are in `INPUT_SCHEMA.md`.
- Execution steps are in `WORKFLOW.md`.
- Scoring logic is in `SCORING_RULES.md`.
- Risk boundaries are in `RISK_RULES.md`.
- Output shape is in `OUTPUT_SCHEMA.md`.
- Niche rules are in `niches/`.

This makes review, modification, and contribution easier.

### 4. Safer Human-in-the-Loop Workflow

The Skill is intentionally a planning assistant, not an auto-publishing system.

It helps generate topics, titles, structures, copy drafts, and risk reminders. The creator remains responsible for facts, real experiences, product details, advertising disclosures, and final publishing decisions.

### 5. Better for Open Source

A Markdown-only repository is easier to inspect and fork. Contributors can improve niche rules, examples, translations, and risk guidance without setting up a development environment.

That simplicity is a feature, not a limitation.
