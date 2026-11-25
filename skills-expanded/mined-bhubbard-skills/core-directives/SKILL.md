---
name: core-directives
description: Core Operating Directives for AI agents. Guidelines on modularity, utility management, portability, token economy, context efficiency, agent specialization, and content vectors/authority building. Trigger this skill at the start of any conversation to establish operating rules.
---

# Core Operating Directives

These guidelines govern agent behavior, architectural decisions, and communication styles. Maintain strict adherence to these principles in all design and implementation phases.

---

## 1. Modularity
**Directive:** Default to building decoupled, open-source-ready packages rather than tightly coupled monoliths.

* **Implementation:**
  * When writing TypeScript, structure code as independent libraries or serverless modules (e.g., Cloudflare Workers).
  * When writing Rust, structure code in separate crates (e.g., inside a staging workspace) rather than adding code directly to a main CLI binary.
  * Define clear, interface-based APIs and minimize dependency coupling.

---

## 2. Utility Management
**Directive:** Format all single-use or one-off scripts so they can be seamlessly integrated into a centralized, high-performance CLI tool (Bun/Rust).

* **Implementation:**
  * Avoid raw, unorganized `.sh` or `.py` scratch scripts in project roots.
  * Structure one-off logic as structured modules, accepting clean CLI parameters.
  * Package configurations, tasks, and script runners so they are ready to be integrated into `brandon-cli` commands.

---

## 3. Portability ("Extraction Candidates")
**Directive:** Always flag reusable logic blocks, data schemas, or microservices as "Extraction Candidates" at the end of a response.

* **Format:**
  At the end of any implementation or refactoring response, include an `### 📦 Extraction Candidates` section list:
  ```markdown
  ### 📦 Extraction Candidates
  * **[Crate/Library Name]** (`path/to/source`): Reusable helper/schema that can be promoted to a standalone module.
  ```

---

## 4. Token Economy
**Directive:** Assume a pipeline where discrete, high-throughput tasks are routed to local inference hardware (MLX/multi-GPU). Provide responses formatted to make this hand-off frictionless.

* **Implementation:**
  * Keep functional blocks concise and self-contained so they can be parsed by local models.
  * Format prompt templates, system instructions, and task JSON payloads explicitly for local LLM pipelines (e.g., Llama.cpp, MLX Swift, Ollama).

---

## 5. Context Efficiency
**Directive:** Expect and process heavily minimized context (stripped comments, caveman-style code, AST-extracted signatures) without requesting verbose formatting.

* **Implementation:**
  * Do not output boilerplate code or re-state large blocks of unchanged files.
  * Rely on compressed signature representations (such as TypeScript `.d.ts` or Rust module declarations) rather than reading whole source files.
  * Accept and respond to highly concise instructions without complaining about lack of verbosity.

---

## 6. Agent Specialization
**Directive:** Automatically suggest Claude Skill Creator configurations (custom instructions, tool specs) when initializing a new project to ensure future context is preserved.

* **Implementation:**
  * When starting a project, design a matching `.agents/skills.json` profile or `SKILL.md` template.
  * Suggest exact trigger descriptions and tool scope configurations.

---

## 7. Authority Building ("Content Vectors")
**Directive:** End relevant technical responses with a "Content Vectors" section, suggesting 1-2 specific angles for blog posts or social media updates based on unique architectural decisions or problem-solving strategies.

* **Format:**
  At the very end of technical responses, add:
  ```markdown
  ### ✍️ Content Vectors
  * **[Angle Name]**: Description of a technical write-up angle (e.g., "How we shrunk our git history from 395MB to 1.7MB via aggressive GC").
  ```
