---
name: gazebo-sim
description: >
  Expert guidance for Gazebo Harmonic (Gazebo 8) simulation for ROS 2 — SDF worlds, physics, sensor plugins, and ros_gz_bridge. Use when working with Gazebo, gz sim, simulation, SDF, world file, ros_gz_bridge, ros_gz_sim, spawn model, physics engine, sensor plugin, camera plugin, LiDAR plugin, IMU plugin, GPU ray sensor, differential drive, tracked vehicle, DART physics, Bullet physics, URDF to SDF, collision geometry, inertia tensor, friction, damping, or when a model sinks through the floor, flies away, joints explode, simulation is slow, sensors don't publish, or the bridge to ROS 2 isn't working.
---

# Gazebo Harmonic Simulation Guide

> **Quick navigation**
> - World creation, physics engines, lighting, custom worlds -> `references/world-setup.md`
> - ROS 2 bridging, topic mapping, launch files, spawning models -> `references/ros2-integration.md`
> - Robot models, URDF/SDF, inertia, collision, plugins -> `references/robot-models.md`
> - CLI debugging, physics issues, sensor debugging, diagnostics -> `references/debugging.md`

---

## What Is Gazebo Harmonic?

Gazebo Harmonic (also called Gazebo 8 or "new Gazebo") is the current LTS release of the
Gazebo simulator, part of the rewritten Gazebo project (formerly Ignition). It replaced
"Gazebo Classic" (the `gazebo` command) which reached end-of-life in January 2025.

### Key Differences from Classic Gazebo

| Aspect | Classic Gazebo (`gazebo`) | Gazebo Harmonic (`gz sim`) |
|--------|--------------------------|----------------------------|
| Command | `gazebo`, `gzserver`, `gzclient` | `gz sim`, `gz sim -s` (server), `gz sim -g` (GUI) |
| Model format | SDF + URDF with `<gazebo>` tags | SDF preferred; URDF supported via automatic conversion |
| Transport | Gazebo Transport (custom) | gz-transport (DDS-like, separate from ROS 2 DDS) |
| ROS bridge | `gazebo_ros_pkgs` | `ros_gz_bridge`, `ros_gz_sim`, `ros_gz_image` |
| Plugin API | `ModelPlugin`, `WorldPlugin`, etc. | `System` interface with `ISystemConfigure`, `ISystemPreUpdate`, etc. |
| Physics | ODE (default), Bullet, DART, Simbody | DART (default), Bullet, TPE |
| Topic CLI | `gz topic` (classic) | `gz topic` (new, different API) |
| Environment var | `GAZEBO_MODEL_PATH` | `GZ_SIM_RESOURCE_PATH` |

**If you see `gazebo` commands or `gazebo_ros` packages in a tutorial, it is for Classic Gazebo
and will NOT work with Harmonic.** Always look for `gz sim` commands and `ros_gz_*` packages.

---

## Architecture Overview

Gazebo Harmonic is built from modular libraries. Understanding this architecture helps when
debugging issues or choosing which component to configure.

```
+------------------+     +------------------+     +------------------+
|   gz-sim         |     |   gz-gui         |     |   gz-launch      |
|   (simulation    |     |   (3D viewer,    |     |   (launch system, |
|    orchestrator) |     |    GUI plugins)  |     |    ERB templates) |
+--------+---------+     +--------+---------+     +------------------+
         |                        |
+--------+---------+     +--------+---------+
|   gz-physics     |     |   gz-rendering   |
|   (DART, Bullet, |     |   (OGRE 2.x,     |
|    TPE engines)  |     |    scene graph)   |
+--------+---------+     +--------+---------+
         |                        |
+--------+---------+     +--------+---------+
|   gz-sensors     |     |   gz-transport   |
|   (IMU, LiDAR,   |     |   (pub/sub,      |
|    camera, etc.) |     |    services)     |
+------------------+     +------------------+
```

