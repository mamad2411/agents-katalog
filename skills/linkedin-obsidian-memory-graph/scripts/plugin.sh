#!/bin/bash
CONF="$HOME/Documents/AgentsMemory/.obsidian/community-plugins.json"
CMD="$1"
ID="$2"
if [ "$CMD" = "list" ]; then
  python3 -m json.tool "$CONF"
elif [ "$CMD" = "on" ]; then
  CONF="$CONF" PID="$ID" python3 -c "import json,os; f=os.environ['CONF']; d=json.load(open(f)); d[os.environ['PID']]=True; json.dump(d,open(f,'w')); print('ON:', os.environ['PID'])"
elif [ "$CMD" = "off" ]; then
  CONF="$CONF" PID="$ID" python3 -c "import json,os; f=os.environ['CONF']; d=json.load(open(f)); d[os.environ['PID']]=False; json.dump(d,open(f,'w')); print('OFF:', os.environ['PID'])"
else
  echo "pakai: plugin.sh on|off|list [plugin-id]"
  exit 1
fi
echo "CATATAN: restart Obsidian agar perubahan aktif."
