---
alwaysApply: false
---

# CI 构建错误诊断 Agent

## 触发条件
当用户提到以下关键词时激活：CI 报错、构建失败、build error、job-error、workflow 失败、Docker 构建失败。

## 诊断流程

### 第一步：读取最新日志（防止缓存误读）
每次诊断必须重新读取日志文件，禁止使用任何缓存内容：
- 读取 `.github/workflows/job-logs/job-error.log`（强制实时读取）
- 读取 `.github/workflows/docker-publish.yml`

### 第二步：读取构建相关文件
- `Dockerfile`
- `package.json`
- `vite.config.ts`
- `.dockerignore`
- `docker-compose.yml`

### 第三步：获取最近提交变更
运行以下命令获取最近一次提交的变更文件列表：
```powershell
git diff HEAD~1 HEAD --name-only
```
再获取具体 diff：
```powershell
git diff HEAD~1 HEAD
```

### 第四步：错误定位与分析
按以下优先级逐层排查：

1. **依赖缺失**：`package.json` 中是否缺少 `vite.config.ts` / `Dockerfile` 引用的包
2. **构建参数**：`ARG` / `ENV` / `build-args` 是否匹配
3. **文件路径**：`COPY` 指令的路径是否与 `.dockerignore` 冲突
4. **平台兼容性**：多平台构建（amd64/arm64）的特定问题
5. **缓存问题**：GHA cache 是否导致旧依赖被复用
6. **Secret/证书**：secret mount 是否正确传递

### 第五步：输出诊断报告
格式如下：
- 错误位置：（Dockerfile 行号 / workflow step 名称）
- 根本原因：（一句话说明）
- 受影响文件：（列出相关文件）
- 修复方案：（给出具体的代码修改）

## 注意事项
- 每次诊断前必须用工具实时读取 job-error.log，不得依赖对话上下文中已有的日志内容
- 关注日志中 `ERROR`、`exit code`、`failed` 关键字
- 多平台构建失败时，注意区分是 amd64 还是 arm64 先报错
- Docker layer cache 命中不代表依赖正确，需核对 package.json 与 import 语句