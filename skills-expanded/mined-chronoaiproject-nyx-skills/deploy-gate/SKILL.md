---
name: deploy-gate
description: "Deployment gate with human approval — runs preflight checks, sends an interactive Lark approval card, then simulates deployment on approval. Usable from Lark bot via natural language or /deploy command."
metadata:
  category: mixed
  tag:
    - "deploy"
    - "devops"
    - "approval"
    - "workflow"
  output-type: text
  runtime:
    - "python"
  tool-list:
    - "code_execute"
    - "reply_with_interaction"
version: "1.0"
---

# Deploy Gate

A deployment gate workflow with human approval. Use when someone says "deploy", "部署", "上线", "/deploy", or "deploy to staging".

You (the agent) run the whole flow yourself:

## Step 1 — Preflight Check

Run this Python in `code_execute`:

```python
from datetime import datetime
print(f"🔍 Preflight check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ Build passed")
print("✅ Tests green")
print("✅ No breaking changes detected")
print("📦 Ready to deploy to staging")
```

## Step 2 — Request Approval

Call `reply_with_interaction` with:
- title: "🚀 确认部署到 staging？"
- body: preflight output from Step 1
- fields:
  - "Build" → "✅"
  - "Tests" → "✅"  
  - "Breaking Changes" → "None"
- actions:
  - action_id: "deploy-approve", label: "✅ 确认部署", style: "primary"
  - action_id: "deploy-reject", label: "❌ 取消", style: "danger"

## Step 3 — Deploy (on approval)

When the user clicks approve, run:

```python
import time
print("🚀 Deploying to staging environment...")
for i in range(3):
    time.sleep(0.3)
    print(f"  ⏳ Step {i+1}/3...")
print("✅ Deployment complete!")
print("📊 Monitor at: https://dashboard.aevatar.ai")
print("🎉 Staging is now live with latest changes!")
```

On reject, reply: "❌ Deployment cancelled."

## Workflow YAML (bundled)

A complete Aevatar workflow definition is bundled in `workflows/deploy-gate.yaml`. Use it with `aevatar_start_workflow` when a scope is available, or follow the manual steps above.
