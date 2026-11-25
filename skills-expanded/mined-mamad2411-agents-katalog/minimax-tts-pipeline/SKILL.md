---
name: minimax-tts-pipeline
description: >
  将文本文件通过 MiniMax TTS API 生成中文口播音频，自动处理多音字、英文缩写、
  混合模型名、数字读法等高频发音错误。当用户说"使用MiniMax生成口播音频"时触发。
---

# MiniMax TTS 发音控制

将文本文件逐步处理发音问题，最终调用 MiniMax TTS API 生成音频。

## 输入

| 参数 | 必填 | 说明 |
|------|------|------|
| 文本文件路径 | 是 | 待处理的 .txt 文件绝对路径 |
| 输出目录 | 否 | 默认在输入文件同目录下创建 `tts-{YYYYMMDD-HHMMSS}/` 目录 |

## 用户发音规则管理

当用户提出添加/查询/删除/修改发音规则（如"Qwen 读作千问"、"看看有哪些规则"、"删掉 Qwen 的规则"）时，读取 `<SKILL_DIR>/references/manage-user-rules.md` 和 `<SKILL_DIR>/references/pronunciation-rules.md`，然后按指引操作 `<SKILL_DIR>/user-rules.json`。

## 工作流

```
输入.txt → input.raw.txt → [脚本] normalize_punctuation.py → input.txt
         → [脚本] scan_terms.py → terms.json(草稿)
         → [Subagent 1] 补全规范化 → terms.json
         → [脚本] validate + generate_normalized.py → normalized.txt
         → [Subagent 2] 补全读法 + 多音字识别 → terms.json
         → [脚本] validate
         → [Subagent 3] 复核 → terms.json(review.pass)
         → [脚本] validate + call_tts.py → output.wav + output.title
         → [脚本] title_to_srt.py → output.srt
```

用 `<SKILL_DIR>` 表示本 skill 目录的绝对路径。
用 `<run_dir>` 表示当前运行的输出目录的绝对路径（即 Step 0 中创建的 `tts-{YYYYMMDD-HHMMSS}/` 目录的完整路径）。

### Step -1：环境预检测

在开始任何处理之前，依次检测运行环境和 MiniMax API Key。

**Python 与依赖检测：**

1. 执行 `python3 --version`，确认 Python >= 3.10。如果版本过低或未安装，提示用户安装后重试，停止流程。
2. 执行 `python3 -c "import requests"`，确认 `requests` 库已安装。如果未安装，提示用户执行 `pip3 install requests`（或 `pip install requests`）后重试，停止流程。

**API Key 检测：**

3. 检查 `<SKILL_DIR>/.env`（即与 SKILL.md 同级目录下的 `.env` 文件）是否存在。如果不存在，新建一个空的 `.env` 文件。
4. 读取该 `.env` 文件，检查是否存在 `MINIMAX_API_KEY` 且值非空。
5. 如果已配置，继续下一步。
6. 如果未配置，向用户询问 MiniMax API Key。用户给出后，将 `MINIMAX_API_KEY=<用户提供的值>` 追加到 `<SKILL_DIR>/.env` 文件中，然后继续。

### Step 0：初始化运行目录

1. 从用户输入获取文本文件路径。
2. 创建 `<input_dir>/tts-{YYYYMMDD-HHMMSS}/` 目录，其中 `<input_dir>` 是输入文件所在目录；除非用户显式指定输出目录，否则不得改用当前工作目录或 skill 项目目录。
   - 如果因沙箱或权限限制无法写入输入文件同级目录，必须先请求用户授权；只有用户明确同意时，才允许改用其他目录。
3. 复制输入文件为 `<run_dir>/input.raw.txt`。
4. 执行标点规范化：

```bash
python3 <SKILL_DIR>/scripts/normalize_punctuation.py <run_dir>/input.raw.txt <run_dir>/input.txt
```

5. 执行：

```bash
python3 <SKILL_DIR>/scripts/scan_terms.py <run_dir>/input.txt <run_dir>/terms.json
```

6. 进入 Step 1。

### Step 1：大小写规范化判断

将 `<SKILL_DIR>` 和 `<run_dir>` 替换为实际绝对路径后，发送以下 prompt 给 subagent：

```
请先阅读以下文件，然后执行任务。

## 必读文件（按顺序阅读）

1. 操作指引：<SKILL_DIR>/references/step-1-normalize.md
2. 发音规则参考：<SKILL_DIR>/references/pronunciation-rules.md
3. 用户自定义规则：<SKILL_DIR>/user-rules.json（如文件不存在则跳过）
4. 原文：<run_dir>/input.txt
5. 候选词：<run_dir>/terms.json

## 任务

按操作指引的规则，处理 terms.json 中每个 term 的 normalized、category、reason 字段。

## 输出

直接修改并保存 <run_dir>/terms.json（不要创建新文件）。

## 校验

修改完成后，执行 `python3 <SKILL_DIR>/scripts/validate_terms.py <run_dir>/terms.json 1`。如果校验失败，根据 errors 列表修正 terms.json，重新校验，直到通过。

## 收尾

校验通过后，执行 `python3 <SKILL_DIR>/scripts/generate_normalized.py <run_dir>/input.txt <run_dir>/terms.json <run_dir>/normalized.txt`。
```

### Step 2：发音读法判断

将 `<SKILL_DIR>` 和 `<run_dir>` 替换为实际绝对路径后，发送以下 prompt 给 subagent：

