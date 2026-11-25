---
name: china-cloud-cdn-deploy
description: "国内云服务器与 CDN 部署：选内地节点（阿里云/腾讯云/华为云）、可备案的服务器规格、Docker/Nginx 部署、HTTPS、CDN 加速区域与备案关系、境外依赖（Google Fonts、npm、Docker Hub、OpenAI）在内地不可用的替换。Use when deploying an agent-built app to mainland China, configuring CDN for China, or debugging 'works abroad but slow/blocked in China'."
---

# 国内云服务器与 CDN 部署 · Mainland Cloud & CDN Deploy

> 属于 [golive-china-skills](https://github.com/xianyu110/golive-china-skills)。核对日期：2026-10-04。**规则会变，本文不是法律意见。**

**English summary:** Deploy to a mainland region the right way: buy a server that qualifies for ICP filing, deploy with Docker/Nginx + HTTPS, put a China CDN in front only after filing, and strip out foreign dependencies (Google Fonts/Analytics, reCAPTCHA, foreign CDNs, OpenAI/Anthropic APIs) that fail or are slow from inside China. This is the most automatable skill in the pack.

## 关键规则（已核对）

- **服务器要能备案**：以阿里云为例，备案需中国内地节点、包年包月且购买时长累计满 3 个月；ECS 需公网带宽，按量付费需先转包年包月，免费试用不能备案；轻量应用服务器同理。[^ali-server]
- **CDN 与备案**：阿里云 CDN 加速区域选"仅中国内地"或"全球"时，加速域名**必须已完成 ICP 备案**（可在其他接入商备案）；选"全球（不包含中国内地）"则不需要。备案刚完成可能有数据延迟。[^ali-cdn]
- 腾讯云、华为云规则相近但细节不同，以对应文档为准。⚠️ 价格、配额经常调整，本 skill **不写价格**。

## 前置条件

- [ ] 已确定备案主体与域名（`domain-realname-dns`）
- [ ] 云账号已实名（个人或企业）
- [ ] 应用可容器化（Dockerfile）或有构建产物

## 步骤

1. **依赖体检（agent，强烈建议先做）**：扫描代码与构建链，列出内地访问可能失败或很慢的依赖，并给替换方案：

| 境外依赖 | 常见替换思路 |
|---|---|
| Google Fonts / Google Analytics / reCAPTCHA | 字体自托管；国内统计（如百度统计）或自建；国内验证码服务 |
| 公共 CDN（jsDelivr/unpkg/cdnjs） | 打包进产物或放自己的 OSS/COS + CDN |
| Docker Hub / npm / PyPI / GitHub Releases | 云厂商镜像仓库、npm/PyPI 国内镜像、构建在 CI 完成后推镜像 |
| OpenAI / Anthropic API | 见 `llm-api-in-china`（官方不支持中国内地区域） |
| 境外 OAuth（Google/GitHub 登录） | 增加手机号/微信登录 |

2. **选地域与机型（human 决定，agent 建议）**：用户在哪就选哪（华北/华东/华南）；先按"可备案条件"买。
3. **备案期间（agent）**：可先在服务器上用 IP + 自签证书做内部测试；对外开放以备案通过为准（`icp-beian`）。
4. **部署（agent）**：安全组只放行 80/443/22（22 限制来源 IP）；Docker Compose + Nginx 反代；systemd 或 compose `restart: unless-stopped`。
5. **HTTPS（agent）**：云厂商证书或 ACME；开启 HTTP→HTTPS 跳转、HSTS（确认所有子域都已 HTTPS 再开）。
6. **对象存储 + CDN（agent，备案后）**：静态资源放 OSS/COS；CDN 加速区域选"中国内地"；回源 HTTPS；配置缓存规则与 Referer 防盗链。
7. **验证（agent）**：从内地网络（或云拨测）检查首屏、证书、回源；`curl -w "%{time_total}"` 记录。
8. **继续**：公安备案（`gongan-beian`）、隐私政策（`pipl-privacy-policy`）。

## 检查清单

- [ ] 服务器满足可备案条件（内地节点、包年包月时长达标）
- [ ] 前端无 Google Fonts / 境外公共 CDN / 境外统计脚本残留
- [ ] 安全组最小开放；SSH 禁密码登录
- [ ] HTTPS 全站，证书自动续期
- [ ] CDN 仅在域名备案后添加，加速区域与备案状态匹配
- [ ] 日志与用户数据存储在内地（如涉及个人信息出境，见 `pipl-privacy-policy`）
- [ ] 备份与监控（云监控告警、数据库快照）

## 常见失败原因与修复

| 现象 | 修复 |
|---|---|
| CDN 添加域名报"未备案" | 先完成 ICP 备案，或等待备案数据同步后再添加[^ali-cdn] |
| 备案提交提示服务器不满足条件 | 转包年包月/续费到满 3 个月；免费试用实例不能用[^ali-server] |
| 内地用户白屏/很慢 | 去除 Google Fonts 等境外资源 |
| 域名被接入商拦截提示"未备案" | 未备案域名解析到内地服务器会被拦截，先备案 |
| 镜像拉取失败 | 使用云厂商容器镜像服务 |

## Agent 能做 vs 人必须做

| Agent | 人 |
|---|---|
| 依赖体检与替换 PR | 购买服务器/CDN、付款、选择地域 |
| 写 Dockerfile/compose/Nginx/证书脚本 | 云账号实名、授权 AccessKey（最小权限） |
| 配置安全组、CDN、缓存规则（经授权） | 对数据存储位置、出境做合规决策 |
| 拨测与性能报告 | 备案相关提交 |

## 官方来源

[^ali-server]: 阿里云 ICP 备案前的服务器及接入信息确认 https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-server-access-information-check
[^ali-cdn]: 阿里云 使用阿里云 CDN 加速域名的 ICP 备案要求 https://help.aliyun.com/zh/icp-filing/basic-icp-service/product-overview/use-alibaba-cloud-cdn

另见：阿里云 CDN 添加加速域名 https://help.aliyun.com/zh/cdn/add-a-domain-name

> ⚠️ 免责声明：本文不是法律意见；云厂商规则、价格与配额经常调整，以控制台和官方文档为准。
