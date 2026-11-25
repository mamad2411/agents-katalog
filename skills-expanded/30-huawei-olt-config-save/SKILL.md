---
name: 30-huawei-olt-config-save
description: 区分 commit、手动 save 与 autosave interval；默认都不自动做，仅用户明确选择时执行。
---

# 华为 OLT 配置保存（PERSIST · 可选）

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507；全局 `save` 语法本库标为 `[DISCOVERY]` / `[版本不同]`，须本机 `?` 确认后再执行。

## 目标

把「改配生效」与「落盘」完全拆开：**默认不 save**；仅当用户明确要求持久化时，再走 PERSIST 门禁。

## 默认策略（强制）

- **任何 WRITE / 开通 / 删户 / 回滚之后，都不要自动执行 `save`。**
- `save` 是**可选、按需、由用户选择**的步骤，不是变更流程的固定尾声。
- Agent 在变更结束时应：**汇报运行态结果**，并**询问**用户是否需要现在落盘；未得到明确「要 save / 授权 PERSIST」前保持不落盘。
- 用户也可以选择：本窗口不 save、稍后统一 save、或仅在验收通过后再 save。

## 何时使用本 Skill

仅当用户（或任务）**明确**要求：全局保存、落盘、防重启丢失、或排查「重启后丢配」。不要在普通开通/排障流程里主动插入 save。

## 前置条件（仅在用户选择 save 时）

- 显式 **PERSIST** 授权（WRITE ≠ PERSIST；「改完了」≠「请保存」）
- 用户已确认要落盘的当前运行态（通常建议先验收，但是否验收由用户决定）
- 变更前文本备份建议已完成（`network-config-backup`）
- 本机已用 `?` 确认 `save` 提示与确认交互

## `commit` ≠ `save` ≠ `autosave`

| 动作 | 典型场景 | 作用 | 类别 | 是否默认做 |
|------|----------|------|------|------------|
| `commit` | line/srv profile 等子视图末尾 | 对象进入运行态 | WRITE（对象级） | 按该对象流程需要 |
| 全局 `save` | 特权/系统视图 | **立即**整机落盘一次 | **PERSIST** | **否，仅用户选择时** |
| `autosave interval …` | `(config)#` 全局 | 按间隔**后台**自动落盘策略 | WRITE / 策略级 PERSIST | **否，仅用户明确要求开/关/改间隔时** |

- 只做了 `commit` **不能**假定重启后仍在——留给用户决定是否手动 `save` 或依赖已开启的 autosave。
- **开启 autosave ≠ 代替询问用户是否现在 `save`**；也 **≠** 允许 Agent 在每次改配后手动 `save`。
- 多次改配可以只在用户选定的一次窗口末尾统一手动 `save`；或依赖局方已批准的 autosave 策略。

## 已确认命令

- [已确认] profile 上下文中的 `commit`（见 line/service profile 等 Skill；仅对象级）
- [已确认] 变更前后用 `display` 验收（不替代、也不触发 save / autosave）

## 发现类命令 — 手动落盘（仅用户选择「现在 save」后）

- [DISCOVERY][破坏性][PERSIST] `save`（常见确认：`Are you sure... (y/n)` → 仅在授权后回 `y`）
- [DISCOVERY] `save ?` / 本 release 参数与提示
- [DISCOVERY] 保存后抽样核对（脱敏；勿把完整含密配置写入公开仓库）

## 发现类命令 — 全局自动保存开关（仅用户明确要求时）

在 `(config)#`（或本机等价全局配置视图）先 `autosave ?` / `autosave interval ?` 再操作。下列为 SmartAX 常见形式，**本库未做 R018 实机确认**，一律 `[DISCOVERY]` / `[版本不同]`。

