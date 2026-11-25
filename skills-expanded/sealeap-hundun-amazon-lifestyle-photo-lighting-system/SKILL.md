---
name: sealeap-hundun-amazon-lifestyle-photo-lighting-system
description: "Plan a listing's full visual content set (main image, secondary images, optional video, and A+ modules where brand-registry eligible) mapped to category needs, and art-direct lifestyle photography using color-isolation, centered composition and basic multi-point lighting so the product reads clearly against its environment. Use for 副图该放什么内容、场景图怎么布光、产品和背景怎么做区隔、不同类目图片数量怎么规划、没有专业设备怎么拍场景图、A+ 图片尺寸多大. Do not use to claim a specific lighting setup guarantees higher conversion without an account-level before/after test, or to skip current brand-registry eligibility checks for A+ content."
---

# Amazon 场景图布光与图片体系规划

## 目标

Plan a listing's full visual content set (main image, secondary images, optional video, and A+ modules where brand-registry eligible) mapped to category needs, and art-direct lifestyle photography using color-isolation, centered composition and basic multi-point lighting so the product reads clearly against its environment.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的像素尺寸与各站点 A+ 资格差异为特定时点信息，需以当前后台实时提示与政策为准，不作为长期不变的规范。
- 简约风格更受欢迎、特定构图/光线手法能提升点击率均为来源的经验判断，未经账户内验证前记为待验证假设。
- 场景图中使用未随附赠送的道具需明确视觉呈现不会让买家误解为赠品；来源提到部分买家会因道具产生疑虑，属于需要在图片说明或详情页澄清的风险点。
- 素材必须为自有拍摄或已获合法授权，使用无版权来源不明的图片存在侵权风险，不建议直接采用。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实和当前 Listing
- 同购买意图可比竞品、价格、评论、图片和销量
- Search Term、Placement、CTR、CVR、订单、退货和利润
- VOC、Q&A、退货原因与任何页面或广告变更日志

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先按当前政策确认本账户可用的图片位与资格：主图 1 张（白底）、副图数量上限（含可选视频位）、A+ 内容是否已开通品牌资格及各站点是否都支持同一套模块，不假设所有站点规则一致，以当前后台为准。
2. 按类目规划副图内容分工而非随意拍摄：电子类适合安排功能特写、界面或配件展示、使用场景，必要时补一段功能演示视频；服装/家居类适合安排场景图、材质细节、尺寸参照，具体分工参照同类目在售的高表现 Listing，不照搬其画面只借鉴内容类型。
3. 场景图构图先做产品与环境的视觉隔离：把产品放在画面视觉中心，环境道具尽量选择弱化色彩而让产品保留原色，或反向处理，突出产品而不是环境；道具数量克制，避免喧宾夺主或让买家误以为道具随附赠送。
4. 简易布光可用三点思路搭建：主光模拟自然光从正前方偏上打向产品减少生硬阴影，背景/轮廓光从主体两侧后方打向背景或人物边缘制造分离感，避免逆光或强侧光在产品上投出遮挡细节的阴影；没有专业设备时可用白色泡沫板/反光板加基础灯具搭出近似效果。
5. 素材版权与合规检查：确认拍摄素材为自有拍摄或已获授权，不使用来源不明的网络图片；图片内容不得包含系统生成元素，不得展示非随附赠送的道具造成误导。
6. A+ 内容按当前允许的模块尺寸制作（以后台实时提示的桌面端/移动端尺寸为准），把场景图复用到 A+ 页面时保持风格统一，避免主图、副图、A+ 三处视觉调性不一致。
7. 小批量上线后对比同类目平均水平与自身历史数据，观察点击率与转化率变化，若某类场景图表现不达预期，回头检查是否道具喧宾夺主、构图偏离视觉中心或光线导致细节丢失。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取同类目高表现 Listing 的公开图片内容类型分布，作为图片体系分工的对照参考。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 按类目分工的图片体系清单（主图/副图/视频/A+ 模块）
- 场景图构图与布光方案（含简易设备替代方案）
- 素材版权与合规核查记录
- 上线后点击率/转化率对比记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
