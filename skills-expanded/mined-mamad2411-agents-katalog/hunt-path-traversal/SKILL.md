---
name: hunt-path-traversal
description: 路径遍历专项：验证下载、预览、静态代理、归档提取和文件处理接口的路径规范化、根目录与符号链接边界；只使用自有 marker 文件，不读取系统或用户文件。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-path-traversal

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；只使用预建的自有目录树、marker 和可回滚对象。
- 每轮固定 `baseline → 单路径语义差分 → post-baseline → 权威 marker oracle → evidence`；超时、WAF、错误页、文件名回显和单次 2xx 均是 `INCONCLUSIVE`。
- 不读取 `/etc`、应用配置、其他用户文件、运行时文件系统或外部存储；缺少受控目录 fixture、清理能力或隔离存储时停止。

## 1. Trigger Signals

`file_path_input`、`download_parameter`、`static_file_proxy`、`file_preview_path`、`archive_extract`、`path_normalization_hint`、`symlink_handling_hint`。

## 2. Preconditions / Discovery

建立允许根目录、允许文件名格式、URL/下载参数、归档解压根、重定向/编码处理与存储隔离的 baseline。准备 `allowed/` 与 `outside-controlled/` 两个自有目录及不同 hash marker；符号链接测试仅在自有隔离目录预置。

## 3. Minimal Safe Validation

每次仅比较一个语义：合法相对路径、规范化、父级段、绝对路径、编码或受控 symlink。请求只引用自有 marker；以独立下载/预览结果、文件 hash 或服务端审计确认返回对象。归档仅使用小型无害 fixture，完成后清理。

## 4. Oracle / False Positives

有效：应用可重复返回、覆盖、预览或访问 `outside-controlled/` 内的自有 marker，且响应 hash/审计证明不是缓存或静态路由伪像。`404`、路径回显、异常堆栈、客户端拼接的 URL、CDN fallback 和未知文件错误不成立。

## 5. Stop / Evidence / Routing

停止：任何真实系统/用户/配置文件、共享存储、无法清理的归档、批量路径字典或越界 host。保存目录树、marker hash、单变量请求 shape、pre/post response、审计和清理记录。服务端 include/template loader 转 `hunt-lfi`；上传类型/存储转 `hunt-file-upload`；仅在已有执行 primitive 后转 `hunt-rce`。