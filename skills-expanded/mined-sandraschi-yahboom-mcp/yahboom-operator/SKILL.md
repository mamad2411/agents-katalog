---
name: yahboom-operator
description: Use this skill when controlling or troubleshooting a Yahboom Raspbot v2 (or compatible) robot via the Yahboom MCP server.
---

# Yahboom Raspbot v2 Operator Skill

Use this skill when controlling or troubleshooting a Yahboom Raspbot v2 (or
compatible) robot via the Yahboom MCP server. For hardware, ROS 2, frames, and
integration depth use **yahboom-robots-expert**. All tool names below are the
registered MCP names — call them verbatim.

## Who is this for

- **Agents** (Claude/Cursor/OpenCode driving the robot): follow Workflow Rules
  exactly; never invent tool names; always health-check first.
- **Humans** (dashboard operators): the same sequences work as buttons in
  Mission Control / Diagnostics; this skill explains what the buttons do.

## Tool catalog (real operation names)

- **yahboom_tool(operation, param1, param2, payload)** — portmanteau, 40+ ops.
  Motion: `health_check`, `forward`, `backward`, `turn_left`, `turn_right`,
  `strafe_left`, `strafe_right`, `stop`, `stop_all`, `config_show`,
  `inspect_stack`. Sensors: `read_imu`, `read_battery`, `read_encoders`,
  `read_all`, `read_lidar`. Voice: `say`, `play`, `play_beep`, `play_file`,
  `chat_and_say`, `audio_play`, `audio_store`, `audio_play_stored`,
  `audio_list_stored`, `audio_stop`. Display: `display`, `clear_display`.
  Lightstrip: `led`, `led_off`, `light_effect`, `patrol_car`. Camera PTZ:
  `camera_up`, `camera_down`, `camera_left`, `camera_right`, `camera_reset`,
  `camera_set_pos`, `camera_move`. Trajectory: `start_recording`,
  `stop_recording`, `list_trajectories`. Missions: `explore`,
  `explore_and_map`. Gripper: `gripper_set`, `gripper_open`, `gripper_close`,
  `gripper_status`. Diagnostics: `execute_command` (sandboxed SSH).
- **lidar(operation, source, param1, param2, payload)** — `read`, `read_raw`,
  `read_dreame_map` × source `yahboom`/`dreame`/`auto`.
- **yahboom_help_tool(category, topic)** — categories: motion, sensors,
  connection, api, mcp_tools, startup, troubleshooting.
- **yahboom_agentic_workflow(goal)** — natural-language multi-step goals via
  MCP sampling (needs a sampling-capable client).
- **yahboom_agent_mission(goal, provider, publish_to_ros, speak)** — NL goal
  to validated mission JSON, optional ROS publish + speech.
- **ros_topic_list()**, **ros_node_info(node_name)**, **ros_resync()**,
  **ros_restart_bringup()** (nuclear option, warn first).
- **audio(file_path, operation, file_name)**, **query_logs(source, level,
  search, limit)**, **yahboom_shutdown(reason)**,
  **show_robot_status_card()** (rich status card, works offline).

## Prompts (call by name)

`yahboom_quick_start(robot_ip)`, `yahboom_patrol(duration_seconds)`,
`yahboom_diagnostics()`, `yahboom_patrol_apartment()`,
`yahboom_go_to_recharge()`, plus skills-as-prompts: `yahboom_quick_pilot`,
`yahboom_patrol_sweep`, `yahboom_emergency_halt`, `yahboom_diagnostic_triage`.

## Workflow rules

1. **Safety first**: `yahboom_tool(operation="health_check")` before motion,
   every session; battery < 20% means charge, < 15% means dock now.
2. **Stop after moves**: every timed move ends with `stop`; `stop_all` on any
   surprise. Agentic workflows stop automatically — verify anyway.
3. **Goal-oriented**: `yahboom_agentic_workflow` for multi-step goals (patrol,
   inspect, return); single `yahboom_tool` calls for one-off commands.
4. **LIDAR before blind driving**: `lidar(operation="read")` sectors ahead
   when the map is older than the last move.
5. **Nuclear last**: `ros_restart_bringup` only after `ros_resync` fails.

## Workflows (copy shapes)

**W1 first drive**: health_check → read_battery → forward 0.3 (3 s) → stop →
read_imu. **W2 square patrol**: agentic "forward 2 s, turn left 90°, x4, stop,
report battery". **W3 link triage**: inspect_stack → resync → SSH `docker ps`
→ restart bringup. **W4 trajectory**: start_recording → drive → stop_recording
(name) → list_trajectories. **W5 mission**: agent_mission with concrete target,
publish_to_ros true, watch `/api/v1/missions/status`, abort via missions/stop
then stop_all.

## Troubleshooting

Link down: health → inspect_stack → resync → SSH → restart. No video:
snapshot 204 means empty cache, not error. No voice: I2C probe, then
`YAHBOOM_VOICE_DEVICE` override. Drift: encoders vs IMU cross-check, resync,
short runs. Chat generic: model selected? skills loaded (`GET /api/skills`
lists 4)? Report incidents with correlation_id + stack table + last 20 logs.

## Reference scripts

- `scripts/check_health.py` — REST health/telemetry without an MCP client.
- `scripts/run_patrol_square.ps1` — dual-mode server + dashboard for patrols.
