---
name: ict-engine-runtime
description: |
  ICT-Engine 运行时流水线操作。因子迭代 → 滤波 → BBN 证据 → CatBoost 路径排名 → 执行树。
  触发方式：ict-engine runtime、path ranking trainer、BBN prior init、auto-quant results import
---

# ict-engine-runtime：运行时流水线

ICT-Engine 运行时流水线操作员。负责将因子研究产物转化为执行树决策。

Dense reclaim branch notes: `references/low-hazard-reclaim-branch-pattern.md`.
Real-trade replay guardrails: `references/real-trade-feedback-replay.md`.
Diagnostic/sample-trade replay pattern: `references/diagnostic-feedback-replay-sample-logging.md`.
CRWD 5m PDA/MTF exact downstream repair: `references/crwd-pda-mtf-exact-downstream-repair.md`.

TradingView public strategy absorption: `references/tradingview-public-strategy-absorption.md`.
Board A/B completion audit readback: `references/board-ab-completion-audit-readback.md`.
Provider runtime repair: `references/provider-runtime-repair.md`.

**核心流水线：**
```
因子迭代 → 滤波 → BBN 证据 → CatBoost → 执行树
```

---

## 核心原则

1. **零配置**：默认行为可直接运行，无需用户手动配置复杂参数
2. **Token 友好**：输出简洁，不输出冗余解释
3. **无污染**：不修改仓库代码，通过外部脚本和状态目录隔离操作
4. **热插拔**：用户可通过配置文件自定义权重和特征

---

## 流水线阶段

### Stage 1：因子迭代产物导入

```bash
# 导入 Auto-Quant 策略库
./target/debug/ict-engine auto-quant-results-import \
  --symbol <SYM> --state-dir /tmp/<state> \
  --library strategy_library.json

# 应用 BBN prior
./target/debug/ict-engine auto-quant-prior-init \
  --symbol <SYM> --state-dir /tmp/<state>
```

### Stage 2：滤波层（regime_filter.rs + market_state/）

当前仓库支持的滤波：
- HMM/波动率状态过滤
- 多周期共振过滤
- **市场状态分类**（新增）

**市场状态分类器** (`src/market_state/`)：

```rust
use ict_engine::market_state::{MarketStateClassifier, MarketStateConfig};

// 零配置
let classifier = MarketStateClassifier::new();
let snapshot = classifier.classify(&candles);

// 热插拔配置
let config = MarketStateConfig::load(Path::new("market_state_config.json"))?;
let classifier = MarketStateClassifier::with_config(config);
```

**主大类（PrimaryMarketRegime）**：
- `TrendExpansion` — 趋势扩展（高波动+高流动性+强结构）
- `RangeConsolidation` — 震荡整理（低波动+正常流动性+弱结构）
- `ExtremeStress` — 极端状态（危机波动 或 流动性枯竭）
- `ReversalBrewing` — 反转酝酿（行为极端+结构弱化）

**维度分类器**：
| 维度 | 状态 | 触发条件 |
|------|------|----------|
| 波动率 | LowVol/NormalVol/ElevatedVol/CrisisVol | ATR 百分位阈值 |
| 流动性 | HighLiquidity/NormalLiquidity/ThinLiquidity | 成交量+价格范围 |
| 结构 | Trending/MeanReverting/Ranging/Accumulation/Distribution | ADX+均值偏离+Wyckoff |
| 行为 | Crowding/Exhaustion/FOMO/Capitulation/RiskOn/RiskOff | RSI+成交量异动 |

**热插拔配置模板**：`config/market_state_user_weights_template.json`

**置信度调优参数（v6）**：
- 基础置信度：0.20（避免过低综合置信度）
- 结构权重：50%（趋势识别核心）
- 一致性权重：30%（部分匹配得分）
- 趋势阈值：0.50 / 极端阈值：0.75-0.80 / 反转阈值：0.50

**验证结果**：
- 平均置信度：61%（目标 >50%）
- 高置信比例：4.17%（目标 >30%）
- 可交易比例：79%（目标 >60%）
- VeryLow 比例：0%

**主大类分布**：
- TrendExpansion: 41.7% / RangeConsolidation: 41.7% / ExtremeStress: 16.7%

**验收标准**：每个因子必须声明"允许进入的滤波状态"。

**参考文档**：`references/market-state-confidence-tuning.md` — 置信度调优迭代历史与参数

**高置信 regime 跑法**：`references/regime-confidence-factor-runs.md` — 95% 置信诉求下的运行命令、覆盖口径、OOS sanity check、已知坑

**完整闭环跑法**：`references/auto-quant-bbn-catboost-execution-tree-closure.md` — Auto-Quant → BBN prior → path ranker/CatBoost fallback → execution tree 的实跑顺序、验证口径、已知坑

**Regime-rooted provider Auto-Quant chain**：`references/regime-branch-provider-autoquant-chain.md` — 当盈利因子必须按 `主regime -> 子regime -> 子子regime/盈利因子 -> 盈利因子` 分支，并且要亲跑 provider/Auto-Quant/BBN/CatBoost/execution-tree 时使用；含字段、命令、验收与 repo hygiene。

**真实 Auto-Quant 闭环样例**：`references/auto-quant-runtime-closure-real-run-20260509.md` — 记录一次完整实跑：bootstrap/prepare、seed archived strategies、`uv run --with ta-lib run.py`、手工 v3 manifest、`n_ok=2`、BBN `strategies_applied`、ranker fallback 注册、workflow-status 显示执行树结果。

**v0.4.1 阻塞修复**：`references/auto-quant-v041-exporter-catboost-blockers.md` — 修 Auto-Quant 多 timerange exporter 导致 BBN `trade_count=0`、CatBoost 安装/NaN label/真实模型优先注册问题

**全仓审计跑法**：`references/repo-audit-and-consumer-review.md` — 架构、功能、闭环、测试、实际体验、消费者视角、开源贡献者视角的只读审计流程与已知坑。

