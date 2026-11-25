---
name: sealeap-hundun-amazon-main-image-whitebg-production
description: "Verify current Amazon main-image compliance requirements (pixel size, product-fill ratio, pure white background, prohibited badges or watermarks) and turn a sourced product photo into a compliant white-background main image through a repeatable cutout, resize and export workflow, then diagnose non-display issues via the seller backend's image-issue checks. Use for 主图不显示怎么排查、白底图怎么判断是不是纯白、供应商图片能不能直接用、抠图方式怎么选、主图导出格式与大小要求. Do not use to add platform badges, recommendation labels or watermarks manually, or to skip category-specific image rules that differ from the general main-image rule."
---

# Amazon 主图白底图合规制作

## 目标

Verify current Amazon main-image compliance requirements (pixel size, product-fill ratio, pure white background, prohibited badges or watermarks) and turn a sourced product photo into a compliant white-background main image through a repeatable cutout, resize and export workflow, then diagnose non-display issues via the seller backend's image-issue checks.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的像素下限、最优像素区间、占比百分比与文件大小上限是特定时点的规范摘录，可能已随政策更新变化；一律以当前卖家后台图片要求页面的实时内容为准。
- 系统自动生成的角标、推荐标识等来源提到“不能手动添加”，这一限制以当前平台规则为准；本 Skill 不建议尝试还原或伪造任何系统生成标识。
- 供应商提供的产品图片版权归属与是否可商用需自行确认，直接使用未经授权的他方拍摄图片存在侵权风险；本流程假设图片来源已获得使用授权。
- 抠图与合规处理只解决图片能否正常展示的问题，不等同于图片能提升点击率或转化，效果需另外做单变量验证。

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

1. 上传前到卖家后台帮助搜索当前商品图片要求页，逐条记录本站点、本类目的硬性项：主图最短边像素下限（并了解建议的更优像素区间）、商品主体占画面比例下限、是否允许多角度/多主体拼接出现在主图、是否有类目专属规则；不同类目规则不同，不能用一份通用清单套所有产品。
2. 判定纯白底不能靠肉眼：用截图工具或修图软件的取色器在背景区域取样，确认 RGB 三项数值是否完全一致且达到纯白标准；供应商提供的白底图经常接近白但未达标，必须实测后再决定是否可直接使用。
3. 根据背景类型选择抠图方式：纯色背景用魔棒/选取工具批量选取后删除或反向选取主体；背景含杂物或渐变的复杂背景改用钢笔工具或类似精细路径工具逐步抠出主体，避免用魔棒硬抠导致边缘锯齿或主体缺损。
4. 抠出主体后新建符合像素要求的画布，将主体居中放大到接近满版但不裁切、不留大面积空白边缘，检查边角是否有残留锯齿或半透明像素，必要时用修补工具处理边缘。
5. 核对图片不得包含的内容：不得出现平台角标、推荐标识等系统自动生成的标记（这些由系统按数据表现自动附加，不能手动加到图片上），不得出现自有品牌 logo、水印或与在售商品无关的元素。
6. 导出为当前要求的图片格式，控制文件体积在建议上限以内以避免后台上传卡顿或失败；文件命名使用英文，避免特殊字符或中文导致上传异常。
7. 上传后如图片未在 Listing 页面展示，先到后台的图片问题诊断入口核查具体原因（如占比不足、背景不纯、尺寸不达标等），按提示逐项修正后再重新上传，不盲目重复上传同一张问题图。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 当前站点/类目主图合规要求核对表
- 纯白底取色核验记录
- 抠图与画布处理后的成品图（按格式/大小要求导出）
- 图片不展示问题排查记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
