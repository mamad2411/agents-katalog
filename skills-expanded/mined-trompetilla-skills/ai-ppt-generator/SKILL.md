---
name: ai-ppt-generator
description: The awesome PPT format generation tool provided by baidu. 
metadata: { "openclaw": { "emoji": "📑", "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# AI PPT Generation
Using user input topic/query, generate a highly quality ppt url which can download to local disk. 

## Workflow
1. Executes the Python script located at `scripts/generate_ppt.py` to generate ppt

### generate ppt
#### Example Usage
```bash
 python3 scripts/generate_ppt.py --query "经济总结报告ppt"
```