**因子到实战建议闭环审计**：`references/repo-audit-factor-to-execution-closure.md` — 审计因子迭代、滤波/regime、BBN 证据、CatBoost/path ranker、执行树、recommended_command 是否真实贯通；含本次发现的常见断链清单。

**运行时闭环实现笔记**：`references/runtime-closure-implementation-notes.md` — 将审计缺口落成代码时使用；覆盖 market_state 接入 analyze/BBN/trace、`pass_to_bbn=false` neutral soft evidence、path-ranker lineage、schema 扩字段编译坑、验证命令。

**Heuristic Learning 模块收割**：`references/heuristic-learning-module-harvest.md` — 当用户要求把论文/GitHub 公式、算法、模块拆下来拼进 ict-engine 自迭代链路时使用；含 Triple Barrier、DSR/PBO、Qlib/Alpha101、regime calibration、BBN evidence valuation、path ranking、payoff-shape 的优先接入顺序。

**高夏普因子收割 + seed library**：`references/high-sharpe-factor-harvest-seed-library.md` — 当继续从论文/开源仓库收割跨市场/期权高夏普候选，并生成零配置 hot-plug factor seed candidate JSON 时使用；含 16 个首批候选、用户 VRP/NQ 可选字段、验证命令和坑。

**Heuristic Learning 第一刀**：`references/heuristic-learning-first-slice.md` — 当用户要求先实现 `labeling_triple_barrier.py + factor_payoff_shape_report.py`，或继续做到零配置 payoff pipeline / DSR guard / payoff-gated path-ranker target export 时使用；含 TDD 路径、CLI、字段、短空 stop 符号坑、`thin_density` 非硬拒绝规则、热插拔 profile、PSR/DSR 字段、`probe/promote` 进 path-ranker+BBN、`reject` 仅进 failure memory。

**Heuristic Learning Payoff + Regime Chain**：`references/heuristic-learning-payoff-chain.md` — 当继续 ICT Engine 自迭代/高夏普防幻觉/95% regime confidence 链路时使用；记录已完成的 sidecar 链：Triple Barrier → payoff report → PSR/DSR → Purged CV/PBO → path-ranker target → BBN gate/failure memory → regime confidence report；含用户 VRP/NQ 辅助字段、验证命令、多 agent dirty worktree 处理规则、下一刀 transition evidence aggregator。

**Backtest hotplug + auxiliary / Analyze PDA events**：`references/backtest-hotplug-auxiliary-and-analyze-pda-events.md` — 当补齐 `factor-backtest` 与 `analyze` 的行为级闭环时使用；覆盖 `--auxiliary-evidence`、MTF path 透传、`FactorHotplugConfig` 注册、H4/D1/W1 PDA events 注入 `FactorContext`、定向测试与实跑验证坑。

**Heuristic Learning sidecar slices**：`references/heuristic-learning-sidecar-slices.md` — 当继续 `docs/plans/2026-05-09-heuristic-learning-execution-todo.md` 或类似自迭代链路时使用；覆盖 BBN evidence value、risk-adjusted utility、formula seed library、paper2code adapters、payoff pipeline sidecar closure 的 TDD/验证/提交/闭环审计模式。

**High-Sharpe factor harvest + payoff gates**：`references/high-sharpe-factor-harvest-and-payoff-gates.md` — 当继续 `docs/plans/2026-05-09-high-sharpe-factor-harvest-handoff-todo.md` 或从论文/开源仓库收割高夏普因子时使用；覆盖 16 个 seed candidate、用户可选字段、R22 seed library、R23 payoff gate、DSR/PBO/CVaR/tail-risk failure tags、license posture。

**MTF / FactorContext 小周期 PDA events**：`references/mtf-factorcontext-small-timeframe-pda-events.md` — 当补齐 `30m` 与 `m1/m5/m15/m30/h1` PDA event 透传时使用；覆盖 `FactorContext`、`AnalyzeNativeFrames`、research/backtest/debug/lifecycle 调用点、测试签名与 `cargo test --bin ict-engine multi_timeframe` 验证坑。

**Regime ontology manifest slice**：`references/regime-ontology-manifest-slice.md` — 当做高置信 regime classifier 的 R2 / expert-bank ontology manifest 时使用；记录 53 experts 目标形状、Unknown/Neutral abstain 规则、TDD 与验证命令。

**Regime feature builder slice**：`references/regime-feature-builder-slice.md` — 当继续高置信 regime classifier 的 R3 / feature-builder sidecar 时使用；记录 OHLCV/aux/MTF 输入、VRP/NQ 字段透传、特征输出、TDD 与汇报坑。

**Regime classifier sidecar chain**：`references/regime-classifier-sidecar-chain.md` — 当继续高置信 regime classifier 的 R2-R17 ontology/feature/discovery/expert-trainer/calibration/transition/consumer-bundle/mainline-adapter/read-only BBN evidence sidecar，或要写 handoff TODO 时使用；含文件清单、验证命令、CLI smoke、下一步和提交避污坑。

**主线 regime/CatBoost/execution 审计**：`references/mainline-regime-catboost-execution-audit.md` — 当审计 `regime -> factor-research -> factor-backtest -> analyze/live -> recommendation` 是否真实贯通时使用；含隔离实跑命令、字段覆盖表、已知弱链。

**Market-state threading into factor reports**：`references/market-state-threading-factor-reports.md` — 当 P1 缺口是 `factor-research` / `factor-backtest` 未报告 primary/secondary market_state 时使用；含 TDD、实现形状、CLI runtime smoke 和 `passthrough` 坑。

**Execution trace consumer fields**：`references/mainline-execution-trace-consumer-fields.md` — 当 P2/P3 缺口是 path-ranker/CatBoost 只存在文本 lineage、execution_tree_trace 缺稳定机器字段、triage 缺短理由摘要时使用；含字段形状、TDD 锚点、commit 避污恢复。

