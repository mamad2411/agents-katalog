---
name: vi-say
description: 将 GitHub 项目、官网、文章、播客访谈、已录视频或知识主题制作成讲解视频、动态演示和三比例海报。支持 HTML 前审、授权本地配音、原声剪辑、角色、图解与动画。
license: Apache-2.0
metadata:
  author: Anthony Li
  version: "0.0.15"
---

# vi-say：把内容讲给你看

名称取 Visual + Say。适用于项目分享、产品介绍、文章解读、播客精华、已录视频剪辑、知识科普和实战复盘。当次品牌、参考、角色和已认可素材优先。

## 先选路线，再按节点读文档

先读 [workflow.md](references/workflow.md) 选择场景，再只读当前节点的文档；不要每次加载全部工具说明。

| 路线 | 固定入口 | 要点 |
|---|---|---|
| 小龙讲解（GitHub、产品、知识） | `production.py init` → `review`（HTML 前审＋自查）→ `render`，见 [production.md](references/tools/production.md) | 默认 comic 漫画积木主题，不另写渲染工程 |
| 播客／访谈精华 | [播客精华路线](references/tools/podcast-highlights.md) | 静音原画铺满画幅，新旁白讲重点，标签与气泡在讲到时出现 |
| 真人原声录屏剪辑 | `production.py render-recorded-edit`，见 [原声录屏剪辑](references/tools/recorded-video.md) | 先标口头语和系统播放区间；双语字幕、有声片尾；不加角色 |
| 录屏漫画增强 | `assets/remotion/render-recorded.mjs`，见 [漫画录屏](references/tools/remotion.md#完整录屏的漫画积木路线) | 保留用户要求的片头与双语高亮；不插长静音等页面切换 |
| 企业产品片 | `--preset studio`，见 [产品演示动效](references/tools/business-effects.md) | 可隐藏角色；先用 `production.py catalog` 查实际模块 |

单期产品、台词、事实数字、来源和发布状态放项目资料；小龙固定开场与角色素材属于系列配置。GitHub 项目介绍默认核对当期 Star 数，采集真实产品截图用于成片，口播前 3–5 秒先给出具体问题或收益，见 [内容](references/stages/content.md#github-项目介绍默认项)、[脚本](references/stages/script.md) 与 [画面](references/stages/visuals.md#真实产品截图)。其他可执行能力见 [代码复用地图](references/tools/reuse-map.md)。

| 流程节点 | 独立文档 | 可以调整什么 |
|---|---|---|
| 1. 理解与提炼 | [content.md](references/stages/content.md) | 受众、选题角度、内容范围 |
| 2. 完整脚本 | [script.md](references/stages/script.md) | 表达口吻、叙事结构、传播目标 |
| 3. 分镜 | [storyboard.md](references/stages/storyboard.md) | 解释方式、镜头组织、阅读顺序 |
| 4. 声音 | [voice.md](references/stages/voice.md) | 原声／配音、语言、授权音色、节奏 |
| 5. 字幕与语义时间 | [captions.md](references/stages/captions.md) | 显示方式、字体、强调、位置 |
| 6. 画面与图解 | [visuals.md](references/stages/visuals.md) | 视觉风格、流程图、比较、操作演示 |
| 7. 动画与样片 | [animation.md](references/stages/animation.md) | 动作、转场组合、新增效果 |
| 8. 互动片尾 | [outro.md](references/stages/outro.md) | 文案、行动、图标和布局 |
| 9. HTML 前审 | [workflow.md](references/workflow.md#html-前审) | 视频画面、口播、字幕和动作的同步预览 |
| 10. 海报与发布文案 | [poster.md](references/stages/poster.md)、[publishing-copy.md](references/stages/publishing-copy.md) | 海报构图与纯文本 `发布文案.txt` |
| 11. 检查与交付 | [delivery.md](references/stages/delivery.md) | 交付组合、实际检查记录 |

- 新制完整视频默认先做 [HTML 前审](references/workflow.md#html-前审)。用户确认预览、进入完整发布交付时，先用 `production.py promote-delivery` 将前审清单转为正式清单，再渲染 MP4、核对三比例发布海报与发布文案，并对正式清单运行 `check-delivery`。已有同范围正式清单的局部修改沿用 `revise-delivery`。明确要求先看海报、仅制作海报或跳过 HTML 时，按对应约定执行。
- 片尾在最终声音与时间轴里一起编排，不是最后另拼一段声音。

## 小龙系列的固定做法

- **风格**：[漫画积木风](references/styles/comic-bricks.md)：小龙、粗描边分镜、对话气泡、网点与硬阴影，每个重点是一块积木。五种场景的版式、字号、动效和转场都由代码固定，HTML 前审和 MP4 共用同一组件；每期只改内容、`tone` 背景色、`highlight` 标题高亮和素材。旧玻璃/灰绿方向只留给历史项目，所有效果在 comic 主题下自动画成漫画样式。Bot 造型见 [Bot 样式](references/styles/bots.md)。
- **动效**：从公共库选择：气泡、积木、爆炸贴纸、呼吸卡片（逐条出现、讲完收起）、聚光灯、手绘圈注、打字机、印章、逐条打勾；任意效果都可设 `exit` 收起和 `breathe` 呼吸。动作时间写 `"cue": "口播里的词"`，编译时从最终 WAV 的对齐结果换算，不手填秒数。对动效不满意，就改 `comic-motion.mjs` 的公共参数，见 [动画模块](references/tools/animation-modules.md#跟着口播出现用词代替秒数)。
- **转场**：comic 主题只在 8 种漫画转场里选，片尾入场固定；其他主题的 35 种轮换见 [GL 转场](references/tools/gl-transitions.md)。
- **开场、声音、字幕**：固定开场见 [脚本](references/stages/script.md#小龙系列固定开场)，女声选择见 [声音](references/stages/voice.md#小龙系列的声音选择)，中英双语字幕、中文去标点、关键词高亮见 [字幕](references/stages/captions.md#中文口播的显示标点与关键词)。
- **改配置**：色板读 [色板](references/styles/colors.md)，角色或口型读 [角色](references/styles/character.md)，新增动画或场景读 [extensions.md](references/extensions.md)。配置只用已实现字段；新效果要同时落地画面、校验和实际样片。

## 质量底线

- `compile`、`render` 和 `preview-html` 渲染前自动运行 [检查](references/tools/production.md#渲染前检查)：缺字幕或高亮、片尾没声音、口播长静音、字幕漏句、海报进视频、小龙没用 comic，都会直接报错。例外要在 `project.json` 的 `preflight.allow` 里写明用户原话。字幕时间用 `align_captions.py --cues` 从 ASR 结果生成，不手写对齐脚本。
- 事实和效果依据本期资料与真实素材；模拟界面、对话和图解明确标示意。
- 已录视频默认保留原声、原速，剪辑音画同步。新声音使用获授权的当前参考，默认 1.0 速，平稳连贯；术语短测和最终整轨听审分开做，未听审的只交付明确标注的候选，规则见 [声音](references/stages/voice.md)。
- 字幕、口型与动画都用最终声音的可靠时间；改稿或换音轨后重新对齐，动作时长不随整段等比例拉伸。
- 静态画面、连续运动、音画语义与听感分别检查；自动校验不等于审美或听感通过，没实际检查就标明未检查。
- 制作、候选和听审状态写进文件名、交付说明与检查记录，不烧录到画面；只有用户明确要求才显示。
- 默认小龙与编辑式场景为 16:9，其他比例需要对应实现；三比例海报分别独立构图。

## 交付、归档与分发

- 完整项目开工就建 [交付清单](references/tools/delivery-check.md)。局部修订先用 `production.py revise-delivery` 继承原清单并锁定不变产物。交付前运行 `production.py check-delivery <清单>`，补齐缺项，再按 [交付节点](references/stages/delivery.md) 核对质量。回复同时给出视频与配套文件入口；文件齐全、视听认可、实际发布分开记录。录屏增强与局部修订不缩小原项目的交付范围；发布海报和文案独立交付，不替换视频片头。
- 从技能根目录调用脚本。`private/` 只存用户私有模型、音色参考及必要配置；试音、旁白、缓存、日志写入 `work/<项目>/`，成品写入 `outputs/<项目>/`（根目录只放项目目录）。私有音色配置只从当前制作项目读取，不自动查其他项目。本地配音模型默认放当前项目的 `private/models/`，用户指定共享路径时不重复下载；Remotion 共用 `.cache/remotion/`。
- 归档用 `production.py archive`，按 [归档工具](references/tools/archiving.md) 填清单执行，只保存成品和实际提示词。
- 分发用 `production.py pack outputs/vi-say/vi-say.skill`，排除测试、缓存、产物、私人声音、模型与密钥；全局安装副本不会随源码编辑自动更新。

本技能的原创代码与文档作者为 Anthony Li，采用 [Apache-2.0 许可证](LICENSE)，版权声明见 [NOTICE](NOTICE)。分发包须携带这两个文件；第三方依赖与素材保留各自许可及声明。
