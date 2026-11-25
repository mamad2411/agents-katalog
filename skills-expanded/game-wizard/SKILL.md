---
name: game-wizard
description: "游戏开发一条龙向导 从零做游戏 小白新手 2048 贪吃蛇 打砖块 模板 init qa 验证 GIF Web 试玩 分享 —— 当用户说「做个游戏/我是新手/不知道从哪开始/帮我做一个能玩的游戏」或想要从想法到可分享游戏的完整引导时使用"
---

# 游戏一条龙向导(game_wizard)

把「想法 → 可玩 → 验证 → 可分享」串成阶段机,**每阶段有硬性 gate**——不问「文档写了吗」,问「游戏跑通了吗」。全程可以不打开 Godot 编辑器。

**何时不适用**:3D 大型项目/多人协作管线(本向导面向个人小游戏的第一次成功交付)。

## 第 0 步:四档分诊(先问一句,不要跳过)

| 档 | 用户画像 | 入口 |
|---|---|---|
| **A 没想法** | 「随便,好玩就行」 | 展示三模板一句话介绍(见下),让用户挑一个 + 说一个想改的点 |
| **B 模糊** | 「想做个消除类的/像贪吃蛇那样的」 | 问 2-3 个澄清:①玩法像哪个模板?②想要更快/更难/更大棋盘?③想改什么(速度/数值/规则)?→ 映射模板+调参方向 |
| **C 清晰** | 「做一个 2048,棋盘 5×5,出 4 概率高一点」 | 直接进 S1,需求映射到 GDD+调参表 |
| **D 已有项目** | 「我有个 Godot 项目想加点东西」 | 跳过 S1/S2 的模板部分,从 `setup_project_rules` 开始接手;验证/分享阶段(S3+)同款适用 |

三模板(选型即终局,别过度发散):
- **2048**(`2048`)——数字滑块合并,手脑放松,调参面:棋盘/胜利值/出 2 概率
- **贪吃蛇**(`snake`)——节奏紧张,调参面:速度/网格/穿墙
- **打砖块**(`breakout`)——手感控球,调参面:挡板宽/球速/砖墙/生命

## 阶段机(顺序执行,每阶段 gate 不过不进下一阶段)

### S0 环境(只在做不了时才做)
- Godot 未装 → `npx godot-mcp-enhanced install`(官方 releases 自动下载,零预装);
- 想最终网页试玩 → S4 时会自动装 export templates(~1GB,首次);
- gate:`npx godot-mcp-enhanced doctor` 输出 `✓ Godot found`。

### S1 造(一条命令出可玩 demo)
```bash
npx godot-mcp-enhanced init my-game --template=2048   # 或 snake / breakout
cd my-game
```
- gate:目录含 `main.tscn / design/gdd/<slug>.md / qa/<slug>.qa.md / tuning-src/<slug>.csv / tuning/<slug>.tres` 五件(缺一即失败重跑)。

### S2 改玩法(先 GDD 后代码,调参优先改表)
1. **读** `design/gdd/<slug>.md`(8 段设计文档)→ 与用户对齐要改的段(尤其 Detailed Rules / Tuning Knobs);
2. **改数值** → 编辑 `tuning-src/<slug>.csv` → 用 `csv_to_resources` 工具重导 `tuning/<slug>.tres` → 重启生效(**这是首选:零代码风险**);
3. **改规则** → 让 AI 改 `scripts/game.gd`(遵循 GDD 先更新),改完 `validate_scripts` 编译验证;
4. gate:改动后的 GDD 过 `validate_gdd` 零 error,且向导能复述「改了什么、预期玩家体验变化」。

### S3 验证(qa 硬门——本向导的灵魂)
```bash
npx godot-mcp-enhanced qa run qa/<slug>.qa.md --project .
```
- **gate:进程退出码 0(全 PASSED)才放行 S4**;非 0 → 读报告(`qa report latest`)逐条修,修完重跑;
- 玩法改动大时,同步改 qa 断言面(如改了棋盘大小,断言里的边界值要跟);
- 首跑冷启动可能超 bridge 15s 窗口(资源首次 import)——预热后重跑一次再判。

### S4 导出(浏览器可玩)
```bash
npx godot-mcp-enhanced web .          # 首次自动装 export templates(~1GB,确认后继续)
```
- gate:命令打印 `✓ 试玩地址: http://127.0.0.1:<port>/`,浏览器打开可玩。

### S5 分享(两件套)
```bash
npx godot-mcp-enhanced gif . --keys left,right    # 按游戏选键;2048/snake 用默认方向键
```
- 产物:`dist/demo.gif`(发群/发帖)+ S4 的试玩地址(本机试玩);Web 目录 `build/web/` 可自行部署到任意静态托管;
- 收尾清单:①qa 报告路径(证据)②GIF ③GDD(设计复盘素材)。

## 硬规则(向导纪律)

1. **qa 退出码是唯一 gate 真相**——不以「看起来能跑」「没报错」放行;
2. **改玩法顺序:GDD → 调参表 → 代码**,能改表不写码;
3. 每阶段结束向用户**复述当前状态与下一步**,小白不该猜进度;
4. 全程无需打开 Godot 编辑器(undo 兜底:若用户开了编辑器,editor 层操作全部 Ctrl+Z 可回)。

## 非 Claude Code 客户端

- 项目级安装:`npx godot-mcp-enhanced skills install --target <项目>/.claude/skills`(Cursor 等读项目级 skill 的客户端);
- 任意 MCP 客户端:本 skill 的阶段机是纯 CLI 命令序列,可直接按本文档执行;也可设 `GODOT_SKILL_LIBRARIES` 指向 npm 包内 `skills/` 目录供 `load_skill` 检索。

## 常见偏离

- 跳过 S3 直接导出 → 打回来:未验证的玩法不是「能玩」;
- 改 `tuning/*.tres` 手写数值 → 打回来:改 `tuning-src/*.csv` 再重导(手改 .tres 会被下次重导覆盖);
- 用户要加「一点小功能」导致跨档 → 保持四件套结构(新功能写进 GDD 的 Dependencies + qa 断言),不破坏模板纪律。
