---
name: civ6-ai-copilot
description: 读取 Civilization VI civ6-ai-copilot Mod 最后一次成功汇总的本地玩家可见战情。按清单选择模块，为发展、城市、科技、市政、政策、军事、海军、定居和多人公平问题提供建议。
version: 0.3.9
compatVersion: "0.3"
---

# civ6-ai-copilot

## 怎么使用

玩家点击「更新战情」并看到「简报已汇总」后，当前对局就是这一次导出。从本 Skill 目录调用，不要找仓库、不要选工作目录，也不要搜索历史 snapshot、handoff 或自己写解析脚本。

先看简报：

```bash
node scripts/context.mjs
```

需要看地时再要图，需要一座城或一个单位的明细时再展开。按问题选择图层、页码和实体明细，并核对 `exportId` 相同。

```bash
node scripts/context.mjs --map world
node scripts/context.mjs --map local:city:首都:5
node scripts/context.mjs --city 首都
node scripts/context.mjs --unit 开拓者
```

`--raw` 只把原始导出写到文件并返回路径，供排障。不要把该文件读进日常分析。

## 地图

铺城、移动、战线和局势先看图，再回答。不要自己写脚本把地块扫成文字。一次可以要多层。区域图默认半径 8，局部图默认 5，单次最大半径 20。半径是六边形距离，由你指定。

```bash
node scripts/context.mjs --map world
node scripts/context.mjs --map region:city:首都
node scripts/context.mjs --map local:unit:开拓者:5
node scripts/context.mjs --map local:coord:12,18:9 --map world
```

| 层级 | 用来判断 | 图上的重点 |
| --- | --- | --- |
| `world` | 世界位置、文明、城市、可见军队和资源 | 地形底色、山脉、河流、边界、文明色和全局编号 |
| `region` / `local` · `yields` | 产出、地貌、水源、资源 | 六项游戏产出图标和数值、资源图标、地块归属 |
| `region` / `local` · `operations` | 设施、区域、同格单位和战线 | 游戏设施图标、单位与所属文明、伤害和移动力 |

圆心写成 `city:名称或id`、`unit:名称或id`、`coord:x,y` 或 `selection`。半径接在最后，例如 `local:city:首都:3`。局部和区域请求同时返回产出、设施与单位两层。范围大时自动分页，按 `page` 和 `layer` 选择，格子大小保持可读，分页不削减请求范围。

打开 `mapViews[].image.path`（PNG）。PNG 和 `svgPath` 来自同一份图形。`places` 提供编号索引；`dataPath` 是该页精确数据，包含地块全部已知字段、所有同格单位、城市明细、玩家和图标来源。需要图中省略的单位、城市或数值时读相应 `dataPath`，核对其中 `identity` 与本次 `exportId`。不要把图上最多三个单位图标或有限侧栏当成全部数量。指定 `--map` 后默认不内联整份 `visibleMap`。

图例始终随图输出。P# 是玩家，C# 是城市，U# 是己方单位，V# 是可见外方单位。格顶徽记表示地块所属文明，单位角标表示单位所属文明，两者分别读取。玩家编号未能匹配公开身份时保持未知。

`0` 是已观测零值，`∅` 是已确认空，`?` 是未知。迷雾分为已有历史记录和仅知坐标两种；有历史记录时保留地形与产出，并用斜纹和 T# 标出上次观测回合。历史归属、设施和产出可能变化，不能直接当成本回合事实。未探索和缺测有不同底纹；旧版截断快照里的空缺不会推断成未探索。

Mod 只记住本次载入以后真正观测到的信息；刚加载时的迷雾可能只有坐标。回退回合或切换本地玩家会清空历史。旧快照不补造历史或零产出。

首次生成图时，工具只查询所需游戏类型的公开图标名称，下载后校验并缓存。`CIV6_COPILOT_OFFLINE=1` 禁用网络；`CIV6_COPILOT_ICON_CACHE` 可指定缓存目录。缺少图标时使用名称缩写，缺口写入结果。

坐标只用于核对。面向玩家用相对方向和可见锚点，例如「勇士右上方的盐」。邻接规则见 `references/snapshot-schema.md`。

## 结果

返回一份 JSON。

- `status=ready`：用 `brief` 回答。需要位置时看 `mapViews`，需要明细时看 `detail`。`identity.exportId` 必须和这几步一致。`gaps` 里的事项保持未知：未采集不能写成 0，城邦不可用不能写成安全，地图截断不能写成完整战场。`upgradeCost` 为 0 不是免费升级。不知道价格和许可时，不能断言购买更划算。文明特性和当前队列不是玩家已经选定的长期路线。
- `status=needs-game-refresh`：游戏里还没有写完的导出。把 `userActions` 告诉玩家，请其点击「更新战情」。不要用历史文件顶上。
- `status=runtime-error`：日志或 Tuner 读失败。按 `userActions` 排障。必要时再读 `references/mod-usage-guide.md`。

## 回答

沿用用户当前语言。中文使用文明 6 中文术语，英文使用英文术语。多人局、战争迷雾或信息限制实际影响结论时，用一句话说明本地玩家可见边界。不要要求玩家提供隐藏地图、不可见单位、未遇见文明或其他玩家的私人状态。

数据够用时直接给本回合可执行安排。按问题从「已确认、本回合优先级、建议、风险、仍需关注」里选用，不必每项都写。

## 安装

更新时只替换整个技能目录。分析程序在 `scripts/context-runtime.mjs`，和 `SKILL.md`、`assets/render/` 的 WASM 渲染器及中文字体一起分发。不要再用另一个旧工具目录里的校验器核对版本。安装细节见 `references/mod-usage-guide.md`。

`npm run copilot`、handoff 和 doctor 只用于排障和跨机流程，不是日常步骤。
