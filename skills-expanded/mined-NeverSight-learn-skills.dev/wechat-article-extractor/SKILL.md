---
name: wechat-article-extractor
description: 从微信公众号文章链接中提取完整正文内容、识别图片中的文字和表格。当用户提供微信公众号文章链接（mp.weixin.qq.com），或网页链接中包含微信文章跳转时触发。适用于爬取微信文章内容、提取招聘表格、获取图文资讯等场景。不适用于纯文字问答、与微信内容无关的任务。
---

# 微信公众号文章提取器

## 概述

从微信公众号文章（mp.weixin.qq.com）中提取完整的正文内容，并对文中的图片进行文字识别，特别是包含表格和关键信息的图片。

## 工作流程

微信公众号文章提取分三个阶段：**定位文章链接 → 提取正文文字 → 识别图片内容**。按顺序执行，前一阶段完成后进入下一阶段。

### 第一阶段：定位文章链接

**场景A：用户直接提供了mp.weixin.qq.com链接**

直接进入第二阶段。

**场景B：用户提供了学校官网/学院新闻页面，需要从中找到目标文章链接**

用shell执行以下命令，从新闻列表页中提取目标文章的微信链接：

```bash
curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "新闻列表页URL" 2>/dev/null | grep -i "关键词" | grep -oP 'href="[^"]*"' | head -5
```

关键词用文章标题中的特征词替换。grep -oP会提取包含微信链接的href属性。

### 第二阶段：提取正文文字

用fetch工具获取微信文章的正文内容：

```
fetch(type="url", id="https://mp.weixin.qq.com/s/xxx", question="获取这篇微信公众号文章的完整正文内容，所有段落文字")
```

这会返回文章的标题、作者、发布时间、以及全部段落文字。

**关键判断**：检查返回的正文中，是否存在内容缺失的段落。例如招聘文章中的"招聘计划"章节如果正文中没有对应文字，说明该部分信息以图片形式呈现，需要进入第三阶段。

### 第三阶段：图片内容识别

如果正文完整（所有章节都有对应文字），跳过此阶段。否则执行以下流程。

**步骤1：下载文章中的图片**

先用shell下载原始HTML，然后提取图片URL：

```bash
curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "微信文章URL" 2>/dev/null > /sandbox/workspace/wechat_article_raw.html

python3 << 'PYEOF'
import re, html
with open('/sandbox/workspace/wechat_article_raw.html', 'r', encoding='utf-8') as f:
    content = f.read()
imgs = re.findall(r'data-src="(https://mmbiz[^"]*)"', content)
for i, url in enumerate(imgs):
    print(f"{i+1}: {html.unescape(url)}")
PYEOF
```

**步骤2：下载图片到本地**

```bash
mkdir -p /sandbox/workspace/wechat_imgs
cd /sandbox/workspace/wechat_imgs
curl -s -L -A "Mozilla/5.0" -o "img_1.png" "图片URL1"
curl -s -L -A "Mozilla/5.0" -o "img_2.png" "图片URL2"
# ... 依次下载
```

**步骤3：用fetch工具识别图片内容（核心方法）**

**不要使用tesseract、easyocr、paddleocr等传统OCR工具。** 平台内置的视觉识别能力对中文表格的识别效果远优于它们。

```
fetch(type="file_path", id="/sandbox/workspace/wechat_imgs/img_N.png", question="这是一张表格图片，请完整识别出表格中的所有文字内容，包括每一行每一列的内容，保持表格结构")
```

对于非表格图片，question改为："这张图片的内容是什么？请描述"

**步骤4：整合输出**

将正文文字与图片识别结果整合，形成完整的文章内容。对于表格，用Markdown表格格式输出。

## 关键经验

1. **磁盘空间有限**：sandbox磁盘仅约1.1G，不要尝试安装easyocr、paddleocr等大型OCR包，会因空间不足而失败。

2. **tesseract效果差**：即使安装了tesseract-ocr-chi-sim，对低分辨率中文表格的识别错误率极高，不浪费时间尝试。

3. **fetch视觉识别是最佳方案**：将图片下载到本地后，用fetch(file_path)读取，平台的视觉能力可以完整还原中文表格的结构和内容。这是经过实战验证的最优方法。

4. **图片URL格式**：微信图片URL中，路径含`/640`表示压缩版，`/0`表示原图质量。但有时尺寸相同，不需要刻意替换。

5. **图片数量**：微信文章通常包含5-15张图片，其中大部分是装饰性的（分隔线、标题背景、公众号二维码）。真正包含文字信息的图片通常是招聘表格、数据图表等，优先识别这些。

6. **curl必须带User-Agent**：访问微信文章HTML时，必须设置User-Agent为浏览器格式，否则可能返回空内容或被拦截。

7. **data-src属性**：微信文章的图片URL存储在img标签的data-src属性中，不是src属性。用grep或正则提取时注意这一点。

8. **正文完整性判断**：fetch获取的正文可能缺失部分章节（该章节内容为图片时），需要人工判断哪些章节缺少内容，再针对性识别图片。

## 完整示例

以下是从学院新闻页定位文章、提取正文、识别表格图片的完整执行流程：

**输入**：用户要求读取 `https://law.xtu.edu.cn/c1/xwzx1.htm` 中《"南方法学明珠"欢迎您 诚聘海内外英才加盟》这篇

**执行步骤**：

1. `shell`: curl获取列表页HTML，grep提取目标文章的微信链接
2. `fetch(type="url")`: 获取微信文章正文
3. 发现"03 招聘计划与要求"和"04 引进待遇"章节正文缺失内容
4. `shell`: 下载HTML，提取图片URL，下载10张图片到本地
5. `fetch(type="file_path")`: 对img_7.png（招聘计划表）和img_8.png（待遇表）执行视觉识别
6. 整合输出：正文 + 两张表格的Markdown格式内容

**输出**：完整的文章文字内容 + 招聘计划表格 + 引进待遇表格
