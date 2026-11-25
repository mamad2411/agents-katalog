---
name: cuda-kernel-optimizer
description: "Use when optimizing or diagnosing GPU workload performance with CUDA, CUTLASS, Triton, PyTorch, vLLM or TensorRT-LLM; interpreting NCU, Nsys or PyTorch Profiler evidence; or preparing the workload and correctness checks for such optimization. General coding, skill maintenance and conceptual GPU questions do not require the optimization workflow."
---

# CUDA Kernel and Workload Optimizer

ChatGPT 负责优化判断：识别瓶颈、提出候选、评估投入产出并决定下一步。工具执行明确请求，完成检查、测量、解析和事实记录；工具不选择方向，不判断 ROI，也不生成下一步计划。

围绕用户指定的目标优化。kernel 测量支持 kernel 层结论；workload 或服务层收益必须由用户的真实测试集、精度校验和成对测量支持。不得擅自编造、下载或替换测试 workload。

## 工作与沟通

以一个能改变判断的工作步骤组织执行。同一已说明步骤中的编辑、构建和必要检查可以连续完成；在开始昂贵实验、改变方向或预计投入明显增加时，简要说明证据缺口、预期收益、成本和继续条件。已有授权内的常规操作直接推进，长任务及时报告实质进展。

根据问题选择所需操作。已有报告可以直接分析，简单工具错误可以直接定位修复；完整性能优化才需要建立 Target 和测量链路。验证做到足以支持当前结论，检查通过且没有新疑点时继续交付。

## 按需读取

只加载当前问题需要的资料。第一次使用或接口不明确时查看脚本 `--help` 和 `references/request_protocol.md`；已经确认的接口可直接复用。

| 任务 | 脚本或资料 |
|---|---|
| 检查测试集、精度校验、driver、环境并冻结 Target | `scripts/readiness.py`；`references/environment_readiness.md` |
| baseline、Experiment、screen、target 和 final audit | `scripts/workload_evaluate.py`；`references/performance_iteration.md` |
| Nsight Compute | `scripts/profile_ncu.py`；`references/ncu_metrics_guide.md` |
| Nsight Systems | `scripts/profile_nsys.py` |
| PyTorch Profiler | `scripts/profile_pytorch.py` |
| 编译产物和 SASS | `scripts/compiler_evidence.py`；`scripts/sass_check.py` |
| 离线知识 | `scripts/knowledge_query.py` |
| 选择或恢复最佳版本 | `scripts/champion.py` |
| 服务采样和环境干扰 | `references/serving_evidence_protocol.md`；`references/nonstationary_serving_evidence.md` |
| 上游复用、一手资料与外部 AI | `references/research_augmentation.md` |

## 优化判断

### 建立可比较的起点

明确 primary、minimum effect、不可退化的约束、允许的修改范围和投入上限。先前声明的重要 secondary 可以支持局部结果，但不替换 primary 或决定主目标完成。

通过 readiness 冻结 original、真实测试集、精度规则、driver 和实际环境。修改性能代码前先测原始业务基线，核对决策指标的分子、分母、单位和来源，用 original 重复样本估计测量分辨率。精度未通过时，不解释性能样本。环境缺项时明确结论能支持的范围。多进程启动、依赖和资源可用性按环境参考处理，复用已经验证的配置。

### 从生产路径选择方向

结合已有 profile、源码和运行证据比较系统方向。提出 Candidate 时，说明具体改动省去什么成本、原操作还承担什么作用，以及替换后如何满足目标要求。只追踪会影响下一步判断的依赖；已有可靠依据处即可停止，不要求理解整个系统。

ROI 是派生证据主张。定义 Candidate 真正替换的 production replacement boundary，核对 shape、phase、lowering、graph、dispatch、fallback 和 overlap。只使用同一边界的观测或有依据的保守上界；源码和数学语义一致不能代替执行形态一致。沿依赖判断对关键路径的影响，计入实际 occurrence 和新增成本，不按函数边界截断影响，也不把周围空隙全部算成收益。p95/p99 要按受影响请求和关键路径判断，不能直接套用均值的时间占比。

按对 primary 的预期收益、证据可信度、可行性、风险和验证成本排序。关键前提未知时，选择能最快区分解释的观测或范围受限的生产等价原型。完整生产接入或正式测试前，收益空间与测量分辨率必须足以支持投入；结构化 `opportunity_claim` 保存这些前提，工具只检查显式矛盾和算术。

