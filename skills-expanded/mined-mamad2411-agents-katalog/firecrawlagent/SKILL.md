# Cursor AI 规则 - FireShot 项目（Firecrawl 专项）

> **项目**: FireShot - Firecrawl 云 API 最佳实践和 HawaiiHub 数据采集 **更新时间**: 2025-10-27
> **维护者**: HawaiiHub AI Team

---

## 🌐 语言要求

- **所有输出必须使用简体中文**（代码注释、文档、日志、提示信息）
- 英文仅用于：代码变量名、函数名、类名、包名
- 文档中的技术术语可保留英文（如 Firecrawl、MCP、API）

---

## 🔥 Firecrawl 核心原则

### 1. 工具选择优先级（从高到低）

```python
# ✅ P0: 优先使用 MCP 工具（最简单、最可靠）
result = mcp_firecrawl_firecrawl_scrape(
    url="https://example.com",
    formats=["markdown"],
    onlyMainContent=True  # ⚠️ MCP 工具使用驼峰式
)

# ✅ P1: Python SDK v2（需要更多控制时）
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
result = app.scrape(url, formats=["markdown"], only_main_content=True)  # ⚠️ SDK 使用下划线
# 访问结果：result.markdown（属性），不是 result.get("markdown")

# ❌ 避免: 直接使用 requests + BeautifulSoup（不稳定）
```

**选择决策树**：

- 复杂页面（大量JS、动态加载）→ **MCP 工具**
- 批量爬取（已知 URL 列表）→ **Python SDK batch_scrape**
- 整站爬取 → **Python SDK crawl**
- 搜索 + 爬取 → **Python SDK search**

### 2. 必须遵守的配置规范

```python
# ✅ 正确：使用环境变量
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FIRECRAWL_API_KEY")

# ❌ 错误：硬编码 API 密钥
api_key = "fc-xxxx"  # 永远不要这样做！
```

**环境变量清单**：

```bash
# 必需
FIRECRAWL_API_KEY=fc-xxx

# 推荐（密钥轮换）
FIRECRAWL_API_KEY_BACKUP_1=fc-xxx
FIRECRAWL_API_KEY_BACKUP_2=fc-xxx
FIRECRAWL_API_KEY_BACKUP_3=fc-xxx

# 可选（成本控制）
FIRECRAWL_DAILY_BUDGET=10.0
FIRECRAWL_TIMEOUT=60
```

### 3. 错误处理模式（强制）

```python
# ✅ 正确：完整的错误处理
def safe_scrape(url: str, max_retries: int = 3) -> dict | None:
    """安全爬取，带重试和日志"""
    for attempt in range(max_retries):
        try:
            result = app.scrape(url, formats=["markdown"], only_main_content=True)

            # 验证结果
            if not result or not hasattr(result, "markdown"):
                raise ValueError("返回结果无效")

            logging.info(f"成功爬取: {url}")
            return result

        except RequestTimeoutError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                logging.warning(f"超时，{wait_time}秒后重试... ({attempt+1}/{max_retries})")
                time.sleep(wait_time)
            else:
                logging.error(f"失败（{max_retries}次重试后）: {url} - {e}")
                return None
        except Exception as e:
            logging.error(f"未知错误: {url} - {e}")
            return None

# ❌ 错误：没有错误处理
result = app.scrape(url)  # 可能崩溃
```

### 4. 性能优化（必须）

```python
# ✅ 使用缓存（节省成本 50%+）
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def cached_scrape(url: str) -> str:
    """带缓存的爬取（1小时有效期）"""
    cache_key = f"firecrawl:{url}"

    # 检查 Redis 缓存
    cached = redis_client.get(cache_key)
    if cached:
        return cached

    # 爬取新数据
    result = app.scrape(url, formats=["markdown"], only_main_content=True)
    content = result.markdown

    # 存入缓存（1小时）
    redis_client.setex(cache_key, 3600, content)
    return content

# ✅ 批量爬取（更高效）
urls = ["url1", "url2", "url3"]
results = app.batch_scrape(urls, formats=["markdown"])  # 并发处理

# ❌ 错误：逐个爬取（慢 + 贵）
for url in urls:
    result = app.scrape(url)  # 串行处理
```

---

## 🐍 Python 代码规范

### 1. 类型注解（强制）

```python
# ✅ 正确：所有函数必须有类型注解
from typing import Optional, Dict, List

def scrape_news(
    url: str,
    formats: List[str] = ["markdown"],
    timeout: int = 60
) -> Optional[Dict[str, str]]:
    """
    爬取新闻内容

    Args:
        url: 新闻 URL
        formats: 返回格式列表
        timeout: 超时时间（秒）

    Returns:
        包含 markdown、html 等内容的字典，失败返回 None
    """
    # ... 实现
    return {"markdown": content}

# ❌ 错误：缺少类型注解
def scrape_news(url, formats=["markdown"]):
    return {"markdown": content}
```