**Mainline consumer reason field**：`references/mainline-consumer-reason-field.md` — 当最终消费者需要一个干净短字段合并 `market_state + execution branch/gate/bias + ranker source/model/ready` 时使用；含 `ExecutionTriage.consumer_reason`、`ExecutionTreeOutput.consumer_reason` trace 下沉、normal analyze/analyze-live 报告透传、human 首行和真实 CLI 验证清单。

**Regime consumer bundle + mature ranker validation**：`references/regime-consumer-bundle-and-mature-ranker-validation.md` — 当收束 regime consumer bundle 接入、read-only BBN soft evidence 映射、或复验 mature registered-model path-ranker runtime 时使用；含 trace 字段、bundle fixture、`python3` smoke、mature state 结论。

**Regime bundle BBN soft evidence opt-in**：`references/regime-bundle-bbn-soft-evidence-opt-in.md` — 当继续 regime consumer bundle -> BBN 主线接入时使用；记录默认 read-only、`--apply-regime-bundle-bbn-soft-evidence` 显式生效、analyze/analyze-live adapter 去重、isolated smoke、只提交本轮文件。

**Regime paper-backed feature wiring audit**：`references/regime-paper-backed-feature-wiring-audit.md` — 当用户问论文能给什么 regime 证据、是否还要跑 regime、或要审计 HV/IV/VIX/VVIX/change-point/directional-change/correlation-dispersion 是否进入 sidecar/BBN/CatBoost/execution trace 时使用；核心结论是少加标签，多查证据接线。

**Regime consumer auxiliary evidence wiring**：`references/regime-consumer-aux-wiring.md` — 当 Board A 需要把 `consumer_hints.user_vrp_nq_context` 的 HV/IV/VIX/VVIX/VRP-NQ 辅助字段稳定下沉到 BBN/pre-Bayes、structural path-ranking/CatBoost target、execution tree trace 时使用；含字段名、验证断言和多 agent 边界。

**IBKR intraday/options regime + AQ closure**：`references/ibkr-intraday-options-regime-aq.md` — 当 Board A 需要 1m/5m/15m/30m K线、IBKR 期权/HV/IV、或用户追问是否真的用了 Auto-Quant 时使用；含 `ib_async` runner、`ts -> timestamp` AQ 归一化、validator/CatBoost/AQ 判读坑。

**IBKR options regime-rooted AQ chain**：`references/ibkr-options-regime-rooted-aq-chain.md` — 当盈利因子必须由真实 IBKR option premium/HV/IV 锚定，并带 `主regime -> 子regime -> 子子regime/盈利因子 -> 盈利因子` 通过 provider portability、AQ、BBN、真实 CatBoost、execution-tree 时使用；含 `uv run --with catboost` 重试、成熟度 fail-closed 判读。

**IBKR options overlap / HTF neutralization**：`references/ibkr-options-overlap-neutralization.md` — 当小周期 IBKR 期权因子都赚钱但可能是同一信号时使用；含 entry overlap、Jaccard/one-way overlap、HTF hard-gate 真实回测判读。

**IBKR cross-asset vol/gamma proxy AQ**：`references/ibkr-crossasset-vol-gamma-proxy-aq.md` — 当用户要求用 IBKR 在股指期货、黄金期货、美股上跑波动率/gamma-wall/IV/OI/Greeks 类盈利因子时使用；含真实数据边界、multi-asset Tomac、basket analyze、CatBoost 注册坑与 fail-closed 判读。

**IBKR cross-asset offline parity refinement**：`references/ibkr-crossasset-offline-parity-refine.md` — 当本地 IBKR/Freqtrade feather 可用但 Freqtrade 被 CCXT markets reload/联网元数据阻断时使用；用离线 parity evaluator 区分策略质量与 market metadata 故障，并把候选以 provenance + fail-closed flags 写回 strategy_library。
**IBKR max-window expansion / opportunity density**：`references/max-window-expansion-and-opportunity-density.md` — 当用户要求“10Y if possible”或想判断样本少是时间窗还是机会稀少时使用；记录 asset/bar-size ceilings、contract quirks、和严格信号密度判读。

**IBKR dense K-line practical gates**：`references/ibkr-dense-kline-practical-gates.md` — 当用户要求 IBKR 优先、尽量一个月/一季度上限窗口、从 1min 出发并覆盖 5min/15min/30min/1h，且最终以实战盈利 gate 为准时使用；含 5min 主信号、1min 入场时机、HTF gate 的 fail-closed 判读。

**Provider runtime repair**：`references/provider-runtime-repair.md` — 当 `provider-status` 报 IBKR 依赖缺失、TradingViewRemix/TVR connectivity failed/429，但本机有可用 Python/本地 MCP stdio 时使用；含 zsh login PATH、`~/.zprofile`、`ICT_ENGINE_TRADINGVIEW_MCP_*`、provider-status 与实抓验证。

**Board A provider matrix fail-closed**：`references/board-a-provider-matrix-fail-closed.md` — 当 Board A 要求跨 yfinance/TVR/IBKR/Kraken 验证 95% regime confidence 时使用；记录 provider-ready 不等于 fetch-success、混合 harness 失败后需单 provider 复测、AQ `seed_required` 是 Board B 边界。

**Dense K-line regime branch chain**：`references/dense-kline-regime-branch-chain.md` — 当用户要求多跑 `1m/5m/15m/30m` 增样本，并且仍要保留 `主regime -> 子regime -> 子子regime/盈利因子 -> 盈利因子` 过 Auto-Quant/BBN/CatBoost/执行树时使用；含 timerange、local Auto-Quant checkout、CatBoost train/apply、trace.output 验收坑。

Dense K-line real trade feedback replay: `references/dense-kline-real-trade-feedback-replay.md` — when dense branch要从 Auto-Quant/Freqtrade 聚合结果进入 structural feedback 时使用；必须先导出真实 `trades` 行并校验 `sum(profit_abs) == profit_total_abs`，再回灌 BBN/CatBoost/执行树，禁止用 aggregate summary 合成反馈.

