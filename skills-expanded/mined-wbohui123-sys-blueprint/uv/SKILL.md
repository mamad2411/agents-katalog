---
name: uv
description: 为数据处理与辅助程序准备项目内的 Python 环境和第三方依赖。
disable-model-invocation: true
---

# uv

为当前确需 Python 的程序准备可重复使用的依赖环境。办公内容读取使用 markitdown，演示制作使用 ppt；已有专用入口能完成的操作沿用它。

使用已安装的 uv；先用 `uv --version` 确认可用。

## 两种写法

**一次性，库名写命令里：**

```bash
uv run --with pandas,matplotlib python 脚本.py
uv run --with openpyxl python -c "import openpyxl; print(openpyxl.__version__)"
```

**脚本自带依赖（推荐，脚本能单独跑）：**

```python
# /// script
# dependencies = ["pandas", "matplotlib"]
# ///
import pandas as pd
...
```

然后 `uv run 脚本.py`，依赖它自己装。

## 常用库对应什么活

| 要做什么 | 用哪个 |
|---|---|
| 表格、数据清洗 | `pandas` |
| 画图表出 png | `matplotlib` |
| 读写 Excel | `openpyxl` |
| 读写 Word | `python-docx` |
| 拆合 PDF | `pypdf` |

## 坑

- 需要第三方库时，用 uv 或项目已有的 Python 环境，避免依赖系统 Python 的版本和全局包。
- **头一次取一个新库要几秒**，之后有缓存就快了。长活记得走后台任务。
- `--with` 多个库用逗号隔开，**中间不要有空格**。
- App 已将 uv 缓存、下载的 Python 和 matplotlib 配置放在当前项目的可写临时目录；按当前命令环境使用，避免改回用户目录。