| 命令 | 含义 |
|------|------|
| `autosave interval on` | 打开**按间隔**自动保存总开关 |
| `autosave interval off` | 关闭按间隔自动保存 |
| `autosave interval <分钟>` | 无条件按间隔落盘（常见范围约 10–10080 分钟；文档默认常为 1440≈1 天） |
| `autosave interval configuration [<分钟>]` | 仅当配置有变更时按间隔落盘（文档默认间隔常为 30 分钟；以本机为准） |
| `autosave type { configuration \| data \| all }` | 自动保存对象类型（配置文件 / 数据库 / 二者；本机 `?`） |
| `autosave time on` / `autosave time off` | **定点**自动保存开关；与「按间隔」通常**互斥**，勿同时启用 |

查询/复核（DISCOVERY，以本机为准）：

- 执行 `autosave interval on` 成功时设备常回显当前 switch / interval / type——保留原文作证据
- 或本机 `display`/`autosave` 相关只读查询（先 `?`，勿臆造命令名）

策略建议（运维口径，非强制命令）：

- 过短间隔会加重设备负担；业界常建议间隔 **≥ 60 分钟**，更稳妥按 **天级** 规划
- 开/关 autosave 是**全局策略变更**：须用户明确选择 + WRITE/策略授权；改完后是否再手动 `save` 一次固化该策略，仍由用户选择
- Agent **不得**为「方便」擅自 `autosave interval on`

## 推荐对话顺序（Agent）

```text
1. 完成 WRITE（含必要 commit）与 display 复核
2. 向用户说明：当前变更在运行态；重启前若不落盘可能丢失
3. 询问（可多选，默认全否）：
   a) 现在手动 save 一次？
   b) 查看/调整全局 autosave interval 开关与间隔？
4. 仅对用户明确勾选的项，在授权后执行
5. 若用户都选否：结束变更，记录「未手动持久化；autosave 未改」
```

中止：用户未选择落盘/改 autosave、意外提示、权限拒绝、保存失败 → **不要重试变体 save/autosave**。

## 与其他 Skill

- 变更规划：`16-huawei-olt-safe-change`（默认不落盘、不改 autosave）
- 回滚：`17-huawei-olt-rollback`（回滚后同样不自动 save）
- 生产验收：`19-huawei-olt-production-checklist`（验收通过 ≠ 必须 save / 开 autosave）
- 文本备份：`network-config-backup`（采集 ≠ 设备侧 save / autosave）

## 风险

- **错误地每次操作后 save**：把中间错误状态固化——禁止
- **擅自打开 autosave**：未评估间隔/互斥/双主控影响——禁止
- 过短 `autosave interval`：性能与 flash 磨损风险
- `autosave time` 与 `autosave interval` 冲突导致配置被拒或行为不符合预期
- 用户选择不 save 且 autosave 为 off：重启可能丢运行态——结束时提醒一次即可，勿强迫
- 误确认 y / 错误视图执行 save
- 把完整配置（含密钥）贴进工单或 Git

## 安全规则

优先 `display` / `?`；`commit`、`save`、`autosave` 分级；**手动 save 与 autosave 默认都不做**；不记录凭据；以本 OLT CLI 为权威。

## 禁止事项

- **禁止**在每条改配、每个 Skill、每次开户/删户后自动 `save`
- **禁止**未经用户明确要求执行 `autosave interval on` 或改间隔
- **禁止**把「变更完成」写成隐含的「已保存」或「已开自动保存」
- **禁止**在用户未明确选择时建议「必须马上 save / 必须开 autosave」
- 不得在 profile 里把 `commit` 写成「已全局保存」
- 不得把 API「改配后 save」理解成「每次改配都要 save」或「应默认开 autosave」

## 来源

- ACCESS-GUARDRAILS：`PERSIST` 为独立层级，不是 WRITE 的附带动作
- SmartAX 公开运维材料中的 `autosave interval on|off` / interval / configuration / type（跨系列，标 `[版本不同]`）
- 历史 API「改配后确认再 save」= 可选确认，不是强制尾步
- 一手：MA5800V100R018/SPH507 上已确认的 profile `commit`；`save` / `autosave*` 待本机 DISCOVERY
- 设备 CLI 优先于文档