Provider-quartet regime-rooted AQ chain: `references/provider-quartet-regime-rooted-aq-chain.md` — when a Board B profitability factor must survive yfinance/TradingViewRemix/IBKR/Kraken through AQ, BBN, CatBoost, and execution tree with branch fields intact.

Provider-quartet retry + fail-closed CatBoost handoff: `references/provider-quartet-provider-retry-and-failclosed-catboost.md` — when provider-status is green but first fetches fail, or CatBoost setup is flaky; retry provider axes with operator-like zsh/env, preserve branch fields, and do not claim CatBoost/promotion when fallback ranker or observe/transition_guardrail remains.

Regime-rooted live-ready factor gate: `references/regime-rooted-live-ready-factor-gate.md` — when continuing profitability-factor training under the user's strict rooted-branch and live-ready requirements; covers full branch-path shape, 1m/full-ladder attempts, cost/density Gate 1, fail-closed downstream admission, and the CRWD-style mature-row blocker pattern.
CRWD 5m PDA/MTF downstream fail-closed pattern: `references/crwd-5m-pda-mtf-downstream-failclosed.md` — exact branch/evidence snapshot for a cost-positive, hazard/readiness-passing CRWD 5m branch that remains observation-only because mature rows are insufficient; reminds agents to inspect nested execution-tree ranker fields before judging ranker absence.

Dense downstream SIGTERM readback: `references/dense-downstream-sigterm-readback.md` — when a downstream factor-training runner exits 143/-15, classify the process as incomplete, inspect sibling completed `downstream-*` runs, and fail-close repeated high-hazard/PDA-mismatch branches instead of rerunning blindly.

Provider portability before promotion: `references/provider-portability-before-promotion.md` — when an IBKR-specific MTF factor is promising but a YF/TVR/IBKR/Kraken or similar provider-portability AQ rank is mixed/negative; stop before downstream if no provider row is positive, while preserving the original provider-specific branch as incubate-only.

IBKR ORB/RVOL regime-rooted chain session: `references/ibkr-orb-rvol-regime-chain-session.md` — when turning public ORB/RVOL or similar sourced factors into `1m -> 5m -> 15m -> 30m -> 1h` materials; records the IBKR QQQ ORB/RVOL Gate 1 + BBN/CatBoost/execution-tree fail-closed pattern, provider quartet probes, and exact promotion blockers.

External harvest -> offline practical candidates: `references/external-harvest-offline-practical-candidates.md` — when the user asks to self-source papers/repos/X/open-source strategies and move toward usable factors; reimplement formulas as sidecar candidates, benchmark on existing provider CSVs, import survivors through BBN/CatBoost/execution tree, and fail-closed until mature feedback exists.

BBN / execution-tree stagnation diagnostic: `references/bbn-execution-stagnation-diagnostic.md` — when factor training shows no breakthrough; separates candidate quality, BBN gating, CatBoost/runtime consumption, mature target rows, entry-model bridge gaps, and execution-tree guardrails.

Bridge gap vs execution admission: `references/bridge-gap-vs-execution-admission.md` — when `bridge_needs_confirmation` is cleared but `execution_tree_trace.json` remains `transition_guardrail` / `observe`; separates bridge threshold, transition hazard/PDA disagreement, and execution-readiness gates.

Mature target rows from feedback replay: `references/mature-target-rows-from-feedback-replay.md` — when analyze exists but target maturity/training-weight rows are zero; use copied state + RealTradeRecord JSONL ingest + re-export, with strict truth labels for sample-trade replay vs live fills.

### Stage 3：BBN 证据节点（bbn/evidence.rs）

用户特定特征（VRP V2 相关）：
- `qqq_hv_level`：QQQ 历史波动率水平
- `nq_vs_200d_pct`：NQ 相对 200 日均线位置
- `vix3m_level`：VIX3M 水平
- `qqq_hv_pct_rank_252`：QQQ HV 252 日百分位
- `vvix_over_vix`：VVIX/VIX 比率

**验收标准**：BBN 后验概率更新必须可追溯。

### Stage 4：CatBoost 路径排名

**外部训练器**：`scripts/auto_quant_external/pandas_path_ranker_trainer.py`

```bash
# 导出 target
./target/debug/ict-engine export-structural-path-ranking-target \
  --symbol <SYM> --state-dir /tmp/<state>

# 训练/生成 scores
python scripts/auto_quant_external/pandas_path_ranker_trainer.py \
  --apply --target-csv <target.csv> --output-scores scores.csv

# 应用 scores
./target/debug/ict-engine apply-structural-path-ranking-external-scores \
  --symbol <SYM> --state-dir /tmp/<state> --scores-file scores.csv

# 注册训练器
./target/debug/ict-engine register-structural-path-ranking-trainer-artifact \
  --symbol <SYM> --state-dir /tmp/<state> \
  --artifact-uri file://trainer_artifact.json \
  --model-family catboost --score-column raw_path_score
```

**训练器特性**：
- 零配置：默认行为可直接运行
- 热插拔：用户可通过 `user_weights.json` 自定义权重
- 回退机制：当 VRP V2 特征缺失时，使用 `structural_baseline_score` 或 `current_posterior`

### Stage 5：执行树（execution_tree.rs）

执行树分支：
- `block_crowded`：拥挤阻断
- `wait_for_reversion`：等待回归
- `fill_viable`：填充可行
- `transition_guardrail`：转换护栏

**验收标准**：执行树 trace 必须包含 CatBoost 贡献记录。

---

## Pitfalls

### Repo closure audit: defined module is not enough

