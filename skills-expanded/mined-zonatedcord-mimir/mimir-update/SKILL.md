---
name: mimir-update
description: Update Mimir to the latest version. Safe to run anytime — idempotent.
allowed-tools: [Bash]
---

Execute this bash command and print the output verbatim:

```bash
rm -rf ~/.claude/mimir && \
git clone https://github.com/ZonatedCord/Mimir.git ~/.claude/mimir && \
mkdir -p ~/.claude/commands/ && \
cp -r ~/.claude/mimir/.claude/commands/* ~/.claude/commands/ && \
echo "✅ Mimir updated successfully"
```

Do not add commentary or interpretation. Output only what the commands print.
