---
name: find-repo
description: GitHub仓库搜索与筛选工具。用于：(1) 根据需求在GitHub上搜索合适的开源仓库 (2) 按star数量排序筛选高质量项目 (3) 验证仓库活跃度和README内容 (4) 给出推荐评分和使用建议。当用户说"找仓库"、"搜索GitHub"、"推荐开源项目"时使用此skill。
---

# GitHub仓库搜索与筛选指南

## 概述

帮助用户在GitHub上找到最合适的开源项目。

## 搜索策略

### 第一步：生成搜索关键词

将用户需求拆分为 **6 个英文关键词**：
- **3 个通用词**：只描述功能，没有任何筛选限制
- **3 个限定词**：功能 + 用户特征 + API/离线/免费等

**普通搜索示例**：
用户说"Python Reddit 爬虫，要官方API"

**普通搜索词**：
- "reddit scraper"        ✓ 功能角度：scraper
- "reddit crawler"        ✓ 功能角度（同类词）
- "reddit data extraction" ✓ 广义角度：数据提取

**限定搜索词**：
- "reddit scraper without api"        ✓ Reddit + 无API
- "reddit unofficial api"             ✓ Reddit + 非官方API
- "reddit scraping no auth"           ✓ 爬取 + 无需认证

---

**示例2**：用户说"PDF 发票自动识别提取，需要中文识别能力"

**普通搜索词**：
- "invoice ocr"                       ✓ 功能角度：发票OCR
- "pdf document parsing"              ✓ 功能角度：PDF文档解析
- "receipt recognition"               ✓ 广义角度：收据识别

**限定搜索词**：
- "invoice ocr chinese"               ✓ 发票OCR + 中文
- "pdf table extraction asia"         ✓ PDF表格提取 + 亚洲
- "receipt scanner multilingual"      ✓ 收据扫描 + 多语言

---

### 第二步：执行搜索命令

对每个关键词执行搜索：

```bash
gh search repos "{关键词}" --sort=stars --limit=5 --json name,fullName,url,description,stargazersCount,updatedAt,language,license
```

如果需要指定语言，加 `--language` 参数

### 第三步：去重 + 按star排序

把6个关键词的结果合并去重，**按star数量降序排列**。

**筛选原则**：
- 先找5个以上star明确更高的仓库（高质量项目）
- star 100-499 的前15个是备选项目
- star < 100 的前10个是可选

**停止条件**（防止无限搜索）：
- 连续找到 5 个完全符合的仓库
- 连续搜索 25 个仓库仍未找到足够匹配的
- 已被筛选排除的仓库

**验证原理**：
- ❓ 表示"description 没写XX功能，可能不行"
- ✅ 表示"虽然 description 没法，但star很高，需读README验证"

**对每个候选仓库执行**：

1. 获取仓库信息：
```bash
gh api repos/{owner}/{repo} --jq '{stars: .stargazers_count, forks: .forks_count, open_issues: .open_issues_count, updated: .updated_at, created: .created_at, license: .license.spdx_id, archived: .archived, description: .description, topics: .topics, clone_url: .clone_url, homepage: .homepage}'
```

2. **读取 README** 验证功能匹配：

```bash
gh api repos/{owner}/{repo}/readme --jq '.content' 2>/dev/null | base64 -d 2>/dev/null
```

如果 README 数据过大，只取前 200 行进行判断

3. **检查提交活跃度**：

```bash
gh api repos/{owner}/{repo}/commits --jq '.[0:5] | .[] | {date: .commit.author.date, message: .commit.message}' 2>/dev/null
```

**判断逻辑**：
- 从star最高的开始读 README
- 记录匹配状态：❓ 不确定 / ⚠️ 部分匹配 / ✅ 明确匹配
- 连续找到 5 个明确匹配的仓库后停止搜索
- 如果搜索超过 25 个仍未找到足够匹配的，停止搜索

### 第四步：综合评分

对筛选出的仓库，按维度打分（每项1-5分）：

1. **Star数**：
   - 5k+ = 5分
   - 2k+ = 4分
   - 1k+ = 3分
   - 500+ = 2分
   - 100+ = 1分

2. **活跃度**：
   - 3个月内更新 = 5分
   - 6个月内更新 = 4分
   - 1年内更新 = 3分
   - 2年内更新 = 2分
   - 2年+ = 1分

3. **License友好度**：
   - MIT/Apache/BSD = 5分
   - LGPL = 3分
   - GPL = 2分
   - 无license = 1分

4. **README匹配度**（从README内容判断）：
   - 5分：README明确说了做XX功能，非常适合
   - 4分：README说了做XX功能，比较适合
   - 3分：需要查看功能确认是否满足
   - 2分：README模板化的不确定是否满足
   - 1分：明确不满足

5. **综合指标**：结合 forks、open issues 判断是否 archived

### 输出格式

搜索完成后，给出推荐仓库的信息卡片（每项1-5分）：

---

**推荐仓库**

仓库: owner/repo
链接: https://github.com/owner/repo
Clone: git clone https://github.com/owner/repo.git
Star: xxx
语言: Python / TypeScript / ...
License: MIT / Apache 2.0 / ...
活跃度: xx天前
总分: xx / 25

README 摘要：
[ 2-3句话说明这个项目是做什么的，主要功能是什么 ]

仓库颜色：
- 🟢绿色1：不同功能导向的仓库
- 🟡黄色2：功能接近但侧重点不同的
- 🔴红色3：不推荐/动态/停更/

注意事项：
[ 需要注意的点（语言难度、学习成本等），根据用户说的来 ]

---

## 注意事项

- 关键词一定要用英文
- 如果某一行关键词执行失败，跳过继续
- 推荐仓库选择 6 个最新的仓库
- 如果用户没指定语言，默认不限语言
- 仓库不要太多，根据用户给的关键词精细化搜索
- README 摘要要简洁，说明这个项目做什么的
- Clone URL 确保是可直接使用的
- 仓库颜色要由 README 内容决定，不要乱加

## 使用示例

用户输入："找一个将Word转PDF的工具，需要支持批量转换"

按上述流程执行，最终输出推荐仓库卡片。
