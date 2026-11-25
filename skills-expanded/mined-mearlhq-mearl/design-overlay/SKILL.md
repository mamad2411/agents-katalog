---
name: design-overlay
description: 在 Mearl Popup 中把 SVG、PNG、JPG 设计稿叠加到指定网页，调整锚点、位置、缩放、裁切与混合模式，并进行截图像素差异对比。适用于设计还原检查；不用于修改网页业务内容。
install:
  description: 安装并注册设计稿对比工具箱插件
  command: npx @mearl/setup plugin "$SKILL_DIR"
version: "3.1.0"
---

# 设计稿对比

在网页上叠加 SVG、PNG、JPG 设计稿，调整位置与裁切，再对比当前视口的像素差异。命令必须显式传入当前浏览器的 `tabId`；先用 `tabs` 确认目标。

```bash
mearl overlay tabs
mearl overlay --payload '{"command":"import","input":{"tabId":123,"filePath":"/tmp/design.png"}}'
mearl overlay --payload '{"command":"state","input":{"tabId":123}}'
mearl overlay --payload '{"command":"update","input":{"tabId":123,"settings":{"selector":"#content","opacity":0.5,"blendMode":"difference"}}}'
mearl overlay --payload '{"command":"compare","input":{"tabId":123,"diffPath":"/tmp/design-diff.png"}}'
mearl overlay --payload '{"command":"clear","input":{"tabId":123}}'
```

- `import` 读取执行宿主上的设计稿并应用到网页，单份最多 16 MiB，保留已有显示设置。`apply` 可复用当前标签页会话内的 `assetId`；接收 `tabId`、`assetId` 和可选 `pixelRatio`。
- `update` 的 `settings` 可设置元素锚点 `selector`、位移 `offsetX/offsetY`、透明度 `opacity`（0–1）、缩放 `scale`（0.1–3）、像素密度 `pixelRatio`（1–4）、裁切 `cropTop/cropRight/cropBottom/cropLeft`、`visible`、`locked`、`followScroll` 和 `blendMode`。截图设计稿应按设备像素密度设置 `pixelRatio`。
- `compare` 返回差异像素数、总像素数、比例、尺寸及差异图资源。需要查看或交付差异图时传 `diffPath`，在执行宿主保存 PNG。只比较设计稿与当前可见视口的交集；截图要求目标仍是其窗口的活动标签页。
- 素材和设置按浏览器会话隔离，素材和配置按标签页、业务框架以及网页 origin + pathname 关联，在执行宿主内存中缓存，`state` 可读取或恢复覆盖层。扩展连接使用用户脚本隔离环境；未开启「允许用户脚本」或缺少站点权限时，按宿主指引授权后重试。

用户可从 Popup 工具箱打开「设计稿对比」，粘贴、拖入或选择设计稿，并通过拖拽、裁切和鼠标选点调整覆盖层。打开工具会读取当前网页的覆盖层。鼠标选点及截图资源读取仅供工具页面使用。页面实例与会话缓存由宿主后台管理，Popup 关闭后仍保存拖拽、裁切和锚点变化；当前网页路径的会话激活规则在刷新后恢复覆盖层。关闭浏览器、重载扩展或重启执行宿主后，素材与配置可以丢失，需要重新导入。临时比较资源保留最多 15 分钟，导入分块最多 10 分钟；应用中的设计稿与配置缓存最长 7 天，替换和清除设计稿时释放旧素材。用户通过 `diffPath` 导出的文件保留。
