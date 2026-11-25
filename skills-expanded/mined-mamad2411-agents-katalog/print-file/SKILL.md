---
name: print-file
version: 0.1.0
description: 本地打印文件——发现和控制当前打印设备，把 PDF/文档/图片发送到打印机。每次打印前必须确认纸张大小和黑白/彩色；默认 A4、黑白。适合用户说“打印/打出来/print/把这个文件送打印机”。【重要】必须先读 skill 原文获取正确流程，禁止直接盲打。
---

# 本地打印文件

## 适用场景

用户要求打印本地文件、刚生成的文件、PDF、图片或文档时使用此 skill。

## 核心规则

- 每次打印前必须向用户确认：
  - 纸张大小，默认 `A4`
  - 打印颜色，默认 `黑白`
- 如果用户已经在同一句话明确指定纸张和颜色，可不再追问。
- 不要在未确认纸张和颜色时直接提交打印任务。
- 打印前先确认文件真实存在。
- 优先使用系统默认打印机；如果没有默认打印机，列出可用打印机并让用户选择。
- 如果 `lpstat` 在沙箱内查不到打印机，使用 escalated 权限重试；这通常是 macOS 打印服务访问受限，不代表没有打印机。

## 标准流程

1. 定位文件：

```bash
ls -lh "<file>"
```

2. 查询打印机：

```bash
lpstat -d
lpstat -e
lpstat -p
```

3. 查询目标打印机支持的纸张和颜色选项：

```bash
lpoptions -p "<printer>" -l
```

4. 向用户确认设置。推荐问法：

```text
准备打印 <file> 到 <printer>。纸张用 A4、黑白打印，可以吗？
```

如果用户要改，接受常见值：

| 用户说法 | CUPS 常用值 |
|---|---|
| A4 | `A4` |
| A5 | `A5` |
| Letter | `Letter` |
| 黑白 / 灰度 | `Gray` 或 `monochrome` |
| 彩色 | `RGB` 或 `color` |

5. 提交打印任务。

优先使用通用 CUPS 选项：

```bash
lp -d "<printer>" -o media=A4 -o ColorModel=Gray "<file>"
```

如果打印机不支持 `ColorModel=Gray`，根据 `lpoptions -p "<printer>" -l` 的输出改用实际选项，例如：

```bash
lp -d "<printer>" -o media=A4 -o print-color-mode=monochrome "<file>"
lp -d "<printer>" -o media=A4 -o cupsPrintQuality=Draft "<file>"
```

6. 回报任务号并检查队列：

```bash
lpstat -W not-completed -o "<printer>"
lpstat -p "<printer>" -l
```

## 重新打印

如果用户说“再来一次/重新打印/再打一份”，先查队列：

```bash
lpstat -W not-completed -o "<printer>"
```

- 如果旧任务仍在队列里，先询问是否取消旧任务，避免重复打印。
- 如果用户明确表示旧任务失败、缺纸后重试、卡住了，取消旧任务再重新提交：

```bash
cancel "<job-id>"
lp -d "<printer>" -o media=A4 -o ColorModel=Gray "<file>"
```

## 故障处理

- 红灯、缺纸、卡纸、缺墨等硬件状态通常只能由用户在打印机上处理；CLI 只能看到队列状态。
- `lpstat` 显示任务一直在 `not-completed`：提示用户检查纸张、卡纸、墨水、打印机电源和 USB/Wi-Fi 连接。
- 打印机离线或暂停时，先报告状态，不要反复提交多份任务。
- 用户补纸后要重新打：取消卡住的旧任务，再提交新任务。

## 常用命令速查

```bash
lpstat -d                              # 默认打印机
lpstat -e                              # 打印机名称列表
lpstat -p                              # 打印机状态
lpoptions -p "<printer>" -l            # 支持的纸张/颜色/质量选项
lp -d "<printer>" -o media=A4 -o ColorModel=Gray "<file>"
lpstat -W not-completed -o "<printer>" # 未完成任务
cancel "<job-id>"                      # 取消任务
```
