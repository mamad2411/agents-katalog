---
name: figma-ios-design-token-mapping
description: >-
  Map Figma colors and fonts from the data package into Swift via configurable
  JSON maps under .cursor/bindings/. Hit → emit mapped code snippet; miss →
  UIKit fallback. Use when generating color or font code from design.json.
---

# 颜色 / 字体：映射表优先，未命中走标准 UIKit

> **权威配置**：`.cursor/bindings/color_map.json`、`.cursor/bindings/font_map.json`  
> 示例包（MK）：`.cursor/bindings/examples/mk/`  
> 说明：`.cursor/bindings/README.md`  
> 本 skill **不**写死任何设计系统类名；宿主 token 只活在映射 JSON 的 value 里。

## 核心规则（强制）

```
Figma 颜色/字体
  → 查 bindings 对应 map
  → 命中：原样输出 map 里的代码片段
  → 未命中：用同文件 fallback 模板（标准 UIKit）
```

禁止：
- ❌ 无视映射表手写未在 map 中的宿主 API / 臆造 token
- ❌ 映射未命中时编造不存在的设计系统 API
- ❌ 把映射 value 再「翻译」一遍（value 已是最终代码）

---

## 1. 颜色

### 数据来源

`design.json[node_id].fills[].color`（已是 `rgba(r,g,b,a)` 字符串）。  
**TEXT 文字色也在 `fills[].color`**（`text` 字段只是文案字符串，**没有** `text.color`）。  
评论色变更：`comments.json` 中 `confidence>=medium` 且含 `color` / `color_correction` 的评论优先于节点 fills（阶段 1 **不**把颜色写进 `design.json`，与 iconfont 回写不同）。

### 查表步骤

1. 读 `.cursor/bindings/color_map.json`
2. 用节点颜色按以下 key **依次尝试**（命中即停）：
   - 数据包原文，如 `rgba(255,255,255,0.9)`
   - 规范化：`rgba(r,g,b,1)` / `rgba(r,g,b,0.9)`（alpha=1 不写 `.0`）
   - hex：`#FFFFFF` 或带 alpha `#FFFFFFE6`
   - 旧式元组：`255,255,255,0.9`
3. **命中** → 输出 `map[key]`（本仓示例如 `MKUIStyle.mk_c12()`）
4. **未命中** → 用 `fallback`，替换占位符：

| 占位符 | 含义 |
|--------|------|
| `{r}` `{g}` `{b}` | 0–255 整数 |
| `{a}` | 0–1 透明度 |

默认 fallback：

```swift
UIColor(red: {r}/255.0, green: {g}/255.0, blue: {b}/255.0, alpha: {a})
```

### 映射文件形状

```json
{
  "schema_version": "1.0.0",
  "fallback": "UIColor(red: {r}/255.0, green: {g}/255.0, blue: {b}/255.0, alpha: {a})",
  "map": {
    "#FFFFFF": "MKUIStyle.mk_c12()",
    "rgba(255,255,255,0.9)": "MKUIStyle.mk_c12_90()"
  }
}
```

`map` 为空 = 全部走 UIKit（适合个人开发者）。  
接入宿主色板：把「色值 → 一段 Swift 代码」写入 `map`，或从 `examples/mk/` 复制后按需改。详见 [bindings/README](../../bindings/README.md)。

---

## 2. 字体

### 数据来源

`design.json[node_id].font`（含 `family` / `style` 或 weight / `size`）与 `text`。

### 查表步骤

1. 读 `.cursor/bindings/font_map.json`
2. 构造 key（与 `examples/mk` 的 font_map 一致）：`{family},{Weight},{size}`  
   例：`PingFang SC,Medium,14`  
   亦尝试：`{family}|{Weight}|{size}`
3. **命中** → 输出 `map[key]`（本仓示例如 `MKUIStyle.mk_f14_m()`）
4. **未命中** → 用 `fallback`：

| 占位符 | 含义 |
|--------|------|
| `{font_name}` | PostScript 名（如 `PingFangSC-Medium`），无则用 family |
| `{size}` | 字号 |
| `{family}` `{weight}` | 原始字段 |

默认 fallback：

```swift
UIFont(name: "{font_name}", size: {size}) ?? UIFont.systemFont(ofSize: {size})
```

### 映射文件形状

```json
{
  "schema_version": "1.0.0",
  "fallback": "UIFont(name: \"{font_name}\", size: {size}) ?? UIFont.systemFont(ofSize: {size})",
  "map": {
    "PingFang SC,Medium,14": "MKUIStyle.mk_f14_m()"
  }
}
```

---

## 3. 自定义

| 场景 | 做法 |
|------|------|
| 个人 / 无设计系统 | 保持 `map: {}`，只用 fallback |
| 使用示例包 | `cp .cursor/bindings/examples/mk/*.json .cursor/bindings/` 后按需改 |
| 自建设计系统 | 按「一个色值/字体 → 一段代码」填自己的 `map` |

旧路径 `skills/figma-ios-design-token-mapping/legacy_*.json` 仅作历史备份；**阶段 2 只认 `.cursor/bindings/`**。

---

## 自检

- [ ] 颜色/字体都先查了 bindings map
- [ ] 命中项与 map value **逐字一致**（未再包装）
- [ ] 未命中走 fallback，未编造宿主 API
- [ ] 未在 skill 或代码里写死另一套色表
