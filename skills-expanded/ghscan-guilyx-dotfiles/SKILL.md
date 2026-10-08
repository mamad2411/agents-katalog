---
name: ros2-cli-debug
description: >-
  Use ROS 2 CLI to inspect topics, nodes, params, lifecycle, actions, and bags;
  includes known echo/pub truncation limits for arrays. Use when debugging a
  live graph, ros2 topic pub/echo quirks, bags, or ros2 doctor output.
---

# ROS 2 CLI Debug

## Graph

```bash
ros2 node list
ros2 node info /name
ros2 topic list
ros2 topic info /topic -v
ros2 topic hz /topic
ros2 topic bw /topic
ros2 interface show <pkg>/msg/<Type>
```

## Echo / pub limits (arrays)

- `ros2 topic echo` truncates long arrays at **128 elements** by default (usability). Use `--full-length` / check current distro flags when you need the whole covariance / mesh.
- `ros2 topic pub` historically fails or truncates when YAML arrays get large (notably **>32** elements on older Dashing/Crystal for covariance-style fields). Prefer a tiny publisher node or `ros2 topic pub` with files / repeated smaller msgs when stuck.
- Fixed-size members in tools like `rqt_plot` may need indexed fields (`covariance[0]`) or alternate viz.

## Params / lifecycle / actions

```bash
ros2 param list /node
ros2 param get /node name
ros2 param set /node name value

ros2 lifecycle list /node
ros2 lifecycle set /node configure
ros2 lifecycle set /node activate

ros2 action list
ros2 action info /action_name
```

## Bags

```bash
ros2 bag record -s mcap /topic_a /topic_b
ros2 bag info <dir>
ros2 bag play <dir> --clock
```

Prefer **MCAP** for new recordings.

## Health

```bash
ros2 doctor
ros2 daemon stop && ros2 daemon start
```

No data on a topic that `hz` sees empty for your node → jump to skill `ros2-qos-dds`.