```
请先阅读以下文件，然后执行任务。

## 必读文件（按顺序阅读）

1. 操作指引：<SKILL_DIR>/references/step-2-reading.md
2. 发音规则参考：<SKILL_DIR>/references/pronunciation-rules.md
3. 用户自定义规则：<SKILL_DIR>/user-rules.json（如文件不存在则跳过）
4. 原文：<run_dir>/input.txt
5. 规范化后文本：<run_dir>/normalized.txt
6. 候选词：<run_dir>/terms.json

## 任务

按操作指引的规则，处理 terms.json 中每个 term 的 reading、category 字段，并识别原文中遗漏的多音字。

## 输出

直接修改并保存 <run_dir>/terms.json（不要创建新文件）。

## 校验

修改完成后，执行 `python3 <SKILL_DIR>/scripts/validate_terms.py <run_dir>/terms.json 2`。如果校验失败，根据 errors 列表修正 terms.json，重新校验，直到通过。
```

### Step 3：质量复核

将 `<SKILL_DIR>` 和 `<run_dir>` 替换为实际绝对路径后，发送以下 prompt 给 subagent：

```
请先阅读以下文件，然后执行任务。

## 必读文件（按顺序阅读）

1. 操作指引：<SKILL_DIR>/references/step-3-review.md
2. 发音规则参考：<SKILL_DIR>/references/pronunciation-rules.md
3. 用户自定义规则：<SKILL_DIR>/user-rules.json（如文件不存在则跳过）
4. 原文：<run_dir>/input.txt
5. 规范化文本：<run_dir>/normalized.txt
6. 完整候选词：<run_dir>/terms.json

## 任务

按操作指引的检查项，对 terms.json 做最终质量复核。

## 输出

直接修改并保存 <run_dir>/terms.json（不要创建新文件）。

## 校验

修改完成后，执行 `python3 <SKILL_DIR>/scripts/validate_terms.py <run_dir>/terms.json 3`。如果校验失败，根据 errors 列表修正 terms.json，重新校验，直到通过。
```

### Step 4：生成音频和字幕 JSON

调用 MiniMax TTS API：

```bash
python3 <SKILL_DIR>/scripts/call_tts.py <run_dir>/normalized.txt <run_dir>/terms.json <run_dir>/output.wav <run_dir>/output.title
```

此步骤会：
- 生成并落盘 WAV 音频：`<run_dir>/output.wav`
- 下载并落盘 MiniMax 返回的字幕 JSON：`<run_dir>/output.title`

### Step 5：生成 SRT 字幕

根据 Step 4 得到的 MiniMax 字幕 JSON 和 WAV 音频，生成 SRT 字幕：

```bash
python3 <SKILL_DIR>/scripts/title_to_srt.py <run_dir>/output.title <run_dir>/output.wav <run_dir>/output.srt
```

向用户报告结果：
- 音频文件路径
- MiniMax 字幕 JSON 文件路径
- SRT 字幕文件路径
- 使用了多少条 tone 规则
- 替换了多少处文本

## 落盘文件

```
tts-YYYYMMDD-HHMMSS/
  input.raw.txt    # 原始输入（只读）
  input.txt        # 标点规范化后的输入（只读）
  terms.json       # 全流程唯一结构化工作文件
  normalized.txt   # 规范化后的文本
  output.wav       # MiniMax TTS 输出音频
  output.title     # MiniMax 返回的字级时间戳字幕 JSON
  output.srt       # 根据 output.title + output.wav 生成的 SRT 字幕
```

## 约束

- 全流程只维护一份 terms.json，所有 subagent 都直接修改这同一个文件。
- LLM 只改 terms.json，不直接修改 normalized.txt 或 input.txt。
- 文本替换、tone 生成、API 调用全部由脚本执行。
- 任一阶段校验失败就停止，不继续后续阶段。
- MINIMAX_API_KEY 从 `<SKILL_DIR>/.env` 文件读取。

## Resources

### scripts/
- `normalize_punctuation.py <input> <output>` — 阶段 0：对换行缺失句末标点的文本补充句号
- `scan_terms.py` — 阶段 0：从原文提取候选词，生成 terms.json 草稿
- `validate_terms.py <terms_json> <stage>` — 阶段 1/2/3：校验 terms.json schema
- `generate_normalized.py <input> <terms> <output>` — 阶段 1 后：根据 terms.json 生成规范化文本
- `call_tts.py <normalized> <terms> <output_wav> [output_title]` — 阶段 4：调用 MiniMax TTS API 生成 WAV 音频并下载字幕 JSON
- `title_to_srt.py <input_title> <input_wav> [output_srt]` — 阶段 5：根据 MiniMax 字幕 JSON 和 WAV 音频生成 SRT 字幕

### references/
- `pronunciation-rules.md` — 发音规则速查（category 枚举、reading 格式、关键约束）
- `manage-user-rules.md` — 用户发音规则管理指引（按需加载）
- `api-voice-settings.md` — MiniMax API 请求中 voice_id、speed、vol、pitch 参数说明与修改位置
- `step-1-normalize.md` — step 1 操作指引：大小写规范化判断
- `step-2-reading.md` — step 2 操作指引：发音读法判断 + 多音字识别
- `step-3-review.md` — step 3 操作指引：质量复核

### 其他文件
- `user-rules.json` — 用户自定义发音规则（agent 通过对话维护，各步骤消费）
- `.env` — MiniMax API Key 存储

## API 声音参数修改

如果用户询问或想修改 MiniMax TTS API 请求中的音色、语速、音量、语调参数（`voice_id`、`speed`、`vol`、`pitch`），请先阅读 `<SKILL_DIR>/references/api-voice-settings.md`。这些参数需要直接在 `<SKILL_DIR>/scripts/call_tts.py` 的 payload 中修改。
