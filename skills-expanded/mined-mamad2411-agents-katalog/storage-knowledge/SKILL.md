---
name: storage-knowledge
description: 当在 Golang 中使用 BytedGORM 访问 RDS/MySQL、goredis 访问 Redis/Abase、mongo-go-driver 访问 Bytedoc/MongoDB、tos-sdk-go 访问 TOS、eventbus/client-go 访问 EventBus、inf/sarama 或 tmq/kafka-client 访问 BMQ、rocketmq-go-proxy 访问 RocketMQ、toutiao/elastic 访问 ByteES、bytegraph_gremlin_go 访问 ByteGraph、gopkg/bytekv 访问 ByteKV、或viking_go_client 访问 VikingDB 时使用。
user-invocable: false
---

# Golang 存储访问 SDK 知识库

本知识库提供字节内部常用存储服务 SDK 的使用指南，帮助开发者快速接入各类存储服务。

## RDS (BytedGORM)

关系型数据库服务，基于 MySQL 协议。

**使用场景**：
- 业务数据持久化存储
- 事务性数据操作
- 复杂查询需求

[rds.md](./rds.md) - RDS SDK 使用指南

## Redis (goredis)

高性能缓存和键值存储服务。

**使用场景**：
- 数据缓存
- 分布式锁
- 会话管理
- 计数器/排行榜

[redis.md](./redis.md) - Redis SDK 使用指南

## Bytedoc (mongo-go-driver)

文档型数据库服务，兼容 MongoDB 协议。

**使用场景**：
- 灵活 schema 的数据存储
- 文档型数据模型
- 快速迭代的业务需求

[bytedoc.md](./bytedoc.md) - Bytedoc SDK 使用指南

## Abase (goredis)

字节内部分布式 KV 存储服务。

**使用场景**：
- 大规模 KV 数据存储
- 高吞吐量读写场景
- 海量数据存储

[abase.md](./abase.md) - Abase SDK 使用指南

## TOS (Object Storage)

字节跳动对象存储服务。

**使用场景**：
- 图片/视频等非结构化数据存储
- 大数据分析底层存储
- 数据备份与归档

[tos.md](./tos.md) - TOS SDK 使用指南

## EventBus (eventbus/client-go)

字节内部分布式消息中间件平台。

**使用场景**：
- 异步任务解耦
- 最终一致性事件传递
- 削峰填谷
- 延迟消息/定时任务
- 有序事件流处理

[eventbus.md](./eventbus.md) - EventBus SDK 使用指南

## BMQ&Kafka (inf/sarama, tmq/kafka-client)

字节内部自主研发的高性能消息队列服务，与Kafka协议兼容。

**使用场景**：
- 高吞吐量的离线及近线业务
- 服务间异步通信
- 数据流处理
- 日志收集与分发
- 事件驱动架构

[bmq.md](./bmq.md) - BMQ SDK 使用指南

## RocketMQ (rocketmq-go-proxy)

字节内部高可用、低延迟的消息队列服务。

**使用场景**：
- 高可用/低延迟的线上业务场景
- 交易/支付系统等对消息可靠性以及消息事务要求较高的业务场景
- 异步任务处理的异步消息场景

[rocketmq.md](./rocketmq.md) - RocketMQ SDK 使用指南

## ByteES

字节内部基于Elasticsearch的搜索和分析引擎服务。

**使用场景**：
- 全文检索类应用
- 结构化查询需求
- 时序（日志）类数据存储与分析
- POI类地理位置检索
- 向量检索类应用
- 高安全性场景需求

[bytees.md](./bytees.md) - ByteES SDK 使用指南

## ByteGraph (bytegraph_gremlin_go)

字节自研的分布式图数据存储系统，支持有向属性图数据模型和 Gremlin 图数据库语言。

**使用场景**：
- 图结构数据存储和查询
- 多跳关系查询需求
- 社交网络关系分析
- 推荐系统图计算
- 知识图谱构建

[bytegraph.md](./bytegraph.md) - ByteGraph SDK 使用指南

## ByteKV (bytekv)

分布式事务性键值数据库，提供强一致性保证。

**使用场景**：
- 高数据一致性要求的场景
- 元数据管理（如文件目录、文件元信息）
- 金融数据管理等需要强一致性的业务
- 需要多Key更新原子性的场景

[bytekv.md](./bytekv.md) - ByteKV SDK 使用指南

## VikingDB (viking_go_client)

向量数据库服务，提供近似最近邻（ANN/KNN）向量检索能力。

**使用场景**：
- 推荐、搜索、广告系统
- 图片/音视频等多模态检索
- RAG（检索增强生成）应用
- 向量相似度搜索

[vikingdb.md](./vikingdb.md) - VikingDB SDK 使用指南
