---
name: job-hunter-pro
description: "Professional job hunting automation for Chinese job market. Search, filter, and organize job listings from multiple platforms (Liepin, Zhaopin, LinkedIn, Boss) with intelligent deduplication and structured output."
author: luna-assistant
version: 1.0.0
---

# Job Hunter Pro

> **Professional job hunting automation for the Chinese job market.**

This skill automates the complete job search workflow: multi-platform search, intelligent filtering, company deduplication, and structured output generation.

## 🌟 Features

- **Multi-Platform Search**: Aggregates jobs from Liepin, Zhaopin, LinkedIn, Boss Zhipin, and 51job
- **Smart Filtering**: Location-based filtering (Shanghai downtown only), company type, experience level
- **Intelligent Deduplication**: Real-time company blacklist checking to avoid duplicates
- **Structured Output**: Generates professional CSV/Excel with 11 standardized columns
- **Strict Ratio Control**: Enforces 5-5-5-5 distribution across 4 job categories
- **Browser Automation**: Uses Chrome automation for reliable data extraction

## 🎯 Job Categories (Configurable)

**Default Configuration** (5-5-5-5 Rule):

| Category | Count | Keywords | Priority |
|:---|:---:|:---|:---:|
| **Data Analyst** | 5 | 数据分析师、数据分析专员、商业数据分析 | ⭐⭐⭐⭐⭐ |
| **Trade Specialist** | 5 | 贸易专员、大宗商品交易员、进出口运营 | ⭐⭐⭐⭐ |
| **Foreign Trade** | 5 | 外贸业务员、外贸销售、国际业务专员 | ⭐⭐⭐ |
| **AI/Creative** | 5 | AIGC、AI产品经理、内容运营、漫剧创作 | ⭐⭐⭐ |

**Total**: Exactly 20 jobs per day, strictly 5+5+5+5 distribution

### 🔧 Customizable Categories

Users can define their own job categories in `config.json`:

```json
{
  "job_categories": [
    {
      "name": "数据分析师",
      "count": 5,
      "keywords": ["数据分析师", "数据分析专员", "商业数据分析"],
      "priority": 5
    },
    {
      "name": "产品经理",
      "count": 5,
      "keywords": ["产品经理", "PM", "产品运营"],
      "priority": 4
    },
    {
      "name": "运营专员",
      "count": 5,
      "keywords": ["运营", "新媒体运营", "内容运营"],
      "priority": 3
    },
    {
      "name": "市场营销",
      "count": 5,
      "keywords": ["市场营销", "市场专员", "品牌推广"],
      "priority": 3
    }
  ],
  "total_daily": 20
}
```

**Flexible Distribution**: Users can adjust counts per category (e.g., 8-4-4-4, 10-5-3-2) as long as total = 20

## 📊 Platform Distribution

| Platform | Percentage | Count | URL |
|:---|:---:|:---:|:---|
| 智联招聘 (Zhaopin) | 25% | 5 | zhaopin.com |
| LinkedIn | 25% | 5 | linkedin.com/jobs |
| 猎聘网 (Liepin) | 25% | 5 | liepin.com |
| Boss直聘 + 前程无忧 | 25% | 5 | zhipin.com + 51job.com |

## 🛠️ Tools

### `search_jobs`

Searches for jobs across multiple platforms with intelligent filtering.

**Parameters:**
- `category` (string): Job category name from config
- `count` (number): Number of jobs to find (default: 5)
- `location` (string): Target location (default: "上海市区")
- `exclude_companies` (array): List of companies to exclude
- `verify_links` (boolean): Enable link verification (default: true)

**Example:**
```json
{
  "category": "数据分析师",
  "count": 5,
  "location": "上海市区",
  "exclude_companies": ["Company A", "Company B"],
  "verify_links": true
}
```

**Returns:**
```json
{
  "jobs": [...],
  "verified_count": 5,
  "invalid_count": 0,
  "re_search_count": 0
}
```

### `generate_job_report`

Generates structured Excel report with **clickable hyperlinks** from collected jobs.

**Parameters:**
- `jobs` (array): Array of job objects
- `date` (string): Report date (YYYY-MM-DD)
- `format` (string): "excel" (default, with hyperlinks) or "csv"

**Output Format: Excel with Clickable Links**

✅ **Hyperlink Support**: Job URLs are formatted as clickable hyperlinks in Excel
- Click cell → Opens job page in browser
- Format: `=HYPERLINK("https://...", "点击查看职位")`

**Output Columns:**
1. 排名 (Rank)
2. 职位名称 (Job Title)
3. 公司名称 (Company Name)
4. 公司类型 (Company Type)
5. 地点 (Location)
6. 经验要求 (Experience)
7. 学历要求 (Education)
8. 薪资范围 (Salary Range)
9. **职位链接 (Job URL)** - ✅ **Clickable hyperlink**
10. 匹配度 (Match Percentage)
11. 备注 (Notes)

