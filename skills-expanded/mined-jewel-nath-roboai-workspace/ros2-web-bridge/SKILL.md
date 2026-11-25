---
name: ros2-web-bridge
description: >-
  Connect a ROS 2 Jazzy robot to a browser or a non-ROS program: rosbridge_suite with roslibjs or roslibpy,
  foxglove_bridge, camera streams (web_video_server, compressed images), or a FastAPI service wrapping rclpy
  (executor thread, async service calls, cmd_vel watchdog); kept off the internet with localhost binds and a login.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-18
---

# ROS 2 web bridge

Gets robot data into a web page or a program without ROS, and commands back, without opening the
robot to the network. Checked against the Jazzy releases on 2026-11-18: rosbridge_suite 2.7.1,
foxglove_bridge 3.6.3, web_video_server 3.1.0, roslib 2.1.0 (npm), roslibpy 2.1.0. Not run.

## When to use

- A browser dashboard or teleop page for a robot.
- A camera feed in a web page.
- A program without ROS (a Windows tool, a phone app, a cloud service, a test script) that reads
  topics or calls services.
- Connecting the Foxglove app to a live robot.
- Exposing a few robot functions as an HTTP API.

Not here: nodes, QoS and launch basics ([ros2-core](../ros2-core/SKILL.md)); computers that both
run ROS 2 (use the middleware, see
[choose a ROS 2 middleware](../../wiki/guides/choose-a-ros2-middleware.md)); fleet and cloud
operations (a later `ops-` skill).

## Choose the bridge

| Need | Use | Why |
|---|---|---|
| Dashboard or teleop in a browser, quickly | rosbridge_suite + roslibjs | JSON over WebSocket to any topic, service or action; no server code |
| A Python or other non-ROS program | rosbridge + roslibpy (or any WebSocket client) | No ROS install on that machine |
| Engineers inspecting plots, 3D, logs | foxglove_bridge + the Foxglove app | Binary messages, high rates, built for debugging |
| A camera in a page | web_video_server, or a compressed topic | MJPEG plays in an `<img>` tag |
| Operators across a network, a fixed API, input checks | A FastAPI service on rclpy | Exposes five endpoints, not the whole ROS graph |

They combine: a FastAPI service for commands and web_video_server for video, both behind one
proxy, is a common production shape.

## Quick start

rosbridge on the robot itself, browser on the same machine:

```bash
sudo apt install ros-jazzy-rosbridge-suite
ros2 launch rosbridge_server rosbridge_websocket_launch.xml address:=127.0.0.1
```

```js
import { Ros, Topic } from "roslib";  // npm install roslib@2

const ros = new Ros({ url: "ws://127.0.0.1:9090" });
new Topic({ ros, name: "/odom", messageType: "nav_msgs/msg/Odometry", throttle_rate: 200 })
  .subscribe((msg) => console.log(msg.pose.pose.position));
```

Check: `ss -ltnp | grep 9090` shows `127.0.0.1:9090`, and positions print, at most 5 times a
second.

## Workflow

### 1. Decide what crosses the bridge

List each topic, service and action the client needs, its direction and the rate the screen
really needs (for example 1 Hz for a status panel, 10 Hz for a pose display). Start read-only;
allow writes only to `/cmd_vel` and named services.

Check: a written list exists, and everything else stays off the bridge.

### 2. Run the bridge locked down

- rosbridge: a launch file in your bringup package that sets `address` to `127.0.0.1` and
  `topics_sub_glob`, `topics_pub_glob`, `services_glob` and `params_glob` from the list in step 1.
  The glob values need inner quotes (`'[/odom, /cmd_vel]'`); the full file is in
  [references/rosbridge-clients.md](references/rosbridge-clients.md).
- foxglove_bridge: `ros2 launch foxglove_bridge foxglove_bridge_launch.xml address:=127.0.0.1`
  plus `topic_whitelist` and `capabilities`
  ([references/secure-access.md](references/secure-access.md)).

Check: `ss -ltnp` shows only `127.0.0.1`; a publish to a topic outside the globs leaves a warning
in the `rosbridge_websocket` log and reaches no subscriber.

### 3. Write the client

- roslibjs 2 is an ES module: `import { Ros, Topic, Service } from "roslib"`. Publish plain
  objects; `ROSLIB.Message` and the global `ROSLIB` belong to roslib 1.x tutorials.
- Every subscription gets `throttle_rate` (ms) and `queue_length: 1` unless the page truly needs
  every message.
- Use full type names (`geometry_msgs/msg/TwistStamped`); `ros2 topic info <topic>` gives them.
- `callServiceAsync(request, timeoutSeconds)` for services; handle the rejection.
- Reconnect yourself on `close` (roslib resubscribes once `connect()` succeeds).
- roslibpy: `client.run()` once, `client.terminate()` once at the end.

Check: values update at the throttled rate; the browser's network panel shows the WebSocket
message rate you expect.

### 4. Make teleop fail safe

- Send commands at a steady rate (10 Hz) only while a control is held; on release, window blur,
  hidden tab and socket close, send zero.
