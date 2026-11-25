---
name: ime-lexicon-bridge
description: |
  素材库 ↔ 创作词库 ↔ 画像：harvest 用去 AI 味筛子抽专属词，
  guide 出用词包，acquire 按画像缺口出搜索计划。只读，不 apply。
  触发：抽创作词、用词包、金句抽词、写之前看词、素材库词库打通、画像补词。
---

# bridge — 素材库 ↔ 创作词库 ↔ 画像

父技能：`ime-lexicon`。脚本：`scripts/bridge.py`（确定性，不调 LLM）。

素材库 = 你写过什么；词库 = 你会怎么写；画像 = 你该补哪块行业。
筛子反过来：先拒套话，再留声音/话题，缺口交给 acquire 去搜。

## 三层筛子

1. **拒**：writing-standards / humanize-ai 套话（值得注意的是、至关重要、深度赋能…）一律不进表
2. **留**：话题标签；口头禅（金句/洞见里同一术语 ≥3 次）；按标点+功能字切开的 3–6 字完整术语。不滑窗、不贪心切 8 字
3. **补**：知乎画像 `expertise_domains` 关键词 − 已有词表 = acquire 查询，走 search/build

## harvest

只读素材库的金句 / 洞见文件（`IME_MATERIAL_DIR`，默认 `~/Documents/ime-lexicon/素材库`）。
产物：`创作词库.tsv`（写入 `IME_DICT_DIR`）。禁止 apply，禁止灌全量词库。

```bash
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" harvest
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" harvest --speech
```

`--speech` 读语音转写数据源的转写 / 纠错历史（`IME_SPEECH_DIR` / `IME_XIGUA_DIR`）。

## guide

- `use`：行业/创作词
- `voice`：material 惯用词
- `gap`：素材里抽出、词库还没有的术语（最多 20）

```bash
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" guide --topic 投资理财
```

## acquire

画像 + 素材好词 − 已有词表。默认只打印 `have` / `gap` / `seek`。
`--out` 把 gap 写成一行一词，供 `build --from`。
`--run` 才真搜，append 到 `--out`（没有就写 `_acquire_{topic}.txt`）。不覆盖 `行业词库_*.txt`，不 apply。

```bash
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" acquire --topic 投资理财
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" acquire --topic 投资理财 --out /tmp/缺口.txt
```

画像路径：`IME_PERSONA`，未设时用默认（见 `paths.py`）。输出不含 user_id。

## 纪律

- harvest/guide/acquire 只出表，永远不 apply、不写 usr.dat / WeType
- 素材只取金句/洞见两句型，不抽正文、不抽已删除（~~）段
- 词库逻辑在 ime-lexicon，shili-material / shili-content / humanize-ai 不复制
