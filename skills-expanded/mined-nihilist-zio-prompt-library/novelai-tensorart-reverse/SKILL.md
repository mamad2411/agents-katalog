---
name: novelai-tensorart-reverse
description: Perform model-neutral image model triage before reverse-engineering prompts. Compare plausible families such as Midjourney/Niji, NovelAI, SD/SDXL variants, Flux, GPT Image/DALL-E, and 3D render pipelines; distinguish likely source from best reproduction route and state uncertainty. Query the local Tensor.Art prompt index only when the image and chosen workflow fit Danbooru/SD-style anime illustration tags. Do not force photography, 3D/CG, MJ, Flux, or general image-model work into NovelAI tags.
agent_created: true
---

# NovelAI / Tensor.Art 图片逆向提示词助手

## 这个 skill 做什么

维护一份 **Tensor.Art 官方 articles 开源提示词文章的本地全文索引**，在逆向日系 AI 插画时，按画面特征检索出**真实存在、社区验证过的 tag**，供生成提示词时取用。

- 数据源：`https://tensor.art/articles`（镜像域名 `tensorart.me` 可直连）
- 站点是 Nuxt SSR，`__NUXT_DATA__` 里内嵌了每篇文章的**完整正文**，无需登录、无需浏览器自动化、无需私有 API
- 索引由 `scripts/build_index.py` 生成，默认抓 `MOST_LIKE` + `LATEST` 两个排序批次，合计约 79 篇文章、数千行 tag

**它不做什么**：不负责识别画风、不负责生成整段提示词、不负责保证出图一致。逆向的最终判断仍由你完成。

## 何时触发

- 图片已判断为适合 Danbooru / SD tag 体系的日系插画，且需要补充构件级 tag
- 用户明确指定 NovelAI / Illustrious / Pony / SDXL 等 tag 工作流
- 用户反馈这类插画的头发像塑料、手指诡异、质感不对，需要按减法原则排查
- 用户需要发型、手部、光影、眼睛、姿势、背景、负面词、权重或质量 tag

仅收到“逆向这张图 / 这图什么模型画的”时，不要直接假设 NovelAI，也不要立即运行 tag 搜索。先完成下方模型鉴别步骤；只有画面适合 tag 语料时才使用本 skill。3D CG、摄影、Midjourney、Flux、GPT Image / DALL·E 等路线优先用其适配的渲染、摄影或自然语言提示词，不强行套 Danbooru tag。

## 三条铁律（先读，再检索）

1. **画风靠底模，不靠 tag。** 构图、动作、元素可以反推；线稿粗细、上色方式、渐变、高光形状是底模 / LoRA / finetune 决定的。检索结果只能补充**构件级 tag**，不能用来"堆出画风"。若画风对不上，先问用户当前底模，或建议换底模，而不是继续加词。
2. **减法原则。** 某个部位（头发、手）反复崩坏时，**彻底不描述该部位**，用裁切、遮挡、出画处理，或后期 inpaint。不要补质感词，不要堆负面词——SD 的 negative 是 CFG 反向引导，堆词会把注意力锁死在那个部位上，越改越糟。
3. **语法不通用。** Tensor.Art 文章里的 tag 多为 Danbooru / SD 语法。NovelAI 用 `{}`、`[]`、`::` 权重；SD 用 `(word:1.2)` 和独立 `negative prompt:`；Midjourney 用 `--no`、`--ar`。交付时必须标注模型，跨模型要改写，不能直接照搬。

详细规则与踩坑记录见 `references/reverse_rules.md`。

## 工作流

### Step 1 · 模型鉴别与画面定性（不动手检索之前）

先明确用户目标是推断**原图可能由什么模型生成**、寻找**最适合复现的模型路线**，还是已指定模型下写提示词。根据可见画种、构图习惯、几何与解剖一致性、材质反应、光照/阴影、边缘与笔触、文字及生成瑕疵，比较所有合理候选模型家族，不限于 NovelAI / Midjourney：包括 SD / SDXL（Illustrious、Pony 等）、Flux、GPT Image / DALL·E、其他通用图像生成模型，以及 Blender / Unreal / Octane 等真实 3D 渲染管线。区分“可以用某模型复现”与“原图由该模型生成”，并说明证据、置信度和备选；单凭外观不能确认来源时须明确不确定。