When auditing factor iteration → practical advice, prove each layer is consumed by the next runtime layer, not merely present in source:
- `market_state` primary/secondary labels must enter main analyze, BBN evidence, execution tree, or workflow/report output; otherwise they are sidecar code.
- Profit-factor materials must carry regime branch fields (`main_regime`, `sub_regime`, `sub_sub_regime_or_profit_factor`, `profit_factor`, `regime_profit_branch_path`) before Auto-Quant dispatch. If rank output loses these fields, stop before BBN/CatBoost.
- BBN `pass_to_bbn=false` must actually block or explicitly neutralize inference; a recorded flag alone is not closure.
- CatBoost/path-ranker scores must appear in `execution_tree_trace.json` if the acceptance criterion says execution tree trace contains CatBoost contribution. Workflow-status visibility alone is not enough.
- `recommended_command` often changes only indirectly through selected path; if the user asks for practical advice evidence, check human next-action text includes ranker/BBN/regime reasons.
- Before validation, run `git status --short`; dirty unrelated edits can block `cargo check`. Report that rather than patching unrelated work.
- Multi-agent Board docs are authoritative. Claim a unique lane in the plan/doc first, append Done/Blocked/Handoff evidence after, and do not edit or rerun another agent's active/completed branch.

See `references/repo-audit-factor-to-execution-closure.md` and `references/regime-branch-provider-autoquant-chain.md` for the full checklist.

### Provider readiness parity: shell matters

When `provider-status` or provider fetches look unhealthy from Hermes, verify with the operator shell before diagnosing provider failure. On this host, non-login bash may resolve `python3` to Anaconda without `ccxt`/`redis`/`ib_async`, while zsh login resolves the provider-ready Python. Use:

```bash
zsh -lc 'cd ~/projects-ict-engine/ict-engine && .local-artifacts/cargo-target/debug/ict-engine provider-status --compact'
```

or the explicit provider Python `~/.venvs/ict-engine-provider-py313/bin/python` for fetch scripts. Capture this as a runtime-parity fix, not as provider failure. See `references/provider-runtime-repair.md`.

### IBKR max-window and sparse-signal traps

When the user asks for 10Y/history expansion, do not assume one duration works for every asset or bar size. Probe the largest usable ceiling per asset/bar size, then remeasure strict signal density. Very high win rate with tiny trade count usually means sparse opportunity density, not a durable edge. See `references/max-window-expansion-and-opportunity-density.md`.

### No-breakthrough diagnosis: prove the failing layer

When factor training looks stalled, do not jump straight to new factor ideation. First audit the existing chain with `references/bbn-execution-stagnation-diagnostic.md`:
- Gate 1 failed, `downstream_allowed=false`, or `strict_training_rows=0` means candidate quality / schema is the blocker; stop before BBN.
- BBN is healthy if `strategies_applied`, `evidence_value_gate_passed`, entropy/log-loss deltas, and posterior changes exist.
- CatBoost/path-ranker is healthy if execution tree has `output.path_ranker_score_visible_to_execution_tree=true` and `output.path_ranker_score_used_by_execution_tree=true`.
- No promotion despite healthy BBN/ranker usually means `mature_rows=0`, `rows_with_training_weight=0`, `entry_models[*].matched_rows=0`, `closed_loop_branch_admission.status=fail_closed`, `bridge_needs_confirmation`, or `transition_guardrail`.
- If real trades were ingested but target/entry rows stay zero, the missing bridge is feedback ledger -> policy/entry training rows, not another BBN run.

### Target CSV 行数不足

**症状**：target CSV 只有几行，特征列缺失。
**原因**：VRP V2 等因子特征未在 analyze 阶段注入。
**对策**：训练器使用 `structural_baseline_score` 回退，生成可用分数。

### CatBoost/XGBoost 未安装

**症状**：训练器报 `ERROR: catboost not installed` 或 `RuntimeError: catboost requested but not installed`。
**对策**：若验收要求真实 CatBoost，先用 `uv run --with pandas --with numpy --with catboost python support/scripts/auto_quant_external/pandas_path_ranker_trainer.py ...` 重跑 train/apply；不要只因当前解释器缺包就降级。若任务允许 fallback，再使用加权求和回退模式，基于 `structural_baseline_score` 生成分数。
**重要**：若训练器产物 `trainer_artifact.json` 写的是 `model_family=weighted_feature_sum_v1`，注册时必须使用同一 `--model-family weighted_feature_sum_v1`；不要把 fallback 产物硬注册成 `catboost`。

### 成熟样本为 0

**症状**：`policy-training-status` 显示 `mature_rows=0` 或 `rows_with_training_weight=0`，但 analyze snapshot / BBN / path-ranker 分数已经存在。
**原因**：目标数据缺少可消费的结构化反馈记录，或反馈未桥接到 policy/entry training rows。
**对策**：优先确认 `workflow_snapshot.latest_analyze` 存在；若需要验证反馈桥，复制 state 后按 `references/mature-target-rows-from-feedback-replay.md` 用 `auto-quant-ingest-real-trades` 回灌 `RealTradeRecord` JSONL，再 `export-structural-path-ranking-target`。如果只是 AQ sample_trades 回放，必须标成 diagnostic/sample replay，不可当 live fill。执行树仍 `observe/transition_guardrail` 时继续 fail-closed。

### Dense K-line / Auto-Quant mixed-packet pitfalls

