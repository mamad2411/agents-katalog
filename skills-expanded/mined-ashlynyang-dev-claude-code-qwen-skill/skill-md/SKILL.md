# Qwen — Alibaba Cloud AI Assistant

Call Alibaba's Qwen (通义千问) model for Chinese business analysis, industry research, and general questions.

## When to use this skill

Use Qwen when:
- You need a second opinion on Chinese industry data (餐饮、零售、制造等)
- Researching Chinese market norms, regulations, or business practices
- Validating business logic against Chinese real-world context
- Getting Chinese-language analysis or writing assistance
- Cross-checking numbers/benchmarks against Qwen's training data

## How to call the script

Script path:
```
~/.claude/skills/qwen/scripts/ask_qwen.sh
```

Minimal invocation:
```bash
QWEN_API_KEY=sk-xxxx ~/.claude/skills/qwen/scripts/ask_qwen.sh "你的问题"
```

With system instruction and file context:
```bash
QWEN_API_KEY=sk-xxxx ~/.claude/skills/qwen/scripts/ask_qwen.sh "分析这份数据" \
  --system "你是中国餐饮行业专家" \
  --file /path/to/data.txt
```

With model override:
```bash
QWEN_API_KEY=sk-xxxx ~/.claude/skills/qwen/scripts/ask_qwen.sh "问题" --model qwen-plus
```

The script prints on success:
```
output_path=<path to markdown file>
```

Read the file at `output_path` to get Qwen's response.

## Environment variables

Set these in the environment or prefix the command:
- `QWEN_API_KEY` — Required. Your Dashscope API key (sk-xxxx)
- `QWEN_API_URL` — Optional. Defaults to `https://dashscope.aliyuncs.com/compatible-mode/v1`

## Available models

- `qwen-max` — Most capable, best for complex analysis (default)
- `qwen-plus` — Balanced speed/quality
- `qwen-turbo` — Fastest, good for simple questions
- `qwen-long` — Long context (up to 1M tokens)

## Options

- `--file <path>` — Attach file content as context (repeatable)
- `--system <text>` — System instruction / persona
- `--model <name>` — Override model
- `--max-tokens <n>` — Max output tokens (default: 8192)
- `-o, --output <path>` — Custom output file path
