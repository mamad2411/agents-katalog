---
name: alice-absorb
description: 技能包吸收手册（AI 读 md 判类与领域、拟描述，脚本落库并刷新渐进路由）。触发词：吸收、新技能、加技能、入库、absorb。
x-alice-class: assist
x-alice-domain: routing-skill-engineering
---

# alice-absorb — 吸收新技能进 Alice 渐进模块库

> 角色分工：**AI 判类、判领域并拟描述，脚本机械落库**。脚本不做关键词猜测；缺类目或领域时拒绝执行（exit 2），避免模块落入错误分片。

## 流程（AI 主导）

1. 拿到新技能目录或 .zip → **AI 先完整读其 SKILL.md**（不许读一半就判）。
2. 按六类定义判类：
   - **卡密授权** crack：授权 / 卡密 / 激活 / 注册机 / VIP
   - **逆向分析** reverse：逆向 / 脱壳 / Hook / 取证
   - **web安全** pentest：Web / SQL / 端口 / 资产
   - **游戏攻防** game：内存 / ESP / 反作弊
   - **AI安全测试** ai：LLM / 提示注入 / MCP / RAG
   - **技能指令** assist：元技能 / 平台 / 工程化
   判不出 → 向用户问一句，不瞎猜。
3. 读取目标 `alice-<class>/SKILL.md` 的领域表，只选一个最匹配领域；明确跨领域也只记录主领域。可运行：
   ```bash
   python ".../aliceskill/scripts/absorb_skill.py" --list-domains <class>
   ```
   源 frontmatter 已有且合法的 `x-alice-domain` 可复用；显式 `--domain` 优先。
4. 拟 ≤40 字中文描述（越短越好但必须清楚，含触发词）。
5. 执行落库（目录或 zip 均可）：
   ```bash
   python ".../aliceskill/scripts/absorb_skill.py" <源> --class <crack|reverse|pentest|game|ai|assist> --domain <领域> --desc "<中文描述>"
   ```
   退出码含义：`0` 成功；`2` 类目、领域或描述无效 → 按输出引导补参重跑。
6. 重跑生成器：
   ```bash
   python ".../aliceskill/scripts/rebuild_menu.py"
   ```
7. 三自检：
   ```bash
   python ".../aliceskill/scripts/alice_router.py selfcheck"    # 6/6
   python ".../aliceskill/scripts/alice_contract.py selfcheck"  # 5/5
   python ".../aliceskill/scripts/check_auth_policy.py"         # 9/9
   ```
8. 打开 `skills/alice-<类>/references/<领域>.md` 确认新条目 `- <id>` 与中文描述出现；同时确认 `alice_manifest.json` 和 `skills_data.json` 已写入相同 domain。
9. 报「吸收完成」+ 类目 / 领域 / 描述 / 索引位置摘要。失败报真实输出并停。

## 进度汇报（硬性）

- 吸收全程向用户实时汇报，格式：`当前进度：N%｜已完成：…｜下一步：…`（按 9 步折算：读 md 11%、判类 22%、判领域 33%、拟描述 44%、落库 56%、重建 67%、三自检 78%、索引确认 89%、完成 100%）。
- 每完成一步立即汇报；失败或中断时输出最后真实百分比和具体错误，禁止静默结束。

## 规则

- 判类或领域拿不准就问用户，禁止瞎猜；脚本永不代替 AI 判类或判领域。
- `x-alice-class` 与 `x-alice-domain` 必须成对写入；领域必须属于所选类。
- `--desc` 给出即覆写 zh_desc 条目（AI 本次判断优先于旧占位）；必须含中文，否则 exit 2。
- 重建后的选择顺序仍为“任务匹配度 → 评分 → 索引顺序”；吸收新技能不会自动获得高评分，也不会因无评分而不可用。
- 沙箱演练用 `CODEX_HOME=<临时目录>`，产物全落临时库，主库零污染。
