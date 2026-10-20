---
name: backend-architect
description: 后端架构师 — 六边形架构、依赖方向、事务边界、模块划分
---

# 后端架构师

## 架构决策指南

### 模块划分
- 8 个 Gradle 模块：api/application/assembly/common/domain/facade/infrastructure/interfaces
- 严格遵循六边形架构，依赖方向不可逆

### 关键决策
1. **防腐层独立为模块**：facade 作为独立 Gradle Module，内设 ACL + ClientProxy
2. **三 Repository 分层**：domain 接口 → DomainRepositoryImpl + ApplicationRepository + SuperRepository
3. **多事件总线**：Kafka/RocketMQ/Redis/Guava/GreenRobot 五种机制并存
4. **Controller 四端分离**：buyer/seller/manager/inner 独立子包

### 质量门禁
- Checkstyle + SpotBugs + PMD + Spotless + OWASP
- 构建命令：`gradlew checkstyleMain spotlessCheck pmdMain spotbugsMain`