- The real stop is on the robot: `diff_drive_controller`'s `cmd_vel_timeout` (see
  [ros2-control](../ros2-control/SKILL.md)) or the FastAPI watchdog. The browser cannot be
  trusted to send the last zero.
- `diff_drive_controller` on Jazzy needs `TwistStamped`. Leave the stamp at zero: the controller
  stamps it on arrival. A browser-clock stamp can be "too old" and get dropped.

Check, wheels off the ground: drive, then kill the browser tab or pull the network cable. The
wheels stop within the command timeout.

### 5. Stream the camera

Use the camera's `/compressed` topic, never raw images. web_video_server with
`type=ros_compressed` forwards the JPEG frames without re-encoding; a throttled rosbridge
subscription works for small previews. Details: [references/camera-streaming.md](references/camera-streaming.md).

Check: `ros2 topic hz` on the compressed topic, the frame rate in the browser, and the robot's
CPU load with the stream open.

### 6. Write a FastAPI service when you need a narrow API

Full service: [references/fastapi-rclpy.md](references/fastapi-rclpy.md).

- In FastAPI's `lifespan`: `rclpy.init(signal_handler_options=SignalHandlerOptions.NO)`, one node
  in a `SingleThreadedExecutor` spun on a daemon thread; on exit send zero, shut the executor
  down, destroy the node, `rclpy.try_shutdown()`.
- Shared data crosses threads only through methods that take a lock.
- Await service calls by moving the rclpy future's result onto the event loop
  (`loop.call_soon_threadsafe`); never `spin_until_future_complete` on the spinning node.
- Validate input with pydantic ranges, clamp again in the node, reject NaN, and run a
  command watchdog timer in the node.
- One uvicorn process on `127.0.0.1`.

Check: the `curl` tests in the reference pass (clamped command, watchdog zero, 422 on bad input),
and Ctrl-C exits without a traceback.

### 7. Put everything behind one secure entry point

None of these bridges checks who connects. For one engineer use an SSH tunnel; for a team a VPN;
for a dashboard a reverse proxy with TLS and a login, serving page, WebSocket, video and API from
one origin. Never forward a bridge port to the internet. Config and checks:
[references/secure-access.md](references/secure-access.md).

Check: from another machine the raw ports refuse connections and the proxy asks for a login.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Robot keeps driving after the tab closes | Last command was non-zero and nothing timed out | Controller `cmd_vel_timeout` or node watchdog; dead-man client |
| Web server works but ROS callbacks stop | `spin_until_future_complete` moved the node out of the background executor | Await the future on the event loop (reference) |
| Every request freezes while one waits | Blocking rclpy or `time.sleep` inside `async def` | Await properly, or use a plain `def` endpoint |
| Publish "does nothing" | Glob refused it (only logged), or `Twist` sent where `TwistStamped` is needed | Read the rosbridge log; `ros2 topic info -v` |
| rosbridge fails to start after adding globs | Glob passed without inner quotes became a string array | `value="'[/odom, /cmd_vel]'"` |
| Page stalls when the camera is on | Raw images through JSON | Compressed topic, throttle, or web_video_server |
| WebSocket drops after a minute through a proxy | Proxy idle timeout | Raise `proxy_read_timeout`, or set rosbridge `websocket_ping_interval` |
| Two copies of the API node | uvicorn started with several workers | One process |
| `pip install fastapi` refused on Ubuntu 24.04 | PEP 668 system Python | `apt install python3-fastapi python3-uvicorn`, or a `--system-site-packages` venv |
| roslibpy hangs when reconnecting in the same script | Twisted's loop cannot restart | One client per process; `terminate()` only at exit |
| Anyone on the LAN can drive the robot | Default binds on all interfaces, no login, any origin | `127.0.0.1` binds and the proxy |

## Checks

- `ss -ltnp`: every bridge port on `127.0.0.1`; only the proxy or VPN listens outside.
- From another host: raw ports refused, proxy asks for a login.
- A publish outside the allowed list is refused; an out-of-range API command returns 422.
- Kill-the-tab test stops the robot within the command timeout.
- Browser network panel and `ros2 topic hz` agree with the rates chosen in step 1.

## Distro differences

- **Humble**: rosbridge has the same launch arguments; `diff_drive_controller` can take plain
  `Twist` with `use_stamped_vel: false`.
- **Lyrical**: rosbridge 4.x drops BSON mode (`bson_only_mode`); foxglove_bridge (3.6.3) and
  web_video_server (3.1.1) keep the same parameters.

## Related

- Wiki: [rosbridge_suite](../../wiki/software/rosbridge-suite.md),
  [Foxglove](../../wiki/tools/foxglove.md), [ROS 2](../../wiki/tools/ros2.md),
  [rmw_zenoh](../../wiki/software/rmw-zenoh.md) when the remote side can run ROS 2.
- Skills: [ros2-core](../ros2-core/SKILL.md), [ros2-control](../ros2-control/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md). Later: perception (cameras), bringup and safety.
- Upstream: rosbridge_suite `ROSBRIDGE_PROTOCOL.md`, roslibjs `packages/roslib`, foxglove-sdk
  `ros/src/foxglove_bridge`, web_video_server README.
