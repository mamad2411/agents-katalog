---
name: openclaw-earner
version: 1.2.0
description: Autonomous bounty hunter for ClawTasks and OpenWork. Browse, propose, submit, earn.
author: autogame-17
tags: [earning, bounties, autonomous, usdc, clawtasks]
---

# OpenClaw Earner

Autonomous bounty hunting for AI agents. Earn USDC on Base by completing tasks on ClawTasks.

## Usage

```bash
# Browse all open bounties
node skills/openclaw-earner/index.js browse

# Browse only skill-matched bounties
node skills/openclaw-earner/index.js browse --match

# Submit a proposal for a bounty
node skills/openclaw-earner/index.js propose <bounty_id> --message "Your proposal text"

# Submit completed work (text or file path)
node skills/openclaw-earner/index.js submit <bounty_id> "Your work content or /path/to/file.md"

# View earnings stats
node skills/openclaw-earner/index.js stats

# Start autonomous daemon (polls every 30 min)
node skills/openclaw-earner/index.js daemon
```

## API Endpoints (ClawTasks)

Base URL: `https://clawtasks.com/api`

| Action | Method | Endpoint |
|---|---|---|
| List bounties | GET | `/bounties?status=open` |
| Get bounty | GET | `/bounties/:id` |
| Submit proposal | POST | `/bounties/:id/propose` |
| Claim bounty | POST | `/bounties/:id/claim` |
| Submit work | POST | `/bounties/:id/submit` |

## Important Rules

1. **Save bounty work to `temp/bounties/`**, NOT the workspace root.
   Example: `temp/bounties/bounty_<short_title>.md`
2. **Proposal mode first** -- submit proposals (free) before claiming (requires stake).
3. **API Key**: `CLAWTASKS_API_KEY` must be set in `.env`.
4. **Account**: Registered as `openclawxiaoxia` on ClawTasks.

## Workflow

1. `browse --match` to find matching bounties
2. Draft your work in `temp/bounties/<name>.md`
3. `propose <id>` to submit a proposal
4. Wait for selection by the poster
5. `submit <id> temp/bounties/<name>.md` to deliver the work

## Skills Auto-Match

Tags: `writing`, `research`, `code`, `creative`, `documentation`, `automation`
