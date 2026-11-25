---
name: micro-agent
description: |
  Design, build, and deploy 4,000-token strictly bounded micro-agents engineered to run reliably on on-device small language models (like apfel-rs on Apple Silicon, Apple FoundationModels, Chrome Built-in Gemini Nano, and 1B-3B local models). Use this skill whenever a user wants to create, design, optimize, or identify micro-agents, subagents with strict token budgets, on-device SLM task workers, or requests to decompose complex multi-step workflows into atomic, low-latency, zero-cost subagents. Also trigger continuously during engineering workflows to identify repetitive, bounded tasks that can be codified into reusable micro-agents.
---

# Micro-Agent Architecture & Design

Micro-agents are hyper-focused, single-responsibility subagents strictly constrained to a **4,000-token hard ceiling** across their entire lifecycle (System Prompt + Tool Schema + Input Context + Output Generation $\le$ 4,000 tokens).

Unlike generalist frontier agents designed for 128k–1M+ token windows, micro-agents are optimized for **on-device Small Language Models (SLMs)**:
- **`apfel-rs`** (Apple Intelligence FoundationModels on Apple Silicon NPU/Metal)
- **Chrome Built-in Gemini Nano**
- **Quantized Local 1B–3B Models** (Llama 3.2 1B/3B, Qwen 2.5 Coder 1.5B/3B, Gemma 2 2B)

