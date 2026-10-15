---
name: bid-init
description: |
  初始化标书项目目录结构和配置文件。
  当开始新的投标项目、需要创建标准工作目录时触发。
  前置条件：无。后续步骤：放入招标文件后执行 /bid-analyze-tender。
  触发关键词：初始化、新建项目、bid init、创建目录、start project。
---

# 初始化标书项目

运行 [init.py](scripts/init.py)，在当前工作目录下创建项目结构。

## 完成后

初始化完成后，提示用户：

1. 将招标文件（md格式）放入 `inputs/tender/` 目录
2. 然后执行 `/bid-analyze-tender` 开始解析招标文件
