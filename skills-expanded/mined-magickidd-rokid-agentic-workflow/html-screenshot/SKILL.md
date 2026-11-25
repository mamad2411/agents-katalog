---
name: html-screenshot
description: 批量截图 HTML 交互原型页面。使用 Playwright 自动打开 HTML 文件，逐页切换并保存全屏截图。适用于 Pencil 设计稿导出、HTML 原型文档化、UI 页面存档等场景。
---

# HTML 批量截图

## 快速开始

当用户需要批量截图 HTML 页面时：

1. 确认 HTML 文件路径
2. 运行截图脚本
3. 获取输出目录中的截图文件

## 使用方法

```bash
# 进入项目目录
cd path/to/project

# 安装依赖（首次使用）
pip install playwright
playwright install chromium

# 运行截图
python scripts/screenshot_pages.py
```

## 脚本配置

修改脚本顶部的配置项：

```python
HTML_FILE = "P1_配置后台_交互原型.html"  # HTML 文件名
OUTPUT_DIR = "screenshots"               # 输出目录
VIEWPORT_WIDTH = 1440                     # 视口宽度
VIEWPORT_HEIGHT = 900                     # 视口高度
PAGE_NAMES = {                            # 页面映射
    "page-id": "页面名称",
}
```

## 输出格式

截图文件名格式：`{序号}_{页面名称}.png`

示例：
```
screenshots/
├── 01_专属模型训练.png
├── 02_多模态识别训练.png
└── 13_参考资料库.png
```

## 特殊页面处理

对于通过按钮跳转的子页面（如弹窗、编辑页），需要在脚本中特殊处理：

```python
if page_id == "indoor-zone-edit":
    # 先切换到父页面
    nav_item = page.query_selector('.nav-sub[data-page="indoor-loc"]')
    nav_item.click()
    time.sleep(0.5)
    # 点击进入子页面按钮
    edit_btn = page.query_selector('button[onclick="enterZoneEdit()"]')
    edit_btn.click()
    time.sleep(0.5)
```

## 依赖安装

```bash
# 安装 Playwright
pip install playwright

# 安装 Chromium 浏览器
playwright install chromium

# 验证安装
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 页面找不到 | 检查 HTML 中的元素选择器是否正确 |
| 截图空白 | 增加等待时间 `time.sleep(0.5)` |
| 视口过小 | 调整 `VIEWPORT_WIDTH` 和 `VIEWPORT_HEIGHT` |
| 字体显示异常 | 确保 HTML 文件编码为 UTF-8 |

## 进阶用法

### 自定义截图区域

```python
# 截取指定元素
element = page.query_selector('.content')
element.screenshot(path="element.png")
```

### 滚动截取长页面

```python
# 滚动并拼接截图
page.screenshot(full_page=True)
```

## 详细文档

- 脚本配置说明：见 [README.md](README.md)
- 脚本源码：见 [scripts/screenshot_pages.py](scripts/screenshot_pages.py)
