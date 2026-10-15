---
name: kachaka-ros2-topics
description: >
  kachaka の ROS 2 トピック一覧・読み取り・QoS の扱い。Use when the user wants to read
  kachaka topics (battery, odometry, lidar, imu, camera, map, tf, locations),
  finds `ros2 topic echo` produces no output, hits QoS mismatches (kachaka topics are
  BEST_EFFORT), needs the `--qos-reliability best_effort` flag, or sees the error
  `Failed to create log directory: //.ros/log`. キーワード: ros2 topic, echo, list,
  QoS, BEST_EFFORT, SensorDataQoS, battery_state, odometry, lidar/scan, manual_control.
---

# kachaka の ROS 2 トピック利用

## TL;DR

```sh
# トピック一覧
docker exec -t ros2_bridge-ros2_bridge-1 /opt/kachaka/env.sh ros2 topic list

# echo は --qos-reliability best_effort が必須 (kachakaのトピックはBEST_EFFORTが多い)
docker exec -t ros2_bridge-ros2_bridge-1 /opt/kachaka/env.sh \
  ros2 topic echo --once --qos-reliability best_effort /kachaka/odometry/odometry
```

## QoS の注意 (最頻出ハマりどころ)

**`ros2 topic echo` が無反応** → 9割は QoS 不一致。kachaka のセンサ系トピックの多くは **Reliability: BEST_EFFORT** で publish されている。`ros2 topic echo` のデフォルトは RELIABLE なので、`--qos-reliability best_effort` を付ける。

確認:
```sh
ros2 topic info -v /kachaka/odometry/odometry
# → Reliability: BEST_EFFORT
```

自前ノードを書くときは:
- C++: `rclcpp::SensorDataQoS()`
- Python: `rclpy.qos.qos_profile_sensor_data`

## 主要トピック チートシート

| トピック | 型 | 用途 |
|---|---|---|
| `/kachaka/odometry/odometry` | `nav_msgs/Odometry` | オドメトリ |
| `/kachaka/wheel_odometry/wheel_odometry` | 同上 | 車輪 odom |
| `/kachaka/imu/imu` | `sensor_msgs/Imu` | IMU |
| `/kachaka/lidar/scan` | `sensor_msgs/LaserScan` | 2D LiDAR |
| `/kachaka/front_camera/image_raw` | `sensor_msgs/Image` | 前カメラ |
| `/kachaka/back_camera/image_raw` | `sensor_msgs/Image` | 後ろカメラ |
| `/kachaka/tof_camera/image_raw` | `sensor_msgs/Image` | ToF カメラ |
| `/kachaka/mapping/map` | `nav_msgs/OccupancyGrid` | 地図 |
| `/kachaka/layout/locations/list` | カスタム | 登録位置一覧 |
| `/kachaka/robot_info/battery_state` | `sensor_msgs/BatteryState` | バッテリー |
| `/kachaka/manual_control/cmd_vel` | `geometry_msgs/Twist` | 手動速度指令 (送信用) |
| `/kachaka/goal_pose` | `geometry_msgs/PoseStamped` | 目標位置 (送信用) |
| `/tf`, `/tf_static` | `tf2_msgs/TFMessage` | フレーム |

> 💡 **`battery_state` は `percentage` と `power_supply_status` のみ意味のある値**。`voltage: -1.0`, `present: false` などは kachaka API が埋めていないので無視してOK。

> 💡 **`odometry` の covariance** には信頼度の低い成分に巨大値（1e+16 など）が入る設計。EKFに食わせると勝手に重み付けされる。

## ありがちなエラー

### `Failed to create log directory: //.ros/log`

UID 指定で `docker run` したのに HOME を設定していない。

```sh
docker run --rm -it ... -e HOME=/tmp osrf/ros:humble-desktop-full ...
```

### `ros2 topic list` は出るのに `echo` だけ無反応

1. **`--qos-reliability best_effort` を付け忘れていないか** (これが9割)
2. それでも出ないなら DDS の SHM/コンテナ越境問題 → `kachaka-ros2-env-setup` 参照

## 関連

- 公式リポジトリ（一次情報）: https://github.com/pf-robotics/kachaka-api
- 必要に応じて公式リポジトリの Issues も確認: https://github.com/pf-robotics/kachaka-api/issues
- ブリッジが起動しない / 繋がらない → `kachaka-bridge-setup`
- ROS 2 クライアント環境構築 / DDS 設定 → `kachaka-ros2-env-setup`
- teleop / cmd_vel / goal_pose / rviz2 → `kachaka-ros2-control`
- 人間向けガイド: 同リポジトリ `kachaka-ros2-bridge-guide.md`
