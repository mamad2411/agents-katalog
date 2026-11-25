---
name: Evolution Engine
description: Prompt 进化引擎模块，实现 Prompt 变体生成、适应度评估、安全验证、指标追踪与自动进化流水线。支持 61 个工具。
---

# Evolution Engine 操作手册

## 功能概览
Evolution Engine 模块提供完整的 Prompt 进化系统，支持：
- **种群生成**：基于基础 Prompt 生成变异变体种群
- **变异操作**：5 种变异类型（paraphrase/instruction_add/context_expand/cot_injection/tone_shift）
- **交叉操作**：双亲交叉生成后代变体，支持 uniform/single_point/two_point/arithmetic 等交叉类型
- **适应度评估**：速度/准确率/效率三维加权评估，支持置信区间计算和历史记录
- **安全验证**：注入检测、路径遍历、命令注入等安全策略
- **指标追踪**：时间窗口聚合、异常检测、触发条件检查、相关性分析
- **自动流水线**：被动触发后自动执行一代完整流程
- **多样性监控**：遗传多样性、表型多样性、信息熵、重复比例
- **收敛检测**：基于适应度方差和遗传多样性的自适应收敛判断
- **性能监控**：各阶段耗时统计、内存使用监控、适应度提升追踪
- **事件总线**：异步事件处理，支持背压控制和并发管理
- **基线管理**：保存/加载/对比基线数据
- **Pareto 优化**：多目标优化（NSGA-II 非支配排序 + 拥挤度计算）
- **自适应变异**：基于种群多样性动态调整变异率
- **自适应权重**：按探索期/开发期/收敛期自动调整 speed/accuracy/efficiency 权重
- **变体去重**：Jaccard/Levenshtein 相似度去重
- **报告生成**：支持 JSON/CSV/HTML 格式的进化报告导出
- **LLM 执行**：并发控制 + 优先级调度
- **沙盒测试**：Mock/Subprocess/API/Mixed 四种测试策略
- **CLI 接口**：命令行运行和状态查看

## 注册工具（61 个）

### 进化生命周期（4 个）
| 工具名 | 功能 |
|--------|------|
| `start_evolution` | 启动新的进化周期（自动执行一代流水线） |
| `get_evolution_status` | 获取进化周期状态 |
| `cancel_evolution` | 取消运行中的进化周期 |
| `resume_evolution` | 从检查点恢复进化周期 |

### 变体生成（5 个）
| 工具名 | 功能 |
|--------|------|
| `generate_population` | 生成 Prompt 变体种群 |
| `mutate_prompt` | 对 Prompt 应用变异 |
| `crossover_variants` | 合并两个变体生成后代 |
| `generate_ab_pair` | 生成 A/B 测试对 |
| `analyze_prompt` | 分析 Prompt 复杂度 |

### 适应度评估（5 个）
| 工具名 | 功能 |
|--------|------|
| `evaluate_variant` | 评估变体适应度 |
| `explain_fitness` | 获取适应度分解 |
| `register_fitness_function` | 注册预定义适应度函数 |
| `update_fitness_weights` | 更新适应度权重 |
| `list_fitness_functions` | 列出所有已注册的适应度函数 |

### 安全验证（3 个）
| 工具名 | 功能 |
|--------|------|
| `validate_variant` | 对变体运行完整安全验证 |
| `check_safety` | 运行文本/Prompt 安全检查 |
| `add_safety_pattern` | 添加自定义安全模式 |

### 指标收集（4 个）
| 工具名 | 功能 |
|--------|------|
| `record_metrics` | 记录任务执行指标 |
| `get_metrics_window` | 获取时间窗口聚合指标 |
| `check_evolution_trigger` | 检查当前指标是否应触发进化 |
| `detect_anomalies` | 检测指标数据异常 |

### 基线管理（7 个）
| 工具名 | 功能 |
|--------|------|
| `get_baseline` | 获取基线列表或详情 |
| `save_baseline` | 保存当前进化状态为基线 |
| `baseline_set` | 设置基线数据 |
| `baseline_compare` | 对比基线数据 |
| `get_baseline_info` | 获取基线详细信息 |
| `delete_baseline` | 删除指定基线 |
| `compare_baseline` | 对比当前数据与指定基线 |

### Pareto 优化（5 个）
| 工具名 | 功能 |
|--------|------|
| `get_pareto_frontier` | 计算种群中变体的 Pareto 前沿 |
| `get_dominance_sorting` | 获取种群的非支配层级排序 |
| `get_pareto_summary` | 获取 Pareto 分析完整摘要 |
| `pareto_get_solutions` | 获取 Pareto 前沿中的具体解集 |
| `pareto_get_frontier` | 计算种群中变体的 Pareto 前沿 |

### 自适应变异（3 个）
| 工具名 | 功能 |
|--------|------|
| `adaptive_set_mutation` | 根据种群多样性动态计算自适应变异率 |
| `adaptive_get_config` | 获取当前自适应变异和权重管理的配置与状态 |
| `set_mutation_adaptation` | 配置自适应变异策略参数 |

