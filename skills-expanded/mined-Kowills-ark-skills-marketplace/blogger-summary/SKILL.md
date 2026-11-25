---
name: blogger-summary
description: >
  总结博主(当前支持b站up主）一段时间内的图文动态和视频内容，提取关键观点生成结构化总结，支持多平台。
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Write
  - Edit
  - Skill
  - AskUserQuestion
---

# blogger-summary：博主观点总结

自动获取并总结博主（支持多平台）近期动态、视频字幕，提取关键观点生成清晰的结构化总结。依赖 `opencli` 工具获取数据。

## 依赖要求

- 需要已安装 `opencli`（B站适配器用于获取数据）
- 需要 `jq` 或 `python3` 用于JSON解析

## 使用方式

**示例：**
- `李大霄 今天的观点总结下`
- `于谦 最近讲了什么`

## 执行流程

### 1. 解析参数

从用户表达的意图内容中提取：
- **第一个参数：** UP主名字（必填，精确匹配）
- **第二个参数：** 时间范围天数（可选，默认询问用户确认）

**处理规则：**
- 如果参数为空，提示用户输入UP主名字
- 如果用户只提供了UP主名字，但使用"最近"、"近期"等模糊表述，**必须主动询问**用户需要总结多少天的内容，给出常见选项供选择（例如：1天 / 7天 / 30天）
- 只有当用户明确指定天数时，才使用默认或指定值

### 2. 检查本地缓存

数据保存路径：`~/bili-data/<UP主名字>/<当前日期>/`

- 如果该目录已存在，询问用户是否需要重新获取还是直接使用缓存
- 如果用户选择不更新，跳过数据获取直接读取缓存

### 3. 执行数据获取脚本

运行脚本获取原始数据：

```bash
python3 "$SKILL_DIR/scripts/fetch_bili_content.py" "<UP主名字>" <天数>
```

如果 `$SKILL_DIR` 环境变量不可用，先通过 Bash 获取项目根目录，再拼接路径：
```bash
# 获取当前工作目录作为项目根目录
PROJECT_ROOT="$(pwd)"
python3 "$PROJECT_ROOT/.claude/skills/bili-summary/scripts/fetch_bili_content.py" "<UP主名字>" <天数>
```

**脚本自动完成：**
1. 搜索UP主，精确匹配优先，定位UID
2. 获取多页动态列表，按时间过滤
3. 逐条获取动态详情（文字/图文内容）
4. 对视频类动态，自动提取字幕文本
5. 生成合并文件：`~/bili-data/<UP主名字>/<日期>/combined.md`

### 4. 读取合并内容

- 先通过 Bash 执行 `echo $HOME` 获取用户主目录绝对路径（Read 工具不支持 `~`）
- 使用 Read 工具读取 `$HOME/bili-data/<UP主名字>/<当前日期>/combined.md`（替换为实际绝对路径）
- 如果文件超过 2000 行，使用 offset/limit 参数分段读取避免上下文溢出

### 5. 生成结构化总结

**必须使用以下输出格式：**

```markdown
## <UP主名字> 近 N 天动态总结

### 基本信息
- UID / 主页链接
- 时间范围 / 动态数量

### 动态概览
- 总条数、类型分布（文字/图文/转发/视频）
- 活跃度评估

### 核心内容摘要
按时间顺序，提炼每条动态的关键信息：
- 重要观点和思路
- 关键数据和结论
- 推荐/提及的标的或话题

### 视频内容要点
对有字幕的视频逐一进行详细摘要：
- 视频主题
- 核心论点
- 关键数据和结论

### 总体评价
- 近期关注重点
- 内容倾向

---

原始数据已保存至：`~/bili-data/<UP主名字>/<日期>/`
```

### 6. 生成可视化 HTML（可选）

输出结构化总结后，**必须询问用户**：
> 是否需要生成苹果风格（Liquid Glass）可视化 HTML 页面方便浏览？输出路径：`output/<UP主名字>-summary.html`

如果用户确认：
1. **先读取 HTML 模板**：使用 Read 工具读取 `$SKILL_DIR/templates/bili-summary-tmp.html`（如果 `$SKILL_DIR` 不可用，使用 `$PROJECT_ROOT/.claude/skills/bili-summary/templates/bili-summary-tmp.html`）
2. **基于模板生成 HTML**：严格复用模板中的 CSS 变量体系、class 命名规范和组件结构（如 `.glass`、`.hero`、`.stat-card`、`.section-title`、`.bullet-list`、`.quote-block`、`.dark-block`、`.eval-grid`、`.target-grid`、`.apple-table` 等），将结构化总结内容填充到模板的 `{{{content_sections}}}` 区域
3. **调用 apple skill 增强**（可选）：如果内容中有特别适合可视化的数据（如对比图表、趋势分析），可以调用 `apple-style-page-builder:apple-style-page-ppt-builder-plus` skill 生成额外的可视化组件，但必须确保生成的组件与模板的 CSS 变量体系和设计风格一致
4. **输出路径**：`output/<UP主名字>-summary.html`
5. 生成完成后用浏览器打开并告知用户输出路径

**重要**：模板中的 CSS 和 HTML 结构是基准，生成时必须优先遵循模板风格，不要另起炉灶写全新的 CSS。模板提供了完整的组件库（玻璃卡片、数据表格、引用块、深色块、评估网格等），直接组合使用即可。

## 注意事项

1. **语言：** 总结必须以**中文**输出
2. **客观性：** 保持客观，如实反映UP主表达的观点，不要添加自己的判断
3. **错误处理：** 如果脚本执行失败，显示错误输出并给出排查建议（如检查opencli是否安装、网络连接）
4. **提炼：** 抓住核心观点，避免冗长摘抄，保持总结简洁清晰
5. **HTML生成：** 生成HTML前需要询问用户确认，不要默认生成