- Auto-Quant material `timerange` must be a valid `YYYYMMDD-YYYYMMDD`; descriptive placeholders such as `source_artifact_window` make Freqtrade fail before ranking.
- `pandas_path_ranker_trainer.py` training writes the CatBoost model and `trainer_artifact.json`; run a second `--apply --model-dir ... --output-scores ...` pass before `apply-structural-path-ranking-external-scores`.
- `execution_tree_trace.json` stores ranker evidence under `output.*`; check nested `output.path_ranker_score_visible_to_execution_tree`, `output.path_ranker_score_used_by_execution_tree`, and `output.path_ranker_model_family`.
- If Auto-Quant bootstrap cannot clone remotely but an existing checkout is present under another run's `state/auto-quant/.deps/auto-quant`, pass that local path via `--repo-url`; capture this as a reproducibility workaround, not as a permanent network/tool limitation.
- Dense samples can reveal timeframe split behavior. If `1m/5m` are positive but `15m/30m` are negative, mark the mixed packet `incubate` or split branches; do not promote on aggregate enthusiasm.
- Before structural-feedback replay, export real per-trade rows from Freqtrade/Auto-Quant `trades`; aggregate rank summaries are not acceptable feedback source data. Verify `sum(profit_abs) == profit_total_abs` and preserve branch path + provider/timeframe provenance.
- For repeated replay sessions on the same symbol, read `state/<SYMBOL>/learning_state.json` first and skip already-consumed feedback rows instead of replaying from zero. This keeps replay idempotent and avoids inflating history with duplicate rows.
- When a feedback PnL can be negative, pass `--pnl=<value>` as a single CLI token. Do not split it into `--pnl <value>` or the leading minus may be parsed as a new flag.
- For repeated replay sessions on the same symbol, read `state/<SYMBOL>/learning_state.json` first and skip already-consumed feedback rows instead of replaying from zero. This keeps replay idempotent and avoids inflating history with duplicate rows.
- When a feedback PnL can be negative, pass `--pnl=<value>` as a single CLI token. Do not split it into `--pnl <value>` or the leading minus may be parsed as a new flag.

### 市场状态置信度过低

**症状**：分类器输出高置信比例 < 5%，大量 VeryLow 样本。
**原因**：
1. 各维度置信度计算过于严格（中间值得分接近 0）
2. 一致性计算采用"全有全无"模式
3. 聚合阈值过高
4. 极端状态检测过于敏感

**对策**：
1. 添加基础置信度（vol: 0.35, liq: 0.30, overall: 0.20）
2. 一致性采用部分匹配得分（默认 0.2，部分 0.4-0.5）
3. 降低分类阈值（trend: 0.50, reversal: 0.50）
4. 提高结构权重至 50%
5. 收紧极端状态阈值（波动: 0.75, 流动性: 0.80）

**参考**：`references/market-state-confidence-tuning.md`

---

## 状态验证

```bash
# 检查训练状态
./target/debug/ict-engine policy-training-status \
  --symbol <SYM> --state-dir /tmp/<state> --human

# 检查执行树
./target/debug/ict-engine workflow-status \
  --symbol <SYM> --state-dir /tmp/<state> --human
```

关键指标：
- `trainer_artifact=ready` — 训练器已注册
- `raw_scored_mature >= 30` — 有足够成熟 target rows；注意这是 target-row 口径，不等同于 feedback observation 条数
- `calibration=not_fitted` — 需要更多校准数据

---

## 多维度覆盖要求

每次因子迭代必须满足：

### 多品种
- 指数期货：NQ, ES, YM, RTY
- ETF 代理：SPY, QQQ, IWM, DIA
- 商品/金属：GC, CL, XAU
- 外汇：EUR, GBP, JPY
- 个股：AAPL, MSFT, NVDA, TSLA
- 加密：BTC/USDT, ETH/USDT, SOL/USDT

### 多时间周期
- `1m` → `5m` → `15m` → `1h` → `4h` → `1d` → `1w` → `1M`

### 多共振
- 低周期触发必须检查高周期共振
- 共振结果：aligned / contradicted / neutral / missing

---

## 迭代不理想时

- 去 arXiv 搜索：`trading factor` + `machine learning`
- 去 GitHub 搜索：`trading strategy` + `factor library`
- 搜索：`momentum factor` / `mean reversion factor` / `volatility risk premium`
- 搜索：`ICT trading` + `smart money concepts` + `factor`

---

## Factor Hot-Plug Architecture

### 8 Factor Categories (Rust Enum)

| Category | Family | Compute | Status |
|---|---|---|---|
| `TrendMomentum` | B | `evaluate_trend_momentum` | active |
| `VolatilityMeanReversion` | D | `evaluate_volatility_mean_reversion` | active |
| `StructureIct` | A | `evaluate_structure_ict` | active |
| `CrossMarketSmt` | C | `evaluate_cross_market_smt` | active |
| `OptionsHedging` | G | `evaluate_options_hedging` | active |
| `CrowdingHerding` | E | `evaluate_crowding_herding` | new stub |
| `SpectralRhythm` | F | `evaluate_spectral_rhythm` | new stub |
| `SessionLiquidity` | H | `evaluate_session_liquidity` | new stub |

### Adding a New Factor Family

1. Add variant to `FactorCategory` enum in `src/factor_lab/factor_definition.rs`
2. Add `fn <variant>() -> FactorDefinition` constructor
3. Register in `FactorRegistry::default()` in `src/factors/registry.rs`
4. Add compute path: `fn evaluate_<variant>(&self, candles) -> Vec<FactorSignal>`
5. Add dispatch arm in `FactorDefinition::evaluate()` match
6. Add `allowed_roles()` arm for new category
7. Add `is_footprint_context_only()` variant if applicable
8. Add 3 mutation arms: `mutation_parameter_group`, `mutation_direction_hint`, `mutation_step_size_hint`
9. Update `AGENTS.md` traceability table
10. Update `docs/factor-catalog.md`

### Why Agents Say "No Factors"

Root causes and fixes:
1. **No AGENTS.md** → agents had no entry map. Fix: `AGENTS.md` now exists with full traceability table.
2. **Families E/F/H had zero code** → grep returns nothing. Fix: enum variants + compute stubs added.
3. **Factor code split across `factor_lab/` and `factors/`** → no index. Fix: `docs/factor-catalog.md` single-page index.
4. **5500-line TODO doc unscannable** → agents can't parse 436KB. Fix: catalog + AGENTS.md provide scannable summaries.

## Auto-Quant Output Path Isolation

Auto-Quant artifacts MUST NOT pollute the repo root. Path resolution:

```
ICT_ENGINE_AUTO_QUANT_OUTPUT_DIR env var  (highest priority)
  → if set and non-empty, use that path
  → else: <state-dir>/auto-quant/  (subdirectory, never root)
```