新增非平凡 kernel、通信 primitive 或通用接入前，按外部研究参考核验社区等价能力。优先复用、最小 backport 或窄适配；缺少当前 workload 的 E2E 证据意味着需要测量，不能据此重写已有能力。复用仍适用的研究结果，只核验变化的版本、边界或未解决事实。

### 用最便宜的有效实验取得结论

用能直接回答关键疑点的最低成本证据决定下一步，而不是逐项跑完检查。静态分析、精度测试、计时和 profiler 各回答不同问题；若干输出相等不能解除未解决的并发顺序或存储生命周期疑点。未知部分可用有界诊断澄清，不据此扩大正确性或收益结论。创建 Experiment 时冻结双方版本、比较关系和证据计划，说明失败能否定实现、集成还是机制。已有证据足够推进或拒绝时就行动，不重复验证未变化的前提。

可能支撑正式性能结论的比较由 `workload_evaluate.py` 保存。同一次 driver 调用保存正确性和性能证据，避免重复启动完整 workload；同进程比较必须实际保持声明的共享条件。正式 target 前确认前提仍适用，只有新事实影响判断时才重新分析。

预测与实测实质冲突时先完成 prediction-error reconciliation：检查边界、执行形态、候选范围、coverage、exposure 和成本，修正系统模型后再选择候选。一次实现失败或局部代理测试不能自动关闭整个机制；重试应有能够改变结论的新证据或不同判别方法。

### 保留结果并决定是否继续

只有正式比较通过当前 Target 的 primary verdict，ChatGPT 才能显式选择 Champion。预先声明的 secondary 稳定改善且约束满足时，可以保留为局部结果并说明场景；它不能替代 primary 达成。测试后才发现的收益先作假设，要据此选择 Champion，需冻结新的目标并验证。组合已测机制仍是新 Candidate，需要验证组合结果。

需要 workload 或服务层最终结论时，对 Champion 和 original 执行 final audit。命令超时防止卡死；继续投入由预期收益、剩余不确定性、成本和授权决定。结束前确认最高价值的剩余系统方向没有被一次失败实现误杀。已有系统分析仍适用时直接引用，只有新证据改变排序才重新比较；不为消耗剩余预算重复研究或实验。

暂停或结束时留下简短 Handoff：primary 是否达成、Champion 或 Original、关键证据与收益、局部结果、被拒方向及拒绝范围、未解决问题、停止原因和恢复所需的 workspace 信息。发生预测错误时保留修正后的前提。环境或 runner 修复单独说明成本，不计作性能收益。

## 证据与执行边界

- 结果引用冻结的 Candidate/reference、测试集和实际环境；精度失败使相应性能结果无效。身份不完整只收窄可支持的结论，保留独立有效证据。
- profiler 返回观测事实，知识查询返回材料及适用条件；都不决定下一步。知识无匹配不妨碍源码分析或提出假设。未知 profiler 版本、关键字段或单位不能猜测解析；已知格式的非关键扩展保留为 `unmodeled`。
- 字符串存在不能证明编译器融合、消除或调度；这类结论需要对应版本的 lowered/generated code、编译器记录或运行证据。
- 共享宿主机按环境和性能参考进行有界空闲检查，并保存与正式样本对齐的 CPU/GPU 观测。未解释的重叠干扰影响性能归因，不能据此否定独立的正确性结果。
- GPU 实验、远端代码和 artifact root 由主智能体统一写入；正式共享 GPU 实验串行。独立只读工作可按复杂度并行，周期采样交给确定性命令。
- 外部资料用于核实事实和挑战判断。高影响决策仍有关键不确定性时，按研究参考尝试异构 AI；外部不可用不阻塞本地工作，也不授权扩大结论。保留关键不同意见，最终由当前目标的本地证据决定。
- 驱动、计数器权限、频率、功耗、服务和容器运行时等宿主机变更，默认只给建议，除非用户明确授权。`ERR_NVGPUCTRPERM` 时可改用其他有效证据。

## 使用后反馈

Handoff 中的 `skill friction/feedback` 只记录可行动的问题或值得保留的机制：观察、实际影响、期望改动和最小证据；没有则写 `none`。反馈默认留在用户环境，向外部提交须有明确授权并去除私有材料。普通正确行为和优化结果本身不等于 skill 改进。
