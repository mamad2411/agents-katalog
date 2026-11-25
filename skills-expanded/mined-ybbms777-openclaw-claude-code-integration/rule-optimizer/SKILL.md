---
name: rule-optimizer
description: 规则优化框架。追踪每条规则的效能指标（触发频率、成功率、延迟、满意度），自动评估规则健康度，建议优化变体，支持A/B测试框架。规则从静态生成升级到动态优化。
model: minimax-portal/MiniMax-M2.7
effort: medium
---

# Rule Optimizer — 规则优化框架

## 功能概述

将规则从**静态生成**升级到**动态优化**。持续追踪每条规则的实际效能，自动识别低效能规则并建议改进版本，支持A/B测试验证。

## 核心功能

### 1. 规则效能评分（0-100）

基于4个独立指标的加权评分：

| 指标 | 说明 | 权重 |
|------|------|------|
| 修复成功率 | 规则实际解决问题的概率 | 60% |
| 用户满意度 | 用户对规则的评价（1-5） | 40% |
| ⚠️ 延迟开销 | 规则执行的时间成本 | -（扣分） |
| ℹ️ 触发频率 | 规则触发的频繁程度 | -（监控） |

**评分含义**：
- **80-100** 🟢 **优秀** — 保持活跃，推荐推广
- **50-79** 🟡 **中等** — 监控中，考虑优化
- **20-49** 🟠 **低效** — 进入A/B测试，建议变体
- **<20** 🔴 **废弃** — 考虑删除或深度修改

### 2. 自动规则变体建议

基于效能数据自动推荐改进方向：

```
效能 < 50% ?
  ├─ 建议 "宽松版"：减少条件，降低误检
  ├─ 建议 "严格版"：增加条件，提高准确性
  └─ 建议 "混合版"：条件重新平衡
```

示例：

```
原规则 (score=32)：
  规则：用户说"不对"时立即停止 → 误检率高

建议变体 v1_loose (a/b=5%):
  修改：用户连续说"不对"3次才停止
  期望：降低误检，提高有效性

建议变体 v1_strict (a/b=5%):
  修改：用户说"不对"且操作≥2秒时停止
  期望：提高准确性，减少漏检
```

### 3. A/B 测试框架

自动管理规则变体的试验和升级：

```
规则 v1 (score=65)
  ├─ 变体 v1_loose (a/b=5%)
  │  ├─ 试验100个用户
  │  └─ 结果：score=72 ✓ 升级为主规则
  │
  └─ 变体 v1_strict (a/b=5%)
     ├─ 试验100个用户
     └─ 结果：score=58 ✗ 废弃
```

### 4. 规则生命周期管理

```
Active (高效)
  └─→ 保持监控
  
Active (中效)
  └─→ 进入A/B测试
      ├─→ 变体升级成功 → 新的Active
      └─→ 变体失败 → 继续优化或Testing
      
Testing (试验中)
  └─→ 等待A/B结果
      ├─→ 成功 → Active
      └─→ 失败 → 调整后重试
      
Deprecated (低效)
  └─→ 考虑删除或深度改造
```

---

## 使用方式

### Python API

```python
from skills.rule_optimizer.scripts.rule_optimizer import RuleOptimizer

optimizer = RuleOptimizer()

# 1. 评估规则效能
metrics = optimizer.evaluate_rule_effectiveness("rule_never_modify_funds")
print(f"效能评分: {metrics.effectiveness_score}")
print(f"成功率: {metrics.fix_rate}%")
print(f"用户满意度: {metrics.user_satisfaction}/5")

# 2. 建议优化变体
variants = optimizer.suggest_rule_variants("rule_never_modify_funds")
for v in variants:
    print(f"建议: {v.variant_id} - {v.modification}")

# 3. 记录规则应用
optimizer.record_rule_application(
    rule_id="rule_never_modify_funds",
    fixed=True,           # 规则是否解决了问题
    latency_ms=15.5,      # 执行延迟
    satisfaction=4.5      # 用户满意度(1-5)
)

# 4. 记录A/B测试结果
optimizer.record_ab_test_result(
    variant_id="rule_loose_v1",
    effectiveness=78.5,   # 测试结果效能评分
    sample_count=100      # 测试样本数
)
```

### CLI 使用

