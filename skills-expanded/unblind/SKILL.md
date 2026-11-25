---
name: unblind
description: >
  Routes images to Mimo/OpenAI vision API for text-only models. Use this
  skill when the user sends an image, asks "what's in this picture", says
  "analyze this screenshot", requests "OCR" or "extract text", reviews UI
  designs, reads charts, or uses Chinese triggers like 识别图片/看图.
  Self-healing setup on first run. Does NOT handle video, audio, or PDFs.
metadata:
  version: "1.0.0"
  category: ai-vision
  bundled_tools:
    - scripts/unblind.mjs
  requirements:
    - Node.js >= 18
    - Mimo or OpenAI API key (auto-prompted on first run)
  bundled_resources:
    - resources/phase0-details.md
    - resources/troubleshooting.md
    - resources/best_practices.md
compatibility: Claude Code (bundled script, zero npm deps)
allowed-tools: Bash(node ~/.claude/skills/unblind/scripts/unblind.mjs:*)
---

<!-- LEVEL 1: Metadata above (~180 tokens, always loaded) -->
<!-- LEVEL 2: Instructions below (~550 tokens, loaded on trigger) -->

# Unblind

Route images to vision API. Never pretend to see. Never Read/Edit settings.json.

## Iron Rules

1. Phase 0 mandatory every invocation
2. NEVER Read/Edit `~/.claude/settings.json`
3. Config via CLI (`--config`, `--set-model`) or `node -e`, never via tools
4. Never preamble. Never hallucinate. Always invoke bundled script.
5. Tool reads API key from env automatically

## Quick Start

User sends image → Unblind routes to Mimo/OpenAI → returns text.
OCR → extracts all text. ui-review → critiques layout/UX. describe → detailed description.

## Phase 0: Self-Healing

### 0.1 Health check

```bash
node -e "const fs=require('fs');const os=require('os');const p=require('path').join(os.homedir(),'.claude','settings.json');const s=JSON.parse(fs.readFileSync(p,'utf8'));const issues=[];if(!s.env?.MIMO_API_KEY) issues.push('KEY_MISSING');if(!s.env?.MIMO_VISION_MODEL||s.env.MIMO_VISION_MODEL==='mimo-v2.5-pro') issues.push('MODEL_MISSING');const a=s.permissions?.allow||[];if(!a.some(x=>x.includes('unblind'))) issues.push('PERM_MISSING');if(issues.length) console.log(issues.join(' '));" 2>/dev/null
```

- Empty → healthy, **skip to Phase 1**
- `KEY_MISSING` → 0.3 | `MODEL_MISSING` → 0.5 | `PERM_MISSING` → 0.4

### 0.2 Version check

```bash
cd ~/.claude/skills/unblind && git fetch 2>/dev/null && behind=$(git rev-list HEAD..origin/master --count 2>/dev/null) && [ "$behind" -gt 0 ] && echo "NEEDS_UPDATE $behind"
```

- `NEEDS_UPDATE <N>` → 🐌 `unblind 有 N 个更新没拿... git pull 一下嘛~`（不阻塞）

### 0.3-0.9 Repair → Phase 1

See `resources/phase0-details.md`. All healthy → Phase 1.

## Phase 1-4: Analyze

1. **Detect** image path from `[Image: source: <path>]`. Must be absolute, supported ext, no shell metacharacters.
2. **Classify** mode: `describe` (default), `ocr`, `ui-review`, `chart-data`, `object-detect`, `compare`.
3. **Execute**: `node ~/.claude/skills/unblind/scripts/unblind.mjs '<path>' <mode>` — no preamble.
4. **Report**: print stdout. API key error → back to 0.3.

<!-- LEVEL 3: Resources (on-demand) -->

## Resources

- `resources/phase0-details.md` — 完整 Phase 0 流程、CLI 参考、边缘场景
- `resources/troubleshooting.md` — 修复命令、常见错误、Node.js 配置
- `resources/best_practices.md` — 模型选择、token 优化、调试
- `README.md` — 安装指南、安全验证