| Library | What it does | When you care about it |
|---------|-------------|----------------------|
| **gz-sim** | Coordinates physics, sensors, rendering each step | Always -- this is the core |
| **gz-physics** | Runs physics (DART, Bullet, TPE) | Tuning step size, solver iterations, contact parameters |
| **gz-rendering** | Renders the 3D scene (OGRE 2.x) | Camera/depth sensors, GPU ray, visual appearance |
| **gz-sensors** | Simulates sensor behavior and noise | Adding IMU, LiDAR, camera to your robot |
| **gz-transport** | Pub/sub messaging within Gazebo | Bridging to ROS 2, gz topic CLI |
| **gz-gui** | Qt-based GUI, visualization plugins | Debugging visualization, adding GUI panels |
| **gz-launch** | Launch system with ERB templates | Starting complex simulations (prefer ROS 2 launch instead) |

---

## SDF vs URDF: Which Format for Simulation?

| Criteria | SDF | URDF |
|----------|-----|------|
| **Native to Gazebo?** | Yes -- first-class support | Converted to SDF internally |
| **Sensor definitions** | Full support in `<sensor>` tags | Requires `<gazebo>` extension blocks |
| **Plugin attachment** | Clean `<plugin>` tags in model | Via `<gazebo reference="link_name">` extensions |
| **World definition** | Yes -- can define entire worlds | No -- robot-only format |
| **ROS 2 `robot_description`** | Not supported by `robot_state_publisher` | Native format for ROS 2 toolchain |
| **Visual/collision separation** | Full control per link | Full control per link |
| **Reusable includes** | `<include>` tag for model composition | `xacro` for macro-based composition |

### Decision Guide

```
Do you need robot_state_publisher / MoveIt / Nav2?
+-- YES --> Use URDF (with xacro) for the robot description
|           Add <gazebo> extension blocks for sensors and plugins
|           ros_gz_sim will convert URDF to SDF at spawn time
|
+-- NO ---> Is this a world file (environment, not robot)?
            +-- YES --> Use SDF (worlds are SDF-only)
            +-- NO ---> Use SDF for Gazebo-only models, URDF if ROS tools needed
```

**Practical recommendation:** Use URDF+xacro for robot models (so they work with the full
ROS 2 toolchain) and SDF for world files. This is the most common pattern in the ROS 2
ecosystem.

---

## Common Physics Issues Diagnosis

When something goes wrong in simulation, it is almost always a physics configuration problem.
Here are the most common symptoms and their fixes.

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Model sinks through floor | Missing `<collision>` element on a link | Add `<collision>` geometry to every link that should interact physically |
| Model sinks slowly | Mass too high for default contact parameters | Reduce mass, increase `<kp>` (contact stiffness), or decrease physics step size |
| Model flies away on spawn | Inertia values wildly wrong (e.g., all zeros or copy-paste error) | Recalculate inertia using `gz sdf --inertial-stats` or MeshLab |
| Joints explode / oscillate | Damping too low, step size too large, or conflicting joint limits | Increase `<damping>`, decrease `<max_step_size>`, check joint limits |
| Robot slides on flat ground | Friction coefficients too low | Increase `<mu>` and `<mu2>` in `<surface><friction>` |
| Robot vibrates in place | Physics step size too large for the mass/stiffness ratio | Decrease `<max_step_size>` to 0.0005 or lower |
| Tracked vehicle does not move | Diff-drive plugin on tracked vehicle | Use `TrackedVehicle` plugin instead of `DiffDrive` |
| Simulation runs but nothing moves | Model is `<static>true</static>` | Set `<static>false</static>` for dynamic models |
| Two models pass through each other | Both are `<static>true</static>` | Static-static collision is not computed; make at least one dynamic |

**The #1 beginner mistake:** Defining `<visual>` geometry but forgetting `<collision>` geometry.
The model looks fine but has no physical presence. Always define both.

---

## Sensor Plugin Selection Guide

Gazebo Harmonic includes built-in sensor plugins. You do not need to compile custom plugins
for standard sensors.

