---
name: hunt-mobile-bridge
description: 移动端桥接专项：连接 WebView/deep link/JS bridge 与自有 APK/测试设备的安全边界；用于 app link、WebView、Cordova/React Native 或 mobile API 信号。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-mobile-bridge

## 0. Engagement Gate

- 只在记录了授权、锁定 scope、host/身份态 baseline 后执行；先用主入口确认此路线进入本轮候选。
- 只使用自有账户、对象、域名、回调和可回滚测试数据；WAF、验证码、超时和单次异常均为 `INCONCLUSIVE`。
- 固定节奏为 `baseline → 单变量 probe → post-baseline → oracle → evidence`。第三方资产、共享用户、生产副作用或超出书面窗口时立即停止。

## 1. Trigger Signals

`mobile_deep_link`、`webview_bridge`、`javascript_interface`、`cordova_marker`、`react_native_marker`、`mobile_api_endpoint`。

## 2. Preconditions / Discovery

确认 APK、测试设备、package、deep link domain、bridge 方法和身份态均归属测试环境。Web 页面发现的 mobile endpoint 先做 scope/ownership 标签。

## 3. Minimal Safe Validation

用自有 APK 和模拟器，在 no-op deep link/bridge action 上比较 scheme、origin、参数验证与调用权限；需要原生行为时按 APK board 的攻击网和 MCP recipe 取证。

## 4. Oracle / False Positives

有效：非预期的自有 origin/URL/参数可触发受保护 bridge 或跨 app 数据边界，且设备日志/应用审计证实。单纯 scheme 可打开、崩溃、客户端提示不成立。

## 5. Stop / Evidence / Routing

停止：真实设备数据、其他 app、安装未知 APK、敏感 intent/文件访问。保存 APK hash/package、设备/bridge logs、URL、pre/post state。原生分析转 APK reverse board，API 授权转 `hunt-idor`/`hunt-api-misconfig`。
