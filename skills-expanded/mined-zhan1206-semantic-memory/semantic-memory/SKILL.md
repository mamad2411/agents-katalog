---
name: semantic-memory
description: "OpenClaw 本地记忆与语义检索系统。提供完全离线、轻量化的记忆存储与语义召回能力。核心功能：① 内置本地 Embedding 模型（ONNX量化版 all-MiniLM-L6-v2 / bge-small-zh-v1.5，CPU极速推理<50ms）；② 嵌入式向量数据库（FAISS 内存模式+自动IVF索引）；③ OpenClaw Runtime 深度集成（自动对话Hook、自动语义召回、敏感信息过滤）；④ 长期记忆管理+跨会话知识库（重要性衰减、标签、加密）；⑤ 100%离线、隐私优先、敏感信息自动脱敏。触发场景：用户提及「记忆」「语义检索」「知识库」「记住」「搜索记忆」「根据我的笔记」「上次说过」「之前讨论过」等，或需要自动存储/召回对话记忆时。"
metadata: {"openclaw": {"emoji": "🧠", "requires": {"bins": ["python"]}}}
---

# Semantic Memory — OpenClaw 本地记忆与语义检索系统

## 零配置自动加载

放入 `~/.qclaw/skills/` 后自动生效。**首次使用自动完成**：
1. 自动安装 Python 依赖（onnxruntime、tokenizers、faiss-cpu）
2. 自动下载量化 Embedding 模型（~46MB，国内镜像 hf-mirror.com 自动切换）
3. 自动初始化 FAISS 向量数据库

## 对话自动 Hook（核心自动化机制）

### 机制说明

本 Skill 同时提供 **两层自动化**：

**第一层：SKILL.md 指令级 Hook**（开箱即用）
当本 Skill 被 Agent 加载时，以下规则自动生效，无需用户手动触发。

**第二层：OpenClaw Internal Hook**（需启用）
位于 `~/.qclaw/hooks/semantic-memory-hook/`，监听 `message:received`/`message:sent`/`session:compact:before` 事件，实现进程级自动化。

### 第一层：SKILL.md 指令 Hook（自动执行）

#### 1. 用户消息自动存储
当用户发送消息时，**异步存储**用户消息摘要到记忆库：
```bash
python "{SKILL_DIR}/scripts/run.py" add "<用户消息摘要>" --tags "conversation,user" --importance 0.3
```
- 长消息自动分块（段落优先 → 句子级分割，≤512字符/块，64字符重叠）
- 对话记忆默认 importance=0.3，被检索到后自动提升 +0.02

#### 2. 助手回复自动存储
当助手发送回复后，**异步存储**回复摘要：
```bash
python "{SKILL_DIR}/scripts/run.py" add "<助手回复摘要>" --tags "conversation,assistant" --importance 0.3
```

#### 3. 用户提问时自动语义召回
当用户提出问题或需要回忆之前的信息时，**在回复前**先执行语义召回：
```bash
python "{SKILL_DIR}/scripts/run.py" recall "<用户问题>" --top-k 5 --max-chars 3000
```
将召回的记忆内容注入当前对话上下文，辅助回答。

**自动召回触发条件**（满足任一即触发）：
- 用户提及「之前」「上次」「之前说过」「记得吗」「之前讨论过」「之前聊过」
- 用户要求查找过去的讨论或笔记
- 用户的提问与历史话题明显相关
- 用户显式要求搜索记忆

#### 4. 会话结束时持久化
当 `/new` 或 `/reset` 触发时，保存当前会话关键信息：
```bash
python "{SKILL_DIR}/scripts/run.py" add "<会话摘要>" --tags "session,lifecycle" --importance 0.5
```

### 第二层：OpenClaw Internal Hook（可选启用）

如需进程级自动化（无需 Agent 主动调用），启用 Hook：

```bash
openclaw hooks enable semantic-memory-hook
```

Hook 功能：
- **`message:received`**：自动检测问题并召回记忆，注入 `event.messages`
- **`message:sent`**：自动存储助手回复（异步 fire-and-forget）
- **`session:compact:before`**：压缩前自动保存关键上下文
- **`command:new/reset`**：切换会话前自动保存

### 敏感信息自动过滤

