---
name: lyxy-runner-js
description: Any task that requires Javascript/Typescript processing should use this skill.
compatibility: Requires Bun runtime (https://bun.sh)
---

# lyxy-runner-js

基于 Bun 的 JavaScript/TypeScript 执行技能，提供隔离的脚本执行和自动依赖管理。

## Purpose

**必需依赖**: 此 skill 需要 Bun 运行时，不兼容其他 JavaScript 运行时。

Bun 特性：
- 自动检测和下载依赖（无需 package.json）
- 即时转译 TypeScript
- 跨平台兼容（Windows/macOS/Linux）

**重要**: 如果 Bun 未安装，立即停止任务并引导用户安装。禁止使用 nodejs、npm、yarn、pnpm 等替代工具。

## When to Use

任何 JavaScript/TypeScript 处理任务都应使用此 skill。

### 典型场景
- **数据处理**: JSON/CSV 解析、数据转换
- **API 交互**: HTTP 请求、Web API 调用
- **文件操作**: 文件读写、批量处理
- **脚本自动化**: 构建脚本、任务自动化

### 不适用场景
- ✗ 需要 Node.js 特定 API（如部分原生模块）
- ✗ 需要持久化进程（如服务器）

## Quick Reference

| 场景 | 描述 | 命令 |
|------|------|------|
| 场景1 | 直接执行已存在的脚本 | `bun <script-file>` |
| 场景2 | 在指定路径创建脚本并执行 | 使用 Write 工具创建 → `bun <path>` |
| 场景3 | 使用临时路径执行（默认） | 生成临时路径 → `bun <temp-file>` |

**重要**: 所有场景执行前必须先检查 Bun 环境：`bun --version`

## Workflow

1. **检查 Bun 环境**：执行 `bun --version`，失败则停止并提示安装
2. **选择执行场景**：根据用户意图选择场景1/2/3
3. **执行脚本**：使用 `bun <script>` 运行
4. **捕获输出**：stdout/stderr 分别处理

### 临时路径执行（场景3）

```bash
# 生成临时文件路径
TEMP_FILE=$(bun scripts/get_temp_path.js js)

# 写入脚本内容
cat <<EOF > "$TEMP_FILE"
console.log("Hello from lyxy-runner-js!");
EOF

# 执行脚本
bun "$TEMP_FILE"
```

## References

详细文档请参阅 `references/` 目录：

| 文件 | 内容 |
|------|------|
| `references/examples.md` | 各场景完整示例、TypeScript 示例、依赖管理示例 |
| `references/error-handling.md` | Bun 未安装、语法错误、运行时错误处理 |
| `references/best-practices.md` | 输出处理、临时文件管理、辅助函数 API |
