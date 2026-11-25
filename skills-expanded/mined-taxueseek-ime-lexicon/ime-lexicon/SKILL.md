---
name: ime-lexicon
description: |
  豆包 / 微信输入法个人词库：识别、导出、导入、备份；纠错优化；
  搜索并生成行业/专业/定制词库（并入归档 industry-dict）。
  不走官方导入页。搜索优先 argo，没有就走通用搜索兜底。本技能只出查询、抽词、改表、写回副本。
  生态定位：直接操作豆包 / 微信输入法词库文件层（usr.dat / WeType LevelDB）的 agent skill，
  文件层识别、批量导出、槽位感知注入、整表替换消错、行业词库造词后直接 apply；
  格式互转工具和语音输入插件都不做词库管理。
  触发：个人词库、词库导出、词库导入、反向注入、行业词库、专业词库、定制词库、
  生成行业词库、做词库、行业术语、industry-dict、拼写纠正、豆包词库、
  微信输入法词库、WeType、usr.dat、ime-lexicon、/ime-lexicon
---

# ime-lexicon

主技能管合同和写回。归档的 `industry-dict` 整块在 build 子技能里，不单独恢复顶层。

| 干什么 | 读哪个 |
| --- | --- |
| 搜行业术语、造行业/专业/定制词库 | `sub-skills/build/SKILL.md`（原 industry-dict） |
| 合并、明显拼写/拼音更正、剔噪声 | `sub-skills/optimize/SKILL.md` |
| 素材库 ↔ 创作词库 ↔ 画像 | `sub-skills/bridge/SKILL.md` |
| 导入导出、备份、apply | 本文件 |

不要再写一套爬虫。有 argo 技能/CLI 就用 argo；没有就用宿主通用搜索（web_search / ddgs）。不要把 industry-dict 拆成第三个顶层技能。

## 命令

脚本：`$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py`

```bash
python3 .../ime_lexicon.py detect
python3 .../ime_lexicon.py export --engine all
python3 .../ime_lexicon.py backup
python3 .../ime_lexicon.py search --topic 锂电池
python3 .../ime_lexicon.py search --topic 锂电池 --run --out /tmp/术语.txt
python3 .../ime_lexicon.py search --topic 锂电池 --engine generic --run
python3 .../ime_lexicon.py build --topic 锂电池 --from /tmp/术语.txt --term 材料:磷酸铁锂
python3 .../ime_lexicon.py build --topic 投资理财 --seed thuocl:财经 --out 行业词库_投资理财.tsv
python3 .../ime_lexicon.py optimize --from a.tsv --from b.tsv --profile personal --out DIR
python3 .../ime_lexicon.py optimize --from 行业.tsv --profile industry --budget <剩余槽> --out DIR
python3 .../ime_lexicon.py harvest
python3 .../ime_lexicon.py harvest --speech
python3 .../ime_lexicon.py harvest --sessions
python3 .../ime_lexicon.py guide --topic 投资理财
python3 .../ime_lexicon.py acquire --topic 投资理财
python3 .../ime_lexicon.py import --engine doubao --from 词表.tsv --budget <剩余槽>
python3 .../ime_lexicon.py import --engine doubao --from 优化表.tsv --replace --staging /tmp/ime-lexicon-staging/doubao_XXX
python3 .../ime_lexicon.py apply  --engine doubao --staging /tmp/ime-lexicon-staging/doubao_XXX
python3 .../ime_lexicon.py dedup                      # 豆包重复槽一键去重（原位裁剪，默认只到 staging）
python3 .../ime_lexicon.py dedup --apply              # 输入法已退出时直接写入 live
```

中间表：`word \t pinyin \t freq \t source \t syll \t note`

## 纪律

1. **先拷后读后写。** 不改正在用的 `.dat` / LevelDB。
2. **import 只写 staging。** apply 才覆盖 live，输入法必须已退出。
3. **apply 先备份。**
4. **豆包禁止手改密文 hex。** 只走 rebuild。
5. **不要灌细胞词库。** 豆包个人库槽数随版本变（5000→7500→10000；一条词一槽，不是字数），**槽数/已用/剩余以 `detect` 实读 header 为准，不要背数字**。系统词、短语库、侧车另算。先小批量。第三方全量词库（含 THUOCL 全量）都当细胞源，不作 apply 源。
6. **分层。** 核心必须有拼音；多音进扩展；无拼音进大词库，**禁止 apply**。
7. **写豆包先裁预算。** `--budget N`：个人库先锁，重复键留个人那条，剩余按频次补。
8. 输出里不要贴账号哈希、token、绝对用户名路径。
9. 搜索：有 argo 用 argo，没有用通用搜索。`search` 默认只打计划；`--run` 才真搜（argo 抽到 0 词再降 ddgs）。
10. 公开研究副本在 `微信输入法词库/研究/`，只读对照，不整包写回。
11. **创作打通走 harvest/guide/acquire，不 apply。** harvest 用去 AI 味筛子抽金句/洞见；`--speech` 走语音转写/纠错；`--sessions` 联动 session-digger 的会话索引（只读 `SESSION_DIGGER_DATA_DIR`/`~/.claude/.session-digger` 的 USER 正文，中文走同一套质量闸，技术词要跨会话广度），产 450 条候选短名单；guide 出用词包；acquire 按画像缺口出搜索计划（`--run` 才搜，不覆盖行业表）。四者都不写 usr.dat / WeType，候选表过目后再 optimize/import。
12. **消错替换用 `import --replace`。** 默认 import 是并入 live（保留旧词）；`--replace` 让优化表整表替换，剔除 optimize 已改写/删除的旧词（如错误 agnet、噪声词）。流程：`export` 全量 → `optimize` 修正 → `import --replace` → `apply`（输入法退出）。`--replace` 后无拼音词仍禁止 apply。
13. **重复槽体检用 `dedup`，不用 import --replace。** 豆包引擎重学/同步会按次追加新槽（重复率会持续回涨，实测账号同步在登录时每轮重同步都会追加副本）。`dedup` 走原位裁剪：保留词条字节与槽位不动、只清零重复槽，对引擎扰动最小；整表 rebuild 只留给需要改词内容的 import 流程。detect 的 `doubao_dup_slots` 超 15% 就跑一次。

## 代理步骤

1. `detect`，报两边是否在跑、已用槽。
2. 导出 / 备份 → 只回条数和相对路径。
3. 造行业词 → 读 build，先 `search` 再 `build`；纠错合并 → 读 optimize。
4. 注入先 import 到 staging，回读条数，**问一句要不要 apply**。
5. 未确认或 IME 仍在跑 → 不准 apply。

细节：`references/formats.md`。