```bash
# 评估规则效能
python3 rule_optimizer.py rule_123 --evaluate

# 获取优化建议
python3 rule_optimizer.py rule_123 --suggest

# 记录规则应用
python3 rule_optimizer.py rule_123 --record --fixed --latency 15.5 --satisfaction 4.5

# 记录A/B测试
python3 rule_optimizer.py rule_123_variant --record-ab --effectiveness 78.5 --sample-count 100
```

---

## 数据模型

### RuleMetrics（规则指标）

```python
@dataclass
class RuleMetrics:
    rule_id: str
    trigger_frequency: int          # 过去7天触发次数
    fix_rate: float                 # 修复成功率 (%)
    cost_overhead_ms: float         # 平均延迟 (ms)
    user_satisfaction: float        # 平均满意度 (1-5)
    
    effectiveness_score: float      # 计算得出: 0-100
    status: str                     # active/testing/deprecated
    variants: List[str]             # 相关的变体IDs
```

### RuleVariant（规则变体）

```python
@dataclass
class RuleVariant:
    variant_id: str
    parent_rule_id: str
    modification: str               # 具体修改说明
    a_b_test_sample: float          # A/B份额 (0-1)
    
    trial_effectiveness: Optional[float] = None  # 试验结果
    status: str = "pending"         # pending/active/rejected
```

---

## 效能评分算法

```python
# 步骤1：基础分数（修复成功率为主）
base_score = fix_rate

# 步骤2：加权用户满意度
satisfaction_pct = (user_satisfaction / 5.0) * 100
weighted_score = (base_score × 0.6) + (satisfaction_pct × 0.4)

# 步骤3：延迟惩罚
if latency > 100ms:
    weighted_score ×= 0.8          # 扣20%
elif latency > 50ms:
    weighted_score ×= 0.9          # 扣10%

# 最终得分：0-100
final_score = clamp(weighted_score, 0, 100)
```

**示例计算**：

```
规则A：
  - 成功率: 85%
  - 满意度: 4.5/5 (90%)
  - 延迟: 25ms

  base = 85
  weighted = (85 × 0.6) + (90 × 0.4) = 51 + 36 = 87
  final = 87 (无延迟惩罚)
  → 评分: 87 (优秀) ✅

规则B：
  - 成功率: 60%
  - 满意度: 2.5/5 (50%)
  - 延迟: 150ms

  base = 60
  weighted = (60 × 0.6) + (50 × 0.4) = 36 + 20 = 56
  final = 56 × 0.8 = 44.8 (因延迟扣分)
  → 评分: 45 (低效) ⚠️
```

---

## 工作流例子

### 例子：优化"用户纠正"规则

```
1. 初始状态
   规则：detect_user_correction
   效能: 45 (低效)
   建议: 宽松版本试验

2. A/B 测试
   - 5%用户试用 detect_user_correction_loose
   - 收集100个样本
   - 新效能: 72 ✓

3. 升级决策
   - detect_user_correction_loose → 新主规则
   - detect_user_correction → 废弃 (replaced)
   - 记录变更到AGENTS.md

4. 继续监控
   - 新主规则效能继续被追踪
   - 如果后续效能下降，再次进入测试循环
```

---

## 集成点

### 与 Week 1-4 系统
- ✅ 追踪 evolve 生成规则的效能
- ✅ 监控自 behavior_analyzer 的异常判定
- ✅ 整合 fusion_engine 的决策质量

### 与 OpenClaw 钩子
- `rule:applied` — 记录规则应用
- `user:feedback` — 收集用户满意度
- `a_b:test_complete` — A/B测试完成

---

## 测试覆盖

```bash
pytest skills/rule-optimizer/tests/ -v
# 9/9 通过
```

---

## 性能指标

- **评估耗时**: < 100ms
- **内存开销**: < 20MB
- **数据保留**: 无限制（历史日志）
- **并发**: 支持 ≥ 100 并发评估

---

## 故障排查

### 问题：所有规则都是"中等"评分

**原因**：缺少历史数据或满意度反馈不完整
**解决**：
1. 确保 `.rule-metrics.jsonl` 在增长
2. 加强用户反馈收集
3. 监控一周后重新评估

### 问题：A/B测试变体总是失败

**原因**：修改方向错误或A/B样本太小
**解决**：
1. 增加A/B样本比例（从5%→10%）
2. 重新分析规则的问题根源
3. 尝试相反方向的变体（如松散改严格）

---

## 许可

遵循项目主许可证。

