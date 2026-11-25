---
name: hunt-upload-execution
description: 上传到服务端执行边界专项：在隔离实例中确认上传对象是否会进入解释器、模板或任务执行边界；不上传 webshell、脚本或可执行 payload，只有独立 no-op marker 才可进入 RCE 链路复核。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-upload-execution

## 0. Engagement Gate

- 仅在授权、scope、上传 baseline、隔离执行窗口、书面批准与可审计服务端同时具备时执行；本 Skill 不授权上传 webshell、脚本、宏或任意可执行内容。
- 只接受平台预置或服务端提供的无害 execution marker；不得构造解释器语法、命令、网络回连、文件读写、持久化或后渗透动作。
- 固定执行 `baseline → 单一存储/handler 边界对照 → post-baseline → server audit oracle → evidence`；没有服务端审计时结论只能是 `INCONCLUSIVE`。

## 1. Trigger Signals

`file_upload`、`upload_execution_candidate`、`upload_public_url`、`upload_path_disclosed`、`interpreter_mapping_hint`、`server_side_transform`、`upload_handler_audit_hint`。

## 2. Preconditions / Discovery

确认上传字段、服务器重命名、存储与公开 URL、下载 handler、转换 worker、扩展名/MIME policy 及其与解释器/模板/任务处理器的边界。必须有专用隔离实例、服务端 audit、预置 no-op marker、清理记录和独立批准；普通上传成功不满足前置条件。

## 3. Minimal Safe Validation

先比较普通无害文件在下载/预览/转换链路中的 handler 与 audit；如平台提供预置 marker，仅以该 marker 的受控引用验证“是否进入执行边界”。不上传含代码的文件，也不把文件名、MIME 或路径绕过当成执行证据。每轮结束后删除测试对象并重做 baseline。

## 4. Oracle / False Positives

有效：隔离服务端 audit 可重复证明预置 no-op marker 被指定解释器/worker 实际处理，且预期下载/预览 baseline 可排除缓存、客户端渲染或仅文件存储。公开 URL、Content-Type、文件扩展名、错误栈、上传 2xx、WAF 或扫描器命中均不成立。

## 5. Stop / Evidence / Routing

停止：需要上传任何脚本/webshell/宏、修改 handler/.htaccess/配置、访问真实文件、共享 worker 或无审计证据。保存上传/存储/handler mapping、审批、marker audit、pre/post baseline、删除记录和影响边界。只有该 primitive 连同隔离与 evidence 满足 `hunt-rce` 的全部条件时，才转 `hunt-rce`；否则停在链路复核。