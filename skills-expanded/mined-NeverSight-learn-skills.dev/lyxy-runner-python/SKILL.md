---
name: lyxy-runner-python
description: Any task that requires Python processing should use this skill.
---

# UV Python Runner Skill

指导大模型使用uv运行Python脚本，无需预安装依赖，保持环境整洁。

## Purpose

**必需依赖**: 此skill必需uv工具，不兼容其他Python运行方式。

利用uv隔离环境特性：
- 自动管理虚拟环境和依赖
- 避免系统Python污染
- 支持用户现有脚本（无需修改）
- 自动解析依赖并使用`--with`传递
- 智能检测uv项目，复用项目环境
- 跨平台兼容（Windows/macOS/Linux）

**重要**: 如果uv未安装，立即停止任务并引导用户安装。不要使用python、pip、poetry、venv等替代工具。

## When to Use

任何Python处理任务都应使用此skill。

### 典型场景
- **数据处理**: pandas, numpy, scipy / CSV/JSON/YAML转换 / 统计分析
- **API交互**: HTTP请求（requests, httpx） / API数据检索
- **文件操作**: 重命名、批量处理 / pathlib, shutil操作
- **科学计算**: numpy, scipy / matplotlib, plotly可视化
- **系统工具**: logging / configparser / tqdm, rich进度跟踪

### 不适用场景
- ✗ 需要用户交互（input()）
- ✗ 需要持久化环境（每次都是新环境）
- ✗ 需要命令行参数
- ✗ 需要从stdin读取

## Quick Reference

| 场景 | 命令 |
|------|------|
| uv项目 | `uv run <script_path>` |
| 非uv+有依赖 | `uv run --with pkg1 --with pkg2 <script_path>` |
| 非uv+无依赖 | `uv run <script_path>` |

## Workflow

1. **解析依赖**：分析import语句，提取外部包名（排除标准库）
2. **检测项目**：执行`uv sync --dry-run`判断是否为uv项目
3. **确定路径**：用户指定路径 → 现有脚本 → 临时文件
4. **构造命令**：根据项目类型和依赖构造执行命令
5. **执行脚本**：运行并捕获输出

## References

详细文档请参阅 `references/` 目录：

| 文件 | 内容 |
|------|------|
| `references/examples.md` | 数据分析、API交互、文件操作等完整示例 |
| `references/error-handling.md` | uv未安装、依赖解析失败等错误处理指南 |
| `references/best-practices.md` | 依赖解析、路径处理、项目检测等最佳实践 |
