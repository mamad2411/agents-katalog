---
name: daily
description: 生成今日工作日报。仅在用户显式触发 /daily 时执行，不自动运行。
disable-model-invocation: true
argument-hint: [可选补充说明，如"支付模块联调卡住了"]
allowed-tools: Bash, Write, Read, Glob
---

# /daily — 生成今日工作日报

按以下步骤依次执行，不要跳过任何步骤。

---

## 第一步：采集今日工作记录

今日日期通过 Bash 获取：

```bash
date +%Y-%m-%d
```

使用 Glob 工具查找 `~/docs/[TODAY]/*.md`，这些是 /done skill 生成的会话知识文档。

然后使用 Read 工具逐个读取所有找到的文件。

如果今天没有任何 /done 记录文件，告知用户今天没有可用的工作记录，建议先执行 /done 整理会话后再生成日报。

---

## 第二步：归纳生成日报

从文档中提炼工作内容。

归纳规则：
- 将相关联的工作合并（同一方向的多次会话归为一条）
- 最终 2 到 5 条
- 每条一句话，简短直白
- 不写项目名（不写前缀）
- 不写具体数字（不写"147个文件"、"43个调用方"）
- 不写具体技术名词（不写类名、方法名、框架版本号）
- 只描述做了什么事，用最通俗的话说
- 如果用户通过 $ARGUMENTS 提供了补充说明，融入对应板块

内容板块：
1. 「今日工作：」— 必填
2. 「需要协助：」— 可选，有则写，无则不写
3. 「计划变更：」— 可选，有则写，无则不写

好的日报示例：

```
今日工作：
1. 完成接口时区统一改造
2. 测试环境基础设施迁移
3. 数据映射层规范化重构
```

坏的日报示例（不要这样写）：

```
今日工作：
1. igx-cloud: 自定义 DateTimeScalar 替换 ExtendedScalars.DateTime，统一 GraphQL/REST 时间输出为带时区偏移的 ISO 8601
2. igx-cloud: 移除 TestContainers，改用 docker-compose.test.yml 驱动测试，Redis 从单机升级为 Valkey 集群模式
3. igx-cloud: 8 个业务 DTO 从 record 迁移为 @Value @Builder，创建 9 个 MapStruct Mapper
```

---

## 第三步：写入文件

先创建目录：

```bash
mkdir -p ~/docs/reports/$(date +%Y-%m-%d)
```

使用 Write 工具将日报写入 `~/docs/reports/[TODAY]/report-daily-[TODAY].txt`。

格式要求：
- 纯文本，不用任何 markdown 标记
- 每条用数字编号（1. 2. 3.）
- 板块之间空一行
- 没有内容的可选板块直接省略
- 不加日期、作者、页眉页脚
- 简洁直白，像在群聊里发消息

---

## 第四步：输出确认

完成后输出：

```
日报已生成：~/docs/reports/[TODAY]/report-daily-[TODAY].txt
```

并将日报内容完整展示给用户，方便直接复制粘贴到群聊。