Implementation: `resolve_auto_quant_output_dir()` in `src/main.rs`. All auto-quant
shell functions in `src/auto_quant_command.rs` resolve through `aq_state_dir()`.

Default behavior unchanged: `--state-dir /tmp/...` still works. But when using
default `state/`, auto-quant now lands in `state/auto-quant/` instead of `state/`.

## Agent Entry Map

`AGENTS.md` at repo root is the first file any AI agent should read. It contains:
- Factor traceability table (Rust enum → family → code location → status)
- Design-level family gaps (what's missing beyond the 8 Rust categories)
- Key source paths (factor_lab, factors, factor_lifecycle, regime, bbn, execution_tree)
- Hot-plug convention (how to add new families)
- Architecture rules (zero-config, token-friendly, no pollution, auto-quant isolation)

## Pitfalls (new)

### Adding FactorCategory but forgetting mutation surface

**Symptom**: `cargo check` fails with `non-exhaustive patterns` on `mutation_parameter_group`,
`mutation_direction_hint`, or `mutation_step_size_hint`.
**Root cause**: These three methods all match on `self.category` and require arms for every variant.
**Fix**: Add a match arm for the new variant in ALL THREE methods. The minimal pattern is:
```rust
FactorCategory::NewVariant => match reason {
    "balanced_accuracy_regressed" | "bull_bear_separation_regressed"
    | "bull_bear_separation_weak" | "worst_market_separation_weak" => vec![...],
    "bridge_gap_regressed" | "bridge_gap_too_small"
    | "worst_market_bridge_gap_too_small" => vec![...],
    "pre_bayes_gate_regressed" | "pre_bayes_gate_observe_only"
    | "pre_bayes_gate_neutralized" => vec![...],
    _ => Vec::new(),  // or BTreeMap::new() for the hint methods
},
```

### Cargo check: non-exhaustive patterns after FactorCategory extension

**Symptom**: 3 compile errors all pointing to the same new variants.
**Root cause**: Three match blocks in `factor_definition.rs` all need exhaustive arms.
**Fix**: Add arms in `mutation_parameter_group` (line ~528), `mutation_direction_hint` (line ~637),
`mutation_step_size_hint` (line ~769). All three must be covered or `cargo check` will not pass.

### Impl block after #[cfg(test)] mod tests — clippy items-after-test-module

**Symptom**: `cargo clippy -D warnings` fails with `error: items after a test module`.
**Root cause**: Adding compute stubs as a second `impl FactorDefinition {}` block at the end of
`factor_definition.rs`, after the `#[cfg(test)] mod tests` block. Clippy forbids items after test modules.
**Fix**: Move ALL `impl` blocks BEFORE `#[cfg(test)] mod tests`. The test module must be the last
item in the file. If you need to add methods, insert them into the first `impl` block or place the
new `impl` block before the test module.

### FactorHotplugConfig import path differs between lib and bin crate

**Symptom**: `failed to resolve: unresolved import` for `FactorHotplugConfig`.
**Root cause**: `src/` files included via `mod` in `main.rs` are in the binary crate, not the lib crate.
Lib crate files use `crate::factors::FactorHotplugConfig`. Binary crate files (main.rs, its direct
mods like auto_quant_command.rs, factor_research_runtime.rs) must use `ict_engine::factors::FactorHotplugConfig`.
**Fix**: Check which crate the file belongs to. If `src/lib.rs` re-exports it → `crate::`. If it's a
direct `mod` in `main.rs` → `ict_engine::`.

### Auto-Quant shell functions must resolve output dir through aq_state_dir()

**Symptom**: Auto-Quant artifacts land in repo root `state/<SYM>/` instead of `state/auto-quant/<SYM>/`.
**Root cause**: Shell functions in `src/auto_quant_command.rs` passed `state_dir` directly to
underlying commands, bypassing `resolve_auto_quant_output_dir()`.
**Fix**: Every auto-quant shell function must call `aq_state_dir(state_dir)` (which calls
`resolve_auto_quant_output_dir`) and pass the resolved path to the command layer.
New shell functions MUST NOT pass raw `state_dir` to auto-quant commands.

### experiment state_* dirs polluting repo root

**Symptom**: 20+ `state_autoresearch_*`, `state_cluster_*`, etc. scattered at repo root.
**Root cause**: Auto-research and other commands use `--state-dir state_<experiment>` which creates
directories at the repo root level.
**Fix**: Consolidate experiment state dirs under `state_experiments/`. Add `state_experiments/` to
`.gitignore`. Production state stays in `state/` (already gitignored).

---

## 联系文档

- 因子迭代 board：`docs/plans/2026-05-05-execution-tree-factor-auto-quant-todo.md`
- 运行时闭环 board：`docs/plans/2026-05-07-auto-quant-post-factor-runtime-closure-todo.md`
- 应做事项：`docs/plans/2026-05-07-ict-engine-action-items.md`
- 市场形态定义：`src/factor_lab/pda_prior.rs`
- BBN 证据：`src/bbn/evidence.rs`
- 执行树：`src/application/orchestration/execution_tree.rs`
- **市场状态分类参考**：`references/market-state-classification.md` — 分类器详细参数、聚合逻辑、扩展点
- **因子族 E/F/H 计算桩**：`references/factor-families-efh-compute.md` — 子因子公式、参数表、变异面、已知限制
- **因子热插拔 handoff**：`docs/plans/2026-05-09-factor-hotplug-handoff-todo.md` — 实时 TODO
- **因子目录**：`docs/factor-catalog.md` — 8 族单页索引
- **Agent 入仓地图**：`AGENTS.md` — agent 首读文件

## Hot-Plug FactorRegistry::default() Sweep

When `FactorRegistry::default()` is called, the hotplug config should be applied
immediately after if a `state_dir` is in scope. The pattern:

```rust
let mut registry = FactorRegistry::default();
FactorHotplugConfig::apply_to_registry_if_present(state_dir, &mut registry);
```

Call sites that NEED hotplug (mutable registry + state_dir available):
- `src/main.rs` analyze path (line ~4013) — DONE
- `src/factor_research_runtime.rs` (line ~48) — DONE
- `src/factor_backtest_runtime.rs` `run_factor_backtest` — DONE
- `src/application/data_sources/sop_reports.rs` (line ~429) — DONE

Call sites that are immutable refs (`&FactorRegistry::default()`) or lack
`state_dir` in scope (e.g., regime/recovery.rs, persistence.rs, mutation_templates.rs)
use the full 8-family default and are NOT hotplugged — this is acceptable since
those paths do evaluation/mutation against all families by design.

---

## Development / Extending the Architecture

This section covers developing new modules for the ICT-Engine. Apply these patterns when adding factor families, market state classifiers, confidence validation, or any new submodule — not when running the pipeline (see sections above).

### Core Dev Principles

- **Zero-Config** &mdash; every module provides `Default::default()` for consumer-ready use, plus `with_config(custom)` for hot-pluggable customization
- **No pollution** &mdash; don't modify existing code; modules are self-contained
- **No debt** &mdash; each new file carries its tests inside `#[cfg(test)]`

### Adding a New Module

```rust
// Module file: src/market_state/<module>.rs

/// Config struct with Default
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ModuleConfig {
    pub threshold: f64,
}

impl Default for ModuleConfig {
    fn default() -> Self { Self { threshold: 0.65 } }
}

pub struct Module { config: ModuleConfig, }

impl Module {
    pub fn new() -> Self { Self::with_config(ModuleConfig::default()) }
    pub fn with_config(config: ModuleConfig) -> Self { Self { config } }
}

impl Default for Module { fn default() -> Self { Self::new() } }

#[cfg(test)]
mod tests {
    // Default config works / Custom config works / Edge cases / Confidence thresholds
}
```

Then register in `src/market_state/mod.rs`.

### Three-Layer Confidence System

Located in `references/confidence-validation-implementation.md`.

| Layer | File | Purpose |
|-------|------|---------|
| Historical Backtest Validation | `confidence_validation.rs` | Rolling window per-regime calibration |
| Enhanced Aggregation | `enhanced_aggregation.rs` | Price direction + 5-way consistency |
| Intelligent Secondary Classification | inline in aggregation | Vol+Behavior+PriceDir → secondary regime |

Key parameters: `history_window=252`, `min_samples=30`, `high=0.75`, `medium=0.55`, `low=0.35`.

### Adding a New FactorFamily

1. Add variant to `FactorCategory` enum in `factor_definition.rs`
2. Add `fn <variant>() -> FactorDefinition` constructor
3. Register in `FactorRegistry::default()` in `registry.rs`
4. Add compute path: `fn evaluate_<variant>(...)`
5. Add dispatch arm in `FactorDefinition::evaluate()`
6. Add 3 mutation arms: `mutation_parameter_group`, `mutation_direction_hint`, `mutation_step_size_hint`
7. Update `AGENTS.md` traceability table and `docs/factor-catalog.md`

**Watch for**: `non-exhaustive patterns` on the three mutation methods after adding a new variant — all three need an arm.

### Dev Pitfalls

- **Cargo timeout** &mdash; if `cargo check` hangs >60s, skip it, commit code + tests, mark "⏳ compilation pending". Do not block progress on compilation.
- **Items after test module** &mdash; `clippy -D warnings` rejects impl blocks after `#[cfg(test)]`. Keep `mod tests` as the last item.
- **Lib vs bin crate import** &mdash; lib crate files use `crate::factors::`; binary crate files (direct `mod` in `main.rs`) use `ict_engine::factors::`.
- **Missing price direction** &mdash; always classify Bull/Bear/Neutral from a 20-bar window (2% threshold) before classifying secondary regime.
- **Over-simplified aggregation** &mdash; weighted average loses dimension conflicts. Use multi-dimensional consistency checks (5-way).
- **Auto-Quant shell output dir** &mdash; every shell function must call `aq_state_dir(state_dir)` not pass raw `state_dir` to commands.
- **Mutation surface on new variants** &mdash; three match blocks in `factor_definition.rs` need exhaustive arms for every variant. All three must be covered.
- **`impl` block after test module** &mdash; when adding compute stubs for new families, place ALL `impl` blocks BEFORE `#[cfg(test)]`.

### Commit Pattern

```text
feat(market_state): <module-name> - <one-line-summary>

<details>
- Feature 1
- Feature 2

Design: zero-config, hot-pluggable
Tests: ✅ Test 1, ✅ Test 2
```

## Maturity and execution-tree guardrails

- When replaying structural feedback to recover mature target rows, copy the state root first (`state_*_matured`) and keep the original run untouched.
- If feedback comes from reconstructed/sample trades rather than broker fills, label the source as diagnostic replay (`diagnostic_sample_trade_structural_feedback`) and keep `trade_usable=false` / non-live label fields where supported.
- After replay ingest, always re-export the structural path-ranking target, retrain/apply/register CatBoost, enable runtime, then rerun `analyze`, `workflow-status`, `policy-training-status`, and inspect `execution_tree_trace.json`.
- Treat these as separate gates: ranker maturity (`raw_scored_mature`, `production_validation`, `observation_validation`) and execution admission (`branch`, `execution_bias`, `gate_status`). A ready CatBoost ranker can still remain blocked by `bridge_needs_confirmation` or `transition_guardrail`.
- See `references/diagnostic-feedback-replay.md` for the concrete replay pattern.

## Repo Directory Hygiene

- Production state: `state/` (gitignored, `--state-dir state` default)
- Auto-Quant output: `state/auto-quant/` (subdirectory isolation, env var override)
- Experiment state: `state_experiments/` (gitignored, consolidated from scattered `state_*`)
- Agent entry map: `AGENTS.md` at repo root
- Factor index: `docs/factor-catalog.md`
- Hotplug config: `<state-dir>/factor_hotplug.yaml` or `ICT_ENGINE_FACTOR_HOTPLUG_CONFIG`
