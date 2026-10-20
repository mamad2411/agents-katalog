---
name: param-refactor-semantic-audit
description: >
  参数统一改造/签名变更时的逐点语义审查规范。当用户要给某函数"统一加参数"、
  "全链路透传新参数"、"批量改造调用点"、"统一函数签名"、"重构传参方式"、
  "把 X 参数加到所有调用"、"锁/状态/run_id/user_id/tenant_id 透传"、
  "机械批量 sed 改造"、review 批量参数改造 PR、或发现"加了参数后某处功能失效/
  跳过逻辑不生效/检查被绕过"时使用。核心教训：同一个函数的不同调用点可能依赖
  不同的语义（查任意 vs 查特定、全局 vs 隔离），批量加参数时会误伤语义不同的
  调用点。触发词：统一加参数、批量改造调用点、全链路透传、run_id 隔离、
  tenant_id 透传、签名统一、参数对齐、机械改造、sed 批量替换、跳过检查失效、
  检查被绕过、回归引入、参数语义漂移。
---

# 参数统一改造逐点语义审查

## 核心教训

**同一个函数的不同调用点，可能依赖截然不同的语义。批量给所有调用点加参数时，
会无声地改变其中某些调用点的语义，导致检查逻辑失效、跳过逻辑被绕过等回归。**

典型场景：为做"隔离/互斥"给某函数加 `run_id`/`tenant_id`/`user_id`/`request_id`
参数。这个改动对"读写自己资源"的调用点是对的，但对"检查是否有其他资源在占用"
的调用点是致命的——加上 ID 后，检查从"查任意资源"变成"查我自己"，永远查不到
别人，检查彻底失效。

## 何时触发本 skill

- 给某函数统一加新参数（`run_id`/`tenant_id`/`user_id`/`trace_id` 等）
- 全链路透传一个新标识符
- 重构传参方式（位置参数改关键字、合并参数、拆分函数签名）
- 批量 sed/正则替换调用点
- review 一个"统一改造"性质的 PR/commit
- 线上发现"跳过/去重/互斥检查突然失效"，且近期有参数改造 commit

## 改造前的强制审查清单

### 1. 枚举所有调用点，不要只看"主要调用"

```bash
# 用 -S 找出引入/修改该函数签名的 commit
git log --oneline --all -S "目标函数名(旧签名)" -- 文件路径
git log --oneline --all -S "目标函数名(新签名)" -- 文件路径

# 列出当前所有调用点
grep -rn "目标函数名(" src/ --include="*.py" | grep -v venv | grep -v test
```

**铁律：调用点数量 ≠ 改动点数量。** 一个函数被调 5 次，commit 只 diff 了 5 次
加参数，但如果其中有 1 次的语义和别人不同，就是 1 个 bug。

### 2. 对每个调用点逐一问：这个调用依赖什么语义？

对每个调用点，问自己三个问题：

| 问题 | 答案 A（加 ID 正确） | 答案 B（加 ID 致命） |
|------|---------------------|---------------------|
| 这个调用是"操作自己"还是"检查别人"？ | 操作自己（读写自己的资源数据） | 检查别人（判断是否有其他实例在运行） |
| 加 ID 后，查询范围变窄了吗？ | 变窄是对的（只看自己） | 变窄是错的（应该看所有） |
| 如果 ID 对应的记录不存在，返回 None 合理吗？ | 合理（自己还没写） | 不合理（说明没有别人在跑，应该放行；但加 ID 后变成"查自己没查到→放行"，逻辑反转） |

**答案 B 的调用点，绝不能加 ID 参数。** 必须改用"查任意"的函数（如
`get_latest_*`/`scan_*`/不带 ID 的重载）。

### 3. 识别"语义对立"的调用对

同一函数的调用点里，如果同时存在这两类，就是高危信号：

- **"自查类"**：读自己实例的最终进度、写自己实例的状态、获取自己的锁
- **"他查类"**：检查资源是否被占用、判断是否有重复任务、去重检查

这两类对"是否带 ID"的需求是**相反的**。批量改造时必须分开处理：
- 自查类 → 加 ID（带 `get_state(task_id, run_id, resource)`）
- 他查类 → 不加 ID 或用 scan 版（带 `get_latest_state(task_id, resource)`，再
  `if existing.run_id != run_id` 排除自身）

### 4. 检查"防御性 guard"是否需要同步加

如果改造引入了新的"自身资源"概念（如本次 run），且存在"查任意资源"的调用，
必须加自排除 guard，避免误判自己：