**Excel Features:**
- ✅ Clickable job links (opens in browser)
- ✅ Auto-filter enabled on all columns
- ✅ Freeze header row
- ✅ Conditional formatting for match percentage
- ✅ Professional styling with borders

### `update_company_blacklist`

Updates the company blacklist with newly found companies.

**Parameters:**
- `companies` (array): List of company names to add

## 📍 Location Filtering

### ✅ Included (Shanghai Downtown)
- **黄浦区、静安区、徐汇区、长宁区**
- **普陀区** (部分)、**虹口区、杨浦区**
- **浦东新区**: 陆家嘴、世纪大道、张江（核心区域）
- **闵行区**: 虹桥、七宝（靠近市区部分）

### ❌ Excluded (Suburbs)
- 嘉定区、青浦区、松江区、奉贤区、金山区
- 宝山区（大部分）、崇明区
- 浦东: 川沙、周浦、南汇、金桥（偏外）
- 闵行: 浦江、莘庄（偏外）

## 🔍 Complete Workflow

### Phase 1: Job Search
```
1. Load configuration (job categories, location, platforms)
2. Load company blacklist from ~/Desktop/求职/已推荐公司清单.txt
3. For each job category:
   a. Search platform with category keywords
   b. Extract job details (title, company, location, salary, URL)
   c. Filter by location (downtown only)
   d. Check company against blacklist
   e. Collect until target count per category
```

### Phase 2: Link Verification ⭐ NEW
```
4. For each collected job:
   a. Extract job URL
   b. Send HTTP HEAD request to verify URL accessibility
   c. Check response status (200 = valid, 404/500 = invalid)
   d. Verify page content contains job details (not error page)
   e. Mark as "✅ Verified" or "❌ Invalid"
   
5. Filter out invalid links:
   - Remove jobs with 404/500 status
   - Remove jobs with redirect to homepage
   - Remove jobs with "position closed" message
   
6. If insufficient valid jobs after filtering:
   - Re-search to fill gaps
   - Target: 20 verified jobs minimum
```

### Phase 3: Report Generation
```
7. Generate Excel report with verified jobs only
8. Format job URLs as clickable hyperlinks
9. Apply styling (filters, conditional formatting)
```

### Phase 4: Delivery
```
10. Update company blacklist with new companies
11. Save Excel to ~/Desktop/求职/
12. Send report to user via Feishu
13. Include summary: "20 jobs found, 18 verified, 2 invalid links filtered"
```

## 🔗 Link Verification Details

### Verification Process

**Step 1: URL Accessibility Check**
```python
# Check if URL is accessible
response = requests.head(job_url, timeout=10, allow_redirects=True)
if response.status_code == 200:
    status = "accessible"
elif response.status_code in [404, 410]:
    status = "job_not_found"
elif response.status_code >= 500:
    status = "server_error"
```

**Step 2: Content Validation**
```python
# Verify page contains actual job content
response = requests.get(job_url, timeout=10)
content = response.text.lower()

# Check for job-related keywords
job_keywords = ["职位", "工作", "薪资", "要求", "经验", "学历"]
if any(keyword in content for keyword in job_keywords):
    content_valid = True
else:
    content_valid = False  # Might be error page or redirect

# Check for "closed" or "expired" indicators
closed_indicators = ["已关闭", "已停止", "已过期", "position closed", "no longer available"]
if any(indicator in content for indicator in closed_indicators):
    job_closed = True
```

**Step 3: Retry Logic**
```python
# If verification fails, retry with full GET request
if not verified:
    response = requests.get(job_url, timeout=15, headers=user_agent)
    # Re-check content
```

### Verification Results

| Status | Meaning | Action |
|:---|:---|:---|
| ✅ **Verified** | Link valid, job active | Include in report |
| ❌ **404/410** | Job not found | Discard, re-search |
| ❌ **500+** | Server error | Retry once, then discard |
| ❌ **Redirect to homepage** | Job expired | Discard, re-search |
| ❌ **Content mismatch** | Not a job page | Discard, re-search |
| ❌ **Job closed** | Position filled | Discard, re-search |

### Quality Guarantee

**Minimum Standard**: 
- 20 jobs searched
- 100% links verified
- ≥18 valid jobs in final report
- If <18 valid: auto re-search to fill gaps

## 📁 File Structure

```
~/Desktop/求职/
├── 已推荐公司清单.txt     # Company blacklist
├── 职位列表_YYYY-MM-DD.xlsx  # Daily job report
├── YourName_Resume_EN.docx   # English resume (rename to your name)
└── YourName_Resume_CN.pdf    # Chinese resume (rename to your name)
```

## 💼 Company Types

- **外企** (Foreign Enterprise)
- **民企** (Private Enterprise)
- **国企** (State-owned Enterprise)
- **上市公司** (Listed Company)