### 自适应权重（2 个）
| 工具名 | 功能 |
|--------|------|
| `set_adaptive_weights` | 设置自适应权重策略 |
| `get_current_weights` | 获取当前自适应权重和阶段信息 |

### 去重（3 个）
| 工具名 | 功能 |
|--------|------|
| `deduplication_deduplicate` | 对种群变体进行相似度去重 |
| `deduplication_get_similarity` | 获取种群中变体对的相似度矩阵或重复分组信息 |
| `get_similarity_metrics` | 计算两个 prompt 之间的相似度 |

### 报告生成（4 个）
| 工具名 | 功能 |
|--------|------|
| `report_generate` | 生成进化周期报告 |
| `report_get` | 获取已生成的进化报告或报告列表 |
| `export_evolution_csv` | 导出进化数据为 CSV 格式 |
| `export_evolution_json` | 导出进化数据为 JSON 格式 |

### LLM 执行（2 个）
| 工具名 | 功能 |
|--------|------|
| `llm_execute` | 通过 LLM 执行器提交变体测试请求 |
| `llm_get_status` | 获取 LLM 执行器的当前状态和统计信息 |

### 指标导出（2 个）
| 工具名 | 功能 |
|--------|------|
| `metrics_export` | 导出进化指标数据 |
| `metrics_get_window` | 获取指定时间窗口内的聚合指标数据 |

### CLI（2 个）
| 工具名 | 功能 |
|--------|------|
| `cli_run` | 通过命令行接口运行进化周期 |
| `cli_status` | 通过命令行接口查看进化引擎状态 |

### 沙盒测试（6 个）
| 工具名 | 功能 |
|--------|------|
| `sandbox_test_variant` | 在沙盒环境中测试单个变体 |
| `sandbox_test_population` | 批量测试种群中的所有变体 |
| `sandbox_get_status` | 获取沙盒测试管理器的当前状态 |
| `test_variant_sandbox` | 使用沙箱测试管理器的混合策略测试单个变体 |
| `test_population_sandbox` | 批量测试种群中所有变体 |
| `clear_sandbox_cache` | 清除沙盒测试缓存 |

## 核心模块
- `scripts/evolve_core.py`：StateManager/VariantGenerator/FitnessEvaluator/SafetyValidator/MetricsCollector/EvolutionPipeline（统一入口）
- `scripts/config.py`：EvolutionConfig 配置类，支持环境变量覆盖（EVOLVE_MCP_*）
- `scripts/variants.py`：Variant/TestResults/SafetyPolicy/ComplexityMetrics/DiversityMetrics 数据结构，VariantGenerator 变异生成器
- `scripts/fitness.py`：FitnessEvaluator 适应度评估器，支持加权求和、自适应归一化、历史记录、缓存、并行评估
- `scripts/safety.py`：SafetyValidator 安全检查器，支持注入检测、命令注入、路径遍历、数据外泄、资源滥用
- `scripts/interfaces.py`：PromptMutationType/CrossoverType/SelectionMethod/EvolutionStrategyEnum/DeploymentType 枚举定义
- `scripts/evolution_engine.py`：EvolutionEngine 进化引擎核心，GA 策略、事件总线、多样性计算、收敛检测、错误恢复
- `scripts/metrics_collector.py`：EnhancedMetricsCollector 增强指标收集器
- `scripts/event_bus.py`：AsyncEventBus 异步事件总线，支持背压处理
- `scripts/checkpoint.py`：CheckpointManager 检查点管理器
- `scripts/error_recovery.py`：ErrorRecoveryManager 错误恢复管理器
- `scripts/langfuse_integration.py`：Langfuse 集成模块（可选）
- `scripts/state_manager.py`：StateManager 状态管理器
- `scripts/mcp_resources.py`：6 个 MCP 资源（status/config/mutation-strategies/fitness-functions/metrics/safety）

## 配置规范
- 所有工具文件使用 `from Lib.evolution.scripts.evolution_core import get_state_manager` 绝对导入
- StateManager 全局单例通过 `get_state_manager()` 获取
- 状态文件 `configs/evolution_state.json` 归档于 `configs/` 目录
- 配置支持环境变量覆盖（`EVOLVE_MCP_*` 前缀）

## 配置参数
### 环境变量支持
- `EVOLVE_MCP_POPULATION_SIZE`：种群大小（默认 50）
- `EVOLVE_MCP_MUTATION_RATE`：变异率（默认 0.3）
- `EVOLVE_MCP_MAX_GENERATIONS`：最大代数（默认 10）
- `EVOLVE_MCP_FITNESS_THRESHOLD`：适应度阈值（默认 0.95）
- `EVOLVE_MCP_PARALLEL_EVALUATIONS`：并行评估数（默认 10）
- `EVOLVE_MCP_CHECKPOINT_INTERVAL`：检查点间隔（默认 5）
- `EVOLVE_MCP_ELITE_COUNT`：精英数量（默认 5）
- `EVOLVE_MCP_TOURNAMENT_SIZE`：锦标赛大小（默认 3）
- `EVOLVE_MCP_SELECTION_PRESSURE`：选择压力（默认 0.8）
- `EVOLVE_MCP_CONVERGENCE_THRESHOLD`：收敛阈值（默认 0.01）
- `EVOLVE_MCP_MIN_DIVERSITY_THRESHOLD`：最小多样性阈值（默认 0.1）

