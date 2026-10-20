---
name: publicist-china-ai-compliance
description: AI-generated content labeling compliance for mainland China, 显性标识/隐性标识 requirements per 《人工智能生成合成内容标识办法》 (effective 2025-09-01). Use when any pitch/content contains AI-generated segments.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# AI content labeling compliance, China market (2025-09-01 生效)

**Scope**. Mandatory compliance for ALL AI-generated content distributed in mainland China. Pair with `publicist-china` + platform skills.

## Legal basis
- **《人工智能生成合成内容标识办法》**, 国家网信办等四部门联合发布，2025-09-01 正式施行
- **《生成式人工智能服务管理暂行办法》**, 2023-08-15 生效，第4条要求标识
- **《互联网信息服务深度合成管理规定》**, 2022-12 生效，衔接适用

## Dual labeling requirement (双标识制)

### 显性标识, 用户可感知
| Content Type | Placement | Format Example |
|---|---|---|
| **文本** | 始末适当位置或交互界面 | "【AI生成】本段落由AI辅助创作" / 文末 "注：部分内容经AI润色" |
| **图片** | 适当位置 (水印/角标) | 右下角 "AI生成" 图标 + 半透明水印 |
| **音频** | 始末适当位置或交互界面 | 开头/结尾语音："本音频包含AI生成内容" |
| **视频** | 始末画面或播放周边适当位置 | 首帧/尾帧 "AI生成" 字幕 + 播放器角标 |
| **虚拟场景** | 起始适当位置或持续过程 | 进入场景提示："包含AI生成合成内容" |
| **下载/导出文件** | 文件内嵌 | 元数据 + 可视化标识同步保留 |

### 隐性标识, 机器可读 (元数据)
**必须字段** (嵌入文件元数据):
- 生成合成内容属性信息
- 服务提供者名称或编码
- 内容编号
- **鼓励**. 数字水印 (鲁棒性/不可感知)

## Platform enforcement (2025-09-01 后)
| Platform | Enforcement |
|---|---|
| 微信公众号 | 发布前核验标识；未标识/疑似 → 添加风险提示、限流 |
| 小红书 | AI内容必须标注；模糊/误导 → 违规限流 |
| 知乎 | 发布AI内容必须显著标识；否则增加标识/限制/封禁 |
| 抖音 | 逐帧扫描 + 链接分析；未标识 → 拦截、流量关停 |
| B站 | 上架审核核验标识；应用分发平台审核生成服务资质 |
| 百家号/头条/搜狐/网易 | 同步执行国家标准 |

## Compliance checklist (per pitch/content piece)
- [ ] **识别 AI 段落**. 哪些句子/图片/音视频由 AI 生成/辅助
- [ ] **显性标识**. 按内容类型在规定位置添加可见标识
- [ ] **隐性标识**. 文件元数据嵌入 4 字段 + 推荐数字水印
- [ ] **用户协议**. 明确标识规范，用户要求去除显性标识 → 协议约定责任 + 日志保存 ≥6个月
- [ ] **平台核验**. 发布前自检通过平台检测逻辑
- [ ] **记录留存**. 生成工具/版本/参数/标识位置/时间, 备查

## Pitch integration (how to declare in our workflow)
在 `prompts/china.md` 或平台技能的 pitch 模板中添加：
```
AI内容声明：本推介材料中 [第X段/配图X/数据可视化X] 由 [工具名/模型版本] 生成/辅助。
显性标识位置：[文首/文末/图片右下角/视频首帧]
隐性标识：元数据已嵌入 [提供者编码/内容编号]
```

## Negative patterns (避坑)
- ❌ 只加隐性不加显性 (用户无感知 = 违规)
- ❌ 标识位置不规范 (如文本只在文中间夹杂)
- ❌ 伪装成纯人工 (不声明 = 欺骗 = 重罚)
- ❌ 用户要求去除显性标识 → 未签协议/未留存日志
- ❌ 跨平台同步时标识丢失 (Wechatsync 等工具需保留标识)

## References
- `http://www.gov.cn/zhengce/zhengceku/2025-09/01/content_6980xxx.htm`, 办法全文
- `https://www.news.cn/legal/20250901/a12108b0b10249e5bae4435269e40c91/c.html`, 新华网解读
- 普华永道《人工智能生成合成内容标识办法》合规解码
- `skills/publicist-china/references/law-and-ethics.md`
- 各平台 2025 下半年合规公告

## What this skill does not do
- ❌ No auto-labeling tool (reference only)
- ❌ No legal advice (escalate to counsel)
- ❌ No MCP/CLI tools
