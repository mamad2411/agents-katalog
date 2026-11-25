---
title: MythicMobs 额外词条
description: ArcartX 为 MythicMobs 提供的自定义技能词条
---

import { Step, Steps } from 'fumadocs-ui/components/steps';
import { Callout } from 'fumadocs-ui/components/callout';

## MythicMobs 额外词条

ArcartX 为 MythicMobs 提供了一系列自定义技能词条。以下是所有可用的词条及其参数说明。

每个参数都支持缩写和全名两种写法，例如 `m` 和 `model` 等价。

### 模型相关

```yaml
# 设置实体模型
# m(model): 模型 ID，为空则删除模型（默认 ""）
# s(scale): 缩放大小（默认 1.0）
# r(reset): 是否重置上下文（默认 true）
# r 为 false 时不会更新模型上下文，适用于骨骼相同的模型动态切换而不中断动画
model{m=model_id; s=1; r=true} @self
```

```yaml
# 播放动画
# n(name): 动作名（默认 "idle"）
# t(transitionTime): 过渡时长，单位 tick（默认 5）
# s(speed): 播放速度（默认 1.0）
# k(time): 持续时间，单位 tick，-1 为播放一次（默认 -1）
animation{n=idle; t=5; s=1; k=-1} @self
```

```yaml
# 隐藏骨骼
# b(bone): 骨骼名（默认 "head"）
# h(hide): 是否隐藏（默认 true）
hideBone{b=head; h=true} @self
```

```yaml
# 设置动作替换
# s(state): 状态名（默认 "idle"）
# a(animation): 替换为的动作名（默认 "idle"）
defaultState{s=idle; a=idle2} @self
```

### 碰撞与代理

```yaml
# 设置碰撞体积
# w(width): 宽度（默认 1.0）
# h(height): 高度（默认 1.0）
hitbox{w=1; h=1} @self
```

```yaml
# 代理碰撞箱
# 生成一个隐形实体代替本体接受伤害，解决体积变大后寻路 AI 异常的问题
# 使用前需要先关闭本体的碰撞功能
# w(width): 宽度（默认 1.0）
# h(height): 高度（默认 1.0）
# u(update): 是否更新已存在的代理碰撞箱大小（默认 false）
# r(remove): 是否移除代理碰撞箱（默认 false）
hitboxProxy{w=10; h=10} @self
hitboxProxy{w=11; h=11; u=true} @self
hitboxProxy{r=true} @self
```

<Callout type="info">
    代理碰撞箱不会被 MythicMobs 范围技能选中（处理方式类似 MythicMobs 与 ModelEngine 的兼容）。在某些情况下，你可能需要对其它技能插件进行额外兼容。
</Callout>

### 坐骑系统

通过代理碰撞箱实现坐骑功能，支持船、地面生物、车辆、飞行、潜艇五种类型。

```yaml
# 设置坐骑类型
# t(type): 坐骑类型（默认 "NONE"）
# 可选值: GROUND(地面) | FLY(飞行) | BOAT(船) | CAR(车辆) | DIVING(潜艇) | NONE(关闭)
proxyMountType{t=GROUND} @self
```

```yaml
# 设置坐骑速度
# s(moveSpeed): 移动速度（默认 0.3）
# fu(flyUpSpeed): 飞行上升速度（默认 0.08）
# fd(flyDownSpeed): 飞行下降速度（默认 0.06）
# bt(boatTurnSpeed): 船转向速度（默认 2.0）
proxyMountSpeed{s=0.3; fu=0.08; fd=0.06; bt=2.0} @self
```

```yaml
# 添加额外座位
# x/y/z: 座位相对于代理实体的偏移坐标（默认均为 0.0）
proxyAddSeat{x=0; y=0; z=1} @self
```

<Callout type="info">
    使用坐骑功能前，需要先通过 `hitboxProxy` 创建代理碰撞箱，再设置坐骑类型和速度。玩家右键代理实体即可上车。
</Callout>

### 音效与特效

```yaml
# 播放 3D 音效
# s(sound): 音频文件路径（默认 "null"，即不播放）
# c(category): 音频类型（默认 "master"）
# d(distOrRoll): 范围（默认 16）
# p(pitch): 音调（默认 1.0）
# k(keepTime): 持续时间，单位毫秒（默认 2000）
sound3d{s=sounds/hit.ogg; c=master; d=16; p=1; k=2000} @self
```

```yaml
# 在目标实体位置播放锤地特效（同步给可以看到该实体的玩家）
# r(radius): 半径（默认 3.0）
# d(depth): 深度（默认 0.3）
# i(in): 进入时间（默认 10）
# k(keep): 持续时间（默认 40）
# o(out): 退出时间（默认 20）
# m(mode): 动画类型 0|1|2（默认 0）
hammerEffect{r=3; d=0.3; i=10; k=40; o=20; m=0} @self
```

### UI 与相机

```yaml
# 向目标玩家发送 UI 通讯包，触发 UI 的 packetHandler
# u(ui): 界面 ID（默认 ""）
# ph(packetHandler): 处理器名称（默认 ""）
# pack/p: 包内容，字符串（默认 ""）
uiPacket{u=my_ui; ph=handler_name; pack=data}
# 注意，这个要选择目标，而不是@self，@self是发给释放者
```

```yaml
# 摇晃目标镜头
# d(duration): 持续 tick（默认 20）
# a(amplitude): 幅度（默认 14）
cameraShake{d=20; a=14} @target
```

### 基岩粒子

```yaml
# 在目标实体位置播放基岩粒子
# id(pid): 粒子 ID（默认 ""）
bedrockParticle{id=magic}
```

## 自定义词条名称

如果你使用的其它插件和 ArcartX 的词条名称冲突，可以在 `plugins/ArcartX/link/mythicmobs_key_words.yml` 中修改词条名称。

<Callout type="warn">
    修改词条名称后需要重启服务端才会生效。
</Callout>

<Callout type="info">
    如果你从旧版本升级，原来位于 `mythicmobs/key_words.yml` 的配置文件会自动迁移到 `link/mythicmobs_key_words.yml`。
</Callout>
