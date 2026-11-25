---
name: metricx-knowledge
description: 当需要为Go服务添加监控打点、使用metricx库进行metrics上报时使用，包括但不限于使用code.byted.org/gopkg/metricx库的时候。
user-invocable: false
---

# metricx 知识库

metricx是字节跳动内部的Go语言监控打点库，提供预定义Metric Model的集中管理方式，支持多Metric输出源，能够高效、高质量地进行metrics上报。它底层默认依赖metrics v3，同时通过配套Lint避免metrics v3可能遇到的误用问题，让打点代码更加规范和易于维护。

## 快速入门

metricx的核心设计理念是通过预定义Metric Model来集中管理所有打点，这为代码生成提供了清晰的模板结构。快速入门需要了解以下几个关键方面：

- **Metric Model定义**：如何通过结构体定义来组织不同类型的metrics
- **初始化配置**：metricx.MustInit的基本使用和选项配置
- **基础打点类型**：Counter、Timer、Gauge等基本打点方法
- **标签管理**：静态tags和动态tnames的使用方式

**使用场景**：
- 新服务首次添加监控打点
- 了解metricx的基本设计理念
- 快速实现基础metrics上报功能

[quick-start.md](./quick-start.md) - 快速入门指南

## 打点类型与使用

metricx支持多种打点类型，每种类型对应不同的监控场景和统计需求：

- **Counter**：用于累积值统计，对应metrics v3的Measurer.IncrCounter
- **RateCounter**：用于单位时间累积值统计，对应metrics v3的Measurer.Inc
- **Gauge**：记录瞬时值，对应metrics v3的Measurer.Store
- **Timer**：记录耗时，会计算min/max/avg/sum/count/分位值，对应metrics v3的Measurer.Observe
- **Histogram**：直方图类型打点

**使用场景**：
- 根据业务需求选择合适的打点类型
- 理解不同打点类型的统计特性
- 设计合理的监控指标体系

[metric-types.md](./metric-types.md) - 打点类型详解

## 字段标签与配置

metricx通过结构体字段标签来定义metric的元信息，这是代码生成的重要依据：

- **metric标签**：定义metric name后缀，如`metric:"dbread.throughput"`
- **prefix标签**：用于嵌套结构体，为结构体内字段统一加前缀
- **tags标签**：定义静态键值对，适用于tag键值均已知的情况
- **tnames标签**：定义预定义tag name，允许打点时动态传入对应的value

**使用场景**：
- 设计Metric Model的结构
- 配置metric的命名和标签策略
- 处理静态和动态标签的组合使用

[field-tags.md](./field-tags.md) - 字段标签配置

## 最佳实践与示例

metricx提供了丰富的使用示例和最佳实践，帮助开发者避免常见问题：

- **DB+缓存打点场景**：展示如何为数据库操作和缓存命中设计metrics
- **同时上报metrics和influxdb**：配置多输出源的示例
- **全局标签配置**：通过WithGlobalTags添加环境信息标签
- **耗时单位调整**：使用WithTimeUnit自定义Timer的单位

**使用场景**：
- 参考实际业务场景的实现示例
- 学习多存储上报的配置方法
- 了解环境标签的最佳实践

[best-practices.md](./best-practices.md) - 最佳实践指南

## 高级功能与选项

metricx提供了一系列选项来满足高级使用需求：

- **WithFactories**：配置上报的目标存储，支持同时向多个Factory打点
- **WithNamespace**：自定义metric name前缀，覆盖默认的env.PSM()
- **WithTimeUnit**：调整Timer的耗时单位，如time.Nanosecond
- **默认行为**：了解metrics和influxdb输出的默认配置差异

**使用场景**：
- 定制化metricx的配置
- 实现特殊的监控需求
- 理解库的默认行为以便正确使用

[advanced-options.md](./advanced-options.md) - 高级选项配置