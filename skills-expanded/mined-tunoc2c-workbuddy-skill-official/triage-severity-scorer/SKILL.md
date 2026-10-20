---
name: triage-severity-scorer
pack: universal
description: 给一个错误簇按九个维度打 0~1 分,再用权重合成严重度。triage 引擎的核心评分器,被 triage_engine.py 自动调用;也可被 architect 手动调用复核某张工单的分数。
when_to_use: triage_engine 处理每个错误簇时;架构师怀疑某工单"被低估"或"被夸大"想复核时。
when_NOT_to_use: 不要用它来"决定要不要建单"——那是阈值 + 历史去重的事,只用分数排序与触发不同响应级别。
---

# Skill: Triage Severity Scorer

## 九个维度(权重总和 = 1.0)

| 维度 | 权重 | 0 分长什么样 | 1 分长什么样 |
|---|---|---|---|
| **frequency** | 0.18 | <1 次/天 | >50 次/天 |
| **user_impact** | 0.18 | 0 个独立用户 | ≥25 个独立用户 |
| **endpoint_criticality** | 0.12 | 内部/调试端点 | 支付/登录/webhook |
| **level** | 0.10 | warn | fatal/panic |
| **is_regression** | 0.12 | 首次出现 | 之前已 closed 的指纹复现 |
| **breadth** | 0.08 | 单一端点 | ≥5 个端点跨越 |
| **trend** | 0.08 | 日均下降 | 相比昨日 ≥3x |
| **revenue_path** | 0.08 | 不触及收入 | 直接阻断收入 |
| **data_integrity** | 0.06 | 只读路径 | 有写/迁移/删除关键字 |

## 给每个维度的"判断锚点"

- **frequency**:用 `min(count / 50, 1.0)`,与原始事件数线性映射。
- **user_impact**:`min(unique_users / 25, 1.0)`。**未捕获 user_id 不要给 0**——看端点性质给 0.3 估值,并在工单里 flag 出"日志缺 user_id"。
- **endpoint_criticality**:端点路径/消息含 `pay|billing|checkout|auth|login|webhook` → 1.0;含 `admin|internal|debug` → 0.4;其他 0.2。
- **level**:`fatal` → 1.0,`error` → 0.5,`warn` → 0.2。
- **is_regression**:查 `state/triage-history.jsonl`——该 fingerprint 是否在过去 30 天有过 closed 记录?有 → 1.0,首次 → 0.0。**回归是最严重的信号之一,优先级永远高于首次出现的同分**。
- **breadth**:`min(unique_endpoints / 5, 1.0)`。
- **trend**:`min(today / max(yesterday, 1), 3) / 3`,即 3 倍及以上算 1.0。
- **revenue_path**:消息或端点含 `pay|billing|checkout|subscription|invoice|refund` → 1.0;其他 0.0。
- **data_integrity**:消息含 `delete|migrate|corrupt|integrity|truncate|drop` → 1.0;含 `write|update` → 0.6;只读 → 0.0。

## 输出

```json
{
  "fingerprint": "afe21543915f",
  "score": 0.507,
  "dimensions": { "frequency": 0.20, "user_impact": 0.40, ... },
  "reason": "支付 webhook 失败 14 次,跨 10 个用户,触及收入路径"
}
```

## 触发不同响应级别(由 triage_engine 用)

- **score ≥ 0.7**:P0,@channel 通知 + 立即建单;若 verifier 判定"用户已经在丢钱",触发 incident 流程
- **0.5 ≤ score < 0.7**:P1,自动建单,@当日 oncall
- **0.35 ≤ score < 0.5**:P2,自动建单,普通分配
- **< 0.35**:不建单,只汇总进每日健康报告

## 反模式

- ❌ 让一个维度的 1.0 直接决定总分——权重的意义就在防它
- ❌ 因为"听起来不严重"就压分——你不是在评估感受,是在打可被反查的分数
- ❌ 忽略 regression 维度——这是预防"修了又坏"循环的唯一信号
