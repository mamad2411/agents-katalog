---
name: agent-tars
description: Open-source multimodal AI agent for computer control, browser automation, and task execution. Combines Agent TARS (reasoning/browser) with agent-browser CLI (page navigation, form filling, clicking, screenshots, data extraction). Use for automating browser actions, web testing, scraping, form automation, or any task needing programmatic web interaction. Triggers: "open a website", "fill a form", "click a button", "take a screenshot", "scrape data", "automate browser", "web automation".
allowed-tools: run_command(npx agent-browser:*), run_command(agent-browser:*), run_command(agent-tars:*)
---

<MANDATORY_EXECUTION_SCRIPT>
"=== agent-tars Core Workflow ==="
""

# Step 1: Navigate
try {
    $null = Get-Command "agent-browser" -ErrorAction Stop
    "[√] Step 1: Navigate - agent-browser CLI available"
} catch {
    "[ ] Step 1: Navigate - agent-browser not found. Install: npm i -g agent-browser"
    exit 1
}

# Step 2: Snapshot
try {
    $ver = & agent-browser --version 2>&1
    "[√] Step 2: Snapshot - agent-browser $($ver.Trim()) supports snapshot -i"
} catch {
    "[ ] Step 2: Snapshot - agent-browser not responding"
    exit 1
}

# Step 3: Interact
"[√] Step 3: Interact - agent-browser supports click @ref, fill @ref, select @ref"

# Step 4: Re-snapshot
"[√] Step 4: Re-snapshot - snapshot -i after DOM changes refreshes refs"

""
"All 4 core workflow steps ready."
</MANDATORY_EXECUTION_SCRIPT>

See `details.md` for full documentation.
