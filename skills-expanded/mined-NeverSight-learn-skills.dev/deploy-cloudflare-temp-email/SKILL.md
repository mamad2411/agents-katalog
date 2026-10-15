---
name: deploy-cloudflare-temp-email
description: 部署临时邮箱服务
---

# 概述

基于开源项目[cloudflare_temp_email](https://github.com/dreamhunter2333/cloudflare_temp_email) 和 cloudflare 账号部署临时邮箱服务

## 何时使用

当人类搭档明确部署新的临时邮箱服务, 或者对已经部署的临时邮箱服务进行更改,修复时使用.

## 方法

确保 git clone 了cloudflare_temp_email源码到本地后根据项目内的文档进行进行部署

**关键文档**

- [quick-start](https://github.com/dreamhunter2333/cloudflare_temp_email/blob/main/vitepress-docs/docs/zh/guide/quick-start.md)

- [Cloudflare Worker 后端](https://github.com/dreamhunter2333/cloudflare_temp_email/blob/main/vitepress-docs/docs/zh/guide/cli/worker.md)

- [Cloudflare Pages 前端](https://github.com/dreamhunter2333/cloudflare_temp_email/blob/main/vitepress-docs/docs/zh/guide/cli/pages.md)

- [初始化/更新 D1 数据库](https://github.com/dreamhunter2333/cloudflare_temp_email/blob/main/vitepress-docs/docs/zh/guide/cli/d1.md)

- 其他情况根据最新文档和源码进行解决.

## 账号配置

- 通常本机环境变量配置了 CLOUDFLARE_API_TOKEN 环境变量以及其他需要的环境变量, 

## 要求

- 如果缺少相关资源必须向你的人类搭档反映情况,而不是硬着头皮做.
- 完成任务后主动向你的人类搭档告知详情,特别是使用方式.
- 编写独立完整的报告文件记录你这次工作的过程和成果.