| Sensor | SDF `<sensor type="">` | Gazebo Topic Type | ROS 2 Message (via bridge) | Notes |
|--------|----------------------|-------------------|---------------------------|-------|
| IMU | `imu` | `gz.msgs.IMU` | `sensor_msgs/msg/Imu` | Attach to robot base link |
| 2D LiDAR | `gpu_lidar` | `gz.msgs.LaserScan` | `sensor_msgs/msg/LaserScan` | GPU-accelerated, use for 2D scans |
| 3D LiDAR | `gpu_lidar` | `gz.msgs.PointCloudPacked` | `sensor_msgs/msg/PointCloud2` | Same plugin, multiple vertical rays |
| Camera (RGB) | `camera` | `gz.msgs.Image` | `sensor_msgs/msg/Image` | Set `<width>`, `<height>`, `<format>` |
| Depth Camera | `depth_camera` | `gz.msgs.Image` (depth) | `sensor_msgs/msg/Image` | Outputs 32-bit float depth image |
| RGBD Camera | `rgbd_camera` | `gz.msgs.Image` + depth | `sensor_msgs/msg/Image` x2 | Combined color + depth |
| Contact Sensor | `contact` | `gz.msgs.Contacts` | `ros_gz_interfaces/msg/Contacts` | Requires `<collision>` element name |
| Altimeter | `altimeter` | `gz.msgs.Altimeter` | `sensor_msgs/msg/FluidPressure` | Height above ground |
| Magnetometer | `magnetometer` | `gz.msgs.Magnetometer` | `sensor_msgs/msg/MagneticField` | Simulated compass |
| Air Pressure | `air_pressure` | `gz.msgs.FluidPressure` | `sensor_msgs/msg/FluidPressure` | Barometric pressure |

### Adding Noise to Sensors

All sensors support Gaussian noise configuration. Always add noise for realistic simulation:

```xml
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate>
  <imu>
    <angular_velocity>
      <x><noise type="gaussian">
        <mean>0.0</mean>
        <stddev>0.01</stddev>
      </noise></x>
      <!-- repeat for y, z -->
    </angular_velocity>
    <linear_acceleration>
      <x><noise type="gaussian">
        <mean>0.0</mean>
        <stddev>0.1</stddev>
      </noise></x>
      <!-- repeat for y, z -->
    </linear_acceleration>
  </imu>
</sensor>
```

---

## Performance Optimization Tips

Simulation performance is measured by **Real-Time Factor (RTF)**. An RTF of 1.0 means the
simulation runs at real-world speed. Below 1.0 means it is slower than real time.

### Quick Wins

| Optimization | Impact | How |
|-------------|--------|-----|
| Simplify collision geometry | High | Use primitives (box, cylinder, sphere) instead of mesh for collision |
| Reduce LiDAR ray count | High | Use fewer horizontal/vertical samples; 360 rays is usually enough for 2D |
| Lower camera resolution | Medium | Use 320x240 for development; increase for final testing only |
| Increase physics step size | Medium | `<max_step_size>0.002</max_step_size>` (default 0.001) -- but may reduce accuracy |
| Reduce sensor update rates | Medium | IMU at 100 Hz, LiDAR at 10 Hz, camera at 15 Hz is usually sufficient |
| Use headless mode | Medium | `gz sim -s` (server only, no GUI rendering) |
| Disable shadows | Low | In GUI settings or world SDF `<scene><shadows>false</shadows></scene>` |

### Performance Budget

For a single robot with sensors on a typical development machine:

| Component | Budget |
|-----------|--------|
| Physics (DART) | ~20% of step time |
| LiDAR (GPU ray) | ~30% of step time |
| Camera rendering | ~30% of step time |
| Sensor processing | ~10% of step time |
| Other (transport, etc.) | ~10% of step time |

If RTF drops below 0.5, check `gz sim --levels` output and consider reducing sensor fidelity
or switching to headless mode for algorithm development.

---

## Physics Engine Selection

| Engine | Best For | Limitations |
|--------|----------|------------|
| **DART** (default) | General robotics, articulated bodies, accurate contacts | Slower than Bullet for large scenes |
| **Bullet** | Large environments, many objects, gaming-style physics | Less accurate joint constraints |
| **TPE** (Trivial Physics Engine) | Non-physics testing, kinematic-only scenarios | No contact forces or joint constraints, no friction; use for pure sensing pipelines |

**Recommendation:** Start with DART (the default). Only switch to Bullet if you have
performance issues with many objects, or TPE if you only need kinematic motion for
testing sensor pipelines.

---

