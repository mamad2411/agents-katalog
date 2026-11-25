---
name: ghostty-tint
description: 给 Ghostty（及任何支持 OSC 11 的终端）的每个新面板/分屏/标签自动换一种和谐的低饱和背景色，并能把一句话的「气质」描述变成 N 色色板。Use when the user wants random or rotating terminal pane colors, 每个分屏不同颜色, 面板随机配色, 终端背景自动换色, Ghostty 配色/主题/背景色, 区分多个 AI 会话或任务窗口, 想要某种气质/感觉/风格的终端颜色（如"京都秋天""赛博""护眼""莫兰迪"）, or wants 8/12/16/24 colors. Also for installing, switching moods, regenerating palettes with a different color count, or debugging why pane colors don't change.
---

# ghostty-tint：让每个面板都有自己的颜色

你要帮用户得到「每开一个面板，自动换一种好看的、彼此协调的背景色」，并且颜色的气质符合他的描述。整个过程用户只需要说一句话，你来完成安装、生成、体检、给出切换命令和备选气质。

本 Skill 目录自带全部文件（下文用 `<skill>` 表示本 SKILL.md 所在目录）：

```
<skill>/tint.sh            核心：被 source 进 ~/.zshrc，新面板自动换色，提供 tint 命令
<skill>/install.sh         安装器（幂等，可重复运行）
<skill>/tools/tint-gen.py  气质生成器：OKLCH 固定亮度/彩度，只转色相；也能体检色板
<skill>/moods/*.tint       7 种内置气质
```

## 第 1 步：判断用户要什么

| 用户说的 | 你要做的 |
|---|---|
| 「帮我装一下」「我也想要面板随机颜色」 | 安装（第 2 步）→ 推荐 3 个气质（第 5 步） |
| 「换个气质」「有没有暗色的」 | 列出内置气质，给出 `tint mood <名字>` |
| 「我想要 ××× 的感觉」 | 把描述翻译成参数生成新气质（第 3、4 步） |
| 「改成 16 色 / 24 色」 | `--like <当前气质> --count N` 重新生成 |
| 「颜色没变」 | 排查（文末） |

用户没说颜色数量时：浅色默认 8 色；用户常开很多面板（≥6 个分屏、多 AI 会话）时建议 12 色。

## 第 2 步：安装（只需一次）

先检查：`test -r ~/.config/ghostty-tint/tint.sh && echo installed`。没装就运行：

```bash
bash <skill>/install.sh            # 可加 --mood mist 设默认气质
```

它会复制文件到 `~/.config/ghostty-tint/`，并在 `~/.zshrc`/`~/.bashrc` 里加一段带标记的 source（重复运行不会重复添加）。如果它提示 rc 里已有别的 OSC 11 换色逻辑，告诉用户旧逻辑会和新逻辑互相覆盖，**征得同意后**再帮他注释掉旧的那几行，不要擅自删除。

注意：你的 Bash 工具不是用户的终端面板，你执行 `tint` 的颜色用户看不到。让用户自己在 Ghostty 里运行切换命令，或新开一个面板（⌘D）。

## 第 3 步：把「气质」翻译成参数

气质 = 亮度 L + 彩度 C + 色相范围（hue 起点 + span 跨度）。所有颜色共享 L 和 C，只有色相不同，所以天然协调、文字在每个面板上一样清楚。

| 维度 | 取值参考 |
|---|---|
| L 亮度 | 浅色 0.86–0.94（越高越轻盈，0.93 像雾，0.86 像灰调纸）；深色 0.20–0.30 |
| C 彩度 | 0.015 几乎是灰 · 0.025 低饱和（默认纸感）· 0.04 清楚的颜色 · 0.055 糖果感；深色可到 0.06 |
| hue 色相 | 0 粉红 · 30 珊瑚 · 60 杏 · 95 黄 · 130 黄绿 · 150 绿 · 190 青 · 240 蓝 · 280 靛 · 310 紫 · 345 粉 |
| span 跨度 | 360 全色轮（最好区分）· 120–160 一段色相（更统一、更有主题感）。span < 360 时 C 要 ≥ 0.03 才分得清 |

翻译示例（照这个思路推理，不要死记）：

| 用户描述 | 参数 | 理由 |
|---|---|---|
| 京都秋天、寺庙、枫叶 | `--l 0.89 --c 0.045 --hue 20 --span 110` | 红—橙—金一段暖色，略深像旧木 |
| 护眼、长时间写代码 | `--l 0.92 --c 0.025 --hue 100 --span 120` | 黄绿到青，低彩度 |
| 北欧、冷静、极简 | `--l 0.93 --c 0.02 --hue 200 --span 140` | 冷灰蓝，几乎无彩 |
| 少女心、春天 | `--l 0.92 --c 0.05 --hue 330 --span 160` | 粉—桃—杏 |
| 赛博朋克、直播演示 | `--l 0.24 --c 0.065 --hue 280 --span 360 --dark` | 深底高彩 |
| 深夜、低调、不刺眼 | `--l 0.26 --c 0.025 --hue 200 --span 360 --dark` | 深色低彩 |
| 「像这个颜色」+ 一个色值 | `--seed '#RRGGBB'` | 从种子色取 L/C/hue，绕色轮扩展 |