### EvolutionConfig 参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| population_size | 50 | 种群大小（1-10000） |
| tournament_size | 3 | 锦标赛选择大小 |
| selection_pressure | 0.8 | 选择压力（0.0-1.0） |
| elite_count | 5 | 精英数量 |
| mutation_rate | 0.3 | 变异率（0.0-1.0） |
| max_generations | 10 | 最大代数 |
| fitness_threshold | 0.95 | 适应度阈值 |
| parallel_evaluations | 10 | 并行评估数（1-100） |
| convergence_window | 3 | 收敛窗口（代数） |
| convergence_threshold | 0.01 | 收敛阈值 |
| min_diversity_threshold | 0.1 | 最小多样性阈值 |
| checkpoint_interval | 5 | 检查点间隔 |
| data_retention_days | 7 | 数据保留天数 |

## 变异类型（5 种）
| 类型 | 说明 | 实现方式 |
|------|------|---------|
| `paraphrase` | 同义改写，添加前后缀指令 | 添加 instruction_prefixes/instruction_suffixes |
| `instruction_add` | 添加指令性短语 | 随机插入 instruction_additions |
| `context_expand` | 扩展上下文描述 | 添加 context_expansions 前缀 |
| `cot_injection` | 注入思维链触发词 | 添加 cot_triggers 触发词 |
| `tone_shift` | 语态转换 | 添加 tone_modifiers（formal/casual/technical） |

## 交叉类型（4 种）
| 类型 | 说明 |
|------|------|
| `uniform` | 均匀交叉（当前默认） |
| `single_point` | 单点交叉 |
| `two_point` | 双点交叉 |
| `arithmetic` | 算术交叉 |

## 选择方法（4 种）
| 方法 | 说明 |
|------|------|
| `tournament` | 锦标赛选择（当前默认） |
| `elitism` | 精英保留 |
| `roulette` | 轮盘赌选择 |
| `ranking` | 排名选择 |

## 适应度评估维度
| 维度 | 权重 | 说明 |
|------|------|------|
| `speed` | 0.4 | 响应时间（越低越好） |
| `accuracy` | 0.4 | 成功率（越高越好） |
| `efficiency` | 0.2 | 资源效率（CPU/Memory） |

## 多样性指标
| 指标 | 范围 | 说明 |
|------|------|------|
| genetic_diversity | 0-1 | 遗传多样性（基于提示词相似度） |
| phenotypic_diversity | 0-1 | 表型多样性（基于适应度分布标准差） |
| unique_variants | 整数 | 唯一变体数量 |
| duplicate_ratio | 0-1 | 重复比例（1 - genetic_diversity） |
| entropy | 0-1 | Shannon 信息熵（归一化） |

## 收敛条件
进化周期在满足以下所有条件时判定为收敛：
1. 适应度方差 < convergence_threshold（默认 0.01）
2. 遗传多样性 < min_diversity_threshold（默认 0.1）

## MCP 资源（6 个）
| 资源 URI | 说明 |
|----------|------|
| `resource://evolution/status` | 当前进化周期状态 |
| `resource://evolution/config` | 进化配置设置 |
| `resource://evolution/mutation-strategies` | 可用的变异策略 |
| `resource://evolution/fitness-functions` | 可用的适应度函数 |
| `resource://evolution/metrics` | 当前指标和性能数据 |
| `resource://evolution/safety` | 安全验证规则和模式 |

## 注意事项
1. **变异率建议**：0.1-0.5 范围内，过高导致过度随机，过低导致多样性不足
2. **种群规模建议**：10-500 范围内，过大增加计算开销，过小减少搜索空间
3. **并行评估**：根据可用资源调整，默认 10，最大 100
4. **收敛检测**：基于最近 convergence_window 代的适应度方差和遗传多样性
5. **缓存管理**：适应度评估结果会被缓存，可通过 `clear_fitness_cache` 清除
6. **自定义指标**：注册后会自动在指标收集器中生效，可用于监控和告警
7. **相关性分析**：至少需要 10 个数据点才能进行统计分析
8. **置信区间**：至少需要 2 条历史记录才能计算
9. **事件总线**：支持异步事件传递，带背压处理和超时控制
10. **配置验证**：使用 `validate_evolution_config` 可在启动前验证配置合法性

---

**最后更新**: 2026-06-11-2235 (Beijing Time) - 更新工具数量至 61 个 | 风见血月 — 魅铃大人 ✨