## Essential Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `GZ_SIM_RESOURCE_PATH` | Additional model/world search paths | `export GZ_SIM_RESOURCE_PATH=$HOME/my_models:$GZ_SIM_RESOURCE_PATH` |
| `GZ_SIM_SYSTEM_PLUGIN_PATH` | Custom plugin search paths | `export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/my_plugins/lib` |
| `GZ_PARTITION` | Isolate Gazebo transport namespaces | `export GZ_PARTITION=my_sim` |
| `GZ_IP` | Network interface for multi-machine sim | `export GZ_IP=192.168.1.100` |
| `GZ_VERBOSE` | Log verbosity (0-4) | `export GZ_VERBOSE=3` |

---

## Common Gazebo Harmonic Packages (ROS 2)

Install these for ROS 2 Jazzy + Gazebo Harmonic integration:

```bash
# Core Gazebo Harmonic (if not installed with ROS)
sudo apt install gz-harmonic

# ROS 2 <-> Gazebo bridge packages (use your ROS 2 distro)
sudo apt install ros-${ROS_DISTRO}-ros-gz-bridge
sudo apt install ros-${ROS_DISTRO}-ros-gz-sim
sudo apt install ros-${ROS_DISTRO}-ros-gz-image

# Convenience metapackage
sudo apt install ros-${ROS_DISTRO}-ros-gz
```

**Version compatibility matrix:**

| ROS 2 Distro | Gazebo Version | Bridge Package |
|--------------|----------------|----------------|
| Humble | Fortress (default) or Harmonic | `ros-humble-ros-gz` |
| Iron | Fortress or Harmonic | `ros-iron-ros-gz` |
| Jazzy | Harmonic (default) | `ros-jazzy-ros-gz` |

---

## Coordinate Systems and Units

Gazebo uses the **Z-up** coordinate convention and **metric** units throughout.

| Quantity | Unit | Convention |
|----------|------|-----------|
| Length | meters (m) | All dimensions, positions |
| Mass | kilograms (kg) | All mass values |
| Time | seconds (s) | Step size, rates |
| Angle | radians (rad) | Joint positions, orientations |
| Force | newtons (N) | Applied forces, contact forces |
| Torque | newton-meters (N*m) | Joint torques |
| Temperature | kelvin (K) | Thermal sensor |

### Pose Format

Poses in SDF use `<pose>x y z roll pitch yaw</pose>` where:
- x, y, z are position in meters
- roll, pitch, yaw are orientation in radians (Euler angles, intrinsic XYZ)

```xml
<!-- Model at x=1, y=2, z=0 with 90-degree rotation around Z -->
<pose>1.0 2.0 0.0 0 0 1.5708</pose>
```

---

## Quick Start: First Simulation in 5 Minutes

For those who want to see something working immediately before diving into the details.

```bash
# 1. Create a minimal world file
cat > /tmp/test_world.sdf << 'EOF'
<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="test_world">
    <physics name="default" type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <light type="directional" name="sun">
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <direction>-0.5 0.1 -0.9</direction>
    </light>
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="c"><geometry><plane><normal>0 0 1</normal></plane></geometry></collision>
        <visual name="v"><geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry></visual>
      </link>
    </model>
  </world>
</sdf>
EOF

# 2. Launch it
gz sim /tmp/test_world.sdf

# 3. In the GUI, right-click to add shapes from the toolbar
# 4. Use gz topic -l in another terminal to see what is published
```

---

## Typical Workflow

```
1. Create/edit world SDF file
   --> See references/world-setup.md

2. Create/edit robot model (URDF or SDF)
   --> See references/robot-models.md

3. Write ROS 2 launch file to start Gazebo + spawn robot + bridge topics
   --> See references/ros2-integration.md

4. Run simulation, debug issues
   --> See references/debugging.md

5. Iterate: tune physics, add sensors, improve world
```

---

## Reference File Index

| File | Read when |
|------|-----------|
| `references/world-setup.md` | Creating simulation environments, configuring physics engines, adding lighting, building custom worlds |
| `references/ros2-integration.md` | Bridging Gazebo and ROS 2, writing launch files, spawning models, synchronizing clocks |
| `references/robot-models.md` | Building robot models, URDF/SDF conversion, inertia calculation, adding sensors and plugins |
| `references/debugging.md` | Diagnosing physics issues, CLI debugging tools, sensor debugging, performance profiling |
