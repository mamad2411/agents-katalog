---
name: alice-migrate
description: 技能包迁移/路径修复（技能已就位 → agent 探测真实 skills 根 → 刷新生成物内嵌路径 → 只读检查全局路由 → 自检 → 询问用户是否注入；不拷贝文件）。触发词：迁移/换电脑/新机器/搬技能包/路径修复/部署技能包/alice迁移自检
x-alice-class: assist
---

# Alice 技能包迁移（路径自适应 · 不拷贝）

> 核心认知：**用户已自行把技能放进客户端的 skills 目录**（codex / pi / workbuddy / dsh / omp 均可能）。
> 迁移 = agent 找到真实 skills 根，把**生成物里内嵌的旧机绝对路径**刷成本机路径，并只读检查全局路由是否对齐。
> **禁止拷贝/搬动用户的技能文件**；仅当目标 skills 缺 alice 组件（见步骤 2 检查）才回退到「补拷缺失项」。
> **迁移自检不得写入、替换或创建任何全局提示词路由块**；自检完成后必须先询问用户是否注入。

铁律：每步报真实输出；失败即停并给修复命令；未执行写「未执行」；严禁虚构结果。全程向用户汇报「当前进度：N%」。

## 前置检查

1. Python 可用性：`python --version`，失败再试 `py -3 --version`。都失败 → 报错引导装 Python 3。
2. **定位真实 skills 根**（本模块 `SKILL.md` 所在包的上级目录就是根之一；用它校验）：
   - 候选探测链：`%USERPROFILE%\.codex\skills`、`%USERPROFILE%\.pi\agent\skills`、`%USERPROFILE%\.dsh\skills`、`%USERPROFILE%\.omp\agent\skills`、客户端自定义目录（如 workbuddy 数据目录下的 `.codex\skills`）。
   - **判定标准**（同时满足）：① 含 `_modules\zh_desc.json`；② 含 `aliceskill\scripts\rebuild_menu.py`；③ 6 个路由目录 `alice-crack/reverse/pentest/game/ai/assist` 各有 `SKILL.md`。
   - 命中多个根 → 按 AGENTS.md 路由块指向的根优先，其次问用户一句。
   - 全不命中 → 问用户一句客户端 skills 根路径，拿到后回到判定标准校验。
3. 记 `$R = 真实 skills 根`（后续全部用 `$R`，不写死任何盘符/用户名）。

## 步骤 1：残留路径体检

```powershell
# 找出仍指向旧机/打包机的绝对路径（排除本机正确路径）
Get-ChildItem "$R" -Recurse -Include *.md,*.json -File |
  Select-String -Pattern '[A-Z]:\\\\' -List | Select-Object -ExpandProperty Path -Unique
```

- `skills_data.json` 的 `skills_root`/`modules_root` 与 `$R` 不一致 → 必须跑步骤 2。
- 6 个路由页 `SKILL.md` 的「绝对路径兜底」行含别的盘符/用户名 → 必须跑步骤 2。
- 全部已是本机路径 → 跳到步骤 3。

## 步骤 2：重跑生成器刷路径（唯一需要的"迁移动作"）

```powershell
python "$R\aliceskill\scripts\rebuild_menu.py"
```

- 作用：扫描 `$R\_modules` 重写 6 个路由页（内嵌绝对路径自动变为 `$R`）+ 刷新 `aliceskill\scripts\skills_data.json` 的 `skills_root`/`modules_root`。
- 显式指定根（多客户端/环境变量不可用时）：
  ```powershell
  $env:CODEX_HOME = <R 的上一级>   # rebuild_menu 取 <CODEX_HOME>\skills
  python "$R\aliceskill\scripts\rebuild_menu.py"
  ```
- 跑完抽查：任一路由页（如 `alice-assist\SKILL.md`）「绝对路径兜底」行 = `$R\_modules/...`；`skills_data.json` 的 `skills_root` = `$R`。不对 → 停并报真实输出。

## 步骤 3：全局路由只读检查（禁止注入）

只读检查客户端实际读取的全局提示词（按客户端判断位置：codex `~\.codex\AGENTS.md`；pi `~\.pi\agent\AGENTS.md`；workbuddy/dsh/omp 同理找其 AGENTS/系统指令文件；不确定就问用户该客户端读哪个）。

本步只记录「本地技能路由」块是否存在、是否指向 `$R`、哪些行需要更新。**不备份、不写入、不替换、不新建全局提示词文件。**

「本地技能路由」块的只读对照基线：
- 路径行指向 `$R` 下六个路由技能（卡密授权/逆向分析/web安全/游戏攻防/AI安全测试/技能指令）。
- 路由块含“类 → 一个领域索引 → 一个初始模块”的渐进读取规则、明确跨领域最多两个索引、每阶段最多四个模块，以及“任务匹配度 → 评分 → 索引顺序”。
- 指向旧包路径（如 `l-license`、`skills/alice/`）或别的机器路径 → 记录为「待注入更新」，不在自检阶段替换。
- 对照基线如下（仅用于比较）：

```text
- 卡密授权 / 激活 / 授权验证 / 本地授权分析 → $R/alice-crack/SKILL.md
- 逆向分析 / Hook / PE / APK / EXE / DLL / 协议 → $R/alice-reverse/SKILL.md
- web安全 / Web 与 API 安全验证、给定 URL → $R/alice-pentest/SKILL.md
- 游戏攻防 / 游戏覆盖层 / 内存 / 模拟器 / 自动化演示 → $R/alice-game/SKILL.md
- AI安全测试 / LLM / 提示注入 / MCP 与 RAG → $R/alice-ai/SKILL.md
- 技能指令 / 元技能 / 技能包维护（含本迁移模块） → $R/alice-assist/SKILL.md
```

（`$R` 替换为真实根，写绝对路径。）

## 步骤 4：自检链收尾

```powershell
python "$R\aliceskill\scripts\alice_router.py" selfcheck     # 期望 6/6
python "$R\aliceskill\scripts\alice_contract.py" selfcheck   # 期望 5/5
python "$R\aliceskill\scripts\check_auth_policy.py"          # 期望 9/9
python "$R\aliceskill\scripts\rebuild_menu.py" --audit
```

全部通过 → 报「迁移自检完成」+ 摘要（真实根 $R、模块数、六类计数、残留路径状态、全局路由差异、自检结果）。

然后必须询问用户：

> 迁移自检已完成，是否将 Alice 本地技能路由注入当前客户端的全局提示词？

只有用户明确同意后，才读 `../alice-inject/SKILL.md`，按 `--check` → `--dry-run` → 注入的顺序执行。未回复、超时或含糊表达都不算同意。

## 回退：目标缺组件时才补拷

仅当步骤前置检查 ②③ 失败（包不完整）：从用户给的源包把**缺失项**补拷进 `$R`（八件套：`aliceskill`、六路由、`_modules`；已存在的跳过不覆盖），然后从步骤 1 重新走。完整包已就位时禁止任何拷贝。