When paired with zero-token mathematical decision engines like **[`zev-rs`](https://github.com/bhubbard/zev-rs)**, micro-agents create an edge cascade: microsecond zero-token classification $\to$ sub-100ms local micro-agent execution $\to$ zero network API cost.

---

## 📐 The 4,000-Token Budget Envelope

Every micro-agent must conform to the **4K Contract**:

| Component | Strict Token Budget | Optimization Technique |
| :--- | :--- | :--- |
| **System Prompt & Role** | **150 – 300 tokens** | Imperative, zero fluff, explicit output schema, no conversational persona. |
| **Tool Definition** | **0 – 300 tokens** | Zero-or-one tool policy. Prefer pure string-to-string transforms or JSON. |
| **Input Context Payload** | **2,000 – 2,500 tokens** | Pre-filtered AST slice, compiler stderr, or isolated function diff. Never entire files. |
| **Output Generation** | **500 – 1,000 tokens** | Direct replacement patch, structured JSON, or concise commit message. |
| **TOTAL** | **$\le$ 4,000 tokens** | **Guaranteed zero truncation on Apple Silicon FoundationModels.** |

---

## 🏛️ Micro-Agent Archetypes

Micro-agents strictly adhere to the **Single Responsibility Principle (SRP)**. Never combine multiple orthogonal tasks into one micro-agent.

```
                    ┌────────────────────────┐
                    │ Parent Agent / Zev-RS  │
                    └───────────┬────────────┘
              Cascades to       │ (< 4,000 tokens)
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
 ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
 │    Healer    │        │ Synthesizer  │        │  Classifier  │
 │(Compiler/Lint)│        │(Tests/Commits)│       │ (Route/Triage)│
 └──────────────┘        └──────────────┘        └──────────────┘
```

### 1. The Healer (Compiler & Lint Fixer)
- **Role**: Takes a compiler error diagnostic (`rustc`, `tsc`, `clippy`) and 15–30 surrounding code lines.
- **Output**: Unified patch or replacement lines.
- **Example**: [`catalog/rust-compiler-healer.md`](catalog/rust-compiler-healer.md), [`catalog/rustc-borrow-healer.md`](catalog/rustc-borrow-healer.md).

### 2. The Synthesizer (Tests & Documentation)
- **Role**: Takes an isolated struct/function signature and generates 3 edge-case tests or docstrings.
- **Output**: Code block with `#[test]` or standard doc comments.
- **Example**: [`catalog/unit-test-synthesizer.md`](catalog/unit-test-synthesizer.md).

### 3. The Committer (Changelog & Commits)
- **Role**: Takes `git diff --stat` and key diff chunks; produces conventional commit message.
- **Output**: `feat(scope): concise summary` + 3 bullet points.
- **Example**: [`catalog/conventional-committer.md`](catalog/conventional-committer.md).

### 4. The Transformer (AST & API Refactor)
- **Role**: Rewrites deprecated function calls or transforms one data structure into another.
- **Output**: Clean replacement code.
- **Example**: [`catalog/ast-refactor-transformer.md`](catalog/ast-refactor-transformer.md), [`catalog/glam-transform-bridge.md`](catalog/glam-transform-bridge.md).

### 5. The Schema Validator & Repairer
- **Role**: Takes malformed or incomplete JSON/YAML and repairs it to conform to a target schema.
- **Output**: Strictly valid JSON with zero conversational commentary.
- **Example**: [`catalog/schema-validator.md`](catalog/schema-validator.md), [`catalog/astro-schema-ld-scaffolder.md`](catalog/astro-schema-ld-scaffolder.md).

---

## 📚 Complete Micro-Agent Catalog (51 Agents)

| Micro-Agent | Primary Cluster | Role & Responsibility | Measured Tokens |
| :--- | :--- | :--- | :--- |
| [`cinematic-prompt-enhancer`](catalog/cinematic-prompt-enhancer.md) | Generative MLX | Expands raw prompts into 35mm cinematic lighting & camera specs | 258 tokens |
| [`mlx-safetensors-key-mapper`](catalog/mlx-safetensors-key-mapper.md) | Generative MLX | Maps PyTorch/Diffusers state_dict keys to MLX flattened/native keys | 260 tokens |
| [`flow-matching-sigma-calculator`](catalog/flow-matching-sigma-calculator.md) | Generative MLX | Computes shifted discrete sigma sequences for flow matching schedulers | 210 tokens |
| [`lora-delta-calculator`](catalog/lora-delta-calculator.md) | Generative MLX | Calculates LoRA rank, alpha, and scaling factor for matrix delta fusion | 230 tokens |
| [`hyperframes-motion-designer`](catalog/hyperframes-motion-designer.md) | HyperFrames | Generates mathematical Bezier & spring progress logic for `window.__hf` | 332 tokens |
| [`comfyui-node-rewirer`](catalog/comfyui-node-rewirer.md) | ComfyUI / LTX | Verifies socket type parity and links graph nodes | 227 tokens |
| [`bevy-component-scaffolder`](catalog/bevy-component-scaffolder.md) | Game Engine / ECS | Converts C++/GDScript gameplay structs into Bevy ECS components | 272 tokens |
| [`glam-transform-bridge`](catalog/glam-transform-bridge.md) | Game Physics | Synthesizes `glam::Mat4` and `glam::Quat` affine transformations | 252 tokens |
| [`spring-physics-converter`](catalog/spring-physics-converter.md) | Motion Design | Converts physical spring triplets to designer response/damping parameters | 280 tokens |
| [`mobile-tap-safety-fixer`](catalog/mobile-tap-safety-fixer.md) | Mobile Native | Patches buttons with touch-action, tap-highlight suppression, and 44px min-size | 250 tokens |
| [`layout-shift-cls-healer`](catalog/layout-shift-cls-healer.md) | Web Performance | Injects explicit aspect-ratio and dimensions to guarantee CLS = 0 | 240 tokens |
| [`tailwind-class-sorter`](catalog/tailwind-class-sorter.md) | Frontend CSS | Reorders utility classes by box-model cascade specificity | 240 tokens |
| [`accessible-alt-text`](catalog/accessible-alt-text.md) | A11y & SEO | Generates concise WCAG 2.2 AA compliant image descriptions | 244 tokens |
| [`edge-vision-alt-tagger`](catalog/edge-vision-alt-tagger.md) | Cloudflare Edge AI | Generates concise WCAG 2.2 AA alt text and SEO image title from vision tags | 250 tokens |
| [`natural-to-awk`](catalog/natural-to-awk.md) | CLI & Logs | Translates natural-language log extraction into single-line `awk` commands | 194 tokens |
| [`astro-schema-ld-scaffolder`](catalog/astro-schema-ld-scaffolder.md) | Astro Web | Generates valid Schema.org JSON-LD `<script>` graphs from frontmatter | 295 tokens |
| [`hydration-island-advisor`](catalog/hydration-island-advisor.md) | Astro Web | Recommends optimal island hydration directives (`client:visible`, etc.) | 282 tokens |
| [`cloudflare-d1-migration-maker`](catalog/cloudflare-d1-migration-maker.md) | Cloudflare Edge | Generates forward SQLite DDL migrations from TypeScript entity diffs | 338 tokens |
| [`cloudflare-waf-rule-builder`](catalog/cloudflare-waf-rule-builder.md) | Cloudflare Edge | Translates natural security policies into Wirefilter / Ruleset Engine expressions | 270 tokens |
| [`edge-cache-control-optimizer`](catalog/edge-cache-control-optimizer.md) | Cloudflare Edge | Synthesizes optimal Cache-Control, CDN-Cache-Control, and Cache-Tag headers | 260 tokens |
| [`wrangler-binding-auditor`](catalog/wrangler-binding-auditor.md) | Cloudflare Edge | Audits Worker code against wrangler.toml to identify missing bindings | 280 tokens |
| [`turnstile-edge-validator`](catalog/turnstile-edge-validator.md) | Edge Security | Generates zero-dependency Turnstile siteverify token validation functions | 320 tokens |
| [`op-secret-reference-scrubber`](catalog/op-secret-reference-scrubber.md) | Secrets & Security | Sanitizes plaintext secrets into canonical `op://vault/item/field` references | 230 tokens |
| [`op-dotenv-injector`](catalog/op-dotenv-injector.md) | Secrets & Security | Generates `op run` command strings and injected `.env.op` templates | 260 tokens |
| [`leaddocket-webhook-triage-parser`](catalog/leaddocket-webhook-triage-parser.md) | Legal CRM | Normalizes raw LeadDocket webhook intake payloads into structured JSON | 280 tokens |
| [`filevine-custom-field-sanitizer`](catalog/filevine-custom-field-sanitizer.md) | Legal Tech | Sanitizes custom field labels into camelCase Filevine selector codes | 210 tokens |
| [`opendental-cdt-code-mapper`](catalog/opendental-cdt-code-mapper.md) | Dental EHR | Maps clinical dental procedure terms to canonical ADA CDT procedure codes | 320 tokens |
| [`opendental-tooth-number-normalizer`](catalog/opendental-tooth-number-normalizer.md) | Dental EHR | Normalizes tooth IDs between Universal (1-32, A-T), FDI (11-85), and Palmer | 220 tokens |
| [`serp-rank-delta-calculator`](catalog/serp-rank-delta-calculator.md) | SERP & Tracking | Computes rank position displacement, volatility scores, and SERP features | 280 tokens |
| [`keyword-search-intent-classifier`](catalog/keyword-search-intent-classifier.md) | SEO & Search | Classifies queries into Informational, Navigational, Commercial, Transactional | 240 tokens |
| [`xml-sitemap-index-validator`](catalog/xml-sitemap-index-validator.md) | Technical SEO | Audits XML sitemaps for W3C schema compliance, URL counts, and lastmod dates | 270 tokens |
| [`fonoster-call-flow-scaffolder`](catalog/fonoster-call-flow-scaffolder.md) | Telephony | Scaffolds Fonoster Voice JavaScript handlers with speech and DTMF gathers | 340 tokens |
| [`e164-phone-normalizer`](catalog/e164-phone-normalizer.md) | Telephony | Canonicalizes phone numbers to ITU-T E.164 with toll-free detection | 230 tokens |
| [`decision-model-benchmark-evaluator`](catalog/decision-model-benchmark-evaluator.md) | Decision Models | Evaluates model choices, Bradley-Terry probabilities, and transitivity checks | 290 tokens |
| [`timesfm-forecast-patch-tokenizer`](catalog/timesfm-forecast-patch-tokenizer.md) | Foundation Models | Normalizes time-series and tokenizes series into fixed-length forecast patches | 290 tokens |
| [`obj-mesh-normal-recalculator`](catalog/obj-mesh-normal-recalculator.md) | 3D Geometry | Computes area-weighted vertex normals from triangle mesh faces | 310 tokens |
| [`modular-snap-socket-aligner`](catalog/modular-snap-socket-aligner.md) | 3D Kitbash | Computes affine rigid transform (translation + quat) to snap modular sockets | 280 tokens |
| [`water-spectrum-dispersion-calculator`](catalog/water-spectrum-dispersion-calculator.md) | Fluid Physics | Computes shallow water wave dispersion frequency and 60-second loop quantization | 240 tokens |
| [`pacejka-tire-friction-calculator`](catalog/pacejka-tire-friction-calculator.md) | Vehicle Dynamics | Evaluates Pacejka Magic Formula for lateral cornering grip and tire forces | 260 tokens |
| [`conventional-committer`](catalog/conventional-committer.md) | Git Engineering | Synthesizes Conventional Commit messages from `git diff --stat` | 273 tokens |
| [`unit-test-synthesizer`](catalog/unit-test-synthesizer.md) | Testing / QA | Synthesizes happy-path, boundary, and error tests for a single function | 328 tokens |
| [`c2rust-function-porter`](catalog/c2rust-function-porter.md) | Code Porting | Transpiles isolated C++/C#/Python functions into idiomatic safe Rust | 351 tokens |
| [`c2rust-test-porter`](catalog/c2rust-test-porter.md) | Code Porting | Converts GoogleTest/Catch2/pytest test suites to standard `#[test]` Rust | 326 tokens |
| [`c2rust-type-scaffolder`](catalog/c2rust-type-scaffolder.md) | Code Porting | Maps C++ structs, enums, and smart pointers to idiomatic Rust types | 345 tokens |
| [`c2rust-crate-mapper`](catalog/c2rust-crate-mapper.md) | Code Porting | Maps C++ `#include` headers to modern Rust crates with `Cargo.toml` lines | 321 tokens |
| [`cpp-oop-to-data-oriented`](catalog/cpp-oop-to-data-oriented.md) | Code Porting | Converts C++ OOP virtual class hierarchies into Rust Data-Oriented enums | 432 tokens |
| [`rust-compiler-healer`](catalog/rust-compiler-healer.md) | Rust Systems | One-shot patch generator for syntax and type mismatch errors | 219 tokens |
| [`rustc-borrow-healer`](catalog/rustc-borrow-healer.md) | Rust Systems | Resolves E0382, E0499, and E0502 borrow-checker diagnostics | 256 tokens |
| [`rustc-error-burn-down`](catalog/rustc-error-burn-down.md) | Code Porting | Generates surgical 1-line patches for specific `rustc` diagnostic errors | 343 tokens |
| [`ast-refactor-transformer`](catalog/ast-refactor-transformer.md) | Refactoring | Replaces deprecated API patterns with modern idioms | 171 tokens |
| [`schema-validator`](catalog/schema-validator.md) | Data Quality | Heals corrupted or truncated JSON/YAML payloads | 157 tokens |

---

## 🏛️ The 5-Pillar Architecture Evolution

To eliminate model hallucinations, context blindness, prompt rot, and orchestration latency, the micro-agent framework enforces five architectural pillars:

### 1. The Tier 0 Rule (Zero-Token Deterministic Engine)
If a task can be expressed as a pure function, closed-form math equation, or regular expression, **an LLM is strictly banned from executing it**.
- Dedicated tool: [`tools/tier0_deterministic.py`](tools/tier0_deterministic.py)
- Features: Flow matching sigmas (nanoseconds), Filevine camelCase sanitization (microseconds), Apple fluid spring physics calculations, LoRA scale multipliers, Tailwind CSS cascade sorting, E.164 phone canonicalization, Pacejka tire friction, tooth notation conversion, and ocean wave dispersion.

### 2. Guaranteed Output Reliability via Grammar-Guided Sampling
Small models (1B–3B) must never output free-form text when structured data is expected.
- Documentation: [`references/grammar_guided_decoding.md`](references/grammar_guided_decoding.md)
- Logit Masking: In `apfel-rs` and `mlx-lm`, token logits are constrained via GBNF or JSON Schema state machines, making syntax errors, missing braces, and conversational pleasantries physically impossible.

### 3. AST-Hydrated Slices (Eliminating Context Blindness)
Never pass a blind 15-line code window to a code repair micro-agent.
- Documentation: [`references/ast_hydrated_slicing.md`](references/ast_hydrated_slicing.md)
- The Dependency Triad: Every code micro-agent receives (1) the diagnostic error span, (2) the enclosing function AST call site, and (3) the target struct/trait definition site.
- Auto-Escalation Gate: If an error crosses $>2$ files or external crate trait bounds, the micro-agent automatically bails and escalates to the frontier workspace agent.

### 4. Automated CI Regression Suite (`eval_catalog.py`)
Prompts without regression tests rot silently over time.
- Test runner: [`scripts/eval_catalog.py`](scripts/eval_catalog.py)
- Audits all 51 catalog markdown specifications in CI: verifies the 4K envelope, validates output contract syntax, tests Tier 0 deterministic tool parity, and asserts verification harness integrity.
- Run locally or in GitHub Actions:
  ```bash
  python3 skills/micro-agent/scripts/eval_catalog.py
  ```

### 5. Orchestration Modes (Eliminating the Multi-Hop Tax)
Never chain 6 micro-agents in serial to solve a multi-file system task.
- Documentation: [`references/orchestration_patterns.md`](references/orchestration_patterns.md)
- The Frontier Toolbelt: The Frontier Model (Claude / Gemini) maintains the 200k repository context and system architecture, invoking micro-agents and Tier 0 tools as **instantaneous zero-cost worker tools** within its tool loop.

---

## 🔍 Continuous Discovery: Identifying Candidates Across Projects

While working in any repository (`~/PROJECTS`), proactively scan for operations that can be codified into micro-agents or Tier 0 tools. 

### The 4-Filter Discovery Heuristic:
1. **Bounded Context**: Can the input payload be trimmed to $< 2,000$ tokens without losing critical context?
2. **Single-Shot**: Can the task be solved in exactly **one model turn** without conversational back-and-forth?
3. **Deterministic Output**: Can the output format be specified as a rigid patch, JSON object, or short text block?
4. **Repetitive Velocity**: Will this operation occur frequently across repos (e.g. fixing borrow-checker errors, writing release notes, generating mock data)?

**Action**: When all 4 criteria are met, create a new specification in `skills/micro-agent/catalog/<name>.md`.

---

## ⚡ Integration with `apfel-rs` and `zev-rs`

On Apple Silicon machines:
1. **Stage 0 (`zev-rs`)**: Ultra-fast calibrated probabilistic routing in **5.8 microseconds** with zero tokens.
2. **Stage 1 (`apfel-rs` Micro-Agent + Verification Harness)**: On-device execution via Apple FoundationModels / CoreML in **< 100 milliseconds** within the 4k-token budget with grammar-guided logit masking. Deterministic harness checks output; if valid, commit immediately.
3. **Stage 2 (Frontier Subagent)**: Escalate to Claude / Gemini only when Stage 1 verification fails or when multi-file repo synthesis exceeds 4,000 tokens.

Read [`references/apfel_integration.md`](references/apfel_integration.md) for concrete Rust/Swift bridging code.

---

## 🛠️ Step-by-Step: How to Build a New Micro-Agent

1. **Check Tier 0 First**: If the operation is arithmetic or regex, write a deterministic function in `tools/tier0_deterministic.py`.
2. **Define the Single Responsibility**: State exactly one input type and one output type.
3. **Write the Lean System Prompt**: Use [`templates/micro_agent_prompt.md`](templates/micro_agent_prompt.md) to keep it under 200 tokens.
4. **Establish AST Triad Input Pruning**: Extract the diagnostic, call site AST, and definition site AST.
5. **Run the CI Evaluation Suite**:
   ```bash
   python3 skills/micro-agent/scripts/eval_catalog.py
   ```
6. **Publish to Catalog**: Commit the new micro-agent to `skills/micro-agent/catalog/`.