## 第 4 步：生成 → 起名 → 体检

```bash
python3 <skill>/tools/tint-gen.py --name kyoto --title "京都秋 Kyoto" \
  --vibe "旧木与枫叶，暖而不燥" --count 8 --l 0.89 --c 0.045 --hue 20 --span 110 \
  -o ~/.config/ghostty-tint/moods/kyoto.tint
```

然后**给每个颜色起一个有画面感的中文名**：打开生成的文件，把每行 `bg #XXXXXX 红 red` 改成 `bg #XXXXXX 枫红 maple red`（中文名 + 英文名 + 保留色相英文词，方便用户 `tint red`）。名字要和气质同一个世界观（京都 → 枫红、柿色、金阁、抹茶、苔庭……）。不要改色值，不要改顺序（顺序必须保持色相顺序，tint 会自动分散取色）。

最后体检：

```bash
python3 <skill>/tools/tint-gen.py --check ~/.config/ghostty-tint/moods/kyoto.tint
```

- 最低对比度 < 7：浅色把 L 调高 0.02，深色把 L 调低 0.02，重新生成。
- 相邻面板最小色差 ΔE < 3：C 加 0.008 或 span 加大，重新生成。
- 两项都过了才交付。

## 第 5 步：交付话术

回复保持短，按这个结构（不要复述过程）：

1. 一句话说做好了什么：「给你做了 8 色『京都秋』：旧木与枫叶，暖而不燥。」
2. 一张色板表：序号 · 名字 · 色值（Markdown 表格，最多 16 行，更多就只列前 8 个加「…」）。
3. 让用户在 Ghostty 里执行（用代码块，方便复制）：
   ```
   tint mood kyoto
   ```
   并说明：之后每个新面板（⌘D 分屏 / ⌘T 标签）会按黄金角顺序依次换色，相邻面板永远差得够远。
4. **再给 3 个备选气质**，每个一行：名字 + 一句气质 + 切换命令。优先从内置气质里选和用户描述最接近/最互补的（比如用户要暖色，就给一个冷静的、一个深色的、一个更活泼的），也可以给出一条现成的生成命令。

内置气质：

| id | 名字 | 色数 | 气质 |
|---|---|---|---|
| paper | 纸感 Paper | 8 | 低饱和暖纸色，像一桌便签（默认） |
| mist | 晨雾 Mist | 8 | 冷调雾色，安静专注不累眼 |
| matcha | 茶室 Matcha | 8 | 抹茶麦秆苔藓，木质温润 |
| macaron | 马卡龙 Macaron | 12 | 甜而不腻，开再多也不撞色 |
| morandi | 莫兰迪 Morandi | 16 | 灰调高级，16 色依旧克制 |
| midnight | 夜航 Midnight | 8 | 深夜舷窗，暗色也有温度（深色） |
| neon | 霓虹 Neon | 12 | 赛博夜市，深底高彩适合演示（深色） |

任意内置气质都能改数量：`tint gen --like morandi --count 24 --name morandi24 -o ~/.config/ghostty-tint/moods/morandi24.tint`。

## 常用命令（告诉用户时挑相关的说，别全贴）

```
tint              换下一个颜色           tint ls           看当前气质所有颜色
tint random       随机换一个             tint mood         列出全部气质
tint 3 / tint red / tint 后端   指定颜色  tint mood mist    切换气质
tint '#D7E2EC'    任意颜色               tint reset        恢复主题默认
```

环境变量（写在 rc 里 source 之前）：`TINT_ORDER=random|seq|spread`、`TINT_AUTO=0`（不自动换）、`TINT_ANY_TERM=1`（iTerm2/WezTerm/kitty 等也启用）、`TINT_WASH=1`（宿主不支持分屏独立 OSC 11 时用单元格底色铺满，如旧版 cmux）。

## 排查：颜色没变

按顺序检查，找到原因就停：

1. 是否是新面板？已打开的面板不会自己变，运行 `source ~/.zshrc && tint` 或新开面板。
2. `grep -n ghostty-tint ~/.zshrc` 有没有那段 source；`echo $TERM_PROGRAM` 是否为 `ghostty`（不是的话设 `TINT_ANY_TERM=1`）。
3. rc 里后面是否还有别的脚本又发了 OSC 11 或 `clear`/主题切换把颜色盖掉（把 source 行移到 rc 末尾试试）。
4. tmux 里：已自动透传；若仍无效，在 `~/.tmux.conf` 加 `set -g allow-passthrough on`。
5. Ghostty 的 `background-opacity` < 1 时颜色会被透明度冲淡，这是正常现象。
6. 嵌入 Ghostty 的宿主（如旧版 cmux）所有分屏变成同一色：设 `TINT_WASH=1`。
