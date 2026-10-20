# Cursor Agent 规则配置

## 代码格式化规则

**⚠️ 重要：每次完成代码修改后，必须自动格式化代码！**

### 强制要求
在完成任何代码修改后，agent **必须**执行以下操作：

1. **Python 文件修改后**（`*.py`）：
   - 运行 `python -m black <修改的文件路径>` 格式化代码
   - 运行 `python -m isort <修改的文件路径>` 整理导入
   - 确保代码符合项目风格

2. **前端文件修改后**（`frontend/src/**/*.{ts,tsx,js,jsx}`）：
   - 运行 `cd frontend && npm run lint -- --fix` 自动修复代码
   - 确保代码符合 ESLint 规则

3. **批量修改后**：
   - 可以使用 `npm run format` 格式化所有代码
   - 或使用 `make format`（如果使用 Makefile）

### 格式化工具
- **Python**: `black` (行长度 88) + `isort` (black 兼容模式) + `pyright` (类型检查)
- **Frontend**: ESLint (自动修复模式)

### 执行时机
**每次 agent 完成代码编辑操作后，立即执行格式化命令，不要等待用户手动格式化。**

### 自动格式化配置

#### 1. Cursor/VS Code 保存时自动格式化
项目已配置 `.vscode/settings.json`，在保存文件时会自动格式化代码。

**配置内容**：
- Python 文件：使用 `black-formatter` 和 `isort` 扩展自动格式化
- TypeScript/JavaScript 文件：使用 `ESLint` 扩展自动修复

**推荐扩展**（`.vscode/extensions.json`）：
- `ms-python.python` - Python 语言支持
- `ms-python.black-formatter` - Black 格式化器
- `ms-python.isort` - isort 导入排序
- `dbaeumer.vscode-eslint` - ESLint 支持

**使用方式**：
1. 安装推荐的扩展（Cursor 会自动提示）
2. 保存文件时会自动格式化（`Ctrl+S` / `Cmd+S`）

#### 2. Cursor Post-Completion 任务
项目已配置 Cursor 内置的 post-completion 任务（`.cursor/tasks.json`），在每次 agent 执行完成后会自动运行 `make format`。

配置文件内容：
```json
{
  "tasks": {
    "postCompletion": {
      "format": ["make format"]
    }
  }
}
```

#### 2. Git Hooks

项目已配置多个 Git hooks，用于自动化代码质量和提交流程。

**安装 Git Hooks**：
```bash
make install-hooks
```

##### Pre-Commit Hook
在每次 `git commit` 前自动执行 `make format`，确保提交的代码格式一致。

功能：
- 提交前自动运行 `make format`
- 如果格式化失败，会阻止提交
- 如果格式化修改了文件，会自动重新添加到暂存区

##### Prepare-Commit-Msg Hook
使用 LLM 自动生成 commit message，分析代码变更并生成符合规范的提交信息。

功能：
- 自动分析暂存区的代码变更（git diff）
- 使用 OpenAI API 生成清晰的 commit message
- 遵循 Conventional Commits 规范
- 如果已有 commit message，则跳过自动生成

**配置要求**：
- 需要设置 `OPENAI_API_KEY` 环境变量（在 `.env` 文件中）
- 可选：设置 `OPENAI_BASE_URL` 和 `OPENAI_MODEL` 来自定义 API 端点或模型

**Hook 文件位置**：
- 源文件：`.githooks/` 目录（已提交到仓库）
  - `pre-commit`: 代码格式化 hook
  - `prepare-commit-msg`: commit message 生成 hook
  - `generate_commit_message.py`: LLM 生成脚本
- 安装位置：`.git/hooks/`（通过 `make install-hooks` 安装）

**注意**：首次克隆仓库或新团队成员加入时，需要运行 `make install-hooks` 来安装 hooks。

### 示例
```bash
# 修改了 Python 文件后
python -m black backroom_agent/agent/graph.py
python -m isort backroom_agent/agent/graph.py

# 修改了前端文件后  
cd frontend && npm run lint -- --fix

# 任务完成前，必须执行统一格式化
make format
```

**记住：代码修改 + 最终执行 `make format` = 完整的任务完成！**
