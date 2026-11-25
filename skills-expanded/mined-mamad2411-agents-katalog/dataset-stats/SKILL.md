# /dataset-stats — Show download stats and what's missing

## Instructions

Run this command and show the output to the user:

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/Wave-5-research && uv run scripts/download_manager.py --status 2>&1
```

Then also show disk usage:

```bash
echo "=== DISK ==="
du -sh /Volumes/AIFlowDev/RobotFlowLabs/datasets/models/
du -sh /Volumes/AIFlowDev/RobotFlowLabs/datasets/datasets/
du -sh /Volumes/AIFlowDev/RobotFlowLabs/datasets/repos/
echo "TOTAL: $(du -sh /Volumes/AIFlowDev/RobotFlowLabs/datasets/ | cut -f1)"
```

Summarize: how many done, how many pending, total GB on disk, what's still missing.

If the user wants to download missing items:
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/Wave-5-research
uv run scripts/download_manager.py --all
```

To refresh the map after downloads:
```bash
uv run scripts/update_map.py
```
