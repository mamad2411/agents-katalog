---
name: xskill-dev
description: Use when developing xskill itself — editing agent tool docstrings, changing the generate agent tool surface, or verifying what schema the Agno framework actually sends to the model. Covers the dump_schema workflow and where tool descriptions come from.
---

# Developing xskill

## 工具描述从哪来

Agno 框架直接把 `@tool` 装饰的 Python 函数 docstring 当作发给模型的工具描述，
参数说明也从 docstring 里解析。也就是说 docstring 就是模型上下文的一部分：

- 写给模型看，不写内部实现细节（内部细节放代码注释）。
- 系统提示词里不要再抄一遍工具清单，框架会自动注入 schema，抄了会漂移。
- generate 代理的轨迹工具在 `src/xskill/agents/traj_tools.py`，
  通用工具在 `src/xskill/agents/agent_tools.py`，
  wiki 工具在 `src/xskill/agents/llm_wiki.py`。

## 改完 docstring 必跑：dump_schema

改任何工具的 docstring 或签名之后，跑一次导出脚本，看 Agno 实际生成的
schema 是什么样，确认模型看到的和你想的一致：

```bash
/home/admin/xskill/.venv/bin/python \
  scratch/standalone-generate/tool_surface/dump_schema.py
```

输出写在同目录 `SCHEMA.txt`。对照检查：

- 每个工具的 description 是否完整、有没有被截断或混进实现细节；
- 参数名、类型、必填项是否与函数签名一致；
- 新增或删除工具后，工具总数是否符合预期（generate 面当前是 16 个）。

`SCHEMA.txt` 可以进 code review diff，reviewer 能直接看到模型侧的变化。

## 上下文预算的流式陷阱

`_wrap_with_context_mgmt` 只包 `model.invoke`。任何用 `stream=True` 跑 agent
的路径都会走 `invoke_stream`，完全绕过 compact、spill 和超长兜底，模型跑在
后端原生窗口里（DeepSeek 是 1M），而且日志里一条 CONTEXT 事件都不会有。
产品 GenerateAgent 用非流式 `agent.run()` 所以没事；写实验脚本、demo、
新 agent 入口时必须非流式，或先给 `invoke_stream` 补包装。判断预算机制
是否真在跑，看 agent.log 里有没有 CONTEXT 事件（Compacted context、
Spilled、Compact was not needed 任意一种）。

llm_cfg 里开剪裁的键名是 `enable_spill`，不是 `spill`。

## 相关材料

- 工具面设计与取舍：`docs/plans/2026-08-27-generate-tool-surface.md`
- 独立实验台（Phoenix 观测、变体对比）：`scratch/standalone-generate/`，
  入口 `run_experiment.py`，`product` 变体加载产品 traj_tools 与产品
  SYSTEM_PROMPT，是验证产品行为的首选变体。
