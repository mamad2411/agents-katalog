#!/bin/bash
# plugin_audit.sh — matikan plugin berat otomatis, lapor sisanya.
CONF="$HOME/Documents/AgentsMemory/.obsidian/community-plugins.json"
HEAVY="obsidian-excalidraw-plugin obsidian-git"
for p in $HEAVY; do
  CONF="$CONF" PID="$p" python3 -c "import json,os; f=os.environ['CONF']; d=json.load(open(f)); d[os.environ['PID']]=False; json.dump(d,open(f,'w')); print('OFF:', os.environ['PID'])"
done
echo "--- status ---"
python3 -c "import json; d=json.load(open('$CONF')); print('ON:', [k for k,v in d.items() if v]); print('OFF:', [k for k,v in d.items() if not v])"
echo "restart Obsidian agar berlaku."
