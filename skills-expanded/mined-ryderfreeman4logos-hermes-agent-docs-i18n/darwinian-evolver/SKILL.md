---
name: darwinian-evolver
description: Evolve prompts/regex/SQL/code with Imbue's evolution loop.
version: 0.1.0
author: Bihruze (Asahi0x), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [evolution, optimization, prompt-engineering, research]
    related_skills: [arxiv, jupyter-notebook]
---

# 达尔文进化器

运行 Imbue 提供的 [darwinian_evolver](https://github.com/imbue-ai/darwinian_evolver) —— 一种由大语言模型驱动的进化搜索算法 —— 以便根据适应度函数优化**提示词、正则表达式、SQL 查询或小型代码片段**。

状态：该技能仅为上游工具的简单封装。它负责安装该工具，指导智能体编写 `Problem` 定义（包括实体、评估器与变异器），并通过上游 CLI 或自定义的 Python 驱动程序来控制进化循环的运行。

**许可证**：上游工具采用 **AGPL-3.0** 许可协议。该技能仅通过上游 CLI 或 `subprocess`/`uv run` 命令来调用它（属于单纯的内容整合），严禁将上游工具的类直接导入到 Hermes 中。

## 适用场景

- 用户提出“优化这个提示词”、“为 X 设计更优的正则表达式”、“自动改进这段代码/SQL 查询”或“寻找更好的指令”等需求。
- 您已拥有用于评估的指标（精确匹配度、正则匹配率、单元测试结果、大语言模型评分或运行时指标），同时也有初始候选方案。若没有评估指标，请先定义一个——这是最困难的部分。
- 成本可接受：一次典型运行需要 50–500 次大语言模型调用。在 gpt-4o-mini 上成本仅为几美分；而在 Claude Sonnet 上则可能需要几美元。

**不适用场景**：
- 优化目标具有可微性（此时应使用梯度下降法/DSPy）。
- 只需要尝试 2–3 种变体——可直接手动编写即可。
- 适应度信号完全依赖主观判断，且没有可量化的评估标准。

## 先决条件

- Python ≥3.11
- `git`、`uv`（或 `pip`）
- 下列任意一个 API 密钥：`OPENROUTER_API_KEY`、`ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`

该技能附带了一个名为 `parrot_openrouter.py` 的小型驱动程序，它通过 OpenAI SDK 使用 `OPENROUTER_API_KEY`，因此任何在 OpenRouter 上的模型均可使用。而上游 CLI 本身则固定支持 Anthropic，需要 `ANTHROPIC_API_KEY`。

## 安装（只需一次）

通过 `terminal` 工具运行即可：

```bash
mkdir -p ~/.hermes/cache/darwinian-evolver && cd ~/.hermes/cache/darwinian-evolver
[ -d darwinian_evolver ] || git clone --depth 1 https://github.com/imbue-ai/darwinian_evolver.git
cd darwinian_evolver && uv sync
```

验证：

```bash
cd ~/.hermes/cache/darwinian-evolver/darwinian_evolver \
  && uv run darwinian_evolver --help | head -5
```

## 快速入门——内置的 Parrot 示例

简易功能测试（需要 `ANTHROPIC_API_KEY`）：

```bash
cd ~/.hermes/cache/darwinian-evolver/darwinian_evolver
uv run darwinian_evolver parrot \
  --num_iterations 2 \
  --num_parents_per_iteration 2 \
  --mutator_concurrency 2 --evaluator_concurrency 2 \
  --output_dir /tmp/parrot_demo
```

输出结果：
- `/tmp/parrot_demo/snapshots/iteration_N.pkl` — 每次迭代后的种群数据（已序列化）
- `/tmp/parrot_demo/<jsonl>` — 每次迭代的 JSON 日志文件（路径会在运行时显示）

请在浏览器中打开 `~/.hermes/cache/darwinian-evolver/darwinian_evolver/darwinian_evolver/lineage_visualizer.html`，并加载该 JSON 日志以查看进化树。

## 快速入门 — OpenRouter 驱动（无需 Anthropic 密钥）

该技能附带了 `scripts/parrot_openrouter.py` 脚本——问题设定与普通 Parrot 问题相同，但 LLM 调用会通过 OpenRouter 进行，因此任何提供商均可使用。

```bash
# From wherever the skill is installed:
SKILL_DIR=~/.hermes/skills/research/darwinian-evolver
DE_DIR=~/.hermes/cache/darwinian-evolver/darwinian_evolver

cd "$DE_DIR" && \
  EVOLVER_MODEL='openai/gpt-4o-mini' \
  uv run --with openai python "$SKILL_DIR/scripts/parrot_openrouter.py" \
    --num_iterations 3 --num_parents_per_iteration 2 \
    --output_dir /tmp/parrot_or
```

使用 `scripts/show_snapshot.py` 查看结果：

```bash
uv run --with openai python "$SKILL_DIR/scripts/show_snapshot.py" \
  /tmp/parrot_or/snapshots/iteration_3.pkl
```

预期输出：按得分排序的7个优化后的提示模板，其中最优结果的得分应在0.6–0.8之间（初始种子`Say {{ phrase }}`的得分为0.000）。

## 定义自定义问题

该技能提供了`templates/custom_problem_template.py`文件——可直接复制、编辑并运行。需定义以下三个要素：

1. **`Organism`**——一个基于Pydantic的`BaseModel`子类，用于存储需要优化的内容（如`prompt_template: str`、`regex_pattern: str`、`sql_query: str`、`code_block: str`等）。需为其添加一个`run(*args)`方法以执行相关操作。

2. **`Evaluator`**——具备`.evaluate(organism) -> EvaluationResult(score=..., trainable_failure_cases=[...], holdout_failure_cases=[...], is_viable=True)`方法。
   - **`score`**的取值范围为[0, 1]，数值越高表示效果越好。
   - **`trainable_failure_cases`**——即变异器所接收的输入数据，需包含足够的上下文（输入内容、预期结果、实际输出），以便大语言模型进行诊断。
   - **`holdout_failure_cases`**——不会被变异器处理，可用于检测过拟合现象。
   - 除非该`Organism`完全无法使用（出现异常或返回None等），否则默认设置`is_viable=True`。得分为0但仍然可用的`Organism`也是允许的，只是会在父代选择过程中被降低权重。

3. **`Mutator`**——具备`.mutate(organism, failure_cases, learning_log_entries) -> list[Organism]`方法。其典型工作流程为：构建一个包含当前`Organism`、相关失败案例以及修复建议请求的大语言模型提示语；解析大语言模型的响应；并返回一个新的`Organism`对象。若解析失败，则返回`[]`，由循环机制处理该情况。

随后需编写一个驱动脚本，将`Problem(initial_organism, evaluator, [mutators])`与`EvolveProblemLoop`相连接，并通过`loop.run(num_iterations=N)`进行迭代——随附的`scripts/parrot_openrouter.py`文件可作为参考。

## 真正重要的超参数

| 参数 | 默认值 | 何时调整 |
|---|---|---|
| `--num_iterations` | 5 | 当对评估器有足够信心后，可提升至10–20次 |
| `--num_parents_per_iteration` | 4 | 若需低成本探索，可降至2个 |
| `--mutator_concurrency` | 10 | 为避免遇到速率限制，可降至2–4个 |
| `--evaluator_concurrency` | 10 | 与上述参数相同，因为评估器也会调用大语言模型 |
| `--batch_size` | 1 | 当变异器能够同时处理多个失败案例时，可提升至3–5 |
| `--verify_mutations` | 关闭 | 当变异器效率低下（根据Imbue指标，后续运行中的成本节省幅度未超过10倍）时，可开启该选项 |
| `--midpoint_score` | `p75` | 除非得分分布过于集中，否则无需调整 |
| `--sharpness` | 10 | 无需调整 |

## 常见问题与注意事项

1. **“初始`Organism`必须可用”**——即便初始种子的得分为0，也应在`EvaluationResult`中设置`is_viable=True`。因为若`Organism`不可用，意味着循环没有可优化的对象，因此会被直接排除。

2. **提供方的内容过滤机制会导致运行失败**。基于Azure的OpenRouter模型会对类似“忽略之前的指令”这样的短语返回HTTP 400错误。建议在调用大语言模型时使用`try/except`结构进行异常处理，并返回`f"<LLM_ERROR: {e}>"`，这样优化工具会将该`Organism`的得分设为0并继续下一轮优化。

3. **`loop.run()`是一个生成器函数**——仅在其被迭代调用时才会执行相应操作。应使用`for snap in loop.run(num_iterations=N):`的语法来遍历结果。

4. **快照为嵌套的pickle格式文件**。`iteration_N.pkl`文件中包含一个字典，该字典又包含`population_snapshot`字段（即更多经过序列化的字节数据）。若要反序列化这些数据，必须确保在相同的路径下可以导入`Organism`类。

5. **默认的并发设置过高**。10/10的并发级别在大多数提供方平台上都会触发速率限制。建议从2/2开始逐步调整。

6. **命令行工具默认绑定Anthropic平台**。执行`uv run darwinian_evolver <problem>`命令时会自动使用`ANTHROPIC_API_KEY`并调用Claude Sonnet模型。若要使用其他提供方，需编写类似`parrot_openrouter.py`的驱动脚本。

7. **受AGPL许可证约束**。严禁在Hermes核心代码中直接使用`from darwinian_evolver import ...`语句。不过，放在`~/.hermes/skills/...`目录下的自定义驱动脚本属于用户端代码，是允许使用的。

8. **没有PyPI安装包**。执行`pip install darwinian-evolver`命令会下载错误的版本。务必从GitHub仓库直接安装该工具。

## 验证方法

完成安装并运行相关脚本后，只要退出码为0即表示操作成功。

```bash
DE_DIR=~/.hermes/cache/darwinian-evolver/darwinian_evolver
ls "$DE_DIR/darwinian_evolver/lineage_visualizer.html" >/dev/null && \
cd "$DE_DIR" && uv run darwinian_evolver --help >/dev/null && \
echo "darwinian-evolver: OK"
```

## 参考资料

- [Imbue研究文章](https://imbue.com/research/2026-02-27-darwinian-evolver/)
- [ARC-AGI-2实验结果](https://imbue.com/research/2026-02-27-arc-agi-2-evolution/)
- [imbue-ai/darwinian_evolver项目](https://github.com/imbue-ai/darwinian_evolver)（AGPL-3.0许可证）
- [达尔文哥德尔机器](https://arxiv.org/abs/2505.22954)
- [PromptBreeder工具](https://arxiv.org/abs/2309.16797)
