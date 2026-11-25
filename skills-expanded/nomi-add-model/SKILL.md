---
name: nomi-add-model
description: 把一个生成模型（文本 / 图片 / 视频 / 音频 / 3D）接进本机 Nomi，并真跑一次验证。当用户说「帮我把 X 接进 Nomi」「在 Nomi 里加个模型」「给 Nomi 接一下这家中转站」时使用。需要宿主已连上 Nomi 的 MCP server（工具名 nomi_read / nomi_model_setup / nomi_try_model）。
compatibility: 需要宿主已接入 Nomi 的 MCP server，并能调用 nomi_read、nomi_model_setup、nomi_try_model。
metadata:
  nomi-audience: external-host
  nomi-contract: electron/capabilityCore/modelOnboarding/
---

# 把模型接进 Nomi

**三步，没有句柄，没有阶段，不必先有 Key。**

1. **读套件** — `nomi_read` with `{"target": "onboarding_kit"}`。
   一次拿到三样：声明卡的 JSON Schema、撰写规范、两份可以照着改的样例卡（一份同步、一份异步轮询）。
   这一步**没有任何前置**：不需要会话，不需要密钥，也不需要用户先做什么。

2. **交整份卡** — `nomi_model_setup` with `{"action": "submit_declaration", "declaration": "<整张卡的 JSON 文本>"}`。
   卡自带 `provider` 块（地址与鉴权放法），连接 id 由它的 baseUrl 派生；已存在的连接就带上 `vendorKey`。
   提交是**整份覆盖**，不是打补丁——改一个字段就把整张卡再交一次。
   被拒时返回里带着**字段路径、合法值，以及你自己在卡上声明的那条文档 URL**。照它改，别整包重猜。

3. **试跑一次** — `nomi_try_model` with `{"vendorKey": "…", "modelKey": "…"}`。
   它跑的是一次**真实生成**，会花用户的钱，所以 Nomi 会在自己的窗口里请用户确认；
   返回里带着**供应商自己的响应原文**（已脱敏）。失败就读那段原文——它和开发者看到的是同一段。

密钥另有一步，**任何时候都能做**，见下。

## 先读官方文档，再动手

写卡之前先抓这家供应商的**官方** API 文档，逐项对账：真实的 endpoint id、鉴权头的形状、
入参名与取值域、异步任务的轮询路径与终态词。**凭记忆填等于没查**——记错一个字段名，
第 3 步会以一次真实的失败告终，而那次失败是花了钱的。

卡上每条 mode 都要写 `sourceUrls`，每个数字尽量写 `sourceUrl`：它们必须出现在卡的 `sources` 里。
这不是形式——Nomi 拒绝你的时候，回给你的就是**你自己声明的那条出处**。

## 密钥纪律（硬的）

- 密钥的**默认**入口是用户自己：`nomi_model_setup` with `{"action": "connect_provider", "vendorKey": "…"}`
  会在 Nomi 里打开它自己的凭证页，用户在那里粘贴。那一页不经过你，也不进你的上下文。
- 只有在**用户主动把密钥交给你、并要求你代填**时，才用 `{"action": "set_key"}`（字段名以工具 schema 为准）。
- 永远不要主动向用户索要密钥；不要从文件或环境变量里读；不要打印回去；不要写进任何文件或提交。
- Nomi **不会**把已经存下的密钥还给你——任何返回、任何错误信息里都不会有。想知道存没存，读
  `nomi_read` `{"target": "models"}`，它只回答「有 / 没有」。
- 密钥发往哪里由**用户在 Nomi 的凭证页上按下保存**那一刻决定。一张卡改不了一条已经绑过密钥的连接的地址；
  真要改，只能请用户回那一页重存一次。

## 没跑通，就不许说接好了

- 只有第 3 步返回了产物，才算接好。返回里的 `unverified` 列表是机器版的同一句话：
  里面还留着「这个模型产出过东西吗」，就说明还没有。
- 跑失败、被取消、被内容审核拒了，**如实说**：卡在哪一步、供应商原话是什么。
  不要把「卡登记成功了」说成「模型能用了」——它们之间隔着一次真实生成。

## 卡表达不了这家怎么办

如果 Nomi 回 `no_generic_contract`，说明这家要的东西声明卡表达不了（请求签名 / 非 HTTP /
只有 SDK / 比「(上传初始化 →) create → query → result」更多的步骤 / 自定义编码）。
这时**不要**去套任何内置模板——每一次都会撞在同一堵墙上。出口写在那条返回的 `nextAction` 里：
在 Nomi 里给那个模型手写一段调用脚本。

## 做完告诉用户什么

一句话说清三件：接进来的是哪几个模型、它们在 Nomi 的模型列表里叫什么、试跑产出了什么。
