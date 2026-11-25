---
name: figma-ios-iconfont-mapping
description: >-
  Map iconfont nodes from design.json[node].iconfont into Swift via
  .cursor/bindings/iconfont_map.json. Hit → emit mapped font/text snippets;
  miss → fallback + TODO. Use when generating icon/button code from iconfont nodes.
---

# Iconfont：映射表优先，未命中走 fallback

> **权威配置**：`.cursor/bindings/iconfont_map.json`  
> 示例包（MK）：`.cursor/bindings/examples/mk/iconfont_map.json`  
> 颜色仍走 [figma-ios-design-token-mapping](../figma-ios-design-token-mapping/SKILL.md)（查 `color_map.json`）。  
> 本 skill **不**写死宿主 iconfont 类名；调用约定只活在 `iconfont_map.json` 里。

## 核心规则（强制）

```
design.json[node].iconfont.symbol
  → 查 bindings/iconfont_map.json 的 map
  → 命中：用 map 里的 font / text（可替换 {size}）
  → 未命中：用 fallback + TODO 注释（禁止臆造 OC 属性名）
```

---

## 数据来源

`figma-ios-preload-data` 已识别 iconfont 并写入 `design.json[node_id].iconfont`：

```json
{
  "symbol": "icon_query_24",
  "size_hint": 24,
  "color": "rgba(255,255,255,1)",
  "rotation": 90.0,
  "source": "comment"
}
```

| 字段 | 用法 |
|------|------|
| `symbol` | **查表 key**（已含评论修正） |
| `size_hint` | 替换 map/fallback 里的 `{size}`；缺失则用 `min(frame.w, frame.h)` |
| `color` | 走 color_map（见颜色 skill） |
| `rotation` | 有且 \|deg\|≥1 时加 `transform`；评论要求不旋转则忽略 |

> 若数据包仍带旧字段 `lib_hint` / `objc_property` / `font_call`：**忽略**。阶段 1 已不再写入；**生成以 `iconfont_map.json` 为准**。

`source`：`explicit` / `implicit` / `comment`（阶段 1 已处理评论覆盖，阶段 2 直接用 `symbol`）。

## 集合容器

`_role.is_iconfont_library == true`（如 `iconfont_24`）**自身不渲染**，跳过。

---

## 查表步骤

1. 读 `.cursor/bindings/iconfont_map.json`
2. 用 `iconfont.symbol` 查 `map`
3. **命中** →

```swift
label.font = <map.font>    // 替换 {size}
label.text = <map.text>
label.textColor = <color_map 查 iconfont.color 的结果>
```

4. **未命中** → 输出 `fallback.comment`（替换 `{symbol}`），再用 `fallback.font` / `fallback.text`；**禁止**编造 `MKIconFont.shared().mk_xxx`

### 映射文件形状

```json
{
  "schema_version": "1.0.0",
  "fallback": {
    "font": "UIFont.systemFont(ofSize: {size})",
    "text": "\"?\"",
    "comment": "// TODO(阶段2): iconfont `{symbol}` 未在 iconfont_map.json 命中"
  },
  "map": {
    "icon_query_24": {
      "font": "MKIconFont.iconFont(withSize: 24)",
      "text": "MKIconFont.shared().mk_icon_query_24"
    },
    "icon_next_12": {
      "font": "MKIconFont.iconFont(withSize: {size})",
      "text": "MKIconFont.shared().mk_icon_next_12"
    }
  }
}
```

`map` 为空 = 全部走 fallback（个人开发者）。  
接入宿主 iconfont：从 `examples/mk/iconfont_map.json` 复制后改，或按「一个 symbol → font/text 两段代码」自建。详见 [bindings/README](../../bindings/README.md)。

---

## 旋转

```swift
// 仅当 iconfont.rotation 存在且评论未禁止旋转
icon.transform = CGAffineTransform(rotationAngle: CGFloat(rotation) * .pi / 180)
```

评论含「不要旋转 / 保持原始方向」且 `confidence>=medium` → 忽略 `rotation`。

---

## 生成模板（示意）

命中 map 后：

```swift
// Figma node: I1:407;2:7337  iconfont/icon_query_24
let queryIcon = UILabel()
queryIcon.font = MKIconFont.iconFont(withSize: 24)           // map.font
queryIcon.text = MKIconFont.shared().mk_icon_query_24       // map.text
queryIcon.textColor = /* color_map 查 iconfont.color；未命中则 UIColor fallback */
```

按钮同理：`titleLabel?.font` + `setTitle(_:for:)` 使用同一对 font/text。

未命中：

```swift
// TODO(阶段2): iconfont `icon_unknown_24` 未在 iconfont_map.json 命中
let icon = UILabel()
icon.font = UIFont.systemFont(ofSize: 24)
icon.text = "?"
```

---

## 自检

- [ ] 渲染的 iconfont 均来自 `design.json[node].iconfont`
- [ ] `iconfont_library` 已跳过
- [ ] symbol 先查了 `iconfont_map.json`
- [ ] 命中项 font/text 与 map **一致**
- [ ] 未命中有 TODO，未臆造属性名
- [ ] 颜色走 color_map，未另写死色表