### 2. 文档字符串（强制，中文）

```python
# ✅ 正确：完整的中文 docstring
def analyze_articles(articles: List[Dict]) -> Dict[str, int]:
    """
    分析文章数据统计信息

    统计内容：
    - 作者分布
    - 发布时间分布
    - 热门关键词

    Args:
        articles: 文章列表，每个文章包含 title、author、date 等字段

    Returns:
        统计结果字典，包含：
        - total_articles: 总文章数
        - authors: 作者统计 {作者名: 文章数}
        - keywords: 关键词统计 {关键词: 出现次数}

    Example:
        >>> articles = [{"title": "测试", "author": "张三", "date": "2025-10-27"}]
        >>> stats = analyze_articles(articles)
        >>> print(stats["total_articles"])
        1
    """
    # ... 实现
```

### 3. 代码风格（基于 Ruff）

```python
# ✅ 使用双引号（项目标准）
message = "爬取成功"
url = "https://example.com"

# ✅ 导入顺序：标准库 → 第三方库 → 本地模块
import json
import re
from datetime import datetime
from collections import defaultdict

from firecrawl import FirecrawlApp
from dotenv import load_dotenv

from .utils import parse_date
from .config import FIRECRAWL_API_KEY

# ✅ 格式化：使用 Black/Ruff
# 每行最多 88 字符
# 函数间空 2 行
# 类定义间空 2 行

# ✅ 命名规范
class ArticleScraper:  # 类名：大驼峰
    def __init__(self):
        self.api_key = ""  # 实例变量：snake_case

    def scrape_article(self) -> str:  # 方法名：snake_case
        return ""

FIRECRAWL_API_URL = "https://api.firecrawl.dev"  # 常量：大写+下划线
```

### 4. 测试要求（使用 pytest）

```python
# ✅ 测试文件：tests/test_scraper.py
import pytest
from unittest.mock import Mock, patch

def test_scrape_success():
    """测试：成功爬取文章"""
    # Arrange
    mock_result = Mock()
    mock_result.markdown = "# 测试文章"

    # Act
    with patch("firecrawl.FirecrawlApp.scrape", return_value=mock_result):
        result = scrape_news("https://test.com")

    # Assert
    assert result is not None
    assert "markdown" in result
    assert result["markdown"] == "# 测试文章"

def test_scrape_timeout():
    """测试：超时重试机制"""
    with patch("firecrawl.FirecrawlApp.scrape", side_effect=RequestTimeoutError):
        result = safe_scrape("https://test.com", max_retries=2)

    assert result is None

# ❌ 不使用 unittest
# ❌ 测试必须有 docstring
```

---

## 📊 数据处理规范

### 1. 数据保存格式

```python
# ✅ 必须保存 3 种格式（三角互验）
def save_scraped_data(content: str, metadata: Dict) -> None:
    """保存爬取的数据到多种格式"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. 原始 Markdown（人类可读）
    with open(f"raw_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(f"# 爬取数据\n\n")
        f.write(f"> 时间: {datetime.now()}\n\n")
        f.write(content)

    # 2. 结构化 JSON（程序处理）
    with open(f"data_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump({
            "content": content,
            "metadata": metadata,
            "scraped_at": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)

    # 3. CSV（分析工具）
    with open(f"data_{timestamp}.csv", "w", encoding="utf-8") as f:
        # ... CSV 导出逻辑
```

### 2. 数据验证

```python
# ✅ 使用 Pydantic 验证数据
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class Article(BaseModel):
    """文章数据模型"""
    title: str = Field(..., min_length=1, max_length=200)
    url: HttpUrl
    author: str
    date: str  # ISO 8601 格式
    content: Optional[str] = None

    class Config:
        # 允许额外字段
        extra = "allow"

# 使用
try:
    article = Article(
        title="测试文章",
        url="https://example.com",
        author="张三",
        date="2025-10-27"
    )
except ValidationError as e:
    logging.error(f"数据验证失败: {e}")
```

---

## 💰 成本控制规范

### 1. 请求计数和预算监控

