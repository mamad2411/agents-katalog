---
name: docker-first-runner
description: 引导 AI 使用 Docker 优先策略运行脚本。当用户需要执行 Python、Node.js 或其他脚本时，本技能帮助 AI 基于环境检测和版本兼容性决定使用 Docker 容器化（首选）还是本地执行。
---

# Docker 优先执行器

用于在运行脚本时决定使用 Docker 容器化还是本地执行的指南。

## 何时使用

- 运行/执行 Python 脚本
- 运行/执行 Node.js 脚本
- 运行/执行任何代码文件
- 执行需要特定运行时版本的命令

## 快速开始

```bash
# 1. 检测环境
node scripts/detect-env.js

# 2. 如需要，比较版本
node scripts/version-compare.js "$(本地版本)" "$(所需版本)"

# 3. 使用选定的方法执行
```

## 工作流程

1. **使用 `scripts/detect-env.js` 检测环境**
   ```bash
   node scripts/detect-env.js
   ```

2. **解析 JSON 输出** - 脚本返回关于可用运行时的结构化数据

3. **选择执行方式**：
   - 如果 `docker.usable` 为 true → 使用 Docker
   - 如果 Docker 不可用 → 使用 `scripts/version-compare.js` 检查本地版本
   - 根据比较结果构建合适的命令

4. **使用选定的方法执行**

## 参考文件

| 文件 | 用途 |
|------|------|
| `scripts/detect-env.js` | 环境检测 - 检查 Docker 和本地运行时 |
| `scripts/version-compare.js` | 版本比较工具 |
| `references/language-matrix.md` | 各语言的版本要求 |
| `references/strategy-guide.md` | 详细的决策逻辑和边界情况 |
