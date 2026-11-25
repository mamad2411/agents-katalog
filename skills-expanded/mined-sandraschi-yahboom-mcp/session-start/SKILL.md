---
name: session-start
description: Yahboom MCP session context - robot health check and tool awareness on session start.
---

# session-start

## Session Context (Yahboom MCP)

MCP server for the Yahboom Raspbot v2 (Boomy) ROS 2 robot: motion, sensors, LIDAR, camera PTZ, voice, display, lightstrip, missions, and diagnostics.

**Before starting work:**
1. Check robot health: `yahboom_tool(operation="health_check")`
2. List live ROS topics: `ros_topic_list()`

**At end of work:**
- Stop the robot if you moved it: `yahboom_tool(operation="stop")`
- Confirm server state via `query_logs(limit=20)`