```python
# ✅ 实现请求计数器
class FirecrawlClient:
    """Firecrawl 客户端（带成本控制）"""

    def __init__(self, api_key: str, daily_budget: float = 10.0):
        self.app = FirecrawlApp(api_key=api_key)
        self.daily_budget = daily_budget
        self.request_count = 0
        self.total_cost = 0.0

    def scrape(self, url: str, **kwargs) -> dict:
        """爬取并记录成本"""
        # 检查预算
        if self.total_cost >= self.daily_budget:
            raise BudgetExceededError(f"超出每日预算: ${self.daily_budget}")

        # 执行爬取
        result = self.app.scrape(url, **kwargs)

        # 记录成本（假设 $0.01/请求）
        cost = 0.01
        self.request_count += 1
        self.total_cost += cost

        logging.info(
            f"请求 #{self.request_count} | "
            f"成本: ${cost:.4f} | "
            f"累计: ${self.total_cost:.2f}/{self.daily_budget}"
        )

        return result
```

### 2. 密钥轮换

```python
# ✅ 自动密钥轮换（突破速率限制）
import itertools

class RotatingFirecrawlClient:
    """支持密钥轮换的客户端"""

    def __init__(self, api_keys: List[str]):
        self.api_keys = itertools.cycle(api_keys)  # 循环使用
        self.current_key = next(self.api_keys)
        self.app = FirecrawlApp(api_key=self.current_key)

    def scrape(self, url: str, **kwargs) -> dict:
        """爬取（失败自动切换密钥）"""
        try:
            return self.app.scrape(url, **kwargs)
        except RateLimitError:
            # 切换到下一个密钥
            self.current_key = next(self.api_keys)
            self.app = FirecrawlApp(api_key=self.current_key)
            logging.info(f"切换密钥: {self.current_key[:10]}...")
            return self.app.scrape(url, **kwargs)

# 使用
client = RotatingFirecrawlClient([
    os.getenv("FIRECRAWL_API_KEY"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_1"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_2"),
    os.getenv("FIRECRAWL_API_KEY_BACKUP_3"),
])
```

---

## 🏗️ 项目结构规范

```
FireShot/
├── .env                          # 环境变量（不提交到 Git）
├── .env.template                 # 环境变量模板
├── .cursorrules                  # 本文件
├── .gitignore                    # Git 忽略文件
│
├── requirements.txt              # Python 依赖
├── pyproject.toml               # 项目配置（使用 uv/poetry）
│
├── docs/                        # 文档
│   ├── FIRECRAWL_CLOUD_API_RULES.md
│   ├── FIRECRAWL_CLOUD_SETUP_GUIDE.md
│   └── SETUP_COMPLETE.md
│
├── scripts/                     # 工具脚本
│   ├── scrape_firecrawl_blog.py
│   ├── analyze_firecrawl_blog.py
│   └── test_api_keys.py
│
├── src/                         # 源代码
│   ├── __init__.py
│   ├── scraper.py              # 爬虫核心逻辑
│   ├── parser.py               # 数据解析
│   ├── storage.py              # 数据存储
│   └── utils.py                # 工具函数
│
├── tests/                       # 测试代码
│   ├── __init__.py
│   ├── test_scraper.py
│   └── test_parser.py
│
├── data/                        # 数据目录
│   ├── raw/                    # 原始数据
│   ├── processed/              # 处理后数据
│   └── cache/                  # 缓存
│
└── logs/                        # 日志文件
    ├── firecrawl.log
    └── errors.log
```

---

## 📝 Git 提交规范

### Conventional Commits（强制）

```bash
# 格式：<类型>(<范围>): <描述>

# ✅ 正确的提交消息
git commit -m "feat(scraper): 添加 Firecrawl MCP 工具支持"
git commit -m "fix(parser): 修复文章日期解析错误"
git commit -m "docs(api): 更新 API 密钥配置指南"
git commit -m "refactor(storage): 优化数据存储格式"
git commit -m "perf(cache): 实现 Redis 缓存机制，节省 50% 成本"

# ❌ 错误的提交消息
git commit -m "更新代码"
git commit -m "fix bug"
```

**类型清单**：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链
- `style`: 代码格式（不影响功能）

---

## 🎯 HawaiiHub 专项规范

### 1. 新闻爬取模板

```python
# ✅ 标准的新闻爬取流程
from typing import List, Dict
import logging

HAWAII_NEWS_SOURCES = [
    "https://www.hawaiinewsnow.com/",
    "https://www.staradvertiser.com/",
    "https://www.civilbeat.org/",
]

def scrape_hawaii_news(sources: List[str]) -> List[Dict]:
    """
    爬取夏威夷新闻

    Args:
        sources: 新闻源 URL 列表

    Returns:
        新闻文章列表
    """
    articles = []

    for source in sources:
        try:
            # 1. 爬取首页
            result = app.scrape(
                url=source,
                formats=["markdown"],
                only_main_content=True  # SDK v2 使用下划线
            )

            # 2. 提取文章链接
            links = extract_article_links(result.markdown)

            # 3. 批量爬取文章内容
            article_results = batch_scrape(links[:10])  # 限制 10 篇

            # 4. 解析和存储
            for article in article_results:
                parsed = parse_news_article(article)
                articles.append(parsed)

            logging.info(f"成功爬取 {source}: {len(article_results)} 篇文章")

        except Exception as e:
            logging.error(f"爬取失败 {source}: {e}")
            continue

    return articles
```

