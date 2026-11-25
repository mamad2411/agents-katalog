---
name: sdd-spec-verification
description: >
  SDD（spec 驱动开发）动手实现前的齐备性核验。当用户拿出一份 spec / 设计文档 / mockup
  并问「可以开工了吗」「这份计划齐不齐」「看看还差什么」时使用，或自己准备按 ticket 开工前使用。
  逐条把 spec 里的调研事实与代码实际对照、把 mockup 与 spec 的决策对照、把验收命令真跑一遍。
  产出一分「阻塞项 / 中等问题 / 已核实无误」清单，修完再开工。
agent_created: true
task_type: dev.sdd_spec_verification
---

# SDD 开工前核验（spec 齐备性审查）

## 何时用

- 用户拿出一堆 SDD 文档（spec.md / design-decisions.md / mockup / tickets.md）问能否开工
- 自己准备按 tickets 动手前，先花 15 分钟过一遍本清单

**为什么值得做**：spec 是别人（或上一轮自己）基于记忆/推测写的，调研事实常与代码漂移。
一次核验能抓出「整条数据流建立在错误假设上」这类会导致大面积返工的硬伤。
Parcae 入站网关那次，核验抓出了「复用池的 per-project 统计」这个根本性错误——
实测 `pool.stream()` 根本不记 project usage，而 harness 以流式为主，按原设计做核心功能会是空的。

## 核验六步（按此顺序，每步都要拿代码证据）

### 1. 调研事实逐条对代码（最容易出硬伤）

spec 里凡出现「X 已有 / 复用 X / X 会记录」这类断言，**逐条 grep 验证调用点**，不要看函数名就信。

```bash
grep -n "_record_usage\|_record_call" server/llm_pool/pool.py   # 看调用点落在哪些函数里
```

判据：**调用点所在的函数区间是否覆盖 spec 依赖的那条路径**。
例：`_record_usage` 只在 `call()`/`call_simple()` 内调用 → 流式路径零统计 → spec 说「复用统计」即错。

同理验证：`stream()` 的事件里有没有需要回填的字段（如上游 key 名）；统计结构体到底有几个字段。

### 2. Bounds / 文件归属核对

spec 说「只改 A、B」，核验 A、B 是否真的是那些东西的所在处：

```bash
grep -rn "class CallRecord\|GATEWAY_EXCLUDE =" --include=*.py server/
```

常见坑：
- 数据结构在 `types.py` 而非主模块
- 常量在 `mcp_whitelist.py` 而非 `main.py`
- 收录清单按 **operation_id** 而非路径（写 `/v1/*` 无效，必须逐个 operation_id）
- MCP 网关是 **fail-open**：新端点默认进工具列表，必须显式排除

顺带判断：**能不能连这个文件都不改**（把逻辑上移到新包里，往往能消除回归风险面）。

### 3. mockup / 设计稿 vs spec 决策一致性

mockup 是"画图时顺手加的"，常与已拍板决策冲突。逐页签比对：

| 检查点 | 典型冲突 |
|---|---|
| 决策表里明确否掉的选项 | mockup 里还留着（如「无 tier 兜底」vs mockup 的 tier:4 行） |
| Out of Scope 里写的功能 | mockup 里还画着按钮（如「日志导出」不做出按钮还在） |
| 底部技术说明注 | 写着已被推翻的数据流（如「复用池统计」） |
| 表格列 / 详情字段 | mockup 要的字段 spec 的字段表没定义 |

**冲突时以 spec 的拍板为准改 mockup**（spec 是用户拍过的），除非用户另有指示。

### 4. 引用路径是否真实存在

spec / design 里引用的 `.md`、`.html` 路径逐个 `ls` 验证。常见：文档后来搬了目录，
或当初写 spec 时引用了一个从未创建的文件。

另外注意：**富规格（1:1 mockup）若放在会被清理的目录**（如 `temp/`），要提醒归档。

### 5. 验收命令真跑一遍（不要只写不跑）

这是最容易造假的一环。三类常见不可用：

| 现象 | 根因 | 解法 |
|---|---|---|
| 全量 `pytest tests/` 挂死 20+ 分钟后崩溃 | 含 gpu/browser/real_backend/network 层，无环境时卡死 | 用 marker 过滤的直连 pytest |
| `run_all.py --quick` 报 `0 passed 0 failed` | 内部带 `-n auto`，受限环境 xdist worker 全 `node down` | `-p no:xdist` 或直连 pytest |
| 结果文件里没有汇总行 | atexit 清理被删防拦截 → SystemExit（**结果本身是对的，只是汇总丢了**） | **加 `--junit-xml=<path>`**，XML 在退出前落盘 |

跑完用 XML 取精确数字，别靠 grep 终端输出：

```python
import xml.etree.ElementTree as ET
s = ET.parse(path).getroot()
s = s.find('testsuite') or s
print(s.get('tests'), s.get('failures'), s.get('skipped'))
```

### 6. 基线冻结（判据要可执行）

- **收集总数**、**通过数**、**失败名字集合**、**skipped 数** 四项一起钉
- 基线往往**不是全绿**。若判据写 `failed = 0`，基线有存量失败就永远不绿，
  等于逼实现者「去修别人的存量失败」或造假 → 改为 **失败集合冻结**（允许基线失败，不允许新名字）
- 存量失败要**独立复跑**证明与本次改动无关（stash 对照是最硬的证据）
- 写明「若开工前仓库又发生 pull，作废重跑」

## 产出格式

```
## 结论：齐备 / 不齐备
### 阻塞项（不修会返工，逐条给「原假设 → 实测 → 修正方向」）
### 中等问题（建议一并修）
### 已核验属实（可放心依赖）——让用户可以只审这一节就快速相信其余部分
```

每条都要带**文件路径 + 行号**证据。用户若要求「顺手修」，修完把修正以「勘误 + 日期」形式
写回 spec 原文（保留原表述 + 标注为什么改），不要默默改掉——改后要能追溯当初怎么想的。

## 本机（Parcae）已知环境坑

- `data/*` 被 .gitignore 忽略 → 存 key/密钥/SQLite 不会进 git，安全
- `import server.main` 的测试（如 smoke）在沙箱 shell 必崩：`screen/session/manager.py` access violation，需桌面会话
- 后台 bash 任务在会话结束后可能丢失 → 长任务把结果**写文件**，下轮直接读文件

## 开工后别忘了

- 每个 ticket 完结更新 `tickets.md` 状态标记（☐/🔄/✅/⛔）
- CHANGELOG `[Unreleased]/Added` 加条目（项目惯例是超详细中文条目，含"关键设计修正"和验证方式）
- 收尾把 mockup 从 `temp/` 归档
