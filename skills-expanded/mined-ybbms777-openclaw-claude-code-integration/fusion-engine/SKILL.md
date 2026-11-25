---
name: fusion-engine
description: 多源数据融合引擎。整合命令执行反馈、用户交互、系统状态信号，生成综合决策上下文评分（0-100）。为工具调用提供4维度融合评分和决策建议。
model: minimax-portal/MiniMax-M2.7
effort: high
---

# Fusion Engine — 多源数据融合引擎

## 功能概述

从三个独立的数据维度收集信息，通过加权融合算法生成综合的决策上下文评分，为精准工具调用提供科学依据。

## 核心功能

### 1. 三维数据融合

| 数据源 | 权重 | 说明 |
|--------|------|------|
| LanceDB 记忆相关性 | 30% | 历史相似操作的可信度和成功率 |
| 命令执行成功率 | 30% | 此工具在历史中的成功率 |
| 用户交互偏好 | 25% | 用户过往决策模式和满意度 |
| 系统状态 | 15% | CPU/内存/磁盘/网络健康度 |

### 2. 融合评分系统

```
综合评分 = (LanceDB相关性 × 0.30) 
         + (命令成功率 × 0.30)
         + (用户偏好 × 0.25)
         + (系统健康 × 0.15)
```

**评分区间**：
- **75-100** 🟢 **自动允许** — 直接执行，高度可信
- **50-74** 🟡 **请求确认** — 向用户确认后执行
- **0-49** 🔴 **阻止** — 阻止执行，可能存在风险或不适当

### 3. 多维度评估

#### 3.1 LanceDB 记忆相关性 (0-100)

评估当前操作在历史中的相似度和可信度：

```python
if 相关记忆存在:
    平均重要性 = 相关记忆的importance平均值
    成功率 = 相关记忆中成功的比例
    
    评分 = 40 + (平均重要性 × 40) + (成功率 × 20)
else:
    评分 = 40  # 无历史，保守估计
```

#### 3.2 命令执行成功率 (0-100)

基于历史执行数据统计：

```python
成功率(%) = (成功次数 / 总执行次数) × 100
评分 = min(100, 成功率(%))
```

#### 3.3 用户交互偏好 (0-100)

整合用户过往的决策模式：

```python
接受率(%) = (用户批准数 / 总交互数) × 100
平均满意度 = 用户给定的满意度评分(1-5)对应的百分制

评分 = (接受率 × 0.6) + (平均满意度 × 0.4)
```

#### 3.4 系统健康状况 (0-100)

实时检测系统资源状态：

```python
CPU分数 = 100 - CPU使用率(%)
内存分数 = 100 - 内存使用率(%)
磁盘分数 = 100 - 磁盘使用率(%)

评分 = (CPU分数 + 内存分数 + 磁盘分数) / 3
```

### 4. 决策推理

每个决策都附带清晰的推理日志：

```json
{
  "tool": "bash",
  "final_score": 73.5,
  "decision": "request_confirm",
  "reasoning": {
    "memory": {
      "score": 75,
      "note": "基于LanceDB中相关记忆的可信度"
    },
    "cmd_success": {
      "score": 80,
      "note": "基于历史执行的成功率"
    },
    "user_pref": {
      "score": 70,
      "note": "基于用户过往决策模式"
    },
    "system": {
      "score": 65,
      "note": "基于系统资源和网络状态"
    }
  }
}
```

---

## 使用方式

### Python API

```python
from skills.fusion_engine.scripts.fusion_engine import MultiSourceFusionEngine

engine = MultiSourceFusionEngine()

# 生成融合得分
score = engine.fuse_decision_context(
    tool_name="bash",
    params={"command": "rm /tmp/test.txt"},
    session_id="session_123"
)

print(f"最终评分: {score.final_score}")
print(f"决策: {score.decision}")  # "auto_allow", "request_confirm", "block"

# 保存决策到日志
engine.save_decision("bash", score, "session_123")
```

### CLI 使用

```bash
# 基础用法
python3 fusion_engine.py bash '{"command": "ls"}'

# 带会话ID
python3 fusion_engine.py write '{"file": "test.txt"}' --session-id session_123

# 保存决策
python3 fusion_engine.py bash '{"command": "rm /tmp/old"}' --save

# 自定义工作目录
python3 fusion_engine.py bash '{"command": "pwd"}' --workspace ~/.openclaw/workspace
```

### 与 yolo_classifier 集成

