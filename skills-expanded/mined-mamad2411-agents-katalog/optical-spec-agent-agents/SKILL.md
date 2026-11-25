# AGENTS.md

## Project identity

This project is `optical-spec-agent`.

It is not a general chatbot and not a full optical simulation platform yet.
Current goal: convert natural-language optical simulation requests into a structured, provenance-aware `OpticalSpec`, validate missing/inferred/confirmed fields, and translate supported specs into solver-specific scripts.

The main current pipeline is:

```text
natural language input
→ RuleBasedParser
→ OpticalSpec
→ SpecValidator
→ CLI/API output
→ MeepAdapter
→ generated Meep Python script
```

## 项目定位

这个项目是 `optical-spec-agent`。

它现在不是通用聊天机器人，也还不是完整的光学仿真平台。
当前目标是把自然语言光学仿真需求转换成带 provenance 的结构化 `OpticalSpec`，明确字段是 `confirmed / inferred / missing`，再把受支持的 spec 翻译成 solver 脚本。

当前主链路是：

```text
natural language input
→ RuleBasedParser
→ OpticalSpec
→ SpecValidator
→ CLI/API output
→ MeepAdapter
→ generated Meep Python script
```

## Current priority

Do not expand scope unless explicitly asked.

The current development priority is productization around the strongest hero path
and safe parser evolution:

- natural language optical task
- → validated, provenance-aware `OpticalSpec`
- → Meep script generation for supported nanoparticle-on-film specs
- → optional local Meep execution artifacts when Meep is installed
- → v0.8 rule / llm / hybrid parser modes, with rule still the default
- → deterministic local mock LLM provider for tests and demos; no external API required
- → v0.9 synchronous workflow orchestration with auditable artifacts and replay

The released baseline is v0.5.0. Current v0.6 work is local/manual diagnostics
for physical-candidate stability, spectrum consistency, mesh sanity, and monitor
geometry. Current v0.7/v0.8/v0.9 main-branch work adds adapter scaffolds, LLM
parser foundation, and local workflow orchestration. Keep these capabilities
honest: they are not production validation.

## 当前优先级

除非被明确要求，否则不要主动扩 scope。

当前开发重点是围绕最强主链路和安全 parser 演进做 productization：

- 自然语言光学任务
- → 带 provenance 的结构化 `OpticalSpec`
- → 对受支持的 nanoparticle-on-film spec 生成 Meep 脚本
- → 如果本地安装 Meep，则可选生成 execution artifacts
- → v0.8 增加 rule / llm / hybrid parser 模式，但默认仍然是 rule-based
- → LLM 测试和 demo 使用确定性的本地 mock provider，不需要外部 API
- → v0.9 同步 workflow orchestration，输出可审计 artifacts 并支持 replay

已发布基线是 v0.5.0。当前 v0.6 工作是 local/manual diagnostics，包括
physical-candidate stability、spectrum consistency、mesh sanity 和 monitor geometry。
当前 v0.7/v0.8/v0.9 main branch 工作增加 adapter scaffolds、LLM parser foundation
和 local workflow orchestration。
这些能力必须保持诚实：它们不是 production validation。

## Important files

- `src/optical_spec_agent/models/spec.py`
- `src/optical_spec_agent/models/base.py`
- `src/optical_spec_agent/parsers/rule_based.py`
- `src/optical_spec_agent/validators/spec_validator.py`
- `src/optical_spec_agent/services/spec_service.py`
- `src/optical_spec_agent/adapters/meep/translator.py`
- `src/optical_spec_agent/adapters/meep/template.py`
- `src/optical_spec_agent/execution/meep_runner.py`
- `src/optical_spec_agent/analysis/`
- `src/optical_spec_agent/cli/main.py`
- `scripts/`
- `docs/`
- `benchmarks/`
- `tests/`

## Coding rules

- Prefer small, reviewable changes.
- Do not rewrite the entire parser.
- Keep LLM parsing provider-agnostic and mock-testable; do not require external APIs.
- Do not add new solver adapters yet.
- Do not add UI work yet.
- Do not silently hide missing physical parameters behind defaults.
- If a default is used, record it and report it clearly.
- Keep confirmed / inferred / missing provenance meaningful.

## 编码约定

- 优先做小范围、容易 review 的修改。
- 不要重写整个 parser。
- LLM parsing 必须 provider-agnostic 且可用 mock 测试；不要要求外部 API。
- 先不要新增其他 solver adapter。
- 先不要做 UI。
- 不要用默认值静默掩盖缺失的物理参数。
- 如果使用默认值，必须记录并清楚报告。
- 保持 `confirmed / inferred / missing` 的 provenance 有实际意义。

## Testing

Before finishing code changes, run:

```bash
pytest
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
```

If parser behavior is intentionally changed, treat exact snapshot benchmark updates as a separate explicit decision:

```bash
python benchmarks/run_benchmark.py --mode exact
```

## 测试要求

完成代码修改前，至少运行：

```bash
pytest
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
```

如果 parser 行为被有意修改，`exact` snapshot benchmark 是否更新应作为单独、明确的决定：

```bash
python benchmarks/run_benchmark.py --mode exact
```