```python
# 错误：查任意实例，但自己刚启动的实例也会被当成"已在运行"
existing = get_latest_state(task_id, resource)
if existing and existing.status == "running":
    return  # 自己查到自己 → 永远跳过 → 死锁

# 正确：查任意实例，但排除自己
existing = get_latest_state(task_id, resource)
if (
    existing
    and existing.status == "running"
    and existing.run_id != run_id  # 排除自身
):
    return
```

## 真实案例：参数隔离改造导致的跳过检查失效

### 背景

某项目的资源锁模块，`get_state(task_id, resource)` 原本查"该 task+resource 任意实例的状态"。
一次改造做"锁 value 加 run_id 隔离"，给函数加了 `run_id` 参数，变成
`get_state(task_id, run_id, resource)`，并机械地把全链路 4 处调用都加上了 `run_id`。

### 回归点

其中 3 处加 `run_id` 是对的（读自己实例的最终进度），**唯独"资源是否已在运行"的
跳过检查那处加 `run_id` 是致命的**：

```python
# 改造前（正确）
existing = get_state(task_id, resource)
if existing and existing.status == "running":
    return  # 跳过：查任意实例，发现别的实例在跑

# 改造后（回归）
existing = get_state(task_id, run_id, resource)
if existing and existing.status == "running":
    return  # 失效：查自己这个新实例，永远查不到（还没写入），永不跳过
```

### 现象

定时任务在手动任务还没全部完成时触发，用新的 `run_id` 检查"资源是否在运行"，
查自己的新 run → 查不到 → 不跳过 → 启动全新 run 重做 → 前端数据按最新 run 显示，
被重置，用户感知为"数据被清零重做"。

### 定位方法

```bash
# 1. 找引入 run_id 参数的 commit
git log --oneline --all -S "get_state(task_id, run_id, resource)" -- src/
# → abc1234

# 2. 看该 commit 对每个调用点的 diff
git show abc1234 -- src/ | grep -B2 -A2 "get_state"
# 发现 4 处调用都加了 run_id，但其中"跳过检查"那处的语义和其他 3 处不同
```

### 修复模式

跳过检查那处改用 `get_latest_state`（scan 所有 run_id）+ 自排除 guard：

```python
existing = get_latest_state(task_id, resource)  # 不带 run_id
if (
    existing
    and existing.status == "running"
    and existing.run_id != run_id  # 排除自身 run
):
    return  # 跳过：查任意实例，发现"别的"实例在跑
```

## 改造 commit 的自查模板

提交"统一加参数"类 commit 前，过一遍这个 checklist：

- [ ] 已枚举该函数所有调用点（`grep -rn`，不只看主调用）
- [ ] 对每个调用点确认：是"自查类"还是"他查类"
- [ ] "他查类"调用点没有盲目加 ID（改用 scan/不带 ID 的版本）
- [ ] "他查类"调用点加了自排除 guard（`!= run_id`）
- [ ] commit message 里**明确列出**哪些调用点加了 ID、哪些没加及原因
- [ ] 跑了涉及该函数的单元测试（`pytest -k 函数名`）

## commit message 规范

这类改造的 commit message 必须说明语义区分，避免 reviewer 误以为"统一加参数"
是无脑操作：

```
fix(模块): 函数 X 加 run_id 参数，区分自查与他查调用点

【改动】
- lock.py: get_state 加 run_id 参数（自查类，查特定实例）
- lock.py: 新增 get_latest_state（他查类，scan 任意实例）
- task.py: 3 处读最终进度调用加 run_id（自查，正确）
- task.py: 1 处跳过检查改用 get_latest_state（他查，不能加 run_id）

【原因】
跳过检查的语义是"查是否有其他实例在跑"，加 run_id 后变成"查自己是否在跑"，
永远查不到 → 跳过失效 → 定时任务与手动任务并发重复执行。
```

## 反面信号（看到这些要立刻警觉）

| 信号 | 含义 |
|------|------|
| commit 标题含"统一"/"全链路"/"批量" + 参数名 | 高概率有调用点被误伤 |
| diff 里同一函数 N 处调用，改动完全一致（机械 sed） | 没做逐点语义审查 |
| commit message 只说"加 X 参数做隔离"，没列调用点区分 | reviewer 无法判断语义 |
| 改造后某处"检查/跳过/去重"逻辑静默失效（不报错但行为变了） | 典型回归特征 |
| 函数有 `get_*` 和 `get_latest_*` 两个版本，但调用点只用了一个 | 可能用错了版本 |

## 与其他 skill 的衔接

- 发现回归后修复时，参考 `root-cause-no-patch`：定位根因而非加补丁掩盖
- 如果改造涉及数据库查询语义变化，参考 `mysql-expert` 检查索引和查询计划
- 涉及 commit message，用 `chinese-commit-messages`