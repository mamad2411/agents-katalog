---
name: file-to-markdown
description: 将 raw 文件夹中的文件（PDF、Word、JPG 等）自动转换为 Markdown 格式并保存到 wiki 文件夹。优先使用免费的 markitdown，失败时可选使用智谱付费 API。
user_invocable: true
---

# File to Markdown 转换工具

## 功能说明

此 skill 用于将 `raw` 文件夹中的文件自动转换为 Markdown 格式，并保存到 `wiki` 文件夹中。

## 支持的文件格式

- PDF 文档
- Word 文档
- Excel 表格
- PPT 演示文稿
- 图片文件
- 其他 markitdown 支持的格式

## 使用方法

### 方式 1：手动调用

```
/file-to-markdown [文件名]
```

- 不指定文件名时，会处理 raw 文件夹中所有未转换的文件
- 指定文件名时，只处理该文件

### 方式 2：自动监控（推荐）

**完全自动化！** 启动后台服务，自动监控 raw 文件夹：

```bash
# 启动自动转换服务
bash .claude/skills/file-to-markdown/start_auto_convert.sh
```

- ✅ 自动检测新文件
- ✅ 自动转换
- ✅ 自动保存到 wiki 文件夹
- ✅ 支持 macOS 系统通知

详细配置请查看 [AUTO_CONVERT_GUIDE.md](./AUTO_CONVERT_GUIDE.md)

### 方式 3：对话启动监控（最简单）⭐

**直接告诉 Claude，自动启动监控服务！**

当用户说以下内容时，**自动启动监控服务**：
- "启动自动监控"、"开启自动转换"
- "自动监控 raw 文件夹"
- "开始监控文件"
- "启用自动转换"
- "让文件自动转换"

**Claude 会自动**：
1. 启动后台监控服务
2. 告诉你服务已启动
3. 显示监控状态

### 方式 4：手动触发

当用户说以下内容时，**手动转换文件**：
- "转换文件"、"解析文件"
- "处理 raw 文件夹"
- "生成 markdown"
- "把 PDF 转成 Markdown"

## 转换流程

1. **检测文件**：扫描 raw 文件夹中的文件
2. **markitdown 转换**：优先使用开源的 markitdown 库进行转换
3. **智谱 API（可选）**：如果 markitdown 失败或效果不佳，询问用户是否使用智谱付费 API
4. **保存结果**：将转换后的 Markdown 保存到 wiki 文件夹

## 智谱 API 成本说明

如果 markitdown 转换失败，可选择使用智谱 API，成本如下（按优先级排序）：

| 服务类型 | 适用场景 | 价格 |
|---------|---------|------|
| Lite | 简单文档，仅文本 | 当前免费（2025-10-08 后 0.01元/次） |
| OCR | 仅图片文件 | 0.01元/次 |
| Expert | PDF 文档，高精度 | 0.012元/页 |
| Prime | 复杂排版，图文混排 | 0.12元/页 |

**注意**：使用智谱 API 前需要确认，并在 `.env` 文件中配置 `ZHIPU_API_KEY`。

## 执行步骤

### ⚡ 快速判断：用户意图

首先判断用户的意图：

**如果用户提到以下关键词**：
- "启动监控"、"开启监控"、"自动监控"
- "开始监控"、"启用自动转换"
- "让文件自动转换"、"自动转换"

**→ 执行自动监控启动流程**（见下方"自动监控流程"）

**否则**：
- **→ 执行手动转换流程**（见下方"手动转换流程"）

---

### 🤖 自动监控流程

当用户要求启动监控时，按以下步骤执行：

#### 步骤 1：检查依赖

```bash
# 检查并安装 watchdog
python3 -c "import watchdog" 2>/dev/null || pip3 install -q watchdog

# 检查并安装 markitdown[all]
python3 -c "from markitdown import MarkItDown" 2>/dev/null || pip3 install -q 'markitdown[all]'
```

#### 步骤 2：启动监控服务

```bash
# 使用 Bash 工具运行（后台模式）
cd "/Users/wangzf/Desktop/法律AI/法律知识库"
nohup python3 .claude/skills/file-to-markdown/auto_converter.py > .claude/skills/file-to-markdown/auto_convert.log 2>&1 &
```

#### 步骤 3：确认服务启动

```bash
# 检查服务是否启动成功
ps aux | grep auto_converter.py | grep -v grep
```

#### 步骤 4：告知用户

告诉用户：
```
✅ 自动监控服务已启动！

📁 监控目录: /Users/wangzf/Desktop/法律AI/法律知识库/raw
📝 输出目录: /Users/wangzf/Desktop/法律AI/法律知识库/wiki
📊 日志文件: .claude/skills/file-to-markdown/auto_convert.log

现在你可以：
1. 把文件放入 raw 文件夹，会自动转换
2. 在 wiki 文件夹查看转换结果
3. 收到 macOS 系统通知

查看实时日志：
tail -f .claude/skills/file-to-markdown/auto_convert.log

停止服务：
ps aux | grep auto_converter | grep -v grep | awk '{print $2}' | xargs kill
```

---

### 📄 手动转换流程

### 步骤 1：检查依赖

首先检查并安装必要的依赖：

```bash
pip install markitdown
pip install zhipuai  # 可选，用于智谱 API
```

#### 步骤 2：扫描文件

扫描 raw 文件夹，找出需要转换的文件：

```python
import os

raw_dir = "raw"
wiki_dir = "wiki"

# 获取所有待转换文件
files_to_convert = []
for file in os.listdir(raw_dir):
    if file.startswith('.'):
        continue
    raw_path = os.path.join(raw_dir, file)
    wiki_path = os.path.join(wiki_dir, os.path.splitext(file)[0] + '.md')
    if not os.path.exists(wiki_path):
        files_to_convert.append(file)
```

#### 步骤 3：使用 markitdown 转换

对每个文件尝试使用 markitdown 转换：

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("raw/example.pdf")
markdown_content = result.text_content
```

#### 步骤 4：处理转换失败

如果 markitdown 转换失败或效果不佳：
1. 告知用户具体问题
2. 展示智谱 API 的选项和价格
3. **必须等待用户确认**后才能调用付费接口

#### 步骤 5：保存结果

将转换成功的内容保存到 wiki 文件夹：

```python
output_path = os.path.join("wiki", base_name + ".md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(markdown_content)
```

## 配置要求

### 环境变量

如需使用智谱 API，请在项目根目录创建 `.env` 文件：

```
ZHIPU_API_KEY=your_api_key_here
```

### API Key 获取

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册并登录
3. 在 API Keys 页面创建新的 API Key

## 注意事项

1. **付费接口确认**：调用智谱 API 前必须获得用户明确确认
2. **成本优先**：优先使用免费或低成本的接口
3. **文件覆盖**：如果 wiki 文件夹中已存在同名文件，会询问是否覆盖
4. **大文件处理**：超过 100MB 的文件可能需要较长时间处理

## 示例对话

**用户**：转换 raw 文件夹中的所有文件

**助手**：
1. 检查到 raw 文件夹中有 3 个文件待转换
2. 正在使用 markitdown 转换...
3. 2 个文件转换成功
4. 1 个文件（complex.pdf）markitdown 转换效果不佳
5. 是否使用智谱 API 转换 complex.pdf？
   - Lite（免费）：适合简单文档
   - Expert（0.012元/页）：适合 PDF
   - Prime（0.12元/页）：适合复杂排版

**用户**：使用 Expert

**助手**：正在调用智谱 Expert API... 转换成功，已保存到 wiki/complex.md
