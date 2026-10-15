---
name: kachaka-ros2-control
description: >
  kachaka を ROS 2 から動かす (teleop, cmd_vel, goal_pose, rviz2) と、自前コンテナから
  接続する際の実行方法。Use when the user wants to drive kachaka via teleop, send
  `/kachaka/manual_control/cmd_vel`, publish to `/kachaka/goal_pose` for autonomous
  navigation, visualize in rviz2, or separate multiple kachakas via `ROS_DOMAIN_ID`.
  キーワード: teleop, cmd_vel, goal_pose, rviz2, ROS_LOCALHOST_ONLY, ROS_DOMAIN_ID,
  マルチロボット.
---

# kachaka を動かす

## TL;DR

先に `kachaka-ros2-env-setup` で `kachaka-ros2-client` イメージを作り、ブリッジとクライアントの両方に `ROS_LOCALHOST_ONLY=1` を設定しておく。

```sh
docker run --rm -it \
  --network=host \
  -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp \
  -e ROS_LOCALHOST_ONLY=1 \
  kachaka-ros2-client
```

## 動かしてみる

### teleop (キー操作)

クライアントコンテナの中で:

```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r cmd_vel:=/kachaka/manual_control/cmd_vel
```

`i` / `j` / `k` / `l` で前進/旋回。`q` / `z` で速度を変える。

> ⚠️ 走らせる前に **周囲の安全確認** を必ずすること。

### 自律走行 (ゴール送信)

`/kachaka/goal_pose` (`geometry_msgs/PoseStamped`) を publish すると目標位置まで自律走行。
rviz2 で `2D Goal Pose` で送るのが一番楽。

### rviz2 で可視化

```sh
rviz2
```

- Fixed Frame: `odom`
- Add → By Topic → `/kachaka/lidar/scan`, `/kachaka/odometry/odometry`, `/kachaka/mapping/map` など

## 複数 kachaka が同じネットワークにいる場合

`ROS_DOMAIN_ID` を kachaka ごとに分けて、DDS の混線を防ぐ:

```sh
export ROS_DOMAIN_ID=1   # 各 kachaka で異なる値
ROS_LOCALHOST_ONLY=1 RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ./start_bridge.sh <IP>
```

クライアント側でも同じ `ROS_DOMAIN_ID` を `-e` で渡す。ハッカソンやハンズオン会では、あわせて `ROS_LOCALHOST_ONLY=1` も必ず渡す。

## 関連

- 公式リポジトリ（一次情報）: https://github.com/pf-robotics/kachaka-api
- 必要に応じて公式リポジトリの Issues も確認: https://github.com/pf-robotics/kachaka-api/issues
- ブリッジ起動・接続トラブル → `kachaka-bridge-setup`
- ROS 2 クライアント環境構築 → `kachaka-ros2-env-setup`
- トピック仕様・QoS → `kachaka-ros2-topics`
- 人間向けガイド: 同リポジトリ `kachaka-ros2-bridge-guide.md`