所有通过 `add` 和 `add_conversation` 存储的记忆都会**自动脱敏**：
- API 密钥（`sk-...`、`api_key=...`）→ `[REDACTED_API_KEY]`
- 密码（`password=...`）→ `[REDACTED_PASSWORD]`
- 身份证号（18位）→ `[REDACTED_ID_CARD]`
- 银行卡号（16-19位）→ `[REDACTED_BANK_CARD]`
- 手机号（1xx-xxxx-xxxx）→ `[REDACTED_PHONE]`
- 邮箱地址 → `[REDACTED_EMAIL]`
- JWT Token → `[REDACTED_JWT]`
- AWS 密钥 → `[REDACTED_AWS_KEY/SECRET]`
- 私钥标记 → `[REDACTED_PRIVATE_KEY]`

如果文本超过 60% 的内容被脱敏，将**拒绝存储**该条记忆。

### 记忆去重

所有通过 `add` 添加的记忆都会**自动去重**：
- 语义相似度超过 `dedup_threshold`（默认 0.95）时，视为重复记忆
- 重复记忆不会重新存储，而是微增原始记忆的重要性 +0.05
- 原始记忆会记录 `duplicate_count` 字段
- 可通过 `config set dedup_enabled false` 关闭去重
- 可通过 `config set dedup_threshold 0.9` 调整去重阈值

### 上下文窗口适配

`recall` 命令支持 `--max-chars` 参数控制召回文本总长度，避免超出模型上下文窗口：
- 默认预算：3000 字符
- 自动截断：按相似度排序，超预算时停止追加
- 返回 `truncated: true` 标记提示结果被截断

### 与内置 memory 功能的兼容

- 本 Skill 与 OpenClaw 内置 `memory_search`/`memory_get` 工具**互补共存**
- 内置 memory 基于 MEMORY.md 文件（关键词+语义搜索），本 Skill 基于向量数据库（精确语义检索）
- 两者不冲突，可同时使用
- 当内置 memory 搜索未找到结果时，可回退到本 Skill 的向量检索

## CLI 命令速查

所有命令通过 `python "{SKILL_DIR}/scripts/run.py"` 执行，输出 JSON。

### 记忆操作

| 命令 | 说明 | 示例 |
|------|------|------|
| `add <文本>` | 添加记忆 | `add "今天和张三讨论了AI" --tags "工作,重要" --importance 0.8` |
| `search <查询>` | 语义搜索 | `search "张三讨论了什么" --top-k 5` |
| `recall <查询>` | 语义召回+格式化 | `recall "张三讨论了什么" --top-k 5 --max-chars 3000` |
| `list` | 列出记忆 | `list --tag 工作 --limit 50 --sort importance` |
| `get <ID>` | 获取单条 | `get a1b2c3d4e5f6` |
| `tag <ID> <标签>` | 添加标签 | `tag a1b2c3d4e5f6 "重要,工作"` |
| `importance <ID> <值>` | 设重要性 | `importance a1b2c3d4e5f6 0.9` |
| `edit <ID> <文本>` | 编辑内容 | `edit a1b2c3d4e5f6 "更新后的内容"` |
| `delete <ID>` | 删除记忆 | `delete a1b2c3d4e5f6` |
| `stats` | 统计信息 | `stats` |
| `forget` | 自动遗忘 | `forget` (dry-run) / `forget --apply` |
| `clear --confirm` | 清空记忆 | `clear --confirm` |
| `encrypt <密码>` | 加密记忆库 | `encrypt mypassword` |
| `unlock <密码>` | 解密记忆库 | `unlock mypassword` |

### 知识库操作

| 命令 | 说明 | 示例 |
|------|------|------|
| `kb create <名称>` | 创建知识库 | `kb create "Python笔记" --desc "Python学习"` |
| `kb list` | 列出知识库 | `kb list` |
| `kb add <名称> <文件>` | 添加文档 | `kb add "Python笔记" ./notes.pdf` |
| `kb query <名称> <问题>` | 查询知识库 | `kb query "Python笔记" "什么是闭包"` |
| `kb delete <名称>` | 删除知识库 | `kb delete "Python笔记"` |
| `import <文件> --kb <名称>` | 导入文件 | `import ./doc.pdf --kb "笔记"` |
| `import-dir <目录> --kb <名称>` | 批量导入 | `import-dir ./docs/ --kb "笔记"` |

支持的文档格式：`.txt`, `.md`, `.pdf`, `.docx`

### 配置操作

| 命令 | 说明 | 示例 |
|------|------|------|
| `config get [key]` | 获取配置 | `config get search_min_score` |
| `config set <key> <value>` | 设置配置 | `config set dedup_threshold 0.9` |
| `config reset` | 重置为默认 | `config reset` |

### 性能监控

| 命令 | 说明 | 示例 |
|------|------|------|
| `metrics` | 查看性能指标 | `metrics` |

## 自然语言交互示例

