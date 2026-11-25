#!/usr/bin/env bash
# Nyalakan animation-workflow MCP untuk Claude sementara (±590 token/request).
# Matikan lagi: hapus entry "animation-workflow" dari mcpServers di ~/.claude/settings.json
python3 - <<'PY'
import json
p='/Users/chaali0324/.claude/settings.json'
s=json.load(open(p))
s.setdefault('mcpServers',{})['animation-workflow']={
 "type":"stdio","command":"npx","args":["-y","animation-workflow-mcp"]}
json.dump(s,open(p,'w'),indent=2)
print('animation-workflow ON — restart claude untuk apply')
PY
