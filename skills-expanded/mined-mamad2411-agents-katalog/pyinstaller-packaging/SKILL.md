---
name: pyinstaller-packaging
description: 将 Python 项目打包为 Windows 可分发的 .exe 可执行程序。当用户要求"打包""构建 exe""出包""PyInstaller""打一个 vX.X 版本"或涉及 build.py/dist 产物时使用。
---

# Python 打包 EXE——PyInstaller 实战

## 核心流程

```
源码 + 依赖 → PyInstaller 分析 → 资源收集 → 打包 → dist/ 产出 .exe
```

## 平台特定注意事项

### `--add-data` 路径分隔符

Windows 用**分号**，Linux 用冒号——混用会导致运行时找不到文件。

```bash
# Windows（正确）
--add-data "templates;templates"
# Linux（正确）
--add-data "templates:templates"
```

### 运行时资源路径适配

PyInstaller 把数据文件解压到临时目录 `sys._MEIPASS`，代码必须用以下模式适配：

```python
import sys, os

def resource_path(relative_path):
    """获取资源绝对路径，兼容打包和开发模式。"""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)
```

### 杀毒软件误报缓解

`--onefile` 打包的 .exe 本质是自解压归档，壳特征易被误报。

缓解方法：
- 优先用 `--onedir` 分发（误报率大幅降低）
- 用 `--clean` 确保无旧签名残留
- 给 .exe 加数字签名（如 `signtool`）

### 版本号嵌入

通过 `--version-file` 传入 Windows 版本信息文件（`file_version_info.txt`），让 .exe 右键属性显示版本号。详见 `references/version-info.md`。

## 典型工作流

```bash
# 1. 清理旧产物
rm -rf build/ dist/ *.spec
# 2. 调试阶段先用 --onedir 验证功能
pyinstaller --onedir --clean main.py
# 3. 确认能跑通再 --onefile 出发布版
pyinstaller --onefile --clean --name "MyApp_v1.0" --icon=icon.ico main.py
# 4. 验证产物
dist/MyApp_v1.0.exe --help
# 5. 分发（压缩 zip 命名含版本号）
```

## .spec 文件（进阶控制）

当命令行参数不够用时，用 `.spec` 文件精细控制排除规则、钩子注入等。生成与定制示例见 `references/spec-examples.md`。

```bash
pyi-makespec --onefile --name MyApp main.py
# 编辑 MyApp.spec 后构建
pyinstaller MyApp.spec
```

## Q&A 机制与项目配置

`packaging.json` 持久化静态信息，避免重复询问。详细流程见 `references/qa-flow.md`，模板见 `references/project-config-template.json`。

核心规则：
- **首次打包**：问 5 个必要问题（软件名/入口/版本号/模式/数据文件），其余默认，回车跳过
- **后续打包**：只问版本号 + 有无临时变更，其余字段静默沿用
- **轻量项目**：无数据文件/隐式 import/图标时自动跳过对应问题
- **构建成功**：写回 JSON（只更新版本号）；失败不写回

## 执行步骤

1. **加载配置**：packaging.json 存在 → 一行摘要 + 只问版本号；不存在 → 5 个默认值问题
2. **确认变更**：问"有临时变更吗"，收集本次特殊需求
3. **拼装命令**：从 JSON 提取参数，执行 `pyinstaller`
4. **验证**：在 dist/ 目录运行 .exe，确认功能正常
5. **保存并分发**：写回 JSON → zip 压缩命名含版本号