随后记录画种、宽高比、主体与动作、构图、光源方向与色温、色彩盘、介质与场景元素、易崩部位和画风特征。只有判断为适合 Danbooru / SD tag 的日系插画时，才继续使用下方 Tensor.Art 检索步骤；其他画种应采用对应模型的自然语言、渲染或摄影提示词，不套用本地 tag 索引。

### Step 2 · 检索相似构件 tag

```bash
python scripts/search.py hair backlight hand --limit 5 --lines 12
python scripts/search.py "头发 逆光 手部" --topic hair
python scripts/search.py --topic negative --lines 20
python scripts/search.py --list                     # 浏览全部文章标题
python scripts/search.py --topics                  # 可用主题
python scripts/search.py --article <id>            # 读某一篇完整正文
python scripts/search.py hair --json               # 程序化读取
```

关键词用**画面里真实存在的构件**，中英日皆可（内置中文→英文 tag 映射）。不要一次塞十几个词，先挑 2–4 个最能区分该图的。命中行通常就是 `english tag 中文注释` 形式，可直接取用。

若索引缺失或过期：

```bash
python scripts/build_index.py             # 增量合并
python scripts/build_index.py --refresh  # 全量重建
python scripts/build_index.py --url "https://tensorart.me/articles?sort=LATEST"
python scripts/build_index.py --article <id>     # 补抓单篇详情页
```

### Step 3 · 取用（只取需要的）

从命中行里挑 **少量** 与画面直接对应的 tag，按「主体 → 构图/动作 → 光影 → 背景 → 质量词」组织。
- 质量词最多 2–3 个，`masterpiece, best quality` 即可；`score_9` 系列只适用于 Pony，别混进 Illustrious。
- `negative prompt:` 控制在 **12 词以内**，单行逗号分隔，只写全局崩坏项（低分辨率、多余肢体、文字水印），不写具体部位质感。
- 参考文章里的模型/设置说明要单独提出来告知用户（例如某篇注明测试底模是 `Illustrious - AnimeMaster`），这往往比 tag 更有价值。

### Step 4 · 输出

- **每组提示词一个独立代码块，组内完全自包含**，不写「沿用上方母版」、不要求用户手动拼接。
- 每组开头标注所选模型和语法路线；简要说明选择依据及模型来源判断的不确定性。
- 只有选用 Midjourney 时才添加对应 MJ 参数；竖版 `--ar 9:16 --hd --raw --p`，方形 `--ar 1:1 --hd --raw --p`，横版 `--ar 16:9 --hd --raw --p`。不要将这些参数带入其他模型。
- 附一句模型/底模建议：画风相似度主要靠对应模型、底模与 LoRA；tag 只负责构件。
- 若用户提供了失败图，先对比「哪类差异是底模造成的」，不要只调 tag。

## 索引维护

- 索引文件：`assets/index.json`（结构化）+ `assets/articles/<id>.txt`（每篇纯文本）
- 仅在 `build_index.py` 中联网；`search.py` 完全离线，可反复调用
- 站点改版导致解析失败时，先看 `scripts/build_index.py` 的 `payload_root()` 与 `collect_articles()`，它们只依赖 `__NUXT_DATA__` 的 devalue 扁平数组结构
- 网络提示：`tensor.art` 在部分代理下返回 502，**抓取统一走 `tensorart.me`**；给用户看的原文链接仍用 `tensor.art`

## 故障排查

| 现象 | 处理 |
| --- | --- |
| `index missing` | 先跑 `python scripts/build_index.py` |
| 抓取全 FAIL | 确认能访问 `https://tensorart.me/articles`；保留已有索引继续离线检索 |
| 检索 0 命中 | 换英文 tag、`--list` 浏览目录、`--topic` 单独过滤 |
| 出图仍有塑料发 / 怪手 | 停止加词，改用减法原则 + 裁切 / inpaint，并核对底模 |
