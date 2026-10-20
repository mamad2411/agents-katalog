---
name: operate-through-channels
description: |
  通过正确渠道修复，不绕过架构抽象层。
  修代码不修数据 / 通过公开接口操作 / 验证必须端到端 / 修完重启验证。
  触发词：docker exec、进入容器、容器内直接操作、直接改数据库、手动改 DB、绕过业务逻辑、
  修数据不修代码、docker exec -it、kubectl exec、shell 进容器、直接改表、绕过 API。
---

# Operate Through Channels — 通过正确渠道修复

> 问题的根在代码，就在代码里修；根在配置，就改配置重启。
> 不要因为「改数据结果一样」就绕过架构层直接动手。

## 触发条件

容器化应用排障、数据库数据异常、API 返回错误、爬虫/定时任务不执行、微服务链路中断
——以及任何涉及 AI 绕过分层架构「走捷径」的场景。

## 三条铁律

### 1. 修代码不修数据

数据不对 → 说明代码有路径未覆盖 → 找到那条路径并修复 → 重新跑让数据自然产生。

**❌ 错误**（AI 最常见的捷径）：
```python
# 爬虫没跑，数据库里没有数据 → 直接 INSERT 一条
# "数据有了，问题解决了"
```

**✅ 正确**：
```python
# 定位爬虫为什么不跑 → 修复 bug → 重启容器 → 等待数据自然流入
```

| 现象 | ❌ AI 倾向 | ✅ 正确做法 |
|------|-----------|-----------|
| 数据缺失 | 手动 INSERT 补数据 | 修代码 → 重跑产生数据 |
| 数据状态错误 | UPDATE 修正状态 | 查代码逻辑 → 修 bug → 自然流转 |
| 关联数据不一致 | 手动 sync | 定位原子性漏洞 → 加事务/补偿 |

**验证方法**：数据是否通过**用户操作或定时任务的自然流程**进入系统？是从前端点一下能复现吗？不能 → 说明数据是"假"的，问题其实没解决。

---

### 2. 通过公开接口操作

对容器：用 Docker API、Portainer、Docker Compose、K8s API，不用 `docker exec` shell 进去。
对服务：调 REST API / gRPC / Message Queue，不直接连数据库写 SQL。
对配置：改配置文件 → 重启/热加载，不用 `exec` 进去 `sed`。

**❌ 错误**：
```bash
docker exec -it crawler-container bash
# 进去改代码、手动跑脚本、直接删数据库记录
```

**✅ 正确**：
```bash
# 方式 A：通过 Docker API 重启（最轻量）
curl -X POST http://docker-host:2375/containers/crawler-container/restart

# 方式 B：通过 Compose 重建
docker compose up -d --build crawler-service

# 方式 C：热更新（如果支持）
curl -X POST http://crawler-service:8080/-/reload
```

| 抽象层 | ❌ 绕过方式 | ✅ 正确渠道 |
|--------|-----------|-----------|
| 容器 | `docker exec` shell 进入 | Docker API / Compose / K8s API |
| 数据库 | 直连 SQL client | 业务 API 端点 / ORM Repository |
| 配置 | exec 进去 `sed` 改文件 | 挂载 ConfigMap / `.env` 重载 |
| 消息队列 | 直连 `redis-cli`/`rabbitmqctl` | 业务 API 触发 / Admin UI |

---

### 3. 验证必须端到端

不查数据库来证明"数据有了"，要通过业务前端或 API 看到数据回流。

**❌ 错误验证**：
```bash
# 直接查数据库确认
docker exec -it postgres psql -c "SELECT * FROM crawler_results"
# "有数据了，OK"
```

**✅ 正确验证**：
```bash
# 方式 A：调业务 API 确认
curl http://api-server:8080/api/v1/crawler/stats

# 方式 B：前端浏览器验证
# playwright: 打开管理页面 → 导航到数据看板 → 确认展示正常

# 方式 C：业务日志确认
docker logs crawler-container --tail 20
```

**为什么重要**：数据库有数据不代表前端能正常展示、不代表下次增量跑正确、不代表业务链路通。
只有端到端验证能确认**整条链路**是健康的。

---

## 检查清单

排障时逐项确认，**禁止跳步**：

- [ ] 我先定位了代码根因（不是数据表象），带「文件:行号」
- [ ] 我没有直接操作数据库（INSERT/UPDATE/DELETE）
- [ ] 我没有 `docker exec` 或 `kubectl exec` 进容器
- [ ] 我通过 Docker API / Compose / 编排工具控制容器生命周期
- [ ] 我通过业务 API 或前端验证了修复效果（不是查 DB）
- [ ] 修复后数据是自然产生的，可以从前端操作复现
