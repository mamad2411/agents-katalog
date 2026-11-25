---
name: gamedev-factory
description: Yomi 游戏工厂流水线：多 agent 分工做游戏（策划/美术/试玩验收 subagent + 帧驱动 E2E + errors.md 经验闭环）。当立项新游戏、游戏进入量产/验收/收尾阶段，或要用 games/_factory 的引擎与骨架时使用。
---

# Gamedev Factory

原则：产出者不验收；v1 一周可发布；失败经验就近存放在 errors.md。

角色模板在 `~/.yomi/agents/`（game-designer / game-artist / game-playtester），用 agent 工具的 template 参数起。重活拆 subagent 并行，验收必须独立。
派活心跳：subagent 出发 30 分钟后检查一次产出迹象（文件/汇报），没有就 post_message 询问，无响应立即人工接管——静默烂尾是最贵的失败模式。

## 阶段与完成判据

### 1. 立项 → game-designer
- 产出：GDD（概念/MDA 三段/范围线/数据表字段）
- 判据：GDD 写明 v1 发布线；品类含内容边际成本评估（规则/文字/物理类 ≈ 0 优先，卡牌/RPG 勿入）

### 2. 技术路线
- 二选一：直写 Phaser TS（小品，默认）｜_factory 引擎 + skeleton（有匹配骨架时）
- 判据：选 skeleton 时记录 skeleton-catalog 的 when-not-to-use 排除理由；骨架的 errors.md 已通读

### 3. 原型（机制先行，美术占位）
- 判据：核心循环可玩；E2E 帧驱动全绿（fc.step，零墙钟等待）

### 4. 量产（并行）
- 内容：数据表进 src/data/；美术：game-artist subagent（imagegen 管线）
- 判据：资产 REPORT.md 在案、风格统一过目检；emoji/SVG 回退可发布，美术不阻塞

### 5. 验收 → game-playtester
- 判据：blocker 清零 + E2E 全绿；手感类只记录现象，签字权归主人

### 6. 收尾（evolve 回写）
- 判据全部满足才算完：
  - 项目根 errors.md 收录本轮新坑（症状→原因→修复）
  - 坑属骨架通病 → 回写 games/_factory/skeletons/&lt;slug&gt;/errors.md；属通用工程 → memory/lesson.md
  - NOW.md 对应行关闭（写 worklog 后移除）

## 模板资产

| 用途 | 位置 |
|------|------|
| 引擎/骨架/模块/schema | `games/_factory/`（上游 tettethu/VibeGame，Apache 2.0） |
| 帧控制器（直写 Phaser 用） | `src/core/framecontrol.ts`（移植范例见 games/ghost-fishing） |
| E2E harness 骨架 | `e2e/harness.mjs`（范例见 games/ghost-fishing/e2e） |
| 引擎/组件/设计理论文档 | gamedev skill references/vibegame/ |
| 美术量产 | imagegen skill + game-artist 角色 |