### 2. 数据清洗规范

```python
# ✅ 新闻数据清洗
def clean_news_content(content: str) -> str:
    """
    清洗新闻内容

    移除：
    - 广告
    - 导航栏
    - 相关文章推荐
    - 社交媒体按钮
    """
    # 使用 Firecrawl 的 only_main_content 已经做了基础清洗
    # 这里只需要额外处理

    # 移除特定模式
    patterns_to_remove = [
        r"Subscribe to.*newsletter",
        r"Advertisement",
        r"Related Articles",
        r"Share on.*",
    ]

    for pattern in patterns_to_remove:
        content = re.sub(pattern, "", content, flags=re.IGNORECASE)

    # 规范化空白
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip()
```

---

## 🔧 开发工具配置

### 1. VSCode/Cursor 设置

```json
// .vscode/settings.json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.rulers": [88],
    "editor.tabSize": 4
  }
}
```

### 2. Ruff 配置

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
]

[tool.ruff.format]
quote-style = "double"  # 强制双引号
```

### 3. Pre-commit 钩子

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

---

## 📚 必读文档优先级

### P0（立即阅读）

1. **SDK_CONFIGURATION_COMPLETE.md** - SDK 配置总结（2025-10-27 最新）
2. **FIRECRAWL_CLOUD_SETUP_GUIDE.md** - 10 分钟快速上手
3. **FIRECRAWL_BLOG_SCRAPING_SUMMARY.md** - 实战案例

### P1（本周阅读）

4. **FIRECRAWL_CLOUD_API_RULES.md** - 完整 API 规范
5. **FIRECRAWL_ECOSYSTEM_GUIDE.md** - 生态系统概览
6. **Firecrawl更新日志汇总.md** - v1.0 → v2.4.0 完整演进

---

## 🆕 Firecrawl SDK v2 重要变化（2025-10-27）

### 命名约定变化

```python
# ✅ SDK v2 正确写法（下划线命名）
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],
    only_main_content=True,    # ✅ 下划线
    max_age=172800000,          # ✅ 下划线
    block_ads=True,             # ✅ 下划线
    skip_tls_verification=True, # ✅ 下划线
    remove_base64_images=True   # ✅ 下划线
)

# ❌ 错误写法（驼峰式，v1 旧版本）
result = app.scrape(
    url="https://example.com",
    formats=["markdown"],
    onlyMainContent=True,       # ❌ 驼峰式会报错
    maxAge=172800000,           # ❌ 驼峰式会报错
)
```

### 返回值类型变化

```python
# ✅ SDK v2 正确写法（Document 对象）
result = app.scrape(url="https://example.com", formats=["markdown"])
content = result.markdown       # ✅ 属性访问
title = result.metadata.title   # ✅ 元数据访问
url = result.url                # ✅ URL 访问

# ❌ 错误写法（字典访问，v1 旧版本）
content = result.get("markdown")      # ❌ 会报错：'Document' object has no attribute 'get'
content = result["markdown"]          # ❌ 会报错
```

### 批量爬取返回值

```python
# ✅ 正确处理 batch_scrape 返回值
results = app.batch_scrape(urls=["url1", "url2", "url3"], formats=["markdown"])

for item in results:
    if isinstance(item, tuple):
        success, result = item
        if success:
            print(result.markdown)
    else:
        print(item.markdown)