```python
# 在 yolo_classifier.py 中
from skills.fusion_engine.scripts.fusion_engine import MultiSourceFusionEngine

def classify_with_fusion(tool_name, params, session_id):
    # 第1层：旧的静态分类
    static_risk = yolo_static_classify(tool_name, params)
    
    # 第2层：新的融合评分
    fusion_engine = MultiSourceFusionEngine()
    fusion_score = fusion_engine.fuse_decision_context(
        tool_name, params, session_id
    )
    
    # 综合决策
    if fusion_score.decision == "block":
        return {"risk": "CRITICAL", "reason": "融合评分过低"}
    
    return {
        "risk": static_risk,
        "fusion_score": fusion_score.final_score,
        "decision": fusion_score.decision
    }
```

### 与 behavior_analyzer 集成

```python
# 在决策前检查会话行为
from skills.behavior_analyzer.scripts.behavior_analyzer import SessionBehaviorAnalyzer

analyzer = SessionBehaviorAnalyzer()
metrics = analyzer.analyze_session(session_id)

if metrics.health_score < 40:
    # 会话异常，降低融合评分权重
    engine.weights["user_pref"] = 0.1  # 降低信任
    engine.weights["memory"] = 0.2
```

---

## 数据源

### 输入（自动收集）

1. **历史执行记录** `.command-execution.jsonl`
   ```json
   {"tool": "bash", "status": "success", "timestamp": "..."}
   ```

2. **用户交互记录** `.user-interactions.jsonl`
   ```json
   {"tool": "write", "action": "approved", "satisfaction": 5}
   ```

3. **系统状态** (实时读取 psutil)
   - CPU、内存、磁盘使用率

4. **LanceDB 记忆** (可选)
   - 相关操作的历史记录和效果评分

### 输出（决策日志）

`.fusion-decisions.jsonl`：

```json
{
  "timestamp": "2026-04-11T10:30:00",
  "tool": "bash",
  "session_id": "session_123",
  "fusion_score": 73.5,
  "decision": "request_confirm",
  "components": {
    "memory": 75.0,
    "cmd_success": 80.0,
    "user_pref": 70.0,
    "system": 65.0
  }
}
```

---

## 配置调整

### 权重自定义

```python
engine.weights = {
    "memory": 0.40,      # 增加记忆权重
    "cmd_success": 0.25,
    "user_pref": 0.25,
    "system": 0.10,
}
```

### 决策阈值调整

```python
engine.thresholds = {
    "auto_allow": 80,       # 提高自动执行门槛
    "request_confirm": 50,
    "block": 0,
}
```

---

## 性能指标

- **评分耗时**: < 200ms (typically < 100ms)
- **内存开销**: < 30MB
- **历史保留**: 不限（可按日期分片）
- **并发**: 支持 ≥ 100 并发请求

---

## 测试覆盖

```bash
# 运行所有测试
pytest skills/fusion-engine/tests/ -v

# 生成覆盖率报告
pytest skills/fusion-engine/tests/ --cov=skills.fusion_engine
```

**测试覆盖**：
- ✅ 三维数据独立评估 (3个测试)
- ✅ 有/无历史数据下的评分 (6个测试)
- ✅ 加权融合计算 (1个测试)
- ✅ 决策规则 (3个测试)
- ✅ 系统健康评估 (1个测试)
- ✅ 端到端集成 (2个测试)

---

## 集成点

### 与 Week 1-4 系统
- ✅ 使用 yolo_classifier 的初始风险评级
- ✅ 融合 behavior_analyzer 的会话健康得分
- ✅ 参考 evolve 的规则应用频率
- ✅ 监控 self-eval 的异常记录

### 与 OpenClaw 2.0 钩子
- `agent:tool_dispatch` — 工具调用决策前调用
- `agent:tool_result` — 工具执行后更新历史
- `user:confirmation` — 用户交互时记录偏好

---

## 进阶：自定义融合策略

```python
class CustomFusionEngine(MultiSourceFusionEngine):
    def _evaluate_memory_relevance(self, tool_name, params, session_id):
        # 自定义记忆评估逻辑
        score = super()._evaluate_memory_relevance(tool_name, params, session_id)
        
        # 额外逻辑：如果是金融操作，提高相关性权重
        if "finance" in tool_name or "money" in str(params):
            score *= 1.2
        
        return min(100, score)
```

---

## 故障排查

### 问题：所有操作得分都很低

**原因**：无历史数据或系统资源压力大
**解决**：
1. 检查 `.command-execution.jsonl` 是否在增长
2. 检查系统CPU/内存使用率
3. 调整权重，降低对历史数据的依赖

### 问题：融合得分与实际需求不符

**原因**：权重配置不匹配业务场景
**解决**：根据实际使用情况调整权重配置

---

## 许可

遵循项目主许可证。

