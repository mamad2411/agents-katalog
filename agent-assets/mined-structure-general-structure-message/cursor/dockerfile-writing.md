---
description: |
triggers:
  - 写 Dockerfile
  - Docker 化
  - 容器化
  - 写 dockerfile
  - dockerize
  - 容器化部署
role: devops
priority: high
category: ci
stack: _common
alwaysApply: false
---


# Dockerfile 编写

> 按生态双模板生成 Dockerfile。**MUST 含健康检查、时区、三件套**。

## 前置条件

- 已确定服务类型（后端 / 前端）
- 已确定基础镜像版本

## 执行步骤

### 第 1 步：确定服务类型

**MUST 询问用户**：

```
Q1: 服务类型？
    a) 后端 Spring Boot
    b) 前端（Vue / React / 静态站点）

Q2: JDK 版本（后端）？
    默认：21（structure-projects 当前主线）
    备选：17

Q3: 端口？
    默认：后端 8080，前端 80
```

### 第 2 步：生成对应模板

#### 后端 Spring Boot

按 `wiki/_common/docker.md` 模板 A 生成：
- `Dockerfile`
- `liveness.sh`（健康检查脚本）

#### 前端 Nginx

按 `wiki/_common/docker.md` 模板 B 生成：
- `Dockerfile`
- `nginx.template`

### 第 3 步：生成 .dockerignore

```
.git
.gitignore
.github/
node_modules/
dist/
target/
*.md
.idea/
.vscode/
.DS_Store
*.log
coverage/
docs/
changes/
wiki/
```

### 第 4 步：本地验证

```bash
# 构建镜像
docker build -t test-image:v1 .

# 运行容器
docker run -d -p 8080:8080 --name test test-image:v1

# 检查健康
docker ps  # 看 STATUS 列
docker logs test

# 清理
docker stop test && docker rm test
```

## 关键约束（MUST 遵守）

- ✅ **MUST** 使用 `alpine` 变体
- ✅ **MUST** 设置时区 `TZ=Asia/Shanghai`
- ✅ **MUST** 配置 `HEALTHCHECK`
- ✅ **MUST** 用 `ENTRYPOINT` 而非 `CMD`
- ✅ **MUST** 清理包管理器缓存
- ❌ **MUST NOT** 在 Dockerfile 里做 `mvn package` / `npm install`
- ❌ **MUST NOT** 硬编码环境配置

## 产出物

- Dockerfile
- liveness.sh（后端）
- nginx.template（前端）
- .dockerignore

## 完成标准

- Dockerfile 语法正确
- 本地构建成功
- 容器运行健康检查通过

## 关联

- 后续：`docker-compose-design` / `ci-pipeline-design`
- Wiki：`wiki/_common/docker.md`