```
用户: 帮我记住今天和张三讨论了 AI 项目进展
→ 执行: python run.py add "和张三讨论了AI项目进展" --tags "工作" --importance 0.7
→ 回复: 已记住！记忆ID: a1b2c3d4e5f6

用户: 我上次和张三聊了什么？
→ 执行: python run.py recall "和张三聊天讨论" --top-k 5
→ 自动召回相关记忆并回答

用户: 创建一个「Python学习笔记」知识库
→ 执行: python run.py kb create "Python学习笔记" --desc "Python学习"

用户: 根据我的 Python 笔记，解释闭包是什么
→ 执行: python run.py recall "什么是闭包" --kb "Python学习笔记" --top-k 5
→ 在知识库中检索并回答

用户: 把这个 PDF 导入到我的 Python 笔记里
→ 执行: python run.py import ./file.pdf --kb "Python学习笔记"

用户: 列出所有重要标记的记忆
→ 执行: python run.py list --tag 重要

用户: 删除关于项目A的所有记忆
→ 执行: python run.py search "项目A" → 逐条 delete
```

## 重要参数

所有参数均可通过 `config set` 命令自定义，以下为默认值：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| model_id | all-MiniLM-L6-v2 | Embedding 模型 |
| chunk_max_chars | 512 | 每块最大字符数 |
| chunk_overlap | 64 | 块间重叠字符数 |
| search_top_k | 5 | 默认返回条数 |
| search_min_score | 0.2 | 最低相似度阈值 |
| half_life_days | 30 | 衰减半衰期（天） |
| min_importance | 0.1 | 自动遗忘阈值 |
| conversation_importance | 0.3 | 对话记忆默认重要性 |
| recall_importance_boost | 0.02 | 检索后重要性微增量 |
| auto_recall_max_chars | 3000 | 召回上下文预算 |
| dedup_enabled | true | 是否启用去重 |
| dedup_threshold | 0.95 | 去重相似度阈值 |
| sensitive_filter_enabled | true | 是否启用敏感过滤 |
| sensitive_max_redact_ratio | 0.6 | 最大脱敏率 |
| metrics_enabled | true | 是否启用性能监控 |

## 国内用户专属适配

- 模型下载自动切换国内镜像（hf-mirror.com → huggingface.co）
- 默认内置中文专用模型 bge-small-zh-v1.5 (512维)
- 自动语言检测：中文占比>30%时使用中文模型

## 完整命令参考

详见 [references/commands.md](references/commands.md)

## 技术架构详解

详见 [references/architecture.md](references/architecture.md)

## REST API 服务

提供 FastAPI HTTP 接口，适合程序化调用和跨语言集成：

```bash
# 启动 API 服务
python scripts/api_server.py --port 8765

# 访问 Swagger 文档
open http://localhost:8765/docs
```

详见 [api_examples.md](api_examples.md)，包含 cURL、Python requests、JavaScript 示例。

## 交互式菜单模式

无需记忆命令，通过菜单操作记忆和知识库：

```bash
python scripts/run.py --interactive
# 或
python scripts/run.py -i
```

提供 4 大功能模块：记忆管理、知识库管理、配置管理、系统统计。

## 批量操作

支持大规模数据导入和管理：

```bash
# 从文本文件批量添加（每行一条）
python scripts/batch.py add-file ./memories.txt --tags "工作" --importance 0.6

# 批量导入目录文档
python scripts/batch.py import-dir ./docs/ "我的知识库" --exts ".txt,.md,.pdf"

# 按标签批量删除
python scripts/batch.py delete-by-tag "临时" --dry-run

# 批量导出记忆到 JSON
python scripts/batch.py export <id1> <id2> --output backup.json
```

## Docker 部署

```bash
# 构建镜像
cd docker && docker build -t semantic-memory .

# 运行
docker run -p 8765:8765 -v ~/.qclaw/data:/data semantic-memory

# 查看日志
docker logs -f <container_id>
```

详见 [docker/README.md](docker/README.md)。

## Shell 自动补全

安装命令行自动补全（支持 Bash/Zsh/Fish）：

```bash
# Bash
cp shell/semantic-memory.bash /etc/bash_completion.d/
source ~/.bashrc

# Zsh
cp shell/semantic-memory.zsh ~/.zsh/completions/_semantic-memory

# Fish
cp shell/semantic-memory.fish ~/.config/fish/completions/
```

## 开发与测试

```bash
# 安装开发依赖
pip install -e ".[all]"

# 运行测试
pytest tests/ -v

# 带覆盖率
pytest tests/ -v --cov=scripts --cov-report=html

# 运行特定测试
pytest tests/test_memory_manager.py -v
```

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。