```

### v2 新功能

1. **默认缓存**: `max_age=172800000`（2天）可节省 50%+ 成本
2. **Summary 格式**: `formats=["summary"]` 直接获取摘要
3. **搜索分类**:
   - `categories=["github"]` - GitHub 搜索
   - `categories=["research"]` - 学术搜索（arXiv、Nature、IEEE、PubMed）
   - `categories=["pdf"]` - PDF 文档搜索
4. **智能爬取**: 传入 prompt 参数自动推导路径和限制

---

## ⚠️ 禁止事项

### 绝对禁止

1. ❌ **硬编码 API 密钥**到代码中
2. ❌ **提交 .env 文件**到 Git
3. ❌ **跳过错误处理**（所有外部调用必须 try-except）
4. ❌ **无限重试**（必须设置 max_retries）
5. ❌ **忽略成本监控**（必须记录每次 API 调用）
6. ❌ **使用单引号**（Python 项目统一双引号）
7. ❌ **缺少类型注解**（所有函数必须有完整类型）
8. ❌ **缺少文档字符串**（所有公开函数/类必须有 docstring）
9. ❌ **生成无用的报告文档**（如 *_REPORT.md、*_COMPLETE.md、*_SUMMARY.md 等）
10. ❌ **创建临时脚本**（除非用户明确要求且有长期维护价值）

### 文档生成规范 📋

**允许更新的文档**：
- `CHANGELOG.md` - 变更日志（必须）
- `README.md` - 项目说明（核心章节更新）
- `.cursor/logs/development/YYYY-MM/YYYY-MM-DD.md` - 开发日志（详细记录）

**禁止创建的文档**：
- ❌ 执行报告（*_EXECUTION_REPORT.md）
- ❌ 完成总结（*_COMPLETE.md、*_SUMMARY.md）
- ❌ 优化报告（**OPTIMIZATION**.md）
- ❌ 测试报告（*_TEST_REPORT.md）
- ❌ 配置报告（**CONFIG**.md）
- ❌ 任何形式的"完成"、"总结"、"报告"类文档

**唯一例外**：用户明确要求"生成XXX报告文档"时才可以创建。

**脚本创建规范**：
- ✅ 允许：长期维护的工具脚本（如 `scripts/cleanup_dependencies.sh`）
- ❌ 禁止：一次性使用的临时脚本
- ❌ 禁止：重复现有功能的脚本
- ❌ 禁止：测试脚本（应使用 pytest）

### 强烈不推荐

1. ⚠️ 不检查缓存直接爬取（浪费成本）
2. ⚠️ 串行处理大量 URL（使用 batch_scrape）
3. ⚠️ 不记录日志（难以调试）
4. ⚠️ 不验证数据格式（使用 Pydantic）
5. ⚠️ 在根目录创建文档（应放在 `docs/` 或 `.cursor/logs/`）

---

## 🎓 最佳实践总结

### 爬取策略

1. **先 Map，后 Crawl/Scrape**

   ```python
   # 1. 发现所有 URL
   urls = app.map(url="https://example.com")

   # 2. 批量爬取
   results = app.batch_scrape(urls['links'][:100])
   ```

2. **使用 Search 发现内容**

   ```python
   # 搜索 + 爬取一步完成
   results = app.search(
       query="夏威夷 华人 餐厅",
       sources=[{"type": "web"}],
       limit=10,
       scrapeOptions={"formats": ["markdown"]}
   )
   ```

3. **合理设置爬取频率**

   ```python
   import time

   for url in urls:
       result = scrape(url)
       time.sleep(1)  # 避免触发速率限制
   ```

### 数据管理

1. **分离原始数据和处理数据**
2. **使用版本控制**（文件名加时间戳）
3. **定期清理缓存**（避免存储爆炸）
4. **备份重要数据**（异地备份）

### 监控告警

1. **成本监控**：每日检查 API 使用量
2. **错误告警**：超时 > 3 次发送 Slack 通知
3. **性能跟踪**：记录平均响应时间

---

## 🚀 快速启动清单

新成员入职时，按顺序执行：

```bash
# 1. 克隆项目
cd /Users/zhiledeng/Downloads/FireShot

# 2. 安装依赖
pip3 install --break-system-packages firecrawl-py python-dotenv requests pydantic

# 3. 配置环境变量
cp env.template .env
# 编辑 .env，填入 API 密钥

# 4. 测试 API 密钥
python3 test_api_keys.py

# 5. 运行示例
python3 quick_start.py

# 6. 阅读文档
cat FIRECRAWL_CLOUD_SETUP_GUIDE.md
cat SETUP_COMPLETE.md

# 7. 开始开发
# 参考 scrape_firecrawl_blog.py 和 analyze_firecrawl_blog.py
```

---

## 📞 获取帮助

### 遇到问题？

1. **查看文档**: `docs/` 目录下的所有 Markdown 文件
2. **运行诊断**: `python3 test_api_keys.py`
3. **查看日志**: `tail -f logs/firecrawl.log`
4. **官方资源**:
   - 文档: https://docs.firecrawl.dev/
   - Discord: https://discord.gg/firecrawl
   - GitHub: https://github.com/mendableai/firecrawl

---

**版本**: v1.0.0 **最后更新**: 2025-10-27 **维护者**: HawaiiHub AI Team **适用项目**: FireShot +
HawaiiHub
