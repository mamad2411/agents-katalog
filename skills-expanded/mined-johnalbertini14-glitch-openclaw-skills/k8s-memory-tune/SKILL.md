# K8s JVM 内存调优

**触发词**: oomkilled, memory_limit, jvm_heap, container_memory, k8s 内存

## 问题
K8s Pod 被 OOMKilled，JVM 内存 limit 设置不合理

## 解决方案
1. 使用 MaxRAMPercentage 动态计算堆大小
2. 容器感知内存监控
3. 峰值流量预警

```yaml
# JVM 参数
-XX:+UseCGroupMemoryLimitForHeap
-XX:MaxRAMPercentage=75.0
```
