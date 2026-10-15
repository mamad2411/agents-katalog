---
name: "jeesite"
description: "JeeSite快速开发平台文档总索引。Invoke when user asks about JeeSite documentation, or when the topic doesn't clearly match a single sub-skill."
---

# JeeSite 文档 Skills 集合

JeeSite 快速开发平台文档 Skills 集合，供 AI Agent 检索和调用。

## 文档获取方式

按需缓存，有效期3天。优先从本地缓存读取，缓存过期或不存在时自动下载并转换为 Markdown：

- **缓存目录**: `references/.cache/<skill-name>/`（权限不足时自动回退到 `~/.cache/jeesite/<skill-name>/`）
- **按需缓存**: `python3 scripts/cache_docs.py --skill <skill-name> --permalink <permalink>`
- **强制更新**: `python3 scripts/cache_docs.py --skill <skill-name> --permalink <permalink> --force`

## Skills 列表

| Skill name     | 名称      | 说明                                        |
|----------------|---------|-------------------------------------------|
| quick-start    | 快速了解    | 平台简介、架构特点、技术选型、功能介绍等基础知识                  |
| backend-dev    | 后端开发手册  | 安装部署、代码生成、DAO、数据权限、Shiro等后端开发指南           |
| frontend-vue   | Vue前端手册 | Vue前端CRUD、表单、表格、组件、权限等前端开发指南              |
| frontend-beetl | 经典前端手册  | Beetl视图、Form、DataGrid、JS框架等经典前端开发指南       |
| extend-fun     | 扩展功能专题  | BPM工作流、AI相关、CMS、SSO、OAuth2、定时任务、对象存储等扩展功能 |
| cloud-arch     | 云服务技术架构 | SaaS、集群、微服务、分布式事务等云服务架构                   |
| support        | 技术支持与服务 | 技术支持服务、版本区别、联系方式                          |

## 路由策略

1. 根据用户问题，匹配上表中最相关的 Skill name
2. 加载对应 `references/<name>/SKILL.md` 获取详细文档映射
3. 根据文档映射表定位具体文档，获取 permalink
4. 执行缓存命令：`python3 scripts/cache_docs.py --skill <name> --permalink <permalink>`
   - 若缓存有效（3天内），直接返回缓存文件路径
   - 若缓存过期或不存在，自动下载并转换为 Markdown 保存
5. 使用 Read 工具读取缓存文件
6. 如果用户问题跨多个 Skill，可同时加载多个子 Skill

## 快速路由参考

| 用户问题方向 | 推荐Skill |
|-------------|-----------|
| JeeSite是什么、架构、技术选型、功能介绍 | quick-start |
| 安装部署、代码生成、DAO、MyBatis、Shiro、数据权限 | backend-dev |
| Vue3、前端CRUD、表单、表格、组件、前端权限 | frontend-vue |
| Beetl、DataGrid、经典前端、全栈版 | frontend-beetl |
| BPM工作流、CMS、SSO、OAuth2、消息推送、作业调度 | extend-fun |
| SaaS多租户、集群、微服务、分布式事务、分库分表 | cloud-arch |
| 技术支持、版本区别、联系方式、授权 | support |
