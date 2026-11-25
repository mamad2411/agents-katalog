---
name: ime-lexicon-optimize
description: |
  合并多份词表，自动改明显英文笔误和「词对、拼音错」，剔除 v2u / 拼音当词。
  吃不准的进待确认，不写回输入法。
---

# optimize — 修正个人词库

父技能：`ime-lexicon`。本文件只改表。

## 何时用

- 豆包 + 微信两库合成一份
- 纠 `agnet` / `clade` / `skils` 这类明显错误
- 删指定垃圾词（`xx但是`）
- 不要在这里搜新行业词（走 build / 原 industry-dict）

## 自动改 vs 待确认

自动改（表在脚本 `TYPO_MAP`）：

- `agnet→agent` `clade→claude` `gork/grokgrok→grok` `flsah→flash`
- `shft→shift` `skilsub→skill` `prma→proma` `boos→boss`
- 词是英文、拼音只差 1 个字母，且不是高频缩写（`skills/skils` 改，`skill/skil` 留）

不自动改：`ocv`、产品名、短前缀。进 `待确认.tsv`。

## 命令

```bash
python3 "$HOME/.agents/skills/ime-lexicon/scripts/ime_lexicon.py" optimize \
  --from 工具/豆包输入法/个人词库.tsv \
  --from 工具/微信输入法/个人词库.tsv \
  --drop 'xx但是' --drop 'xx进入设置' \
  --out 工具/词库整合/优化
```

产出：`词库.tsv` `更正记录.tsv` `待确认.tsv`。

`--no-auto` 只合并不改字。

`--profile personal`（默认）：只砍「的了 / 的吧」、≥16 字句子、v2u。习惯词（含频次=1 的「示例词」）留。`--drop-fragments` 才再剔个人碎片。

`--profile industry`：再砍过长（≥10 字）、频次=1 残片、「的了」类、叠词。行业表默认狠。

`--budget N`：裁到 N 条。重复 (词,拼音) 留个人库（source 含 doubao/wetype/personal）。个人已超 N 则个人按频次留前 N。

## 代理步骤

1. 跑 optimize，报 in / out / fixed / review / profile。
2. 待确认里点名的才再改，不替用户猜缩写。
3. 要写回 → 父技能 import staging，问一句 apply。整表超过豆包剩余槽就加 `--budget`。
