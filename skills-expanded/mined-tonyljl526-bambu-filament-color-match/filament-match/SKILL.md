---
name: filament-match
version: 1.2.0
description: 离线耗材配色助手，内置拓竹官方材料色库、彩多屋纯色色卡和 Polymaker 官方 HEX 色卡，可根据 HEX 或图片主色匹配最接近的耗材颜色，并生成本地 HTML 色卡，无需联网查询。
---

# 3D打印耗材颜色识别助手

这是一个本地离线使用的 3D 打印耗材配色 Skill。它会优先使用随包提供的数据快照，不联网查询，除非用户明确要求刷新或核验色库来源。

适合用来回答这类问题：

- 这张图片里的蓝色/红色/黄色，更接近哪款耗材？
- 一个 HEX 色值在拓竹或彩多屋里最接近哪几个颜色？
- 帮我生成一个可搜索、可筛选、可打印的本地 HTML 色卡。
- 做多色打印时，帮我列出材料系列、中文名、HEX 和感知色差。

## 支持色库

- `--brand bambu`（默认）：拓竹官方色库，覆盖 PETG HF、PLA Basic、PLA Matte、PLA Lite。
- `--brand caiduowu`：彩多屋纯色色卡，来自用户提供的彩多屋色卡海报，已排除透明、彩虹、金属、变色龙、夜光、双色/三色/四色等非纯色条目。
- `--brand polymaker`：Polymaker 官方 HEX 色卡，来自 Polymaker 商品页中明确标注 `HEX Code` 的颜色条目。

## 使用流程

1. 找到当前 Skill 目录，并按需要选择数据源：
   - 拓竹：`references/bambu-filament-colors.json`
   - 彩多屋：`references/caiduowu-filament-colors.json`
2. 如果用户提供图片，运行：

```bash
python3 scripts/match_colors.py \
  --brand bambu \
  --image "/absolute/path/to/image.png" \
  --materials "petg,pla-basic,pla-matte,pla-lite" \
  --colors 6 \
  --top 3 \
  --html "/absolute/path/to/bambu-color-card.html"
```

3. 如果用户提供已知 HEX 色值，运行：

```bash
python3 scripts/match_colors.py \
  --brand caiduowu \
  --hex "#E8AFCF,#0056B8,#F9DFB9" \
  --top 3 \
  --html "/absolute/path/to/filament-color-card.html"
```

```bash
python3 scripts/match_colors.py \
  --brand polymaker \
  --hex "#0056B8,#FEC600,#C12E1F" \
  --top 3 \
  --html "/absolute/path/to/polymaker-color-card.html"
```

4. 输出推荐结果时，说明品牌/色库、材料系列、中文名、英文名（如有）、HEX 和 Delta E 色差。
5. 如果生成了 HTML 色卡，把本地文件路径返回给用户。

## 匹配规则

- 拓竹色库中，`petg` 默认映射为 `PETG HF`。
- 除非用户指定材料范围，否则使用当前品牌下的全部材料系列参与匹配。
- 普通近色匹配优先使用纯色耗材。
- 只有在用户明确需要渐变耗材时，才加 `--include-gradients`。彩多屋当前只包含纯色条目。
- 如果不同材料拥有相同或相近 HEX，也要保留为不同候选，因为它们对应不同购买选择。
- 结果表示“数字参考色的最近匹配”，不保证实物打印颜色完全一致。光线、相机白平衡、材料表面、层纹和打印参数都会影响观感。
- 彩多屋 HEX 是从用户提供海报中抽样估算的代表色，不是厂家公布的官方数字色值。
- Polymaker 只收录官方商品数据中明确带 `HEX Code` 的条目；没有官方 HEX 的颜色故意跳过。
- 产品图如果有大面积纯色背景，默认会抑制边缘背景；如果用户要匹配背景本身，再加 `--keep-background`。

## 常用命令

列出拓竹色库：

```bash
python3 scripts/match_colors.py --list
```

列出彩多屋纯色色库：

```bash
python3 scripts/match_colors.py --brand caiduowu --list
```

列出 Polymaker 官方 HEX 色库：

```bash
python3 scripts/match_colors.py --brand polymaker --list
```

生成可搜索的本地 HTML 色卡：

```bash
python3 scripts/match_colors.py \
  --catalog-html "/absolute/path/to/bambu-90-color-catalog.html"
```

```bash
python3 scripts/match_colors.py \
  --brand caiduowu \
  --catalog-html "/absolute/path/to/caiduowu-pure-color-catalog.html"
```

```bash
python3 scripts/match_colors.py \
  --brand polymaker \
  --catalog-html "/absolute/path/to/polymaker-official-hex-catalog.html"
```

输出 JSON 结果：

```bash
python3 scripts/match_colors.py --hex "#FF0000" --json
```

只匹配指定材料系列：

```bash
python3 scripts/match_colors.py --image "/path/image.jpg" --materials "pla-matte,pla-lite"
```

```bash
python3 scripts/match_colors.py \
  --brand caiduowu \
  --image "/path/image.jpg" \
  --materials "petg,pla-matte,pla-bio,pla-silk-solid"
```

## 数据说明

如果用户关心数据来源、可信边界或限制，读取 `references/data-notes.md`。

拓竹 JSON 包含：

- 38 个 PLA Basic 条目
- 25 个 PLA Matte 条目
- 13 个 PLA Lite 条目
- 14 个 PETG HF 条目

它保留了拓竹官方中文名、英文名、内部标识、官方 `#RRGGBBAA`、派生 `#RRGGBB`，以及渐变色端点。

彩多屋 JSON 包含 125 个纯色条目，覆盖：

- PETG-CF
- ABS
- PETG
- PLA Matte
- PLA+ Bio
- PLA Silk Solid
- TPU
- PLA-CF

彩多屋透明、彩虹、金属、变色龙、夜光、丝绸多色、双色、三色和四色条目已故意排除。

Polymaker JSON 包含 158 个官方 HEX 条目，覆盖：

- PolyLite PLA
- PolyMax PLA
- PolySonic PLA
- PolyLite LW-PLA
- Panchroma Matte PLA
- Panchroma Satin PLA
- Polymaker PETG
- PolyLite Translucent PETG
- PolyMax PETG
- PolyLite ABS
- Polymaker ASA
- PolyFlex TPU90
- PolyFlex TPU95
- PolyFlex TPU95-HF
