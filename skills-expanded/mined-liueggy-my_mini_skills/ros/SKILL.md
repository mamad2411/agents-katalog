---
name: ros
description: 当用户提到 ROS、ROS1、ROS2、catkin、colcon、roscore、topic、service、action、launch、rviz、gazebo、tf、urdf、xacro、slam、nav2、机器人中间件、机器人节点通信、传感器驱动、导航栈、机械臂 ROS 集成，或希望学习、搭建、调试、解释、编写、运行 ROS/ROS 2 工程时使用此技能。也用于创建最小示例节点、工作空间、launch 文件、消息接口示例、诊断通信问题、解释架构与数据流、比较 ROS1 与 ROS2、以及为具体机器人项目设计软件结构。
---

# ROS Skill

默认优先适配 **Ubuntu 20.04 + ROS Noetic（ROS1）**。如果用户没有特别说明版本，且上下文明显是 Noetic/catkin/roscore/roslaunch，就按 ROS Noetic 回答；如果用户明确提到 ROS2、colcon、ament、ros2 命令，再切换到 ROS2 方案。

在处理 ROS/ROS 2 请求时，优先判断用户目标属于哪一类：
1. 学习概念：解释架构、通信模型、坐标系、工作空间、构建系统。
2. 编码实现：创建 publisher/subscriber、service、action、launch、URDF/Xacro、参数文件。
3. 环境搭建：安装 ROS、创建 workspace、配置依赖、构建与运行。
4. 调试排障：topic 不通、节点找不到、TF 断裂、构建失败、依赖缺失。
5. 项目设计：为移动机器人、机械臂、SLAM、导航、仿真设计模块结构。

## 核心原则

- 默认环境优先按 **Ubuntu 20.04 + ROS Noetic** 组织命令与示例。
- 先区分 **ROS 1** 还是 **ROS 2**；如果用户给出 `roscore`、`catkin_make`、`rosrun`、`roslaunch`，通常就是 ROS1/Noetic。
- 所有建议都尽量围绕用户的 Ubuntu 版本、机器人硬件、仿真/实机环境展开。
- 对初学者优先给“最小可运行示例”；对工程问题优先给“可验证的排障步骤”。
- 解释概念时，尽量结合机器人数据流：传感器 → 感知/定位 → 规划 → 控制 → 执行器。
- 如果涉及文件创建，按 catkin 工作空间结构组织清晰路径。

## 快速判断框架

### 一、如果用户是在“学 ROS”
重点解释：
- node：独立进程/功能模块
- topic：发布订阅，适合连续数据流
- service：同步请求响应
- action：长任务，可反馈、可取消
- parameter：配置项
- tf/tf2：坐标系变换树
- launch：批量启动与参数编排
- bag：录制与回放数据
- rviz / rqt：可视化与调试
- catkin（ROS1）/ colcon + ament（ROS2）：构建系统

### 二、如果用户要“写代码”
先确认：
- ROS 版本：ROS1 / ROS2
- 语言：Python / C++
- 包名、节点名、话题名
- 输入输出消息类型

默认交付顺序：
1. 包结构
2. 节点代码
3. package.xml / CMakeLists.txt（如需要）
4. launch 文件
5. 构建与运行命令
6. 验证命令（如 `rostopic list` 或 `ros2 topic list`）

### 三、如果用户要“排障”
按以下顺序排查：
1. 环境是否 source 正确
2. 工作空间是否成功构建
3. 节点是否实际启动
4. topic / service / action 名称是否匹配
5. ROS master（ROS1）或 DDS 发现（ROS2）是否正常
6. TF 树是否连通
7. 时间源是否一致（仿真时间 / 实时时钟）
8. 依赖包和消息接口是否齐全

## Noetic 常见命令模板

### 环境与工作空间
- `source /opt/ros/noetic/setup.bash`
- `mkdir -p ~/catkin_ws/src`
- `cd ~/catkin_ws && catkin_make`
- `source ~/catkin_ws/devel/setup.bash`
- `echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc`