## ⚠️ Important Rules

1. **Strict 5-5-5-5 Distribution**: Never deviate from the ratio
2. **Job URL Required**: Every job must include a valid application link
3. **Location Filter**: Only Shanghai downtown, no suburbs
4. **Real-time Deduplication**: Check blacklist before adding each job
5. **Browser-First**: Use browser automation, not Brave Search API
6. **Daily Limit**: Exactly 20 jobs, no more, no less

## 📦 Installation

```bash
# Using OpenClaw CLI
openclaw install skill https://github.com/your-username/job-hunter-pro

# Or using ClawHub
clawhub install job-hunter-pro
```

## 🔧 Configuration

Create `~/.openclaw/job-hunter-pro/config.json`:

```json
{
  "target_location": "上海市区",
  "daily_target": 20,
  "job_categories": [
    {
      "name": "数据分析师",
      "count": 5,
      "keywords": ["数据分析师", "数据分析专员", "商业数据分析"],
      "priority": 5
    },
    {
      "name": "贸易专员",
      "count": 5,
      "keywords": ["贸易专员", "大宗商品交易员", "进出口运营"],
      "priority": 4
    },
    {
      "name": "外贸业务员",
      "count": 5,
      "keywords": ["外贸业务员", "外贸销售", "国际业务专员"],
      "priority": 3
    },
    {
      "name": "AI创作",
      "count": 5,
      "keywords": ["AIGC", "AI产品经理", "内容运营", "漫剧创作"],
      "priority": 3
    }
  ],
  "platforms": [
    "zhaopin",
    "linkedin",
    "liepin",
    "zhipin",
    "51job"
  ],
  "output_path": "~/Desktop/求职/",
  "blacklist_file": "~/Desktop/求职/已推荐公司清单.txt",
  "excel_settings": {
    "hyperlink_format": "clickable",
    "auto_filter": true,
    "freeze_header": true,
    "conditional_formatting": true
  }
}
```

## 🚀 Usage Examples

### Daily Job Search
```
User: "搜索职位"
Agent: 
  1. Load blacklist
  2. Search 4 categories (5 jobs each)
  3. Generate Excel report
  4. Send via Feishu
```

### Specific Category Search
```
User: "再找5个数据分析师职位"
Agent:
  1. Search data_analyst category
  2. Filter by location
  3. Check blacklist
  4. Return 5 jobs
```

### Generate Report
```
User: "生成昨天的职位报告"
Agent:
  1. Read collected jobs from memory
  2. Generate formatted Excel
  3. Save to ~/Desktop/求职/
```

## 📝 Output Example

**Excel File**: `职位列表_2026-03-15.xlsx`

### 📊 Excel Preview

| 排名 | 职位名称 | 公司名称 | 公司类型 | 地点 | 经验要求 | 学历要求 | 薪资范围 | **职位链接** | 匹配度 | 备注 |
|:---:|:---|:---|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | 数据分析师 | ABC科技 | 外企 | 静安区 | 3-5年 | 本科 | 25-35K | **[点击查看职位](https://www.liepin.com/job/12345.html)** ⬅️ **可点击** | 95% | 匹配度高 |
| 2 | 贸易专员 | XYZ贸易 | 民企 | 黄浦区 | 1-3年 | 本科 | 15-25K | **[点击查看职位](https://www.zhaopin.com/job/67890.html)** ⬅️ **可点击** | 90% | - |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### ✨ Excel Features

✅ **Clickable Hyperlinks**: 
- 职位链接列 = 可点击的超链接
- 点击单元格 → 自动打开浏览器
- 格式：`=HYPERLINK("URL", "点击查看职位")`

✅ **Auto-Filter**: 所有列支持筛选排序
✅ **Freeze Header**: 首行冻结，滚动时可见
✅ **Conditional Formatting**: 匹配度高亮显示
✅ **Professional Styling**: 边框、颜色、字体优化

### 🖱️ 使用方法

1. **打开Excel文件**
2. **点击"职位链接"列**的任意单元格
3. **自动打开浏览器**并跳转到职位详情页
4. **直接投递简历**

## 🔗 Dependencies

- **browser-automation**: For web scraping
- **multi-search-engine**: Fallback search
- **excel-automation**: For report generation
- **feishu-doc**: For sending reports

## 📄 License

MIT License - Free for personal and commercial use.

---

*Optimized for the Chinese job market | Created by Luna Assistant & Gavin Zhang (zhan1250)*

---

## 👥 Contributors

| Role | Name | Contribution |
|:---|:---|:---|
| **Product Owner** | Gavin Zhang (zhan1250) | 需求定义、功能设计、测试验证 |
| **Developer** | Luna Assistant | 技术实现、文档编写、代码优化 |

**Collaboration**: This skill was co-designed through iterative optimization between human insight and AI implementation.