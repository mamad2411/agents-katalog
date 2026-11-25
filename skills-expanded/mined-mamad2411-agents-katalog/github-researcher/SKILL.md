---
name: github-researcher
description: GitHub 开源项目深度调研工具。在 GitHub 上搜索、分析特定领域的开源项目，汇总生成结构化调研报告。触发场景：用户要求"调研 GitHub 上的 XXX 工具"、"搜索 XXX 开源项目"、"汇总 GitHub 仓库"、"找 XXX 的开源替代方案"、"对比 GitHub 上的 XXX 项目"、或需要批量分析开源项目并输出报告时使用此 skill。
---

# GitHub 开源项目调研工具

深度调研 GitHub 上的开源项目，生成结构化调研报告。

**默认报告存放路径:** `/Users/lytton/mac_wps_clound/Obsidian笔记知识库/调研分析`

## 工作流程

### 1. 需求确认

明确调研目标：
- 调研领域/功能（如：视频下载工具、PDF 处理库、CLI 框架）
- 目标语言/技术栈（可选）
- 特殊需求（如：star 数要求、维护状态、许可证）

询问用户：
- 报告输出路径（默认询问）
- 是否有特定关注点

### 2. 多维度搜索

使用 WebSearch 进行多轮搜索，覆盖不同关键词组合：

```
# 搜索策略模板
"github {功能} {类型} downloader/scraper/tool/library"
"github {功能} stars:>1000"
"site:github.com {功能} {技术栈}"
"github {功能} best practices"
"github {竞品名} alternative"
```

**搜索维度：**
- 功能关键词（中英文）
- 技术栈（Python/TypeScript/Go/Rust 等）
- 使用场景（CLI/GUI/API/Web）
- 相关话题（GitHub Topics）

### 3. 信息收集

对每个发现的仓库，收集以下信息：

| 字段 | 说明 |
|------|------|
| 仓库名称 | owner/repo |
| 星标数 | stars 数量 |
| 主要功能 | 核心特性 |
| 技术栈 | 语言/框架 |
| 维护状态 | 最近更新时间 |
| 许可证 | MIT/Apache/etc |
| 特点/亮点 | 独特优势 |

**信息来源：**
- GitHub 仓库主页
- README.md
- Issues/Discussions
- Release 页面

### 4. 分类整理

将仓库按功能/用途分类：

```
示例分类结构：
├── 综合工具（功能全面）
├── 专用工具（特定场景）
├── CLI 工具
├── GUI/桌面应用
├── 库/SDK
├── 浏览器扩展
└── 已弃用/不维护
```

### 5. 对比分析

制作对比表格，包含关键指标：

| 工具名 | Stars | 语言 | 无需API | GUI | 功能A | 功能B | 推荐指数 |
|--------|-------|------|---------|-----|-------|-------|----------|
| ... | ... | ... | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ⭐⭐⭐⭐ |

### 6. 生成报告

输出 Markdown 格式报告，包含：

```markdown
# {调研主题} GitHub 开源项目调研报告

> 调研日期: YYYY-MM-DD
> 调研目标: [目标描述]

## 一、最推荐工具（Top Picks）
[2-3 个最佳选择，含详细说明]

## 二、分类工具列表
[按类别组织的仓库列表]

## 三、功能对比表
[对比表格]

## 四、使用建议
[按场景推荐]

## 五、注意事项
[法律/技术/安全提醒]

## 六、参考链接
[所有仓库链接]
```

### 7. 保存报告

**默认路径:** `/Users/lytton/mac_wps_clound/Obsidian笔记知识库/调研分析`

- 文件命名格式: `{调研主题}-GitHub调研报告.md`
- 用户可指定其他路径，否则使用默认路径
- 使用 Write 工具写入文件
- 确认写入成功

## 搜索技巧

### GitHub 高级搜索语法

| 语法 | 示例 | 说明 |
|------|------|------|
| `stars:>n` | `stars:>1000` | star 数大于 n |
| `language:xxx` | `language:python` | 指定语言 |
| `pushed:>date` | `pushed:>2024-01-01` | 最近更新 |
| `license:xxx` | `license:mit` | 许可证类型 |
| `topic:xxx` | `topic:twitter` | GitHub Topic |

### 关键词扩展

```
英文: downloader, scraper, exporter, batch, bulk, archive
中文: 下载, 爬取, 导出, 批量, 归档
场景: CLI, GUI, API, web, extension
```

## 质量标准

1. **覆盖面**: 每个调研至少发现 10+ 相关仓库
2. **深度**: Top 3 工具需详细说明功能和使用方式
3. **时效**: 标注仓库最后更新时间
4. **实用**: 提供具体使用建议和代码示例
5. **客观**: 包含注意事项和局限性