### 启动与运行
- `roscore`
- `rosrun <package_name> <node_name>`
- `roslaunch <package_name> <file.launch>`
- `rosnode list`
- `rosnode info <node_name>`

### Topic 调试
- `rostopic list`
- `rostopic echo <topic_name>`
- `rostopic hz <topic_name>`
- `rostopic type <topic_name>`
- `rostopic pub <topic_name> <msg_type> '<yaml_data>'`

### Service 调试
- `rosservice list`
- `rosservice info <service_name>`
- `rosservice type <service_name>`
- `rosservice call <service_name> <args>`

### 参数与消息
- `rosparam list`
- `rosparam get <param_name>`
- `rosparam set <param_name> <value>`
- `rosmsg show <msg_type>`
- `rossrv show <srv_type>`

### TF / 可视化 / 录包
- `rosrun tf view_frames`
- `rosrun rqt_tf_tree rqt_tf_tree`
- `rviz`
- `rqt_graph`
- `rosbag record -a`
- `rosbag play <bag_file>`
- `rosbag info <bag_file>`

### 构建与依赖
- `catkin_create_pkg <pkg_name> rospy roscpp std_msgs`
- `cd ~/catkin_ws && catkin_make`
- `catkin_make clean`
- `rospack find <package_name>`
- `roscd <package_name>`
- `rosdep install --from-paths src --ignore-src -r -y`

## 常用解释模板

### ROS 是什么
ROS 不是传统操作系统，而是机器人软件框架与工具链。核心思路是把系统拆成多个节点，通过标准消息接口通信。

### Noetic 的定位
ROS Noetic 是 ROS1 的长期支持发行版，常见于 Ubuntu 20.04，常配合 catkin、Python3、roscore、roslaunch 使用。

### ROS1 与 ROS2 的关键差别
- ROS1：依赖 roscore/master，生态成熟，上手快。
- ROS2：基于 DDS，去中心化发现，QoS 更强，更适合工程化与实时场景。

### 典型移动机器人数据流
- 激光/相机/IMU 发布传感器数据
- 定位/SLAM 节点输出位姿和地图
- 规划节点计算路径
- 控制节点输出速度指令
- 驱动节点执行到底盘

## 实操建议

- 生成代码时优先给最小可运行示例，再给扩展方向。
- 如果是 Noetic，默认采用 catkin 工作空间和 Python3。
- 提供命令时注明在哪个目录运行。
- 若用户给出报错，优先基于报错文本逐条定位，而不是泛泛解释。
- 若用户要搭项目骨架，可建议以下目录思路：
  - `src/`：源码包
  - `launch/`：启动文件
  - `config/`：参数 YAML
  - `urdf/`：机器人模型
  - `rviz/`：可视化配置
  - `scripts/`：辅助脚本

## 配套参考文件

按需读取以下文件，不必一次性展开：
- `references/noetic-cli-cheatsheet.md`
- `references/noetic-workspace-guide.md`
- `references/common-errors.md`
- `references/architecture-patterns.md`

## 回答风格

- 对初学者：先讲整体图景，再讲名词。
- 对 Noetic 开发者：直接给命令、目录、代码和验证步骤。
- 对架构问题：画清楚节点、话题、服务、动作、TF 关系。
- 对 ROS2 问题：不要误用 Noetic 命令，改用 ROS2 命令体系。

## 何时需要进一步追问

仅在以下关键信息缺失时追问：
- 当前到底是 ROS1/Noetic 还是 ROS2
- 目标系统（Ubuntu / Docker / 板卡）
- Python 还是 C++
- 真实机器人还是仿真
- 当前报错或期望行为

如果用户明确说是 Ubuntu 20.04 + Noetic，则直接按 Noetic 提供方案，无需再次确认。
